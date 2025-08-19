"""
FastAPI Backend for Dynamic Lead Generation

Main application entry point with environment-specific configuration,
middleware setup, and route configuration.
"""

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import uvicorn
import os
import sys
import logging

# Load environment variables first
load_dotenv()

# Validate environment before importing other modules
from app.utils.env_validator import validate_environment
from app.utils.config_loader import get_api_config, get_security_config

# Validate environment variables
if not validate_environment():
    print("❌ Environment validation failed. Please check your .env file.")
    print("Run 'python -m app.utils.env_validator help' for setup instructions.")
    sys.exit(1)

# Load configurations
api_config = get_api_config()
security_config = get_security_config()

# Set up logging with environment-specific settings
from app.utils.fastapi_logging import setup_fastapi_logging, LoggingMiddleware, log_health_check

setup_fastapi_logging(
    log_level=os.getenv('LOG_LEVEL', 'INFO'),
    log_file=os.getenv('LOG_FILE')
)

logger = logging.getLogger(__name__)

# Set up tracing
from app.utils.langsmith_tracing import setup_graph_tracing
setup_graph_tracing()

# Import middleware and configuration
from app.middleware.rate_limiting import create_rate_limit_middleware
from app.middleware.input_validation import create_input_validation_middleware
from app.middleware.response_sanitization import create_response_sanitization_middleware
from app.middleware.admin_auth import create_admin_auth_middleware
from app.middleware.security_headers import create_security_headers_middleware
from app.middleware.request_limits import create_request_limits_middleware
from app.cors_config import configure_cors

# Import session management
from starlette.middleware.sessions import SessionMiddleware
from app.session_store import RedisSessionStore

# Import routes
from app.routes import survey_api, health, theme_api, analytics_api, admin_api, admin_forms_api, admin_analytics_api, admin_themes_api, admin_business_api

# Create FastAPI application with environment-specific settings
app = FastAPI(
    title=api_config.title,
    description=api_config.description,
    version=api_config.version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "survey",
            "description": "Survey management endpoints for frontend integration"
        },
        {
            "name": "themes",
            "description": "Theme management endpoints for form customization"
        },
        {
            "name": "analytics",
            "description": "Analytics and performance tracking endpoints"
        },
        {
            "name": "admin",
            "description": "Admin user management and client configuration endpoints"
        },
        {
            "name": "admin-forms",
            "description": "Admin form management endpoints"
        },
        {
            "name": "admin-analytics",
            "description": "Admin analytics and reporting endpoints"
        },
        {
            "name": "admin-themes",
            "description": "Admin theme management endpoints"
        },
        {
            "name": "admin-business",
            "description": "Admin business information and settings endpoints"
        },
        {
            "name": "health", 
            "description": "Health check and monitoring endpoints"
        }
    ]
)

# Configure CORS middleware with environment-based settings
configure_cors(app)

# Initialize session store and middleware
session_store = RedisSessionStore()

# Add security middleware (order matters!)
# 1. Security headers first (sets secure response headers)
app.add_middleware(create_security_headers_middleware())

# 2. Session middleware (must be before other middleware that might use sessions)
app.add_middleware(
    SessionMiddleware, 
    secret_key=os.getenv('SESSION_SECRET_KEY', 'dev-secret-key-change-in-production'),
    max_age=1800,  # 30 minutes
    path='/api/survey',
    same_site='lax',
    https_only=os.getenv('ENVIRONMENT', 'development').lower() != 'development'
)

# 3. Request limits (size and timeout protection)
app.add_middleware(create_request_limits_middleware())

# 4. Rate limiting (before input validation to prevent excessive processing)
app.add_middleware(create_rate_limit_middleware())

# 5. Input validation (sanitize and validate all incoming data)
app.add_middleware(create_input_validation_middleware())

# 6. Admin authentication (protect admin endpoints)
app.add_middleware(create_admin_auth_middleware())

# 7. Response sanitization (clean outgoing data)
app.add_middleware(create_response_sanitization_middleware())

# 8. Logging middleware last (log after all security processing)
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(survey_api.router, tags=["survey"])
app.include_router(theme_api.router, tags=["themes"])
app.include_router(analytics_api.router, tags=["analytics"])
app.include_router(admin_api.router, tags=["admin"])
app.include_router(admin_forms_api.router, tags=["admin-forms"])
app.include_router(admin_analytics_api.router, tags=["admin-analytics"])
app.include_router(admin_themes_api.router, tags=["admin-themes"])
app.include_router(admin_business_api.router, tags=["admin-business"])
app.include_router(health.router, tags=["health"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Dynamic Lead Generation API",
        "status": "active",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Detailed health check with system status"""
    try:
        # Test database connection
        from app.database import db
        db_healthy = db.test_connection()
        
        # Test OpenAI connection
        openai_healthy = bool(os.getenv('OPENAI_API_KEY'))
        
        return {
            "status": "healthy" if (db_healthy and openai_healthy) else "degraded",
            "database": "connected" if db_healthy else "disconnected",
            "openai": "configured" if openai_healthy else "not_configured",
            "timestamp": "2025-01-27T00:00:00Z"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2025-01-27T00:00:00Z"
        }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )