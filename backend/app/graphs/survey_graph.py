"""Survey Flow Graph for LangGraph.

Main survey orchestration graph that implements the complete adaptive form flow:
Question Selection → Phrasing → Engagement → Present Step → Score → Continue/Complete

This replaces the FlowEngine with a proper LangGraph implementation.
"""

from __future__ import annotations
from langgraph.graph import StateGraph, END

from ..state import SurveyState
from .nodes.initialize_session_node import initialize_session_node
from .nodes.supervisor_nodes import (
    select_questions_node,
    phrase_questions_node, 
    create_engagement_node,
    score_lead_node
)
from .nodes.update_step_node import update_step_node
from .nodes.persistence_nodes import (
    save_responses_node,
    update_session_node,
    save_completion_node
)
from .nodes.completion_nodes import (
    message_generation_node,
    finalization_node,
    completion_node
)
from .nodes.routing_logic import should_continue_survey


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
    
    # Add database persistence nodes
    graph.add_node("save_responses", save_responses_node)
    graph.add_node("update_session", update_session_node)
    graph.add_node("save_completion", save_completion_node)
    
    # Add completion flow nodes
    graph.add_node("message_generation", message_generation_node)
    graph.add_node("finalization", finalization_node)
    graph.add_node("completion", completion_node)
    
    # Set entry point
    graph.set_entry_point("initialize_session")
    
    # Add edges for the main flow
    graph.add_edge("initialize_session", "select_questions")
    graph.add_edge("select_questions", "phrase_questions")
    graph.add_edge("phrase_questions", "create_engagement")
    graph.add_edge("create_engagement", "update_step")
    graph.add_edge("update_step", "update_session")  # Save session state after each step
    graph.add_edge("update_session", "score_lead")
    
    # Add conditional routing after scoring
    graph.add_conditional_edges(
        "score_lead",
        should_continue_survey,
        {
            "continue": "select_questions",  # Loop back to select more questions
            "complete": "message_generation",  # Start completion flow
            END: END  # End graph (wait for user responses)
        }
    )
    
    # Completion flow with message generation and finalization
    graph.add_edge("message_generation", "save_completion")
    graph.add_edge("save_completion", "finalization")
    graph.add_edge("finalization", "completion")
    graph.add_edge("completion", END)
    
    return graph


# Export compiled graph for use
survey_graph = build_survey_graph().compile()