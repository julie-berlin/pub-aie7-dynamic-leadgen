"""
Routing Logic for LangGraph Survey Flow

Contains decision functions that determine survey flow routing.
"""

from __future__ import annotations

from langgraph.graph import END

from ...state import SurveyGraphState
from ..toolbelts.minimal_toolbelt import minimal_toolbelt


def should_continue_survey(state: SurveyGraphState) -> str:
    """
    Determine if survey should continue or complete based on business rules.
    Updated to work with hierarchical state structure.
    
    Args:
        state: Current SurveyGraphState with hierarchical structure
        
    Returns:
        String routing decision: "continue", "complete", or END
    """
    try:
        # Extract from hierarchical state
        core = state.get('core', {})
        question_strategy = state.get('question_strategy', {})
        lead_intelligence = state.get('lead_intelligence', {})
        engagement = state.get('engagement', {})
        
        responses = lead_intelligence.get('responses', [])
        step = core.get('step', 0)
        
        # CRITICAL: If no responses yet, we've just prepared the first step
        # The graph should END here and wait for user to provide responses
        if not responses:
            print("Decision: END (waiting for user responses)")
            return END
        
        # Extract question data
        all_questions = question_strategy.get('all_questions', [])
        asked_questions = question_strategy.get('asked_questions', [])
        current_questions = question_strategy.get('current_questions', [])
        
        available_questions = [q for q in all_questions if q['id'] not in asked_questions]
        
        lead_status = lead_intelligence.get('lead_status', 'unknown')
        abandonment_status = engagement.get('abandonment_status', 'active')
        
        # Business rules for completion
        should_complete = (
            abandonment_status == 'abandoned' or  # User abandoned
            not all_questions or  # No questions loaded at all
            not available_questions or  # No more questions available
            not current_questions or  # No questions selected for current step
            len(responses) >= 8 or  # Maximum questions asked
            step >= 12 or  # Maximum steps reached (safety valve)
            (lead_status in ['yes', 'no'] and len(responses) >= 4)  # Clear qualification with minimum questions
        )
        
        print(f"Continue check - Step: {step}, Available: {len(available_questions)}, Current: {len(current_questions)}, Responses: {len(responses)}, Status: {lead_status}, Abandonment: {abandonment_status}")
        
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


def should_wait_or_continue(state: SurveyGraphState) -> str:
    """
    Determine if graph should wait for user input or continue processing.
    Used after step preparation to decide next action.
    """
    try:
        core = state.get('core', {})
        lead_intelligence = state.get('lead_intelligence', {})
        
        pending_responses = state.get('pending_responses', [])
        responses = lead_intelligence.get('responses', [])
        completed = core.get('completed', False)
        
        if completed:
            return END
        elif pending_responses:
            return "process_responses"  # New responses to process
        elif not responses:
            return END  # Wait for first responses
        else:
            return "continue_flow"  # Continue with next step
            
    except Exception as e:
        print(f"Error in should_wait_or_continue: {e}")
        return END


def should_continue_or_complete(state: SurveyGraphState) -> str:
    """
    Determine if survey should continue or complete after processing responses.
    Similar to should_continue_survey but specifically for post-response processing.
    """
    try:
        # Use the same logic as should_continue_survey
        return should_continue_survey(state)
            
    except Exception as e:
        print(f"Error in should_continue_or_complete: {e}")
        return "complete"


def route_completion_type(state: SurveyGraphState) -> str:
    """
    Route to appropriate completion flow based on lead qualification.
    
    Returns:
        "qualified_completion" for yes/maybe leads (personalized message)
        "unqualified_completion" for no leads (simple message)
        "abandoned_completion" for abandoned sessions
    """
    try:
        lead_intelligence = state.get('lead_intelligence', {})
        engagement = state.get('engagement', {})
        
        lead_status = lead_intelligence.get('lead_status', 'unknown')
        abandonment_status = engagement.get('abandonment_status', 'active')
        
        if abandonment_status == 'abandoned':
            print(f"Routing to abandoned completion - abandonment status: {abandonment_status}")
            return "abandoned_completion"
        elif lead_status in ['yes', 'maybe']:
            print(f"Routing to qualified completion - lead status: {lead_status}")
            return "qualified_completion"
        else:
            print(f"Routing to unqualified completion - lead status: {lead_status}")
            return "unqualified_completion"
            
    except Exception as e:
        print(f"Error in route_completion_type: {e}")
        # Default to unqualified completion
        return "unqualified_completion"


def is_abandoned(state: SurveyGraphState) -> str:
    """
    Check if session has been abandoned.
    Used for timeout-based abandonment detection.
    """
    try:
        engagement = state.get('engagement', {})
        abandonment_status = engagement.get('abandonment_status', 'active')
        
        if abandonment_status == 'abandoned':
            return "abandoned"
        else:
            return "active"
            
    except Exception as e:
        print(f"Error in is_abandoned: {e}")
        return "active"