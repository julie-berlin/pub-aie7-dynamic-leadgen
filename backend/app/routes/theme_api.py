"""
Theme Management API - Support for Frontend Theme System

This module provides API endpoints for:
1. Theme management for forms and clients
2. Form configuration with theme integration
3. Client branding and theme preferences
4. System theme management
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from typing import Dict, Any, List, Optional, Union
import logging
from datetime import datetime
import json
import uuid

from app.database import get_database_connection

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/themes", tags=["themes"])

# === PYDANTIC MODELS FOR THEME SYSTEM ===

class ThemeColors(BaseModel):
    """Color configuration for a theme."""
    primary: str = Field(..., description="Primary brand color")
    primaryHover: str = Field(..., description="Primary color on hover")
    primaryLight: str = Field(..., description="Light variant of primary")
    secondary: str = Field(..., description="Secondary color")
    secondaryHover: str = Field(..., description="Secondary color on hover")
    secondaryLight: str = Field(..., description="Light variant of secondary")
    accent: str = Field(..., description="Accent color for highlights")
    text: str = Field(..., description="Primary text color")
    textLight: str = Field(..., description="Light text color")
    textMuted: str = Field(..., description="Muted text color")
    background: str = Field(..., description="Main background color")
    backgroundLight: str = Field(..., description="Light background color")
    border: str = Field(..., description="Border color")
    error: str = Field(..., description="Error state color")
    success: str = Field(..., description="Success state color")
    warning: str = Field(..., description="Warning state color")

class ThemeTypography(BaseModel):
    """Typography configuration for a theme."""
    primary: str = Field(..., description="Primary font family")
    secondary: str = Field(..., description="Secondary font family")

class ThemeSpacing(BaseModel):
    """Spacing configuration for a theme."""
    section: str = Field("2rem", description="Section spacing")
    element: str = Field("1rem", description="Element spacing")
    page: str = Field("2rem", description="Page padding")
    input: str = Field("1rem", description="Input field padding")
    button: str = Field("0.75rem 1.5rem", description="Button padding")

class ThemeConfig(BaseModel):
    """Complete theme configuration."""
    name: str = Field(..., description="Theme name")
    colors: ThemeColors
    typography: ThemeTypography
    spacing: ThemeSpacing
    borderRadius: str = Field("0.5rem", description="Default border radius")
    borderRadiusLg: str = Field("0.75rem", description="Large border radius")
    shadow: str = Field("0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)", description="Default shadow")
    shadowLg: str = Field("0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)", description="Large shadow")

class ClientThemeRequest(BaseModel):
    """Request to create or update a client theme."""
    name: str = Field(..., description="Theme name")
    description: Optional[str] = Field(None, description="Theme description")
    theme_config: ThemeConfig
    is_default: bool = Field(False, description="Set as client default theme")

class ClientThemeResponse(BaseModel):
    """Response model for client themes."""
    id: str
    client_id: Optional[str]
    name: str
    description: Optional[str]
    theme_config: ThemeConfig
    is_default: bool
    is_system_theme: bool
    usage_count: int
    last_used_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class FormDisplaySettings(BaseModel):
    """Display settings for forms."""
    showProgress: bool = Field(True, description="Show progress bar")
    allowBack: bool = Field(True, description="Allow back navigation")
    saveProgress: bool = Field(True, description="Auto-save form progress")
    timeLimit: Optional[int] = Field(None, description="Time limit in minutes")
    redirectUrl: Optional[str] = Field(None, description="Redirect URL after completion")

class FormConfigRequest(BaseModel):
    """Request to update form configuration with theme."""
    theme_config: Optional[ThemeConfig] = Field(None, description="Custom theme for this form")
    theme_id: Optional[str] = Field(None, description="ID of existing theme to use")
    display_settings: Optional[FormDisplaySettings] = Field(None, description="Display settings")
    frontend_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional frontend metadata")

class FormConfigResponse(BaseModel):
    """Response model for form configuration."""
    id: str
    client_id: str
    title: str
    description: Optional[str]
    theme_config: Optional[ThemeConfig]
    display_settings: FormDisplaySettings
    frontend_metadata: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime

class ThemeListResponse(BaseModel):
    """Response for theme list queries."""
    themes: List[ClientThemeResponse]
    total_count: int
    system_themes_count: int

# === THEME MANAGEMENT ENDPOINTS ===

@router.get("/client/{client_id}", response_model=ThemeListResponse)
async def get_client_themes(client_id: str, include_system: bool = True):
    """Get all themes available to a client."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Build query based on whether to include system themes
            if include_system:
                cursor.execute("""
                    SELECT id, client_id, name, description, theme_config, is_default,
                           is_system_theme, usage_count, last_used_at, created_at, updated_at
                    FROM client_themes
                    WHERE client_id = %s OR is_system_theme = true
                    ORDER BY is_default DESC, is_system_theme ASC, name ASC
                """, (client_id,))
            else:
                cursor.execute("""
                    SELECT id, client_id, name, description, theme_config, is_default,
                           is_system_theme, usage_count, last_used_at, created_at, updated_at
                    FROM client_themes
                    WHERE client_id = %s
                    ORDER BY is_default DESC, name ASC
                """, (client_id,))
            
            themes_data = cursor.fetchall()
            
            # Count system themes
            cursor.execute("SELECT COUNT(*) FROM client_themes WHERE is_system_theme = true")
            system_count = cursor.fetchone()[0]
            
            themes = []
            for row in themes_data:
                themes.append(ClientThemeResponse(
                    id=str(row[0]),
                    client_id=str(row[1]) if row[1] else None,
                    name=row[2],
                    description=row[3],
                    theme_config=ThemeConfig(**row[4]),
                    is_default=row[5],
                    is_system_theme=row[6],
                    usage_count=row[7],
                    last_used_at=row[8],
                    created_at=row[9],
                    updated_at=row[10]
                ))
            
            return ThemeListResponse(
                themes=themes,
                total_count=len(themes),
                system_themes_count=system_count
            )
            
    except Exception as e:
        logger.error(f"Failed to get client themes: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve themes")

