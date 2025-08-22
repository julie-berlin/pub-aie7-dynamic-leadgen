"""
Admin API - Admin User Management and Client Configuration

This module provides API endpoints for:
1. Admin user authentication and management
2. Client settings and branding configuration
3. Form management for admin users
4. Team member invitation and role management
"""

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, EmailStr, validator
import re
from urllib.parse import urlparse
from pathlib import Path
from typing import Dict, Any, List, Optional, Literal
import logging
from datetime import datetime, timedelta
import uuid
import hashlib
import secrets
import jwt

from app.database import get_database_connection
from app.utils.file_upload import validate_and_store_logo, remove_logo
from app.utils.response_helpers import success_response, error_response
# Import working admin auth functions
from app.routes.admin_auth import get_current_admin_user as get_working_admin_user

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

# Import AdminUserResponse from admin_auth.py
from app.routes.admin_auth import AdminUserResponse

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

    @validator('logo_url')
    def validate_logo_url(cls, v):
        """Validate logo URL format and path."""
        if v is None:
            return v
        
        # Check if it's a valid URL format or relative path
        if v.startswith('http://') or v.startswith('https://'):
            # External URL - validate URL format
            parsed = urlparse(v)
            if not parsed.netloc:
                raise ValueError('Invalid URL format')
        elif v.startswith('/api/files/'):
            # Internal API path - validate format
            if not re.match(r'^/api/files/clients/[a-zA-Z0-9-]+/logos/[a-zA-Z0-9._-]+$', v):
                raise ValueError('Invalid internal logo path format')
        else:
            raise ValueError('Logo URL must be either an external URL (http/https) or internal API path (/api/files/)')
        
        return v

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

class LeadResponse(BaseModel):
    """Response model for lead data."""
    session_id: str
    form_id: str
    form_title: str
    lead_status: Literal["yes", "maybe", "no", "unknown"]
    completion_type: Optional[str]
    final_score: int
    started_at: datetime
    completed_at: Optional[datetime]
    last_updated: datetime
    # Contact info (only for qualified leads)
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    # Conversion tracking
    actual_conversion: Optional[bool] = None
    conversion_date: Optional[datetime] = None
    conversion_value: Optional[float] = None
    conversion_type: Optional[str] = None
    # UTM data
    utm_source: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_medium: Optional[str] = None

class LeadConversionUpdate(BaseModel):
    """Request model for updating lead conversion status."""
    actual_conversion: bool
    conversion_date: Optional[datetime] = None
    conversion_value: Optional[float] = Field(None, ge=0)
    conversion_type: Optional[str] = None
    notes: Optional[str] = None

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

# Use the working admin auth function from admin_auth.py instead of broken psycopg2 version
get_current_admin_user = get_working_admin_user

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

@router.put("/client/settings", response_model=ClientSettingsResponse)
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
            
    except HTTPException:
        raise
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

# === LOGO UPLOAD ENDPOINTS ===

@router.post("/upload/logo")
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
        
        # Update the client_settings table with the new logo URL
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Check if client_settings record exists
            cursor.execute("""
                SELECT id FROM client_settings WHERE client_id = %s
            """, (current_user.client_id,))
            
            if cursor.fetchone():
                # Update existing record
                cursor.execute("""
                    UPDATE client_settings 
                    SET logo_url = %s, updated_at = NOW()
                    WHERE client_id = %s
                """, (upload_result['url'], current_user.client_id))
            else:
                # Create new record
                cursor.execute("""
                    INSERT INTO client_settings (id, client_id, logo_url)
                    VALUES (%s, %s, %s)
                """, (str(uuid.uuid4()), current_user.client_id, upload_result['url']))
            
            conn.commit()
        
        return {
            "success": True,
            "data": {
                "logo_url": upload_result['url'],
                "filename": upload_result['filename'],
                "size": upload_result['size'],
                "uploaded_at": upload_result['uploaded_at']
            },
            "message": "Logo uploaded successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to upload logo: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload logo")

