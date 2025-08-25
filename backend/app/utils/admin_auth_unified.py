"""
Unified Admin Authentication System

This module provides a single, consistent authentication system for all admin operations.
It replaces the scattered JWT token generation and validation logic across different modules.
"""

import os
import jwt
import time
import hashlib
import secrets
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'dev-secret-key-change-in-production')
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', '1'))

class AdminAuthService:
    """Unified admin authentication service"""
    
    def __init__(self):
        self.jwt_secret = JWT_SECRET
        self.jwt_algorithm = JWT_ALGORITHM
        self.jwt_expiration_hours = JWT_EXPIRATION_HOURS
    
    def create_access_token(self, user_id: str, client_id: str, role: str = 'admin') -> tuple[str, int]:
        """
        Create a JWT access token with consistent payload structure.
        Returns: (token, expires_in_seconds)
        """
        expiration = datetime.now(timezone.utc) + timedelta(hours=self.jwt_expiration_hours)
        payload = {
            'user_id': user_id,
            'client_id': client_id,
            'role': role,
            'exp': expiration,
            'iat': datetime.now(timezone.utc)
        }
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        expires_in = int(self.jwt_expiration_hours * 3600)
        
        logger.info(f"Created access token for user {user_id}, client {client_id}, expires in {expires_in}s")
        return token, expires_in
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify JWT token and return payload.
        Returns None if token is invalid or expired.
        """
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            
            # Validate required fields
            required_fields = ['user_id', 'client_id', 'exp']
            if not all(field in payload for field in required_fields):
                logger.warning(f"Token missing required fields: {required_fields}")
                return None
            
            # Check expiration (jwt.decode already does this, but let's be explicit)
            if payload.get('exp', 0) < time.time():
                logger.warning("Token has expired")
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
    
    def hash_password(self, password: str) -> str:
        """Hash a password with salt."""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}:{password_hash.hex()}"
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        try:
            salt, stored_hash = hashed_password.split(':')
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return password_hash.hex() == stored_hash
        except ValueError:
            return False

# Global instance
admin_auth = AdminAuthService()

# Convenience functions for backwards compatibility
def create_access_token(user_id: str, client_id: str, role: str = 'admin') -> tuple[str, int]:
    """Create access token - unified function"""
    return admin_auth.create_access_token(user_id, client_id, role)

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify token - unified function"""
    return admin_auth.verify_token(token)

def hash_password(password: str) -> str:
    """Hash password - unified function"""
    return admin_auth.hash_password(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password - unified function"""
    return admin_auth.verify_password(password, hashed_password)