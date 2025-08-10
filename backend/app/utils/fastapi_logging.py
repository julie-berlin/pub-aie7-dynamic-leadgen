"""
FastAPI Standard Logging Configuration

Implements FastAPI best practices for logging:
- Request/response logging middleware
- Structured JSON logging for production
- Request correlation IDs
- Performance metrics
- Error tracking
"""

import logging
import json
import time
import uuid
from typing import Optional, Dict, Any
from datetime import datetime

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message
import uvicorn

# Configure standard Python logging
def setup_fastapi_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """Set up logging configuration for FastAPI application"""
    
    # Create formatters
    console_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    json_formatter = JSONFormatter()
    
    # Configure root logger
    logging.basicConfig(level=getattr(logging, log_level.upper()))
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    
    # Configure loggers
    loggers = [
        "uvicorn.access",
        "uvicorn.error", 
        "fastapi",
        "survey_api",
        "survey_system"
    ]
    
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.addHandler(console_handler)
        logger.setLevel(getattr(logging, log_level.upper()))
        logger.propagate = False
    
    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(json_formatter)
        
        for logger_name in loggers:
            logger = logging.getLogger(logger_name)
            logger.addHandler(file_handler)
    
    print(f"✅ FastAPI logging configured - Level: {log_level}")

class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add any extra fields
        if hasattr(record, 'correlation_id'):
            log_data["correlation_id"] = record.correlation_id
        if hasattr(record, 'session_id'):
            log_data["session_id"] = record.session_id
        if hasattr(record, 'user_id'):
            log_data["user_id"] = record.user_id
        
        return json.dumps(log_data)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and responses with correlation IDs"""
    
    async def dispatch(self, request: Request, call_next):
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())[:8]
        
        # Add to request state
        request.state.correlation_id = correlation_id
        
        # Log request start
        start_time = time.time()
        
        # Get client IP
        client_ip = self._get_client_ip(request)
        
        logger = logging.getLogger("survey_api")
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={
                "correlation_id": correlation_id,
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "client_ip": client_ip,
                "user_agent": request.headers.get("user-agent", "unknown"),
                "event_type": "request_started"
            }
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Log response
            logger.info(
                f"Request completed: {request.method} {request.url.path} - {response.status_code}",
                extra={
                    "correlation_id": correlation_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": round(duration_ms, 2),
                    "client_ip": client_ip,
                    "event_type": "request_completed",
                    "success": response.status_code < 400
                }
            )
            
            # Add correlation ID to response headers
            response.headers["X-Correlation-ID"] = correlation_id
            
            return response
            
        except Exception as e:
            # Calculate duration for error case
            duration_ms = (time.time() - start_time) * 1000
            
            logger.error(
                f"Request failed: {request.method} {request.url.path}",
                extra={
                    "correlation_id": correlation_id,
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": round(duration_ms, 2),
                    "client_ip": client_ip,
                    "error": str(e),
                    "event_type": "request_failed"
                },
                exc_info=True
            )
            raise
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request headers"""
        # Check for forwarded headers first (common in production)
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        # Fallback to direct connection
        return request.client.host if request.client else "unknown"

# Survey-specific logging helpers

