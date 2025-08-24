"""
Admin Uploads API - File Upload Management

This module provides API endpoints for:
1. Logo upload and management
2. Favicon upload and management
3. File validation and processing
4. Client asset management
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import Dict, Any
import logging
from datetime import datetime
import uuid

from app.database import db
from app.utils.file_upload import validate_and_store_logo, remove_logo
from app.utils.response_helpers import success_response, error_response
from app.routes.admin_auth import AdminUserResponse, get_current_admin_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin/upload", tags=["admin-uploads"])

# === LOGO UPLOAD ENDPOINTS ===

@router.post("/logo")
async def upload_logo(
    file: UploadFile = File(...),
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Upload a logo for the client."""
    try:
        # Validate file is provided
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Process the logo upload
        upload_result = await validate_and_store_logo(file, current_user.client_id)
        
        # Update the client_settings table with the new logo URL and file_id
        # Check if client_settings record exists
        settings_result = db.client.table('client_settings').select('id').eq('client_id', current_user.client_id).execute()
        
        settings_update = {
            'logo_url': upload_result['url'],
            'logo_file_id': upload_result.get('file_id'),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        if settings_result.data:
            # Update existing record
            update_result = db.client.table('client_settings').update(settings_update).eq('client_id', current_user.client_id).execute()
            
            if not update_result.data:
                raise HTTPException(status_code=500, detail="Failed to update client settings with logo URL")
        else:
            # Create new record
            new_settings = {
                'id': str(uuid.uuid4()),
                'client_id': current_user.client_id,
                **settings_update
            }
            
            insert_result = db.client.table('client_settings').insert(new_settings).execute()
            if not insert_result.data:
                raise HTTPException(status_code=500, detail="Failed to create client settings record")
        
        return success_response({
            "logo_url": upload_result['url'],
            "filename": upload_result['filename'],
            "size": upload_result['size'],
            "uploaded_at": upload_result['uploaded_at'],
            "file_id": upload_result.get('file_id')
        }, "Logo uploaded successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to upload logo: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload logo")

@router.delete("/logo/{filename}")
async def delete_logo(
    filename: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Delete a logo file."""
    try:
        # Delete the file
        success = remove_logo(filename, current_user.client_id)
        
        if success:
            # Update client_settings to remove logo_url and logo_file_id
            update_result = db.client.table('client_settings').update({
                'logo_url': None,
                'logo_file_id': None,
                'updated_at': datetime.utcnow().isoformat()
            }).eq('client_id', current_user.client_id).execute()
            
            
            # Note: We don't fail if the update doesn't work since the file is already deleted
            # This handles cases where client_settings record might not exist
            
            return success_response({
                "filename": filename
            }, "Logo deleted successfully")
        else:
            raise HTTPException(status_code=404, detail="Logo file not found or could not be deleted")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete logo: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete logo")

@router.post("/favicon")
async def upload_favicon(
    file: UploadFile = File(...),
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Upload a favicon for the client."""
    try:
        # Validate file is provided
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Validate file type for favicon (should be .ico, .png, or .svg)
        if not file.content_type in ['image/x-icon', 'image/png', 'image/svg+xml']:
            raise HTTPException(
                status_code=400, 
                detail="Favicon must be an ICO, PNG, or SVG file"
            )
        
        # Validate file size (max 1MB for favicon)
        file_content = await file.read()
        if len(file_content) > 1024 * 1024:  # 1MB
            raise HTTPException(status_code=400, detail="Favicon size must be less than 1MB")
        
        # Reset file position
        await file.seek(0)
        
        # TODO: Implement favicon-specific upload logic
        # For now, use similar logic to logo upload but with different path
        upload_result = {
            'url': f'/api/files/clients/{current_user.client_id}/favicons/{file.filename}',
            'filename': file.filename,
            'size': len(file_content),
            'uploaded_at': datetime.utcnow().isoformat()
        }
        
        # Update the client_settings table with the new favicon URL
        settings_result = db.client.table('client_settings').select('id').eq('client_id', current_user.client_id).execute()
        
        if settings_result.data:
            # Update existing record
            update_result = db.client.table('client_settings').update({
                'favicon_url': upload_result['url'],
                'updated_at': datetime.utcnow().isoformat()
            }).eq('client_id', current_user.client_id).execute()
            
            if not update_result.data:
                raise HTTPException(status_code=500, detail="Failed to update client settings with favicon URL")
        else:
            # Create new record
            new_settings = {
                'id': str(uuid.uuid4()),
                'client_id': current_user.client_id,
                'favicon_url': upload_result['url']
            }
            
            insert_result = db.client.table('client_settings').insert(new_settings).execute()
            if not insert_result.data:
                raise HTTPException(status_code=500, detail="Failed to create client settings record")
        
        return success_response({
            "favicon_url": upload_result['url'],
            "filename": upload_result['filename'],
            "size": upload_result['size'],
            "uploaded_at": upload_result['uploaded_at']
        }, "Favicon uploaded successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to upload favicon: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload favicon")

@router.delete("/favicon/{filename}")
async def delete_favicon(
    filename: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Delete a favicon file."""
    try:
        # TODO: Implement favicon-specific delete logic
        # For now, assume success
        success = True
        
        if success:
            # Update client_settings to remove favicon_url
            update_result = db.client.table('client_settings').update({
                'favicon_url': None,
                'updated_at': datetime.utcnow().isoformat()
            }).eq('client_id', current_user.client_id).execute()
            
            return success_response({
                "filename": filename
            }, "Favicon deleted successfully")
        else:
            raise HTTPException(status_code=404, detail="Favicon file not found or could not be deleted")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete favicon: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete favicon")

@router.get("/assets")
async def list_client_assets(
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """List all uploaded assets for the client."""
    try:
        # Get client settings to see what assets are configured
        settings_result = db.client.table('client_settings').select(
            'logo_url, favicon_url'
        ).eq('client_id', current_user.client_id).execute()
        
        assets = {
            "logo_url": None,
            "favicon_url": None,
            "total_assets": 0
        }
        
        if settings_result.data:
            settings = settings_result.data[0]
            assets["logo_url"] = settings.get('logo_url')
            assets["favicon_url"] = settings.get('favicon_url')
            
            # Count non-null assets
            assets["total_assets"] = sum(1 for url in [assets["logo_url"], assets["favicon_url"]] if url)
        
        return success_response(assets, "Client assets retrieved successfully")
        
    except Exception as e:
        logger.error(f"Failed to list client assets: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve client assets")