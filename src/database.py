"""
Database utilities for Supabase integration
"""
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SupabaseClient:
    """Wrapper for Supabase operations"""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.anon_key = os.getenv("SUPABASE_ANON_KEY")
        self.service_key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not all([self.url, self.anon_key, self.service_key]):
            raise ValueError("Missing Supabase environment variables")
        
        # Use service key for backend operations
        self.client: Client = create_client(self.url, self.service_key)
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            # Test with a simple query that should always work
            result = self.client.table("clients").select("count", count="exact").execute()
            return True
        except Exception as e:
            error_str = str(e)
            if "Legacy API keys are disabled" in error_str:
                print("🔐 Legacy API keys are disabled. Please get new publishable/secret keys from your Supabase dashboard.")
                print("   Go to: Settings → API → Get new publishable and secret keys")
            elif "does not exist" in error_str or "relation" in error_str:
                print("🔧 Database connection works, but tables don't exist yet.")
                print("   Run the database_schema_fixed.sql file in your Supabase SQL Editor first.")
                return False
            else:
                print(f"Connection test failed: {e}")
            return False
    
    # === Client Management ===
    
    def create_client_record(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new client record"""
        result = self.client.table("clients").insert(client_data).execute()
        return result.data[0] if result.data else {}
    
    def get_client(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get client by ID"""
        result = self.client.table("clients").select("*").eq("id", client_id).execute()
        return result.data[0] if result.data else None
    
    # === Form Management ===
    
    def create_form(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new form configuration"""
        result = self.client.table("forms").insert(form_data).execute()
        return result.data[0] if result.data else {}
    
    def get_form(self, form_id: str) -> Optional[Dict[str, Any]]:
        """Get form configuration by ID"""
        result = self.client.table("forms").select("*").eq("id", form_id).execute()
        return result.data[0] if result.data else None
    
    # === Lead Session Management ===
    
    def create_lead_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new lead session"""
        result = self.client.table("lead_sessions").insert(session_data).execute()
        return result.data[0] if result.data else {}
    
    def update_lead_session(self, session_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update lead session"""
        result = self.client.table("lead_sessions").update(updates).eq("session_id", session_id).execute()
        return result.data[0] if result.data else {}
    
    def get_lead_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get lead session by ID"""
        result = self.client.table("lead_sessions").select("*").eq("session_id", session_id).execute()
        return result.data[0] if result.data else None
    
    # === Response Management ===
    
    def create_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new response record"""
        result = self.client.table("responses").insert(response_data).execute()
        return result.data[0] if result.data else {}
    
    def get_session_responses(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all responses for a session"""
        result = self.client.table("responses").select("*").eq("session_id", session_id).order("timestamp").execute()
        return result.data or []
    
    # === Lead Outcome Management ===
    
    def create_lead_outcome(self, outcome_data: Dict[str, Any]) -> Dict[str, Any]:
        """Record lead conversion outcome"""
        result = self.client.table("lead_outcomes").insert(outcome_data).execute()
        return result.data[0] if result.data else {}
    
    def get_historical_outcomes(self, form_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get historical conversion data for ML learning"""
        query = self.client.table("lead_outcomes").select("*")
        if form_id:
            query = query.eq("form_id", form_id)
        result = query.execute()
        return result.data or []

# Singleton instance
db = SupabaseClient()