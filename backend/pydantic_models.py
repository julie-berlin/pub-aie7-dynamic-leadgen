"""
Consolidated Pydantic Models for Type Safety

All data models for the survey system including:
- API Request/Response models  
- State models for graph nodes
- Database models
- Internal data structures
"""

from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Dict, Any, Optional, Literal, Union
from datetime import datetime
from enum import Enum

# === ENUMS AND LITERALS ===

class LeadStatus(str, Enum):
    UNKNOWN = "unknown"
    YES = "yes" 
    MAYBE = "maybe"
    NO = "no"

class AbandonmentStatus(str, Enum):
    ACTIVE = "active"
    AT_RISK = "at_risk"
    HIGH_RISK = "high_risk"
    ABANDONED = "abandoned"

class CompletionType(str, Enum):
    QUALIFIED = "qualified"
    UNQUALIFIED = "unqualified"
    ABANDONED = "abandoned"
    QUALIFIED_FALLBACK = "qualified_fallback"
    UNQUALIFIED_ERROR = "unqualified_error"

class FlowPhase(str, Enum):
    INITIALIZATION = "initialization"
    QUESTIONING = "questioning" 
    QUALIFICATION = "qualification"
    COMPLETION = "completion"

class FlowStrategy(str, Enum):
    STANDARD = "STANDARD"
    RECOVERY = "RECOVERY"
    QUALIFIED_COMPLETION = "QUALIFIED_COMPLETION"
    ABANDONMENT_PREVENTION = "ABANDONMENT_PREVENTION"

# === API REQUEST MODELS ===

