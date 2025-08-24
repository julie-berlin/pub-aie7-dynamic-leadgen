"""
Themes API - RESTful Theme Management Endpoints

This module provides clean RESTful API endpoints for:
1. Creating, reading, updating, and deleting themes
2. Theme configuration management with multi-tenant security  
3. Color and font customization management
4. All operations are automatically scoped to the authenticated client

SECURITY: All endpoints enforce row-level security - each client can only
access their own themes. Cross-client access attempts return 404.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import Dict, Any, List, Optional, Literal
import logging
from datetime import datetime
import uuid

from app.database import db
from app.routes.admin_auth import AdminUserResponse
from app.routes.admin_auth import get_current_admin_user
from app.utils.response_helpers import success_response, error_response
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/themes", tags=["themes"])

# === PYDANTIC MODELS ===

class ThemeColorsConfig(BaseModel):
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

class ThemeTypographyConfig(BaseModel):
    """Typography configuration for a theme."""
    primary: str = Field(..., description="Primary font family")
    secondary: str = Field(..., description="Secondary font family")

class ThemeSpacingConfig(BaseModel):
    """Spacing configuration for a theme."""
    section: str = Field("2rem", description="Section spacing")
    element: str = Field("1rem", description="Element spacing")

class ThemeConfig(BaseModel):
    """Complete theme configuration."""
    name: str = Field(..., description="Theme name")
    colors: ThemeColorsConfig
    typography: ThemeTypographyConfig
    spacing: ThemeSpacingConfig
    borderRadius: str = Field("0.5rem", description="Default border radius")
    borderRadiusLg: str = Field("0.75rem", description="Large border radius")
    shadow: str = Field("0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)", description="Default shadow")
    shadowLg: str = Field("0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)", description="Large shadow")
    logo_url: Optional[str] = Field(None, description="Logo URL for branded forms")

class ThemeCreateRequest(BaseModel):
    """Request to create a new theme."""
    name: str = Field(..., description="Theme name")
    description: Optional[str] = Field(None, description="Theme description")
    theme_config: ThemeConfig
    primary_color: str = Field(..., description="Primary color (extracted from theme_config)")
    secondary_color: str = Field(..., description="Secondary color (extracted from theme_config)")
    font_family: str = Field(..., description="Font family (extracted from theme_config)")
    is_default: bool = Field(False, description="Set as client default theme")

class ThemeUpdateRequest(BaseModel):
    """Request to update an existing theme."""
    name: Optional[str] = Field(None, description="Theme name")
    description: Optional[str] = Field(None, description="Theme description")
    theme_config: Optional[ThemeConfig] = Field(None, description="Theme configuration")
    primary_color: Optional[str] = Field(None, description="Primary color")
    secondary_color: Optional[str] = Field(None, description="Secondary color")
    font_family: Optional[str] = Field(None, description="Font family")
    is_default: Optional[bool] = Field(None, description="Set as client default theme")

class ThemeResponse(BaseModel):
    """Response model for themes."""
    id: str
    client_id: str
    name: str
    description: Optional[str]
    theme_config: ThemeConfig
    primary_color: str
    secondary_color: str
    font_family: str
    is_default: bool
    is_system_theme: bool
    created_at: datetime
    updated_at: datetime

class ThemeListResponse(BaseModel):
    """Response for theme list queries."""
    themes: List[ThemeResponse]
    total_count: int

# === UTILITY FUNCTIONS WITH CLIENT SCOPING ===

def transform_theme_to_frontend_format(admin_theme_config: dict) -> dict:
    """
    Transform admin-saved theme config to complete frontend ThemeConfig format.
    
    Admin saves: {primary_color, font_family, border_radius, logo_url, custom_css}
    Frontend expects: Complete ThemeConfig with colors, typography, spacing, etc.
    """
    primary_color = admin_theme_config.get('primary_color', '#3b82f6')
    font_family = admin_theme_config.get('font_family', 'Inter')
    border_radius = admin_theme_config.get('border_radius', '0.5rem')
    logo_url = admin_theme_config.get('logo_url')
    custom_css = admin_theme_config.get('custom_css')
    
    # Generate color variations from primary color
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(r, g, b):
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def darken_color(hex_color, factor=0.8):
        r, g, b = hex_to_rgb(hex_color)
        r = int(r * factor)
        g = int(g * factor) 
        b = int(b * factor)
        return rgb_to_hex(r, g, b)
    
    def lighten_color(hex_color, factor=0.9):
        r, g, b = hex_to_rgb(hex_color)
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        return rgb_to_hex(r, g, b)
    
    # Generate theme variations
    primary_hover = darken_color(primary_color, 0.85)
    primary_light = lighten_color(primary_color, 0.85)
    
    theme_data = {
        "name": "Custom Theme",
        "colors": {
            "primary": primary_color,
            "primaryHover": primary_hover,
            "primaryLight": primary_light,
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
            "primary": f"{font_family}, sans-serif",
            "secondary": f"{font_family}, sans-serif"
        },
        "spacing": {
            "section": "2rem",
            "element": "1rem",
            "page": "2rem",
            "input": "1rem",
            "button": "0.75rem 1.5rem"
        },
        "borderRadius": border_radius,
        "borderRadiusLg": "0.75rem",
        "shadow": "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
        "shadowLg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
    }
    
    # Add logo and custom CSS if provided
    if logo_url:
        theme_data["logo_url"] = logo_url
    if custom_css:
        theme_data["custom_css"] = custom_css
        
    return theme_data

def verify_theme_ownership(theme_id: str, client_id: str) -> bool:
    """
    Verify that a theme belongs to the specified client.
    Returns False if theme doesn't exist OR belongs to another client.
    """
    try:
        # Use Supabase client
        result = db.client.table("client_themes")\
            .select("id")\
            .eq("id", theme_id)\
            .eq("client_id", client_id)\
            .execute()
        
        return len(result.data) > 0
    except Exception as e:
        logger.error(f"Error verifying theme ownership: {e}")
        return False

# === THEME CRUD ENDPOINTS ===

@router.get("/")
async def list_themes(
    include_system: bool = Query(True, description="Include system themes"),
    limit: int = Query(50, ge=1, le=100, description="Number of themes to return"),
    offset: int = Query(0, ge=0, description="Number of themes to skip"),
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """List all themes for the authenticated client."""
    try:
        # Use Supabase client
        
        # Build query based on whether to include system themes
        query = db.client.table("client_themes").select("*")
        
        if include_system:
            query = query.or_(f"client_id.eq.{current_user.client_id},is_system_theme.eq.true")
        else:
            query = query.eq("client_id", current_user.client_id)
        
        # Execute query with pagination
        result = query.order("is_default", desc=True)\
                     .order("name")\
                     .range(offset, offset + limit - 1)\
                     .execute()
        
        # Count total themes
        count_query = db.client.table("client_themes").select("id", count="exact")
        if include_system:
            count_query = count_query.or_(f"client_id.eq.{current_user.client_id},is_system_theme.eq.true")
        else:
            count_query = count_query.eq("client_id", current_user.client_id)
        
        count_result = count_query.execute()
        total_count = count_result.count if count_result.count else 0
        
        # Format response
        themes = []
        for theme_data in result.data:
            themes.append({
                "id": theme_data["id"],
                "client_id": theme_data["client_id"],
                "name": theme_data["name"],
                "description": theme_data["description"],
                "theme_config": theme_data["theme_config"],
                "primary_color": theme_data.get("primary_color", "#3B82F6"),
                "secondary_color": theme_data.get("secondary_color", "#64748B"),
                "font_family": theme_data.get("font_family", "Inter, system-ui, sans-serif"),
                "is_default": theme_data["is_default"],
                "is_system_theme": theme_data["is_system_theme"],
                "created_at": theme_data["created_at"],
                "updated_at": theme_data["updated_at"]
            })
        
        return success_response(
            data={
                "themes": themes,
                "total_count": total_count,
                "limit": limit,
                "offset": offset
            },
            message="Themes retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to list themes: {e}")
        return error_response("Failed to retrieve themes", status_code=500)

@router.post("/")
async def create_theme(
    theme_request: ThemeCreateRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Create a new theme for the authenticated client."""
    try:
        logger.info(f"Creating theme for client {current_user.client_id}: {theme_request}")
        # Use Supabase client
        
        # If setting as default, unset other default themes for this client
        if theme_request.is_default:
            db.client.table("client_themes")\
                .update({"is_default": False})\
                .eq("client_id", current_user.client_id)\
                .eq("is_default", True)\
                .execute()
        
        # Create new theme
        theme_id = str(uuid.uuid4())
        theme_data = {
            "id": theme_id,
            "client_id": current_user.client_id,
            "name": theme_request.name,
            "description": theme_request.description,
            "theme_config": theme_request.theme_config.model_dump(),
            "primary_color": theme_request.primary_color,
            "secondary_color": theme_request.secondary_color,
            "font_family": theme_request.font_family,
            "is_default": theme_request.is_default,
            "is_system_theme": False
        }
        
        result = db.client.table("client_themes")\
            .insert(theme_data)\
            .execute()
        
        logger.info(f"Theme creation result: {result}")
        
        if not result.data:
            logger.error(f"Theme creation failed - no data returned: {result}")
            return error_response("Failed to create theme", status_code=500)
        
        created_theme = result.data[0]
        
        return success_response(
            data={
                "id": created_theme["id"],
                "client_id": created_theme["client_id"],
                "name": created_theme["name"],
                "description": created_theme["description"],
                "theme_config": created_theme["theme_config"],
                "primary_color": created_theme["primary_color"],
                "secondary_color": created_theme["secondary_color"],
                "font_family": created_theme["font_family"],
                "is_default": created_theme["is_default"],
                "is_system_theme": created_theme["is_system_theme"],
                "created_at": created_theme["created_at"],
                "updated_at": created_theme["updated_at"]
            },
            message="Theme created successfully",
            status_code=201
        )
        
    except Exception as e:
        logger.error(f"Failed to create theme: {e}")
        if "duplicate key" in str(e).lower() or "unique constraint" in str(e).lower():
            return error_response("Theme name already exists for this client", status_code=409)
        return error_response("Failed to create theme", status_code=500)

