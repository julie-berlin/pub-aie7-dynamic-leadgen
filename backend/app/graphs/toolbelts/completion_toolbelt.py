"""
Completion Nodes Tool Belt

Contains tools needed for completion message generation and finalization.
"""

from ...tools import load_client_info
from ...models import get_chat_model


class CompletionToolBelt:
    """Tool belt for completion nodes with client info and LLM capabilities."""
    
    def __init__(self):
        self.load_client_info = load_client_info
        self.get_chat_model = get_chat_model
    
    def get_tools(self):
        """Get list of tools for this node."""
        return [self.load_client_info]
    
    def get_llm_model(self, **kwargs):
        """Get LLM model for message generation."""
        return self.get_chat_model(**kwargs)


# Global instance
completion_toolbelt = CompletionToolBelt()