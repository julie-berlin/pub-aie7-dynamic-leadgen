"""
Admin API - Admin User Management and Client Configuration

This module provides API endpoints for:
1. Admin user authentication and management
2. Client settings and branding configuration
3. Form management for admin users
4. Team member invitation and role management
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Dict, Any, List, Optional, Literal
import logging
from datetime import datetime, timedelta
import uuid
import hashlib
import secrets
import jwt

from app.database import get_database_connection

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin", tags=["admin"])
security = HTTPBearer()

# JWT Configuration (should be in environment variables)
JWT_SECRET = "your-jwt-secret-key"  # This should be in environment variables
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# === PYDANTIC MODELS FOR ADMIN SYSTEM ===

class AdminUserRegister(BaseModel):
    """Request to register a new admin user."""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    client_id: str = Field(..., description="Client organization ID")
    role: Literal["owner", "admin", "editor", "viewer"] = Field("admin")

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class AdminUserLogin(BaseModel):
    """Request to log in an admin user."""
    email: EmailStr
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

class ClientSettingsResponse(BaseModel):
    """Response model for client settings."""
    id: str
    client_id: str
    logo_url: Optional[str]
    favicon_url: Optional[str]
    brand_colors: Optional[Dict[str, str]]
    font_preferences: Optional[Dict[str, str]]
    default_theme_id: Optional[str]
    default_form_settings: Dict[str, Any]
    custom_domain: Optional[str]
    custom_domain_verified: bool
    white_label_enabled: bool
    from_email: Optional[str]
    reply_to_email: Optional[str]
    webhook_url: Optional[str]
    plan_type: str
    monthly_form_limit: int
    monthly_response_limit: int
    created_at: datetime
    updated_at: datetime

class TeamInviteRequest(BaseModel):
    """Request to invite a team member."""
    email: EmailStr
    role: Literal["admin", "editor", "viewer"]
    first_name: str
    last_name: str

class TeamMemberResponse(BaseModel):
    """Response model for team members."""
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    last_login_at: Optional[datetime]
    invitation_status: Literal["pending", "accepted", "expired"]
    created_at: datetime

# === UTILITY FUNCTIONS ===

def hash_password(password: str) -> str:
    """Hash a password with salt."""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}:{password_hash.hex()}"

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    try:
        salt, stored_hash = hashed_password.split(':')
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return password_hash.hex() == stored_hash
    except ValueError:
        return False

def create_access_token(user_id: str, client_id: str) -> tuple[str, int]:
    """Create a JWT access token."""
    expiration = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    payload = {
        'user_id': user_id,
        'client_id': client_id,
        'exp': expiration,
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token, int(JWT_EXPIRATION_HOURS * 3600)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_admin_user(token_payload: dict = Depends(verify_token)) -> AdminUserResponse:
    """Get current admin user from token."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, client_id, email, first_name, last_name, role, permissions,
                       is_active, email_verified, last_login_at, login_count, created_at
                FROM admin_users
                WHERE id = %s AND is_active = true
            """, (token_payload['user_id'],))
            
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=401, detail="User not found or inactive")
            
            return AdminUserResponse(
                id=str(result[0]),
                client_id=str(result[1]),
                email=result[2],
                first_name=result[3],
                last_name=result[4],
                role=result[5],
                permissions=result[6] or [],
                is_active=result[7],
                email_verified=result[8],
                last_login_at=result[9],
                login_count=result[10],
                created_at=result[11]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get current user: {e}")
        raise HTTPException(status_code=500, detail="Failed to authenticate user")

# === AUTHENTICATION ENDPOINTS ===

@router.post("/auth/register", response_model=AdminTokenResponse)
async def register_admin_user(user_request: AdminUserRegister):
    """Register a new admin user."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Check if user already exists
            cursor.execute("SELECT id FROM admin_users WHERE email = %s", (user_request.email,))
            if cursor.fetchone():
                raise HTTPException(status_code=409, detail="User with this email already exists")
            
            # Check if client exists
            cursor.execute("SELECT id FROM clients WHERE id = %s", (user_request.client_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Client not found")
            
            # Create user
            user_id = str(uuid.uuid4())
            password_hash = hash_password(user_request.password)
            
            # Set permissions based on role
            permissions = {
                "owner": ["*"],
                "admin": ["forms:*", "analytics:*", "team:*", "settings:*"],
                "editor": ["forms:read", "forms:write", "analytics:read"],
                "viewer": ["forms:read", "analytics:read"]
            }.get(user_request.role, ["forms:read"])
            
            cursor.execute("""
                INSERT INTO admin_users 
                (id, client_id, email, password_hash, first_name, last_name, role, permissions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING created_at
            """, (
                user_id, user_request.client_id, user_request.email, password_hash,
                user_request.first_name, user_request.last_name, user_request.role,
                permissions
            ))
            
            created_at = cursor.fetchone()[0]
            conn.commit()
            
            # Create access token
            access_token, expires_in = create_access_token(user_id, user_request.client_id)
            
            user_response = AdminUserResponse(
                id=user_id,
                client_id=user_request.client_id,
                email=user_request.email,
                first_name=user_request.first_name,
                last_name=user_request.last_name,
                role=user_request.role,
                permissions=permissions,
                is_active=True,
                email_verified=False,
                last_login_at=None,
                login_count=0,
                created_at=created_at
            )
            
            return AdminTokenResponse(
                access_token=access_token,
                expires_in=expires_in,
                user=user_response
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to register user: {e}")
        raise HTTPException(status_code=500, detail="Failed to register user")

@router.post("/auth/login", response_model=AdminTokenResponse)
async def login_admin_user(login_request: AdminUserLogin):
    """Log in an admin user."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Get user by email
            cursor.execute("""
                SELECT id, client_id, email, password_hash, first_name, last_name, role, 
                       permissions, is_active, email_verified, login_count, created_at
                FROM admin_users
                WHERE email = %s
            """, (login_request.email,))
            
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=401, detail="Invalid email or password")
            
            user_data = result
            if not user_data[8]:  # is_active
                raise HTTPException(status_code=401, detail="Account is deactivated")
            
            # Verify password
            if not verify_password(login_request.password, user_data[3]):
                raise HTTPException(status_code=401, detail="Invalid email or password")
            
            # Update login tracking
            cursor.execute("""
                UPDATE admin_users 
                SET last_login_at = NOW(), login_count = login_count + 1
                WHERE id = %s
                RETURNING last_login_at
            """, (user_data[0],))
            
            last_login = cursor.fetchone()[0]
            conn.commit()
            
            # Create access token
            access_token, expires_in = create_access_token(str(user_data[0]), str(user_data[1]))
            
            user_response = AdminUserResponse(
                id=str(user_data[0]),
                client_id=str(user_data[1]),
                email=user_data[2],
                first_name=user_data[4],
                last_name=user_data[5],
                role=user_data[6],
                permissions=user_data[7] or [],
                is_active=user_data[8],
                email_verified=user_data[9],
                last_login_at=last_login,
                login_count=user_data[10] + 1,
                created_at=user_data[11]
            )
            
            return AdminTokenResponse(
                access_token=access_token,
                expires_in=expires_in,
                user=user_response
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to login user: {e}")
        raise HTTPException(status_code=500, detail="Failed to login user")

@router.get("/auth/me", response_model=AdminUserResponse)
async def get_current_user(current_user: AdminUserResponse = Depends(get_current_admin_user)):
    """Get current authenticated user."""
    return current_user

# === CLIENT SETTINGS ENDPOINTS ===

@router.get("/client/settings", response_model=ClientSettingsResponse)
async def get_client_settings(current_user: AdminUserResponse = Depends(get_current_admin_user)):
    """Get client settings and branding configuration."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, client_id, logo_url, favicon_url, brand_colors, font_preferences,
                       default_theme_id, default_form_settings, custom_domain, custom_domain_verified,
                       white_label_enabled, from_email, reply_to_email, webhook_url,
                       plan_type, monthly_form_limit, monthly_response_limit, created_at, updated_at
                FROM client_settings
                WHERE client_id = %s
            """, (current_user.client_id,))
            
            result = cursor.fetchone()
            if not result:
                # Create default settings for client
                settings_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO client_settings (id, client_id)
                    VALUES (%s, %s)
                    RETURNING id, client_id, logo_url, favicon_url, brand_colors, font_preferences,
                             default_theme_id, default_form_settings, custom_domain, custom_domain_verified,
                             white_label_enabled, from_email, reply_to_email, webhook_url,
                             plan_type, monthly_form_limit, monthly_response_limit, created_at, updated_at
                """, (settings_id, current_user.client_id))
                result = cursor.fetchone()
                conn.commit()
            
            return ClientSettingsResponse(
                id=str(result[0]),
                client_id=str(result[1]),
                logo_url=result[2],
                favicon_url=result[3],
                brand_colors=result[4],
                font_preferences=result[5],
                default_theme_id=str(result[6]) if result[6] else None,
                default_form_settings=result[7] or {},
                custom_domain=result[8],
                custom_domain_verified=result[9] or False,
                white_label_enabled=result[10] or False,
                from_email=result[11],
                reply_to_email=result[12],
                webhook_url=result[13],
                plan_type=result[14] or 'free',
                monthly_form_limit=result[15] or 1000,
                monthly_response_limit=result[16] or 10000,
                created_at=result[17],
                updated_at=result[18]
            )
            
    except Exception as e:
        logger.error(f"Failed to get client settings: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve client settings")

@router.put("/client/settings", response_model=ClientSettingsResponse)
async def update_client_settings(
    settings_request: ClientSettingsRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Update client settings and branding."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Build dynamic update query
            update_fields = []
            update_values = []
            
            for field_name, field_value in settings_request.dict(exclude_unset=True).items():
                if field_value is not None:
                    update_fields.append(f"{field_name} = %s")
                    update_values.append(field_value)
            
            if update_fields:
                update_fields.append("updated_at = NOW()")
                update_values.append(current_user.client_id)
                
                query = f"""
                    UPDATE client_settings 
                    SET {', '.join(update_fields)}
                    WHERE client_id = %s
                    RETURNING updated_at
                """
                cursor.execute(query, update_values)
                conn.commit()
            
            # Return updated settings
            return await get_client_settings(current_user)
            
    except Exception as e:
        logger.error(f"Failed to update client settings: {e}")
        raise HTTPException(status_code=500, detail="Failed to update client settings")

# === TEAM MANAGEMENT ENDPOINTS ===

@router.get("/team/members", response_model=List[TeamMemberResponse])
async def get_team_members(current_user: AdminUserResponse = Depends(get_current_admin_user)):
    """Get all team members for the client."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, email, first_name, last_name, role, is_active, 
                       last_login_at, invitation_expires, created_at
                FROM admin_users
                WHERE client_id = %s
                ORDER BY created_at DESC
            """, (current_user.client_id,))
            
            results = cursor.fetchall()
            team_members = []
            
            for row in results:
                invitation_status = "accepted"
                if row[7]:  # invitation_expires
                    if row[7] > datetime.now():
                        invitation_status = "pending"
                    else:
                        invitation_status = "expired"
                
                team_members.append(TeamMemberResponse(
                    id=str(row[0]),
                    email=row[1],
                    first_name=row[2],
                    last_name=row[3],
                    role=row[4],
                    is_active=row[5],
                    last_login_at=row[6],
                    invitation_status=invitation_status,
                    created_at=row[8]
                ))
            
            return team_members
            
    except Exception as e:
        logger.error(f"Failed to get team members: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve team members")

@router.post("/team/invite", response_model=TeamMemberResponse)
async def invite_team_member(
    invite_request: TeamInviteRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Invite a new team member."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Check if user already exists
            cursor.execute("SELECT id FROM admin_users WHERE email = %s", (invite_request.email,))
            if cursor.fetchone():
                raise HTTPException(status_code=409, detail="User with this email already exists")
            
            # Create invitation
            user_id = str(uuid.uuid4())
            invitation_token = secrets.token_urlsafe(32)
            invitation_expires = datetime.now() + timedelta(days=7)
            
            # Set permissions based on role
            permissions = {
                "admin": ["forms:*", "analytics:*", "team:read", "settings:read"],
                "editor": ["forms:read", "forms:write", "analytics:read"],
                "viewer": ["forms:read", "analytics:read"]
            }.get(invite_request.role, ["forms:read"])
            
            cursor.execute("""
                INSERT INTO admin_users 
                (id, client_id, email, password_hash, first_name, last_name, role, permissions,
                 is_active, invitation_token, invitation_expires, created_by_user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING created_at
            """, (
                user_id, current_user.client_id, invite_request.email, "PENDING",
                invite_request.first_name, invite_request.last_name, invite_request.role,
                permissions, False, invitation_token, invitation_expires, current_user.id
            ))
            
            created_at = cursor.fetchone()[0]
            conn.commit()
            
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
                created_at=created_at
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to invite team member: {e}")
        raise HTTPException(status_code=500, detail="Failed to invite team member")

@router.delete("/team/members/{user_id}")
async def remove_team_member(
    user_id: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Remove a team member."""
    try:
        # Only owners and admins can remove team members
        if current_user.role not in ["owner", "admin"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Check if user exists and is in same client
            cursor.execute("""
                SELECT id FROM admin_users 
                WHERE id = %s AND client_id = %s
            """, (user_id, current_user.client_id))
            
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Team member not found")
            
            # Cannot remove yourself
            if user_id == current_user.id:
                raise HTTPException(status_code=400, detail="Cannot remove yourself")
            
            # Deactivate user instead of deleting
            cursor.execute("""
                UPDATE admin_users 
                SET is_active = false, updated_at = NOW()
                WHERE id = %s
            """, (user_id,))
            
            conn.commit()
            return {"status": "success", "message": "Team member removed successfully"}
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to remove team member: {e}")
        raise HTTPException(status_code=500, detail="Failed to remove team member")