class StartSessionRequest(BaseModel):
    """Request to start a new survey session with UTM tracking."""
    form_id: str = Field(..., description="Form configuration identifier")
    client_id: Optional[str] = Field(None, description="Optional client identifier")
    
    # UTM Parameters
    utm_source: Optional[str] = Field(None, description="Marketing source (facebook, google, etc.)")
    utm_medium: Optional[str] = Field(None, description="Marketing medium (social, cpc, email)")
    utm_campaign: Optional[str] = Field(None, description="Campaign name")
    utm_content: Optional[str] = Field(None, description="Ad content identifier")
    utm_term: Optional[str] = Field(None, description="Search term")
    
    # Additional tracking
    landing_page: Optional[str] = Field(None, description="Landing page URL")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")

    @validator('form_id')
    def validate_form_id(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('form_id cannot be empty')
        return v.strip()

class SubmitResponsesRequest(BaseModel):
    """Request to submit survey responses for a step.
    
    Security Note: session_id is now obtained from HTTP-only cookie,
    not from request body. This prevents XSS session hijacking.
    """
    responses: List[Dict[str, Any]] = Field(..., description="User responses for current step")
    
    @validator('responses')
    def validate_responses(cls, v):
        if not isinstance(v, list):
            raise ValueError('responses must be a list')
        for response in v:
            if not isinstance(response, dict):
                raise ValueError('each response must be a dictionary')
            if 'question_id' not in response or 'answer' not in response:
                raise ValueError('each response must have question_id and answer')
        return v

class AbandonSessionRequest(BaseModel):
    """Request to mark a session as abandoned."""
    session_id: str = Field(..., description="Session identifier")
    reason: Optional[str] = Field(None, description="Abandonment reason")

# === API RESPONSE MODELS ===

class QuestionData(BaseModel):
    """Individual question data for frontend."""
    id: int = Field(..., description="Question ID within form")
    question: str = Field(..., description="Original question text") 
    phrased_question: str = Field(..., description="AI-adapted question text")
    data_type: str = Field(default="text", description="Expected response data type")
    is_required: bool = Field(default=False, description="Whether question is required")
    options: Optional[List[str]] = Field(None, description="Multiple choice options")
    scoring_rubric: Optional[str] = Field(None, description="Scoring criteria")

class StartSessionResponse(BaseModel):
    """Response for session initialization."""
    session_id: str = Field(..., description="Unique session identifier")
    questions: List[QuestionData] = Field(..., description="Initial questions")
    headline: str = Field(..., description="Engaging step headline")
    motivation: str = Field(..., description="Motivational content")
    step: int = Field(default=1, description="Current step number")
    progress: Dict[str, Any] = Field(default_factory=dict, description="Progress indicators")

class StepResponse(BaseModel):
    """Response for survey step progression."""
    session_id: str = Field(..., description="Session identifier")
    step: int = Field(..., description="Current step number")
    questions: List[QuestionData] = Field(..., description="Questions for this step")
    headline: str = Field(..., description="Engaging step headline")
    motivation: str = Field(..., description="Motivational content")
    progress: Dict[str, Any] = Field(default_factory=dict, description="Progress information")
    completed: bool = Field(default=False, description="Whether survey is complete")

class CompletionResponse(BaseModel):
    """Response for survey completion."""
    session_id: str = Field(..., description="Session identifier")
    lead_status: LeadStatus = Field(..., description="Final lead qualification")
    final_score: int = Field(..., description="Final lead score")
    completion_message: str = Field(..., description="Personalized completion message")
    completion_type: CompletionType = Field(..., description="Type of completion")
    completed_at: datetime = Field(..., description="Completion timestamp")

class SessionStatusResponse(BaseModel):
    """Response for session status inquiry."""
    session_id: str = Field(..., description="Session identifier")
    form_id: str = Field(..., description="Form configuration ID")
    step: int = Field(..., description="Current step number")
    completed: bool = Field(..., description="Whether session is completed")
    lead_status: LeadStatus = Field(..., description="Current lead qualification")
    current_score: int = Field(..., description="Current lead score")
    responses_count: int = Field(..., description="Number of responses collected")
    started_at: datetime = Field(..., description="Session start timestamp")
    last_updated: datetime = Field(..., description="Last update timestamp")
    abandonment_status: AbandonmentStatus = Field(..., description="Abandonment risk status")

class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")

# === STATE MODELS FOR GRAPH NODES ===

class CoreSurveyState(BaseModel):
    """Core survey state shared across all graph nodes."""
    session_id: str = Field(..., description="Unique session identifier")
    form_id: str = Field(..., description="Form configuration ID")
    client_id: Optional[str] = Field(None, description="Client ID")
    started_at: str = Field(..., description="Session start timestamp")
    last_updated: str = Field(..., description="Last update timestamp") 
    step: int = Field(default=0, description="Current step number")
    completed: bool = Field(default=False, description="Completion status")
    completion_type: Optional[CompletionType] = Field(None, description="Type of completion")
    completed_at: Optional[str] = Field(None, description="Completion timestamp")
    
    # UTM and tracking parameters
    utm_source: Optional[str] = Field(None, description="UTM source parameter")
    utm_medium: Optional[str] = Field(None, description="UTM medium parameter")
    utm_campaign: Optional[str] = Field(None, description="UTM campaign parameter")
    utm_content: Optional[str] = Field(None, description="UTM content parameter")
    utm_term: Optional[str] = Field(None, description="UTM term parameter")
    referrer: Optional[str] = Field(None, description="HTTP referrer")
    user_agent: Optional[str] = Field(None, description="User agent string")
    ip_address: Optional[str] = Field(None, description="Client IP address")
    landing_page: Optional[str] = Field(None, description="Landing page URL")

    class Config:
        use_enum_values = True

class MasterFlowState(BaseModel):
    """Master flow control state."""
    core: CoreSurveyState = Field(..., description="Core state reference")
    flow_phase: FlowPhase = Field(..., description="Current flow phase")
    completion_probability: float = Field(default=0.5, ge=0, le=1, description="Completion probability")
    flow_strategy: FlowStrategy = Field(..., description="Current flow strategy")

class QuestionDataInternal(BaseModel):
    """Internal question data structure for graph nodes."""
    question_id: int = Field(..., description="Question ID")
    question_text: str = Field(..., description="Original question text")
    phrased_question: Optional[str] = Field(None, description="AI-phrased version")
    data_type: str = Field(default="text", description="Response data type")
    is_required: bool = Field(default=False, description="Required flag")
    options: Optional[List[str]] = Field(None, description="Multiple choice options")
    scoring_rubric: Optional[str] = Field(None, description="Scoring criteria")
    category: Optional[str] = Field(None, description="Question category")

class QuestionStrategyState(BaseModel):
    """Question selection and management state."""
    all_questions: List[QuestionDataInternal] = Field(default_factory=list, description="All available questions")
    asked_questions: List[int] = Field(default_factory=list, description="Question IDs already asked")
    current_questions: List[QuestionDataInternal] = Field(default_factory=list, description="Current step questions")
    phrased_questions: List[QuestionDataInternal] = Field(default_factory=list, description="AI-phrased questions")
    question_strategy: Dict[str, Any] = Field(default_factory=dict, description="Selection strategy")
    selection_history: List[Dict[str, Any]] = Field(default_factory=list, description="Selection history")

class ResponseData(BaseModel):
    """Individual response data."""
    question_id: int = Field(..., description="Question ID")
    question_text: str = Field(..., description="Original question")
    phrased_question: Optional[str] = Field(None, description="Phrased question")
    answer: str = Field(..., description="User's answer")
    timestamp: str = Field(..., description="Response timestamp")
    step: int = Field(..., description="Step number when answered")
    data_type: str = Field(default="text", description="Data type")
    is_required: bool = Field(default=False, description="Required flag")
    scoring_rubric: Optional[str] = Field(None, description="Scoring criteria")
    score_awarded: int = Field(default=0, description="Points awarded")

class LeadIntelligenceState(BaseModel):
    """Lead scoring and qualification state."""
    responses: List[ResponseData] = Field(default_factory=list, description="All responses")
    current_score: int = Field(default=0, description="Current lead score")
    score_history: List[int] = Field(default_factory=list, description="Score progression")
    lead_status: LeadStatus = Field(default=LeadStatus.UNKNOWN, description="Lead qualification")
    qualification_reasoning: List[str] = Field(default_factory=list, description="Qualification logic")
    risk_factors: List[str] = Field(default_factory=list, description="Negative indicators")
    positive_indicators: List[str] = Field(default_factory=list, description="Positive indicators")

class EngagementState(BaseModel):
    """User engagement and abandonment tracking state."""
    abandonment_risk: float = Field(default=0.3, ge=0, le=1, description="Risk of abandonment (0-1)")
    engagement_metrics: Dict[str, Any] = Field(default_factory=dict, description="Engagement data")
    step_headline: str = Field(default="", description="Current step headline")
    step_motivation: str = Field(default="", description="Motivational text")
    engagement_history: List[Dict[str, Any]] = Field(default_factory=list, description="Engagement events")
    retention_strategies: List[str] = Field(default_factory=list, description="Applied strategies")
    last_activity_timestamp: str = Field(..., description="Last activity time")
    abandonment_status: AbandonmentStatus = Field(default=AbandonmentStatus.ACTIVE, description="Abandonment status")
    time_on_step: Optional[int] = Field(None, description="Seconds on current step")
    hesitation_indicators: int = Field(default=0, description="Hesitation count")

class OperationLogEntry(BaseModel):
    """Individual operation log entry."""
    operation: str = Field(..., description="Operation name")
    timestamp: str = Field(..., description="Operation timestamp")
    details: str = Field(default="", description="Operation details")
    step: Optional[int] = Field(None, description="Step number")

class SurveyGraphState(BaseModel):
    """Complete survey graph state - consolidates all sub-states."""
    # Hierarchical state components
    core: CoreSurveyState = Field(..., description="Core survey state")
    master_flow: MasterFlowState = Field(..., description="Master flow state")
    question_strategy: QuestionStrategyState = Field(..., description="Question strategy state")
    lead_intelligence: LeadIntelligenceState = Field(..., description="Lead intelligence state")
    engagement: EngagementState = Field(..., description="Engagement state")
    
    # Shared data
    supervisor_messages: List[str] = Field(default_factory=list, description="Inter-supervisor messages")
    shared_context: Dict[str, Any] = Field(default_factory=dict, description="Shared context data")
    
    # API interaction
    pending_responses: List[Dict[str, Any]] = Field(default_factory=list, description="Pending user responses")
    frontend_response: Optional[Dict[str, Any]] = Field(None, description="Response for frontend")
    
    # Routing control flags  
    route_to_lead_intelligence: Optional[bool] = Field(None, description="Flag to route to lead intelligence")
    check_abandonment: Optional[bool] = Field(None, description="Flag to check abandonment")
    route_decision: Optional[str] = Field(None, description="'continue' or 'end' - controls flow routing")
    
    # Completion
    completion_message: Optional[str] = Field(None, description="Final completion message")
    
    # Logging and debugging
    error_log: List[str] = Field(default_factory=list, description="Error messages")
    operation_log: List[OperationLogEntry] = Field(default_factory=list, description="Operation history")
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    session_recovery_data: Optional[Dict[str, Any]] = Field(None, description="Recovery information")

    class Config:
        use_enum_values = True
        
    @validator('core', 'master_flow', 'question_strategy', 'lead_intelligence', 'engagement')
    def validate_required_states(cls, v):
        if v is None:
            raise ValueError('Required state component cannot be None')
        return v

# === DATABASE MODELS ===

class ClientModel(BaseModel):
    """Client/business model."""
    id: Optional[str] = Field(None, description="Client UUID")
    name: str = Field(..., description="Client name")
    business_name: Optional[str] = Field(None, description="Business name")
    email: str = Field(..., description="Client email")
    owner_name: str = Field(..., description="Owner name")
    contact_name: Optional[str] = Field(None, description="Alternative contact")
    business_type: Optional[str] = Field(None, description="Business type")
    industry: Optional[str] = Field(None, description="Industry")
    address: Optional[str] = Field(None, description="Business address")
    phone: Optional[str] = Field(None, description="Phone number")
    website: Optional[str] = Field(None, description="Website URL")
    background: Optional[str] = Field(None, description="Business background")
    goals: Optional[str] = Field(None, description="Business goals")
    target_audience: Optional[str] = Field(None, description="Target audience")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Update timestamp")

class FormConfigModel(BaseModel):
    """Form configuration model."""
    id: Optional[str] = Field(None, description="Form UUID")
    client_id: str = Field(..., description="Client UUID")
    title: str = Field(..., description="Form title")
    description: Optional[str] = Field(None, description="Form description")
    lead_scoring_threshold_yes: int = Field(default=80, description="Yes threshold")
    lead_scoring_threshold_maybe: int = Field(default=50, description="Maybe threshold")
    max_questions: int = Field(default=8, description="Maximum questions")
    min_questions_before_fail: int = Field(default=4, description="Minimum before fail")
    completion_message_template: Optional[str] = Field(None, description="Message template")
    unqualified_message: str = Field(default="Thank you for your time.", description="Unqualified message")
    is_active: bool = Field(default=True, description="Active flag")
    settings: Dict[str, Any] = Field(default_factory=dict, description="Additional settings")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Update timestamp")

# === FORMS API MODELS ===

class FormQuestionConfig(BaseModel):
    """Configuration for a form question."""
    question_id: int
    question_order: int
    question_text: str
    question_type: str = Field(default="text")
    options: Optional[Dict[str, Any]] = None
    validation_rules: Optional[Dict[str, Any]] = None
    scoring_rubric: Optional[Dict[str, Any]] = None
    is_required: bool = Field(default=False)
    description: Optional[str] = None
    placeholder: Optional[str] = None

class FormCreateRequest(BaseModel):
    """Request to create a new form."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Literal["draft", "active", "paused", "archived"] = Field(default="draft")
    tags: Optional[List[str]] = Field(default_factory=list)
    theme_config: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    # Scoring configuration
    lead_scoring_threshold_yes: int = Field(default=80, ge=0, le=100)
    lead_scoring_threshold_maybe: int = Field(default=50, ge=0, le=100)
    
    # Business rules
    max_questions: int = Field(default=8, ge=1, le=20)
    min_questions_before_fail: int = Field(default=4, ge=1, le=10)
    
    # Templates
    completion_message_template: Optional[str] = None
    unqualified_message: str = Field(default="Thank you for your time.")
    
    # Additional settings
    settings: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    # Questions
    questions: Optional[List[FormQuestionConfig]] = Field(default_factory=list)

    @validator('lead_scoring_threshold_maybe')
    def validate_thresholds(cls, v, values):
        if 'lead_scoring_threshold_yes' in values and v >= values['lead_scoring_threshold_yes']:
            raise ValueError('Maybe threshold must be less than Yes threshold')
        return v

class FormUpdateRequest(BaseModel):
    """Request to update an existing form (PUT - full update)."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Literal["draft", "active", "paused", "archived"]
    tags: List[str] = Field(default_factory=list)
    theme_config: Dict[str, Any] = Field(default_factory=dict)
    
    # Scoring configuration
    lead_scoring_threshold_yes: int = Field(..., ge=0, le=100)
    lead_scoring_threshold_maybe: int = Field(..., ge=0, le=100)
    
    # Business rules
    max_questions: int = Field(..., ge=1, le=20)
    min_questions_before_fail: int = Field(..., ge=1, le=10)
    
    # Templates
    completion_message_template: Optional[str] = None
    unqualified_message: str
    
    # Additional settings
    settings: Dict[str, Any] = Field(default_factory=dict)

    @validator('lead_scoring_threshold_maybe')
    def validate_thresholds(cls, v, values):
        if 'lead_scoring_threshold_yes' in values and v >= values['lead_scoring_threshold_yes']:
            raise ValueError('Maybe threshold must be less than Yes threshold')
        return v

class FormPatchRequest(BaseModel):
    """Request to partially update a form (PATCH)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[Literal["draft", "active", "paused", "archived"]] = None
    tags: Optional[List[str]] = None
    theme_config: Optional[Dict[str, Any]] = None
    
    # Scoring configuration
    lead_scoring_threshold_yes: Optional[int] = Field(None, ge=0, le=100)
    lead_scoring_threshold_maybe: Optional[int] = Field(None, ge=0, le=100)
    
    # Business rules
    max_questions: Optional[int] = Field(None, ge=1, le=20)
    min_questions_before_fail: Optional[int] = Field(None, ge=1, le=10)
    
    # Templates
    completion_message_template: Optional[str] = None
    unqualified_message: Optional[str] = None
    
    # Additional settings
    settings: Optional[Dict[str, Any]] = None

class FormResponse(BaseModel):
    """Response model for form data."""
    id: str
    client_id: str
    title: str
    description: Optional[str]
    status: str
    tags: List[str]
    theme_config: Dict[str, Any]
    
    # Scoring configuration
    lead_scoring_threshold_yes: int
    lead_scoring_threshold_maybe: int
    
    # Business rules
    max_questions: int
    min_questions_before_fail: int
    
    # Templates
    completion_message_template: Optional[str]
    unqualified_message: str
    
    # Additional settings
    settings: Dict[str, Any]
    is_active: bool
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    # Statistics (calculated fields)
    total_responses: int = 0
    conversion_rate: float = 0.0
    average_completion_time: int = 0  # seconds
    
    # Questions
    questions: List[FormQuestionConfig] = []

class FormListResponse(BaseModel):
    """Response model for form list with pagination."""
    forms: List[FormResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int

# === CLIENTS API MODELS ===

class ClientUpdateRequest(BaseModel):
    """Request to update client information (PUT - full update)."""
    business_name: str = Field(..., min_length=1, max_length=200)
    business_description: str = Field(..., max_length=1000)
    industry: str = Field(..., max_length=100)
    website_url: Optional[str] = None
    contact_email: str = Field(...)
    contact_phone: Optional[str] = Field(None, max_length=20)
    business_address: Optional[str] = Field(None, max_length=500)
    business_type: Optional[str] = Field(None, max_length=100)
    target_audience: Optional[str] = Field(None, max_length=500)
    goals: Optional[str] = Field(None, max_length=1000)

class ClientPatchRequest(BaseModel):
    """Request to partially update client information (PATCH)."""
    business_name: Optional[str] = Field(None, min_length=1, max_length=200)
    business_description: Optional[str] = Field(None, max_length=1000)
    industry: Optional[str] = Field(None, max_length=100)
    website_url: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = Field(None, max_length=20)
    business_address: Optional[str] = Field(None, max_length=500)
    business_type: Optional[str] = Field(None, max_length=100)
    target_audience: Optional[str] = Field(None, max_length=500)
    goals: Optional[str] = Field(None, max_length=1000)

class ClientResponse(BaseModel):
    """Response model for client data."""
    id: str
    name: str
    business_name: Optional[str]
    email: str
    owner_name: str
    contact_name: Optional[str]
    business_type: Optional[str]
    industry: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    background: Optional[str]
    goals: Optional[str]
    target_audience: Optional[str]
    created_at: datetime
    updated_at: datetime

# === THEMES API MODELS ===

class ThemeCreateRequest(BaseModel):
    """Request to create a new theme."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    primary_color: str = Field(..., pattern=r'^#[0-9A-Fa-f]{6}$')
    secondary_color: str = Field(..., pattern=r'^#[0-9A-Fa-f]{6}$')
    accent_color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    font_family: Optional[str] = Field(None, max_length=100)
    custom_css: Optional[str] = Field(None, max_length=10000)
    settings: Optional[Dict[str, Any]] = Field(default_factory=dict)

class ThemeUpdateRequest(BaseModel):
    """Request to update a theme (PUT - full update)."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    primary_color: str = Field(..., pattern=r'^#[0-9A-Fa-f]{6}$')
    secondary_color: str = Field(..., pattern=r'^#[0-9A-Fa-f]{6}$')
    accent_color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    font_family: Optional[str] = Field(None, max_length=100)
    custom_css: Optional[str] = Field(None, max_length=10000)
    settings: Dict[str, Any] = Field(default_factory=dict)

class ThemePatchRequest(BaseModel):
    """Request to partially update a theme (PATCH)."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    primary_color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    secondary_color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    accent_color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    font_family: Optional[str] = Field(None, max_length=100)
    custom_css: Optional[str] = Field(None, max_length=10000)
    settings: Optional[Dict[str, Any]] = None

class ThemeResponse(BaseModel):
    """Response model for theme data."""
    id: str
    client_id: str
    name: str
    description: Optional[str]
    primary_color: str
    secondary_color: str
    accent_color: Optional[str]
    font_family: Optional[str]
    custom_css: Optional[str]
    settings: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime

class ThemeListResponse(BaseModel):
    """Response model for theme list."""
    themes: List[ThemeResponse]
    total_count: int

# === UTILITY FUNCTIONS ===

def create_initial_state(
    session_id: str,
    form_id: str,
    client_id: Optional[str] = None,
    utm_data: Optional[Dict[str, Any]] = None
) -> SurveyGraphState:
    """Create initial survey graph state with proper defaults."""
    current_time = datetime.now().isoformat()
    
    core_state = CoreSurveyState(
        session_id=session_id,
        form_id=form_id,
        client_id=client_id,
        started_at=current_time,
        last_updated=current_time,
        **(utm_data or {})
    )
    
    master_flow = MasterFlowState(
        core=core_state,
        flow_phase=FlowPhase.INITIALIZATION,
        flow_strategy=FlowStrategy.STANDARD
    )
    
    engagement_state = EngagementState(
        last_activity_timestamp=current_time
    )
    
    return SurveyGraphState(
        core=core_state,
        master_flow=master_flow,
        question_strategy=QuestionStrategyState(),
        lead_intelligence=LeadIntelligenceState(),
        engagement=engagement_state
    )