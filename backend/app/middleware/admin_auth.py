"""
Admin authentication middleware for protected endpoints
"""

import os
import jwt
import time
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Optional, Set, Dict, Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.config_loader import get_security_config, SecurityConfig

logger = logging.getLogger(__name__)


class AdminAuthenticator:
    """Handles admin authentication and authorization"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.jwt_secret = os.getenv('JWT_SECRET', 'dev-secret-key-change-in-production')
        self.admin_api_key = os.getenv('ADMIN_API_KEY', '')
        
        # Rate limiting for auth attempts
        self.auth_attempts: Dict[str, list] = {}
        self.max_attempts = 5
        self.lockout_duration = 300  # 5 minutes
        
        logger.info(f"Admin authentication initialized - "
                   f"auth_enabled: {config.auth_enabled}, "
                   f"admin_key_required: {config.admin_key_required}")
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        x_forwarded_for = request.headers.get('X-Forwarded-For')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        
        x_real_ip = request.headers.get('X-Real-IP')
        if x_real_ip:
            return x_real_ip.strip()
        
        return request.client.host if request.client else 'unknown'
    
    def _is_rate_limited(self, ip: str) -> bool:
        """Check if IP is rate limited for authentication"""
        if ip not in self.auth_attempts:
            return False
        
        current_time = time.time()
        # Clean old attempts
        self.auth_attempts[ip] = [
            attempt_time for attempt_time in self.auth_attempts[ip]
            if current_time - attempt_time < self.lockout_duration
        ]
        
        return len(self.auth_attempts[ip]) >= self.max_attempts
    
    def _record_auth_attempt(self, ip: str):
        """Record failed authentication attempt"""
        if ip not in self.auth_attempts:
            self.auth_attempts[ip] = []
        
        self.auth_attempts[ip].append(time.time())
        logger.warning(f"Failed admin auth attempt from {ip} (attempt {len(self.auth_attempts[ip])})")
    
    def _verify_api_key(self, api_key: str) -> bool:
        """Verify admin API key"""
        if not self.admin_api_key:
            logger.warning("ADMIN_API_KEY not configured")
            return False
        
        # Use constant-time comparison to prevent timing attacks
        return hashlib.sha256(api_key.encode()).hexdigest() == \
               hashlib.sha256(self.admin_api_key.encode()).hexdigest()
    
    def _verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            
            # Check expiration
            if payload.get('exp', 0) < time.time():
                return None
            
            # Validate that token has required fields
            if not payload.get('user_id') or not payload.get('client_id'):
                return None
            
            return payload
        
        except jwt.InvalidTokenError:
            return None
    
    def _generate_jwt_token(self, user_id: str, role: str = 'admin') -> str:
        """Generate JWT token for admin user"""
        payload = {
            'user_id': user_id,
            'role': role,
            'iat': time.time(),
            'exp': time.time() + (self.config.jwt_expire_minutes * 60)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def authenticate_request(self, request: Request) -> tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Authenticate admin request
        Returns: (is_authenticated, error_message, user_info)
        """
        ip = self._get_client_ip(request)
        
        # Check rate limiting
        if self._is_rate_limited(ip):
            return False, "Too many failed authentication attempts. Try again later.", None
        
        # Get authentication credentials
        api_key = request.headers.get('X-Admin-Key')
        auth_header = request.headers.get('Authorization', '')
        jwt_token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else None
        
        # Try API key authentication first
        if api_key:
            if self._verify_api_key(api_key):
                logger.info(f"Admin authenticated via API key from {ip}")
                return True, None, {'auth_method': 'api_key', 'ip': ip}
            else:
                self._record_auth_attempt(ip)
                return False, "Invalid API key", None
        
        # Try JWT token authentication
        if jwt_token:
            payload = self._verify_jwt_token(jwt_token)
            if payload:
                logger.info(f"Admin authenticated via JWT from {ip}")
                return True, None, {
                    'auth_method': 'jwt',
                    'user_id': payload.get('user_id'),
                    'role': payload.get('role'),
                    'ip': ip
                }
            else:
                self._record_auth_attempt(ip)
                return False, "Invalid or expired token", None
        
        # No valid authentication found
        self._record_auth_attempt(ip)
        return False, "Authentication required", None


