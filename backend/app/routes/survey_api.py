"""Survey API endpoints with consistent response format and fastapi-sessions."""

from fastapi import APIRouter, HTTPException, Request, Header, Response, Cookie
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import os

# Import consolidated Pydantic models  
from pydantic_models import (
    StartSessionRequest,
    StartSessionResponse,
    SubmitResponsesRequest,
    StepResponse,
    CompletionResponse,
    SessionStatusResponse,
    AbandonSessionRequest,
    ErrorResponse,
    QuestionData,
    SurveyGraphState,
    create_initial_state,
    LeadStatus,
    CompletionType
)
from app.graphs.simplified_survey_graph import (
    simplified_survey_graph as intelligent_survey_graph,
    start_simplified_survey as start_intelligent_survey,
    process_survey_step as process_survey_responses,
    check_abandonment as check_survey_abandonment
)
from app.utils.response_helpers import (
    success_response,
    error_response,
    not_found_response,
    server_error_response
)
from app.session_manager import (
    create_survey_session,
    get_session_from_request,
    update_survey_session,
    delete_survey_session,
    set_session_cookie
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/survey", tags=["survey"])


@router.post("/start")
async def start_session(
    http_request: Request,
    request: StartSessionRequest,
    referer: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(None),
    x_forwarded_for: Optional[str] = Header(None)
):
    """
    Start a new survey session with secure session management.
    
    This endpoint:
    1. Captures UTM parameters and tracking data
    2. Initializes the survey flow
    3. Returns the first set of questions
    4. Sets secure session cookie via fastapi-sessions (OWASP compliant)
    
    Security: Session managed by fastapi-sessions with Redis backend.
    """
    try:
        # Prepare initial state with tracking data
        initial_state = {
            'metadata': {
                'form_id': request.form_id,
                'client_id': request.client_id,
                'utm_source': request.utm_source,
                'utm_medium': request.utm_medium,
                'utm_campaign': request.utm_campaign,
                'utm_content': request.utm_content,
                'utm_term': request.utm_term,
                'landing_page': request.landing_page,
                'referrer': referer,
                'user_agent': user_agent,
                'ip_address': x_forwarded_for or 'unknown'
            }
        }
        
        # Run the graph to initialize and get first questions
        result = await intelligent_survey_graph.ainvoke(initial_state)
        
        logger.debug(f"Graph result type: {type(result)}")
        logger.debug(f"Graph result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        # Extract frontend response
        frontend_data = result.get('frontend_response', {})
        logger.debug(f"Frontend data: {frontend_data}")
        session_id = frontend_data.get('session_id')
        logger.debug(f"Extracted session_id: {session_id}")
        
        # Create session data for fastapi-sessions
        if session_id:
            session_data = {
                "session_id": session_id,
                "form_id": request.form_id,
                "client_id": request.client_id,
                "created_at": datetime.now().isoformat(),
                "utm_data": {
                    "utm_source": request.utm_source,
                    "utm_medium": request.utm_medium,
                    "utm_campaign": request.utm_campaign,
                    "utm_content": request.utm_content,
                    "utm_term": request.utm_term,
                    "landing_page": request.landing_page
                }
            }
            
            # Create session using Starlette session manager
            session_uuid = await create_survey_session(http_request, session_data)
            logger.info(f"Created secure session: {session_uuid}")
            
        # Extract form details from graph response
        form_details = result.get('form_details', {})
        
        # If not at top level, check inside frontend_response
        if not form_details:
            form_details = frontend_data.get('form_details', {})
            
        logger.debug(f"Extracted form_details: {form_details}")
        
        # Load business name from client_id (server-side only)
        business_name = None
        client_id = form_details.get('client_id')
        logger.info(f"🏢 Loading business name for client_id: {client_id}")
        if client_id:
            try:
                from ..database import db
                client_data = db.client.table('clients').select('business_name').eq('id', client_id).execute()
                logger.info(f"🏢 Client query result: {client_data.data}")
                if client_data.data and len(client_data.data) > 0:
                    business_name = client_data.data[0].get('business_name')
                    logger.info(f"🏢 Successfully loaded business name: {business_name}")
                else:
                    logger.warning(f"🏢 No client data found for client_id: {client_id}")
            except Exception as e:
                logger.error(f"🏢 Failed to load business name for client {client_id}: {e}")
        else:
            logger.warning(f"🏢 No client_id found in form_details: {form_details}")
        
        # Create response with consistent format
        json_response = success_response(
            data={
                "form": {
                    "id": form_details.get('id', request.form_id),
                    "title": form_details.get('title', 'Survey'),
                    "description": form_details.get('description'),
                    "businessName": business_name,
                    "theme": frontend_data.get('theme')
                },
                "step": {
                    "stepNumber": frontend_data.get('step', 1),
                    "totalSteps": frontend_data.get('total_steps', 1),
                    "questions": frontend_data.get('questions', []),
                    "headline": frontend_data.get('headline', 'Welcome!'),
                    "subheading": frontend_data.get('motivation'),
                    "isComplete": False
                }
            },
            message="Session started successfully"
        )
        
        # Session cookie is handled automatically by Starlette SessionMiddleware
            
        return json_response
        
    except Exception as e:
        logger.error(f"Failed to start session: {e}")
        return server_error_response("Failed to initialize survey session")


@router.post("/step")
async def submit_and_continue(
    request: SubmitResponsesRequest,
    http_request: Request
):
    """
    Submit responses and get the next step.
    
    This endpoint:
    1. Reads session from fastapi-sessions
    2. Saves the submitted responses immediately
    3. Processes responses through supervisors
    4. Returns next questions or completion message
    
    Security: Session managed by fastapi-sessions.
    """
    try:
        # Get session data using Redis session manager
        session_data = await get_session_from_request(http_request)
        if not session_data:
            return error_response(
                "No survey session found. Please start a new survey.",
                status_code=401
            )
            
        session_id = session_data.get('session_id')
        logger.info(f"Processing step for session: {session_id}")
        
        # Load existing session data from database to get form_id and other state
        from ..database import db
        db_session_data = db.get_lead_session(session_id)
        if not db_session_data:
            return not_found_response("Session", session_id)
        
        # Prepare state with full session context plus new responses
        state_update = {
            'core': {
                'session_id': session_id,
                'form_id': db_session_data.get('form_id'),  # Critical: include form_id
                'step': db_session_data.get('step', 0),
                'client_id': db_session_data.get('client_id')
            },
            'pending_responses': request.responses
        }
        
        # Run the graph starting from response processing
        result = await intelligent_survey_graph.ainvoke(
            state_update,
            {"recursion_limit": 25}
        )
        
        # Check if survey is complete
        core = result.get('core', {})
        completed = core.get('completed', False)
        
        # Get frontend response data
        frontend_data = result.get('frontend_response', {})
        
        # Prepare response data
        response_data = {
            "isComplete": completed
        }
        
        if completed:
            # Form is complete - return completion data
            response_data["completionData"] = {
                "leadStatus": result.get('lead_status', 'unknown'),
                "score": result.get('lead_score', 0),
                "message": result.get('completion_message', 'Thank you for your time and interest.'),
                "nextSteps": result.get('next_steps', [])
            }
            message = "Form completed successfully"
        else:
            # Continue with next step
            response_data["nextStep"] = {
                "stepNumber": frontend_data.get('step', 1),
                "totalSteps": frontend_data.get('total_steps', 1),
                "questions": frontend_data.get('questions', []),
                "headline": frontend_data.get('headline', ''),
                "subheading": frontend_data.get('motivation'),
                "isComplete": False
            }
            message = "Responses submitted successfully"
        
        return success_response(
            data=response_data,
            message=message
        )
        
    except Exception as e:
        logger.error(f"Failed to process step: {e}")
        return server_error_response("Failed to process survey step")


@router.post("/abandon")
async def mark_abandoned(request: Request):
    """
    Mark a session as abandoned.
    
    Called by frontend when user leaves or times out.
    Security: Session managed by fastapi-sessions.
    """
    try:
        # Get session data using Redis session manager
        session_data = await get_session_from_request(request)
        if not session_data:
            return error_response(
                "No survey session found. Session may have already expired.",
                status_code=401
            )
            
        session_id = session_data.get('session_id')
        logger.info(f"Marking session as abandoned: {session_id}")
        
        # Load existing session data from database to get form_id and other state
        from ..database import db
        db_session_data = db.get_lead_session(session_id)
        if not db_session_data:
            return not_found_response("Session", session_id)
        
        # Update session as abandoned with full context
        state_update = {
            'core': {
                'session_id': session_id,
                'form_id': db_session_data.get('form_id'),  # Critical: include form_id
                'client_id': db_session_data.get('client_id'),
                'completed': True
            },
            'engagement': {
                'abandonment_status': 'abandoned',
                'abandonment_risk': 1.0
            }
        }
        
        # Run abandonment flow
        await intelligent_survey_graph.ainvoke(state_update)
        
        return success_response(
            message="Abandonment recorded"
        )
        
    except Exception as e:
        logger.error(f"Failed to mark session as abandoned: {e}")
        return server_error_response("Failed to update session")


@router.get("/status")
async def get_session_status(request: Request):
    """
    Get the current status of a survey session.
    
    Useful for resuming sessions or checking completion.
    Security: Session managed by fastapi-sessions.
    """
    try:
        # Get session data using Redis session manager
        session_data = await get_session_from_request(request)
        if not session_data:
            return error_response(
                "No survey session found. Please start a new survey.",
                status_code=401
            )
            
        session_id = session_data.get('session_id')
        
        # Load session from database
        from ..database import db
        
        db_session_data = db.get_lead_session(session_id)
        if not db_session_data:
            return not_found_response("Session", session_id)
        
        # Get additional data
        responses = db.get_session_responses(session_id)
        
        return success_response(
            data={
                "status": "completed" if db_session_data.get('completed', False) else "active",
                "step": db_session_data.get('step', 0),
                "completed": db_session_data.get('completed', False),
                "leadStatus": db_session_data.get('lead_status', 'unknown'),
                "abandonmentRisk": float(db_session_data.get('abandonment_risk', 0.3)),
                "abandonmentStatus": db_session_data.get('abandonment_status', 'active'),
                "formId": db_session_data.get('form_id', ''),
                "startedAt": db_session_data.get('started_at'),
                "completedAt": db_session_data.get('completed_at'),
                "responseCount": len(responses),
                "completionType": db_session_data.get('completion_type')
            },
            message="Session status retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to get session status: {e}")
        return server_error_response("Failed to retrieve session status")


@router.get("/db-health")
async def database_health_check():
    """
    Database-specific health check for the survey system.
    
    Returns database connectivity and survey-specific table status.
    """
    try:
        from ..database import db
        import json
        
        # Test basic database connection
        db_connected = db.test_connection()
        
        # Test survey-specific functionality
        forms_accessible = False
        sample_form = None
        try:
            # Try to load a sample form
            sample_form = db.get_form("dogwalk_demo_form") 
            forms_accessible = sample_form is not None
        except Exception:
            pass
        
        status = "healthy" if (db_connected and forms_accessible) else "degraded"
        
        return success_response(
            data={
                "database_connected": db_connected,
                "forms_table_accessible": forms_accessible,
                "sample_form_loaded": sample_form is not None,
                "timestamp": datetime.now().isoformat(),
                "status": status
            },
            message=f"Database is {status}"
        )
        
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return error_response(
            "Database health check failed",
            status_code=503,
            data={
                "database_connected": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "unhealthy"
            }
        )


@router.get("/forms/{form_id}/validate")
async def validate_form(form_id: str):
    """
    Validate that a form exists and is properly configured.
    
    Useful for frontend validation before starting a survey.
    """
    try:
        from ..database import db
        from ..tools import load_questions, load_client_info
        import json
        
        # Check if form exists
        form = db.get_form(form_id)
        if not form:
            return not_found_response("Form", form_id)
        
        # Check if questions exist
        questions_json = load_questions.invoke({'form_id': form_id})
        questions = json.loads(questions_json) if questions_json else []
        
        # Check if client info exists
        client_json = load_client_info.invoke({'form_id': form_id})
        client_info = json.loads(client_json) if client_json else {}
        
        return success_response(
            data={
                "form": {
                    "id": form_id,
                    "title": form.get('title', ''),
                    "description": form.get('description', ''),
                    "active": True
                }
            },
            message="Form is available"
        )
        
    except Exception as e:
        logger.error(f"Failed to validate form {form_id}: {e}")
        return server_error_response("Failed to validate form")