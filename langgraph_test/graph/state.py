"""State definitions for standalone survey graph testing."""

from typing import TypedDict, List, Dict, Any, Optional, Literal

class CoreSurveyState(TypedDict):
    """Core survey state information."""
    session_id: str
    form_id: str
    client_id: Optional[str]
    started_at: str
    last_updated: str
    step: int
    completed: bool
    
class QuestionStrategyState(TypedDict):
    """State for question selection and strategy."""
    all_questions: List[Dict[str, Any]]
    asked_questions: List[int]
    current_questions: List[Dict[str, Any]]
    phrased_questions: List[str]
    question_strategy: Dict[str, Any]
    selection_history: List[Dict[str, Any]]

class LeadIntelligenceState(TypedDict):
    """State for lead scoring and qualification."""
    responses: List[Dict[str, Any]]
    current_score: int
    score_history: List[Dict[str, Any]]
    lead_status: Literal["unknown", "yes", "maybe", "no", "continue"]
    qualification_reasoning: List[Dict[str, Any]]
    risk_factors: List[str]
    positive_indicators: List[str]

class SurveyState(TypedDict):
    """Main state for the survey graph."""
    # Core state
    core: CoreSurveyState
    
    # Strategy states
    question_strategy: QuestionStrategyState
    lead_intelligence: LeadIntelligenceState
    
    # Workflow control
    pending_responses: List[Dict[str, Any]]
    frontend_response: Optional[Dict[str, Any]]
    
    # Routing flags
    route_to_lead_intelligence: Optional[bool]
    check_abandonment: Optional[bool]
    
    # Results
    lead_status: Optional[str]
    completed: Optional[bool]
    completion_message: Optional[str]
    step_type: Optional[str]
    
    # Tool results
    tool_results: Optional[Dict[str, Any]]
    tool_score_boost: Optional[int]
    
    # Metadata
    error_log: List[Dict[str, Any]]
    operation_log: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    
    # Timing
    timing_data: Optional[Dict[str, Any]]
    abandonment_info: Optional[Dict[str, Any]]