@router.post("/client/{client_id}", response_model=ClientThemeResponse)
async def create_client_theme(client_id: str, theme_request: ClientThemeRequest):
    """Create a new theme for a client."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # If setting as default, unset other default themes
            if theme_request.is_default:
                cursor.execute("""
                    UPDATE client_themes 
                    SET is_default = false 
                    WHERE client_id = %s AND is_default = true
                """, (client_id,))
            
            # Create new theme
            theme_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO client_themes 
                (id, client_id, name, description, theme_config, is_default)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, created_at, updated_at
            """, (
                theme_id,
                client_id,
                theme_request.name,
                theme_request.description,
                json.dumps(theme_request.theme_config.dict()),
                theme_request.is_default
            ))
            
            result = cursor.fetchone()
            conn.commit()
            
            return ClientThemeResponse(
                id=theme_id,
                client_id=client_id,
                name=theme_request.name,
                description=theme_request.description,
                theme_config=theme_request.theme_config,
                is_default=theme_request.is_default,
                is_system_theme=False,
                usage_count=0,
                last_used_at=None,
                created_at=result[1],
                updated_at=result[2]
            )
            
    except Exception as e:
        logger.error(f"Failed to create client theme: {e}")
        if "unique constraint" in str(e).lower():
            raise HTTPException(status_code=409, detail="Theme name already exists for this client")
        raise HTTPException(status_code=500, detail="Failed to create theme")

