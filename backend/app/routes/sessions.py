"""
Session Management Routes

API endpoints for form session lifecycle management.
Uses SurveyFlowManager with LangGraph implementation.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import sys
import os
from datetime import datetime
import uuid

# Add parent directories to path for imports
current_dir = os.path.dirname(__file__)
api_dir = os.path.dirname(current_dir)
app_dir = os.path.dirname(api_dir)
root_dir = os.path.dirname(app_dir)

sys.path.extend([api_dir, app_dir, root_dir])

from backend.py_models import (
    SessionStartRequest, SessionStepRequest, SessionCompleteRequest,
    SessionStepResponse, SessionStatusResponse, SessionCompletionResponse,
    QuestionResponse, ErrorResponse
)

# Import our LangGraph-based flow manager
from survey_flow_manager import SurveyFlowManager

router = APIRouter()

# Global flow manager instance
flow_manager = SurveyFlowManager()

@router.post("/sessions/start", response_model=SessionStepResponse)
async def start_session(request: SessionStartRequest):
    """
    Start a new lead generation session

    Creates a new session, initializes state, and returns the first form step.
    """
    try:
        # Initialize session with LangGraph flow manager
        session_result = await flow_manager.start_session(
            form_id=request.form_id,
            client_id=request.client_id,
            metadata=request.metadata
        )

        # Convert questions to response format
        questions = [
            QuestionResponse(
                id=q['id'],
                question=q['question'],
                phrased_question=q.get('phrased_question', q['question']),
                data_type=q.get('data_type', 'text'),
                is_required=q.get('is_required', False)
            )
            for q in session_result['questions']
        ]

        return SessionStepResponse(
            session_id=session_result['session_id'],
            step=session_result['step'],
            headline=session_result['headline'],
            motivation=session_result['motivation'],
            questions=questions,
            progress={
                'current_step': session_result['step'],
                'total_responses': 0,
                'completion_percentage': 0
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start session: {str(e)}"
        )

@router.post("/sessions/step", response_model=SessionStepResponse)
async def process_step(request: SessionStepRequest):
    """
    Process a form step with user responses

    Processes user responses, advances the form flow, and returns the next step.
    """
    try:
        # Advance session step with LangGraph flow manager
        step_result = await flow_manager.advance_session_step(
            session_id=request.session_id,
            responses=request.responses
        )

        # Check if session is complete
        if step_result.get('completed', False):
            # Return completion redirect
            raise HTTPException(
                status_code=302,
                detail="Session completed",
                headers={"Location": f"/sessions/{request.session_id}/complete"}
            )

        # Convert questions to response format
        questions = [
            QuestionResponse(
                id=q['id'],
                question=q['question'],
                phrased_question=q.get('phrased_question', q['question']),
                data_type=q.get('data_type', 'text'),
                is_required=q.get('is_required', False)
            )
            for q in step_result['questions']
        ]

        return SessionStepResponse(
            session_id=step_result['session_id'],
            step=step_result['step'],
            headline=step_result['headline'],
            motivation=step_result['motivation'],
            questions=questions,
            progress={
                'current_step': step_result['step'],
                'total_responses': step_result.get('total_responses', 0),
                'completion_percentage': min(100, step_result.get('total_responses', 0) * 20)
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process step: {str(e)}"
        )

@router.get("/sessions/{session_id}", response_model=SessionStatusResponse)
async def get_session_status(session_id: str):
    """
    Get current session status and state

    Returns the current state of a session without advancing the flow.
    """
    try:
        status = await flow_manager.get_session_status(session_id)

        if not status:
            raise HTTPException(
                status_code=404,
                detail=f"Session {session_id} not found"
            )

        return SessionStatusResponse(
            session_id=status['session_id'],
            form_id=status['form_id'],
            step=status['step'],
            completed=status['completed'],
            lead_status=status['lead_status'],
            score=status['score'],
            responses_count=status['responses_count'],
            started_at=datetime.fromisoformat(status['started_at']),
            last_updated=datetime.fromisoformat(status['last_updated'])
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get session status: {str(e)}"
        )

@router.post("/sessions/{session_id}/complete", response_model=SessionCompletionResponse)
async def complete_session(session_id: str, request: SessionCompleteRequest = None):
    """
    Complete a session and get final results

    Finalizes the session, generates completion message, and returns final status.
    """
    try:
        # Finalize session with LangGraph flow manager
        completion_result = await flow_manager.finalize_session(
            session_id=session_id,
            final_responses=request.final_responses if request else []
        )

        return SessionCompletionResponse(
            session_id=completion_result['session_id'],
            lead_status=completion_result['lead_status'],
            final_score=completion_result['final_score'],
            completion_message=completion_result['completion_message'],
            next_steps=completion_result.get('next_steps', []),
            completed_at=datetime.fromisoformat(completion_result['completed_at'])
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to complete session: {str(e)}"
        )

@router.delete("/sessions/{session_id}")
async def abandon_session(session_id: str):
    """
    Mark a session as abandoned

    Records session abandonment for analytics and cleanup.
    """
    try:
        result = await flow_manager.mark_session_abandoned(session_id)

        return {
            "message": f"Session {session_id} marked as abandoned",
            "abandoned_at": result.get('abandoned_at'),
            "step_abandoned": result.get('step_abandoned'),
            "responses_collected": result.get('responses_collected', 0)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to abandon session: {str(e)}"
        )
