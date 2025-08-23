"""
Admin-specific database connections using psycopg2 for raw SQL operations.
This is separate from the main Supabase client for admin authentication and user management.
"""
import psycopg2
import psycopg2.extras
from urllib.parse import urlparse
from .utils.config_loader import get_database_config
import logging

logger = logging.getLogger(__name__)

def get_admin_database_connection():
    """Get raw psycopg2 connection for admin API operations that need raw SQL"""
    try:
        # Get Supabase database URL from config
        config = get_database_config()
        db_url = config.url
        
        # Parse the URL to get connection components
        parsed = urlparse(db_url)
        
        # Create psycopg2 connection
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path[1:],  # Remove leading slash
            user=parsed.username,
            password=parsed.password,
            sslmode='require'
        )
        
        # Use RealDictCursor for easier column access by name
        conn.cursor_factory = psycopg2.extras.RealDictCursor
        return conn
        
    except Exception as e:
        logger.error(f"Failed to create admin database connection: {e}")
        raise