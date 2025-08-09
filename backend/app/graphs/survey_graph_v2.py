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
from .nodes.tracking_and_response_nodes import (
    initialize_session_with_tracking_node,
    process_user_responses_node,
    save_responses_immediately_node,
    check_abandonment_node,
    prepare_step_for_frontend_node,
    qualified_message_generation_node,
    unqualified_completion_node
)
from .nodes.question_selection_node import question_selection_node
from .nodes.question_phrasing_node import question_phrasing_node
from .nodes.routing_logic import (
    should_wait_or_continue,
    should_continue_or_complete,
    route_completion_type,
    is_abandoned
)


def build_survey_graph_v2() -> StateGraph:
    """
    Build the real-world survey flow graph with proper nodes from Phases 2-5.
    
    Multiple entry points:
    1. initialize_with_tracking - First visit with UTM params
    2. process_responses - When user submits answers  
    3. check_abandonment - Timeout/abandonment checks
    """
    graph = StateGraph(SurveyGraphState)
    
    # === INITIALIZATION FLOW ===
    # Entry point 1: New session with tracking
    graph.add_node("initialize_with_tracking", initialize_session_with_tracking_node)
    
    # === QUESTION GENERATION FLOW ===
    graph.add_node("question_selection", question_selection_node)
    graph.add_node("question_phrasing", question_phrasing_node)
    
    # === RESPONSE PROCESSING FLOW ===
    # Entry point 2: User submits answers
    graph.add_node("process_responses", process_user_responses_node)
    graph.add_node("save_responses_immediately", save_responses_immediately_node)
    
    # === STEP MANAGEMENT ===
    graph.add_node("prepare_step_for_frontend", prepare_step_for_frontend_node)
    
    # === ABANDONMENT CHECKING ===
    # Entry point 3: Timeout checks
    graph.add_node("check_abandonment", check_abandonment_node)
    
    # === COMPLETION FLOW ===
    graph.add_node("qualified_message_generation", qualified_message_generation_node)
    graph.add_node("unqualified_completion", unqualified_completion_node)
    
    # === FLOW CONNECTIONS ===
    
    # === MULTIPLE ENTRY POINTS ===
    # Default entry point: New session initialization
    graph.set_entry_point("initialize_with_tracking")
    
    # Note: Other entry points are handled by the API layer invoking specific nodes
    
    # After initialization, generate first questions
    graph.add_edge("initialize_with_tracking", "question_selection")
    graph.add_edge("question_selection", "question_phrasing")
    graph.add_edge("question_phrasing", "prepare_step_for_frontend")
    
    # After preparing step, wait for user or continue based on state
    graph.add_conditional_edges(
        "prepare_step_for_frontend",
        should_wait_or_continue,
        {
            END: END,  # Wait for user input (first questions)
            "process_responses": "process_responses",  # Has pending responses
            "continue_flow": "question_selection"  # Continue to next step
        }
    )
    
    # === ENTRY POINT 2: RESPONSE PROCESSING FLOW ===
    # When user submits responses, save immediately then continue
    graph.add_edge("process_responses", "save_responses_immediately")
    
    # After saving responses, check if we should continue or complete
    graph.add_conditional_edges(
        "save_responses_immediately",
        should_continue_or_complete,
        {
            "continue": "question_selection",  # Get more questions
            "complete": "route_to_completion"  # Ready to complete
        }
    )
    
    # === COMPLETION ROUTING ===
    # Route to appropriate completion based on lead status
    graph.add_node("route_to_completion", lambda state: state)  # Pass-through node
    graph.add_conditional_edges(
        "route_to_completion",
        route_completion_type,
        {
            "qualified_completion": "qualified_message_generation",
            "unqualified_completion": "unqualified_completion",
            "abandoned_completion": "mark_abandoned"  # Handle abandonment separately
        }
    )
    
    # === ABANDONMENT HANDLING ===
    graph.add_node("mark_abandoned", lambda state: {
        **state,
        'core': {
            **state.get('core', {}),
            'completed': True,
            'completion_type': 'abandoned'
        },
        'engagement': {
            **state.get('engagement', {}),
            'abandonment_status': 'abandoned',
            'abandonment_risk': 1.0
        }
    })
    
    # === ENTRY POINT 3: ABANDONMENT CHECK ===
    # Abandonment detection flow
    graph.add_conditional_edges(
        "check_abandonment",
        is_abandoned,
        {
            "abandoned": "mark_abandoned",  # Mark as abandoned, don't complete
            "active": END  # Still active, return to wait
        }
    )
    
    # === COMPLETION FLOWS ===
    # All completion types end the flow
    graph.add_edge("qualified_message_generation", END)
    graph.add_edge("unqualified_completion", END)
    graph.add_edge("mark_abandoned", END)  # Abandonment also ends flow
    
    return graph


# Note: All routing functions are imported from .nodes.routing_logic


# Export compiled graph
survey_graph_v2 = build_survey_graph_v2().compile()


# Helper functions for API entry points
async def start_new_session(initial_state: dict) -> dict:
    """
    Entry point 1: Start new session with tracking.
    Used by POST /api/survey/start
    """
    return await survey_graph_v2.ainvoke(initial_state)


async def process_user_responses(state_with_responses: dict) -> dict:
    """
    Entry point 2: Process user responses.
    Used by POST /api/survey/step
    """
    # Start from the response processing node
    return await survey_graph_v2.ainvoke(state_with_responses, {
        "recursion_limit": 25,
        "debug": False
    })


async def check_session_abandonment(session_state: dict) -> dict:
    """
    Entry point 3: Check for abandonment.
    Used by timeout/cron jobs
    """
    # Start from abandonment check node
    return await survey_graph_v2.ainvoke(session_state)