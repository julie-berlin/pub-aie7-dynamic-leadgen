"""
Request size limiting and timeout protection middleware
"""

import asyncio
import time
import logging
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.utils.config_loader import get_security_config, SecurityConfig

logger = logging.getLogger(__name__)


class RequestLimitsMiddleware(BaseHTTPMiddleware):
    """Middleware for enforcing request size limits and timeouts"""
    
    def __init__(self, app, config: Optional[SecurityConfig] = None):
        super().__init__(app)
        if config is None:
            config = get_security_config()
        
        self.config = config
        
        # Convert MB to bytes for size limits
        self.max_request_size = config.max_file_size  # Already in bytes
        
        # Timeout tracking
        self.active_requests: Dict[str, float] = {}
        
        # Different size limits for different endpoints
        self.endpoint_limits = {
            '/upload/': config.max_file_size,  # File uploads
            '/api/': config.max_input_length * 10,  # API endpoints (text * 10)
            '/admin/': config.max_file_size // 2,  # Admin endpoints
        }
        
        # Endpoints that get longer timeouts
        self.long_timeout_paths = {
            '/api/survey/process',  # LLM processing
            '/api/analytics',  # Complex queries
            '/admin/reports'  # Report generation
        }
        
        logger.info(f"Request limits middleware initialized - "
                   f"max_size: {self.max_request_size} bytes, "
                   f"timeout: {config.session_timeout}s")
    
    def _get_request_id(self, request: Request) -> str:
        """Generate unique request ID for tracking"""
        return f"{request.client.host if request.client else 'unknown'}:{request.url.path}:{time.time()}"
    
    def _get_size_limit(self, request: Request) -> int:
        """Get size limit for specific endpoint"""
        path = request.url.path
        
        # Check specific endpoint limits
        for endpoint_path, limit in self.endpoint_limits.items():
            if endpoint_path in path:
                return limit
        
        # Default limit
        return self.max_request_size
    
    def _get_timeout_limit(self, request: Request) -> int:
        """Get timeout limit for specific endpoint"""
        path = request.url.path
        base_timeout = 30  # Default 30 seconds
        
        # Longer timeouts for specific endpoints
        if any(long_path in path for long_path in self.long_timeout_paths):
            return base_timeout * 3  # 90 seconds for LLM processing
        
        # Admin endpoints get more time
        if '/admin/' in path:
            return base_timeout * 2  # 60 seconds
        
        return base_timeout
    
    async def _check_request_size(self, request: Request) -> Optional[Response]:
        """Check if request exceeds size limits"""
        if request.method not in ['POST', 'PUT', 'PATCH']:
            return None
        
        # Get content length from headers
        content_length = request.headers.get('content-length')
        if content_length:
            try:
                size = int(content_length)
                limit = self._get_size_limit(request)
                
                if size > limit:
                    logger.warning(f"Request size exceeded: {size} > {limit} bytes from {request.client.host if request.client else 'unknown'}")
                    
                    return JSONResponse(
                        status_code=413,
                        content={
                            "error": "Request too large",
                            "message": f"Request size {size} bytes exceeds limit of {limit} bytes",
                            "limit": limit,
                            "received": size
                        }
                    )
            except ValueError:
                logger.warning(f"Invalid content-length header: {content_length}")
        
        return None
    
    async def _read_body_with_limit(self, request: Request) -> bytes:
        """Read request body with size limit enforcement"""
        limit = self._get_size_limit(request)
        body = b''
        
        async def receive():
            return await request.receive()
        
        while True:
            message = await receive()
            
            if message['type'] == 'http.request':
                chunk = message.get('body', b'')
                if chunk:
                    body += chunk
                    
                    # Check size while reading
                    if len(body) > limit:
                        raise HTTPException(
                            status_code=413,
                            detail=f"Request body too large: exceeds {limit} bytes"
                        )
                
                if not message.get('more_body', False):
                    break
            else:
                break
        
        return body
    
    def _cleanup_active_requests(self):
        """Clean up old request tracking entries"""
        current_time = time.time()
        expired_requests = [
            req_id for req_id, start_time in self.active_requests.items()
            if current_time - start_time > 300  # 5 minutes
        ]
        
        for req_id in expired_requests:
            del self.active_requests[req_id]
    
    async def dispatch(self, request: Request, call_next):
        """Apply request limits and timeouts"""
        
        # Generate request ID for tracking
        request_id = self._get_request_id(request)
        start_time = time.time()
        self.active_requests[request_id] = start_time
        
        try:
            # Check request size limits
            size_check = await self._check_request_size(request)
            if size_check:
                return size_check
            
            # Get timeout for this endpoint
            timeout_limit = self._get_timeout_limit(request)
            
            # Create timeout task
            try:
                response = await asyncio.wait_for(
                    call_next(request),
                    timeout=timeout_limit
                )
                
                # Add timing headers
                execution_time = time.time() - start_time
                response.headers["X-Request-Duration"] = f"{execution_time:.3f}s"
                response.headers["X-Request-Timeout"] = f"{timeout_limit}s"
                
                # Log slow requests
                if execution_time > timeout_limit * 0.8:  # 80% of timeout
                    logger.warning(f"Slow request: {request.url.path} took {execution_time:.3f}s "
                                 f"(timeout: {timeout_limit}s)")
                
                return response
            
            except asyncio.TimeoutError:
                logger.error(f"Request timeout: {request.url.path} exceeded {timeout_limit}s")
                
                return JSONResponse(
                    status_code=504,
                    content={
                        "error": "Request timeout",
                        "message": f"Request took longer than {timeout_limit} seconds",
                        "timeout_limit": timeout_limit,
                        "path": request.url.path
                    },
                    headers={
                        "X-Request-Timeout": f"{timeout_limit}s",
                        "X-Timeout-Reason": "processing_timeout"
                    }
                )
        
        except HTTPException as e:
            # Re-raise HTTP exceptions
            raise e
        
        except Exception as e:
            logger.error(f"Error in request limits middleware: {e}")
            
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "message": "Request processing failed"
                }
            )
        
        finally:
            # Clean up tracking
            if request_id in self.active_requests:
                del self.active_requests[request_id]
            
            # Periodic cleanup
            if len(self.active_requests) > 100:
                self._cleanup_active_requests()
    
    def get_active_requests_count(self) -> int:
        """Get count of currently active requests"""
        self._cleanup_active_requests()
        return len(self.active_requests)
    
    def get_request_stats(self) -> Dict[str, Any]:
        """Get request statistics"""
        self._cleanup_active_requests()
        
        return {
            "active_requests": len(self.active_requests),
            "max_request_size": self.max_request_size,
            "endpoint_limits": self.endpoint_limits,
            "config": {
                "max_file_size": self.config.max_file_size,
                "max_input_length": self.config.max_input_length,
                "session_timeout": self.config.session_timeout
            }
        }


def create_request_limits_middleware(config: Optional[SecurityConfig] = None):
    """Create request limits middleware with configuration"""
    if config is None:
        config = get_security_config()
    
    def middleware_factory(app):
        return RequestLimitsMiddleware(app, config)
    
    return middleware_factory