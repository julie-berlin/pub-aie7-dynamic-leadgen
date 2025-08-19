"""Intelligent Survey Graph - Complete implementation with supervisors and LLM-driven nodes."""

from __future__ import annotations
from langgraph.graph import StateGraph, END
from typing import Dict, Any
import logging

from ..state import SurveyState

# Import existing logic-based nodes (preserved)
from .nodes.tracking_and_response_nodes import (
    initialize_session_with_tracking_node,
    save_responses_immediately_node,
    prepare_step_for_frontend_node
)
from .nodes.lead_scoring_node import lead_scoring_node

# Import new intelligent nodes
from .supervisors.survey_admin_supervisor_v2 import survey_admin_supervisor_node
from .supervisors.lead_intelligence_supervisor_v2 import lead_intelligence_supervisor_node
from .nodes.intelligent_question_selection_node import intelligent_question_selection_node
from .nodes.intelligent_question_phrasing_node import intelligent_question_phrasing_node
from .nodes.intelligent_engagement_node import intelligent_engagement_node
from .nodes.validate_and_adjust_score_node import validate_and_adjust_score_node
from .nodes.unified_completion_message_node import unified_completion_message_node

logger = logging.getLogger(__name__)


def build_intelligent_survey_graph() -> StateGraph:
    """
    Build the intelligent survey graph with supervisor orchestration.
    
    Flow:
    1. Initialize session with tracking
    2. Survey Admin Supervisor makes strategic decisions
    3. Intelligent question selection (LLM within rules)
    4. Question phrasing for engagement (LLM)
    5. Engagement messaging (LLM)
    6. Present to user / handle abandonment
    7. Save responses
    8. Lead Intelligence Supervisor analyzes + tools
    9. Mathematical lead scoring
    10. LLM validates and adjusts score
    11. Unified completion messaging (LLM)
    12. Finalize session
    """
    graph = StateGraph(SurveyState)
    
    # === INITIALIZATION FLOW ===
    graph.add_node("initialize_with_tracking", initialize_session_with_tracking_node)
    
    # === SURVEY ADMINISTRATION SUPERVISOR FLOW ===
    graph.add_node("survey_admin_supervisor", survey_admin_supervisor_node)
    graph.add_node("intelligent_question_selection", intelligent_question_selection_node)
    graph.add_node("intelligent_question_phrasing", intelligent_question_phrasing_node)
    graph.add_node("intelligent_engagement", intelligent_engagement_node)
    graph.add_node("prepare_step_for_frontend", prepare_step_for_frontend_node)
    
    # === RESPONSE PROCESSING FLOW ===
    graph.add_node("save_responses_immediately", save_responses_immediately_node)
    
    # === LEAD INTELLIGENCE FLOW ===
    graph.add_node("lead_intelligence_supervisor", lead_intelligence_supervisor_node)
    graph.add_node("calculate_lead_score", lead_scoring_node)
    graph.add_node("validate_and_adjust_score", validate_and_adjust_score_node)
    
    # === COMPLETION FLOW ===
    graph.add_node("unified_completion_message", unified_completion_message_node)
    graph.add_node("finalize_session", finalize_session_node)
    
    # === ABANDONMENT HANDLING ===
    graph.add_node("check_and_handle_abandonment", check_and_handle_abandonment_node)
    
    # === FLOW CONNECTIONS ===
    
    # Start with session initialization
    graph.set_entry_point("initialize_with_tracking")
    
    # After initialization, survey admin supervisor makes strategic decisions
    graph.add_edge("initialize_with_tracking", "survey_admin_supervisor")
    
    # Survey administration flow
    graph.add_edge("survey_admin_supervisor", "intelligent_question_selection")
    graph.add_edge("intelligent_question_selection", "intelligent_question_phrasing") 
    graph.add_edge("intelligent_question_phrasing", "intelligent_engagement")
    graph.add_edge("intelligent_engagement", "prepare_step_for_frontend")
    
    # After preparing step, conditional routing
    graph.add_conditional_edges(
        "prepare_step_for_frontend",
        should_wait_or_continue,
        {
            END: END,  # Wait for user input
            "save_responses_immediately": "save_responses_immediately",  # Process pending responses
            "check_and_handle_abandonment": "check_and_handle_abandonment"  # Check abandonment
        }
    )
    
    # Response processing flow
    graph.add_edge("save_responses_immediately", "lead_intelligence_supervisor")
    
    # Lead intelligence analysis with potential tool usage
    graph.add_edge("lead_intelligence_supervisor", "calculate_lead_score")
    graph.add_edge("calculate_lead_score", "validate_and_adjust_score")
    
    # After score validation, determine next action
    graph.add_conditional_edges(
        "validate_and_adjust_score",
        should_continue_or_complete,
        {
            "continue": "survey_admin_supervisor",  # Continue survey
            "complete": "unified_completion_message"  # Complete survey
        }
    )
    
    # Completion flow
    graph.add_edge("unified_completion_message", "finalize_session")
    graph.add_edge("finalize_session", END)
    
    # Abandonment flow
    graph.add_edge("check_and_handle_abandonment", "finalize_session")
    
    return graph


