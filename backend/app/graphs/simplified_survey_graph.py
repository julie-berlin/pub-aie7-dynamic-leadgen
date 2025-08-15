"""Simplified Survey Graph - Streamlined implementation with consolidated supervisors."""

from __future__ import annotations
from langgraph.graph import StateGraph, END
from typing import Dict, Any
import logging

from ..state import SurveyState

# Import consolidated supervisors
from .supervisors.consolidated_survey_admin_supervisor import consolidated_survey_admin_node
from .supervisors.consolidated_lead_intelligence_agent import consolidated_lead_intelligence_node

# Import toolbelts
from .toolbelts.abandonment_toolbelt import abandonment_toolbelt

# Import existing initialization node (kept as-is)
from .nodes.tracking_and_response_nodes import initialize_session_with_tracking_node

logger = logging.getLogger(__name__)


def build_simplified_survey_graph() -> StateGraph:
    """
    Build the simplified survey graph with consolidated supervisors.
    
    Simplified Flow:
    1. Initialize session with tracking
    2. Survey Admin Supervisor (handles selection, phrasing, engagement, frontend prep)
    3. Wait for user response / check abandonment
    4. Lead Intelligence Agent (handles saving, scoring, tools, status, messages)
    5. Continue or complete based on lead status
    """
    graph = StateGraph(SurveyState)
    
    # === NODE DEFINITIONS ===
    
    # Initialization (kept as-is)
    graph.add_node("initialize_with_tracking", initialize_session_with_tracking_node)
    
    # Consolidated Survey Administration
    graph.add_node("survey_administration", consolidated_survey_admin_node)
    
    # Consolidated Lead Intelligence
    graph.add_node("lead_intelligence", consolidated_lead_intelligence_node)
    
    # Abandonment handling (kept as-is)
    graph.add_node("check_abandonment", check_abandonment_node)
    
    # === FLOW CONNECTIONS ===
    
    # Entry point
    graph.set_entry_point("initialize_with_tracking")
    
    # After initialization, go to survey administration
    graph.add_edge("initialize_with_tracking", "survey_administration")
    
    # After survey admin prepares questions, conditional routing
    graph.add_conditional_edges(
        "survey_administration",
        route_after_survey_admin,
        {
            END: END,  # Wait for user input
            "check_abandonment": "check_abandonment",  # Check for abandonment
            "lead_intelligence": "lead_intelligence"  # Process responses
        }
    )
    
    # After lead intelligence processing, conditional routing
    graph.add_conditional_edges(
        "lead_intelligence",
        route_after_lead_intelligence,
        {
            "survey_administration": "survey_administration",  # Continue survey
            END: END  # Complete survey
        }
    )
    
    # Abandonment always leads to END
    graph.add_edge("check_abandonment", END)
    
    return graph


# === ABANDONMENT NODE ===

def check_abandonment_node(state: SurveyState) -> Dict[str, Any]:
    """Check and handle abandonment using toolbelt."""
    try:
        session_id = state.get("core", {}).get("session_id")
        last_activity = state.get("timing_data", {}).get("last_activity_time")
        
        # Check abandonment
        check_result = abandonment_toolbelt.check_abandonment(
            session_id=session_id,
            last_activity_time=last_activity
        )
        
        if check_result["is_abandoned"]:
            # Mark as abandoned
            abandonment_toolbelt.mark_session_abandoned(
                session_id=session_id,
                abandonment_reason=check_result["reason"],
                abandonment_details={
                    "questions_answered": len(state.get("lead_intelligence", {}).get("responses", [])),
                    "time_on_form": check_result.get("minutes_inactive", 0)
                }
            )
            
            return {
                "status": "abandoned",
                "completed": True,
                "abandonment_info": check_result
            }
        
        # Still active
        return {
            "status": "active",
            "abandonment_check": "passed"
        }
        
    except Exception as e:
        logger.error(f"Abandonment check error: {e}")
        return {
            "status": "active",
            "error": str(e)
        }


# === ROUTING FUNCTIONS ===

def route_after_survey_admin(state: SurveyState) -> str:
    """Determine routing after survey administration."""
    
    # Check if survey admin indicated to route to lead intelligence
    if state.get("route_to_lead_intelligence"):
        return "lead_intelligence"
    
    # Check if we have pending responses to process (legacy check)
    if state.get("pending_responses"):
        return "lead_intelligence"
    
    # Check for abandonment flag
    if state.get("check_abandonment", False):
        return "check_abandonment"
    
    # Check if survey admin marked as complete
    step_type = state.get("step_type", "questions")
    if step_type == "completion":
        return END
    
    # Default: wait for user input
    return END


def route_after_lead_intelligence(state: SurveyState) -> str:
    """Determine routing after lead intelligence processing."""
    
    lead_status = state.get("lead_status", "continue")
    completed = state.get("completed", False)
    
    # If completed or final status reached
    if completed or lead_status in ["qualified", "maybe", "no"]:
        return END
    
    # Continue survey for more questions
    if lead_status == "continue":
        return "survey_administration"
    
    # Default to END
    return END


# === COMPILE GRAPH ===

# Export compiled graph
simplified_survey_graph = build_simplified_survey_graph().compile()


# === API INTEGRATION HELPERS ===

async def start_simplified_survey(initial_state: dict) -> dict:
    """
    Entry point for simplified survey.
    Used by POST /api/survey/start
    """
    return await simplified_survey_graph.ainvoke(initial_state)


async def process_survey_step(state_with_responses: dict) -> dict:
    """
    Process user responses in simplified flow.
    Used by POST /api/survey/step
    """
    # When we have pending responses, start from survey_administration 
    # which will route to lead_intelligence via the routing logic
    return await simplified_survey_graph.ainvoke(state_with_responses)


async def check_abandonment(session_state: dict) -> dict:
    """
    Check for abandonment.
    Used by background tasks
    """
    session_state["check_abandonment"] = True
    
    return await simplified_survey_graph.ainvoke(
        session_state,
        config={"configurable": {"entry_point": "survey_administration"}}
    )


# === DEBUGGING HELPERS ===

def get_graph_structure() -> Dict[str, Any]:
    """Get the structure of the simplified graph for debugging."""
    return {
        "nodes": [
            "initialize_with_tracking",
            "survey_administration",
            "lead_intelligence", 
            "check_abandonment"
        ],
        "edges": [
            ("initialize_with_tracking", "survey_administration"),
            ("survey_administration", "conditional"),
            ("lead_intelligence", "conditional"),
            ("check_abandonment", "END")
        ],
        "entry_point": "initialize_with_tracking"
    }


def validate_state_transitions(state: SurveyState) -> bool:
    """Validate that state transitions are working correctly."""
    try:
        # Check required state fields exist
        required_fields = ["core", "question_strategy", "lead_intelligence"]
        for field in required_fields:
            if field not in state:
                logger.error(f"Missing required state field: {field}")
                return False
        
        # Check core fields
        core = state.get("core", {})
        if not core.get("session_id"):
            logger.error("Missing session_id in core state")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"State validation error: {e}")
        return False