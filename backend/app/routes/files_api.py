"""
File Serving API - Serves uploaded files with proper security and caching

Provides endpoints for serving uploaded files like logos, with appropriate
security headers, content type detection, and caching support.
"""

import os
import mimetypes
from pathlib import Path
from typing import Optional
import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Response, Request, UploadFile, File, Depends
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer

from app.utils.file_upload import file_upload_handler
from app.utils.response_helpers import success_response, error_response
from app.routes.admin_api import AdminUserResponse
from app.utils.mock_auth import get_mock_admin_user as get_current_admin_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/files", tags=["files"])
security = HTTPBearer()

# Load upload configuration with fallback
upload_config = {
    'url_settings': {
        'cache_max_age': 86400,
        'base_url': '/api/files'
    },
    'logging': {
        'log_file_access': True
    }
}

@router.post("/upload/logo")
async def upload_logo(
    logo: UploadFile = File(...),
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """
    Upload a logo file for the authenticated client
    
    - **logo**: Logo file to upload (JPG, PNG, GIF, max 5MB)
    - Returns the file URL and metadata
    """
    try:
        # Validate file type
        if not logo.content_type or not logo.content_type.startswith('image/'):
            return error_response("Invalid file type. Please upload an image file.", status_code=400)
        
        # Validate file size (5MB max)
        file_size = 0
        logo_content = await logo.read()
        file_size = len(logo_content)
        
        if file_size > 5 * 1024 * 1024:  # 5MB
            return error_response("File size too large. Maximum size is 5MB.", status_code=400)
        
        # Reset file position
        await logo.seek(0)
        
        # Upload the file
        upload_result = await file_upload_handler.process_logo_upload(
            file=logo,
            client_id=current_user.client_id
        )
        
        # Update client settings with new logo URL
        try:
            from app.database import db
            
            # Update client company_logo_url
            update_result = db.client.table("clients")\
                .update({"company_logo_url": upload_result["url"]})\
                .eq("id", current_user.client_id)\
                .execute()
            
            if not update_result.data:
                logger.warning(f"Failed to update client company_logo_url for client {current_user.client_id}")
            else:
                logger.info(f"Successfully updated client company_logo_url for client {current_user.client_id}")
            
        except Exception as db_error:
            logger.error(f"Failed to update client company_logo_url: {db_error}")
            # Don't fail the upload, just log the error
        
        return success_response(
            data={
                "url": upload_result["url"],
                "filename": upload_result["filename"],
                "size": upload_result["size"],
                "content_type": upload_result["mime_type"]
            },
            message="Logo uploaded successfully"
        )
        
    except Exception as e:
        import traceback
        logger.error(f"Logo upload failed: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return error_response(f"Upload failed: {str(e)}", status_code=500)

@router.get("/clients/{client_id}/logos/{filename}")
async def serve_logo(
    client_id: str,
    filename: str,
    request: Request,
    response: Response
) -> FileResponse:
    """
    Serve logo files with appropriate caching headers
    
    - **filename**: The logo filename to serve
    - Returns the logo file with proper MIME type and caching headers
    """
    try:
        # Validate filename to prevent directory traversal attacks
        if not _is_safe_filename(filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid filename"
            )
        
        # Get client-specific file path
        client_logos_dir = file_upload_handler.storage._get_client_directory(client_id, "logos")
        file_path = client_logos_dir / filename
        
        # Verify client isolation for security
        if not file_upload_handler.storage._ensure_client_isolation(client_id, filename):
            logger.warning(f"Client isolation check failed for {filename} (client {client_id})")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Check if file exists
        if not file_path.exists() or not file_path.is_file():
            logger.warning(f"Logo file not found: {filename} for client {client_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Logo not found"
            )
        
        # Log file access if enabled
        if upload_config.get('logging', {}).get('log_file_access', False):
            client_ip = request.client.host if request.client else "unknown"
            logger.info(f"Logo accessed: {filename} by {client_ip}")
        
        # Determine content type
        content_type, _ = mimetypes.guess_type(str(file_path))
        if not content_type:
            content_type = "application/octet-stream"
        
        # Set caching headers
        cache_max_age = upload_config.get('url_settings', {}).get('cache_max_age', 86400)
        
        # Create response headers
        headers = {
            "Cache-Control": f"public, max-age={cache_max_age}",
            "Content-Type": content_type,
            # Security headers
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Content-Security-Policy": "default-src 'none'; img-src 'self';"
        }
        
        return FileResponse(
            path=str(file_path),
            media_type=content_type,
            headers=headers,
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving logo {filename}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error serving file"
        )

@router.get("/clients/{client_id}/logos/{filename}/info")
async def get_logo_info(client_id: str, filename: str) -> dict:
    """
    Get metadata information about a logo file
    
    - **filename**: The logo filename
    - Returns file metadata including size, upload date, etc.
    """
    try:
        # Validate filename
        if not _is_safe_filename(filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid filename"
            )
        
        # Get file info
        file_info = file_upload_handler.get_logo_info(filename, client_id)
        
        if not file_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Logo not found"
            )
        
        return {
            "success": True,
            "data": file_info,
            "message": "Logo information retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting logo info {filename}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving file information"
        )

@router.head("/clients/{client_id}/logos/{filename}")
async def check_logo_exists(client_id: str, filename: str) -> Response:
    """
    Check if a logo file exists (HEAD request)
    
    - **filename**: The logo filename to check
    - Returns 200 if file exists, 404 if not found
    """
    try:
        # Validate filename
        if not _is_safe_filename(filename):
            return Response(status_code=status.HTTP_400_BAD_REQUEST)
        
        # Check if file exists in client-specific directory
        client_logos_dir = file_upload_handler.storage._get_client_directory(client_id, "logos")
        file_path = client_logos_dir / filename
        
        if file_path.exists() and file_path.is_file():
            # Get file size for Content-Length header
            file_size = file_path.stat().st_size
            
            # Determine content type
            content_type, _ = mimetypes.guess_type(str(file_path))
            if not content_type:
                content_type = "application/octet-stream"
            
            return Response(
                status_code=status.HTTP_200_OK,
                headers={
                    "Content-Type": content_type,
                    "Content-Length": str(file_size),
                    "Cache-Control": f"public, max-age={upload_config.get('url_settings', {}).get('cache_max_age', 86400)}"
                }
            )
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        logger.error(f"Error checking logo {filename}: {str(e)}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

def _is_safe_filename(filename: str) -> bool:
    """
    Validate filename for security
    
    Prevents directory traversal attacks and validates filename format
    """
    # Check for directory traversal attempts
    if ".." in filename or "/" in filename or "\\" in filename:
        return False
    
    # Check for empty or invalid filenames
    if not filename or filename.startswith(".") or len(filename) > 255:
        return False
    
    # Check for valid characters (alphanumeric, dash, underscore, dot)
    import re
    if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
        return False
    
    return True

# Health check for file serving
@router.get("/health")
async def files_health_check() -> dict:
    """Health check for file serving functionality"""
    try:
        # Check if base upload directories exist
        base_dir = file_upload_handler.storage.base_upload_dir
        temp_dir = file_upload_handler.storage.temp_dir
        
        health_status = {
            "status": "healthy",
            "directories": {
                "base_upload_dir": {
                    "exists": base_dir.exists(),
                    "writable": os.access(base_dir, os.W_OK) if base_dir.exists() else False,
                    "path": str(base_dir)
                },
                "temp_dir": {
                    "exists": temp_dir.exists(), 
                    "writable": os.access(temp_dir, os.W_OK) if temp_dir.exists() else False,
                    "path": str(temp_dir)
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # Overall health check
        all_healthy = all([
            health_status["directories"]["base_upload_dir"]["exists"],
            health_status["directories"]["base_upload_dir"]["writable"],
            health_status["directories"]["temp_dir"]["exists"],
            health_status["directories"]["temp_dir"]["writable"]
        ])
        
        if not all_healthy:
            health_status["status"] = "degraded"
        
        return {
            "success": True,
            "data": health_status,
            "message": "File serving health check completed"
        }
        
    except Exception as e:
        logger.error(f"File serving health check failed: {str(e)}")
        return {
            "success": False,
            "data": {"status": "unhealthy", "error": str(e)},
            "message": "File serving health check failed"
        }