# === HELPER NODES ===

def finalize_session_node(state: SurveyState) -> Dict[str, Any]:
    """Finalize session with final database updates."""
    try:
        from ..database import db
        
        session_id = state.get("session_id")
        lead_status = state.get("lead_status", "unknown")
        final_score = state.get("final_score", 0)
        completion_message = state.get("completion_message", "")
        
        # Update session with final status
        final_updates = {
            "status": "completed",
            "completed_at": "now()",
            "lead_status": lead_status,
            "final_score": final_score,
            "completion_message": completion_message
        }
        
        # Add to maybe queue if needed
        if lead_status == "maybe":
            final_updates["requires_review"] = True
            final_updates["review_priority"] = "normal"
        
        # Update database
        db.update_lead_session(session_id, final_updates)
        
        return {
            "completed": True,
            "session_finalized": True,
            "final_status": lead_status,
            "database_updated": True
        }
        
    except Exception as e:
        logger.error(f"Session finalization error: {e}")
        return {
            "completed": True,
            "session_finalized": False,
            "error": str(e)
        }


def check_and_handle_abandonment_node(state: SurveyState) -> Dict[str, Any]:
    """Combined abandonment detection and handling."""
    try:
        from ..database import db
        from datetime import datetime, timedelta
        
        session_id = state.get("session_id")
        last_activity = state.get("last_activity_time")
        
        # Simple abandonment check (can be enhanced)
        if last_activity:
            time_since_activity = datetime.now() - last_activity
            if time_since_activity > timedelta(minutes=10):  # 10 minutes timeout
                
                # Mark as abandoned in database
                db.update_lead_session(session_id, {
                    "status": "abandoned",
                    "abandoned_at": "now()",
                    "completion_type": "timeout"
                })
                
                return {
                    "status": "abandoned",
                    "completed": True,
                    "completion_type": "abandoned",
                    "abandonment_reason": "timeout"
                }
        
        # Still active
        return {
            "status": "active",
            "abandonment_check": "passed"
        }
        
    except Exception as e:
        logger.error(f"Abandonment handling error: {e}")
        return {
            "status": "active",
            "error": str(e)
        }


# === ROUTING FUNCTIONS ===

def should_wait_or_continue(state: SurveyState) -> str:
    """Determine if we should wait for user or continue processing."""
    # Check if we have pending responses to process
    if state.get("pending_responses"):
        return "save_responses_immediately"
    
    # Check for abandonment
    if state.get("check_abandonment", False):
        return "check_and_handle_abandonment"
    
    # Default: wait for user input
    return END


def should_continue_or_complete(state: SurveyState) -> str:
    """Determine if survey should continue or complete."""
    lead_status = state.get("lead_status", "continue")
    
    if lead_status == "continue":
        return "continue"
    else:
        return "complete"


# Export compiled graph
intelligent_survey_graph = build_intelligent_survey_graph().compile()


# Helper functions for API integration
async def start_intelligent_survey(initial_state: dict) -> dict:
    """
    Entry point for intelligent survey with supervisors.
    Used by POST /api/survey/start
    """
    return await intelligent_survey_graph.ainvoke(initial_state)


async def process_survey_responses(state_with_responses: dict) -> dict:
    """
    Entry point for processing user responses.
    Used by POST /api/survey/step
    """
    # Set entry point for response processing
    return await intelligent_survey_graph.ainvoke(
        state_with_responses,
        config={"configurable": {"entry_point": "save_responses_immediately"}}
    )


async def check_survey_abandonment(session_state: dict) -> dict:
    """
    Entry point for abandonment checks.
    Used by background tasks
    """
    return await intelligent_survey_graph.ainvoke(
        session_state,
        config={"configurable": {"entry_point": "check_and_handle_abandonment"}}
    )