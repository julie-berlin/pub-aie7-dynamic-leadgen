"""
Redis session store implementation for Starlette SessionMiddleware.

This implements a custom session store that uses Redis as the backend,
following the Starlette SessionMiddleware interface.
"""

import json
import os
import uuid
from typing import Optional

import redis.asyncio as redis


class RedisSessionStore:
    """Redis-backed session store for Starlette SessionMiddleware."""
    
    def __init__(self, redis_url: str = None, prefix: str = "session:", ttl: int = 1800):
        """
        Initialize Redis session store.
        
        Args:
            redis_url: Redis connection URL
            prefix: Key prefix for session data
            ttl: Session TTL in seconds (default: 30 minutes)
        """
        self.redis_url = redis_url or os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.prefix = prefix
        self.ttl = ttl
        self._redis = None
    
    async def _get_redis(self):
        """Get Redis client instance."""
        if self._redis is None:
            self._redis = redis.from_url(self.redis_url, decode_responses=True)
        return self._redis
    
    def _make_key(self, session_id: str) -> str:
        """Create Redis key for session ID."""
        return f"{self.prefix}{session_id}"
    
    async def read(self, session_id: str) -> dict:
        """
        Read session data from Redis.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session data dictionary
        """
        if not session_id:
            return {}
            
        redis_client = await self._get_redis()
        key = self._make_key(session_id)
        
        data = await redis_client.get(key)
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {}
        
        return {}
    
    async def write(self, session_id: str, data: dict) -> None:
        """
        Write session data to Redis.
        
        Args:
            session_id: Session identifier
            data: Session data to store
        """
        if not session_id:
            return
            
        redis_client = await self._get_redis()
        key = self._make_key(session_id)
        
        # Store data with TTL
        await redis_client.setex(key, self.ttl, json.dumps(data))
    
    async def remove(self, session_id: str) -> None:
        """
        Remove session data from Redis.
        
        Args:
            session_id: Session identifier
        """
        if not session_id:
            return
            
        redis_client = await self._get_redis()
        key = self._make_key(session_id)
        await redis_client.delete(key)
    
    async def generate_id(self) -> str:
        """Generate a new session ID."""
        return str(uuid.uuid4())
    
    async def health_check(self) -> bool:
        """Check if Redis is healthy."""
        try:
            redis_client = await self._get_redis()
            await redis_client.ping()
            return True
        except Exception:
            return False