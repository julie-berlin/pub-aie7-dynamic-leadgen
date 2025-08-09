"""
Pydantic Models for API Request/Response

Data models for session management and form interactions.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime

# Request Models
class SessionStartRequest(BaseModel):
    """Request to start a new lead session"""
    form_id: str = Field(..., description="Unique identifier for the form configuration")
    client_id: Optional[str] = Field(None, description="Optional client identifier")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional session metadata")

class SessionStepRequest(BaseModel):
    """Request to process a form step"""
    session_id: str = Field(..., description="Unique session identifier")
    responses: List[Dict[str, Any]] = Field(..., description="User responses for current step")

class SessionCompleteRequest(BaseModel):
    """Request to complete a session"""
    session_id: str = Field(..., description="Unique session identifier")
    final_responses: Optional[List[Dict[str, Any]]] = Field(default_factory=list, description="Any final responses")

# Response Models
class QuestionResponse(BaseModel):
    """Individual question for form step"""
    id: int = Field(..., description="Question ID")
    question: str = Field(..., description="Original question text")
    phrased_question: str = Field(..., description="AI-adapted question text")
    data_type: str = Field(..., description="Expected response data type")
    is_required: bool = Field(default=False, description="Whether question is required")

class SessionStepResponse(BaseModel):
    """Response for form step"""
    session_id: str = Field(..., description="Session identifier")
    step: int = Field(..., description="Current step number")
    headline: str = Field(..., description="Engaging step headline")
    motivation: str = Field(..., description="Motivational content")
    questions: List[QuestionResponse] = Field(..., description="Questions for this step")
    progress: Dict[str, Any] = Field(..., description="Progress information")

class SessionStatusResponse(BaseModel):
    """Session status and state"""
    session_id: str = Field(..., description="Session identifier")
    form_id: str = Field(..., description="Form configuration ID")
    step: int = Field(..., description="Current step number")
    completed: bool = Field(..., description="Whether session is completed")
    lead_status: Literal["unknown", "yes", "maybe", "no"] = Field(..., description="Current lead qualification status")
    score: int = Field(..., description="Current lead score (0-100)")
    responses_count: int = Field(..., description="Number of responses collected")
    started_at: datetime = Field(..., description="Session start timestamp")
    last_updated: datetime = Field(..., description="Last update timestamp")

class SessionCompletionResponse(BaseModel):
    """Final session completion response"""
    session_id: str = Field(..., description="Session identifier")
    lead_status: Literal["yes", "maybe", "no"] = Field(..., description="Final lead qualification")
    final_score: int = Field(..., description="Final lead score (0-100)")
    completion_message: str = Field(..., description="Personalized completion message")
    next_steps: List[str] = Field(..., description="Recommended next steps")
    completed_at: datetime = Field(..., description="Completion timestamp")

class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")