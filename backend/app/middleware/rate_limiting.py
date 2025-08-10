"""
Rate limiting middleware with environment-specific configuration
"""

import time
import logging
from collections import defaultdict
from typing import Dict, List, Optional
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.config_loader import get_rate_limit_config, RateLimitConfig

logger = logging.getLogger(__name__)


class InMemoryRateLimiter:
    """Simple in-memory rate limiter for development/staging"""
    
    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.cleanup_interval = 60  # Clean up old records every minute
        self.last_cleanup = time.time()
    
    def _cleanup_old_requests(self, current_time: float):
        """Remove requests older than the window"""
        if current_time - self.last_cleanup < self.cleanup_interval:
            return
            
        cutoff_time = current_time - self.config.window_seconds
        for key in list(self.requests.keys()):
            self.requests[key] = [
                req_time for req_time in self.requests[key] 
                if req_time > cutoff_time
            ]
            if not self.requests[key]:
                del self.requests[key]
        
        self.last_cleanup = current_time
    
    def is_allowed(self, identifier: str) -> tuple[bool, Dict[str, int]]:
        """Check if request is allowed and return rate limit headers"""
        current_time = time.time()
        self._cleanup_old_requests(current_time)
        
        # Get requests in the current window
        cutoff_time = current_time - self.config.window_seconds
        recent_requests = [
            req_time for req_time in self.requests[identifier]
            if req_time > cutoff_time
        ]
        
        # Check if we can allow this request
        if len(recent_requests) >= self.config.requests_per_minute:
            # Check if we have burst capacity
            very_recent = [
                req_time for req_time in recent_requests
                if req_time > current_time - 10  # Last 10 seconds
            ]
            if len(very_recent) >= self.config.burst_size:
                return False, {
                    'limit': self.config.requests_per_minute,
                    'remaining': 0,
                    'reset': int(current_time + self.config.window_seconds)
                }
        
        # Allow the request
        self.requests[identifier].append(current_time)
        
        remaining = max(0, self.config.requests_per_minute - len(recent_requests) - 1)
        return True, {
            'limit': self.config.requests_per_minute,
            'remaining': remaining,
            'reset': int(current_time + self.config.window_seconds)
        }


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware with environment-specific configuration"""
    
    def __init__(self, app, config: Optional[RateLimitConfig] = None):
        super().__init__(app)
        if config is None:
            config = get_rate_limit_config()
        
        self.config = config
        self.rate_limiter = InMemoryRateLimiter(config) if config.enabled else None
        
        logger.info(f"Rate limiting {'enabled' if config.enabled else 'disabled'} - "
                   f"Limit: {config.requests_per_minute}/min, Burst: {config.burst_size}")
    
    def _get_identifier(self, request: Request) -> str:
        """Get identifier for rate limiting (IP address or API key)"""
        if self.config.per_ip:
            # Get real IP address (handle proxy headers)
            x_forwarded_for = request.headers.get('X-Forwarded-For')
            if x_forwarded_for:
                return x_forwarded_for.split(',')[0].strip()
            
            x_real_ip = request.headers.get('X-Real-IP')
            if x_real_ip:
                return x_real_ip.strip()
            
            return request.client.host if request.client else 'unknown'
        
        # Could also rate limit by API key if authentication is enabled
        return request.client.host if request.client else 'unknown'
    
    def _should_skip_rate_limiting(self, request: Request) -> bool:
        """Check if this request should skip rate limiting"""
        # Skip rate limiting for health checks
        if request.url.path in ['/health', '/ping', '/ready']:
            return True
        
        # Skip for admin endpoints if they have proper authentication
        # This would be implemented based on your auth system
        
        return False
    
    async def dispatch(self, request: Request, call_next):
        """Apply rate limiting to requests"""
        
        # Skip if rate limiting is disabled
        if not self.config.enabled or not self.rate_limiter:
            return await call_next(request)
        
        # Skip certain endpoints
        if self._should_skip_rate_limiting(request):
            return await call_next(request)
        
        # Check rate limit
        identifier = self._get_identifier(request)
        allowed, headers = self.rate_limiter.is_allowed(identifier)
        
        if not allowed:
            logger.warning(f"Rate limit exceeded for {identifier}: {request.url.path}")
            
            response_headers = {}
            if self.config.include_headers:
                response_headers = {
                    'X-RateLimit-Limit': str(headers['limit']),
                    'X-RateLimit-Remaining': str(headers['remaining']),
                    'X-RateLimit-Reset': str(headers['reset']),
                }
            
            return JSONResponse(
                status_code=429,
                content={
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Limit: {headers["limit"]} per minute',
                    'retry_after': headers['reset'] - int(time.time())
                },
                headers=response_headers
            )
        
        # Process the request
        response = await call_next(request)
        
        # Add rate limit headers to successful responses
        if self.config.include_headers:
            response.headers['X-RateLimit-Limit'] = str(headers['limit'])
            response.headers['X-RateLimit-Remaining'] = str(headers['remaining'])
            response.headers['X-RateLimit-Reset'] = str(headers['reset'])
        
        return response


def create_rate_limit_middleware(config: Optional[RateLimitConfig] = None):
    """Create rate limiting middleware with configuration"""
    if config is None:
        config = get_rate_limit_config()
    
    def middleware_factory(app):
        return RateLimitMiddleware(app, config)
    
    return middleware_factory