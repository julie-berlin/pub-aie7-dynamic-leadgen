"""
Database utilities for Supabase integration with environment-specific configuration
"""
import os
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from supabase import create_client, Client
from dotenv import load_dotenv
from .utils.config_loader import get_database_config, DatabaseConfig

# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)

class SupabaseClient:
    """Wrapper for Supabase operations with connection pooling and environment-specific settings"""
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        """Initialize with database configuration"""
        if config is None:
            config = get_database_config()
        
        self.config = config
        self.url = config.url
        self.publishable_key = config.publishable_key
        self.secret_key = config.secret_key
        
        if not all([self.url, self.publishable_key, self.secret_key]):
            raise ValueError("Missing Supabase environment variables: SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, SUPABASE_SECRET_KEY required")
        
        # Connection pool settings
        self.pool_size = config.pool_size
        self.max_overflow = config.pool_max_overflow
        self.query_timeout = config.query_timeout
        
        # Use secret key for backend operations
        self.client: Client = create_client(
            self.url, 
            self.secret_key
        )
        
        # Connection pool tracking
        self._active_connections = 0
        self._total_connections = 0
        self._failed_connections = 0
        
        logger.info(f"Database client initialized - Pool size: {self.pool_size}, Environment: {os.getenv('ENVIRONMENT', 'development')}")
    
    def _execute_with_retry(self, operation_func, *args, **kwargs):
        """Execute database operation with retry logic"""
        for attempt in range(self.config.retry_attempts):
            try:
                self._active_connections += 1
                self._total_connections += 1
                
                start_time = time.time()
                result = operation_func(*args, **kwargs)
                
                # Log slow queries
                execution_time = time.time() - start_time
                if execution_time > 1.0:  # Log queries taking more than 1 second
                    logger.warning(f"Slow query detected: {execution_time:.2f}s")
                
                return result
            
            except Exception as e:
                self._failed_connections += 1
                logger.warning(f"Database operation failed (attempt {attempt + 1}/{self.config.retry_attempts}): {e}")
                
                if attempt == self.config.retry_attempts - 1:  # Last attempt
                    raise e
                
                time.sleep(self.config.retry_delay)
            finally:
                self._active_connections = max(0, self._active_connections - 1)

    def test_connection(self) -> bool:
        """Test database connection with retry logic"""
        def _test():
            return self.client.table("clients").select("count", count="exact").execute()
        
        try:
            self._execute_with_retry(_test)
            logger.info("Database connection test successful")
            return True
        except Exception as e:
            error_str = str(e)
            if "does not exist" in error_str or "relation" in error_str:
                logger.info("Database connection works, but tables don't exist yet")
                print("🔧 Database connection works, but tables don't exist yet.")
                print("   Run the database/001_initial_schema.sql file in your Supabase SQL Editor first.")
                return False
            else:
                logger.error(f"Connection test failed: {e}")
                print(f"Connection test failed: {e}")
            return False
    
    def get_connection_stats(self) -> Dict[str, int]:
        """Get connection pool statistics"""
        return {
            'active_connections': self._active_connections,
            'total_connections': self._total_connections,
            'failed_connections': self._failed_connections,
            'pool_size': self.pool_size,
            'max_overflow': self.max_overflow
        }
    
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
        questions = result.data or []
        
        # CRITICAL FIX: Map question_id to id for consistent internal usage
        # The database stores question ID as 'question_id' but the code expects 'id'
        # This prevents questions from repeating - see FIX_DOCUMENTATION.md
        for q in questions:
            if 'question_id' in q and 'id' not in q:
                q['id'] = q['question_id']
                logger.debug(f"🔥 QUESTION ID MAPPING: Mapped question_id {q['question_id']} to id field")
        
        return questions
    
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
    
    def get_tracking_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get tracking data for a session"""
        result = self.client.table("tracking_data").select("*").eq("session_id", session_id).execute()
        return result.data[0] if result.data else None
    
    # === Session State Management ===
    
    def save_session_snapshot(self, session_id: str, full_state: Dict[str, Any], step: int, recovery_reason: str = None) -> Dict[str, Any]:
        """Save session state snapshot for recovery"""
        snapshot_data = {
            "session_id": session_id,
            "full_state": full_state,
            "core_state": full_state.get('core', {}),
            "step": step,
            "recoverable": True,
            "recovery_reason": recovery_reason,
            "created_at": datetime.now().isoformat()
        }
        result = self.client.table("session_snapshots").insert(snapshot_data).execute()
        return result.data[0] if result.data else {}
    
    def get_latest_session_snapshot(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the most recent recoverable snapshot for a session"""
        result = self.client.table("session_snapshots")\
            .select("*")\
            .eq("session_id", session_id)\
            .eq("recoverable", True)\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()
        return result.data[0] if result.data else None
    
    # === Enhanced Lead Session Management ===
    
    def update_lead_session_with_tracking(self, session_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update lead session with automatic timestamp and abandonment tracking"""
        updates_with_timestamp = {
            **updates,
            "last_updated": datetime.now().isoformat(),
            "last_activity_timestamp": datetime.now().isoformat()
        }
        result = self.client.table("lead_sessions").update(updates_with_timestamp).eq("session_id", session_id).execute()
        return result.data[0] if result.data else {}
    
    def mark_session_abandoned(self, session_id: str) -> Dict[str, Any]:
        """Mark session as abandoned with proper metadata"""
        abandon_data = {
            "abandonment_status": "abandoned",
            "abandonment_risk": 1.0,
            "completed": True,
            "completion_type": "abandoned",
            "completed_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        result = self.client.table("lead_sessions").update(abandon_data).eq("session_id", session_id).execute()
        return result.data[0] if result.data else {}
    
    # === Analytics and Reporting ===
    
    def get_form_analytics(self, form_id: str, days: int = 30) -> Dict[str, Any]:
        """Get analytics for a form over the last N days"""
        from datetime import timedelta
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        # Get session stats
        sessions = self.client.table("lead_sessions")\
            .select("*")\
            .eq("form_id", form_id)\
            .gte("started_at", cutoff_date)\
            .execute()
        
        if not sessions.data:
            return {"total_sessions": 0}
        
        total_sessions = len(sessions.data)
        completed_sessions = len([s for s in sessions.data if s.get('completed')])
        qualified_leads = len([s for s in sessions.data if s.get('lead_status') == 'yes'])
        maybe_leads = len([s for s in sessions.data if s.get('lead_status') == 'maybe'])
        abandoned_sessions = len([s for s in sessions.data if s.get('completion_type') == 'abandoned'])
        
        return {
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "completion_rate": completed_sessions / total_sessions if total_sessions > 0 else 0,
            "qualified_leads": qualified_leads,
            "maybe_leads": maybe_leads,
            "qualified_rate": qualified_leads / completed_sessions if completed_sessions > 0 else 0,
            "abandoned_sessions": abandoned_sessions,
            "abandonment_rate": abandoned_sessions / total_sessions if total_sessions > 0 else 0,
            "avg_steps": sum(s.get('step', 0) for s in sessions.data) / total_sessions if total_sessions > 0 else 0
        }
    
    def get_utm_performance(self, form_id: str = None, days: int = 30) -> List[Dict[str, Any]]:
        """Get UTM source performance analytics"""
        from datetime import timedelta
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        query = self.client.table("tracking_data")\
            .select("utm_source, utm_campaign, utm_medium")\
            .gte("created_at", cutoff_date)
        
        if form_id:
            # Join with lead_sessions to filter by form
            query = query.eq("session_id", f"lead_sessions(form_id.eq.{form_id})")
        
        result = query.execute()
        return result.data or []
    
    # === Question Tracking Management ===
    
    def get_asked_questions(self, session_id: str) -> List[int]:
        """Get list of question_ids already asked for this session"""
        try:
            # Simple and reliable: get all questions that have responses (including placeholders)
            result = self.client.table("responses").select("question_id").eq("session_id", session_id).execute()
            asked_questions = [r["question_id"] for r in result.data] if result.data else []
            return asked_questions
        except Exception as e:
            logger.error(f"Error getting asked questions for session {session_id}: {e}")
            return []
    
    def mark_questions_asked(self, session_id: str, question_ids: List[int], questions_data: List[Dict] = None) -> bool:
        """Mark questions as asked by creating entries in responses table"""
        try:
            for q_id in question_ids:
                # Check if already exists
                existing = self.client.table("responses").select("id").eq("session_id", session_id).eq("question_id", q_id).execute()
                if existing.data:
                    continue  # Already marked
                
                # Find question text from questions_data if provided
                question_text = f"Question {q_id}"  # Default
                if questions_data:
                    for q in questions_data:
                        if q.get('question_id') == q_id:
                            question_text = q.get('question', q.get('question_text', f"Question {q_id}"))
                            break
                
                # Create placeholder response to mark as asked
                placeholder = {
                    "session_id": session_id,
                    "question_id": q_id,
                    "question_text": question_text,
                    "answer": "ASKED_PLACEHOLDER",  # Placeholder to mark as asked
                    "timestamp": "now()",
                    "step": 0
                }
                
                self.client.table("responses").insert(placeholder).execute()
                logger.info(f"DATABASE: Marked question {q_id} as asked with placeholder response")
            
            return True
        except Exception as e:
            logger.error(f"Error marking questions as asked for session {session_id}: {e}")
            return False
    
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

def get_database_connection():
    """Compatibility wrapper for Phase 2 API modules"""
    return db