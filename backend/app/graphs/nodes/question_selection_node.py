"""Question Selection Node for LangGraph.

Intelligently selects 1-3 logically related questions for each form step,
avoiding repetition and following business rules.

Replaces the old AgentExecutor pattern with direct function calls for better performance.
"""

from typing import Dict, Any, List
from ...state import SurveyState


def question_selection_node(state: SurveyState) -> Dict[str, Any]:
    """
    Select questions for the next form step based on current state.
    
    Args:
        state: Current SurveyState containing questions, responses, etc.
    
    Returns:
        Dict with current_step_questions update for state
    """
    try:
        all_questions = state.get('all_questions', [])
        asked_ids = state.get('asked_questions', [])
        step = state.get('step', 0)
        response_count = len(state.get('responses', []))
        
        # Filter available questions
        available = [q for q in all_questions if q['id'] not in asked_ids]
        
        if not available:
            return {"current_step_questions": []}
        
        # Business rules for selection
        tough_questions = [q for q in available
                          if 'dangerous' in q.get('scoring_rubric', '').lower()
                          or 'must be' in q.get('scoring_rubric', '').lower()
                          or 'required' in q.get('scoring_rubric', '').lower()]
        
        easy_questions = [q for q in available if q not in tough_questions]
        
        # Select based on step and response count
        if step < 2 or response_count < 4:
            # Early steps - use easy questions
            candidates = easy_questions if easy_questions else available
        else:
            # Can now ask tough questions
            candidates = available
        
        # Group related questions by category
        contact_questions = [q for q in candidates
                           if any(word in q['question'].lower()
                                 for word in ['name', 'phone', 'email', 'contact'])]
        
        dog_questions = [q for q in candidates
                        if any(word in q['question'].lower()
                              for word in ['dog', 'breed', 'walk', 'vaccination'])]
        
        service_questions = [q for q in candidates
                           if any(word in q['question'].lower()
                                 for word in ['times', 'frequency', 'benefit', 'training'])]
        
        # Select 1-3 questions from same category when possible
        selected = []
        if contact_questions and response_count >= 3:
            # Ask contact info questions later in the flow
            selected = contact_questions[:2]
        elif dog_questions:
            selected = dog_questions[:2]
        elif service_questions:
            selected = service_questions[:2]
        else:
            selected = candidates[:2]
        
        # Ensure we don't exceed 3 questions and have at least 1
        selected = selected[:3]
        if not selected and candidates:
            selected = [candidates[0]]
        
        return {"current_step_questions": selected}
        
    except Exception as e:
        print(f"Error in question selection node: {e}")
        # Return empty selection on error
        return {"current_step_questions": []}


def get_selected_question_ids(state: SurveyState) -> List[int]:
    """
    Utility function to extract question IDs from current step questions.
    
    Args:
        state: Current SurveyState
        
    Returns:
        List of selected question IDs
    """
    current_questions = state.get('current_step_questions', [])
    return [q['id'] for q in current_questions]