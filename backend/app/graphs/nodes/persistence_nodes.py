"""
Database Persistence Nodes for LangGraph Survey Flow

Handles database operations for responses, sessions, and completion data.
"""

from __future__ import annotations
from typing import Dict, Any
from datetime import datetime
import json

from ...state import SurveyState
from ..toolbelts.persistence_toolbelt import persistence_toolbelt


def save_responses_node(state: SurveyState) -> Dict[str, Any]:
    """
    Save user responses to database.
    
    Args:
        state: Current SurveyState with responses to save
        
    Returns:
        Dict with success status (doesn't modify state)
    """
    try:
        responses = state.get('responses', [])
        if not responses:
            return {}  # No responses to save
            
        # Get only the latest responses that need to be saved
        # In a real implementation, you'd track which responses are already saved
        session_id = state.get('session_id', '')
        
        # Save responses using our tool
        responses_json = json.dumps(responses)
        result = persistence_toolbelt.save_responses.invoke({
            "session_id": session_id,
            "responses_data": responses_json
        })
        
        print(f"Saved responses: {result}")
        return {}  # Don't modify state, just persist to DB
        
    except Exception as e:
        print(f"Error saving responses: {e}")
        return {}


def update_session_node(state: SurveyState) -> Dict[str, Any]:
    """
    Update session data in database.
    
    Args:
        state: Current SurveyState
        
    Returns:
        Dict with success status (doesn't modify state)
    """
    try:
        session_id = state.get('session_id', '')
        
        # Prepare session update data
        update_data = {
            'step_count': state.get('step', 0),
            'final_score': state.get('score', 0),
            'lead_status': state.get('lead_status', 'unknown'),
            'completed': state.get('completed', False),
            'updated_at': state.get('last_updated', datetime.now().isoformat())
        }
        
        # Update session using our tool
        updates_json = json.dumps(update_data)
        result = persistence_toolbelt.update_session.invoke({
            "session_id": session_id,
            "updates_data": updates_json
        })
        
        print(f"Updated session: {result}")
        return {}  # Don't modify state, just persist to DB
        
    except Exception as e:
        print(f"Error updating session: {e}")
        return {}


def save_completion_node(state: SurveyState) -> Dict[str, Any]:
    """
    Finalize session with completion data in database.
    
    Args:
        state: Current SurveyState with final data
        
    Returns:
        Dict with success status (doesn't modify state)
    """
    try:
        session_id = state.get('session_id', '')
        
        # Prepare final completion data
        final_data = {
            'final_score': state.get('score', 0),
            'lead_status': state.get('lead_status', 'unknown'),
            'completed_at': datetime.now().isoformat(),
            'step_count': state.get('step', 0),
            'response_count': len(state.get('responses', []))
        }
        
        # Finalize session using our tool
        final_json = json.dumps(final_data)
        result = persistence_toolbelt.finalize_session.invoke({
            "session_id": session_id,
            "final_data": final_json
        })
        
        print(f"Finalized session: {result}")
        return {}  # Don't modify state, just persist to DB
        
    except Exception as e:
        print(f"Error finalizing session: {e}")
        return {}