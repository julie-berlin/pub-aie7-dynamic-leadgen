#!/usr/bin/env python3
"""
Generate TypeScript types from Pydantic models.

This script creates TypeScript type definitions that match our Pydantic models,
ensuring type safety between backend and frontend.
"""

import json
from typing import get_type_hints, get_origin, get_args, Union
from datetime import datetime
from enum import Enum

# Import our Pydantic models
from pydantic_models import (
    StartSessionRequest,
    SubmitResponsesRequest,
    AbandonSessionRequest,
    StartSessionResponse,
    StepResponse,
    CompletionResponse,
    SessionStatusResponse,
    ErrorResponse,
    QuestionData,
    LeadStatus,
    AbandonmentStatus,
    CompletionType,
    FlowPhase,
    FlowStrategy
)

# Import Phase 2 models
try:
    from app.routes.theme_api import (
        ThemeColors,
        ThemeTypography,
        ThemeSpacing,
        ThemeConfig,
        ClientThemeRequest,
        ClientThemeResponse,
        FormDisplaySettings,
        FormConfigRequest,
        FormConfigResponse,
        ThemeListResponse
    )
    from app.routes.analytics_api import (
        EventTrackingRequest,
        FormMetrics,
        FormPerformanceResponse,
        AnalyticsTimeSeriesData,
        FormAnalyticsDashboard,
        EventAnalyticsResponse
    )
    from app.routes.admin_api import (
        AdminUserRegister,
        AdminUserLogin,
        AdminUserResponse,
        AdminTokenResponse,
        ClientSettingsRequest,
        ClientSettingsResponse,
        TeamInviteRequest,
        TeamMemberResponse
    )
    PHASE2_AVAILABLE = True
except ImportError as e:
    PHASE2_AVAILABLE = False


def pydantic_to_typescript_type(pydantic_type, optional=False) -> str:
    """Convert Python/Pydantic types to TypeScript types."""
    
    # Handle Optional types
    origin = get_origin(pydantic_type)
    if origin is not None:
        args = get_args(pydantic_type)
        
        # Handle Union types (Optional is Union[T, None])
        if origin is Union:
            # Check if it's Optional (Union with None)
            if len(args) == 2 and type(None) in args:
                non_none_type = next(arg for arg in args if arg is not type(None))
                return pydantic_to_typescript_type(non_none_type, optional=True)
            # Handle other unions
            else:
                union_types = [pydantic_to_typescript_type(arg) for arg in args]
                result = " | ".join(union_types)
                return f"({result})" + ("?" if optional else "")
        
        # Handle List types
        elif origin is list:
            item_type = pydantic_to_typescript_type(args[0])
            result = f"{item_type}[]"
            return result + ("?" if optional else "")
        
        # Handle Dict types
        elif origin is dict:
            if len(args) >= 2:
                key_type = pydantic_to_typescript_type(args[0])
                value_type = pydantic_to_typescript_type(args[1])
                result = f"Record<{key_type}, {value_type}>"
            else:
                result = "Record<string, any>"
            return result + ("?" if optional else "")
    
    # Handle basic types
    type_mapping = {
        str: "string",
        int: "number",
        float: "number",
        bool: "boolean",
        datetime: "string",  # ISO date strings
        type(None): "null",
        dict: "Record<string, any>",
        list: "any[]",
        "Any": "any"
    }
    
    # Handle string representation of types
    type_str = str(pydantic_type)
    if "EmailStr" in type_str:
        result = "string"
        return result + ("?" if optional else "")
    if "Decimal" in type_str:
        result = "number"
        return result + ("?" if optional else "")
    
    # Handle Literal types
    if origin and str(origin) == "typing.Literal":
        literal_values = [f'"{str(arg)}"' for arg in args]
        result = " | ".join(literal_values)
        return result + ("?" if optional else "")
    
    # Handle enum types
    if isinstance(pydantic_type, type) and issubclass(pydantic_type, Enum):
        enum_values = [f'"{value.value}"' for value in pydantic_type]
        result = " | ".join(enum_values)
        return result + ("?" if optional else "")
    
    # Direct type mapping
    ts_type = type_mapping.get(pydantic_type, "any")
    return ts_type + ("?" if optional else "")


