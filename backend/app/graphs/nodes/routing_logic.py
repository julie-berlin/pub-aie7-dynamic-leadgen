"""
Routing Logic for LangGraph Survey Flow

Contains decision functions that determine survey flow routing.
"""

from __future__ import annotations

from langgraph.graph import END

from ...state import SurveyState
from ..toolbelts.minimal_toolbelt import minimal_toolbelt


def should_continue_survey(state: SurveyState) -> str:
    """
    Determine if survey should continue or complete based on business rules.
    
    This is the key decision point: 
    - If no responses yet, we've prepared the first step → END (wait for user)
    - If responses exist, check if we need more questions → continue or complete
    
    Args:
        state: Current SurveyState
        
    Returns:
        String routing decision: "continue", "complete", or END
    """
    try:
        responses = state.get('responses', [])
        
        # CRITICAL: If no responses yet, we've just prepared the first step
        # The graph should END here and wait for user to provide responses
        if not responses:
            print("Decision: END (waiting for user responses)")
            return END
        
        # If we have responses, check normal completion criteria
        all_questions = state.get('all_questions', [])
        asked_questions = state.get('asked_questions', [])
        current_step_questions = state.get('current_step_questions', [])
        
        available_questions = [q for q in all_questions if q['id'] not in asked_questions]
        
        lead_status = state.get('lead_status', 'unknown')
        failed_required = state.get('failed_required', False)
        step = state.get('step', 0)
        
        # Business rules for completion (when we have responses)
        should_complete = (
            not all_questions or  # No questions loaded at all
            not available_questions or  # No more questions available
            not current_step_questions or  # No questions selected for current step
            failed_required or  # Failed critical requirement
            len(responses) >= 6 or  # Maximum questions asked
            step >= 10 or  # Maximum steps reached (safety valve)
            (lead_status in ['yes', 'no'] and len(responses) >= 4)  # Clear qualification with minimum questions
        )
        
        print(f"Continue check - Step: {step}, Available: {len(available_questions)}, Current: {len(current_step_questions)}, Responses: {len(responses)}, Status: {lead_status}")
        
        if should_complete:
            print("Decision: COMPLETE")
            return "complete"
        else:
            print("Decision: CONTINUE")
            return "continue"
            
    except Exception as e:
        print(f"Error in should_continue_survey: {e}")
        # Default to complete on error to avoid infinite loops
        return "complete"