"""
Persistence Nodes Tool Belt

Contains only database-related tools for persistence operations.
"""

from ...tools import save_responses, update_session, finalize_session, create_session, save_tracking_data, save_response


class PersistenceToolBelt:
    """Tool belt for persistence nodes with database operation capabilities."""
    
    def __init__(self):
        self.save_responses = save_responses
        self.update_session = update_session
        self.finalize_session = finalize_session
        self.create_session = create_session
        self.save_tracking_data = save_tracking_data
        self.save_response = save_response
    
    def get_tools(self):
        """Get list of database tools for this node."""
        return [
            self.save_responses,
            self.update_session, 
            self.finalize_session,
            self.create_session,
            self.save_tracking_data,
            self.save_response
        ]


# Global instance
persistence_toolbelt = PersistenceToolBelt()