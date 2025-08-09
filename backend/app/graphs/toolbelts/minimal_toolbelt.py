"""
Minimal Tool Belt

For nodes that don't require external tools - only internal operations.
"""


class MinimalToolBelt:
    """Tool belt for nodes that perform only internal state operations."""
    
    def __init__(self):
        pass
    
    def get_tools(self):
        """Get empty list of tools - no external tools needed."""
        return []


# Global instance
minimal_toolbelt = MinimalToolBelt()