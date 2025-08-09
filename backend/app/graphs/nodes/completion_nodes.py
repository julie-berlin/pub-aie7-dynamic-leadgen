"""
Completion Flow Nodes for LangGraph Survey Flow

Handles completion message generation, finalization, and completion state management.
"""

from __future__ import annotations
from typing import Dict, Any
from datetime import datetime
import json

from ...state import SurveyState
from ..toolbelts.completion_toolbelt import completion_toolbelt
from .completion_helpers import extract_personalization_data, generate_completion_message_with_llm


def message_generation_node(state: SurveyState) -> Dict[str, Any]:
    """
    Generate personalized completion message using LLM based on business context.
    
    Args:
        state: Current SurveyState with responses and lead status
        
    Returns:
        Dict with completion_message and next_steps for state
    """
    try:
        form_id = state.get('form_id', 'dogwalk_demo_form')
        lead_status = state.get('lead_status', 'unknown')
        responses = state.get('responses', [])
        
        # Load client info for business context using our tool belt
        client_json = completion_toolbelt.load_client_info.invoke({"form_id": form_id})
        client_info = json.loads(client_json) if client_json else {}
        
        business_name = client_info.get('information', {}).get('name', 'Our Business')
        owner_name = client_info.get('information', {}).get('owner', 'The Owner')
        business_context = {
            'background': client_info.get('background', ''),
            'goals': client_info.get('goals', ''),
            'information': client_info.get('information', {})
        }
        
        # Extract personalization data from responses
        personalization = extract_personalization_data(responses)
        
        # Generate completion message using LLM
        completion_data = generate_completion_message_with_llm(
            lead_status=lead_status,
            personalization=personalization,
            business_name=business_name,
            owner_name=owner_name,
            business_context=business_context
        )
        
        return {
            'completion_message': completion_data['completion_message'],
            'next_steps': completion_data['next_steps']
        }
        
    except Exception as e:
        print(f"Error in message generation: {e}")
        # Fallback message
        return {
            'completion_message': "Thank you for your time! We appreciate your interest.",
            'next_steps': ["We'll be in touch soon with next steps."]
        }


def finalization_node(state: SurveyState) -> Dict[str, Any]:
    """
    Finalize survey session and prepare final state.
    
    Args:
        state: Current SurveyState
        
    Returns:
        Dict with final completion updates
    """
    try:
        final_timestamp = datetime.now().isoformat()
        
        return {
            'completed': True,
            'last_updated': final_timestamp,
            'completed_at': final_timestamp
        }
        
    except Exception as e:
        print(f"Error in finalization: {e}")
        return {
            'completed': True,
            'last_updated': datetime.now().isoformat()
        }


def completion_node(state: SurveyState) -> Dict[str, Any]:
    """
    Mark survey as completed and prepare final state.
    
    Args:
        state: Current SurveyState
        
    Returns:
        Dict with completed flag and final timestamp
    """
    return {
        'completed': True,
        'last_updated': datetime.now().isoformat()
    }