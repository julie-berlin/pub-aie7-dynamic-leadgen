"""SQLite database implementation for standalone testing."""

import sqlite3
import json
import logging
import time
import random
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

def retry_db_operation(max_retries=3, delay_range=(0.1, 0.5)):
    """Decorator to retry database operations on lock/busy errors."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    if "database is locked" in str(e).lower() or "busy" in str(e).lower():
                        if attempt < max_retries - 1:
                            delay = random.uniform(*delay_range)
                            logger.warning(f"Database locked, retrying in {delay:.2f}s (attempt {attempt + 1}/{max_retries})")
                            time.sleep(delay)
                            continue
                    raise e
                except Exception as e:
                    raise e
            return None
        return wrapper
    return decorator

class SQLiteDatabase:
    """SQLite implementation matching Supabase schema."""
    
    def __init__(self, db_path: str = "test_survey.db"):
        """Initialize SQLite database connection."""
        self.db_path = db_path
        self.conn = None
        # Ensure we can write to the database
        import os
        if os.path.exists(db_path):
            os.chmod(db_path, 0o666)  # Make writable
        self._connect()
        self._create_schema()
        
    def _connect(self):
        """Create database connection with better concurrency handling."""
        self.conn = sqlite3.connect(
            self.db_path, 
            check_same_thread=False,
            timeout=30.0,  # 30 second timeout for locks
            isolation_level=None  # Autocommit mode for better concurrency
        )
        self.conn.row_factory = sqlite3.Row
        
        # Enable WAL mode for better concurrent access
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.execute("PRAGMA cache_size=1000")
        self.conn.execute("PRAGMA temp_store=memory")
        
    def _create_schema(self):
        """Create database schema matching production."""
        cursor = self.conn.cursor()
        
        # Clients table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                business_name TEXT,
                email TEXT NOT NULL UNIQUE,
                owner_name TEXT NOT NULL,
                business_type TEXT,
                industry TEXT,
                background TEXT,
                goals TEXT,
                target_audience TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Forms table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS forms (
                id TEXT PRIMARY KEY,
                client_id TEXT REFERENCES clients(id),
                title TEXT NOT NULL,
                description TEXT,
                lead_scoring_threshold_yes INTEGER DEFAULT 80,
                lead_scoring_threshold_maybe INTEGER DEFAULT 50,
                max_questions INTEGER DEFAULT 8,
                min_questions_before_fail INTEGER DEFAULT 4,
                completion_message_template TEXT,
                unqualified_message TEXT DEFAULT 'Thank you for your time.',
                is_active BOOLEAN DEFAULT 1,
                settings TEXT DEFAULT '{}',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Form questions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS form_questions (
                id TEXT PRIMARY KEY,
                form_id TEXT REFERENCES forms(id),
                question_id INTEGER NOT NULL,
                question_order INTEGER NOT NULL,
                question_text TEXT NOT NULL,
                question_type TEXT DEFAULT 'text',
                options TEXT,
                is_required BOOLEAN DEFAULT 0,
                scoring_rubric TEXT,
                category TEXT,
                metadata TEXT DEFAULT '{}',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(form_id, question_id)
            )
        """)
        
        # Lead sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lead_sessions (
                id TEXT PRIMARY KEY,
                form_id TEXT REFERENCES forms(id),
                session_id TEXT UNIQUE NOT NULL,
                client_id TEXT REFERENCES clients(id),
                started_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT,
                step INTEGER DEFAULT 0,
                completed BOOLEAN DEFAULT 0,
                current_score INTEGER DEFAULT 0,
                final_score INTEGER DEFAULT 0,
                lead_status TEXT DEFAULT 'unknown',
                completion_type TEXT,
                completion_message TEXT,
                abandonment_status TEXT DEFAULT 'active',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Responses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS responses (
                id TEXT PRIMARY KEY,
                session_id TEXT REFERENCES lead_sessions(session_id),
                question_id INTEGER NOT NULL,
                question_text TEXT NOT NULL,
                phrased_question TEXT,
                answer TEXT NOT NULL,
                step INTEGER NOT NULL,
                submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
                score_awarded INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
    
    def get_form(self, form_id: str) -> Optional[Dict[str, Any]]:
        """Get form configuration."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM forms WHERE id = ?", (form_id,))
        row = cursor.fetchone()
        if row:
            result = dict(row)
            result['settings'] = json.loads(result.get('settings', '{}'))
            return result
        return None
    
    def get_form_questions(self, form_id: str) -> List[Dict[str, Any]]:
        """Get all questions for a form."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM form_questions 
            WHERE form_id = ? 
            ORDER BY question_order
        """, (form_id,))
        questions = []
        for row in cursor.fetchall():
            question = dict(row)
            if question.get('options'):
                question['options'] = json.loads(question['options'])
            if question.get('metadata'):
                question['metadata'] = json.loads(question['metadata'])
            questions.append(question)
        return questions
    
    def get_client(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get client information."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    @retry_db_operation()
    def create_lead_session(self, session_data: Dict[str, Any]) -> bool:
        """Create a new lead session."""
        try:
            cursor = self.conn.cursor()
            
            # Check if session already exists
            cursor.execute("SELECT session_id FROM lead_sessions WHERE session_id = ?", (session_data['session_id'],))
            if cursor.fetchone():
                logger.info(f"Session {session_data['session_id']} already exists")
                return True
            
            cursor.execute("""
                INSERT INTO lead_sessions (
                    id, session_id, form_id, client_id, 
                    started_at, last_updated, step
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                session_data.get('id', session_data['session_id']),
                session_data['session_id'],
                session_data['form_id'],
                session_data.get('client_id'),
                datetime.now().isoformat(),
                datetime.now().isoformat(),
                0
            ))
            # No need to commit in autocommit mode
            logger.info(f"Created session: {session_data['session_id']}")
            return True
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            logger.error(f"Session data: {session_data}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def get_lead_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get lead session data."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM lead_sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    @retry_db_operation()
    def update_lead_session(self, session_id: str, update_data: Dict[str, Any]) -> bool:
        """Update lead session."""
        try:
            cursor = self.conn.cursor()
            
            # Build dynamic update query
            set_clauses = []
            values = []
            for key, value in update_data.items():
                if key not in ['session_id', 'id']:
                    set_clauses.append(f"{key} = ?")
                    values.append(value)
            
            if not set_clauses:
                return True
            
            values.append(session_id)
            query = f"""
                UPDATE lead_sessions 
                SET {', '.join(set_clauses)}, last_updated = CURRENT_TIMESTAMP
                WHERE session_id = ?
            """
            
            cursor.execute(query, values)
            # No need to commit in autocommit mode
            return True
        except Exception as e:
            logger.error(f"Failed to update session: {e}")
            return False
    
    @retry_db_operation()
    def save_response(self, session_id: str, response_data: Dict[str, Any]) -> bool:
        """Save a user response."""
        try:
            cursor = self.conn.cursor()
            
            # Check if response already exists
            response_id = f"{session_id}_{response_data['question_id']}"
            cursor.execute("SELECT id FROM responses WHERE id = ?", (response_id,))
            if cursor.fetchone():
                logger.info(f"Response {response_id} already exists")
                return True
            
            cursor.execute("""
                INSERT INTO responses (
                    id, session_id, question_id, question_text,
                    phrased_question, answer, step, score_awarded
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                response_id,
                session_id,
                response_data['question_id'],
                response_data.get('question_text', ''),
                response_data.get('phrased_question', ''),
                response_data['answer'],
                response_data.get('step', 0),
                response_data.get('score_awarded', 0)
            ))
            # No need to commit in autocommit mode
            logger.info(f"Saved response: {response_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to save response: {e}")
            logger.error(f"Response data: {response_data}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def get_responses(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all responses for a session."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM responses 
            WHERE session_id = ? 
            ORDER BY step
        """, (session_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_asked_questions(self, session_id: str) -> List[int]:
        """Get list of question IDs already asked in this session."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT DISTINCT question_id FROM responses 
            WHERE session_id = ?
        """, (session_id,))
        return [row[0] for row in cursor.fetchall()]
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

# Global database instance
db = SQLiteDatabase()