"""Survey Flow Graph V2 - Properly structured for real-world usage.

Actual flow:
1. User arrives with UTM params → Initialize session with tracking
2. Generate first step questions → Return to frontend
3. User submits answers → Save immediately → Generate next step
4. Repeat until complete or abandoned
5. Conditional completion based on qualification
"""

from __future__ import annotations
from langgraph.graph import StateGraph, END

from ..state import SurveyGraphState
from .nodes.initialize_session_node import initialize_session_with_tracking_node
from .nodes.supervisor_integration_nodes import (
    master_flow_coordination_node,
    question_strategy_node,
    lead_intelligence_node,
    engagement_supervision_node,
    supervisor_coordination_node
)
from .nodes.response_processing_nodes import (
    process_user_responses_node,
    save_responses_immediately_node,
    check_abandonment_node
)
from .nodes.step_preparation_nodes import (
    prepare_step_for_frontend_node,
    update_step_node
)
from .nodes.persistence_nodes import (
    update_session_node,
    save_completion_node
)
from .nodes.completion_nodes import (
    qualified_message_generation_node,
    unqualified_completion_node,
    finalization_node
)


def build_survey_graph_v2() -> StateGraph:
    """
    Build the real-world survey flow graph.
    
    Two main entry points:
    1. initialize_with_tracking - First visit with UTM params
    2. process_responses - When user submits answers
    """
    graph = StateGraph(SurveyGraphState)
    
    # === INITIALIZATION FLOW ===
    # Entry point 1: New session with tracking
    graph.add_node("initialize_with_tracking", initialize_session_with_tracking_node)
    
    # === QUESTION GENERATION FLOW ===
    # Supervisor coordination for question selection
    graph.add_node("master_coordination", master_flow_coordination_node)
    graph.add_node("question_strategy", question_strategy_node)
    graph.add_node("lead_intelligence", lead_intelligence_node)
    graph.add_node("engagement_supervision", engagement_supervision_node)
    graph.add_node("supervisor_coordination", supervisor_coordination_node)
    
    # === RESPONSE PROCESSING FLOW ===
    # Entry point 2: User submits answers
    graph.add_node("process_responses", process_user_responses_node)
    graph.add_node("save_responses_immediately", save_responses_immediately_node)
    graph.add_node("check_abandonment", check_abandonment_node)
    
    # === STEP MANAGEMENT ===
    graph.add_node("prepare_step_for_frontend", prepare_step_for_frontend_node)
    graph.add_node("update_step", update_step_node)
    graph.add_node("update_session", update_session_node)
    
    # === COMPLETION FLOW ===
    graph.add_node("qualified_message_generation", qualified_message_generation_node)
    graph.add_node("unqualified_completion", unqualified_completion_node)
    graph.add_node("save_completion", save_completion_node)
    graph.add_node("finalization", finalization_node)
    
    # === FLOW CONNECTIONS ===
    
    # Initialization flow
    graph.set_entry_point("initialize_with_tracking")
    graph.add_edge("initialize_with_tracking", "master_coordination")
    
    # Supervisor flow (parallel execution)
    graph.add_edge("master_coordination", "question_strategy")
    graph.add_edge("master_coordination", "lead_intelligence") 
    graph.add_edge("master_coordination", "engagement_supervision")
    
    # Supervisors converge
    graph.add_edge("question_strategy", "supervisor_coordination")
    graph.add_edge("lead_intelligence", "supervisor_coordination")
    graph.add_edge("engagement_supervision", "supervisor_coordination")
    
    # Prepare step for frontend
    graph.add_edge("supervisor_coordination", "prepare_step_for_frontend")
    graph.add_edge("prepare_step_for_frontend", "update_step")
    
    # Update session in parallel (fire-and-forget)
    graph.add_edge("update_step", "update_session")
    
    # First decision point: Wait for user or continue
    graph.add_conditional_edges(
        "update_step",
        should_wait_or_continue,
        {
            "wait_for_user": END,  # Return questions to frontend
            "continue_flow": "master_coordination",  # Process more
            "check_abandonment": "check_abandonment"  # Check if abandoned
        }
    )
    
    # Response processing flow (alternate entry)
    graph.add_edge("process_responses", "save_responses_immediately")
    graph.add_edge("save_responses_immediately", "lead_intelligence")  # Re-score with new responses
    
    # After processing responses, check if we should continue
    graph.add_conditional_edges(
        "lead_intelligence",
        should_continue_or_complete,
        {
            "continue": "master_coordination",  # Get more questions
            "complete_qualified": "qualified_message_generation",  # Qualified/Maybe
            "complete_unqualified": "unqualified_completion"  # Not qualified
        }
    )
    
    # Abandonment check
    graph.add_conditional_edges(
        "check_abandonment",
        is_abandoned,
        {
            "abandoned": "unqualified_completion",  # Mark as abandoned
            "active": END  # Still active, wait more
        }
    )
    
    # Completion flows
    graph.add_edge("qualified_message_generation", "save_completion")
    graph.add_edge("unqualified_completion", "save_completion")
    graph.add_edge("save_completion", "finalization")
    graph.add_edge("finalization", END)
    
    return graph


def should_wait_or_continue(state: SurveyGraphState) -> str:
    """
    Determine if we should wait for user input or continue processing.
    """
    # Check if we have responses to process
    lead_intelligence = state.get('lead_intelligence', {})
    responses = lead_intelligence.get('responses', [])
    
    # If no responses yet, wait for user
    if not responses:
        return "wait_for_user"
    
    # Check if enough time has passed for abandonment check
    engagement = state.get('engagement', {})
    last_activity = engagement.get('last_activity_timestamp')
    if last_activity and should_check_abandonment(last_activity):
        return "check_abandonment"
    
    # Otherwise continue flow
    return "continue_flow"


def should_continue_or_complete(state: SurveyGraphState) -> str:
    """
    After processing responses, decide next action.
    """
    master_flow = state.get('master_flow', {})
    lead_intelligence = state.get('lead_intelligence', {})
    
    # Check completion criteria
    responses = lead_intelligence.get('responses', [])
    lead_status = lead_intelligence.get('lead_status', 'unknown')
    
    # Business rules
    if len(responses) >= 10:  # Max questions
        if lead_status in ['yes', 'maybe']:
            return "complete_qualified"
        else:
            return "complete_unqualified"
    
    if lead_status == 'no' and len(responses) >= 4:  # Failed after minimum
        return "complete_unqualified"
    
    if lead_status == 'yes' and len(responses) >= 6:  # Qualified with enough data
        return "complete_qualified"
    
    # Default: continue getting more questions
    return "continue"


def is_abandoned(state: SurveyGraphState) -> str:
    """
    Check if session is abandoned.
    """
    engagement = state.get('engagement', {})
    abandonment_risk = engagement.get('abandonment_risk', 0)
    
    if abandonment_risk > 0.8:  # High confidence of abandonment
        return "abandoned"
    else:
        return "active"


def should_check_abandonment(last_activity: str) -> bool:
    """
    Determine if enough time has passed to check abandonment.
    """
    from datetime import datetime, timedelta
    
    try:
        last_time = datetime.fromisoformat(last_activity)
        time_since = datetime.now() - last_time
        
        # Check if more than 5 minutes of inactivity
        return time_since > timedelta(minutes=5)
    except:
        return False


# Export compiled graph
survey_graph_v2 = build_survey_graph_v2().compile()