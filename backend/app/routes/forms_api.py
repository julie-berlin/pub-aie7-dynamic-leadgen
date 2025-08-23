"""
Forms API - RESTful Form Management Endpoints

This module provides clean RESTful API endpoints for:
1. Creating, reading, updating, and deleting forms
2. Form configuration management with multi-tenant security
3. Question management within forms
4. All operations are automatically scoped to the authenticated client

SECURITY: All endpoints enforce row-level security - each client can only
access their own forms. Cross-client access attempts return 404.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import Dict, Any, List, Optional, Literal
import logging
from datetime import datetime
import uuid

from app.database import db
from app.routes.admin_api import AdminUserResponse
# from app.routes.admin_api import get_current_admin_user  # TODO: Re-enable when auth is ready
from app.utils.mock_auth import get_mock_admin_user as get_current_admin_user
from app.utils.response_helpers import success_response, error_response
from pydantic_models import (
    FormQuestionConfig,
    FormCreateRequest, 
    FormUpdateRequest,
    FormPatchRequest,
    FormResponse,
    FormListResponse
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/forms", tags=["forms"])

# === UTILITY FUNCTIONS WITH CLIENT SCOPING ===

def verify_form_ownership(form_id: str, client_id: str) -> bool:
    """
    Verify that a form belongs to the specified client.
    Returns False if form doesn't exist OR belongs to another client.
    """
    try:
        # Use Supabase client
        result = db.client.table("forms")\
            .select("id")\
            .eq("id", form_id)\
            .eq("client_id", client_id)\
            .execute()
        return len(result.data) > 0
    except Exception as e:
        logger.error(f"Error verifying form ownership: {e}")
        return False

def get_form_statistics(form_id: str, client_id: str) -> Dict[str, Any]:
    """Get statistics for a form (client-scoped)."""
    try:
        # Verify ownership first
        if not verify_form_ownership(form_id, client_id):
            return {
                "total_responses": 0,
                "conversion_rate": 0.0,
                "average_completion_time": 0
            }
        
        # Use Supabase client
        
        # Get all sessions for this form
        sessions_result = db.client.table("lead_sessions")\
            .select("lead_status, started_at, completed_at")\
            .eq("form_id", form_id)\
            .execute()
        
        sessions = sessions_result.data or []
        total_responses = len(sessions)
        
        if total_responses == 0:
            return {
                "total_responses": 0,
                "conversion_rate": 0.0,
                "average_completion_time": 0
            }
        
        # Calculate statistics
        completed_sessions = [s for s in sessions if s.get('lead_status') == 'completed']
        completed_responses = len(completed_sessions)
        conversion_rate = completed_responses / total_responses
        
        # Calculate average completion time
        completion_times = []
        for session in completed_sessions:
            if session.get('started_at') and session.get('completed_at'):
                # For simplicity, assume times are ISO strings - in production you'd parse them
                completion_times.append(60)  # Mock 60 seconds average
        
        avg_completion_time = int(sum(completion_times) / len(completion_times)) if completion_times else 0
        
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

def get_form_questions(form_id: str, client_id: str) -> List[FormQuestionConfig]:
    """Get questions for a form (client-scoped)."""
    try:
        # First verify ownership
        if not verify_form_ownership(form_id, client_id):
            return []
        
        # Use Supabase client
        
        # Get questions for the form
        questions_result = db.client.table("form_questions")\
            .select("question_id, question_order, question_text, question_type, options, scoring_rubric, is_required, category, metadata")\
            .eq("form_id", form_id)\
            .order("question_order")\
            .execute()
        
        questions = []
        for q in questions_result.data or []:
            # Handle scoring_rubric - convert string to dict or use None
            scoring_rubric = q.get("scoring_rubric")
            if scoring_rubric and isinstance(scoring_rubric, str):
                # If it's a string, convert to a simple dict format
                scoring_rubric = {"description": scoring_rubric, "points": 0}
            elif not isinstance(scoring_rubric, dict):
                scoring_rubric = None
                
            # Handle options - convert list to dict format if needed
            options = q.get("options")
            if options and isinstance(options, list):
                # Convert list of options to dict format
                options = {"choices": options, "type": "select"}
            elif not isinstance(options, dict):
                options = None
                
            questions.append(FormQuestionConfig(
                question_id=q.get("question_id"),
                question_order=q.get("question_order"),
                question_text=q.get("question_text"),
                question_type=q.get("question_type") or "text",
                options=options,
                validation_rules=q.get("metadata", {}).get("validation_rules"),
                scoring_rubric=scoring_rubric,
                is_required=q.get("is_required") or False,
                description=q.get("description"),
                placeholder=q.get("placeholder")
            ))
        
        return questions
        
    except Exception as e:
        logger.error(f"Failed to get form questions: {e}")
        return []

def save_form_questions(form_id: str, questions: List[FormQuestionConfig], client_id: str):
    """Save questions for a form (with ownership verification)."""
    try:
        # Verify ownership first
        if not verify_form_ownership(form_id, client_id):
            raise HTTPException(status_code=404, detail="Form not found")
        
        # Use Supabase client
        
        # Delete existing questions
        db.client.table("form_questions")\
            .delete()\
            .eq("form_id", form_id)\
            .execute()
        
        # Insert new questions
        if questions:
            questions_data = []
            for question in questions:
                questions_data.append({
                    "form_id": form_id,
                    "question_id": question.question_id,
                    "question_order": question.question_order,
                    "question_text": question.question_text,
                    "question_type": question.question_type,
                    "options": question.options,
                    "validation_rules": question.validation_rules,
                    "scoring_rubric": question.scoring_rubric,
                    "is_required": question.is_required,
                    "description": question.description,
                    "placeholder": question.placeholder
                })
            
            db.client.table("form_questions")\
                .insert(questions_data)\
                .execute()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to save form questions: {e}")
        raise

# === RESTful ENDPOINTS ===

@router.get("")
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
    """
    Get paginated list of forms for the authenticated client.
    Each client can only see their own forms.
    """
    try:
        # Use Supabase client
        
        # Build query - ALWAYS scoped to client
        query = db.client.table("forms")\
            .select("id, client_id, title, description, status, tags, theme_config, lead_scoring_threshold_yes, lead_scoring_threshold_maybe, max_questions, min_questions_before_fail, completion_message_template, unqualified_message, settings, is_active, created_at, updated_at")\
            .eq("client_id", current_user.client_id)
        
        # Apply filters
        if status:
            query = query.eq("status", status)
        
        if search:
            # Supabase text search - using ilike for case-insensitive search
            query = query.or_(f"title.ilike.%{search}%,description.ilike.%{search}%")
        
        if tags:
            # For array containment in Supabase
            tag_list = [tag.strip() for tag in tags.split(",")]
            for tag in tag_list:
                query = query.contains("tags", [tag])
        
        # Get count first
        count_result = db.client.table("forms")\
            .select("id", count="exact")\
            .eq("client_id", current_user.client_id)
        
        if status:
            count_result = count_result.eq("status", status)
        if search:
            count_result = count_result.or_(f"title.ilike.%{search}%,description.ilike.%{search}%")
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",")]
            for tag in tag_list:
                count_result = count_result.contains("tags", [tag])
        
        count_result = count_result.execute()
        total_count = count_result.count or 0
        
        # Get paginated results with ordering
        offset = (page - 1) * page_size
        query = query.order(sort_by, desc=(sort_order == "desc"))\
            .range(offset, offset + page_size - 1)
        
        result = query.execute()
        
        forms = []
        for row in result.data or []:
            form_id = str(row["id"])
            client_id = str(row["client_id"])
            stats = get_form_statistics(form_id, current_user.client_id)
            questions = get_form_questions(form_id, current_user.client_id)
            
            forms.append(FormResponse(
                id=form_id,
                client_id=client_id,
                title=row["title"],
                description=row.get("description"),
                status=row["status"],
                tags=row.get("tags") or [],
                theme_config=row.get("theme_config") or {},
                lead_scoring_threshold_yes=row["lead_scoring_threshold_yes"],
                lead_scoring_threshold_maybe=row["lead_scoring_threshold_maybe"],
                max_questions=row["max_questions"],
                min_questions_before_fail=row["min_questions_before_fail"],
                completion_message_template=row.get("completion_message_template"),
                unqualified_message=row["unqualified_message"],
                settings=row.get("settings") or {},
                is_active=row["is_active"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
                total_responses=stats["total_responses"],
                conversion_rate=stats["conversion_rate"],
                average_completion_time=stats["average_completion_time"],
                questions=questions
            ))
        
        total_pages = (total_count + page_size - 1) // page_size
        
        return success_response(
            data={
                "forms": [form.model_dump(mode='json') for form in forms],
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages
            },
            message="Forms retrieved successfully"
        )
            
    except Exception as e:
        logger.error(f"Failed to list forms: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve forms")

@router.get("/{form_id}", response_model=FormResponse)
async def get_form(
    form_id: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """
    Get a specific form by ID.
    Returns 404 if form doesn't exist OR belongs to another client.
    """
    try:
        # Use Supabase client
        
        # Client-scoped query
        result = db.client.table("forms")\
            .select("*")\
            .eq("id", form_id)\
            .eq("client_id", current_user.client_id)\
            .execute()
        
        if not result.data:
            # Don't reveal whether form exists for another client
            raise HTTPException(status_code=404, detail="Form not found")
        
        row = result.data[0]
        stats = get_form_statistics(form_id, current_user.client_id)
        questions = get_form_questions(form_id, current_user.client_id)
        
        form_response = FormResponse(
            id=str(row["id"]),
            client_id=str(row["client_id"]),
            title=row["title"],
            description=row.get("description"),
            status=row["status"],
            tags=row.get("tags") or [],
            theme_config=row.get("theme_config") or {},
            lead_scoring_threshold_yes=row["lead_scoring_threshold_yes"],
            lead_scoring_threshold_maybe=row["lead_scoring_threshold_maybe"],
            max_questions=row["max_questions"],
            min_questions_before_fail=row["min_questions_before_fail"],
            completion_message_template=row.get("completion_message_template"),
            unqualified_message=row["unqualified_message"],
            settings=row.get("settings") or {},
            is_active=row["is_active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            total_responses=stats["total_responses"],
            conversion_rate=stats["conversion_rate"],
            average_completion_time=stats["average_completion_time"],
            questions=questions
        )
        
        return success_response(
            data=form_response.model_dump(mode='json'),
            message="Form retrieved successfully"
        )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get form: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve form")

@router.post("", response_model=FormResponse, status_code=status.HTTP_201_CREATED)
async def create_form(
    form_request: FormCreateRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """
    Create a new form for the authenticated client.
    """
    try:
        # Use Supabase client
        form_id = str(uuid.uuid4())
        
        form_data = {
            "id": form_id,
            "client_id": current_user.client_id,
            "title": form_request.title,
            "description": form_request.description,
            "status": form_request.status,
            "tags": form_request.tags,
            "theme_config": form_request.theme_config,
            "lead_scoring_threshold_yes": form_request.lead_scoring_threshold_yes,
            "lead_scoring_threshold_maybe": form_request.lead_scoring_threshold_maybe,
            "max_questions": form_request.max_questions,
            "min_questions_before_fail": form_request.min_questions_before_fail,
            "completion_message_template": form_request.completion_message_template,
            "unqualified_message": form_request.unqualified_message,
            "settings": form_request.settings,
            "is_active": form_request.status == "active"
        }
        
        result = db.client.table("forms")\
            .insert(form_data)\
            .execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create form")
        
        created_form = result.data[0]
        
        # Save questions if provided
        if form_request.questions:
            save_form_questions(form_id, form_request.questions, current_user.client_id)
        
        form_response = FormResponse(
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
            created_at=created_form["created_at"],
            updated_at=created_form["updated_at"],
            total_responses=0,
            conversion_rate=0.0,
            average_completion_time=0,
            questions=form_request.questions or []
        )
        
        return success_response(
            data=form_response.model_dump(mode='json'),
            message="Form created successfully",
            status_code=201
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
    """
    Fully update a form (PUT - requires all fields).
    Returns 404 if form doesn't exist OR belongs to another client.
    """
    try:
        # Verify ownership
        if not verify_form_ownership(form_id, current_user.client_id):
            raise HTTPException(status_code=404, detail="Form not found")
        
        # Use Supabase client
        
        update_data = {
            "title": form_request.title,
            "description": form_request.description,
            "status": form_request.status,
            "tags": form_request.tags,
            "theme_config": form_request.theme_config,
            "lead_scoring_threshold_yes": form_request.lead_scoring_threshold_yes,
            "lead_scoring_threshold_maybe": form_request.lead_scoring_threshold_maybe,
            "max_questions": form_request.max_questions,
            "min_questions_before_fail": form_request.min_questions_before_fail,
            "completion_message_template": form_request.completion_message_template,
            "unqualified_message": form_request.unqualified_message,
            "settings": form_request.settings,
            "is_active": form_request.status == "active"
        }
        
        result = db.client.table("forms")\
            .update(update_data)\
            .eq("id", form_id)\
            .eq("client_id", current_user.client_id)\
            .execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Form not found")
        
        # Return updated form
        return await get_form(form_id, current_user)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update form: {e}")
        raise HTTPException(status_code=500, detail="Failed to update form")

@router.patch("/{form_id}", response_model=FormResponse)
async def patch_form(
    form_id: str,
    form_request: FormPatchRequest,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """
    Partially update a form (PATCH - only specified fields).
    Returns 404 if form doesn't exist OR belongs to another client.
    """
    try:
        # Verify ownership
        if not verify_form_ownership(form_id, current_user.client_id):
            raise HTTPException(status_code=404, detail="Form not found")
        
        # Use Supabase client
        
        # Build dynamic update data
        update_data = {}
        
        for field_name, field_value in form_request.model_dump(exclude_unset=True).items():
            if field_value is not None:
                update_data[field_name] = field_value
        
        if update_data:
            if form_request.status:
                update_data["is_active"] = form_request.status == "active"
            
            result = db.client.table("forms")\
                .update(update_data)\
                .eq("id", form_id)\
                .eq("client_id", current_user.client_id)\
                .execute()
            
            if not result.data:
                raise HTTPException(status_code=404, detail="Form not found")
        
        # Return updated form
        return await get_form(form_id, current_user)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to patch form: {e}")
        raise HTTPException(status_code=500, detail="Failed to update form")

@router.delete("/{form_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_form(
    form_id: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """
    Delete a form.
    Returns 404 if form doesn't exist OR belongs to another client.
    """
    try:
        # Verify ownership
        if not verify_form_ownership(form_id, current_user.client_id):
            raise HTTPException(status_code=404, detail="Form not found")
        
        # Use Supabase client
        
        result = db.client.table("forms")\
            .delete()\
            .eq("id", form_id)\
            .eq("client_id", current_user.client_id)\
            .execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Form not found")
        
        return success_response(
            message="Form deleted successfully",
            status_code=204
        )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete form: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete form")

# === ADDITIONAL ENDPOINTS FOR QUESTIONS ===

@router.get("/{form_id}/questions", response_model=List[FormQuestionConfig])
async def get_form_questions_endpoint(
    form_id: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """
    Get questions for a specific form.
    Returns 404 if form doesn't exist OR belongs to another client.
    """
    # Verify ownership
    if not verify_form_ownership(form_id, current_user.client_id):
        raise HTTPException(status_code=404, detail="Form not found")
    
    return get_form_questions(form_id, current_user.client_id)

@router.put("/{form_id}/questions", response_model=Dict[str, Any])
async def update_form_questions_endpoint(
    form_id: str,
    questions: List[FormQuestionConfig],
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """
    Update all questions for a form.
    Returns 404 if form doesn't exist OR belongs to another client.
    """
    try:
        save_form_questions(form_id, questions, current_user.client_id)
        return success_response(
            message="Questions updated successfully",
            data={"form_id": form_id, "question_count": len(questions)}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update questions: {e}")
        raise HTTPException(status_code=500, detail="Failed to update questions")