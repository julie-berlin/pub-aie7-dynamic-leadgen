"""
Admin Forms API - Form CRUD Operations for Admin Interface

This module provides API endpoints for:
1. Creating, reading, updating, and deleting forms
2. Form configuration management
3. Question management within forms
4. Bulk operations on forms
5. Form duplication and templating
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
router = APIRouter(prefix="/api/admin/forms", tags=["admin-forms"])

# === PYDANTIC MODELS FOR FORMS ===

class QuestionConfig(BaseModel):
    """Configuration for a form question."""
    question_id: int
    question_order: int
    question_text: str
    question_type: str = Field(default="text")
    options: Optional[Dict[str, Any]] = None
    validation_rules: Optional[Dict[str, Any]] = None
    scoring_rubric: Optional[Dict[str, Any]] = None
    is_required: bool = Field(default=False)
    description: Optional[str] = None
    placeholder: Optional[str] = None

class FormCreateRequest(BaseModel):
    """Request to create a new form."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Literal["draft", "active", "paused", "archived"] = Field(default="draft")
    tags: Optional[List[str]] = Field(default_factory=list)
    theme_config: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    # Scoring configuration
    lead_scoring_threshold_yes: int = Field(default=80, ge=0, le=100)
    lead_scoring_threshold_maybe: int = Field(default=50, ge=0, le=100)
    
    # Business rules
    max_questions: int = Field(default=8, ge=1, le=20)
    min_questions_before_fail: int = Field(default=4, ge=1, le=10)
    
    # Templates
    completion_message_template: Optional[str] = None
    unqualified_message: str = Field(default="Thank you for your time.")
    
    # Additional settings
    settings: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    # Questions
    questions: Optional[List[QuestionConfig]] = Field(default_factory=list)

    @validator('lead_scoring_threshold_maybe')
    def validate_thresholds(cls, v, values):
        if 'lead_scoring_threshold_yes' in values and v >= values['lead_scoring_threshold_yes']:
            raise ValueError('Maybe threshold must be less than Yes threshold')
        return v