class AdminAuthMiddleware(BaseHTTPMiddleware):
    """Middleware for admin authentication on protected endpoints"""
    
    def __init__(self, app, config: Optional[SecurityConfig] = None):
        super().__init__(app)
        if config is None:
            config = get_security_config()
        
        self.config = config
        self.authenticator = AdminAuthenticator(config) if config.auth_enabled else None
        
        # Protected admin paths
        self.admin_paths = {
            '/admin/',
            '/internal/',
            '/debug/',
            '/system/',
            '/management/',
            '/api/admin/'  # Add API admin endpoints
        }
        
        # Always protected paths (even if auth is disabled elsewhere)
        self.critical_paths = {
            '/admin/users',
            '/admin/config',
            '/admin/database',
            '/debug/logs',
            '/system/restart'
        }
        
        logger.info(f"Admin auth middleware initialized - "
                   f"protected_paths: {len(self.admin_paths)}, "
                   f"auth_enabled: {config.auth_enabled}")
    
    def _is_protected_path(self, path: str) -> bool:
        """Check if path requires admin authentication"""
        if not self.config.auth_enabled:
            # Even if auth is disabled, protect critical paths
            return any(critical_path in path for critical_path in self.critical_paths)
        
        return any(admin_path in path for admin_path in self.admin_paths)
    
    def _is_critical_path(self, path: str) -> bool:
        """Check if path is always protected regardless of settings"""
        return any(critical_path in path for critical_path in self.critical_paths)
    
    async def dispatch(self, request: Request, call_next):
        """Apply admin authentication to protected endpoints"""
        
        # Check if this path requires authentication
        if not self._is_protected_path(request.url.path):
            return await call_next(request)
        
        # If auth is disabled but this is a critical path, block access
        if not self.config.auth_enabled and self._is_critical_path(request.url.path):
            logger.warning(f"Blocked access to critical path without auth: {request.url.path}")
            return JSONResponse(
                status_code=503,
                content={
                    "error": "Service unavailable",
                    "message": "Admin authentication must be enabled to access this endpoint"
                }
            )
        
        # Skip if authenticator not available
        if not self.authenticator:
            return JSONResponse(
                status_code=503,
                content={
                    "error": "Authentication service unavailable",
                    "message": "Admin authentication is not properly configured"
                }
            )
        
        # Authenticate request
        is_authenticated, error_message, user_info = self.authenticator.authenticate_request(request)
        
        if not is_authenticated:
            logger.warning(f"Unauthorized admin access attempt: {request.url.path} from {user_info.get('ip', 'unknown') if user_info else 'unknown'}")
            
            return JSONResponse(
                status_code=401,
                content={
                    "error": "Unauthorized",
                    "message": error_message,
                    "required_auth": ["X-Admin-Key header", "Authorization: Bearer <jwt_token>"]
                },
                headers={
                    "WWW-Authenticate": "Bearer"
                }
            )
        
        # Add user info to request for downstream use
        request.state.admin_user = user_info
        
        # Process the authenticated request
        try:
            response = await call_next(request)
            
            # Add admin session headers
            response.headers["X-Admin-Session"] = "active"
            response.headers["X-Auth-Method"] = user_info.get('auth_method', 'unknown')
            
            return response
        
        except Exception as e:
            logger.error(f"Error processing admin request: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error"}
            )


def create_admin_auth_middleware(config: Optional[SecurityConfig] = None):
    """Create admin authentication middleware with configuration"""
    if config is None:
        config = get_security_config()
    
    def middleware_factory(app):
        return AdminAuthMiddleware(app, config)
    
    return middleware_factory


# Helper function to get admin user info in route handlers
def get_admin_user(request: Request) -> Optional[Dict[str, Any]]:
    """Get authenticated admin user info from request"""
    return getattr(request.state, 'admin_user', None)


# Helper function to generate admin JWT token (for login endpoints)
def generate_admin_token(user_id: str, config: Optional[SecurityConfig] = None) -> str:
    """Generate JWT token for admin user"""
    if config is None:
        config = get_security_config()
    
    authenticator = AdminAuthenticator(config)
    return authenticator._generate_jwt_token(user_id)