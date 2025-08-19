"""
Admin Themes API - Theme Management for Admin Interface

This module provides API endpoints for:
1. Creating, reading, updating, and deleting client themes
2. Managing system themes and client-specific themes  
3. Theme configuration and customization
4. Setting default themes for clients
5. Theme preview and validation
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
from pydantic import BaseModel, Field, validator
from typing import Dict, Any, List, Optional, Literal
import logging
from datetime import datetime
import uuid
import json

from app.database import get_database_connection
from app.routes.admin_api import get_current_admin_user, AdminUserResponse
from app.utils.response_helpers import create_success_response, create_error_response

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin/themes", tags=["admin-themes"])

# === PYDANTIC MODELS FOR THEMES ===

class ThemeConfig(BaseModel):
    """Theme configuration schema."""
    colors: Dict[str, Any] = Field(default_factory=dict)
    typography: Dict[str, Any] = Field(default_factory=dict)
    spacing: Dict[str, Any] = Field(default_factory=dict)
    borderRadius: Optional[str] = None
    borderRadiusLg: Optional[str] = None
    shadow: Optional[str] = None
    shadowLg: Optional[str] = None
    
    @validator('colors')
    def validate_colors(cls, v):
        required_color_keys = ['primary', 'secondary', 'background', 'text']
        if not all(key in v for key in required_color_keys):
            raise ValueError(f'Colors must include: {", ".join(required_color_keys)}')
        return v

class ThemeCreateRequest(BaseModel):
    """Request to create a new theme."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    theme_config: ThemeConfig
    is_default: bool = Field(default=False)

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Theme name cannot be empty')
        return v.strip()

