"""
Security headers middleware for enhanced protection
"""

import os
import logging
from typing import Optional, Dict, List
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.utils.config_loader import get_security_config, SecurityConfig

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware that adds security headers to all responses"""
    
    def __init__(self, app, config: Optional[SecurityConfig] = None):
        super().__init__(app)
        if config is None:
            config = get_security_config()
        
        self.config = config
        self.environment = os.getenv('ENVIRONMENT', 'development').lower()
        
        # Determine if we're in production
        self.is_production = self.environment == 'production'
        
        logger.info(f"Security headers middleware initialized - "
                   f"environment: {self.environment}, "
                   f"force_https: {config.force_https}, "
                   f"hsts_enabled: {config.hsts_enabled}")
    
    def _get_csp_policy(self) -> str:
        """Get Content Security Policy based on environment"""
        if self.environment == 'development':
            # More permissive for development
            return (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
                "font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data: https:; "
                "connect-src 'self' https://api.openai.com https://api.anthropic.com; "
                "frame-src 'none'; "
                "object-src 'none'; "
                "base-uri 'self'"
            )
        else:
            # Strict policy for production/staging
            return (
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data: https:; "
                "connect-src 'self' https://api.openai.com https://api.anthropic.com; "
                "frame-src 'none'; "
                "object-src 'none'; "
                "base-uri 'self'; "
                "form-action 'self'; "
                "frame-ancestors 'none'"
            )
    
    def _get_permissions_policy(self) -> str:
        """Get Permissions Policy header"""
        # Disable potentially dangerous features
        policies = [
            "geolocation=()",
            "microphone=()",
            "camera=()",
            "magnetometer=()",
            "gyroscope=()",
            "speaker=()",
            "vibrate=()",
            "fullscreen=(self)",
            "payment=()"
        ]
        return ", ".join(policies)
    
    def _should_add_security_headers(self, request: Request) -> bool:
        """Determine if security headers should be added"""
        # Skip for static files and API docs in development
        skip_paths = {'/docs', '/redoc', '/openapi.json'}
        if not self.is_production and request.url.path in skip_paths:
            return False
        
        return True
    
    def _get_security_headers(self, request: Request, response: Response) -> Dict[str, str]:
        """Get all security headers for the response"""
        headers = {}
        
        # X-Content-Type-Options
        headers["X-Content-Type-Options"] = "nosniff"
        
        # X-Frame-Options
        headers["X-Frame-Options"] = "DENY"
        
        # X-XSS-Protection (legacy but still useful for older browsers)
        headers["X-XSS-Protection"] = "1; mode=block"
        
        # Referrer Policy
        headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Content Security Policy
        if self.config.csp_enabled:
            headers["Content-Security-Policy"] = self._get_csp_policy()
        
        # Strict Transport Security (HTTPS only)
        if self.config.hsts_enabled and self.config.force_https:
            if self.is_production:
                # 1 year for production
                headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
            else:
                # Shorter for staging
                headers["Strict-Transport-Security"] = "max-age=86400; includeSubDomains"
        
        # Permissions Policy
        headers["Permissions-Policy"] = self._get_permissions_policy()
        
        # Cross-Origin Embedder Policy
        headers["Cross-Origin-Embedder-Policy"] = "require-corp"
        
        # Cross-Origin Opener Policy  
        headers["Cross-Origin-Opener-Policy"] = "same-origin"
        
        # Cross-Origin Resource Policy
        headers["Cross-Origin-Resource-Policy"] = "same-origin"
        
        # Server header removal/obfuscation
        headers["Server"] = "Dynamic-Survey-API"
        
        # Cache control for sensitive endpoints
        if any(sensitive in request.url.path for sensitive in ['/admin', '/api/', '/internal']):
            headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            headers["Pragma"] = "no-cache"
            headers["Expires"] = "0"
        
        # Security metadata for monitoring
        headers["X-Security-Level"] = "high" if self.is_production else "medium"
        headers["X-Environment"] = self.environment
        
        return headers
    
    def _check_https_redirect(self, request: Request) -> Optional[Response]:
        """Check if HTTPS redirect is needed"""
        if not self.config.force_https:
            return None
        
        # Skip for health checks and local development
        if request.url.path in {'/health', '/ping'} or request.client.host in {'127.0.0.1', 'localhost'}:
            return None
        
        # Check if request is already HTTPS
        if request.url.scheme == 'https':
            return None
        
        # Check X-Forwarded-Proto header (for load balancers)
        forwarded_proto = request.headers.get('X-Forwarded-Proto')
        if forwarded_proto == 'https':
            return None
        
        # Redirect to HTTPS
        https_url = request.url.replace(scheme='https')
        logger.info(f"Redirecting to HTTPS: {request.url} -> {https_url}")
        
        return Response(
            content=f"Redirecting to HTTPS: {https_url}",
            status_code=301,
            headers={"Location": str(https_url)}
        )
    
    async def dispatch(self, request: Request, call_next):
        """Apply security headers to responses"""
        
        # Check for HTTPS redirect
        if self.config.force_https:
            https_redirect = self._check_https_redirect(request)
            if https_redirect:
                return https_redirect
        
        # Process the request
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            # Even for errors, add basic security headers
            response = Response(
                content="Internal Server Error",
                status_code=500,
                headers={"X-Content-Type-Options": "nosniff"}
            )
        
        # Add security headers
        if self._should_add_security_headers(request):
            security_headers = self._get_security_headers(request, response)
            
            for header_name, header_value in security_headers.items():
                response.headers[header_name] = header_value
            
            # Remove potentially leaky headers
            headers_to_remove = ["X-Powered-By", "Server"]
            for header in headers_to_remove:
                if header in response.headers:
                    del response.headers[header]
                    
            # Override server header
            response.headers["Server"] = "Dynamic-Survey-API"
        
        return response


def create_security_headers_middleware(config: Optional[SecurityConfig] = None):
    """Create security headers middleware with configuration"""
    if config is None:
        config = get_security_config()
    
    def middleware_factory(app):
        return SecurityHeadersMiddleware(app, config)
    
    return middleware_factory