@router.delete("/upload/logo/{filename}")
async def delete_logo(
    filename: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Delete a logo file."""
    try:
        # Delete the file
        success = remove_logo(filename, current_user.client_id)
        
        if success:
            # Update client_settings to remove logo_url
            conn = get_database_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE client_settings 
                    SET logo_url = NULL, updated_at = NOW()
                    WHERE client_id = %s
                """, (current_user.client_id,))
                conn.commit()
            
            return {
                "success": True,
                "data": {"filename": filename},
                "message": "Logo deleted successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Logo not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete logo: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete logo")

# === LEADS MANAGEMENT ENDPOINTS ===

@router.get("/leads")
async def get_leads(
    form_id: Optional[str] = None,
    status: Optional[str] = None,
    converted: Optional[bool] = None,
    limit: int = 100,
    offset: int = 0,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get all leads for the client with optional filtering."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Build the WHERE clause with filters
            where_conditions = ["ls.client_id = %s"]
            query_params = [current_user.client_id]
            
            if form_id:
                where_conditions.append("ls.form_id = %s")
                query_params.append(form_id)
            
            if status:
                where_conditions.append("ls.lead_status = %s")
                query_params.append(status)
            
            if converted is not None:
                if converted:
                    where_conditions.append("lo.actual_conversion = true")
                else:
                    where_conditions.append("(lo.actual_conversion = false OR lo.actual_conversion IS NULL)")
            
            where_clause = " AND ".join(where_conditions)
            
            # Add limit and offset to params
            query_params.extend([limit, offset])
            
            query = f"""
                SELECT 
                    ls.session_id,
                    ls.form_id,
                    f.title as form_title,
                    ls.lead_status,
                    ls.completion_type,
                    ls.final_score,
                    ls.started_at,
                    ls.completed_at,
                    ls.last_updated,
                    -- Contact info from responses
                    MAX(CASE WHEN r.question_text ILIKE '%name%' AND r.question_text NOT ILIKE '%business%' THEN r.answer END) as contact_name,
                    MAX(CASE WHEN r.question_text ILIKE '%email%' THEN r.answer END) as contact_email,
                    MAX(CASE WHEN r.question_text ILIKE '%phone%' THEN r.answer END) as contact_phone,
                    -- Conversion data
                    lo.actual_conversion,
                    lo.conversion_date,
                    lo.conversion_value,
                    lo.conversion_type,
                    -- UTM data
                    td.utm_source,
                    td.utm_campaign,
                    td.utm_medium
                FROM lead_sessions ls
                LEFT JOIN forms f ON ls.form_id = f.id
                LEFT JOIN responses r ON ls.session_id = r.session_id
                LEFT JOIN lead_outcomes lo ON ls.session_id = lo.session_id
                LEFT JOIN tracking_data td ON ls.session_id = td.session_id
                WHERE {where_clause}
                GROUP BY 
                    ls.session_id, ls.form_id, f.title, ls.lead_status, ls.completion_type,
                    ls.final_score, ls.started_at, ls.completed_at, ls.last_updated,
                    lo.actual_conversion, lo.conversion_date, lo.conversion_value, lo.conversion_type,
                    td.utm_source, td.utm_campaign, td.utm_medium
                ORDER BY ls.started_at DESC
                LIMIT %s OFFSET %s
            """
            
            cursor.execute(query, query_params)
            results = cursor.fetchall()
            
            leads = []
            for row in results:
                leads.append({
                    "session_id": row[0],
                    "form_id": str(row[1]),
                    "form_title": row[2] or "Unknown Form",
                    "lead_status": row[3] or "unknown",
                    "completion_type": row[4],
                    "final_score": row[5] or 0,
                    "started_at": row[6],
                    "completed_at": row[7],
                    "last_updated": row[8],
                    "contact_name": row[9],
                    "contact_email": row[10],
                    "contact_phone": row[11],
                    "actual_conversion": row[12],
                    "conversion_date": row[13],
                    "conversion_value": float(row[14]) if row[14] else None,
                    "conversion_type": row[15],
                    "utm_source": row[16],
                    "utm_campaign": row[17],
                    "utm_medium": row[18]
                })
            
            return success_response(
                data={
                    "leads": leads,
                    "pagination": {
                        "limit": limit,
                        "offset": offset,
                        "total": len(leads)
                    }
                },
                message=f"Retrieved {len(leads)} leads"
            )
            
    except Exception as e:
        logger.error(f"Failed to get leads: {e}")
        return error_response("Failed to retrieve leads", 500)

@router.get("/leads/{session_id}")
async def get_lead_detail(
    session_id: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get detailed information about a specific lead."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    ls.session_id,
                    ls.form_id,
                    f.title as form_title,
                    ls.lead_status,
                    ls.completion_type,
                    ls.final_score,
                    ls.started_at,
                    ls.completed_at,
                    ls.last_updated,
                    -- Contact info from responses
                    MAX(CASE WHEN r.question_text ILIKE '%name%' AND r.question_text NOT ILIKE '%business%' THEN r.answer END) as contact_name,
                    MAX(CASE WHEN r.question_text ILIKE '%email%' THEN r.answer END) as contact_email,
                    MAX(CASE WHEN r.question_text ILIKE '%phone%' THEN r.answer END) as contact_phone,
                    -- Conversion data
                    lo.actual_conversion,
                    lo.conversion_date,
                    lo.conversion_value,
                    lo.conversion_type,
                    -- UTM data
                    td.utm_source,
                    td.utm_campaign,
                    td.utm_medium
                FROM lead_sessions ls
                LEFT JOIN forms f ON ls.form_id = f.id
                LEFT JOIN responses r ON ls.session_id = r.session_id
                LEFT JOIN lead_outcomes lo ON ls.session_id = lo.session_id
                LEFT JOIN tracking_data td ON ls.session_id = td.session_id
                WHERE ls.session_id = %s AND ls.client_id = %s
                GROUP BY 
                    ls.session_id, ls.form_id, f.title, ls.lead_status, ls.completion_type,
                    ls.final_score, ls.started_at, ls.completed_at, ls.last_updated,
                    lo.actual_conversion, lo.conversion_date, lo.conversion_value, lo.conversion_type,
                    td.utm_source, td.utm_campaign, td.utm_medium
            """, (session_id, current_user.client_id))
            
            result = cursor.fetchone()
            if not result:
                return error_response("Lead not found", 404)
            
            lead_data = {
                "session_id": result[0],
                "form_id": str(result[1]),
                "form_title": result[2] or "Unknown Form",
                "lead_status": result[3] or "unknown",
                "completion_type": result[4],
                "final_score": result[5] or 0,
                "started_at": result[6],
                "completed_at": result[7],
                "last_updated": result[8],
                "contact_name": result[9],
                "contact_email": result[10],
                "contact_phone": result[11],
                "actual_conversion": result[12],
                "conversion_date": result[13],
                "conversion_value": float(result[14]) if result[14] else None,
                "conversion_type": result[15],
                "utm_source": result[16],
                "utm_campaign": result[17],
                "utm_medium": result[18]
            }
            
            return success_response(
                data={"lead": lead_data},
                message="Lead details retrieved successfully"
            )
            
    except Exception as e:
        logger.error(f"Failed to get lead detail: {e}")
        return error_response("Failed to retrieve lead details", 500)

@router.put("/leads/{session_id}/conversion")
async def update_lead_conversion(
    session_id: str,
    conversion_update: LeadConversionUpdate,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Update the conversion status of a lead."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Verify the lead belongs to this client
            cursor.execute("""
                SELECT ls.id FROM lead_sessions ls 
                WHERE ls.session_id = %s AND ls.client_id = %s
            """, (session_id, current_user.client_id))
            
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Lead not found")
            
            # Check if lead_outcome record exists
            cursor.execute("""
                SELECT id FROM lead_outcomes WHERE session_id = %s
            """, (session_id,))
            
            outcome_exists = cursor.fetchone()
            
            if outcome_exists:
                # Update existing outcome
                cursor.execute("""
                    UPDATE lead_outcomes 
                    SET actual_conversion = %s,
                        conversion_date = %s,
                        conversion_value = %s,
                        conversion_type = %s,
                        notes = %s
                    WHERE session_id = %s
                """, (
                    conversion_update.actual_conversion,
                    conversion_update.conversion_date,
                    conversion_update.conversion_value,
                    conversion_update.conversion_type,
                    conversion_update.notes,
                    session_id
                ))
            else:
                # Create new outcome record
                # Get form_id for the record
                cursor.execute("SELECT form_id FROM lead_sessions WHERE session_id = %s", (session_id,))
                form_id = cursor.fetchone()[0]
                
                cursor.execute("""
                    INSERT INTO lead_outcomes 
                    (id, session_id, form_id, actual_conversion, conversion_date, 
                     conversion_value, conversion_type, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    str(uuid.uuid4()),
                    session_id,
                    form_id,
                    conversion_update.actual_conversion,
                    conversion_update.conversion_date,
                    conversion_update.conversion_value,
                    conversion_update.conversion_type,
                    conversion_update.notes
                ))
            
            conn.commit()
            
            return success_response(
                data={
                    "session_id": session_id,
                    "actual_conversion": conversion_update.actual_conversion,
                    "conversion_date": conversion_update.conversion_date,
                    "conversion_value": conversion_update.conversion_value,
                    "conversion_type": conversion_update.conversion_type
                },
                message=f"Lead conversion status updated to {'converted' if conversion_update.actual_conversion else 'not converted'}"
            )
            
    except Exception as e:
        logger.error(f"Failed to update lead conversion: {e}")
        return error_response("Failed to update lead conversion", 500)

@router.get("/leads/stats/summary")
async def get_leads_summary(
    form_id: Optional[str] = None,
    days: int = 30,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get summary statistics for leads."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Build WHERE clause
            where_conditions = ["ls.client_id = %s", "ls.started_at >= NOW() - INTERVAL '%s days'"]
            query_params = [current_user.client_id, days]
            
            if form_id:
                where_conditions.append("ls.form_id = %s")
                query_params.append(form_id)
            
            where_clause = " AND ".join(where_conditions)
            
            # Get lead status counts
            cursor.execute(f"""
                SELECT 
                    ls.lead_status,
                    COUNT(*) as count,
                    AVG(ls.final_score) as avg_score
                FROM lead_sessions ls
                WHERE {where_clause}
                GROUP BY ls.lead_status
            """, query_params)
            
            status_stats = {row[0]: {"count": row[1], "avg_score": float(row[2]) if row[2] else 0} for row in cursor.fetchall()}
            
            # Get conversion stats
            cursor.execute(f"""
                SELECT 
                    COUNT(*) as total_leads,
                    COUNT(lo.actual_conversion) as tracked_conversions,
                    SUM(CASE WHEN lo.actual_conversion = true THEN 1 ELSE 0 END) as conversions,
                    SUM(lo.conversion_value) as total_value,
                    AVG(lo.conversion_value) as avg_value
                FROM lead_sessions ls
                LEFT JOIN lead_outcomes lo ON ls.session_id = lo.session_id
                WHERE {where_clause}
            """, query_params)
            
            conv_result = cursor.fetchone()
            conversion_stats = {
                "total_leads": conv_result[0],
                "tracked_conversions": conv_result[1],
                "conversions": conv_result[2],
                "conversion_rate": (conv_result[2] / conv_result[1] * 100) if conv_result[1] > 0 else 0,
                "total_value": float(conv_result[4]) if conv_result[4] else 0,
                "avg_value": float(conv_result[5]) if conv_result[5] else 0
            }
            
            # Get UTM source stats
            cursor.execute(f"""
                SELECT 
                    td.utm_source,
                    COUNT(*) as leads,
                    SUM(CASE WHEN lo.actual_conversion = true THEN 1 ELSE 0 END) as conversions
                FROM lead_sessions ls
                LEFT JOIN tracking_data td ON ls.session_id = td.session_id
                LEFT JOIN lead_outcomes lo ON ls.session_id = lo.session_id
                WHERE {where_clause} AND td.utm_source IS NOT NULL
                GROUP BY td.utm_source
                ORDER BY leads DESC
                LIMIT 10
            """, query_params)
            
            utm_stats = [{"source": row[0], "leads": row[1], "conversions": row[2]} for row in cursor.fetchall()]
            
            return success_response(
                data={
                    "status_breakdown": status_stats,
                    "conversion_stats": conversion_stats,
                    "utm_sources": utm_stats,
                    "period_days": days
                },
                message=f"Lead summary for last {days} days"
            )
            
    except Exception as e:
        logger.error(f"Failed to get leads summary: {e}")
        return error_response("Failed to retrieve leads summary", 500)