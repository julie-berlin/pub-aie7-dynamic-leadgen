"""
Health check and monitoring endpoints for production deployment
"""

import os
import time
import psutil
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.database import db
from app.utils.config_loader import get_database_config, get_security_config
from app.middleware.admin_auth import get_admin_user
from app.middleware.request_limits import RequestLimitsMiddleware

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/health", tags=["health"])

# Cache system metrics for better performance
_metrics_cache = {}
_cache_ttl = 30  # seconds


def _get_cached_metrics(metric_name: str, compute_func):
    """Get cached metrics with TTL"""
    now = time.time()
    cache_key = f"{metric_name}_{now // _cache_ttl}"
    
    if cache_key not in _metrics_cache:
        _metrics_cache[cache_key] = {
            'data': compute_func(),
            'timestamp': now
        }
        
        # Clean old cache entries
        old_keys = [k for k in _metrics_cache.keys() if _metrics_cache[k]['timestamp'] < now - _cache_ttl * 2]
        for old_key in old_keys:
            del _metrics_cache[old_key]
    
    return _metrics_cache[cache_key]['data']


def _get_system_metrics() -> Dict[str, Any]:
    """Get system performance metrics"""
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        return {
            'cpu': {
                'usage_percent': cpu_percent,
                'cores': psutil.cpu_count(),
                'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else None
            },
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'usage_percent': memory.percent
            },
            'disk': {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'usage_percent': disk.percent
            },
            'boot_time': psutil.boot_time()
        }
    except Exception as e:
        logger.warning(f"Failed to get system metrics: {e}")
        return {'error': 'system_metrics_unavailable'}


def _get_application_metrics() -> Dict[str, Any]:
    """Get application-specific metrics"""
    try:
        # Database connection stats
        db_stats = db.get_connection_stats()
        
        # Environment info
        environment = os.getenv('ENVIRONMENT', 'unknown')
        
        # Configuration status
        config_status = {
            'database_configured': bool(os.getenv('SUPABASE_URL')),
            'openai_configured': bool(os.getenv('OPENAI_API_KEY')),
            'admin_auth_configured': bool(os.getenv('ADMIN_API_KEY')),
            'jwt_configured': bool(os.getenv('JWT_SECRET')),
            'sentry_configured': bool(os.getenv('SENTRY_DSN')),
            'redis_configured': bool(os.getenv('REDIS_URL'))
        }
        
        return {
            'environment': environment,
            'python_version': f"{psutil.sys.version_info.major}.{psutil.sys.version_info.minor}.{psutil.sys.version_info.micro}",
            'uptime_seconds': time.time() - psutil.Process().create_time(),
            'database': db_stats,
            'configuration': config_status,
            'log_level': os.getenv('LOG_LEVEL', 'INFO')
        }
    except Exception as e:
        logger.warning(f"Failed to get application metrics: {e}")
        return {'error': 'application_metrics_unavailable'}