class ThemeUpdateRequest(BaseModel):
    """Request to update an existing theme."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    theme_config: Optional[ThemeConfig] = None
    is_default: Optional[bool] = None

class ThemeResponse(BaseModel):
    """Response model for theme data."""
    id: str
    client_id: Optional[str]
    name: str
    description: Optional[str]
    theme_config: Dict[str, Any]
    is_default: bool
    is_system_theme: bool
    created_at: datetime
    updated_at: datetime

class ThemeListResponse(BaseModel):
    """Response model for theme list with pagination."""
    themes: List[ThemeResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int

class ThemePreviewRequest(BaseModel):
    """Request to preview a theme configuration."""
    theme_config: ThemeConfig
    preview_type: Literal["form", "dashboard", "settings"] = Field(default="form")

class ThemePreviewResponse(BaseModel):
    """Response with preview data for a theme."""
    preview_html: str
    preview_css: str
    theme_config: Dict[str, Any]

# === UTILITY FUNCTIONS ===

def generate_theme_css(theme_config: Dict[str, Any]) -> str:
    """Generate CSS from theme configuration."""
    colors = theme_config.get('colors', {})
    typography = theme_config.get('typography', {})
    spacing = theme_config.get('spacing', {})
    
    css_rules = [
        ":root {",
        f"  --color-primary: {colors.get('primary', '#3B82F6')};",
        f"  --color-secondary: {colors.get('secondary', '#64748B')};",
        f"  --color-accent: {colors.get('accent', '#10B981')};",
        f"  --color-background: {colors.get('background', '#FFFFFF')};",
        f"  --color-surface: {colors.get('surface', '#F8FAFC')};",
        f"  --color-text-primary: {colors.get('text', {}).get('primary', '#1E293B')};",
        f"  --color-text-secondary: {colors.get('text', {}).get('secondary', '#64748B')};",
        f"  --color-border: {colors.get('border', '#E2E8F0')};",
        f"  --font-family: {typography.get('fontFamily', 'Inter, system-ui, sans-serif')};",
        f"  --font-size-base: {typography.get('fontSize', {}).get('base', '16px')};",
        f"  --font-size-heading: {typography.get('fontSize', {}).get('heading', '24px')};",
        f"  --spacing-section: {spacing.get('section', '2rem')};",
        f"  --spacing-element: {spacing.get('element', '1rem')};",
        f"  --border-radius: {theme_config.get('borderRadius', '0.5rem')};",
        f"  --shadow: {theme_config.get('shadow', '0 1px 3px 0 rgb(0 0 0 / 0.1)')};",
        "}"
    ]
    
    return "\n".join(css_rules)

def validate_theme_ownership(theme_id: str, client_id: str) -> bool:
    """Validate that a theme belongs to the client or is a system theme."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT client_id, is_system_theme 
                FROM client_themes 
                WHERE id = %s
            """, (theme_id,))
            
            result = cursor.fetchone()
            if not result:
                return False
            
            theme_client_id, is_system = result
            return is_system or str(theme_client_id) == client_id
            
    except Exception as e:
        logger.error(f"Failed to validate theme ownership: {e}")
        return False

# === THEME CRUD ENDPOINTS ===

@router.get("", response_model=ThemeListResponse)
async def list_themes(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    include_system: bool = Query(True, description="Include system themes"),
    search: Optional[str] = Query(None, description="Search in theme name and description"),
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get paginated list of themes for the client."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Build WHERE clause
            where_conditions = []
            params = []
            
            if include_system:
                where_conditions.append("(client_id = %s OR is_system_theme = true)")
                params.append(current_user.client_id)
            else:
                where_conditions.append("client_id = %s")
                params.append(current_user.client_id)
            
            if search:
                where_conditions.append("(name ILIKE %s OR description ILIKE %s)")
                search_term = f"%{search}%"
                params.extend([search_term, search_term])
            
            where_clause = " AND ".join(where_conditions)
            
            # Get total count
            count_query = f"SELECT COUNT(*) FROM client_themes WHERE {where_clause}"
            cursor.execute(count_query, params)
            total_count = cursor.fetchone()[0]
            
            # Get themes
            offset = (page - 1) * page_size
            themes_query = f"""
                SELECT id, client_id, name, description, theme_config, is_default,
                       is_system_theme, created_at, updated_at
                FROM client_themes 
                WHERE {where_clause}
                ORDER BY is_system_theme DESC, is_default DESC, name ASC
                LIMIT %s OFFSET %s
            """
            params.extend([page_size, offset])
            cursor.execute(themes_query, params)
            
            themes = []
            for row in cursor.fetchall():
                themes.append(ThemeResponse(
                    id=str(row[0]),
                    client_id=str(row[1]) if row[1] else None,
                    name=row[2],
                    description=row[3],
                    theme_config=row[4] or {},
                    is_default=row[5] or False,
                    is_system_theme=row[6] or False,
                    created_at=row[7],
                    updated_at=row[8]
                ))
            
            total_pages = (total_count + page_size - 1) // page_size
            
            return ThemeListResponse(
                themes=themes,
                total_count=total_count,
                page=page,
                page_size=page_size,
                total_pages=total_pages
            )
            
    except Exception as e:
        logger.error(f"Failed to list themes: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve themes")

@router.get("/{theme_id}", response_model=ThemeResponse)
async def get_theme(
    theme_id: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get a specific theme by ID."""
    try:
        if not validate_theme_ownership(theme_id, current_user.client_id):
            raise HTTPException(status_code=404, detail="Theme not found")
        
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, client_id, name, description, theme_config, is_default,
                       is_system_theme, created_at, updated_at
                FROM client_themes 
                WHERE id = %s
            """, (theme_id,))
            
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Theme not found")
            
            return ThemeResponse(
                id=str(row[0]),
                client_id=str(row[1]) if row[1] else None,
                name=row[2],
                description=row[3],
                theme_config=row[4] or {},
                is_default=row[5] or False,
                is_system_theme=row[6] or False,
                created_at=row[7],
                updated_at=row[8]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get theme: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve theme")

@router.post("", response_model=ThemeResponse)
async def create_theme(
    theme_request: ThemeCreateRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Create a new theme."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Check if theme name already exists for this client
            cursor.execute("""
                SELECT id FROM client_themes 
                WHERE client_id = %s AND name = %s
            """, (current_user.client_id, theme_request.name))
            
            if cursor.fetchone():
                raise HTTPException(status_code=409, detail="Theme with this name already exists")
            
            # If setting as default, unset other defaults
            if theme_request.is_default:
                cursor.execute("""
                    UPDATE client_themes 
                    SET is_default = false 
                    WHERE client_id = %s AND is_default = true
                """, (current_user.client_id,))
            
            # Create theme
            theme_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO client_themes 
                (id, client_id, name, description, theme_config, is_default, is_system_theme)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING created_at, updated_at
            """, (
                theme_id, current_user.client_id, theme_request.name,
                theme_request.description, json.dumps(theme_request.theme_config.dict()),
                theme_request.is_default, False
            ))
            
            created_at, updated_at = cursor.fetchone()
            conn.commit()
            
            return ThemeResponse(
                id=theme_id,
                client_id=current_user.client_id,
                name=theme_request.name,
                description=theme_request.description,
                theme_config=theme_request.theme_config.dict(),
                is_default=theme_request.is_default,
                is_system_theme=False,
                created_at=created_at,
                updated_at=updated_at
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create theme: {e}")
        raise HTTPException(status_code=500, detail="Failed to create theme")

@router.put("/{theme_id}", response_model=ThemeResponse)
async def update_theme(
    theme_id: str,
    theme_request: ThemeUpdateRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Update an existing theme."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Check if theme exists and belongs to client (not system theme)
            cursor.execute("""
                SELECT client_id, is_system_theme FROM client_themes 
                WHERE id = %s
            """, (theme_id,))
            
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Theme not found")
            
            theme_client_id, is_system = result
            if is_system or str(theme_client_id) != current_user.client_id:
                raise HTTPException(status_code=403, detail="Cannot modify this theme")
            
            # Check for name conflicts if name is being updated
            if theme_request.name:
                cursor.execute("""
                    SELECT id FROM client_themes 
                    WHERE client_id = %s AND name = %s AND id != %s
                """, (current_user.client_id, theme_request.name, theme_id))
                
                if cursor.fetchone():
                    raise HTTPException(status_code=409, detail="Theme with this name already exists")
            
            # If setting as default, unset other defaults
            if theme_request.is_default:
                cursor.execute("""
                    UPDATE client_themes 
                    SET is_default = false 
                    WHERE client_id = %s AND is_default = true AND id != %s
                """, (current_user.client_id, theme_id))
            
            # Build dynamic update query
            update_fields = []
            update_values = []
            
            for field_name, field_value in theme_request.dict(exclude_unset=True).items():
                if field_value is not None:
                    if field_name == 'theme_config':
                        update_fields.append("theme_config = %s")
                        update_values.append(json.dumps(field_value.dict()))
                    else:
                        update_fields.append(f"{field_name} = %s")
                        update_values.append(field_value)
            
            if update_fields:
                update_fields.append("updated_at = NOW()")
                update_values.append(theme_id)
                
                query = f"""
                    UPDATE client_themes 
                    SET {', '.join(update_fields)}
                    WHERE id = %s
                """
                cursor.execute(query, update_values)
                conn.commit()
            
            # Return updated theme
            return await get_theme(theme_id, current_user)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update theme: {e}")
        raise HTTPException(status_code=500, detail="Failed to update theme")

@router.delete("/{theme_id}")
async def delete_theme(
    theme_id: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Delete a theme."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Check if theme exists and belongs to client (not system theme)
            cursor.execute("""
                SELECT client_id, is_system_theme, is_default FROM client_themes 
                WHERE id = %s
            """, (theme_id,))
            
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Theme not found")
            
            theme_client_id, is_system, is_default = result
            if is_system or str(theme_client_id) != current_user.client_id:
                raise HTTPException(status_code=403, detail="Cannot delete this theme")
            
            if is_default:
                raise HTTPException(status_code=400, detail="Cannot delete the default theme")
            
            # Check if theme is being used by any forms
            cursor.execute("""
                SELECT COUNT(*) FROM forms 
                WHERE client_id = %s 
                AND theme_config->>'theme_id' = %s
            """, (current_user.client_id, theme_id))
            
            forms_using_theme = cursor.fetchone()[0]
            if forms_using_theme > 0:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Cannot delete theme: {forms_using_theme} forms are using this theme"
                )
            
            # Delete theme
            cursor.execute("DELETE FROM client_themes WHERE id = %s", (theme_id,))
            conn.commit()
            
            return create_success_response(
                message="Theme deleted successfully",
                data={"theme_id": theme_id}
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete theme: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete theme")

@router.post("/{theme_id}/set-default")
async def set_default_theme(
    theme_id: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Set a theme as the default for the client."""
    try:
        if not validate_theme_ownership(theme_id, current_user.client_id):
            raise HTTPException(status_code=404, detail="Theme not found")
        
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Unset current default
            cursor.execute("""
                UPDATE client_themes 
                SET is_default = false 
                WHERE client_id = %s AND is_default = true
            """, (current_user.client_id,))
            
            # Set new default
            cursor.execute("""
                UPDATE client_themes 
                SET is_default = true 
                WHERE id = %s
            """, (theme_id,))
            
            conn.commit()
            
            return create_success_response(
                message="Default theme updated successfully",
                data={"theme_id": theme_id}
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to set default theme: {e}")
        raise HTTPException(status_code=500, detail="Failed to set default theme")

# === THEME PREVIEW AND UTILITIES ===

@router.post("/preview", response_model=ThemePreviewResponse)
async def preview_theme(
    preview_request: ThemePreviewRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Generate a preview of a theme configuration."""
    try:
        theme_config = preview_request.theme_config.dict()
        preview_css = generate_theme_css(theme_config)
        
        # Generate preview HTML based on type
        if preview_request.preview_type == "form":
            preview_html = """
            <div class="form-preview">
                <div class="form-header">
                    <h1>Sample Form</h1>
                    <p>This is how your form will look with this theme</p>
                </div>
                <div class="form-content">
                    <div class="form-field">
                        <label>Your Name</label>
                        <input type="text" placeholder="Enter your name" />
                    </div>
                    <div class="form-field">
                        <label>Email Address</label>
                        <input type="email" placeholder="Enter your email" />
                    </div>
                    <button class="form-button">Continue</button>
                </div>
            </div>
            """
        else:
            preview_html = """
            <div class="preview-placeholder">
                <h2>Theme Preview</h2>
                <p>Preview for {type} coming soon</p>
            </div>
            """.format(type=preview_request.preview_type)
        
        return ThemePreviewResponse(
            preview_html=preview_html,
            preview_css=preview_css,
            theme_config=theme_config
        )
        
    except Exception as e:
        logger.error(f"Failed to generate theme preview: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate theme preview")

@router.get("/system-themes", response_model=List[ThemeResponse])
async def get_system_themes():
    """Get all available system themes."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, client_id, name, description, theme_config, is_default,
                       is_system_theme, created_at, updated_at
                FROM client_themes 
                WHERE is_system_theme = true
                ORDER BY name ASC
            """)
            
            themes = []
            for row in cursor.fetchall():
                themes.append(ThemeResponse(
                    id=str(row[0]),
                    client_id=str(row[1]) if row[1] else None,
                    name=row[2],
                    description=row[3],
                    theme_config=row[4] or {},
                    is_default=row[5] or False,
                    is_system_theme=row[6] or False,
                    created_at=row[7],
                    updated_at=row[8]
                ))
            
            return themes
            
    except Exception as e:
        logger.error(f"Failed to get system themes: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve system themes")