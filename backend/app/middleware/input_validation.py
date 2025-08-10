"""
Input validation middleware with security-focused request sanitization
"""

import re
import json
import logging
from typing import Dict, Any, List, Optional, Union
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.config_loader import get_security_config, SecurityConfig

logger = logging.getLogger(__name__)


class InputSanitizer:
    """Sanitizes and validates input data based on security configuration"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        
        # Common XSS patterns
        self.xss_patterns = [
            re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL),
            re.compile(r'javascript:', re.IGNORECASE),
            re.compile(r'on\w+\s*=', re.IGNORECASE),
            re.compile(r'<iframe[^>]*>.*?</iframe>', re.IGNORECASE | re.DOTALL),
            re.compile(r'<object[^>]*>.*?</object>', re.IGNORECASE | re.DOTALL),
            re.compile(r'<embed[^>]*>', re.IGNORECASE),
            re.compile(r'vbscript:', re.IGNORECASE),
            re.compile(r'data:text/html', re.IGNORECASE)
        ]
        
        # SQL injection patterns
        self.sql_patterns = [
            re.compile(r'\bunion\s+select\b', re.IGNORECASE),
            re.compile(r'\bselect\s+.*\bfrom\b', re.IGNORECASE),
            re.compile(r'\bdrop\s+table\b', re.IGNORECASE),
            re.compile(r'\bdelete\s+from\b', re.IGNORECASE),
            re.compile(r'\binsert\s+into\b', re.IGNORECASE),
            re.compile(r'\bupdate\s+.*\bset\b', re.IGNORECASE),
            re.compile(r'[\'";](\s*or\s*1\s*=\s*1|\s*or\s*true)', re.IGNORECASE),
            re.compile(r'--\s*$', re.MULTILINE)
        ]
        
        # Path traversal patterns
        self.path_traversal_patterns = [
            re.compile(r'\.\./', re.IGNORECASE),
            re.compile(r'\.\.\\', re.IGNORECASE),
            re.compile(r'%2e%2e%2f', re.IGNORECASE),
            re.compile(r'%2e%2e\\', re.IGNORECASE)
        ]
    
    def _detect_xss(self, text: str) -> bool:
        """Detect potential XSS attacks"""
        for pattern in self.xss_patterns:
            if pattern.search(text):
                return True
        return False
    
    def _detect_sql_injection(self, text: str) -> bool:
        """Detect potential SQL injection"""
        for pattern in self.sql_patterns:
            if pattern.search(text):
                return True
        return False
    
    def _detect_path_traversal(self, text: str) -> bool:
        """Detect path traversal attempts"""
        for pattern in self.path_traversal_patterns:
            if pattern.search(text):
                return True
        return False
    
    def _sanitize_string(self, text: str) -> str:
        """Sanitize a string by removing dangerous patterns"""
        if not self.config.sanitize_inputs:
            return text
        
        # Remove XSS patterns
        for pattern in self.xss_patterns:
            text = pattern.sub('', text)
        
        # Remove path traversal patterns
        for pattern in self.path_traversal_patterns:
            text = pattern.sub('', text)
        
        # Trim whitespace and limit length
        text = text.strip()
        if len(text) > self.config.max_input_length:
            text = text[:self.config.max_input_length]
        
        return text
    
    def validate_and_sanitize(self, data: Any, path: str = "root") -> tuple[bool, Any, List[str]]:
        """
        Validate and sanitize input data
        Returns: (is_valid, sanitized_data, error_messages)
        """
        errors = []
        
        if isinstance(data, str):
            # Check length
            if len(data) > self.config.max_input_length:
                errors.append(f"{path}: Input too long ({len(data)} > {self.config.max_input_length})")
                return False, data, errors
            
            # Detect attacks
            if self._detect_xss(data):
                errors.append(f"{path}: Potential XSS attack detected")
                logger.warning(f"XSS attempt blocked: {path}")
            
            if self._detect_sql_injection(data):
                errors.append(f"{path}: Potential SQL injection detected")
                logger.warning(f"SQL injection attempt blocked: {path}")
            
            if self._detect_path_traversal(data):
                errors.append(f"{path}: Path traversal attempt detected")
                logger.warning(f"Path traversal attempt blocked: {path}")
            
            if errors:
                return False, data, errors
            
            # Sanitize if enabled
            sanitized = self._sanitize_string(data) if self.config.sanitize_inputs else data
            return True, sanitized, []
        
        elif isinstance(data, dict):
            sanitized_dict = {}
            for key, value in data.items():
                # Validate key
                key_valid, sanitized_key, key_errors = self.validate_and_sanitize(key, f"{path}.{key}")
                if not key_valid:
                    errors.extend(key_errors)
                    continue
                
                # Validate value
                value_valid, sanitized_value, value_errors = self.validate_and_sanitize(value, f"{path}.{key}")
                if not value_valid:
                    errors.extend(value_errors)
                    continue
                
                sanitized_dict[sanitized_key] = sanitized_value
            
            return len(errors) == 0, sanitized_dict, errors
        
        elif isinstance(data, list):
            sanitized_list = []
            for i, item in enumerate(data):
                item_valid, sanitized_item, item_errors = self.validate_and_sanitize(item, f"{path}[{i}]")
                if not item_valid:
                    errors.extend(item_errors)
                    continue
                sanitized_list.append(sanitized_item)
            
            return len(errors) == 0, sanitized_list, errors
        
        elif isinstance(data, (int, float, bool, type(None))):
            # Primitive types are safe
            return True, data, []
        
        else:
            # Unknown type
            errors.append(f"{path}: Unsupported data type: {type(data)}")
            return False, data, errors


class InputValidationMiddleware(BaseHTTPMiddleware):
    """Middleware for validating and sanitizing all input data"""
    
    def __init__(self, app, config: Optional[SecurityConfig] = None):
        super().__init__(app)
        if config is None:
            config = get_security_config()
        
        self.config = config
        self.sanitizer = InputSanitizer(config)
        
        # Endpoints that skip validation (health checks, etc.)
        self.skip_paths = {'/health', '/ping', '/ready', '/docs', '/redoc', '/openapi.json'}
        
        logger.info(f"Input validation middleware initialized - "
                   f"max_length: {config.max_input_length}, "
                   f"sanitize: {config.sanitize_inputs}")
    
    def _should_skip_validation(self, request: Request) -> bool:
        """Check if this request should skip input validation"""
        return request.url.path in self.skip_paths or request.method == "GET"
    
    async def _get_request_body(self, request: Request) -> Optional[Dict[str, Any]]:
        """Safely extract request body"""
        try:
            if request.headers.get('content-type', '').startswith('application/json'):
                body = await request.body()
                if not body:
                    return None
                
                # Check body size
                if len(body) > self.config.max_file_size:
                    raise HTTPException(
                        status_code=413,
                        detail=f"Request body too large: {len(body)} > {self.config.max_file_size}"
                    )
                
                return json.loads(body.decode('utf-8'))
            return None
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in request body")
        except Exception as e:
            logger.error(f"Error reading request body: {e}")
            raise HTTPException(status_code=400, detail="Error processing request body")
    
    async def dispatch(self, request: Request, call_next):
        """Apply input validation to requests"""
        
        # Skip validation for certain endpoints
        if self._should_skip_validation(request):
            return await call_next(request)
        
        # Validate query parameters
        if request.query_params:
            query_dict = dict(request.query_params)
            valid, sanitized_query, errors = self.sanitizer.validate_and_sanitize(query_dict, "query")
            
            if not valid:
                logger.warning(f"Invalid query parameters from {request.client.host}: {errors}")
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": "Invalid query parameters",
                        "details": errors[:5]  # Limit error details
                    }
                )
        
        # Validate request body for POST/PUT/PATCH requests
        if request.method in ["POST", "PUT", "PATCH"]:
            body_data = await self._get_request_body(request)
            
            if body_data is not None:
                valid, sanitized_body, errors = self.sanitizer.validate_and_sanitize(body_data, "body")
                
                if not valid:
                    logger.warning(f"Invalid request body from {request.client.host}: {errors}")
                    return JSONResponse(
                        status_code=400,
                        content={
                            "error": "Invalid request data",
                            "details": errors[:5]  # Limit error details
                        }
                    )
                
                # Store sanitized body for downstream use
                request._sanitized_body = sanitized_body
        
        # Process the request
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error"}
            )


def create_input_validation_middleware(config: Optional[SecurityConfig] = None):
    """Create input validation middleware with configuration"""
    if config is None:
        config = get_security_config()
    
    def middleware_factory(app):
        return InputValidationMiddleware(app, config)
    
    return middleware_factory


# Helper function to get sanitized request body in route handlers
def get_sanitized_body(request: Request) -> Optional[Dict[str, Any]]:
    """Get sanitized request body from middleware"""
    return getattr(request, '_sanitized_body', None)