"""
Update Step Node for LangGraph Survey Flow

Handles step counter and timestamp updates.
"""

from __future__ import annotations
from typing import Dict, Any
from datetime import datetime

from ...state import SurveyState
from ..toolbelts.minimal_toolbelt import minimal_toolbelt


def update_step_node(state: SurveyState) -> Dict[str, Any]:
    """
    Update step counter and last_updated timestamp.
    
    Args:
        state: Current SurveyState
        
    Returns:
        Dict with step and last_updated updates
    """
    return {
        'step': state.get('step', 0) + 1,
        'last_updated': datetime.now().isoformat()
    }