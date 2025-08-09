"""Question Selection Node for LangGraph.

Intelligently selects 1-3 logically related questions for each form step,
avoiding repetition and following business rules.

Replaces the old AgentExecutor pattern with direct function calls for better performance.
"""

from typing import Dict, Any, List
import json
from ...state import SurveyGraphState
from ..toolbelts.persistence_toolbelt import persistence_toolbelt


def question_selection_node(state: SurveyGraphState) -> Dict[str, Any]:
    """
    Select questions for the next form step based on current state.
    
    Args:
        state: Current SurveyGraphState containing hierarchical state
    
    Returns:
        Dict with question_strategy updates for state
    """
    try:
        # Extract state from hierarchical structure
        core = state.get('core', {})
        question_strategy = state.get('question_strategy', {})
        lead_intelligence = state.get('lead_intelligence', {})
        
        form_id = core.get('form_id', 'dogwalk_demo_form')
        step = core.get('step', 0)
        
        # Load questions if not already loaded
        all_questions = question_strategy.get('all_questions', [])
        if not all_questions:
            # Load questions from JSON using tools
            from ...tools import load_questions
            questions_json = load_questions.invoke({'form_id': form_id})
            all_questions = json.loads(questions_json)
        
        asked_ids = question_strategy.get('asked_questions', [])
        responses = lead_intelligence.get('responses', [])
        response_count = len(responses)
        
        # Filter available questions
        available = [q for q in all_questions if q['id'] not in asked_ids]
        
        if not available:
            return {
                'question_strategy': {
                    **question_strategy,
                    'all_questions': all_questions,
                    'current_questions': []
                }
            }
        
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
        
        # Record selection history for supervisor analysis
        selection_entry = {
            'step': step,
            'selected_ids': [q['id'] for q in selected],
            'selection_reasoning': 'Early step easy questions' if step < 2 else 'Mixed difficulty questions',
            'available_count': len(available)
        }
        
        # Update question strategy state
        updated_strategy = {
            **question_strategy,
            'all_questions': all_questions,
            'current_questions': selected,
            'selection_history': question_strategy.get('selection_history', []) + [selection_entry]
        }
        
        return {
            'question_strategy': updated_strategy
        }
        
    except Exception as e:
        print(f"Error in question selection node: {e}")
        # Return empty selection on error
        return {
            'question_strategy': {
                **state.get('question_strategy', {}),
                'current_questions': []
            }
        }


def get_selected_question_ids(state: SurveyGraphState) -> List[int]:
    """
    Utility function to extract question IDs from current step questions.
    
    Args:
        state: Current SurveyGraphState
        
    Returns:
        List of selected question IDs
    """
    question_strategy = state.get('question_strategy', {})
    current_questions = question_strategy.get('current_questions', [])
    return [q['id'] for q in current_questions]