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
import json

from app.database import get_database_connection
from app.routes.admin_api import AdminUserResponse
# from app.routes.admin_api import get_current_admin_user  # TODO: Re-enable when auth is ready
from app.utils.mock_auth import get_mock_admin_user as get_current_admin_user
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
    usage_count: int
    last_used_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class ThemeListResponse(BaseModel):
    """Response for theme list queries."""
    themes: List[ThemeResponse]
    total_count: int

# === UTILITY FUNCTIONS WITH CLIENT SCOPING ===

def verify_theme_ownership(theme_id: str, client_id: str) -> bool:
    """
    Verify that a theme belongs to the specified client.
    Returns False if theme doesn't exist OR belongs to another client.
    """
    try:
        db = get_database_connection()
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
        db = get_database_connection()
        
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
                "usage_count": theme_data.get("usage_count", 0),
                "last_used_at": theme_data.get("last_used_at"),
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
        db = get_database_connection()
        
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
            "is_system_theme": False,
            "usage_count": 0
        }
        
        result = db.client.table("client_themes")\
            .insert(theme_data)\
            .execute()
        
        if not result.data:
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
                "usage_count": created_theme["usage_count"],
                "last_used_at": created_theme.get("last_used_at"),
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
        db = get_database_connection()
        
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
                "usage_count": theme_data.get("usage_count", 0),
                "last_used_at": theme_data.get("last_used_at"),
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
        db = get_database_connection()
        
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
                "usage_count": updated_theme["usage_count"],
                "last_used_at": updated_theme.get("last_used_at"),
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
        db = get_database_connection()
        
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