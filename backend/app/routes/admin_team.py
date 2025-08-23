"""
Admin Team API - Team Member Management

This module provides API endpoints for:
1. Team member listing and management
2. Team member invitation system
3. Role and permission management
4. Team member status updates
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, EmailStr
from typing import List, Literal, Optional
import logging
from datetime import datetime, timedelta
import uuid
import secrets

from app.database import db
from app.utils.response_helpers import success_response, error_response
from app.routes.admin_auth import AdminUserResponse, get_current_admin_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin/team", tags=["admin-team"])

# === PYDANTIC MODELS ===

class TeamInviteRequest(BaseModel):
    """Request to invite a new team member."""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    role: Literal["admin", "editor", "viewer"] = Field("viewer")

class TeamMemberResponse(BaseModel):
    """Response model for team member information."""
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    last_login_at: Optional[datetime] = None
    invitation_status: str  # "accepted", "pending", "expired"
    created_at: datetime

# === TEAM MANAGEMENT ENDPOINTS ===

@router.get("/members", response_model=List[TeamMemberResponse])
async def get_team_members(current_user: AdminUserResponse = Depends(get_current_admin_user)):
    """Get all team members for the client."""
    try:
        # Query team members using Supabase
        result = db.client.table('admin_users').select(
            'id, email, first_name, last_name, role, is_active, last_login_at, invitation_expires, created_at'
        ).eq('client_id', current_user.client_id).order('created_at', desc=True).execute()
        
        team_members = []
        
        for user in result.data:
            invitation_status = "accepted"
            if user.get('invitation_expires'):
                expires_at = datetime.fromisoformat(user['invitation_expires'].replace('Z', '+00:00'))
                if expires_at > datetime.now(expires_at.tzinfo):
                    invitation_status = "pending"
                else:
                    invitation_status = "expired"
            
            team_members.append(TeamMemberResponse(
                id=str(user['id']),
                email=user['email'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                role=user['role'],
                is_active=user['is_active'],
                last_login_at=datetime.fromisoformat(user['last_login_at'].replace('Z', '+00:00')) if user.get('last_login_at') else None,
                invitation_status=invitation_status,
                created_at=datetime.fromisoformat(user['created_at'].replace('Z', '+00:00'))
            ))
        
        return team_members
        
    except Exception as e:
        logger.error(f"Failed to get team members: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve team members")

@router.post("/invite", response_model=TeamMemberResponse)
async def invite_team_member(
    invite_request: TeamInviteRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Invite a new team member."""
    try:
        # Check if user already exists
        existing_user = db.client.table('admin_users').select('id').eq('email', invite_request.email).execute()
        if existing_user.data:
            raise HTTPException(status_code=409, detail="User with this email already exists")
        
        # Create invitation
        user_id = str(uuid.uuid4())
        invitation_token = secrets.token_urlsafe(32)
        invitation_expires = (datetime.now() + timedelta(days=7)).isoformat()
        
        # Set permissions based on role
        permissions = {
            "admin": ["forms:*", "analytics:*", "team:read", "settings:read"],
            "editor": ["forms:read", "forms:write", "analytics:read"],
            "viewer": ["forms:read", "analytics:read"]
        }.get(invite_request.role, ["forms:read"])
        
        # Create new team member invitation
        new_user_data = {
            'id': user_id,
            'client_id': current_user.client_id,
            'email': invite_request.email,
            'password_hash': "PENDING",
            'first_name': invite_request.first_name,
            'last_name': invite_request.last_name,
            'role': invite_request.role,
            'permissions': permissions,
            'is_active': False,
            'invitation_token': invitation_token,
            'invitation_expires': invitation_expires,
            'created_by_user_id': current_user.id
        }
        
        result = db.client.table('admin_users').insert(new_user_data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create team member invitation")
        
        created_user = result.data[0]
        
        # TODO: Send invitation email with invitation_token
        logger.info(f"Team member invited: {invite_request.email} with token: {invitation_token}")
        
        return TeamMemberResponse(
            id=user_id,
            email=invite_request.email,
            first_name=invite_request.first_name,
            last_name=invite_request.last_name,
            role=invite_request.role,
            is_active=False,
            last_login_at=None,
            invitation_status="pending",
            created_at=datetime.fromisoformat(created_user['created_at'].replace('Z', '+00:00'))
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to invite team member: {e}")
        raise HTTPException(status_code=500, detail="Failed to invite team member")

@router.delete("/members/{user_id}")
async def remove_team_member(
    user_id: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Remove a team member."""
    try:
        # Only owners and admins can remove team members
        if current_user.role not in ["owner", "admin"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        # Check if user exists and is in same client
        user_result = db.client.table('admin_users').select('id').eq('id', user_id).eq('client_id', current_user.client_id).execute()
        
        if not user_result.data:
            raise HTTPException(status_code=404, detail="Team member not found")
        
        # Cannot remove yourself
        if user_id == current_user.id:
            raise HTTPException(status_code=400, detail="Cannot remove yourself")
        
        # Deactivate user instead of deleting
        update_result = db.client.table('admin_users').update({
            'is_active': False,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('id', user_id).execute()
        
        if not update_result.data:
            raise HTTPException(status_code=500, detail="Failed to remove team member")
        
        return success_response({"user_id": user_id}, "Team member removed successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to remove team member: {e}")
        raise HTTPException(status_code=500, detail="Failed to remove team member")

@router.put("/members/{user_id}/role")
async def update_team_member_role(
    user_id: str,
    role_data: dict,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Update a team member's role."""
    try:
        # Only owners and admins can update roles
        if current_user.role not in ["owner", "admin"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        new_role = role_data.get('role')
        if new_role not in ["admin", "editor", "viewer"]:
            raise HTTPException(status_code=400, detail="Invalid role")
        
        # Check if user exists and is in same client
        user_result = db.client.table('admin_users').select('id, role').eq('id', user_id).eq('client_id', current_user.client_id).execute()
        
        if not user_result.data:
            raise HTTPException(status_code=404, detail="Team member not found")
        
        # Cannot change your own role
        if user_id == current_user.id:
            raise HTTPException(status_code=400, detail="Cannot change your own role")
        
        # Set permissions based on new role
        permissions = {
            "admin": ["forms:*", "analytics:*", "team:read", "settings:read"],
            "editor": ["forms:read", "forms:write", "analytics:read"],
            "viewer": ["forms:read", "analytics:read"]
        }.get(new_role, ["forms:read"])
        
        # Update user role and permissions
        update_result = db.client.table('admin_users').update({
            'role': new_role,
            'permissions': permissions,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('id', user_id).execute()
        
        if not update_result.data:
            raise HTTPException(status_code=500, detail="Failed to update team member role")
        
        return success_response({
            "user_id": user_id, 
            "new_role": new_role
        }, "Team member role updated successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update team member role: {e}")
        raise HTTPException(status_code=500, detail="Failed to update team member role")

@router.put("/members/{user_id}/activate")
async def activate_team_member(
    user_id: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Activate a deactivated team member."""
    try:
        # Only owners and admins can activate members
        if current_user.role not in ["owner", "admin"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        # Check if user exists and is in same client
        user_result = db.client.table('admin_users').select('id, is_active').eq('id', user_id).eq('client_id', current_user.client_id).execute()
        
        if not user_result.data:
            raise HTTPException(status_code=404, detail="Team member not found")
        
        user = user_result.data[0]
        if user['is_active']:
            raise HTTPException(status_code=400, detail="Team member is already active")
        
        # Activate user
        update_result = db.client.table('admin_users').update({
            'is_active': True,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('id', user_id).execute()
        
        if not update_result.data:
            raise HTTPException(status_code=500, detail="Failed to activate team member")
        
        return success_response({
            "user_id": user_id
        }, "Team member activated successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to activate team member: {e}")
        raise HTTPException(status_code=500, detail="Failed to activate team member")