class SurveyAPILogger:
    """Logger with survey-specific context and methods"""
    
    def __init__(self, name: str = "survey_api"):
        self.logger = logging.getLogger(name)
    
    def log_with_context(
        self,
        level: str,
        message: str,
        correlation_id: Optional[str] = None,
        session_id: Optional[str] = None,
        form_id: Optional[str] = None,
        user_id: Optional[str] = None,
        **extra_data
    ):
        """Log with survey context"""
        extra = {}
        if correlation_id:
            extra["correlation_id"] = correlation_id
        if session_id:
            extra["session_id"] = session_id
        if form_id:
            extra["form_id"] = form_id
        if user_id:
            extra["user_id"] = user_id
        
        extra.update(extra_data)
        
        log_method = getattr(self.logger, level.lower())
        log_method(message, extra=extra)
    
    def session_started(
        self,
        session_id: str,
        form_id: str,
        correlation_id: Optional[str] = None,
        utm_params: Optional[Dict[str, str]] = None,
        client_ip: Optional[str] = None
    ):
        """Log survey session start"""
        self.log_with_context(
            "info",
            f"Survey session started: {session_id}",
            correlation_id=correlation_id,
            session_id=session_id,
            form_id=form_id,
            event_type="session_started",
            utm_params=utm_params,
            client_ip=client_ip
        )
    
    def responses_received(
        self,
        session_id: str,
        form_id: str,
        response_count: int,
        step_number: int,
        correlation_id: Optional[str] = None
    ):
        """Log response submission"""
        self.log_with_context(
            "info",
            f"Responses received for session {session_id}: {response_count} responses at step {step_number}",
            correlation_id=correlation_id,
            session_id=session_id,
            form_id=form_id,
            event_type="responses_received",
            response_count=response_count,
            step_number=step_number
        )
    
    def session_completed(
        self,
        session_id: str,
        form_id: str,
        final_score: float,
        lead_status: str,
        total_steps: int,
        correlation_id: Optional[str] = None
    ):
        """Log session completion"""
        self.log_with_context(
            "info",
            f"Session completed: {session_id} - Status: {lead_status}, Score: {final_score}",
            correlation_id=correlation_id,
            session_id=session_id,
            form_id=form_id,
            event_type="session_completed",
            final_score=final_score,
            lead_status=lead_status,
            total_steps=total_steps
        )
    
    def session_abandoned(
        self,
        session_id: str,
        form_id: str,
        step_number: int,
        reason: Optional[str] = None,
        correlation_id: Optional[str] = None
    ):
        """Log session abandonment"""
        self.log_with_context(
            "warning",
            f"Session abandoned: {session_id} at step {step_number}",
            correlation_id=correlation_id,
            session_id=session_id,
            form_id=form_id,
            event_type="session_abandoned",
            step_number=step_number,
            abandonment_reason=reason
        )
    
    def api_error(
        self,
        error: Exception,
        endpoint: str,
        correlation_id: Optional[str] = None,
        session_id: Optional[str] = None,
        form_id: Optional[str] = None,
        **context
    ):
        """Log API errors with context"""
        self.log_with_context(
            "error",
            f"API error in {endpoint}: {str(error)}",
            correlation_id=correlation_id,
            session_id=session_id,
            form_id=form_id,
            event_type="api_error",
            endpoint=endpoint,
            error_type=type(error).__name__,
            **context
        )
    
    def database_operation(
        self,
        operation: str,
        table: str,
        duration_ms: float,
        success: bool = True,
        correlation_id: Optional[str] = None,
        session_id: Optional[str] = None,
        error: Optional[str] = None
    ):
        """Log database operations"""
        level = "info" if success else "error"
        message = f"Database {operation} on {table}: {'success' if success else 'failed'}"
        
        self.log_with_context(
            level,
            message,
            correlation_id=correlation_id,
            session_id=session_id,
            event_type="database_operation",
            operation=operation,
            table=table,
            duration_ms=duration_ms,
            success=success,
            error=error
        )

# Performance monitoring
class PerformanceLogger:
    """Logger for performance metrics and monitoring"""
    
    def __init__(self):
        self.logger = logging.getLogger("survey_performance")
    
    def log_slow_operation(
        self,
        operation_name: str,
        duration_ms: float,
        threshold_ms: float = 1000,
        **context
    ):
        """Log operations that exceed performance thresholds"""
        if duration_ms > threshold_ms:
            self.logger.warning(
                f"Slow operation detected: {operation_name} took {duration_ms:.2f}ms",
                extra={
                    "event_type": "slow_operation",
                    "operation": operation_name,
                    "duration_ms": duration_ms,
                    "threshold_ms": threshold_ms,
                    **context
                }
            )
    
    def log_graph_execution(
        self,
        session_id: str,
        graph_duration_ms: float,
        node_durations: Dict[str, float],
        total_nodes: int
    ):
        """Log graph execution performance"""
        avg_node_duration = sum(node_durations.values()) / len(node_durations) if node_durations else 0
        slowest_node = max(node_durations.items(), key=lambda x: x[1]) if node_durations else ("none", 0)
        
        self.logger.info(
            f"Graph execution completed for {session_id}",
            extra={
                "event_type": "graph_execution",
                "session_id": session_id,
                "total_duration_ms": graph_duration_ms,
                "total_nodes": total_nodes,
                "avg_node_duration_ms": avg_node_duration,
                "slowest_node": slowest_node[0],
                "slowest_node_duration_ms": slowest_node[1],
                "node_durations": node_durations
            }
        )

# Health check logging
def log_health_check(component: str, status: str, details: Optional[Dict[str, Any]] = None):
    """Log health check results"""
    logger = logging.getLogger("survey_health")
    
    level = "info" if status == "healthy" else "error"
    message = f"Health check - {component}: {status}"
    
    extra = {
        "event_type": "health_check",
        "component": component,
        "status": status
    }
    
    if details:
        extra["details"] = details
    
    logger.log(getattr(logging, level.upper()), message, extra=extra)

# Request context helpers
def get_correlation_id(request: Request) -> Optional[str]:
    """Get correlation ID from request state"""
    return getattr(request.state, 'correlation_id', None)

def add_request_context_to_logger(request: Request, logger: logging.Logger):
    """Add request context to logger for the duration of request"""
    correlation_id = get_correlation_id(request)
    if correlation_id:
        # Create adapter that adds correlation ID to all log records
        return logging.LoggerAdapter(logger, {"correlation_id": correlation_id})
    return logger

# Global logger instances
api_logger = SurveyAPILogger("survey_api")
performance_logger = PerformanceLogger()

# Export main components
__all__ = [
    'setup_fastapi_logging',
    'LoggingMiddleware',
    'SurveyAPILogger',
    'PerformanceLogger',
    'api_logger',
    'performance_logger',
    'log_health_check',
    'get_correlation_id',
    'add_request_context_to_logger'
]