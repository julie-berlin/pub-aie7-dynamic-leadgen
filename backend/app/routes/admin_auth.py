"""
Admin Authentication API - Admin User Login and Management
Separate from main admin_api.py to keep authentication logic isolated
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator
from typing import Dict, Any, List, Optional, Literal
import logging
from datetime import datetime, timedelta
import uuid
import hashlib
import secrets
import jwt

from app.database import db
from app.utils.response_helpers import success_response, error_response
from app.utils.admin_auth_unified import create_access_token, verify_token, hash_password, verify_password

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin/auth", tags=["admin-auth"])
security = HTTPBearer()

# === PYDANTIC MODELS ===

class AdminUserLogin(BaseModel):
    """Request to log in an admin user."""
    email: str  # Changed from EmailStr to allow .test domains
    password: str

class AdminUserResponse(BaseModel):
    """Response model for admin user data."""
    id: str
    client_id: str
    email: str
    first_name: str
    last_name: str
    role: str
    permissions: List[str]
    is_active: bool
    email_verified: bool
    last_login_at: Optional[datetime]
    login_count: int
    created_at: datetime

class AdminTokenResponse(BaseModel):
    """Response model for authentication."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: AdminUserResponse

# === UTILITY FUNCTIONS ===

def verify_token_from_credentials(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token from HTTP Authorization header."""
    token_payload = verify_token(credentials.credentials)
    if not token_payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return token_payload

def get_current_admin_user(token_payload: dict = Depends(verify_token_from_credentials)) -> AdminUserResponse:
    """Get current admin user from token."""
    try:
        # Get user by ID using Supabase client
        result = db.client.table('admin_users').select('*').eq('id', token_payload['user_id']).execute()
        
        if not result.data:
            raise HTTPException(status_code=401, detail="User not found or inactive")
        
        user_data = result.data[0]
        
        # Handle JSONB permissions field properly
        permissions = user_data['permissions'] if user_data['permissions'] else []
        if isinstance(permissions, str):
            import json
            permissions = json.loads(permissions)
        
        return AdminUserResponse(
            id=str(user_data['id']),
            client_id=str(token_payload['client_id']),  # Get client_id from JWT, not database
            email=user_data['email'],
            first_name=user_data.get('first_name') or '',
            last_name=user_data.get('last_name') or '',
            role=user_data.get('role') or 'admin',
            permissions=permissions,
            is_active=user_data.get('is_active', True),
            email_verified=user_data.get('email_verified', False),
            last_login_at=user_data.get('last_login_at'),
            login_count=0,  # Default to 0 since column doesn't exist
            created_at=user_data.get('created_at')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get current user: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")

# === AUTHENTICATION ENDPOINTS ===

@router.post("/login", response_model=AdminTokenResponse)
async def login_admin_user(login_request: AdminUserLogin):
    """Log in an admin user."""
    try:
        # Get user by email using Supabase client
        result = db.client.table('admin_users').select('*').eq('email', login_request.email).execute()
        
        if not result.data:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        user_data = result.data[0]
        
        if not user_data['is_active']:
            raise HTTPException(status_code=401, detail="Account is deactivated")
        
        # Verify password
        if not verify_password(login_request.password, user_data['password_hash']):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Update login tracking (only update last_login_at since login_count column doesn't exist)
        from datetime import datetime, timezone
        current_time = datetime.now(timezone.utc).isoformat()
        update_result = db.client.table('admin_users').update({
            'last_login_at': current_time
        }).eq('id', user_data['id']).execute()
        
        # Create access token
        access_token, expires_in = create_access_token(str(user_data['id']), str(user_data['client_id']))
        
        # Handle JSONB permissions field properly
        permissions = user_data['permissions'] if user_data['permissions'] else []
        if isinstance(permissions, str):
            import json
            permissions = json.loads(permissions)
        
        user_response = AdminUserResponse(
            id=str(user_data['id']),
            client_id=str(user_data['client_id']),
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            role=user_data['role'],
            permissions=permissions,
            is_active=user_data['is_active'],
            email_verified=user_data.get('email_verified', False),
            last_login_at=current_time,  # Use the timestamp we just set
            login_count=0,  # Default to 0 since column doesn't exist
            created_at=user_data['created_at']
        )
        
        token_response = AdminTokenResponse(
            access_token=access_token,
            expires_in=expires_in,
            user=user_response
        )
        
        # Convert to dict with proper datetime serialization
        response_data = token_response.model_dump()
        # Convert datetime fields to ISO strings
        if 'user' in response_data and response_data['user']:
            user_data = response_data['user']
            if 'last_login_at' in user_data and user_data['last_login_at']:
                user_data['last_login_at'] = user_data['last_login_at'].isoformat() if hasattr(user_data['last_login_at'], 'isoformat') else str(user_data['last_login_at'])
            if 'created_at' in user_data and user_data['created_at']:
                user_data['created_at'] = user_data['created_at'].isoformat() if hasattr(user_data['created_at'], 'isoformat') else str(user_data['created_at'])
        
        return success_response(
            data=response_data,
            message="Login successful"
        )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to login user: {e}")
        raise HTTPException(status_code=500, detail="Failed to login user")

@router.get("/me")
async def get_current_user(current_user: AdminUserResponse = Depends(get_current_admin_user)):
    """Get current authenticated user."""
    # Convert to dict with proper datetime serialization
    user_data = current_user.model_dump()
    if 'last_login_at' in user_data and user_data['last_login_at']:
        user_data['last_login_at'] = user_data['last_login_at'].isoformat() if hasattr(user_data['last_login_at'], 'isoformat') else str(user_data['last_login_at'])
    if 'created_at' in user_data and user_data['created_at']:
        user_data['created_at'] = user_data['created_at'].isoformat() if hasattr(user_data['created_at'], 'isoformat') else str(user_data['created_at'])
    
    return success_response(
        data=user_data,
        message="User retrieved successfully"
    )

@router.post("/refresh")
async def refresh_token(current_user: AdminUserResponse = Depends(get_current_admin_user)):
    """Refresh access token."""
    try:
        # Create new access token
        access_token, expires_in = create_access_token(current_user.id, current_user.client_id)
        
        token_response = AdminTokenResponse(
            access_token=access_token,
            expires_in=expires_in,
            user=current_user
        )
        
        # Convert to dict with proper datetime serialization
        response_data = token_response.model_dump()
        if 'user' in response_data and response_data['user']:
            user_data = response_data['user']
            if 'last_login_at' in user_data and user_data['last_login_at']:
                user_data['last_login_at'] = user_data['last_login_at'].isoformat() if hasattr(user_data['last_login_at'], 'isoformat') else str(user_data['last_login_at'])
            if 'created_at' in user_data and user_data['created_at']:
                user_data['created_at'] = user_data['created_at'].isoformat() if hasattr(user_data['created_at'], 'isoformat') else str(user_data['created_at'])
        
        return success_response(
            data=response_data,
            message="Token refreshed successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to refresh token: {e}")
        raise HTTPException(status_code=500, detail="Failed to refresh token")