@router.get("/{theme_id}")
async def get_theme(
    theme_id: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get a specific theme by ID."""
    try:
        # Use Supabase client
        
        # Query with client scoping (includes system themes)
        result = db.client.table("client_themes")\
            .select("*")\
            .eq("id", theme_id)\
            .or_(f"client_id.eq.{current_user.client_id},is_system_theme.eq.true")\
            .execute()
        
        if not result.data:
            return error_response("Theme not found", status_code=404)
        
        theme_data = result.data[0]
        
        return success_response(
            data={
                "id": theme_data["id"],
                "client_id": theme_data["client_id"],
                "name": theme_data["name"],
                "description": theme_data["description"],
                "theme_config": theme_data["theme_config"],
                "primary_color": theme_data.get("primary_color", "#3B82F6"),
                "secondary_color": theme_data.get("secondary_color", "#64748B"),
                "font_family": theme_data.get("font_family", "Inter, system-ui, sans-serif"),
                "is_default": theme_data["is_default"],
                "is_system_theme": theme_data["is_system_theme"],
                "created_at": theme_data["created_at"],
                "updated_at": theme_data["updated_at"]
            },
            message="Theme retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to get theme: {e}")
        return error_response("Failed to retrieve theme", status_code=500)

@router.put("/{theme_id}")
async def update_theme(
    theme_id: str,
    theme_request: ThemeUpdateRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Update an existing theme."""
    try:
        # Use Supabase client
        
        # Verify ownership (only client's own themes, not system themes)
        if not verify_theme_ownership(theme_id, current_user.client_id):
            return error_response("Theme not found", status_code=404)
        
        # Check if it's a system theme (cannot modify)
        theme_check = db.client.table("client_themes")\
            .select("is_system_theme")\
            .eq("id", theme_id)\
            .execute()
        
        if theme_check.data and theme_check.data[0]["is_system_theme"]:
            return error_response("Cannot modify system themes", status_code=403)
        
        # If setting as default, unset other default themes
        if theme_request.is_default:
            db.client.table("client_themes")\
                .update({"is_default": False})\
                .eq("client_id", current_user.client_id)\
                .eq("is_default", True)\
                .neq("id", theme_id)\
                .execute()
        
        # Build update data
        update_data = {}
        if theme_request.name is not None:
            update_data["name"] = theme_request.name
        if theme_request.description is not None:
            update_data["description"] = theme_request.description
        if theme_request.theme_config is not None:
            update_data["theme_config"] = theme_request.theme_config.model_dump()
        if theme_request.primary_color is not None:
            update_data["primary_color"] = theme_request.primary_color
        if theme_request.secondary_color is not None:
            update_data["secondary_color"] = theme_request.secondary_color
        if theme_request.font_family is not None:
            update_data["font_family"] = theme_request.font_family
        if theme_request.is_default is not None:
            update_data["is_default"] = theme_request.is_default
        
        # Update theme
        result = db.client.table("client_themes")\
            .update(update_data)\
            .eq("id", theme_id)\
            .execute()
        
        if not result.data:
            return error_response("Failed to update theme", status_code=500)
        
        updated_theme = result.data[0]
        
        return success_response(
            data={
                "id": updated_theme["id"],
                "client_id": updated_theme["client_id"],
                "name": updated_theme["name"],
                "description": updated_theme["description"],
                "theme_config": updated_theme["theme_config"],
                "primary_color": updated_theme["primary_color"],
                "secondary_color": updated_theme["secondary_color"],
                "font_family": updated_theme["font_family"],
                "is_default": updated_theme["is_default"],
                "is_system_theme": updated_theme["is_system_theme"],
                "created_at": updated_theme["created_at"],
                "updated_at": updated_theme["updated_at"]
            },
            message="Theme updated successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to update theme: {e}")
        return error_response("Failed to update theme", status_code=500)

@router.delete("/{theme_id}")
async def delete_theme(
    theme_id: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Delete a theme."""
    try:
        # Use Supabase client
        
        # Verify ownership (only client's own themes, not system themes)
        if not verify_theme_ownership(theme_id, current_user.client_id):
            return error_response("Theme not found", status_code=404)
        
        # Check if it's a system theme (cannot delete)
        theme_check = db.client.table("client_themes")\
            .select("is_system_theme")\
            .eq("id", theme_id)\
            .execute()
        
        if theme_check.data and theme_check.data[0]["is_system_theme"]:
            return error_response("Cannot delete system themes", status_code=403)
        
        # Check if theme is being used by any forms
        forms_using_theme = db.client.table("forms")\
            .select("id", count="exact")\
            .eq("client_id", current_user.client_id)\
            .contains("theme_config", {"theme_id": theme_id})\
            .execute()
        
        if forms_using_theme.count and forms_using_theme.count > 0:
            return error_response(
                f"Cannot delete theme: {forms_using_theme.count} forms are using this theme",
                status_code=409
            )
        
        # Delete theme
        result = db.client.table("client_themes")\
            .delete()\
            .eq("id", theme_id)\
            .execute()
        
        return success_response(
            data={"theme_id": theme_id},
            message="Theme deleted successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to delete theme: {e}")
        return error_response("Failed to delete theme", status_code=500)

# === FORM THEME ENDPOINTS ===

@router.get("/form/{form_id}/theme")
async def get_form_theme(form_id: str):
    """
    Get the effective theme for a form (form-specific or client default).
    
    This endpoint is called by the frontend form application to load theme configuration.
    No authentication required as this is called by public forms.
    """
    try:
        
        # Get form data including theme_config
        form_data = db.get_form(form_id)
        if not form_data:
            return error_response("Form not found", status_code=404)
        
        # Check if form has a specific theme_config
        theme_config = form_data.get('theme_config')
        
        if theme_config:
            logger.info(f"Found theme_config for form {form_id}: {type(theme_config)}")
            # Transform admin-format theme config to frontend format
            transformed_theme = transform_theme_to_frontend_format(theme_config)
            return success_response(
                data=transformed_theme,
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
                        # Transform client default theme to frontend format
                        transformed_theme = transform_theme_to_frontend_format(theme_config)
                        return success_response(
                            data=transformed_theme,
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
                "element": "1rem",
                "page": "2rem",
                "input": "1rem",
                "button": "0.75rem 1.5rem"
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
            
    except Exception as e:
        logger.error(f"Failed to get form theme: {e}")
        return error_response("Failed to retrieve form theme", status_code=500)