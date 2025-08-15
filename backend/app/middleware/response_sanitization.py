"""
Response sanitization middleware to prevent data leakage and ensure secure output
"""

import json
import logging
from typing import Dict, Any, List, Optional, Set
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.utils.config_loader import get_security_config, SecurityConfig

logger = logging.getLogger(__name__)


class ResponseSanitizer:
    """Sanitizes response data to prevent information leakage"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        
        # Sensitive fields to remove from responses
        self.sensitive_fields = {
            # Database fields
            'password', 'passwd', 'pwd', 'secret', 'token', 'key', 'api_key',
            'private_key', 'secret_key', 'auth_token', 'access_token',
            'refresh_token', 'session_id', 'csrf_token',
            
            # Internal system fields
            'id', 'internal_id', 'uuid', 'guid', '_id', 
            'created_by', 'updated_by', 'deleted_by',
            'internal_notes', 'admin_notes', 'debug_info',
            
            # Configuration and environment
            'config', 'env', 'environment', 'settings',
            'database_url', 'db_url', 'connection_string',
            
            # Personal identifiable information
            'ssn', 'social_security', 'tax_id', 'credit_card', 
            'bank_account', 'routing_number',
            
            # System paths and errors
            'file_path', 'directory', 'stack_trace', 'traceback',
            'error_detail', 'exception_detail'
        }
        
        # Fields to mask instead of remove (show partial data)
        self.mask_fields = {
            'email': lambda x: self._mask_email(x),
            'phone': lambda x: self._mask_phone(x),
            'credit_card': lambda x: self._mask_credit_card(x),
            'ip_address': lambda x: self._mask_ip(x)
        }
        
        # Allowed fields for different environments
        # In development (auth disabled) or production (auth enabled), allow admin fields
        self.allowed_admin_fields = {
            'id', 'client_id', 'question_id', 'created_at', 'updated_at', 'status', 'internal_id'
        }
    
    def _mask_email(self, email: str) -> str:
        """Mask email address: user@domain.com -> u***@d***.com"""
        if '@' not in email:
            return email
        local, domain = email.split('@', 1)
        if '.' not in domain:
            return email
        domain_name, domain_ext = domain.rsplit('.', 1)
        return f"{local[0]}***@{domain_name[0]}***.{domain_ext}"
    
    def _mask_phone(self, phone: str) -> str:
        """Mask phone number: +1234567890 -> +123***7890"""
        if len(phone) < 7:
            return phone
        return phone[:3] + '***' + phone[-4:]
    
    def _mask_credit_card(self, cc: str) -> str:
        """Mask credit card: 1234567890123456 -> ****-****-****-3456"""
        if len(cc) < 8:
            return cc
        return '****-****-****-' + cc[-4:]
    
    def _mask_ip(self, ip: str) -> str:
        """Mask IP address: 192.168.1.100 -> 192.168.*.***"""
        parts = ip.split('.')
        if len(parts) != 4:
            return ip
        return f"{parts[0]}.{parts[1]}.*.***"
    
    def _should_remove_field(self, key: str, is_admin: bool = False) -> bool:
        """Determine if a field should be removed"""
        key_lower = key.lower()
        
        # Always remove highly sensitive fields
        critical_fields = {'password', 'secret', 'token', 'api_key', 'private_key'}
        if any(critical in key_lower for critical in critical_fields):
            return True
        
        # For admin users, allow some internal fields
        if is_admin and key_lower in self.allowed_admin_fields:
            return False
        
        # Remove sensitive fields
        return any(sensitive in key_lower for sensitive in self.sensitive_fields)
    
    def _should_mask_field(self, key: str) -> Optional[str]:
        """Determine if a field should be masked"""
        key_lower = key.lower()
        for mask_field in self.mask_fields:
            if mask_field in key_lower:
                return mask_field
        return None
    
    def sanitize_data(self, data: Any, is_admin: bool = False, path: str = "root") -> Any:
        """Sanitize response data recursively"""
        if isinstance(data, dict):
            sanitized = {}
            for key, value in data.items():
                
                # Check if field should be removed
                if self._should_remove_field(key, is_admin):
                    logger.debug(f"Removed sensitive field: {path}.{key}")
                    continue
                
                # Check if field should be masked
                mask_type = self._should_mask_field(key)
                if mask_type and isinstance(value, str):
                    sanitized[key] = self.mask_fields[mask_type](value)
                    logger.debug(f"Masked field: {path}.{key}")
                else:
                    # Recursively sanitize nested data
                    sanitized[key] = self.sanitize_data(value, is_admin, f"{path}.{key}")
            
            return sanitized
        
        elif isinstance(data, list):
            return [self.sanitize_data(item, is_admin, f"{path}[{i}]") for i, item in enumerate(data)]
        
        elif isinstance(data, str):
            # Limit string length to prevent data leakage
            if len(data) > 10000:  # Large text might contain sensitive info
                return data[:10000] + "... [truncated]"
            return data
        
        else:
            # Return primitive types as-is
            return data
    
    def add_security_metadata(self, data: Dict[str, Any], request: Request) -> Dict[str, Any]:
        """Add security-related metadata to response"""
        if not isinstance(data, dict):
            return data
        
        # Add timestamp for audit trails
        from datetime import datetime
        data['_timestamp'] = datetime.now().isoformat()
        
        # Add sanitization notice for development
        if self.config.sanitize_inputs:
            data['_sanitized'] = True
        
        return data


class ResponseSanitizationMiddleware(BaseHTTPMiddleware):
    """Middleware for sanitizing response data"""
    
    def __init__(self, app, config: Optional[SecurityConfig] = None):
        super().__init__(app)
        if config is None:
            config = get_security_config()
        
        self.config = config
        self.sanitizer = ResponseSanitizer(config)
        
        # Endpoints that skip sanitization
        self.skip_paths = {'/docs', '/redoc', '/openapi.json'}
        
        # Admin endpoints (if authentication is enabled)
        self.admin_paths = {
            '/admin/', '/internal/', '/debug/', 
            '/api/forms', '/api/clients'  # Admin API endpoints
        } if config.auth_enabled else set()
        
        logger.info(f"Response sanitization middleware initialized - "
                   f"sanitize_enabled: {config.sanitize_inputs}, "
                   f"auth_enabled: {config.auth_enabled}")
    
    def _should_skip_sanitization(self, request: Request) -> bool:
        """Check if this request should skip response sanitization"""
        return any(skip_path in request.url.path for skip_path in self.skip_paths)
    
    def _is_admin_request(self, request: Request) -> bool:
        """Check if this is an admin request (simplified - would integrate with auth)"""
        # This would integrate with your authentication system
        # For now, just check path and headers
        
        # Define admin paths for both auth enabled and disabled scenarios
        admin_paths = {
            '/admin/', '/internal/', '/debug/', 
            '/api/forms', '/api/clients'  # Admin API endpoints
        }
        
        # Check if admin path
        is_admin_path = any(admin_path in request.url.path for admin_path in admin_paths)
        
        if not self.config.auth_enabled:
            # In development with auth disabled, treat admin paths as admin requests
            return is_admin_path
        
        # In production with auth enabled, require proper authentication
        if is_admin_path:
            # Check for admin API key (simplified)
            admin_key = request.headers.get('X-Admin-Key')
            has_admin_key = admin_key and len(admin_key) > 10  # Basic validation
            return has_admin_key
        
        return False
    
    async def dispatch(self, request: Request, call_next):
        """Apply response sanitization"""
        
        # Skip sanitization for certain endpoints
        if self._should_skip_sanitization(request):
            return await call_next(request)
        
        # Process the request
        response = await call_next(request)
        
        # Only sanitize JSON responses
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('application/json'):
            return response
        
        try:
            # Get response body
            body = b''
            async for chunk in response.body_iterator:
                body += chunk
            
            if not body:
                return response
            
            # Parse JSON
            try:
                data = json.loads(body.decode('utf-8'))
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON response for sanitization: {request.url.path}")
                return response
            
            # Determine if admin request
            is_admin = self._is_admin_request(request)
            
            # Sanitize data
            sanitized_data = self.sanitizer.sanitize_data(data, is_admin)
            
            # Add security metadata if enabled
            if self.config.sanitize_inputs and isinstance(sanitized_data, dict):
                sanitized_data = self.sanitizer.add_security_metadata(sanitized_data, request)
            
            # Create new response with sanitized data
            return JSONResponse(
                content=sanitized_data,
                status_code=response.status_code,
                headers={
                    key: value for key, value in response.headers.items()
                    if key.lower() not in {'content-length', 'transfer-encoding'}
                }
            )
        
        except Exception as e:
            logger.error(f"Error sanitizing response: {e}")
            # Return original response if sanitization fails
            return response


def create_response_sanitization_middleware(config: Optional[SecurityConfig] = None):
    """Create response sanitization middleware with configuration"""
    if config is None:
        config = get_security_config()
    
    def middleware_factory(app):
        return ResponseSanitizationMiddleware(app, config)
    
    return middleware_factory