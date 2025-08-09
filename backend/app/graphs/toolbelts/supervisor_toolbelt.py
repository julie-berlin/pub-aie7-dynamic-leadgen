"""
Supervisor Nodes Tool Belt

Contains tools needed for supervisor nodes that coordinate other node functions.
"""

from ...tools import load_client_info
from ...models import get_chat_model


class SupervisorToolBelt:
    """Tool belt for supervisor nodes with client info loading and LLM access."""
    
    def __init__(self):
        self.load_client_info = load_client_info
        self.get_chat_model = get_chat_model
    
    def get_tools(self):
        """Get list of tools for this node."""
        return [self.load_client_info]
    
    def get_llm_model(self, **kwargs):
        """Get LLM model for supervision tasks."""
        return self.get_chat_model(**kwargs)


# Global instance
supervisor_toolbelt = SupervisorToolBelt()