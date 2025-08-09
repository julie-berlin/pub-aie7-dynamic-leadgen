"""Shared agent state definitions for LangGraph graphs."""
from __future__ import annotations
from typing import Annotated, TypedDict, List, Dict, Any, Optional, Literal
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """State schema for agent graphs, storing a message list with add_messages."""
    messages: Annotated[List, add_messages]

class SurveyState(TypedDict):
    """State schema for survey flow graphs, containing all session and flow data."""
    # Core session identifiers
    session_id: str
    form_id: str
    client_id: Optional[str]
    
    # Timestamps
    started_at: str  # ISO datetime string
    last_updated: str  # ISO datetime string
    
    # Flow control
    step: int
    completed: bool
    
    # Questions and responses
    all_questions: List[Dict[str, Any]]  # Complete question bank
    asked_questions: List[int]  # List of question IDs already asked
    current_step_questions: List[Dict[str, Any]]  # Questions for current step
    phrased_questions: List[str]  # LLM-adapted question text for current step
    responses: List[Dict[str, Any]]  # Complete response history
    
    # Lead scoring and qualification
    score: int  # Lead score (0-100)
    lead_status: Literal["unknown", "yes", "maybe", "no"]  # Qualification status
    min_questions_met: bool  # Whether minimum 4 questions have been asked
    failed_required: bool  # Whether user failed critical required questions
    
    # Engagement content
    step_headline: str  # AI-generated engaging headline for current step
    step_motivation: str  # AI-generated motivational text for current step
    
    # Additional metadata
    metadata: Dict[str, Any]  # Additional session metadata
