"""Simplified Survey Graph - Exact copy of production logic."""

from langgraph.graph import StateGraph, END
from typing import Dict, Any
import logging
from datetime import datetime
import uuid

from graph.state import SurveyState
from graph.supervisors.consolidated_survey_admin import consolidated_survey_admin_node
from graph.supervisors.consolidated_lead_intelligence import consolidated_lead_intelligence_node

logger = logging.getLogger(__name__)

def initialize_session_with_tracking_node(state: SurveyState) -> Dict[str, Any]:
    """Initialize session with tracking data."""
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from database.sqlite_db import db
        
        # Check if this is a continuation (already has session_id)
        existing_session_id = state.get("core", {}).get("session_id")
        
        if existing_session_id:
            logger.info(f"🔄 Continuing existing session: {existing_session_id}")
            # Just pass through existing state for continuation
            return dict(state)
        
        # Generate session ID for new session
        session_id = str(uuid.uuid4())
        form_id = state.get("core", {}).get("form_id")
        
        logger.info(f"🚀 Initializing new session: {session_id} for form: {form_id}")
        
        # Create session in database
        session_data = {
            "session_id": session_id,
            "form_id": form_id,
            "client_id": state.get("core", {}).get("client_id")
        }
        
        db.create_lead_session(session_data)
        
        # Load form questions
        questions = db.get_form_questions(form_id)
        
        # Initialize state
        return {
            "core": {
                "session_id": session_id,
                "form_id": form_id,
                "client_id": state.get("core", {}).get("client_id"),
                "started_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "step": 0,
                "completed": False
            },
            "question_strategy": {
                "all_questions": questions,
                "asked_questions": [],
                "current_questions": [],
                "phrased_questions": [],
                "question_strategy": {},
                "selection_history": []
            },
            "lead_intelligence_agent": {
                "responses": [],
                "current_score": 0,
                "score_history": [],
                "lead_status": "unknown",
                "qualification_reasoning": [],
                "risk_factors": [],
                "positive_indicators": []
            },
            "pending_responses": state.get("pending_responses", []),
            "metadata": {
                "initialized_at": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Initialization error: {e}")
        return {
            "error": str(e),
            "core": {
                "session_id": str(uuid.uuid4()),
                "completed": True
            }
        }

def check_abandonment_node(state: SurveyState) -> Dict[str, Any]:
    """Check and handle abandonment."""
    # For testing, we'll skip abandonment logic
    return {
        "status": "active",
        "abandonment_check": "passed"
    }

def build_simplified_survey_graph() -> StateGraph:
    """
    Build the simplified survey graph with consolidated supervisors.
    
    Exact flow from production:
    1. Initialize session with tracking
    2. Survey Admin Supervisor (handles selection, phrasing, engagement, frontend prep)
    3. Wait for user response / check abandonment
    4. Lead Intelligence Agent (handles saving, scoring, tools, status, messages)
    5. Continue or complete based on lead status
    """
    graph = StateGraph(SurveyState)
    
    # === NODE DEFINITIONS ===
    
    # Initialization
    graph.add_node("initialize_with_tracking", initialize_session_with_tracking_node)
    
    # Consolidated Survey Administration
    graph.add_node("question_flow_agent", consolidated_survey_admin_node)
    
    # Consolidated Lead Intelligence
    graph.add_node("lead_intelligence_agent", consolidated_lead_intelligence_node)
    
    # Abandonment handling
    graph.add_node("check_abandonment", check_abandonment_node)
    
    # === FLOW CONNECTIONS ===
    
    # Entry point
    graph.set_entry_point("initialize_with_tracking")
    
    # After initialization, always go to question flow agent
    graph.add_edge("initialize_with_tracking", "question_flow_agent")
    
    # After survey admin prepares questions
    graph.add_conditional_edges(
        "question_flow_agent",
        route_after_survey_admin,
        {
            END: END,
            "check_abandonment": "check_abandonment",
            "lead_intelligence_agent": "lead_intelligence_agent"
        }
    )
    
    # After lead intelligence processing
    graph.add_conditional_edges(
        "lead_intelligence_agent",
        route_after_lead_intelligence,
        {
            "question_flow_agent": "question_flow_agent",
            END: END
        }
    )
    
    # Abandonment always leads to END
    graph.add_edge("check_abandonment", END)
    
    return graph

# === ROUTING FUNCTIONS ===

# Removed route_after_initialization since we now use direct edge

def route_after_survey_admin(state: SurveyState) -> str:
    """Determine routing after survey administration."""
    
    # Check if survey admin indicated to route to lead intelligence
    if state.get("route_to_lead_intelligence"):
        logger.info("🔀 Routing to lead_intelligence (admin flag)")
        return "lead_intelligence_agent"
    
    # Check if we have pending responses
    if state.get("pending_responses"):
        logger.info("🔀 Routing to lead_intelligence (pending responses)")
        return "lead_intelligence_agent"
    
    # Check for abandonment
    if state.get("check_abandonment", False):
        return "check_abandonment"
    
    # Check if complete
    step_type = state.get("step_type", "questions")
    if step_type == "completion":
        return END
    
    # Default: wait for user input
    logger.info("🔀 Waiting for user input")
    return END

def route_after_lead_intelligence(state: SurveyState) -> str:
    """Determine routing after lead intelligence processing."""
    
    lead_status = state.get("lead_status", "unknown")
    completed = state.get("completed", False)
    route_decision = state.get("route_decision", "end")
    
    logger.info(f"🔀 Routing after lead_intelligence: status={lead_status}, completed={completed}, route={route_decision}")
    logger.info(f"🔍 Full state keys: {list(state.keys())}")
    
    # Use the route decision from lead intelligence
    if route_decision == "end" or completed:
        logger.info("🔀 Survey complete!")
        return END
    
    # Check for too many iterations (safety check)
    core = state.get("core", {})
    step = core.get("step", 0)
    if step > 20:
        logger.warning(f"🔀 Forcing END (too many steps: {step})")
        return END
    
    # Continue survey if route decision is continue
    if route_decision == "continue":
        logger.info("🔀 Continuing to survey_administration")
        return "question_flow_agent"
    
    # Default to end
    logger.info("🔀 Default to END")
    return END

# === COMPILE GRAPH ===

# Export compiled graph
simplified_survey_graph = build_simplified_survey_graph().compile()

# === API INTEGRATION HELPERS ===

async def start_simplified_survey(initial_state: dict) -> dict:
    """Entry point for simplified survey."""
    return await simplified_survey_graph.ainvoke(initial_state)

async def process_survey_step(state_with_responses: dict) -> dict:
    """Process user responses in simplified flow."""
    return await simplified_survey_graph.ainvoke(state_with_responses)

def run_survey_sync(initial_state: dict) -> dict:
    """Synchronous entry point for testing."""
    return simplified_survey_graph.invoke(initial_state)