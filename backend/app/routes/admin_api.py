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

from app.database import get_database_connection, db
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
        # Build query for lead_sessions with filters
        query = db.client.table('lead_sessions').select('*').eq('client_id', current_user.client_id)
        
        if form_id:
            query = query.eq('form_id', form_id)
        
        if status:
            query = query.eq('lead_status', status)
        
        # Get lead sessions with pagination
        lead_sessions = query.order('started_at', desc=True).range(offset, offset + limit - 1).execute()
        
        if not lead_sessions.data:
            return success_response(
                data={"leads": [], "pagination": {"limit": limit, "offset": offset, "total": 0}},
                message="No leads found"
            )
        
        session_ids = [session['session_id'] for session in lead_sessions.data]
        
        # Get form titles
        form_ids = [session['form_id'] for session in lead_sessions.data if session.get('form_id')]
        forms_data = {}
        if form_ids:
            forms_result = db.client.table('forms').select('id, title').in_('id', form_ids).execute()
            forms_data = {form['id']: form['title'] for form in forms_result.data}
        
        # Get contact info from responses
        responses_result = db.client.table('responses').select('session_id, question_text, answer').in_('session_id', session_ids).execute()
        
        contact_data = {}
        for response in responses_result.data:
            session_id = response['session_id']
            question_text = response['question_text'].lower() if response['question_text'] else ''
            answer = response['answer']
            
            if session_id not in contact_data:
                contact_data[session_id] = {}
            
            # Extract contact info based on question text patterns
            if 'name' in question_text and 'business' not in question_text:
                contact_data[session_id]['contact_name'] = answer
            elif 'email' in question_text:
                contact_data[session_id]['contact_email'] = answer
            elif 'phone' in question_text:
                contact_data[session_id]['contact_phone'] = answer
        
        # Get conversion data
        conversion_result = db.client.table('lead_outcomes').select('*').in_('session_id', session_ids).execute()
        conversion_data = {outcome['session_id']: outcome for outcome in conversion_result.data}
        
        # Get UTM tracking data
        utm_result = db.client.table('tracking_data').select('session_id, utm_source, utm_campaign, utm_medium').in_('session_id', session_ids).execute()
        utm_data = {utm['session_id']: utm for utm in utm_result.data}
        
        # Filter by conversion status if requested
        filtered_sessions = []
        for session in lead_sessions.data:
            session_id = session['session_id']
            outcome = conversion_data.get(session_id, {})
            
            if converted is not None:
                actual_conversion = outcome.get('actual_conversion')
                if converted and not actual_conversion:
                    continue
                elif not converted and actual_conversion:
                    continue
            
            filtered_sessions.append(session)
        
        # Combine all data
        leads = []
        for session in filtered_sessions:
            session_id = session['session_id']
            contact = contact_data.get(session_id, {})
            outcome = conversion_data.get(session_id, {})
            utm = utm_data.get(session_id, {})
            
            leads.append({
                "session_id": session_id,
                "form_id": str(session['form_id']) if session.get('form_id') else '',
                "form_title": forms_data.get(session.get('form_id'), 'Unknown Form'),
                "lead_status": session.get('lead_status') or 'unknown',
                "completion_type": session.get('completion_type'),
                "final_score": session.get('final_score') or 0,
                "started_at": session.get('started_at'),
                "completed_at": session.get('completed_at'),
                "last_updated": session.get('last_updated'),
                "contact_name": contact.get('contact_name'),
                "contact_email": contact.get('contact_email'),
                "contact_phone": contact.get('contact_phone'),
                "actual_conversion": outcome.get('actual_conversion'),
                "conversion_date": outcome.get('conversion_date'),
                "conversion_value": float(outcome['conversion_value']) if outcome.get('conversion_value') else None,
                "conversion_type": outcome.get('conversion_type'),
                "utm_source": utm.get('utm_source'),
                "utm_campaign": utm.get('utm_campaign'),
                "utm_medium": utm.get('utm_medium')
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
        # Get lead session
        lead_result = db.client.table('lead_sessions').select('*').eq('session_id', session_id).eq('client_id', current_user.client_id).execute()
        
        if not lead_result.data:
            return error_response("Lead not found", 404)
        
        session = lead_result.data[0]
        
        # Get form title
        form_title = "Unknown Form"
        if session.get('form_id'):
            form_result = db.client.table('forms').select('title').eq('id', session['form_id']).execute()
            if form_result.data:
                form_title = form_result.data[0]['title']
        
        # Get contact info from responses
        contact_data = {}
        responses_result = db.client.table('responses').select('question_text, answer').eq('session_id', session_id).execute()
        
        for response in responses_result.data:
            question_text = response['question_text'].lower() if response['question_text'] else ''
            answer = response['answer']
            
            # Extract contact info based on question text patterns
            if 'name' in question_text and 'business' not in question_text:
                contact_data['contact_name'] = answer
            elif 'email' in question_text:
                contact_data['contact_email'] = answer
            elif 'phone' in question_text:
                contact_data['contact_phone'] = answer
        
        # Get conversion data
        conversion_result = db.client.table('lead_outcomes').select('*').eq('session_id', session_id).execute()
        outcome = conversion_result.data[0] if conversion_result.data else {}
        
        # Get UTM tracking data
        utm_result = db.client.table('tracking_data').select('utm_source, utm_campaign, utm_medium').eq('session_id', session_id).execute()
        utm = utm_result.data[0] if utm_result.data else {}
        
        lead_data = {
            "session_id": session['session_id'],
            "form_id": str(session['form_id']) if session.get('form_id') else '',
            "form_title": form_title,
            "lead_status": session.get('lead_status') or 'unknown',
            "completion_type": session.get('completion_type'),
            "final_score": session.get('final_score') or 0,
            "started_at": session.get('started_at'),
            "completed_at": session.get('completed_at'),
            "last_updated": session.get('last_updated'),
            "contact_name": contact_data.get('contact_name'),
            "contact_email": contact_data.get('contact_email'),
            "contact_phone": contact_data.get('contact_phone'),
            "actual_conversion": outcome.get('actual_conversion'),
            "conversion_date": outcome.get('conversion_date'),
            "conversion_value": float(outcome['conversion_value']) if outcome.get('conversion_value') else None,
            "conversion_type": outcome.get('conversion_type'),
            "utm_source": utm.get('utm_source'),
            "utm_campaign": utm.get('utm_campaign'),
            "utm_medium": utm.get('utm_medium')
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
        # Verify the lead belongs to this client
        session_result = db.client.table('lead_sessions').select('id, form_id').eq('session_id', session_id).eq('client_id', current_user.client_id).execute()
        
        if not session_result.data:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        form_id = session_result.data[0]['form_id']
        
        # Check if lead_outcome record exists
        outcome_result = db.client.table('lead_outcomes').select('id').eq('session_id', session_id).execute()
        
        outcome_data = {
            "actual_conversion": conversion_update.actual_conversion,
            "conversion_date": conversion_update.conversion_date.isoformat() if conversion_update.conversion_date else None,
            "conversion_value": conversion_update.conversion_value,
            "conversion_type": conversion_update.conversion_type,
            "notes": conversion_update.notes
        }
        
        if outcome_result.data:
            # Update existing outcome
            update_result = db.client.table('lead_outcomes').update(outcome_data).eq('session_id', session_id).execute()
        else:
            # Create new outcome record
            outcome_data.update({
                "id": str(uuid.uuid4()),
                "session_id": session_id,
                "form_id": form_id
            })
            insert_result = db.client.table('lead_outcomes').insert(outcome_data).execute()
        
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
        
    except HTTPException:
        raise
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
        from datetime import datetime, timedelta
        
        # Calculate cutoff date
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        cutoff_date_str = cutoff_date.isoformat()
        
        # Build base query for lead sessions
        query = db.client.table('lead_sessions').select('*').eq('client_id', current_user.client_id).gte('started_at', cutoff_date_str)
        
        if form_id:
            query = query.eq('form_id', form_id)
        
        # Get lead sessions for the period
        sessions_result = query.execute()
        sessions = sessions_result.data
        
        if not sessions:
            return success_response(
                data={
                    "status_breakdown": {},
                    "conversion_stats": {
                        "total_leads": 0,
                        "tracked_conversions": 0,
                        "conversions": 0,
                        "conversion_rate": 0,
                        "total_value": 0,
                        "avg_value": 0
                    },
                    "utm_sources": [],
                    "period_days": days
                },
                message=f"No leads found for last {days} days"
            )
        
        session_ids = [session['session_id'] for session in sessions]
        
        # Calculate status breakdown
        status_stats = {}
        for session in sessions:
            status = session.get('lead_status', 'unknown')
            score = session.get('final_score', 0) or 0
            
            if status not in status_stats:
                status_stats[status] = {'count': 0, 'total_score': 0}
            
            status_stats[status]['count'] += 1
            status_stats[status]['total_score'] += score
        
        # Calculate average scores
        for status, stats in status_stats.items():
            stats['avg_score'] = stats['total_score'] / stats['count'] if stats['count'] > 0 else 0
            del stats['total_score']  # Remove helper field
        
        # Get conversion data
        conversion_result = db.client.table('lead_outcomes').select('*').in_('session_id', session_ids).execute()
        outcomes = conversion_result.data
        
        total_leads = len(sessions)
        tracked_conversions = len(outcomes)
        conversions = sum(1 for outcome in outcomes if outcome.get('actual_conversion'))
        total_value = sum(float(outcome.get('conversion_value', 0) or 0) for outcome in outcomes)
        avg_value = total_value / tracked_conversions if tracked_conversions > 0 else 0
        conversion_rate = (conversions / tracked_conversions * 100) if tracked_conversions > 0 else 0
        
        conversion_stats = {
            "total_leads": total_leads,
            "tracked_conversions": tracked_conversions,
            "conversions": conversions,
            "conversion_rate": conversion_rate,
            "total_value": total_value,
            "avg_value": avg_value
        }
        
        # Get UTM source stats
        utm_result = db.client.table('tracking_data').select('session_id, utm_source').in_('session_id', session_ids).neq('utm_source', 'null').not_.is_('utm_source', 'null').execute()
        utm_data = utm_result.data
        
        # Build UTM stats with conversion data
        utm_stats_dict = {}
        outcome_by_session = {outcome['session_id']: outcome for outcome in outcomes}
        
        for utm in utm_data:
            source = utm.get('utm_source')
            if source and source.strip():
                session_id = utm['session_id']
                if source not in utm_stats_dict:
                    utm_stats_dict[source] = {'leads': 0, 'conversions': 0}
                
                utm_stats_dict[source]['leads'] += 1
                
                # Check if this session converted
                outcome = outcome_by_session.get(session_id)
                if outcome and outcome.get('actual_conversion'):
                    utm_stats_dict[source]['conversions'] += 1
        
        # Convert to list and sort by leads descending
        utm_stats = [
            {"source": source, "leads": stats['leads'], "conversions": stats['conversions']}
            for source, stats in utm_stats_dict.items()
        ]
        utm_stats.sort(key=lambda x: x['leads'], reverse=True)
        utm_stats = utm_stats[:10]  # Limit to top 10
        
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