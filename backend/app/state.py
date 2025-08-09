"""Shared agent state definitions for LangGraph graphs."""
from __future__ import annotations
from typing import Annotated, TypedDict, List, Dict, Any, Optional, Literal
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """State schema for agent graphs, storing a message list with add_messages."""
    messages: Annotated[List, add_messages]

# Core shared state for basic survey information
class CoreSurveyState(TypedDict):
    """Core survey state shared across all supervisors."""
    session_id: str
    form_id: str
    client_id: Optional[str]
    started_at: str
    last_updated: str
    step: int
    completed: bool
    
    # UTM and tracking parameters
    utm_source: Optional[str]
    utm_medium: Optional[str]
    utm_campaign: Optional[str]
    utm_content: Optional[str]
    utm_term: Optional[str]
    referrer: Optional[str]
    user_agent: Optional[str]
    ip_address: Optional[str]
    landing_page: Optional[str]

# Master flow supervisor state
class MasterFlowState(TypedDict):
    """State for master flow supervisor coordination."""
    core: CoreSurveyState
    flow_phase: Literal["initializing", "questioning", "scoring", "completing"]
    completion_probability: float
    flow_strategy: str  # Current high-level strategy
    supervisor_consensus: Dict[str, Any]  # Consensus between supervisors
    coordination_messages: List[Dict[str, Any]]  # Inter-supervisor messages

# Question strategy supervisor state  
class QuestionStrategyState(TypedDict):
    """State for question selection and strategy."""
    all_questions: List[Dict[str, Any]]
    asked_questions: List[int]
    current_questions: List[Dict[str, Any]]
    phrased_questions: List[str]
    question_strategy: Dict[str, Any]  # Current strategy
    selection_history: List[Dict[str, Any]]  # Question selection decisions

# Lead intelligence supervisor state
class LeadIntelligenceState(TypedDict):
    """State for lead scoring and qualification."""
    responses: List[Dict[str, Any]]
    current_score: int
    score_history: List[Dict[str, Any]]
    lead_status: Literal["unknown", "yes", "maybe", "no"]
    qualification_reasoning: List[Dict[str, Any]]
    risk_factors: List[str]
    positive_indicators: List[str]

# Engagement supervisor state
class EngagementState(TypedDict):
    """State for user engagement and retention."""
    abandonment_risk: float
    engagement_metrics: Dict[str, Any]
    step_headline: str
    step_motivation: str
    engagement_history: List[Dict[str, Any]]
    retention_strategies: List[str]
    
    # Activity tracking
    last_activity_timestamp: Optional[str]
    abandonment_status: Literal["active", "at_risk", "high_risk", "abandoned"]
    time_on_step: Optional[float]  # seconds
    hesitation_indicators: int

# Main graph state that coordinates all supervisor states
class SurveyGraphState(TypedDict):
    """Main state for the survey graph that coordinates all supervisor states."""
    # Shared core state
    core: CoreSurveyState
    
    # Supervisor-specific states
    master_flow: MasterFlowState
    question_strategy: QuestionStrategyState  
    lead_intelligence: LeadIntelligenceState
    engagement: EngagementState
    
    # Cross-supervisor communication
    supervisor_messages: List[Dict[str, Any]]
    shared_context: Dict[str, Any]  # Minimal shared context
    
    # API interaction fields
    pending_responses: List[Dict[str, Any]]  # Responses waiting to be processed
    frontend_response: Optional[Dict[str, Any]]  # Data prepared for frontend
    
    # Session management
    session_recovery_data: Optional[Dict[str, Any]]  # For resuming sessions
    completion_message: Optional[str]  # Generated completion message
    
    # Error handling and logging
    error_log: List[Dict[str, Any]]
    operation_log: List[Dict[str, Any]]  # Track all operations
    
    # Metadata and tracking
    metadata: Dict[str, Any]  # Additional tracking data

# Legacy state for backward compatibility during transition
SurveyState = SurveyGraphState  # Alias for existing code
