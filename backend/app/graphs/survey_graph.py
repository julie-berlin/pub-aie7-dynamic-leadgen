"""Survey Flow Graph for LangGraph.

Main survey orchestration graph that implements the complete adaptive form flow:
Question Selection → Phrasing → Engagement → Present Step → Score → Continue/Complete

This replaces the FlowEngine with a proper LangGraph implementation.
"""

from __future__ import annotations
from typing import Dict, Any
from datetime import datetime
import json

from langgraph.graph import StateGraph, END

from ..state import SurveyState
from .nodes.question_selection_node import question_selection_node
from .nodes.question_phrasing_node import question_phrasing_node
from .nodes.engagement_node import engagement_node
from .nodes.lead_scoring_node import lead_scoring_node
from ..tools import load_questions, load_client_info


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
        
        # Load questions using our tool
        questions_json = load_questions.invoke({"form_id": form_id})
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


def select_questions_node(state: SurveyState) -> Dict[str, Any]:
    """Wrapper node for question selection."""
    return question_selection_node(state)


def phrase_questions_node(state: SurveyState) -> Dict[str, Any]:
    """
    Wrapper node for question phrasing with client info.
    
    Args:
        state: Current SurveyState
        
    Returns:
        Dict with phrased_questions update
    """
    try:
        form_id = state.get('form_id', 'dogwalk_demo_form')
        
        # Load client info using our tool
        client_json = load_client_info.invoke({"form_id": form_id})
        client_info = json.loads(client_json) if client_json else {}
        
        return question_phrasing_node(state, client_info)
        
    except Exception as e:
        print(f"Error in phrase questions node: {e}")
        # Fallback to original questions
        original_questions = [q.get('question', '') for q in state.get('current_step_questions', [])]
        return {"phrased_questions": original_questions}


def create_engagement_node(state: SurveyState) -> Dict[str, Any]:
    """
    Wrapper node for engagement with client info.
    
    Args:
        state: Current SurveyState
        
    Returns:
        Dict with step_headline and step_motivation updates
    """
    try:
        form_id = state.get('form_id', 'dogwalk_demo_form')
        
        # Load client info using our tool
        client_json = load_client_info.invoke({"form_id": form_id})
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
    """Wrapper node for lead scoring."""
    return lead_scoring_node(state)


def update_step_node(state: SurveyState) -> Dict[str, Any]:
    """
    Update step counter and last_updated timestamp.
    
    Args:
        state: Current SurveyState
        
    Returns:
        Dict with step and last_updated updates
    """
    return {
        'step': state.get('step', 0) + 1,
        'last_updated': datetime.now().isoformat()
    }


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


def build_survey_graph() -> StateGraph:
    """
    Build the complete survey flow graph.
    
    The flow follows this pattern:
    Start → Initialize → Select Questions → Phrase Questions → Engagement → 
    Update Step → Score Lead → Continue/Complete
    
    Returns:
        Compiled StateGraph ready for execution
    """
    graph = StateGraph(SurveyState)
    
    # Add all nodes
    graph.add_node("initialize_session", initialize_session_node)
    graph.add_node("select_questions", select_questions_node)
    graph.add_node("phrase_questions", phrase_questions_node)
    graph.add_node("create_engagement", create_engagement_node)
    graph.add_node("update_step", update_step_node)
    graph.add_node("score_lead", score_lead_node)
    graph.add_node("completion", completion_node)
    
    # Set entry point
    graph.set_entry_point("initialize_session")
    
    # Add edges for the main flow
    graph.add_edge("initialize_session", "select_questions")
    graph.add_edge("select_questions", "phrase_questions")
    graph.add_edge("phrase_questions", "create_engagement")
    graph.add_edge("create_engagement", "update_step")
    graph.add_edge("update_step", "score_lead")
    
    # Add conditional routing after scoring
    graph.add_conditional_edges(
        "score_lead",
        should_continue_survey,
        {
            "continue": "select_questions",  # Loop back to select more questions
            "complete": "completion",  # Move to completion
            END: END  # End graph (wait for user responses)
        }
    )
    
    # Completion leads to END
    graph.add_edge("completion", END)
    
    return graph


# Export compiled graph for use
survey_graph = build_survey_graph().compile()