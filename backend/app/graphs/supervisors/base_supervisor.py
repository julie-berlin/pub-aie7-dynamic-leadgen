"""Base supervisor agent class with LLM integration and tool calling."""

from __future__ import annotations
from typing import Dict, Any, List, Optional, Type, Union
from abc import ABC, abstractmethod
import json
import logging
from datetime import datetime

from ...models import get_chat_model
from ...state import SurveyState
from ..toolbelts.supervisor_toolbelt import supervisor_toolbelt

logger = logging.getLogger(__name__)


class SupervisorDecision:
    """Represents a decision made by a supervisor with reasoning and confidence."""
    
    def __init__(
        self,
        decision: str,
        reasoning: str,
        confidence: float,
        recommendations: List[str] = None,
        metadata: Dict[str, Any] = None
    ):
        self.decision = decision
        self.reasoning = reasoning
        self.confidence = confidence  # 0.0 to 1.0
        self.recommendations = recommendations or []
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow().isoformat()
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision": self.decision,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "recommendations": self.recommendations,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }


class SupervisorAgent(ABC):
    """Base class for all supervisor agents with LLM integration and tool calling."""
    
    def __init__(
        self, 
        name: str,
        model_name: str = "gpt-4o-mini",
        temperature: float = 0.1,
        max_tokens: int = 1000,
        timeout_seconds: int = 30
    ):
        self.name = name
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout_seconds = timeout_seconds
        
        # Initialize LLM model
        self.model = get_chat_model(
            model_name=model_name,
            temperature=temperature
        )
        
        # Decision history for this supervisor
        self.decision_history: List[SupervisorDecision] = []
        
        logger.info(f"Initialized {name} supervisor with model {model_name}")
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this supervisor."""
        pass
    
    @abstractmethod
    def make_decision(self, state: SurveyState, context: Dict[str, Any] = None) -> SupervisorDecision:
        """Make a decision based on the current state and context."""
        pass
    
    def invoke_llm(
        self, 
        messages: List[Dict[str, str]], 
        tools: List[Any] = None,
        **kwargs
    ) -> Union[str, Dict[str, Any]]:
        """Invoke the LLM with proper error handling and logging."""
        try:
            # Add system message if not present
            if not messages or messages[0].get("role") != "system":
                system_message = {"role": "system", "content": self.get_system_prompt()}
                messages = [system_message] + messages
            
            logger.debug(f"{self.name}: Invoking LLM with {len(messages)} messages")
            
            # Configure model parameters
            model_kwargs = {
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                **kwargs
            }
            
            # Bind tools if provided
            if tools:
                model = self.model.bind_tools(tools)
            else:
                model = self.model
            
            # Invoke model
            response = model.invoke(messages, **model_kwargs)
            
            # Extract content
            if hasattr(response, 'content'):
                content = response.content
            else:
                content = str(response)
            
            logger.debug(f"{self.name}: LLM response received ({len(content)} chars)")
            return content
            
        except Exception as e:
            logger.error(f"{self.name}: LLM invocation failed: {e}")
            raise SupervisorError(f"LLM invocation failed for {self.name}", e)
    
    def load_client_info(self, form_id: str) -> Dict[str, Any]:
        """Load client information for contextualization."""
        try:
            client_json = supervisor_toolbelt.load_client_info.invoke({"form_id": form_id})
            return json.loads(client_json) if client_json else {}
        except Exception as e:
            logger.warning(f"{self.name}: Failed to load client info for {form_id}: {e}")
            return {}
    
    def get_context_summary(self, state: SurveyState) -> str:
        """Generate a context summary for LLM prompting."""
        responses = state.get('responses', [])
        asked_questions = state.get('asked_questions', [])
        score = state.get('score', 0)
        lead_status = state.get('lead_status', 'unknown')
        step = state.get('step', 0)
        
        context_parts = [
            f"Survey Step: {step + 1}",
            f"Questions Asked: {len(asked_questions)}",
            f"Responses Collected: {len(responses)}",
            f"Current Lead Score: {score}",
            f"Lead Status: {lead_status}"
        ]
        
        if responses:
            context_parts.append("Recent Responses:")
            for i, response in enumerate(responses[-3:], 1):  # Last 3 responses
                answer = response.get('answer', 'No answer')
                context_parts.append(f"  {i}. {answer[:100]}..." if len(answer) > 100 else f"  {i}. {answer}")
        
        return "\n".join(context_parts)
    
    def record_decision(self, decision: SupervisorDecision):
        """Record a decision in the supervisor's history."""
        self.decision_history.append(decision)
        logger.info(f"{self.name}: Decision recorded - {decision.decision} (confidence: {decision.confidence:.2f})")
    
    def get_recent_decisions(self, limit: int = 5) -> List[SupervisorDecision]:
        """Get the most recent decisions made by this supervisor."""
        return self.decision_history[-limit:] if self.decision_history else []
    
    def create_decision(
        self,
        decision: str,
        reasoning: str,
        confidence: float = 0.8,
        recommendations: List[str] = None,
        metadata: Dict[str, Any] = None
    ) -> SupervisorDecision:
        """Helper to create and record a supervisor decision."""
        decision_obj = SupervisorDecision(
            decision=decision,
            reasoning=reasoning,
            confidence=confidence,
            recommendations=recommendations or [],
            metadata=metadata or {}
        )
        self.record_decision(decision_obj)
        return decision_obj
    
    def handle_error(self, error: Exception, context: str = "") -> SupervisorDecision:
        """Handle errors with fallback decision making."""
        error_msg = f"{self.name} error in {context}: {str(error)}"
        logger.error(error_msg)
        
        return self.create_decision(
            decision="fallback",
            reasoning=f"Error occurred, using fallback strategy: {error_msg}",
            confidence=0.3,
            metadata={"error": str(error), "context": context}
        )
    
    def validate_state(self, state: SurveyState) -> bool:
        """Validate that the state has required fields for this supervisor."""
        required_fields = ['session_id', 'form_id', 'step']
        
        for field in required_fields:
            if field not in state:
                logger.warning(f"{self.name}: Missing required state field: {field}")
                return False
        
        return True
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', model='{self.model_name}')"


class SupervisorError(Exception):
    """Exception raised by supervisor agents."""
    
    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(message)


class SupervisorCoordinator:
    """Coordinates communication between multiple supervisor agents."""
    
    def __init__(self):
        self.supervisors: Dict[str, SupervisorAgent] = {}
        self.message_log: List[Dict[str, Any]] = []
        
    def register_supervisor(self, supervisor: SupervisorAgent):
        """Register a supervisor with the coordinator."""
        self.supervisors[supervisor.name] = supervisor
        logger.info(f"Registered supervisor: {supervisor.name}")
    
    def send_message(self, from_supervisor: str, to_supervisor: str, message: Dict[str, Any]):
        """Send a message between supervisors."""
        message_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "from": from_supervisor,
            "to": to_supervisor,
            "message": message
        }
        self.message_log.append(message_record)
        logger.debug(f"Message sent from {from_supervisor} to {to_supervisor}")
    
    def get_supervisor(self, name: str) -> Optional[SupervisorAgent]:
        """Get a supervisor by name."""
        return self.supervisors.get(name)
    
    def get_coordination_context(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent coordination messages for context."""
        return self.message_log[-limit:] if self.message_log else []