@router.get("/")
async def basic_health_check():
    """Basic health check endpoint for load balancers"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@router.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return {"message": "pong", "timestamp": datetime.now().isoformat()}


@router.get("/ready")
async def readiness_check():
    """Readiness check - ensures application can serve requests"""
    checks = {}
    overall_status = "ready"
    
    try:
        # Check database connectivity
        db_healthy = db.test_connection()
        checks['database'] = {
            'status': 'healthy' if db_healthy else 'unhealthy',
            'details': 'connection_successful' if db_healthy else 'connection_failed'
        }
        if not db_healthy:
            overall_status = "not_ready"
        
        # Check essential environment variables
        required_vars = ['SUPABASE_URL', 'SUPABASE_SECRET_KEY', 'OPENAI_API_KEY']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        checks['environment'] = {
            'status': 'healthy' if not missing_vars else 'unhealthy',
            'missing_variables': missing_vars
        }
        if missing_vars:
            overall_status = "not_ready"
        
        # Check system resources
        system_metrics = _get_cached_metrics('system', _get_system_metrics)
        if 'error' not in system_metrics:
            memory_ok = system_metrics['memory']['usage_percent'] < 90
            disk_ok = system_metrics['disk']['usage_percent'] < 90
            cpu_ok = system_metrics['cpu']['usage_percent'] < 90
            
            checks['resources'] = {
                'status': 'healthy' if (memory_ok and disk_ok and cpu_ok) else 'degraded',
                'memory_usage': system_metrics['memory']['usage_percent'],
                'disk_usage': system_metrics['disk']['usage_percent'],
                'cpu_usage': system_metrics['cpu']['usage_percent']
            }
            
            if not (memory_ok and disk_ok and cpu_ok):
                overall_status = "degraded"
        
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        overall_status = "not_ready"
        checks['error'] = str(e)
    
    status_code = 200 if overall_status == "ready" else 503
    
    return JSONResponse(
        status_code=status_code,
        content={
            "status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "checks": checks
        }
    )


@router.get("/live")
async def liveness_check():
    """Liveness check - ensures application process is alive"""
    try:
        # Basic process health
        process = psutil.Process()
        
        return {
            "status": "alive",
            "timestamp": datetime.now().isoformat(),
            "process": {
                "pid": process.pid,
                "status": process.status(),
                "create_time": process.create_time(),
                "cpu_percent": process.cpu_percent(),
                "memory_percent": process.memory_percent()
            }
        }
    except Exception as e:
        logger.error(f"Liveness check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
        )


@router.get("/metrics", dependencies=[Depends(get_admin_user)])
async def detailed_metrics(admin_user: Optional[Dict] = None):
    """Detailed system and application metrics (admin only)"""
    try:
        system_metrics = _get_cached_metrics('system', _get_system_metrics)
        app_metrics = _get_cached_metrics('application', _get_application_metrics)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "system": system_metrics,
            "application": app_metrics,
            "request_info": {
                "admin_user": admin_user.get('auth_method') if admin_user else None
            }
        }
    except Exception as e:
        logger.error(f"Metrics collection failed: {e}")
        raise HTTPException(status_code=500, detail="Metrics collection failed")


@router.get("/status")
async def comprehensive_status():
    """Comprehensive status check for monitoring dashboards"""
    try:
        # Get basic health info
        db_healthy = db.test_connection()
        environment = os.getenv('ENVIRONMENT', 'unknown')
        
        # Get cached metrics for performance
        system_metrics = _get_cached_metrics('system', _get_system_metrics)
        app_metrics = _get_cached_metrics('application', _get_application_metrics)
        
        # Determine overall health
        overall_health = "healthy"
        issues = []
        
        # Check database
        if not db_healthy:
            overall_health = "unhealthy"
            issues.append("database_connection_failed")
        
        # Check system resources
        if 'error' not in system_metrics:
            if system_metrics['memory']['usage_percent'] > 90:
                overall_health = "degraded"
                issues.append("high_memory_usage")
            if system_metrics['disk']['usage_percent'] > 90:
                overall_health = "degraded"
                issues.append("low_disk_space")
            if system_metrics['cpu']['usage_percent'] > 90:
                overall_health = "degraded"
                issues.append("high_cpu_usage")
        
        # Security configuration check
        security_config = get_security_config()
        security_status = {
            'auth_enabled': security_config.auth_enabled,
            'input_validation': security_config.sanitize_inputs,
            'https_enforced': security_config.force_https
        }
        
        response = {
            "status": overall_health,
            "timestamp": datetime.now().isoformat(),
            "environment": environment,
            "version": "1.0.0",
            "uptime_seconds": app_metrics.get('uptime_seconds', 0),
            "database": {
                "status": "connected" if db_healthy else "disconnected",
                "connection_stats": app_metrics.get('database', {})
            },
            "security": security_status,
            "issues": issues,
            "system_summary": {
                "cpu_usage": system_metrics.get('cpu', {}).get('usage_percent', 0),
                "memory_usage": system_metrics.get('memory', {}).get('usage_percent', 0),
                "disk_usage": system_metrics.get('disk', {}).get('usage_percent', 0)
            } if 'error' not in system_metrics else None
        }
        
        status_code = 200 if overall_health == "healthy" else (503 if overall_health == "unhealthy" else 200)
        
        return JSONResponse(status_code=status_code, content=response)
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
        )


@router.get("/debug", dependencies=[Depends(get_admin_user)])
async def debug_info(admin_user: Optional[Dict] = None):
    """Debug information for troubleshooting (admin only)"""
    try:
        return {
            "timestamp": datetime.now().isoformat(),
            "environment": {
                "ENVIRONMENT": os.getenv('ENVIRONMENT'),
                "LOG_LEVEL": os.getenv('LOG_LEVEL'),
                "PYTHON_PATH": os.getenv('PYTHONPATH'),
                "PATH": os.getenv('PATH')
            },
            "configuration": {
                "database_config": str(get_database_config()),
                "security_config": str(get_security_config())
            },
            "system": _get_cached_metrics('system', _get_system_metrics),
            "application": _get_cached_metrics('application', _get_application_metrics),
            "admin_info": admin_user
        }
    except Exception as e:
        logger.error(f"Debug info collection failed: {e}")
        raise HTTPException(status_code=500, detail="Debug info collection failed")