"""
FastAPI Backend for Dynamic Lead Generation

Main application entry point with middleware and route configuration.
"""

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import uvicorn
import os

# Load environment variables
load_dotenv()

# Import configuration
from cors_config import configure_cors
from utils.fastapi_logging import setup_fastapi_logging, LoggingMiddleware, log_health_check
from utils.langsmith_tracing import setup_graph_tracing

# Set up logging first
setup_fastapi_logging(
    log_level=os.getenv('LOG_LEVEL', 'INFO'),
    log_file=os.getenv('LOG_FILE')
)

# Set up tracing
setup_graph_tracing()

# Import routes
import sys
import os
sys.path.append(os.path.dirname(__file__))
from routes import survey_api

# Create FastAPI application
app = FastAPI(
    title="Dynamic Lead Generation API",
    description="AI-powered adaptive forms for lead generation and qualification",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "survey",
            "description": "Survey management endpoints for frontend integration"
        },
        {
            "name": "health",
            "description": "Health check and monitoring endpoints"
        }
    ]
)

# Configure CORS middleware with environment-based settings
configure_cors(app)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(survey_api.router, tags=["survey"])

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
        from database import db
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