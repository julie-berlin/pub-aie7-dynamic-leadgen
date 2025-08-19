"""
Local PostgreSQL database utilities for development without Supabase
"""
import os
import asyncio
import logging
from typing import Dict, List, Any, Optional
import asyncpg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)

class LocalPostgresClient:
    """PostgreSQL client for local development"""
    
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "postgresql://postgres:dev_password@localhost:5432/survey_dev")
        self.pool = None
        
    async def connect(self):
        """Create connection pool"""
        if not self.pool:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=1,
                max_size=10,
                command_timeout=60
            )
            logger.info("Connected to local PostgreSQL database")
    
    async def disconnect(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            self.pool = None
    
    async def execute(self, query: str, *args) -> str:
        """Execute a query"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)
    
    async def fetch(self, query: str, *args) -> List[Dict]:
        """Fetch multiple rows"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(row) for row in rows]
    
    async def fetchrow(self, query: str, *args) -> Optional[Dict]:
        """Fetch single row"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *args)
            return dict(row) if row else None
    
    async def insert(self, table: str, data: Dict) -> Optional[Dict]:
        """Insert data and return the inserted row"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(f'${i+1}' for i in range(len(data)))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"
        
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *data.values())
            return dict(row) if row else None
    
    async def update(self, table: str, data: Dict, where: Dict) -> Optional[Dict]:
        """Update data and return the updated row"""
        set_clause = ', '.join(f"{k} = ${i+1}" for i, k in enumerate(data.keys()))
        where_clause = ' AND '.join(f"{k} = ${i+1+len(data)}" for i, k in enumerate(where.keys()))
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause} RETURNING *"
        
        values = list(data.values()) + list(where.values())
        
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *values)
            return dict(row) if row else None
    
    # Methods to match Supabase API
    async def get_form_by_id(self, form_id: str) -> Optional[Dict]:
        """Get form by ID with client data"""
        query = """
            SELECT f.*, c.* 
            FROM forms f
            JOIN clients c ON f.client_id = c.id
            WHERE f.id = $1
        """
        return await self.fetchrow(query, form_id)
    
    async def get_form_questions(self, form_id: str) -> List[Dict]:
        """Get all questions for a form"""
        query = """
            SELECT * FROM form_questions
            WHERE form_id = $1
            ORDER BY order_position
        """
        return await self.fetch(query, form_id)
    
    async def create_lead_session(self, session_data: Dict) -> Optional[Dict]:
        """Create a new lead session"""
        return await self.insert('lead_sessions', session_data)
    
    async def save_response(self, response_data: Dict) -> Optional[Dict]:
        """Save a survey response"""
        return await self.insert('responses', response_data)
    
    async def update_lead_session(self, session_id: str, updates: Dict) -> Optional[Dict]:
        """Update lead session"""
        return await self.update('lead_sessions', updates, {'id': session_id})

# Global client instance
db = LocalPostgresClient()

# Async context manager support
class LocalPostgresManager:
    async def __aenter__(self):
        await db.connect()
        return db
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await db.disconnect()