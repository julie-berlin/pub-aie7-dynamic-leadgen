"""
Initialize Session Tool Belt

Contains only the tools needed for session initialization.
"""

from ...tools import load_questions


class InitializeToolBelt:
    """Tool belt for initialize_session_node with question loading capabilities."""
    
    def __init__(self):
        self.load_questions = load_questions
    
    def get_tools(self):
        """Get list of tools for this node."""
        return [self.load_questions]


# Global instance
initialize_toolbelt = InitializeToolBelt()