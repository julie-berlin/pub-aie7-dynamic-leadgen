"""Base supervisor class for LangGraph agents."""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class SupervisorDecision:
    """Structured decision from a supervisor."""
    decision: str
    reasoning: str
    confidence: float
    recommendations: List[str]
    metadata: Dict[str, Any]

class SupervisorAgent:
    """Base class for supervisor agents."""
    
    def __init__(
        self,
        name: str,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
        timeout_seconds: int = 30,
        **kwargs
    ):
        self.name = name
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout_seconds = timeout_seconds
        self.llm = None
        
    def get_system_prompt(self) -> str:
        """Get the system prompt for this supervisor."""
        raise NotImplementedError("Subclasses must implement get_system_prompt")
    
    def make_decision(self, state: Dict[str, Any], context: Dict[str, Any] = None) -> SupervisorDecision:
        """Make a strategic decision based on current state."""
        raise NotImplementedError("Subclasses must implement make_decision")