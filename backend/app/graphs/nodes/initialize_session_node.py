"""
Initialize Session Node for LangGraph Survey Flow

Handles session initialization with questions and client info loading.
"""

from __future__ import annotations
from typing import Dict, Any
from datetime import datetime
import json

from ...state import SurveyState
from ..toolbelts.initialize_toolbelt import initialize_toolbelt


def initialize_session_node(state: SurveyState) -> Dict[str, Any]:
    """
    Initialize a new survey session with questions and client info.
    
    Args:
        state: Initial SurveyState (may have minimal data)
        
    Returns:
        Dict with all_questions and other initialization updates
    """
    try:
        form_id = state.get('form_id', 'dogwalk_demo_form')
        
        # Load questions using our tool belt
        questions_json = initialize_toolbelt.load_questions.invoke({"form_id": form_id})
        all_questions = json.loads(questions_json) if questions_json else []
        
        # Initialize step counter and empty collections
        updates = {
            'all_questions': all_questions,
            'asked_questions': [],
            'current_step_questions': [],
            'phrased_questions': [],
            'responses': [],
            'step': 0,
            'score': 0,
            'lead_status': 'unknown',
            'min_questions_met': False,
            'failed_required': False,
            'step_headline': '',
            'step_motivation': '',
            'last_updated': datetime.now().isoformat()
        }
        
        return updates
        
    except Exception as e:
        print(f"Error initializing session: {e}")
        return {
            'all_questions': [],
            'step': 0,
            'last_updated': datetime.now().isoformat()
        }