"""
Supervisor Nodes for LangGraph Survey Flow

Nodes that supervise and coordinate other node functions with additional data loading.
These can be extended with LLM supervision logic in the future.
"""

from __future__ import annotations
from typing import Dict, Any
import json

from ...state import SurveyState
from ..toolbelts.supervisor_toolbelt import supervisor_toolbelt
from .question_selection_node import question_selection_node
from .question_phrasing_node import question_phrasing_node
from .engagement_node import engagement_node
from .lead_scoring_node import lead_scoring_node


def select_questions_node(state: SurveyState) -> Dict[str, Any]:
    """Supervisor node for question selection."""
    return question_selection_node(state)


def phrase_questions_node(state: SurveyState) -> Dict[str, Any]:
    """
    Supervisor node for question phrasing with client info.
    
    Args:
        state: Current SurveyState
        
    Returns:
        Dict with phrased_questions update
    """
    try:
        form_id = state.get('form_id', 'dogwalk_demo_form')
        
        # Load client info using our tool belt
        client_json = supervisor_toolbelt.load_client_info.invoke({"form_id": form_id})
        client_info = json.loads(client_json) if client_json else {}
        
        return question_phrasing_node(state, client_info)
        
    except Exception as e:
        print(f"Error in phrase questions node: {e}")
        # Fallback to original questions
        original_questions = [q.get('question', '') for q in state.get('current_step_questions', [])]
        return {"phrased_questions": original_questions}


def create_engagement_node(state: SurveyState) -> Dict[str, Any]:
    """
    Supervisor node for engagement with client info.
    
    Args:
        state: Current SurveyState
        
    Returns:
        Dict with step_headline and step_motivation updates
    """
    try:
        form_id = state.get('form_id', 'dogwalk_demo_form')
        
        # Load client info using our tool belt
        client_json = supervisor_toolbelt.load_client_info.invoke({"form_id": form_id})
        client_info = json.loads(client_json) if client_json else {}
        
        return engagement_node(state, client_info)
        
    except Exception as e:
        print(f"Error in engagement node: {e}")
        # Fallback engagement content
        return {
            "step_headline": "Let's continue! 🚀",
            "step_motivation": "Thanks for taking the time to share with us."
        }


def score_lead_node(state: SurveyState) -> Dict[str, Any]:
    """Supervisor node for lead scoring."""
    return lead_scoring_node(state)