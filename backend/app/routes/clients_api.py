"""
Clients API - RESTful Client/Business Management Endpoints

This module provides clean RESTful API endpoints for:
1. Managing client business information
2. Complete CRUD operations for clients
3. All operations are automatically scoped to the authenticated client

SECURITY: All endpoints enforce row-level security - each client can only
access and modify their own information. Cross-client access attempts return 404.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any, Optional
import logging

from app.database import db
from app.routes.admin_auth import AdminUserResponse
# from app.routes.admin_api import get_current_admin_user  # TODO: Re-enable when auth is ready
from app.routes.admin_auth import get_current_admin_user
from app.utils.response_helpers import success_response, error_response
from pydantic_models import (
    ClientResponse,
    ClientUpdateRequest,
    ClientPatchRequest
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/clients", tags=["clients"])

# === RESTful ENDPOINTS ===

@router.get("/me", response_model=ClientResponse)
async def get_current_client(
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """
    Get the current authenticated client's information.
    Convenience endpoint that doesn't require passing client_id.
    """
    return await get_client(current_user.client_id, current_user)

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """
    Get client information by ID.
    Returns 404 if client doesn't exist OR if trying to access another client's data.
    """
    try:
        # Security check - can only access own client data
        if client_id != current_user.client_id:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Use Supabase client
        
        result = db.client.table("clients")\
            .select("*")\
            .eq("id", client_id)\
            .execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Client not found")
        
        row = result.data[0]
        
        # Fetch all data from client_settings
        settings_data = {}
        try:
            settings_result = db.client.table('client_settings')\
                .select('*')\
                .eq('client_id', client_id)\
                .execute()
            
            if settings_result.data:
                settings_data = settings_result.data[0]
        except Exception as settings_error:
            # Don't fail the request if settings lookup fails, just log it
            logger.warning(f"Failed to fetch client_settings for client {client_id}: {settings_error}")
        
        client_response = ClientResponse(
            id=str(row["id"]),
            name=row["name"],
            legal_name=row.get("legal_name"),
            email=row["email"],
            owner_name=row["owner_name"],
            contact_name=row.get("contact_name"),
            business_type=row.get("business_type"),
            industry=row.get("industry"),
            address=row.get("address"),
            phone=row.get("phone"),
            website=row.get("website"),
            background=row.get("background"),
            goals=row.get("goals"),
            target_audience=row.get("target_audience"),
            logo_url=settings_data.get("logo_url"),
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
        
        return success_response(
            data=client_response.model_dump(mode='json'),
            message="Client retrieved successfully"
        )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get client: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve client")

@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: str,
    client_request: ClientUpdateRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """
    Fully update client information (PUT - requires all fields).
    Returns 404 if trying to update another client's data.
    """
    try:
        # Security check - can only update own client data
        if client_id != current_user.client_id:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Use Supabase client
        
        # First check if client exists
        existing = db.client.table("clients")\
            .select("id")\
            .eq("id", client_id)\
            .execute()
        
        if not existing.data:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Update client with all fields
        update_data = {
            "name": client_request.name,
            "legal_name": client_request.legal_name,
            "background": client_request.business_description,  # Maps to background field
            "industry": client_request.industry,
            "website": client_request.website_url,
            "email": client_request.contact_email,
            "phone": client_request.contact_phone,
            "address": client_request.business_address,
            "business_type": client_request.business_type,
            "target_audience": client_request.target_audience,
            "goals": client_request.goals
        }
        
        result = db.client.table("clients")\
            .update(update_data)\
            .eq("id", client_id)\
            .execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Failed to update client")
        
        # Return updated client
        return await get_client(client_id, current_user)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update client: {e}")
        raise HTTPException(status_code=500, detail="Failed to update client")

@router.patch("/{client_id}", response_model=ClientResponse)
async def patch_client(
    client_id: str,
    client_request: ClientPatchRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """
    Partially update client information (PATCH - only specified fields).
    Returns 404 if trying to update another client's data.
    """
    try:
        # Security check - can only update own client data
        if client_id != current_user.client_id:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Use Supabase client
        
        # First check if client exists
        existing = db.client.table("clients")\
            .select("id")\
            .eq("id", client_id)\
            .execute()
        
        if not existing.data:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Build dynamic update data for clients table
        update_data = {}
        
        # Map request fields to database columns (exclude logo_url - that goes to client_settings)
        field_mapping = {
            'name': 'name',
            'legal_name': 'legal_name',
            'business_description': 'background',
            'industry': 'industry',
            'website_url': 'website',
            'contact_email': 'email',
            'contact_phone': 'phone',
            'business_address': 'address',
            'business_type': 'business_type',
            'target_audience': 'target_audience',
            'goals': 'goals'
        }
        
        for request_field, db_field in field_mapping.items():
            value = getattr(client_request, request_field, None)
            if value is not None:
                update_data[db_field] = value
        
        # Update clients table if there's data to update
        if update_data:
            result = db.client.table("clients")\
                .update(update_data)\
                .eq("id", client_id)\
                .execute()
            
            if not result.data:
                raise HTTPException(status_code=404, detail="Failed to update client")
        
        # Handle logo_url separately - update client_settings table
        logo_url = getattr(client_request, 'logo_url', None)
        if logo_url is not None:
            from datetime import datetime
            import uuid
            
            # Check if client_settings record exists
            settings_result = db.client.table('client_settings').select('id').eq('client_id', client_id).execute()
            
            settings_update = {
                'logo_url': logo_url,
                'updated_at': datetime.now(datetime.UTC).isoformat()
            }
            
            if settings_result.data:
                # Update existing record
                settings_update_result = db.client.table('client_settings').update(settings_update).eq('client_id', client_id).execute()
                if not settings_update_result.data:
                    logger.warning(f"Failed to update client_settings logo_url for client {client_id}")
            else:
                # Create new record
                new_settings = {
                    'id': str(uuid.uuid4()),
                    'client_id': client_id,
                    **settings_update
                }
                
                settings_insert_result = db.client.table('client_settings').insert(new_settings).execute()
                if not settings_insert_result.data:
                    logger.warning(f"Failed to create client_settings record for client {client_id}")
        
        # Return updated client
        return await get_client(client_id, current_user)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to patch client: {e}")
        raise HTTPException(status_code=500, detail="Failed to update client")

@router.put("/me", response_model=ClientResponse)
async def update_current_client(
    client_request: ClientUpdateRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """
    Update the current authenticated client's information (full update).
    Convenience endpoint that doesn't require passing client_id.
    """
    return await update_client(current_user.client_id, client_request, current_user)

@router.patch("/me", response_model=ClientResponse)
async def patch_current_client(
    client_request: ClientPatchRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """
    Partially update the current authenticated client's information.
    Convenience endpoint that doesn't require passing client_id.
    """
    return await patch_client(current_user.client_id, client_request, current_user)

# Note: We don't provide DELETE endpoints for clients as they shouldn't be able to delete themselves
# This would need to be handled by a super-admin or through a different process