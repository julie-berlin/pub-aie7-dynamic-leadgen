"""Survey Flow Graph with Hierarchical Supervisor Architecture.

Implements intelligent survey orchestration using supervisor agents:
- Master Flow Supervisor: Orchestrates overall flow and coordination
- Question Strategy Supervisor: Intelligent question selection and flow
- Lead Intelligence Supervisor: Advanced scoring and qualification
- Engagement Supervisor: Retention and abandonment prevention

Flow: Initialize → Coordinate → Select → Score → Engage → Continue/Complete
"""

from __future__ import annotations
from langgraph.graph import StateGraph, END

from ..state import SurveyGraphState
from .nodes.initialize_session_node import initialize_session_node
from .nodes.supervisor_integration_nodes import (
    master_flow_coordination_node,
    question_strategy_node,
    lead_intelligence_node,
    engagement_supervision_node,
    supervisor_coordination_node
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
    Build the supervisor-based survey flow graph.
    
    The flow follows this intelligent pattern:
    1. Initialize session
    2. Master flow coordination
    3. Parallel supervisor decisions (Question, Lead, Engagement)
    4. Supervisor coordination and context sharing
    5. Update state and persistence
    6. Continue or complete based on master decision
    
    Returns:
        Compiled StateGraph ready for execution
    """
    graph = StateGraph(SurveyGraphState)
    
    # Core initialization
    graph.add_node("initialize_session", initialize_session_node)
    
    # Supervisor nodes
    graph.add_node("master_coordination", master_flow_coordination_node)
    graph.add_node("question_strategy", question_strategy_node)
    graph.add_node("lead_intelligence", lead_intelligence_node)
    graph.add_node("engagement_supervision", engagement_supervision_node)
    graph.add_node("supervisor_coordination", supervisor_coordination_node)
    
    # State management nodes
    graph.add_node("update_step", update_step_node)
    
    # Database persistence nodes
    graph.add_node("save_responses", save_responses_node)
    graph.add_node("update_session", update_session_node)
    graph.add_node("save_completion", save_completion_node)
    
    # Completion flow nodes
    graph.add_node("message_generation", message_generation_node)
    graph.add_node("finalization", finalization_node)
    graph.add_node("completion", completion_node)
    
    # Set entry point
    graph.set_entry_point("initialize_session")
    
    # Initial flow to master coordination
    graph.add_edge("initialize_session", "master_coordination")
    
    # Master coordinates parallel supervisor execution
    graph.add_edge("master_coordination", "question_strategy")
    graph.add_edge("master_coordination", "lead_intelligence")
    graph.add_edge("master_coordination", "engagement_supervision")
    
    # All supervisors converge at coordination node
    graph.add_edge("question_strategy", "supervisor_coordination")
    graph.add_edge("lead_intelligence", "supervisor_coordination")
    graph.add_edge("engagement_supervision", "supervisor_coordination")
    
    # After coordination, update state
    graph.add_edge("supervisor_coordination", "update_step")
    graph.add_edge("update_step", "update_session")
    
    # Conditional routing based on master flow decision
    graph.add_conditional_edges(
        "update_session",
        should_continue_survey_with_supervisors,
        {
            "continue": "master_coordination",  # Loop back to supervisors
            "complete": "message_generation",   # Start completion flow
            END: END  # End graph (wait for user responses)
        }
    )
    
    # Completion flow
    graph.add_edge("message_generation", "save_completion")
    graph.add_edge("save_completion", "finalization")
    graph.add_edge("finalization", "completion")
    graph.add_edge("completion", END)
    
    return graph


def should_continue_survey_with_supervisors(state: SurveyGraphState) -> str:
    """
    Determine if survey should continue based on supervisor decisions.
    
    This routing function uses the master flow supervisor's decision
    along with business rules to determine next steps.
    """
    try:
        # Get master flow decision
        master_flow = state.get('master_flow', {})
        flow_strategy = master_flow.get('flow_strategy', 'CONTINUE')
        
        # Get core state for business rules
        core = state.get('core', {})
        step = core.get('step', 0)
        completed = core.get('completed', False)
        
        # Check if we have responses yet
        lead_intelligence = state.get('lead_intelligence', {})
        responses = lead_intelligence.get('responses', [])
        
        # If no responses yet, wait for user
        if not responses and step == 0:
            return END
        
        # Follow master supervisor decision
        if flow_strategy in ['COMPLETE', 'COMPLETION_PREP']:
            return "complete"
        elif flow_strategy in ['CONTINUE', 'ADAPT', 'RECOVER']:
            # Additional business rule checks
            if step >= 10:  # Max steps safety
                return "complete"
            if completed:
                return "complete"
            return "continue"
        else:
            return "continue"  # Default to continue
            
    except Exception as e:
        # On error, use simple business rules
        if state.get('core', {}).get('step', 0) >= 6:
            return "complete"
        return "continue"


# Export compiled graph for use
survey_graph = build_survey_graph().compile()