@router.get("/theme/{theme_id}", response_model=ClientThemeResponse)
async def get_theme_by_id(theme_id: str):
    """Get a specific theme by ID."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, client_id, name, description, theme_config, is_default,
                       is_system_theme, usage_count, last_used_at, created_at, updated_at
                FROM client_themes
                WHERE id = %s
            """, (theme_id,))
            
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Theme not found")
            
            return ClientThemeResponse(
                id=str(row[0]),
                client_id=str(row[1]) if row[1] else None,
                name=row[2],
                description=row[3],
                theme_config=ThemeConfig(**row[4]),
                is_default=row[5],
                is_system_theme=row[6],
                usage_count=row[7],
                last_used_at=row[8],
                created_at=row[9],
                updated_at=row[10]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get theme: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve theme")

@router.put("/theme/{theme_id}", response_model=ClientThemeResponse)
async def update_theme(theme_id: str, theme_request: ClientThemeRequest):
    """Update an existing theme."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Check if theme exists and get client_id
            cursor.execute("SELECT client_id, is_system_theme FROM client_themes WHERE id = %s", (theme_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Theme not found")
            
            client_id, is_system_theme = result
            if is_system_theme:
                raise HTTPException(status_code=403, detail="Cannot modify system themes")
            
            # If setting as default, unset other default themes
            if theme_request.is_default:
                cursor.execute("""
                    UPDATE client_themes 
                    SET is_default = false 
                    WHERE client_id = %s AND is_default = true AND id != %s
                """, (client_id, theme_id))
            
            # Update theme
            cursor.execute("""
                UPDATE client_themes
                SET name = %s, description = %s, theme_config = %s, is_default = %s, updated_at = NOW()
                WHERE id = %s
                RETURNING updated_at
            """, (
                theme_request.name,
                theme_request.description,
                json.dumps(theme_request.theme_config.dict()),
                theme_request.is_default,
                theme_id
            ))
            
            updated_at = cursor.fetchone()[0]
            conn.commit()
            
            return ClientThemeResponse(
                id=theme_id,
                client_id=str(client_id),
                name=theme_request.name,
                description=theme_request.description,
                theme_config=theme_request.theme_config,
                is_default=theme_request.is_default,
                is_system_theme=False,
                usage_count=0,
                last_used_at=None,
                created_at=datetime.now(),  # We'd need to fetch this for accuracy
                updated_at=updated_at
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update theme: {e}")
        raise HTTPException(status_code=500, detail="Failed to update theme")

@router.delete("/theme/{theme_id}")
async def delete_theme(theme_id: str):
    """Delete a theme."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Check if theme exists and is not a system theme
            cursor.execute("SELECT is_system_theme FROM client_themes WHERE id = %s", (theme_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Theme not found")
            
            if result[0]:  # is_system_theme
                raise HTTPException(status_code=403, detail="Cannot delete system themes")
            
            # Check if theme is being used by any forms
            cursor.execute("SELECT COUNT(*) FROM forms WHERE theme_config->>'theme_id' = %s", (theme_id,))
            forms_using_theme = cursor.fetchone()[0]
            
            if forms_using_theme > 0:
                raise HTTPException(
                    status_code=409, 
                    detail=f"Cannot delete theme: {forms_using_theme} forms are using this theme"
                )
            
            # Delete theme
            cursor.execute("DELETE FROM client_themes WHERE id = %s", (theme_id,))
            conn.commit()
            
            return {"status": "success", "message": "Theme deleted successfully"}
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete theme: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete theme")

# === FORM CONFIGURATION ENDPOINTS ===

@router.get("/form/{form_id}/config", response_model=FormConfigResponse)
async def get_form_config(form_id: str):
    """Get form configuration including theme."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, client_id, title, description, theme_config, 
                       display_settings, frontend_metadata, is_active, created_at, updated_at
                FROM forms
                WHERE id = %s
            """, (form_id,))
            
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Form not found")
            
            # Parse theme_config if exists
            theme_config = None
            if row[4]:
                theme_config = ThemeConfig(**row[4])
            
            # Parse display_settings with defaults
            display_settings = FormDisplaySettings(**(row[5] or {}))
            
            return FormConfigResponse(
                id=str(row[0]),
                client_id=str(row[1]),
                title=row[2],
                description=row[3],
                theme_config=theme_config,
                display_settings=display_settings,
                frontend_metadata=row[6] or {},
                is_active=row[7],
                created_at=row[8],
                updated_at=row[9]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get form config: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve form configuration")

@router.put("/form/{form_id}/config", response_model=FormConfigResponse)
async def update_form_config(form_id: str, config_request: FormConfigRequest):
    """Update form configuration with theme and display settings."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Check if form exists
            cursor.execute("SELECT client_id FROM forms WHERE id = %s", (form_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Form not found")
            
            client_id = result[0]
            
            # Handle theme configuration
            theme_config_json = None
            if config_request.theme_config:
                theme_config_json = json.dumps(config_request.theme_config.dict())
            elif config_request.theme_id:
                # Load theme from theme_id
                cursor.execute("SELECT theme_config FROM client_themes WHERE id = %s", (config_request.theme_id,))
                theme_result = cursor.fetchone()
                if theme_result:
                    theme_config_json = json.dumps(theme_result[0])
                    # Update theme usage
                    cursor.execute("""
                        UPDATE client_themes 
                        SET usage_count = usage_count + 1, last_used_at = NOW()
                        WHERE id = %s
                    """, (config_request.theme_id,))
            
            # Prepare update fields
            update_fields = []
            update_values = []
            
            if theme_config_json:
                update_fields.append("theme_config = %s")
                update_values.append(theme_config_json)
            
            if config_request.display_settings:
                update_fields.append("display_settings = %s")
                update_values.append(json.dumps(config_request.display_settings.dict()))
            
            if config_request.frontend_metadata:
                update_fields.append("frontend_metadata = %s")
                update_values.append(json.dumps(config_request.frontend_metadata))
            
            if update_fields:
                update_fields.append("updated_at = NOW()")
                update_values.append(form_id)
                
                query = f"UPDATE forms SET {', '.join(update_fields)} WHERE id = %s RETURNING updated_at"
                cursor.execute(query, update_values)
                updated_at = cursor.fetchone()[0]
                conn.commit()
            
            # Fetch updated form config
            return await get_form_config(form_id)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update form config: {e}")
        raise HTTPException(status_code=500, detail="Failed to update form configuration")

@router.get("/form/{form_id}/theme")
async def get_form_theme(form_id: str):
    """Get the effective theme for a form (form-specific or client default)."""
    try:
        from ..database import db
        from ..utils.response_helpers import success_response
        
        # Get form data including theme_config
        form_data = db.get_form(form_id)
        if not form_data:
            raise HTTPException(status_code=404, detail="Form not found")
        
        # Check if form has a specific theme_config
        theme_config = form_data.get('theme_config')
        
        if theme_config:
            logger.info(f"Found theme_config for form {form_id}: {type(theme_config)}")
            # Form has a specific theme configuration
            return success_response(
                data=theme_config,
                message="Form-specific theme loaded successfully"
            )
        
        # If no form-specific theme, try to get client's default theme
        client_id = form_data.get('client_id')
        if client_id:
            logger.info(f"Looking for default theme for client {client_id}")
            try:
                # Get client's default theme from client_themes table using Supabase client
                client_theme_data = db.client.table('client_themes').select('theme_config').eq('client_id', client_id).eq('is_default', True).limit(1).execute()
                
                if client_theme_data.data and len(client_theme_data.data) > 0:
                    theme_config = client_theme_data.data[0].get('theme_config')
                    if theme_config:
                        logger.info(f"Found client default theme for {client_id}")
                        return success_response(
                            data=theme_config,
                            message="Client default theme loaded successfully"
                        )
            except Exception as e:
                logger.warning(f"Error loading client theme: {e}")
        
        # Fallback to default theme if no specific theme is found
        logger.info(f"Using fallback default theme for form {form_id}")
        default_theme = {
            "name": "Default Theme",
            "colors": {
                "primary": "#3b82f6",
                "primaryHover": "#2563eb",
                "primaryLight": "#dbeafe",
                "secondary": "#6b7280",
                "secondaryHover": "#4b5563",
                "secondaryLight": "#f3f4f6",
                "accent": "#10b981",
                "text": "#111827",
                "textLight": "#6b7280",
                "textMuted": "#9ca3af",
                "background": "#ffffff",
                "backgroundLight": "#f9fafb",
                "border": "#e5e7eb",
                "error": "#ef4444",
                "success": "#10b981",
                "warning": "#f59e0b"
            },
            "typography": {
                "primary": "Inter, sans-serif",
                "secondary": "Inter, sans-serif"
            },
            "spacing": {
                "section": "2rem",
                "element": "1rem"
            },
            "borderRadius": "0.5rem",
            "borderRadiusLg": "0.75rem",
            "shadow": "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
            "shadowLg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
        }
        
        return success_response(
            data=default_theme,
            message="Default theme loaded successfully"
        )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get form theme: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve form theme")

# === SYSTEM THEME ENDPOINTS ===

@router.get("/system", response_model=ThemeListResponse)
async def get_system_themes():
    """Get all system default themes."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, client_id, name, description, theme_config, is_default,
                       is_system_theme, usage_count, last_used_at, created_at, updated_at
                FROM client_themes
                WHERE is_system_theme = true
                ORDER BY name ASC
            """)
            
            themes_data = cursor.fetchall()
            themes = []
            for row in themes_data:
                themes.append(ClientThemeResponse(
                    id=str(row[0]),
                    client_id=None,
                    name=row[2],
                    description=row[3],
                    theme_config=ThemeConfig(**row[4]),
                    is_default=row[5],
                    is_system_theme=row[6],
                    usage_count=row[7],
                    last_used_at=row[8],
                    created_at=row[9],
                    updated_at=row[10]
                ))
            
            return ThemeListResponse(
                themes=themes,
                total_count=len(themes),
                system_themes_count=len(themes)
            )
            
    except Exception as e:
        logger.error(f"Failed to get system themes: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve system themes")