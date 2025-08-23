"""
Admin Client API - Client Settings and Branding Configuration

This module provides API endpoints for:
1. Client settings and branding configuration
2. Logo and favicon management
3. Custom domain settings
4. White label configuration
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, EmailStr, validator
from urllib.parse import urlparse
from typing import Dict, Any, Optional
import logging
from datetime import datetime
import uuid

from app.database import db
from app.utils.response_helpers import success_response, error_response
from app.routes.admin_auth import AdminUserResponse, get_current_admin_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin/client", tags=["admin-client"])

# === PYDANTIC MODELS ===

class ClientSettingsRequest(BaseModel):
    """Request to update client settings."""
    logo_url: Optional[str] = None
    favicon_url: Optional[str] = None
    brand_colors: Optional[Dict[str, str]] = None
    font_preferences: Optional[Dict[str, str]] = None
    default_theme_id: Optional[str] = None
    default_form_settings: Optional[Dict[str, Any]] = None
    custom_domain: Optional[str] = None
    white_label_enabled: Optional[bool] = None
    from_email: Optional[EmailStr] = None
    reply_to_email: Optional[EmailStr] = None
    webhook_url: Optional[str] = None

    @validator('logo_url')
    def validate_logo_url(cls, v):
        """Validate logo URL format and path."""
        if v is None:
            return v
        
        # Check if it's a valid URL format or relative path
        if v.startswith('http://') or v.startswith('https://'):
            # External URL - validate URL format
            try:
                parsed = urlparse(v)
                if not parsed.scheme or not parsed.netloc:
                    raise ValueError('Invalid external URL format')
            except Exception:
                raise ValueError('Invalid URL format')
        elif v.startswith('/api/files/'):
            # Internal API path - validate path structure
            # Expected format: /api/files/clients/{client_id}/logos/{filename}
            parts = v.split('/')
            if len(parts) < 6 or parts[3] != 'clients' or parts[5] != 'logos':
                raise ValueError('Invalid internal logo path format')
        else:
            raise ValueError('Logo URL must be either an external URL (http/https) or internal path (/api/files/...)')
        
        return v

    @validator('custom_domain')
    def validate_custom_domain(cls, v):
        """Validate custom domain format."""
        if v is None:
            return v
        
        # Basic domain validation
        if not v or '://' in v:
            raise ValueError('Domain should not include protocol')
        
        # Check for valid domain format
        import re
        domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.([a-zA-Z]{2,}|[a-zA-Z]{2,}\.[a-zA-Z]{2,})$'
        if not re.match(domain_pattern, v):
            raise ValueError('Invalid domain format')
        
        return v.lower()

class ClientSettingsResponse(BaseModel):
    """Response model for client settings."""
    id: str
    client_id: str
    logo_url: Optional[str] = None
    favicon_url: Optional[str] = None
    brand_colors: Optional[Dict[str, str]] = None
    font_preferences: Optional[Dict[str, str]] = None
    default_theme_id: Optional[str] = None
    default_form_settings: Dict[str, Any] = {}
    custom_domain: Optional[str] = None
    custom_domain_verified: bool = False
    white_label_enabled: bool = False
    from_email: Optional[str] = None
    reply_to_email: Optional[str] = None
    webhook_url: Optional[str] = None
    plan_type: str = 'free'
    monthly_form_limit: int = 1000
    monthly_response_limit: int = 10000
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# === UTILITY FUNCTIONS ===

def _validate_logo_file_exists(logo_url: str, client_id: str) -> bool:
    """Validate that the logo file exists on the server."""
    if not logo_url.startswith('/api/files/'):
        # External URL - assume it exists (we can't validate external URLs)
        return True
    
    # Extract filename from internal API path: /api/files/clients/{client_id}/logos/{filename}
    try:
        parts = logo_url.split('/')
        if len(parts) >= 6 and parts[3] == 'clients' and parts[5] == 'logos':
            url_client_id = parts[4]
            filename = parts[6]
            
            # Ensure the client_id matches
            if url_client_id != client_id:
                return False
            
            # Check if file exists in the uploads directory
            from app.utils.file_upload import file_upload_handler
            file_info = file_upload_handler.get_logo_info(filename, client_id)
            return file_info is not None
        return False
    except Exception:
        return False

# === CLIENT SETTINGS ENDPOINTS ===

@router.get("/settings", response_model=ClientSettingsResponse)
async def get_client_settings(current_user: AdminUserResponse = Depends(get_current_admin_user)):
    """Get client settings and branding configuration."""
    try:
        # Query client settings using Supabase
        result = db.client.table('client_settings').select('*').eq('client_id', current_user.client_id).execute()
        
        if not result.data:
            # Create default settings for client
            settings_id = str(uuid.uuid4())
            new_settings = {
                'id': settings_id,
                'client_id': current_user.client_id
            }
            
            insert_result = db.client.table('client_settings').insert(new_settings).execute()
            if insert_result.data:
                settings = insert_result.data[0]
            else:
                raise HTTPException(status_code=500, detail="Failed to create default settings")
        else:
            settings = result.data[0]
        
        return ClientSettingsResponse(
            id=str(settings['id']),
            client_id=str(settings['client_id']),
            logo_url=settings.get('logo_url'),
            favicon_url=settings.get('favicon_url'),
            brand_colors=settings.get('brand_colors'),
            font_preferences=settings.get('font_preferences'),
            default_theme_id=str(settings['default_theme_id']) if settings.get('default_theme_id') else None,
            default_form_settings=settings.get('default_form_settings') or {},
            custom_domain=settings.get('custom_domain'),
            custom_domain_verified=settings.get('custom_domain_verified') or False,
            white_label_enabled=settings.get('white_label_enabled') or False,
            from_email=settings.get('from_email'),
            reply_to_email=settings.get('reply_to_email'),
            webhook_url=settings.get('webhook_url'),
            plan_type=settings.get('plan_type') or 'free',
            monthly_form_limit=settings.get('monthly_form_limit') or 1000,
            monthly_response_limit=settings.get('monthly_response_limit') or 10000,
            created_at=datetime.fromisoformat(settings['created_at'].replace('Z', '+00:00')) if settings.get('created_at') else None,
            updated_at=datetime.fromisoformat(settings['updated_at'].replace('Z', '+00:00')) if settings.get('updated_at') else None
        )
        
    except Exception as e:
        logger.error(f"Failed to get client settings: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve client settings")

@router.put("/settings", response_model=ClientSettingsResponse)
async def update_client_settings(
    settings_request: ClientSettingsRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Update client settings and branding."""
    try:
        # Validate logo file existence if logo_url is provided
        if settings_request.logo_url:
            if not _validate_logo_file_exists(settings_request.logo_url, current_user.client_id):
                raise HTTPException(
                    status_code=400, 
                    detail="Logo file does not exist or is not accessible"
                )
        
        # Build update data from non-None fields
        update_data = {}
        for field_name, field_value in settings_request.dict(exclude_unset=True).items():
            if field_value is not None:
                update_data[field_name] = field_value
        
        if update_data:
            # Add updated_at timestamp
            update_data['updated_at'] = datetime.utcnow().isoformat()
            
            # Update using Supabase
            result = db.client.table('client_settings').update(update_data).eq('client_id', current_user.client_id).execute()
            
            if not result.data:
                raise HTTPException(status_code=404, detail="Client settings not found")
        
        # Return updated settings
        return await get_client_settings(current_user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update client settings: {e}")
        raise HTTPException(status_code=500, detail="Failed to update client settings")