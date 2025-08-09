"""
FastAPI Backend for Dynamic Lead Generation

Main application entry point with middleware and route configuration.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
import os

# Load environment variables
load_dotenv()

# Import routes
import sys
import os
sys.path.append(os.path.dirname(__file__))
from routes import sessions

# Create FastAPI application
app = FastAPI(
    title="Dynamic Lead Generation API",
    description="AI-powered adaptive forms for lead generation and qualification",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sessions.router, prefix="/api", tags=["sessions"])

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
        import openai
        openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
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