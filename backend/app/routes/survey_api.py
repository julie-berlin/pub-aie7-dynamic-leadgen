"""Survey API endpoints for frontend interaction."""

from fastapi import APIRouter, HTTPException, Request, Header
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import logging

from ..graphs.survey_graph_v2 import survey_graph_v2

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/survey", tags=["survey"])


class StartSessionRequest(BaseModel):
    """Request model for starting a new survey session."""
    form_id: str
    client_id: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None
    utm_term: Optional[str] = None
    landing_page: Optional[str] = None


class StartSessionResponse(BaseModel):
    """Response model for session initialization."""
    session_id: str
    questions: List[Dict[str, Any]]
    headline: str
    motivation: str
    step: int = 1


class SubmitResponsesRequest(BaseModel):
    """Request model for submitting survey responses."""
    session_id: str
    responses: List[Dict[str, Any]] = Field(
        ..., 
        description="List of {question_id, question_text, answer}"
    )


class StepResponse(BaseModel):
    """Response model for next step data."""
    session_id: str
    step: int
    questions: List[Dict[str, Any]]
    headline: str
    motivation: str
    progress: Dict[str, Any]
    completed: bool = False
    completion_message: Optional[str] = None


@router.post("/start", response_model=StartSessionResponse)
async def start_session(
    request: StartSessionRequest,
    referer: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(None),
    x_forwarded_for: Optional[str] = Header(None)
):
    """
    Start a new survey session with tracking parameters.
    
    This endpoint:
    1. Captures UTM parameters and tracking data
    2. Initializes the survey flow
    3. Returns the first set of questions
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
        result = await survey_graph_v2.ainvoke(initial_state)
        
        # Extract frontend response
        frontend_data = result.get('frontend_response', {})
        
        return StartSessionResponse(
            session_id=frontend_data.get('session_id'),
            questions=frontend_data.get('questions', []),
            headline=frontend_data.get('headline', 'Welcome!'),
            motivation=frontend_data.get('motivation', 'Let\'s get started.'),
            step=1
        )
        
    except Exception as e:
        logger.error(f"Failed to start session: {e}")
        raise HTTPException(status_code=500, detail="Failed to initialize survey session")


@router.post("/step", response_model=StepResponse)
async def submit_and_continue(
    request: SubmitResponsesRequest
):
    """
    Submit responses and get the next step.
    
    This endpoint:
    1. Saves the submitted responses immediately
    2. Processes responses through supervisors
    3. Returns next questions or completion message
    """
    try:
        # Prepare state with responses to process
        state_update = {
            'core': {'session_id': request.session_id},
            'pending_responses': request.responses
        }
        
        # Run the graph starting from response processing
        result = await survey_graph_v2.ainvoke(
            state_update,
            {"recursion_limit": 25}
        )
        
        # Check if survey is complete
        core = result.get('core', {})
        completed = core.get('completed', False)
        
        # Get frontend response data
        frontend_data = result.get('frontend_response', {})
        
        response = StepResponse(
            session_id=request.session_id,
            step=frontend_data.get('step', 1),
            questions=frontend_data.get('questions', []),
            headline=frontend_data.get('headline', ''),
            motivation=frontend_data.get('motivation', ''),
            progress=frontend_data.get('progress', {}),
            completed=completed
        )
        
        # Add completion message if done
        if completed:
            lead_intelligence = result.get('lead_intelligence', {})
            lead_status = lead_intelligence.get('lead_status', 'unknown')
            
            if lead_status in ['yes', 'maybe']:
                response.completion_message = result.get('completion_message', 
                    'Thank you for your interest! We\'ll be in touch soon.')
            else:
                response.completion_message = 'Thank you for your time.'
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to process step: {e}")
        raise HTTPException(status_code=500, detail="Failed to process survey step")


@router.post("/abandon/{session_id}")
async def mark_abandoned(session_id: str):
    """
    Mark a session as abandoned.
    
    Called by frontend when user leaves or times out.
    """
    try:
        # Update session as abandoned
        state_update = {
            'core': {
                'session_id': session_id,
                'completed': True
            },
            'engagement': {
                'abandonment_status': 'abandoned',
                'abandonment_risk': 1.0
            }
        }
        
        # Run abandonment flow
        await survey_graph_v2.ainvoke(state_update)
        
        return {"status": "success", "message": "Session marked as abandoned"}
        
    except Exception as e:
        logger.error(f"Failed to mark session as abandoned: {e}")
        raise HTTPException(status_code=500, detail="Failed to update session")


@router.get("/status/{session_id}")
async def get_session_status(session_id: str):
    """
    Get the current status of a survey session.
    
    Useful for resuming sessions or checking completion.
    """
    try:
        # In a real implementation, load from database
        # For now, return mock status
        return {
            "session_id": session_id,
            "status": "active",
            "step": 3,
            "completed": False,
            "lead_status": "maybe",
            "abandonment_risk": 0.4
        }
        
    except Exception as e:
        logger.error(f"Failed to get session status: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve session status")