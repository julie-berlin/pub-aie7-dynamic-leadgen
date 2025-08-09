#!/usr/bin/env python3
"""
Generate TypeScript types from Pydantic models.

This script creates TypeScript type definitions that match our Pydantic models,
ensuring type safety between backend and frontend.
"""

import json
from typing import get_type_hints, get_origin, get_args
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


def pydantic_to_typescript_type(pydantic_type, optional=False) -> str:
    """Convert Python/Pydantic types to TypeScript types."""
    
    # Handle Optional types
    origin = get_origin(pydantic_type)
    if origin is not None:
        args = get_args(pydantic_type)
        
        # Handle Union types (Optional is Union[T, None])
        if origin is type(Union):
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
    
    # Get model fields and their types
    fields = model_class.__fields__
    
    lines = [f"export interface {interface_name} {{"]
    
    for field_name, field_info in fields.items():
        # Determine if field is optional
        is_optional = not field_info.is_required()
        
        # Get TypeScript type
        ts_type = pydantic_to_typescript_type(field_info.type_, optional=is_optional)
        
        # Add description as comment if available
        description = field_info.description
        if description:
            lines.append(f"  /** {description} */")
        
        # Add field
        optional_marker = "?" if is_optional else ""
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
    
    # Add header
    typescript_content.append("""/**
 * Auto-generated TypeScript types for Survey API
 * Generated from Pydantic models
 * 
 * DO NOT EDIT MANUALLY - This file is auto-generated
 * Run `python3 generate_typescript_types.py` to update
 */

""")
    
    # Generate enums
    enums = [LeadStatus, AbandonmentStatus, CompletionType, FlowPhase, FlowStrategy]
    
    typescript_content.append("// === ENUMS ===\n")
    
    for enum_class in enums:
        typescript_content.append(generate_enum_from_model(enum_class))
        typescript_content.append("")
    
    # Generate interfaces
    api_models = [
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
    
    typescript_content.append("// === API TYPES ===\n")
    
    for model_class in api_models:
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
}

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
    
    for model_class in api_models:
        json_schemas[model_class.__name__] = model_class.schema()
    
    schema_path = "survey-api-schemas.json"
    with open(schema_path, 'w') as f:
        json.dump(json_schemas, f, indent=2, default=str)
    
    print(f"📋 JSON schemas generated: {schema_path}")
    
    return full_content


if __name__ == "__main__":
    # Add Union import fix
    from typing import Union
    main()