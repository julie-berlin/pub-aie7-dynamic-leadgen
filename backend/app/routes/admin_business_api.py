"""
Admin Business API - Business Information Management for Admin Interface

This module provides API endpoints for:
1. Managing client business information and settings
2. Branding and customization options
3. Notification preferences and email settings
4. Integration configurations
5. Subscription and plan management
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
from pydantic import BaseModel, Field, EmailStr, validator, HttpUrl
from typing import Dict, Any, List, Optional, Literal
import logging
from datetime import datetime
import uuid
import json

from app.database import get_database_connection
from app.routes.admin_api import get_current_admin_user, AdminUserResponse
from app.utils.response_helpers import create_success_response, create_error_response

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin/business", tags=["admin-business"])

# === PYDANTIC MODELS FOR BUSINESS MANAGEMENT ===

class BusinessInfoUpdateRequest(BaseModel):
    """Request to update business information."""
    business_name: Optional[str] = Field(None, min_length=1, max_length=200)
    business_description: Optional[str] = Field(None, max_length=1000)
    industry: Optional[str] = Field(None, max_length=100)
    website_url: Optional[HttpUrl] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = Field(None, max_length=20)
    business_address: Optional[str] = Field(None, max_length=500)
    timezone: Optional[str] = Field(None, max_length=50)
    business_hours: Optional[Dict[str, Any]] = None

class BrandingConfigRequest(BaseModel):
    """Request to update branding configuration."""
    company_logo_url: Optional[HttpUrl] = None
    favicon_url: Optional[HttpUrl] = None
    primary_color: Optional[str] = Field(None, regex=r'^#[0-9A-Fa-f]{6}$')
    secondary_color: Optional[str] = Field(None, regex=r'^#[0-9A-Fa-f]{6}$')
    accent_color: Optional[str] = Field(None, regex=r'^#[0-9A-Fa-f]{6}$')
    font_family: Optional[str] = Field(None, max_length=100)
    custom_css: Optional[str] = Field(None, max_length=10000)
    custom_javascript: Optional[str] = Field(None, max_length=10000)
    footer_text: Optional[str] = Field(None, max_length=500)

class NotificationSettingsRequest(BaseModel):
    """Request to update notification settings."""
    email_alerts: Optional[bool] = None
    daily_reports: Optional[bool] = None
    weekly_summaries: Optional[bool] = None
    monthly_reports: Optional[bool] = None
    real_time_notifications: Optional[bool] = None
    lead_notification_email: Optional[EmailStr] = None
    notification_frequency: Optional[Literal["immediate", "hourly", "daily"]] = None
    notification_types: Optional[List[str]] = None

class EmailTemplateRequest(BaseModel):
    """Request to update email templates."""
    template_type: Literal["welcome", "qualified_lead", "maybe_lead", "abandoned_form", "daily_report"]
    subject: str = Field(..., min_length=1, max_length=200)
    html_content: str = Field(..., min_length=1)
    text_content: Optional[str] = None
    variables: Optional[Dict[str, str]] = Field(default_factory=dict)

class IntegrationConfigRequest(BaseModel):
    """Request to configure integrations."""
    integration_type: Literal["webhook", "zapier", "salesforce", "hubspot", "mailchimp", "slack"]
    config: Dict[str, Any]
    is_active: bool = Field(default=True)
    description: Optional[str] = None

class SubscriptionUpdateRequest(BaseModel):
    """Request to update subscription information."""
    subscription_tier: Literal["starter", "professional", "enterprise"]
    monthly_form_limit: Optional[int] = Field(None, ge=1)
    monthly_response_limit: Optional[int] = Field(None, ge=1)
    features: Optional[List[str]] = None

class BusinessInfoResponse(BaseModel):
    """Response model for business information."""
    id: str
    business_name: str
    business_description: Optional[str]
    industry: Optional[str]
    website_url: Optional[str]
    contact_email: Optional[str]
    contact_phone: Optional[str]
    business_address: Optional[str]
    timezone: Optional[str]
    business_hours: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

class BrandingConfigResponse(BaseModel):
    """Response model for branding configuration."""
    company_logo_url: Optional[str]
    favicon_url: Optional[str]
    primary_color: str
    secondary_color: str
    accent_color: Optional[str]
    font_family: Optional[str]
    custom_css: Optional[str]
    custom_javascript: Optional[str]
    footer_text: Optional[str]
    updated_at: datetime

class NotificationSettingsResponse(BaseModel):
    """Response model for notification settings."""
    email_alerts: bool
    daily_reports: bool
    weekly_summaries: bool
    monthly_reports: bool
    real_time_notifications: bool
    lead_notification_email: Optional[str]
    notification_frequency: str
    notification_types: List[str]
    updated_at: datetime

class EmailTemplateResponse(BaseModel):
    """Response model for email templates."""
    id: str
    template_type: str
    subject: str
    html_content: str
    text_content: Optional[str]
    variables: Dict[str, str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

class IntegrationResponse(BaseModel):
    """Response model for integrations."""
    id: str
    integration_type: str
    config: Dict[str, Any]
    is_active: bool
    description: Optional[str]
    last_sync_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class SubscriptionResponse(BaseModel):
    """Response model for subscription information."""
    subscription_tier: str
    monthly_form_limit: int
    monthly_response_limit: int
    current_form_count: int
    current_response_count: int
    features: List[str]
    billing_cycle_start: Optional[datetime]
    billing_cycle_end: Optional[datetime]
    updated_at: datetime

# === BUSINESS INFORMATION ENDPOINTS ===

@router.get("/info", response_model=BusinessInfoResponse)
async def get_business_info(
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get current business information."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, business_name, business_description, industry, website_url,
                       contact_email, contact_phone, business_address, timezone,
                       business_hours, created_at, updated_at
                FROM clients 
                WHERE id = %s
            """, (current_user.client_id,))
            
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Business information not found")
            
            return BusinessInfoResponse(
                id=str(result[0]),
                business_name=result[1],
                business_description=result[2],
                industry=result[3],
                website_url=result[4],
                contact_email=result[5],
                contact_phone=result[6],
                business_address=result[7],
                timezone=result[8],
                business_hours=result[9] or {},
                created_at=result[10],
                updated_at=result[11]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get business info: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve business information")

@router.put("/info", response_model=BusinessInfoResponse)
async def update_business_info(
    business_request: BusinessInfoUpdateRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Update business information."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Build dynamic update query
            update_fields = []
            update_values = []
            
            for field_name, field_value in business_request.dict(exclude_unset=True).items():
                if field_value is not None:
                    if field_name == 'business_hours':
                        update_fields.append("business_hours = %s")
                        update_values.append(json.dumps(field_value))
                    else:
                        update_fields.append(f"{field_name} = %s")
                        update_values.append(str(field_value) if isinstance(field_value, HttpUrl) else field_value)
            
            if update_fields:
                update_fields.append("updated_at = NOW()")
                update_values.append(current_user.client_id)
                
                query = f"""
                    UPDATE clients 
                    SET {', '.join(update_fields)}
                    WHERE id = %s
                """
                cursor.execute(query, update_values)
                conn.commit()
            
            # Return updated business info
            return await get_business_info(current_user)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update business info: {e}")
        raise HTTPException(status_code=500, detail="Failed to update business information")

# === BRANDING CONFIGURATION ENDPOINTS ===

@router.get("/branding", response_model=BrandingConfigResponse)
async def get_branding_config(
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get current branding configuration."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT company_logo_url, primary_color, secondary_color, 
                       custom_domain, updated_at
                FROM clients 
                WHERE id = %s
            """, (current_user.client_id,))
            
            client_result = cursor.fetchone()
            
            # Get additional branding settings from client_settings
            cursor.execute("""
                SELECT branding_config, custom_css, custom_javascript, footer_text, updated_at
                FROM client_settings 
                WHERE client_id = %s
            """, (current_user.client_id,))
            
            settings_result = cursor.fetchone()
            
            if not client_result:
                raise HTTPException(status_code=404, detail="Branding configuration not found")
            
            branding_config = settings_result[0] if settings_result else {}
            
            return BrandingConfigResponse(
                company_logo_url=client_result[0],
                favicon_url=branding_config.get('favicon_url'),
                primary_color=client_result[1] or '#3B82F6',
                secondary_color=client_result[2] or '#64748B',
                accent_color=branding_config.get('accent_color'),
                font_family=branding_config.get('font_family'),
                custom_css=settings_result[1] if settings_result else None,
                custom_javascript=settings_result[2] if settings_result else None,
                footer_text=settings_result[3] if settings_result else None,
                updated_at=settings_result[4] if settings_result else client_result[4]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get branding config: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve branding configuration")

@router.put("/branding", response_model=BrandingConfigResponse)
async def update_branding_config(
    branding_request: BrandingConfigRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Update branding configuration."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Update clients table fields
            client_fields = []
            client_values = []
            
            if branding_request.company_logo_url is not None:
                client_fields.append("company_logo_url = %s")
                client_values.append(str(branding_request.company_logo_url))
            
            if branding_request.primary_color is not None:
                client_fields.append("primary_color = %s")
                client_values.append(branding_request.primary_color)
                
            if branding_request.secondary_color is not None:
                client_fields.append("secondary_color = %s")
                client_values.append(branding_request.secondary_color)
            
            if client_fields:
                client_fields.append("updated_at = NOW()")
                client_values.append(current_user.client_id)
                
                client_query = f"""
                    UPDATE clients 
                    SET {', '.join(client_fields)}
                    WHERE id = %s
                """
                cursor.execute(client_query, client_values)
            
            # Update client_settings table
            settings_fields = []
            settings_values = []
            
            branding_config_updates = {}
            if branding_request.favicon_url is not None:
                branding_config_updates['favicon_url'] = str(branding_request.favicon_url)
            if branding_request.accent_color is not None:
                branding_config_updates['accent_color'] = branding_request.accent_color
            if branding_request.font_family is not None:
                branding_config_updates['font_family'] = branding_request.font_family
            
            if branding_config_updates:
                settings_fields.append("branding_config = branding_config || %s")
                settings_values.append(json.dumps(branding_config_updates))
            
            if branding_request.custom_css is not None:
                settings_fields.append("custom_css = %s")
                settings_values.append(branding_request.custom_css)
                
            if branding_request.custom_javascript is not None:
                settings_fields.append("custom_javascript = %s")
                settings_values.append(branding_request.custom_javascript)
                
            if branding_request.footer_text is not None:
                settings_fields.append("footer_text = %s")
                settings_values.append(branding_request.footer_text)
            
            if settings_fields:
                settings_fields.append("updated_at = NOW()")
                settings_values.append(current_user.client_id)
                
                # Ensure client_settings record exists
                cursor.execute("""
                    INSERT INTO client_settings (id, client_id) 
                    VALUES (%s, %s) 
                    ON CONFLICT (client_id) DO NOTHING
                """, (str(uuid.uuid4()), current_user.client_id))
                
                settings_query = f"""
                    UPDATE client_settings 
                    SET {', '.join(settings_fields)}
                    WHERE client_id = %s
                """
                cursor.execute(settings_query, settings_values)
            
            conn.commit()
            
            # Return updated branding config
            return await get_branding_config(current_user)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update branding config: {e}")
        raise HTTPException(status_code=500, detail="Failed to update branding configuration")

# === NOTIFICATION SETTINGS ENDPOINTS ===

@router.get("/notifications", response_model=NotificationSettingsResponse)
async def get_notification_settings(
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get current notification settings."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT notification_settings, updated_at
                FROM clients 
                WHERE id = %s
            """, (current_user.client_id,))
            
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Notification settings not found")
            
            settings = result[0] or {
                "email_alerts": True,
                "daily_reports": True,
                "weekly_summaries": True,
                "monthly_reports": False,
                "real_time_notifications": True,
                "notification_frequency": "immediate",
                "notification_types": ["qualified_leads", "form_abandonment"]
            }
            
            return NotificationSettingsResponse(
                email_alerts=settings.get('email_alerts', True),
                daily_reports=settings.get('daily_reports', True),
                weekly_summaries=settings.get('weekly_summaries', True),
                monthly_reports=settings.get('monthly_reports', False),
                real_time_notifications=settings.get('real_time_notifications', True),
                lead_notification_email=settings.get('lead_notification_email'),
                notification_frequency=settings.get('notification_frequency', 'immediate'),
                notification_types=settings.get('notification_types', []),
                updated_at=result[1]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get notification settings: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve notification settings")

@router.put("/notifications", response_model=NotificationSettingsResponse)
async def update_notification_settings(
    notification_request: NotificationSettingsRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Update notification settings."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Get current settings
            cursor.execute("""
                SELECT notification_settings FROM clients WHERE id = %s
            """, (current_user.client_id,))
            
            result = cursor.fetchone()
            current_settings = result[0] if result and result[0] else {}
            
            # Update with new values
            for field_name, field_value in notification_request.dict(exclude_unset=True).items():
                if field_value is not None:
                    current_settings[field_name] = field_value
            
            # Update database
            cursor.execute("""
                UPDATE clients 
                SET notification_settings = %s, updated_at = NOW()
                WHERE id = %s
            """, (json.dumps(current_settings), current_user.client_id))
            
            conn.commit()
            
            # Return updated settings
            return await get_notification_settings(current_user)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update notification settings: {e}")
        raise HTTPException(status_code=500, detail="Failed to update notification settings")

# === SUBSCRIPTION MANAGEMENT ENDPOINTS ===

@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription_info(
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get current subscription information."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT subscription_tier, monthly_form_limit, monthly_response_limit, updated_at
                FROM clients 
                WHERE id = %s
            """, (current_user.client_id,))
            
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Subscription information not found")
            
            # Get current usage counts
            cursor.execute("""
                SELECT COUNT(*) FROM forms WHERE client_id = %s AND is_active = true
            """, (current_user.client_id,))
            current_form_count = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(*) 
                FROM lead_sessions ls
                JOIN forms f ON f.id = ls.form_id
                WHERE f.client_id = %s 
                AND ls.started_at >= date_trunc('month', CURRENT_DATE)
            """, (current_user.client_id,))
            current_response_count = cursor.fetchone()[0]
            
            # Define features by tier
            tier_features = {
                "starter": ["basic_analytics", "email_notifications", "5_forms"],
                "professional": ["advanced_analytics", "custom_themes", "integrations", "50_forms", "priority_support"],
                "enterprise": ["unlimited_forms", "white_label", "api_access", "dedicated_support", "custom_integrations"]
            }
            
            return SubscriptionResponse(
                subscription_tier=result[0],
                monthly_form_limit=result[1],
                monthly_response_limit=result[2],
                current_form_count=current_form_count,
                current_response_count=current_response_count,
                features=tier_features.get(result[0], []),
                billing_cycle_start=None,  # Would come from billing system
                billing_cycle_end=None,    # Would come from billing system
                updated_at=result[3]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get subscription info: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve subscription information")

@router.put("/subscription", response_model=SubscriptionResponse)
async def update_subscription(
    subscription_request: SubscriptionUpdateRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Update subscription information."""
    try:
        # In a real implementation, this would integrate with a billing system
        # For now, we'll just update the database fields
        
        conn = get_database_connection()
        with conn.cursor() as cursor:
            update_fields = []
            update_values = []
            
            if subscription_request.subscription_tier:
                update_fields.append("subscription_tier = %s")
                update_values.append(subscription_request.subscription_tier)
                
                # Set default limits based on tier
                tier_limits = {
                    "starter": {"forms": 5, "responses": 1000},
                    "professional": {"forms": 50, "responses": 10000},
                    "enterprise": {"forms": 999, "responses": 100000}
                }
                
                limits = tier_limits.get(subscription_request.subscription_tier, {"forms": 5, "responses": 1000})
                update_fields.extend(["monthly_form_limit = %s", "monthly_response_limit = %s"])
                update_values.extend([limits["forms"], limits["responses"]])
            
            if subscription_request.monthly_form_limit:
                update_fields.append("monthly_form_limit = %s")
                update_values.append(subscription_request.monthly_form_limit)
                
            if subscription_request.monthly_response_limit:
                update_fields.append("monthly_response_limit = %s")
                update_values.append(subscription_request.monthly_response_limit)
            
            if update_fields:
                update_fields.append("updated_at = NOW()")
                update_values.append(current_user.client_id)
                
                query = f"""
                    UPDATE clients 
                    SET {', '.join(update_fields)}
                    WHERE id = %s
                """
                cursor.execute(query, update_values)
                conn.commit()
            
            # Return updated subscription info
            return await get_subscription_info(current_user)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update subscription: {e}")
        raise HTTPException(status_code=500, detail="Failed to update subscription")

# === UTILITY ENDPOINTS ===

@router.get("/usage-stats")
async def get_usage_stats(
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get current usage statistics for the client."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Get forms count
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_forms,
                    COUNT(CASE WHEN is_active = true THEN 1 END) as active_forms,
                    COUNT(CASE WHEN status = 'draft' THEN 1 END) as draft_forms
                FROM forms 
                WHERE client_id = %s
            """, (current_user.client_id,))
            
            forms_stats = cursor.fetchone()
            
            # Get responses count (current month)
            cursor.execute("""
                SELECT COUNT(*) 
                FROM lead_sessions ls
                JOIN forms f ON f.id = ls.form_id
                WHERE f.client_id = %s 
                AND ls.started_at >= date_trunc('month', CURRENT_DATE)
            """, (current_user.client_id,))
            
            monthly_responses = cursor.fetchone()[0]
            
            # Get total responses (all time)
            cursor.execute("""
                SELECT COUNT(*) 
                FROM lead_sessions ls
                JOIN forms f ON f.id = ls.form_id
                WHERE f.client_id = %s
            """, (current_user.client_id,))
            
            total_responses = cursor.fetchone()[0]
            
            # Get subscription limits
            cursor.execute("""
                SELECT monthly_form_limit, monthly_response_limit, subscription_tier
                FROM clients 
                WHERE id = %s
            """, (current_user.client_id,))
            
            limits = cursor.fetchone()
            
            return create_success_response(
                message="Usage statistics retrieved successfully",
                data={
                    "forms": {
                        "total": forms_stats[0],
                        "active": forms_stats[1],
                        "draft": forms_stats[2],
                        "limit": limits[0] if limits else 5
                    },
                    "responses": {
                        "this_month": monthly_responses,
                        "total": total_responses,
                        "monthly_limit": limits[1] if limits else 1000
                    },
                    "subscription_tier": limits[2] if limits else "starter",
                    "usage_percentage": {
                        "forms": (forms_stats[1] / limits[0] * 100) if limits and limits[0] > 0 else 0,
                        "responses": (monthly_responses / limits[1] * 100) if limits and limits[1] > 0 else 0
                    }
                }
            )
            
    except Exception as e:
        logger.error(f"Failed to get usage stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve usage statistics")