def generate_interface_from_model(model_class, interface_name=None) -> str:
    """Generate TypeScript interface from Pydantic model."""
    
    if interface_name is None:
        interface_name = model_class.__name__
    
    # Get model fields and their types (Pydantic v2 compatible)
    fields = model_class.model_fields
    
    lines = [f"export interface {interface_name} {{"]
    
    for field_name, field_info in fields.items():
        # Determine if field is optional (Pydantic v2)
        is_optional = field_info.is_required() == False
        
        # Get TypeScript type (Pydantic v2)
        ts_type = pydantic_to_typescript_type(field_info.annotation, optional=is_optional)
        
        # Add description as comment if available
        description = field_info.description
        if description:
            lines.append(f"  /** {description} */")
        
        # Add field (remove redundant ? from type if already marked optional)
        optional_marker = "?" if is_optional else ""
        if optional_marker and ts_type.endswith("?"):
            ts_type = ts_type[:-1]  # Remove trailing ? from type
        lines.append(f"  {field_name}{optional_marker}: {ts_type};")
    
    lines.append("}")
    
    return "\n".join(lines)


def generate_enum_from_model(enum_class) -> str:
    """Generate TypeScript enum from Python Enum."""
    
    enum_name = enum_class.__name__
    lines = [f"export enum {enum_name} {{"]
    
    for member in enum_class:
        lines.append(f"  {member.name} = '{member.value}',")
    
    lines.append("}")
    
    return "\n".join(lines)


