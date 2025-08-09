"""
Pydantic Validation Helpers for Graph Nodes

Helper functions that demonstrate proper Pydantic validation
for graph node inputs and outputs while maintaining LangGraph compatibility.
"""

from typing import Dict, Any, List, Optional, Union
import logging
from datetime import datetime

from .pydantic_models import (
    SurveyGraphState,
    ResponseData,
    OperationLogEntry,
    QuestionDataInternal,
    CoreSurveyState,
    LeadStatus,
    AbandonmentStatus
)

logger = logging.getLogger(__name__)


def validate_and_extract_state(raw_state: Dict[str, Any]) -> tuple[Optional[SurveyGraphState], Dict[str, Any]]:
    """
    Validate raw state dictionary with Pydantic models.
    
    Returns:
        Tuple of (validated_pydantic_state, raw_dict_state)
        If validation fails, pydantic_state will be None but raw_dict_state is preserved.
    """
    try:
        validated_state = SurveyGraphState(**raw_state)
        return validated_state, raw_state
    except Exception as e:
        logger.warning(f"Pydantic validation failed: {e}")
        return None, raw_state


def validate_responses(raw_responses: List[Dict[str, Any]]) -> List[ResponseData]:
    """
    Validate and convert raw response dictionaries to Pydantic ResponseData models.
    
    Args:
        raw_responses: List of raw response dictionaries
        
    Returns:
        List of validated ResponseData objects
    """
    validated_responses = []
    
    for i, response in enumerate(raw_responses):
        try:
            # Add required fields if missing
            if 'timestamp' not in response:
                response['timestamp'] = datetime.now().isoformat()
            if 'step' not in response:
                response['step'] = 1  # Default step
                
            # Validate with Pydantic
            validated_response = ResponseData(**response)
            validated_responses.append(validated_response)
            
        except Exception as e:
            logger.error(f"Response {i} validation failed: {e}")
            # Continue processing other responses even if one fails
            continue
    
    return validated_responses


def create_operation_log_entry(operation: str, details: str = "", step: Optional[int] = None) -> OperationLogEntry:
    """
    Create a validated operation log entry.
    
    Args:
        operation: Operation name
        details: Operation details
        step: Optional step number
        
    Returns:
        Validated OperationLogEntry
    """
    return OperationLogEntry(
        operation=operation,
        timestamp=datetime.now().isoformat(),
        details=details,
        step=step
    )


def safe_state_update(current_state: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Safely update state dictionary while maintaining Pydantic compatibility.
    
    Args:
        current_state: Current state dictionary
        updates: Updates to apply
        
    Returns:
        Updated state dictionary
    """
    # Deep copy to avoid modifying original
    new_state = current_state.copy()
    
    # Apply updates
    for key, value in updates.items():
        if key in new_state and isinstance(new_state[key], dict) and isinstance(value, dict):
            # Merge dictionaries
            new_state[key] = {**new_state[key], **value}
        else:
            # Direct assignment
            new_state[key] = value
    
    # Attempt validation (optional - log warnings if fails)
    try:
        SurveyGraphState(**new_state)
        logger.debug("State update validation passed")
    except Exception as e:
        logger.warning(f"State update validation failed but continuing: {e}")
    
    return new_state


def extract_api_response_data(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract and validate data for API responses.
    
    Args:
        state: Raw state dictionary
        
    Returns:
        Dictionary suitable for API response models
    """
    validated_state, _ = validate_and_extract_state(state)
    
    if validated_state:
        # Use validated Pydantic models
        return {
            'session_id': validated_state.core.session_id,
            'step': validated_state.core.step,
            'completed': validated_state.core.completed,
            'lead_status': validated_state.lead_intelligence.lead_status.value,
            'current_score': validated_state.lead_intelligence.current_score,
            'abandonment_status': validated_state.engagement.abandonment_status.value,
            'abandonment_risk': validated_state.engagement.abandonment_risk,
            'headline': validated_state.engagement.step_headline,
            'motivation': validated_state.engagement.step_motivation
        }
    else:
        # Fallback to raw dictionary access
        core = state.get('core', {})
        lead_intel = state.get('lead_intelligence', {})
        engagement = state.get('engagement', {})
        
        return {
            'session_id': core.get('session_id', ''),
            'step': core.get('step', 0),
            'completed': core.get('completed', False),
            'lead_status': lead_intel.get('lead_status', 'unknown'),
            'current_score': lead_intel.get('current_score', 0),
            'abandonment_status': engagement.get('abandonment_status', 'active'),
            'abandonment_risk': engagement.get('abandonment_risk', 0.3),
            'headline': engagement.get('step_headline', ''),
            'motivation': engagement.get('step_motivation', '')
        }


# Decorator for graph nodes to add validation
def validate_node_io(func):
    """
    Decorator to add Pydantic validation to graph node functions.
    
    Usage:
        @validate_node_io
        def my_node(state: Dict[str, Any]) -> Dict[str, Any]:
            # Node implementation
            return updated_state
    """
    def wrapper(state: Dict[str, Any]) -> Dict[str, Any]:
        # Log input validation
        validated_input, _ = validate_and_extract_state(state)
        if validated_input:
            logger.debug(f"Node {func.__name__}: Input validation passed")
        else:
            logger.warning(f"Node {func.__name__}: Input validation failed")
        
        # Execute the actual node function
        result = func(state)
        
        # Log output validation
        validated_output, _ = validate_and_extract_state(result)
        if validated_output:
            logger.debug(f"Node {func.__name__}: Output validation passed")
        else:
            logger.warning(f"Node {func.__name__}: Output validation failed")
        
        return result
    
    return wrapper


# Example usage in a graph node:
@validate_node_io
def example_validated_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Example graph node showing proper Pydantic integration.
    """
    # Extract and validate state
    validated_state, raw_state = validate_and_extract_state(state)
    
    if validated_state:
        # Use type-safe Pydantic models
        session_id = validated_state.core.session_id
        current_score = validated_state.lead_intelligence.current_score
        
        # Create new operation log entry
        log_entry = create_operation_log_entry(
            operation="example_operation",
            details=f"Processed session {session_id}",
            step=validated_state.core.step
        )
        
        # Create safe state update
        updates = {
            'lead_intelligence': {'current_score': current_score + 10},
            'operation_log': validated_state.operation_log + [log_entry.model_dump()]
        }
        
        return safe_state_update(raw_state, updates)
    
    else:
        # Fallback to raw dictionary access
        logger.warning("Using raw dictionary access due to validation failure")
        return {
            **raw_state,
            'operation_log': raw_state.get('operation_log', []) + [{
                'operation': 'example_operation_fallback',
                'timestamp': datetime.now().isoformat(),
                'details': 'Used fallback due to validation failure'
            }]
        }