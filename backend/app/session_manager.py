"""
Session management using Starlette's built-in SessionMiddleware with Redis backend.

This module provides simple session helpers that work with Starlette's SessionMiddleware.
"""

import os
import uuid
from typing import Optional

from fastapi import Request
from app.session_store import RedisSessionStore


# Initialize Redis session store for health checks and direct operations
redis_store = RedisSessionStore()


async def create_survey_session(request: Request, session_data: dict) -> str:
    """
    Create a new survey session using Starlette's session middleware.
    
    Args:
        request: FastAPI request object
        session_data: Dictionary containing session information (must include 'session_id')
        
    Returns:
        Session ID string from session_data
    """
    # Store session data in Starlette's session
    # No need for separate survey_session_id - the session_id is in session_data
    request.session['survey_data'] = session_data
    
    return session_data.get('session_id', str(uuid.uuid4()))


async def get_survey_session(request: Request) -> Optional[dict]:
    """
    Get survey session data from request.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Session data dictionary or None if no valid session
    """
    session_data = request.session.get('survey_data')
    
    # Simply return the session_data if it exists
    # The session_id is already inside session_data
    return session_data if session_data else None


async def update_survey_session(request: Request, session_data: dict) -> bool:
    """
    Update existing survey session data.
    
    Args:
        request: FastAPI request object
        session_data: Updated session data
        
    Returns:
        True if successful, False otherwise
    """
    if 'survey_data' not in request.session:
        return False
    
    # Update session data
    request.session['survey_data'] = session_data
    
    return True


async def delete_survey_session(request: Request) -> bool:
    """
    Delete survey session.
    
    Args:
        request: FastAPI request object
        
    Returns:
        True if successful, False otherwise
    """
    if 'survey_data' in request.session:
        del request.session['survey_data']
        return True
    
    return False


# Backward compatibility functions for existing API endpoints
async def create_session(session_data: dict) -> str:
    """
    Create a new session (compatibility function).
    Note: This function requires a request context to work properly.
    """
    return str(uuid.uuid4())


async def get_session_from_request(request: Request) -> Optional[dict]:
    """Get session data from request (main function)."""
    return await get_survey_session(request)


async def update_session(session_id: str, session_data: dict) -> bool:
    """
    Update existing session (compatibility function).
    Note: This function requires a request context to work properly.
    """
    # This is a fallback that won't work without request context
    return False


async def delete_session(session_id: str) -> bool:
    """
    Delete a session (compatibility function).
    Note: This function requires a request context to work properly.
    """
    # This is a fallback that won't work without request context
    return False


def set_session_cookie(response, session_id: str):
    """
    Set session cookie on response.
    
    Note: With Starlette's SessionMiddleware, cookies are handled automatically.
    This function is kept for compatibility but does nothing.
    """
    # No-op: Starlette's SessionMiddleware handles cookies automatically
    pass


# Health check function
async def check_session_health() -> bool:
    """Check if session backend is healthy."""
    try:
        # Test Redis connection (our session store backend)
        return await redis_store.health_check()
    except Exception:
        return False