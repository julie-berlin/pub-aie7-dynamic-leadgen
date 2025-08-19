"""
Response helper utilities for consistent API responses.

All API endpoints should use these helpers to ensure consistent format:
{
  "success": boolean,
  "data": object | null,
  "message": string
}
"""
from typing import Any, Dict, Optional
from fastapi import HTTPException
from fastapi.responses import JSONResponse


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200
) -> JSONResponse:
    """
    Create a successful API response.
    
    Args:
        data: Response data (can be any JSON-serializable object)
        message: Success message
        status_code: HTTP status code
        
    Returns:
        JSONResponse with consistent format
    """
    return JSONResponse(
        content={
            "success": True,
            "data": data,
            "message": message
        },
        status_code=status_code
    )


def error_response(
    message: str,
    status_code: int = 400,
    data: Any = None
) -> JSONResponse:
    """
    Create an error API response.
    
    Args:
        message: Error message
        status_code: HTTP status code
        data: Optional error data (validation errors, etc.)
        
    Returns:
        JSONResponse with consistent format
    """
    return JSONResponse(
        content={
            "success": False,
            "data": data,
            "message": message
        },
        status_code=status_code
    )


def validation_error_response(
    errors: list,
    message: str = "Validation failed"
) -> JSONResponse:
    """
    Create a validation error response.
    
    Args:
        errors: List of validation error details
        message: Error message
        
    Returns:
        JSONResponse with validation errors
    """
    return JSONResponse(
        content={
            "success": False,
            "data": {
                "validation_errors": errors
            },
            "message": message
        },
        status_code=422
    )


def server_error_response(
    message: str = "Internal server error",
    error_id: Optional[str] = None
) -> JSONResponse:
    """
    Create a server error response.
    
    Args:
        message: Error message
        error_id: Optional error ID for tracking
        
    Returns:
        JSONResponse for server errors
    """
    data = {"error_id": error_id} if error_id else None
    
    return JSONResponse(
        content={
            "success": False,
            "data": data,
            "message": message
        },
        status_code=500
    )


def not_found_response(
    resource: str = "Resource",
    resource_id: Optional[str] = None
) -> JSONResponse:
    """
    Create a not found error response.
    
    Args:
        resource: Resource type that was not found
        resource_id: Optional resource identifier
        
    Returns:
        JSONResponse for 404 errors
    """
    message = f"{resource} not found"
    if resource_id:
        message += f": {resource_id}"
        
    return JSONResponse(
        content={
            "success": False,
            "data": {"resource": resource, "resource_id": resource_id} if resource_id else None,
            "message": message
        },
        status_code=404
    )