class FormUpdateRequest(BaseModel):
    """Request to update an existing form."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[Literal["draft", "active", "paused", "archived"]] = None
    tags: Optional[List[str]] = None
    theme_config: Optional[Dict[str, Any]] = None
    
    # Scoring configuration
    lead_scoring_threshold_yes: Optional[int] = Field(None, ge=0, le=100)
    lead_scoring_threshold_maybe: Optional[int] = Field(None, ge=0, le=100)
    
    # Business rules
    max_questions: Optional[int] = Field(None, ge=1, le=20)
    min_questions_before_fail: Optional[int] = Field(None, ge=1, le=10)
    
    # Templates
    completion_message_template: Optional[str] = None
    unqualified_message: Optional[str] = None
    
    # Additional settings
    settings: Optional[Dict[str, Any]] = None

class FormResponse(BaseModel):
    """Response model for form data."""
    id: str
    client_id: str
    title: str
    description: Optional[str]
    status: str
    tags: List[str]
    theme_config: Dict[str, Any]
    
    # Scoring configuration
    lead_scoring_threshold_yes: int
    lead_scoring_threshold_maybe: int
    
    # Business rules
    max_questions: int
    min_questions_before_fail: int
    
    # Templates
    completion_message_template: Optional[str]
    unqualified_message: str
    
    # Additional settings
    settings: Dict[str, Any]
    is_active: bool
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    # Statistics (calculated fields)
    total_responses: int = 0
    conversion_rate: float = 0.0
    average_completion_time: int = 0  # seconds
    
    # Questions
    questions: List[QuestionConfig] = []

class FormListResponse(BaseModel):
    """Response model for form list with pagination."""
    forms: List[FormResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int

class BulkOperationRequest(BaseModel):
    """Request for bulk operations on forms."""
    form_ids: List[str] = Field(..., min_items=1)
    operation: Literal["delete", "archive", "activate", "pause"]

class FormDuplicateRequest(BaseModel):
    """Request to duplicate a form."""
    title: str = Field(..., min_length=1, max_length=200)
    copy_questions: bool = Field(default=True)
    copy_theme: bool = Field(default=True)
    copy_settings: bool = Field(default=True)

# === UTILITY FUNCTIONS ===

def get_form_statistics(form_id: str) -> Dict[str, Any]:
    """Get statistics for a form."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Get response statistics
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_responses,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_responses,
                    AVG(CASE WHEN status = 'completed' AND started_at IS NOT NULL 
                         THEN EXTRACT(EPOCH FROM (completed_at - started_at)) END) as avg_completion_time
                FROM lead_sessions 
                WHERE form_id = %s
            """, (form_id,))
            
            result = cursor.fetchone()
            if result:
                total_responses = result[0] or 0
                completed_responses = result[1] or 0
                avg_completion_time = int(result[2] or 0)
                conversion_rate = (completed_responses / total_responses) if total_responses > 0 else 0.0
                
                return {
                    "total_responses": total_responses,
                    "conversion_rate": conversion_rate,
                    "average_completion_time": avg_completion_time
                }
            
    except Exception as e:
        logger.error(f"Failed to get form statistics: {e}")
    
    return {
        "total_responses": 0,
        "conversion_rate": 0.0,
        "average_completion_time": 0
    }

def get_form_questions(form_id: str) -> List[QuestionConfig]:
    """Get questions for a form."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT question_id, question_order, question_text, question_type,
                       options, validation_rules, scoring_rubric, is_required,
                       description, placeholder
                FROM form_questions 
                WHERE form_id = %s 
                ORDER BY question_order
            """, (form_id,))
            
            questions = []
            for row in cursor.fetchall():
                questions.append(QuestionConfig(
                    question_id=row[0],
                    question_order=row[1],
                    question_text=row[2],
                    question_type=row[3] or "text",
                    options=row[4],
                    validation_rules=row[5],
                    scoring_rubric=row[6],
                    is_required=row[7] or False,
                    description=row[8],
                    placeholder=row[9]
                ))
            
            return questions
            
    except Exception as e:
        logger.error(f"Failed to get form questions: {e}")
        return []

def save_form_questions(form_id: str, questions: List[QuestionConfig]):
    """Save questions for a form."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Delete existing questions
            cursor.execute("DELETE FROM form_questions WHERE form_id = %s", (form_id,))
            
            # Insert new questions
            for question in questions:
                cursor.execute("""
                    INSERT INTO form_questions 
                    (form_id, question_id, question_order, question_text, question_type,
                     options, validation_rules, scoring_rubric, is_required, description, placeholder)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    form_id, question.question_id, question.question_order,
                    question.question_text, question.question_type,
                    json.dumps(question.options) if question.options else None,
                    json.dumps(question.validation_rules) if question.validation_rules else None,
                    json.dumps(question.scoring_rubric) if question.scoring_rubric else None,
                    question.is_required, question.description, question.placeholder
                ))
            
            conn.commit()
            
    except Exception as e:
        logger.error(f"Failed to save form questions: {e}")
        raise

# === FORM CRUD ENDPOINTS ===

@router.get("", response_model=FormListResponse)
async def list_forms(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
    sort_by: str = Query("updated_at", description="Sort by field"),
    sort_order: Literal["asc", "desc"] = Query("desc", description="Sort order"),
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get paginated list of forms for the client."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Build WHERE clause
            where_conditions = ["client_id = %s"]
            params = [current_user.client_id]
            
            if status:
                where_conditions.append("status = %s")
                params.append(status)
            
            if search:
                where_conditions.append("(title ILIKE %s OR description ILIKE %s)")
                search_term = f"%{search}%"
                params.extend([search_term, search_term])
            
            if tags:
                tag_list = [tag.strip() for tag in tags.split(",")]
                where_conditions.append("tags && %s")
                params.append(tag_list)
            
            where_clause = " AND ".join(where_conditions)
            
            # Get total count
            count_query = f"SELECT COUNT(*) FROM forms WHERE {where_clause}"
            cursor.execute(count_query, params)
            total_count = cursor.fetchone()[0]
            
            # Get forms
            offset = (page - 1) * page_size
            forms_query = f"""
                SELECT id, client_id, title, description, status, tags, theme_config,
                       lead_scoring_threshold_yes, lead_scoring_threshold_maybe,
                       max_questions, min_questions_before_fail,
                       completion_message_template, unqualified_message,
                       settings, is_active, created_at, updated_at
                FROM forms 
                WHERE {where_clause}
                ORDER BY {sort_by} {sort_order.upper()}
                LIMIT %s OFFSET %s
            """
            params.extend([page_size, offset])
            cursor.execute(forms_query, params)
            
            forms = []
            for row in cursor.fetchall():
                form_id = str(row[0])
                stats = get_form_statistics(form_id)
                questions = get_form_questions(form_id)
                
                forms.append(FormResponse(
                    id=form_id,
                    client_id=str(row[1]),
                    title=row[2],
                    description=row[3],
                    status=row[4],
                    tags=row[5] or [],
                    theme_config=row[6] or {},
                    lead_scoring_threshold_yes=row[7],
                    lead_scoring_threshold_maybe=row[8],
                    max_questions=row[9],
                    min_questions_before_fail=row[10],
                    completion_message_template=row[11],
                    unqualified_message=row[12],
                    settings=row[13] or {},
                    is_active=row[14],
                    created_at=row[15],
                    updated_at=row[16],
                    total_responses=stats["total_responses"],
                    conversion_rate=stats["conversion_rate"],
                    average_completion_time=stats["average_completion_time"],
                    questions=questions
                ))
            
            total_pages = (total_count + page_size - 1) // page_size
            
            return FormListResponse(
                forms=forms,
                total_count=total_count,
                page=page,
                page_size=page_size,
                total_pages=total_pages
            )
            
    except Exception as e:
        logger.error(f"Failed to list forms: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve forms")

@router.get("/{form_id}", response_model=FormResponse)
async def get_form(
    form_id: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get a specific form by ID."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, client_id, title, description, status, tags, theme_config,
                       lead_scoring_threshold_yes, lead_scoring_threshold_maybe,
                       max_questions, min_questions_before_fail,
                       completion_message_template, unqualified_message,
                       settings, is_active, created_at, updated_at
                FROM forms 
                WHERE id = %s AND client_id = %s
            """, (form_id, current_user.client_id))
            
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Form not found")
            
            stats = get_form_statistics(form_id)
            questions = get_form_questions(form_id)
            
            return FormResponse(
                id=str(row[0]),
                client_id=str(row[1]),
                title=row[2],
                description=row[3],
                status=row[4],
                tags=row[5] or [],
                theme_config=row[6] or {},
                lead_scoring_threshold_yes=row[7],
                lead_scoring_threshold_maybe=row[8],
                max_questions=row[9],
                min_questions_before_fail=row[10],
                completion_message_template=row[11],
                unqualified_message=row[12],
                settings=row[13] or {},
                is_active=row[14],
                created_at=row[15],
                updated_at=row[16],
                total_responses=stats["total_responses"],
                conversion_rate=stats["conversion_rate"],
                average_completion_time=stats["average_completion_time"],
                questions=questions
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get form: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve form")

@router.post("", response_model=FormResponse)
async def create_form(
    form_request: FormCreateRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Create a new form."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            form_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO forms 
                (id, client_id, title, description, status, tags, theme_config,
                 lead_scoring_threshold_yes, lead_scoring_threshold_maybe,
                 max_questions, min_questions_before_fail,
                 completion_message_template, unqualified_message, settings, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING created_at, updated_at
            """, (
                form_id, current_user.client_id, form_request.title,
                form_request.description, form_request.status, form_request.tags,
                json.dumps(form_request.theme_config),
                form_request.lead_scoring_threshold_yes,
                form_request.lead_scoring_threshold_maybe,
                form_request.max_questions, form_request.min_questions_before_fail,
                form_request.completion_message_template,
                form_request.unqualified_message,
                json.dumps(form_request.settings),
                form_request.status == "active"
            ))
            
            created_at, updated_at = cursor.fetchone()
            
            # Save questions if provided
            if form_request.questions:
                save_form_questions(form_id, form_request.questions)
            
            conn.commit()
            
            return FormResponse(
                id=form_id,
                client_id=current_user.client_id,
                title=form_request.title,
                description=form_request.description,
                status=form_request.status,
                tags=form_request.tags,
                theme_config=form_request.theme_config,
                lead_scoring_threshold_yes=form_request.lead_scoring_threshold_yes,
                lead_scoring_threshold_maybe=form_request.lead_scoring_threshold_maybe,
                max_questions=form_request.max_questions,
                min_questions_before_fail=form_request.min_questions_before_fail,
                completion_message_template=form_request.completion_message_template,
                unqualified_message=form_request.unqualified_message,
                settings=form_request.settings,
                is_active=form_request.status == "active",
                created_at=created_at,
                updated_at=updated_at,
                total_responses=0,
                conversion_rate=0.0,
                average_completion_time=0,
                questions=form_request.questions or []
            )
            
    except Exception as e:
        logger.error(f"Failed to create form: {e}")
        raise HTTPException(status_code=500, detail="Failed to create form")

@router.put("/{form_id}", response_model=FormResponse)
async def update_form(
    form_id: str,
    form_request: FormUpdateRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Update an existing form."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Check if form exists and belongs to client
            cursor.execute(
                "SELECT id FROM forms WHERE id = %s AND client_id = %s",
                (form_id, current_user.client_id)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Form not found")
            
            # Build dynamic update query
            update_fields = []
            update_values = []
            
            for field_name, field_value in form_request.dict(exclude_unset=True).items():
                if field_value is not None:
                    if field_name in ['theme_config', 'settings']:
                        update_fields.append(f"{field_name} = %s")
                        update_values.append(json.dumps(field_value))
                    else:
                        update_fields.append(f"{field_name} = %s")
                        update_values.append(field_value)
            
            if update_fields:
                update_fields.append("updated_at = NOW()")
                if form_request.status:
                    update_fields.append("is_active = %s")
                    update_values.append(form_request.status == "active")
                
                update_values.append(form_id)
                
                query = f"""
                    UPDATE forms 
                    SET {', '.join(update_fields)}
                    WHERE id = %s
                """
                cursor.execute(query, update_values)
                conn.commit()
            
            # Return updated form
            return await get_form(form_id, current_user)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update form: {e}")
        raise HTTPException(status_code=500, detail="Failed to update form")

@router.delete("/{form_id}")
async def delete_form(
    form_id: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Delete a form."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Check if form exists and belongs to client
            cursor.execute(
                "SELECT id FROM forms WHERE id = %s AND client_id = %s",
                (form_id, current_user.client_id)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Form not found")
            
            # Delete form (cascade will handle related data)
            cursor.execute("DELETE FROM forms WHERE id = %s", (form_id,))
            conn.commit()
            
            return create_success_response(
                message="Form deleted successfully",
                data={"form_id": form_id}
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete form: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete form")

@router.post("/{form_id}/duplicate", response_model=FormResponse)
async def duplicate_form(
    form_id: str,
    duplicate_request: FormDuplicateRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Duplicate an existing form."""
    try:
        # Get original form
        original_form = await get_form(form_id, current_user)
        
        # Create new form based on original
        new_form_data = FormCreateRequest(
            title=duplicate_request.title,
            description=original_form.description,
            status="draft",  # Always create as draft
            tags=original_form.tags,
            theme_config=original_form.theme_config if duplicate_request.copy_theme else {},
            lead_scoring_threshold_yes=original_form.lead_scoring_threshold_yes,
            lead_scoring_threshold_maybe=original_form.lead_scoring_threshold_maybe,
            max_questions=original_form.max_questions,
            min_questions_before_fail=original_form.min_questions_before_fail,
            completion_message_template=original_form.completion_message_template,
            unqualified_message=original_form.unqualified_message,
            settings=original_form.settings if duplicate_request.copy_settings else {},
            questions=original_form.questions if duplicate_request.copy_questions else []
        )
        
        return await create_form(new_form_data, current_user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to duplicate form: {e}")
        raise HTTPException(status_code=500, detail="Failed to duplicate form")

@router.post("/bulk-operation")
async def bulk_operation(
    operation_request: BulkOperationRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Perform bulk operations on multiple forms."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Verify all forms belong to current client
            placeholders = ','.join(['%s'] * len(operation_request.form_ids))
            cursor.execute(f"""
                SELECT id FROM forms 
                WHERE id IN ({placeholders}) AND client_id = %s
            """, operation_request.form_ids + [current_user.client_id])
            
            found_forms = [str(row[0]) for row in cursor.fetchall()]
            if len(found_forms) != len(operation_request.form_ids):
                missing_forms = set(operation_request.form_ids) - set(found_forms)
                raise HTTPException(
                    status_code=404, 
                    detail=f"Forms not found: {list(missing_forms)}"
                )
            
            # Perform operation
            if operation_request.operation == "delete":
                cursor.execute(f"""
                    DELETE FROM forms WHERE id IN ({placeholders})
                """, operation_request.form_ids)
            
            elif operation_request.operation in ["archive", "activate", "pause"]:
                status_map = {
                    "archive": "archived",
                    "activate": "active", 
                    "pause": "paused"
                }
                new_status = status_map[operation_request.operation]
                is_active = new_status == "active"
                
                cursor.execute(f"""
                    UPDATE forms 
                    SET status = %s, is_active = %s, updated_at = NOW()
                    WHERE id IN ({placeholders})
                """, [new_status, is_active] + operation_request.form_ids)
            
            conn.commit()
            
            return create_success_response(
                message=f"Bulk {operation_request.operation} completed successfully",
                data={
                    "operation": operation_request.operation,
                    "affected_forms": len(operation_request.form_ids)
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to perform bulk operation: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform bulk operation")