def main():
    """Generate complete TypeScript definitions."""
    
    typescript_content = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Add header
    typescript_content.append(f"""/**
 * Auto-generated TypeScript types for Dynamic Survey Platform
 * Generated from Pydantic models
 * 
 * Last updated: {current_date}
 * 
 * DO NOT EDIT MANUALLY - This file is auto-generated
 * Run `python3 backend/generate_typescript_types.py` to update
 * 
 * Phase 2 Support: {"✅ Included" if PHASE2_AVAILABLE else "❌ Not Available"}
 */

""")
    
    # Generate enums
    enums = [LeadStatus, AbandonmentStatus, CompletionType, FlowPhase, FlowStrategy]
    
    typescript_content.append("// === CORE ENUMS ===\n")
    
    for enum_class in enums:
        typescript_content.append(generate_enum_from_model(enum_class))
        typescript_content.append("")
    
    # Generate core survey interfaces
    survey_models = [
        StartSessionRequest,
        SubmitResponsesRequest, 
        AbandonSessionRequest,
        StartSessionResponse,
        StepResponse,
        CompletionResponse,
        SessionStatusResponse,
        ErrorResponse,
        QuestionData
    ]
    
    typescript_content.append("// === CORE SURVEY API TYPES ===\n")
    
    for model_class in survey_models:
        typescript_content.append(generate_interface_from_model(model_class))
        typescript_content.append("")
    
    # Generate Phase 2 types if available
    if PHASE2_AVAILABLE:
        # Theme API types
        theme_models = [
            ThemeColors,
            ThemeTypography,
            ThemeSpacing,
            ThemeConfig,
            ClientThemeRequest,
            ClientThemeResponse,
            FormDisplaySettings,
            FormConfigRequest,
            FormConfigResponse,
            ThemeListResponse
        ]
        
        typescript_content.append("// === THEME MANAGEMENT API TYPES ===\n")
        
        for model_class in theme_models:
            typescript_content.append(generate_interface_from_model(model_class))
            typescript_content.append("")
        
        # Analytics API types
        analytics_models = [
            EventTrackingRequest,
            FormMetrics,
            FormPerformanceResponse,
            AnalyticsTimeSeriesData,
            FormAnalyticsDashboard,
            EventAnalyticsResponse
        ]
        
        typescript_content.append("// === ANALYTICS API TYPES ===\n")
        
        for model_class in analytics_models:
            typescript_content.append(generate_interface_from_model(model_class))
            typescript_content.append("")
        
        # Admin API types
        admin_models = [
            AdminUserRegister,
            AdminUserLogin,
            AdminUserResponse,
            AdminTokenResponse,
            ClientSettingsRequest,
            ClientSettingsResponse,
            TeamInviteRequest,
            TeamMemberResponse
        ]
        
        typescript_content.append("// === ADMIN MANAGEMENT API TYPES ===\n")
        
        for model_class in admin_models:
            typescript_content.append(generate_interface_from_model(model_class))
            typescript_content.append("")
    
    # Add utility types
    typescript_content.append("""// === UTILITY TYPES ===

export interface ResponseSubmission {
  /** Question being answered */
  question_id: number;
  /** User's answer */
  answer: string;
  /** Original question text (for logging) */
  question_text?: string;
  /** Time taken to answer in seconds */
  response_time_seconds?: number;
}

export interface AbandonResponse {
  /** Operation status */
  status: string;
  /** Confirmation message */
  message: string;
}

// === API CLIENT TYPES ===

export interface ApiResponse<T> {
  data?: T;
  error?: ErrorResponse;
  success: boolean;
}

export interface SurveyApiClient {
  startSession(request: StartSessionRequest): Promise<ApiResponse<StartSessionResponse>>;
  submitResponses(request: SubmitResponsesRequest): Promise<ApiResponse<StepResponse>>;
  abandonSession(request: AbandonSessionRequest): Promise<ApiResponse<AbandonResponse>>;
  getSessionStatus(sessionId: string): Promise<ApiResponse<SessionStatusResponse>>;
}""")

    if PHASE2_AVAILABLE:
        typescript_content.append("""

// === PHASE 2 API CLIENTS ===

export interface ThemeApiClient {
  getClientThemes(clientId: string, includeSystem?: boolean): Promise<ApiResponse<ThemeListResponse>>;
  createClientTheme(clientId: string, theme: ClientThemeRequest): Promise<ApiResponse<ClientThemeResponse>>;
  getTheme(themeId: string): Promise<ApiResponse<ClientThemeResponse>>;
  updateTheme(themeId: string, theme: ClientThemeRequest): Promise<ApiResponse<ClientThemeResponse>>;
  deleteTheme(themeId: string): Promise<ApiResponse<{status: string; message: string}>>;
  getFormConfig(formId: string): Promise<ApiResponse<FormConfigResponse>>;
  updateFormConfig(formId: string, config: FormConfigRequest): Promise<ApiResponse<FormConfigResponse>>;
  getFormTheme(formId: string): Promise<ApiResponse<ThemeConfig>>;
  getSystemThemes(): Promise<ApiResponse<ThemeListResponse>>;
}

export interface AnalyticsApiClient {
  trackEvent(event: EventTrackingRequest): Promise<ApiResponse<{status: string; message: string}>>;
  trackEventsBatch(events: EventTrackingRequest[]): Promise<ApiResponse<{status: string; processed: number}>>;
  getFormPerformance(formId: string, startDate?: string, endDate?: string, period?: 'daily' | 'weekly' | 'monthly'): Promise<ApiResponse<FormPerformanceResponse>>;
  getFormDashboard(formId: string, days?: number): Promise<ApiResponse<FormAnalyticsDashboard>>;
  getFormEvents(formId: string, days?: number, eventType?: string): Promise<ApiResponse<EventAnalyticsResponse>>;
  recalculateMetrics(formId: string): Promise<ApiResponse<{status: string; message: string}>>;
}

export interface AdminApiClient {
  register(user: AdminUserRegister): Promise<ApiResponse<AdminTokenResponse>>;
  login(credentials: AdminUserLogin): Promise<ApiResponse<AdminTokenResponse>>;
  getCurrentUser(): Promise<ApiResponse<AdminUserResponse>>;
  getClientSettings(): Promise<ApiResponse<ClientSettingsResponse>>;
  updateClientSettings(settings: ClientSettingsRequest): Promise<ApiResponse<ClientSettingsResponse>>;
  getTeamMembers(): Promise<ApiResponse<TeamMemberResponse[]>>;
  inviteTeamMember(invite: TeamInviteRequest): Promise<ApiResponse<TeamMemberResponse>>;
  removeTeamMember(userId: string): Promise<ApiResponse<{status: string; message: string}>>;
}""")

    typescript_content.append("""

// === FRONTEND HELPERS ===

export interface FormState {
  sessionId: string | null;
  currentStep: number;
  completed: boolean;
  questions: QuestionData[];
  responses: ResponseSubmission[];
  leadStatus: LeadStatus;
  abandonment_status: AbandonmentStatus;
}

export interface ProgressInfo {
  currentStep: number;
  totalSteps: number;
  completionPercentage: number;
  questionsAnswered: number;
}

export interface UTMParams {
  utm_source?: string;
  utm_medium?: string; 
  utm_campaign?: string;
  utm_content?: string;
  utm_term?: string;
}

// === API ENDPOINTS ===

export const API_ENDPOINTS = {
  // Survey API
  START_SESSION: '/api/survey/start',
  SUBMIT_RESPONSES: '/api/survey/step',
  ABANDON_SESSION: '/api/survey/abandon',
  SESSION_STATUS: '/api/survey/status',""")

    if PHASE2_AVAILABLE:
        typescript_content.append("""
  
  // Theme API
  CLIENT_THEMES: '/api/themes/client',
  THEME_BY_ID: '/api/themes/theme',
  FORM_CONFIG: '/api/themes/form',
  SYSTEM_THEMES: '/api/themes/system',
  
  // Analytics API
  TRACK_EVENT: '/api/analytics/events/track',
  TRACK_BATCH: '/api/analytics/events/track/batch',
  FORM_PERFORMANCE: '/api/analytics/form',
  FORM_DASHBOARD: '/api/analytics/form',
  FORM_EVENTS: '/api/analytics/form',
  
  // Admin API
  ADMIN_REGISTER: '/api/admin/auth/register',
  ADMIN_LOGIN: '/api/admin/auth/login',
  ADMIN_ME: '/api/admin/auth/me',
  CLIENT_SETTINGS: '/api/admin/client/settings',
  TEAM_MEMBERS: '/api/admin/team/members',
  TEAM_INVITE: '/api/admin/team/invite',""")

    typescript_content.append("""
} as const;

""")
    
    # Write to file
    output_path = "frontend/src/types/survey-api.ts"
    full_content = "\n".join(typescript_content)
    
    try:
        with open(output_path, 'w') as f:
            f.write(full_content)
        print(f"✅ TypeScript types generated successfully: {output_path}")
    except FileNotFoundError:
        # If frontend directory doesn't exist, write to current directory
        fallback_path = "survey-api-types.ts"
        with open(fallback_path, 'w') as f:
            f.write(full_content)
        print(f"✅ TypeScript types generated: {fallback_path}")
        print("💡 Move this file to your frontend project's types directory")
    
    # Also generate a JSON schema for additional tooling
    json_schemas = {}
    
    # Collect all models for schema generation
    all_models = survey_models[:]
    if PHASE2_AVAILABLE:
        all_models.extend(theme_models + analytics_models + admin_models)
    
    for model_class in all_models:
        json_schemas[model_class.__name__] = model_class.model_json_schema()
    
    schema_path = "survey-api-schemas.json"
    with open(schema_path, 'w') as f:
        json.dump(json_schemas, f, indent=2, default=str)
    
    print(f"📋 JSON schemas generated: {schema_path}")
    
    return full_content


if __name__ == "__main__":
    main()