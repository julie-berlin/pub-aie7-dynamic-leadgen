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
        self.publishable_key = os.getenv("SUPABASE_PUBLISHABLE_KEY")
        self.secret_key = os.getenv("SUPABASE_SECRET_KEY")
        
        if not all([self.url, self.publishable_key, self.secret_key]):
            raise ValueError("Missing Supabase environment variables: SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, SUPABASE_SECRET_KEY required")
        
        # Use secret key for backend operations (replaces service_role key)
        self.client: Client = create_client(self.url, self.secret_key)
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            # Test with a simple query that should always work
            result = self.client.table("clients").select("count", count="exact").execute()
            return True
        except Exception as e:
            error_str = str(e)
            if "does not exist" in error_str or "relation" in error_str:
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
    
    def get_form_questions(self, form_id: str) -> List[Dict[str, Any]]:
        """Get all questions for a form"""
        result = self.client.table("form_questions").select("*").eq("form_id", form_id).order("question_order").execute()
        return result.data or []
    
    def get_client_by_form(self, form_id: str) -> Optional[Dict[str, Any]]:
        """Get client information associated with a form"""
        # First get the form to find the client_id
        form = self.get_form(form_id)
        if not form or not form.get('client_id'):
            return None
        
        # Then get the client data
        return self.get_client(form['client_id'])
    
    def get_form_with_questions(self, form_id: str) -> Dict[str, Any]:
        """Get form configuration with all associated questions"""
        form = self.get_form(form_id)
        if not form:
            return {}
        
        questions = self.get_form_questions(form_id)
        return {
            **form,
            'questions': questions
        }
    
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
    
    def save_individual_response(self, session_id: str, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save individual response immediately (fire-and-forget)"""
        # Add session_id and timestamp if not present
        response_with_metadata = {
            **response_data,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
        result = self.client.table("responses").insert(response_with_metadata).execute()
        return result.data[0] if result.data else {}
    
    # === Tracking Data Management ===
    
    def save_tracking_data(self, session_id: str, tracking_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save UTM and tracking parameters immediately (fire-and-forget)"""
        tracking_with_metadata = {
            **tracking_data,
            "session_id": session_id,
            "created_at": datetime.now().isoformat()
        }
        result = self.client.table("tracking_data").insert(tracking_with_metadata).execute()
        return result.data[0] if result.data else {}
    
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