"""
CORS Configuration for Frontend Integration

Configures Cross-Origin Resource Sharing to allow frontend applications
to access the survey API from different domains.
"""

import os
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def configure_cors(app: FastAPI) -> None:
    """
    Configure CORS middleware for the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    
    # Get allowed origins from environment variables
    allowed_origins_env = os.getenv("CORS_ALLOWED_ORIGINS", "")
    
    # Default allowed origins for development
    default_origins = [
        "http://localhost:3000",          # React development server
        "http://localhost:3001",          # Alternative React port
        "http://localhost:5173",          # Vite development server
        "http://localhost:8080",          # Vue development server
        "http://127.0.0.1:3000",          # Alternative localhost
        "http://127.0.0.1:5173",          # Alternative localhost for Vite
    ]
    
    # Parse environment variable (comma-separated URLs)
    if allowed_origins_env:
        env_origins = [origin.strip() for origin in allowed_origins_env.split(",")]
        allowed_origins = env_origins
    else:
        allowed_origins = default_origins
    
    # Production domains (add these to environment variables)
    production_origins = []
    if os.getenv("PRODUCTION_FRONTEND_URL"):
        production_origins.append(os.getenv("PRODUCTION_FRONTEND_URL"))
    if os.getenv("STAGING_FRONTEND_URL"):
        production_origins.append(os.getenv("STAGING_FRONTEND_URL"))
    
    # Combine all origins
    all_origins = allowed_origins + production_origins
    
    # Remove duplicates while preserving order
    unique_origins = list(dict.fromkeys(all_origins))
    
    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=unique_origins,
        allow_credentials=True,
        allow_methods=[
            "GET",
            "POST", 
            "PUT",
            "DELETE",
            "OPTIONS",
            "HEAD",
            "PATCH"
        ],
        allow_headers=[
            "Accept",
            "Accept-Language", 
            "Content-Language",
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "X-CSRF-Token",
            "X-Session-ID",
            "User-Agent",
            "Referer",
            "Origin"
        ],
        expose_headers=[
            "X-Session-ID",
            "X-Request-ID",
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-RateLimit-Reset"
        ],
        max_age=600  # Cache preflight requests for 10 minutes
    )
    
    print(f"✅ CORS configured for origins: {unique_origins}")


def get_cors_origins() -> List[str]:
    """
    Get the list of allowed CORS origins.
    
    Returns:
        List of allowed origin URLs
    """
    allowed_origins_env = os.getenv("CORS_ALLOWED_ORIGINS", "")
    
    default_origins = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    if allowed_origins_env:
        env_origins = [origin.strip() for origin in allowed_origins_env.split(",")]
        return env_origins
    
    return default_origins


def validate_origin(origin: str) -> bool:
    """
    Validate if an origin is allowed.
    
    Args:
        origin: Origin URL to validate
        
    Returns:
        True if origin is allowed, False otherwise
    """
    allowed_origins = get_cors_origins()
    
    # Add production origins
    if os.getenv("PRODUCTION_FRONTEND_URL"):
        allowed_origins.append(os.getenv("PRODUCTION_FRONTEND_URL"))
    if os.getenv("STAGING_FRONTEND_URL"):
        allowed_origins.append(os.getenv("STAGING_FRONTEND_URL"))
    
    return origin in allowed_origins


# CORS configuration for different environments
CORS_CONFIG = {
    "development": {
        "allow_origins": [
            "http://localhost:3000",
            "http://localhost:3001",
            "http://localhost:5173", 
            "http://localhost:8080",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ],
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    },
    "staging": {
        "allow_origins": [
            "https://staging.yourdomain.com",
            "https://preview.yourdomain.com",
        ],
        "allow_credentials": True,
        "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": [
            "Accept",
            "Content-Type", 
            "Authorization",
            "X-Requested-With",
            "Origin"
        ],
    },
    "production": {
        "allow_origins": [
            "https://yourdomain.com",
            "https://www.yourdomain.com",
        ],
        "allow_credentials": False,  # More secure for production
        "allow_methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": [
            "Accept",
            "Content-Type",
            "X-Requested-With",
            "Origin"
        ],
    }
}


def configure_environment_cors(app: FastAPI, environment: str = "development") -> None:
    """
    Configure CORS based on environment.
    
    Args:
        app: FastAPI application
        environment: "development", "staging", or "production"
    """
    config = CORS_CONFIG.get(environment, CORS_CONFIG["development"])
    
    app.add_middleware(
        CORSMiddleware,
        **config
    )
    
    print(f"✅ CORS configured for {environment} environment")
    print(f"   Allowed origins: {config['allow_origins']}")


# Pre-flight request handling
def add_cors_headers_to_response(response, origin: str):
    """
    Manually add CORS headers to response (if needed).
    
    Args:
        response: FastAPI response object
        origin: Request origin
    """
    if validate_origin(origin):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Authorization, X-Requested-With"
    
    return response


# Usage examples and documentation
CORS_SETUP_EXAMPLES = """
# Environment Variable Setup

## Development (.env.local)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

## Staging (.env.staging)
CORS_ALLOWED_ORIGINS=https://staging.yourdomain.com,https://preview.yourdomain.com
STAGING_FRONTEND_URL=https://staging.yourdomain.com

## Production (.env.production)
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
PRODUCTION_FRONTEND_URL=https://yourdomain.com

# FastAPI Integration

from app.cors_config import configure_cors

app = FastAPI()
configure_cors(app)

# Or environment-specific:
configure_environment_cors(app, environment="production")

# Frontend Integration Examples

## JavaScript/TypeScript
fetch('http://localhost:8000/api/survey/start', {
  method: 'POST',
  credentials: 'include',  // Include cookies if needed
  headers: {
    'Content-Type': 'application/json',
    'Origin': 'http://localhost:3000'
  },
  body: JSON.stringify({
    form_id: 'your-form-id',
    utm_source: 'website'
  })
})

## React with Axios
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  withCredentials: true,  // Include cookies
  headers: {
    'Content-Type': 'application/json'
  }
});

## Vue.js
import axios from 'axios'

Vue.prototype.$http = axios.create({
  baseURL: process.env.VUE_APP_API_URL,
  withCredentials: true
})
"""