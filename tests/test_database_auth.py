"""
Tests for database operations using new authentication (PUBLISHABLE_KEY + SECRET_KEY).
These tests verify the new authentication system works correctly.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))


class TestDatabaseAuthentication:
    """Test suite for new authentication system."""
    
    def test_new_env_vars_available(self, new_env_vars):
        """Test that new environment variables are available."""
        assert new_env_vars["SUPABASE_URL"] is not None
        assert new_env_vars["SUPABASE_PUBLISHABLE_KEY"] is not None
        assert new_env_vars["SUPABASE_SECRET_KEY"] is not None
        
        # Verify key formats
        assert new_env_vars["SUPABASE_URL"].startswith("https://")
        assert new_env_vars["SUPABASE_PUBLISHABLE_KEY"].startswith("sb_publishable_")
        assert new_env_vars["SUPABASE_SECRET_KEY"].startswith("sb_secret_")
    
    def test_client_initialization(self, new_env_vars):
        """Test that SupabaseClient can be initialized with new keys."""
        env_mapping = {
            "SUPABASE_URL": new_env_vars["SUPABASE_URL"],
            "SUPABASE_PUBLISHABLE_KEY": new_env_vars["SUPABASE_PUBLISHABLE_KEY"],
            "SUPABASE_SECRET_KEY": new_env_vars["SUPABASE_SECRET_KEY"],
        }
        
        with patch.dict(os.environ, env_mapping, clear=True):
            # Import here to use patched environment
            from database import SupabaseClient
            
            client = SupabaseClient()
            
            assert client.url == new_env_vars["SUPABASE_URL"]
            assert client.publishable_key == new_env_vars["SUPABASE_PUBLISHABLE_KEY"]
            assert client.secret_key == new_env_vars["SUPABASE_SECRET_KEY"]
            assert client.client is not None
    
    def test_missing_env_vars_raises_error(self):
        """Test that missing environment variables raise ValueError."""
        with patch.dict(os.environ, {"SUPABASE_URL": "https://test.supabase.co"}, clear=True):
            from database import SupabaseClient
            
            with pytest.raises(ValueError, match="Missing Supabase environment variables"):
                SupabaseClient()
    
    @patch('database.create_client')
    def test_connection_test(self, mock_create_client, new_env_vars):
        """Test connection testing with new authentication."""
        # Mock successful connection
        mock_client = MagicMock()
        mock_client.table.return_value.select.return_value.execute.return_value = MagicMock()
        mock_create_client.return_value = mock_client
        
        env_mapping = {
            "SUPABASE_URL": new_env_vars["SUPABASE_URL"],
            "SUPABASE_PUBLISHABLE_KEY": new_env_vars["SUPABASE_PUBLISHABLE_KEY"],
            "SUPABASE_SECRET_KEY": new_env_vars["SUPABASE_SECRET_KEY"],
        }
        
        with patch.dict(os.environ, env_mapping, clear=True):
            from database import SupabaseClient
            
            client = SupabaseClient()
            result = client.test_connection()
            
            assert result is True
            mock_create_client.assert_called_with(
                new_env_vars["SUPABASE_URL"],
                new_env_vars["SUPABASE_SECRET_KEY"]
            )
            mock_client.table.assert_called_with("clients")
    
    @patch('database.create_client')
    def test_crud_operations(self, mock_create_client, new_env_vars, sample_client_data):
        """Test basic CRUD operations with new authentication."""
        # Mock successful database operations
        mock_client = MagicMock()
        mock_client.table.return_value.insert.return_value.execute.return_value.data = [sample_client_data]
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [sample_client_data]
        mock_create_client.return_value = mock_client
        
        env_mapping = {
            "SUPABASE_URL": new_env_vars["SUPABASE_URL"],
            "SUPABASE_PUBLISHABLE_KEY": new_env_vars["SUPABASE_PUBLISHABLE_KEY"],
            "SUPABASE_SECRET_KEY": new_env_vars["SUPABASE_SECRET_KEY"],
        }
        
        with patch.dict(os.environ, env_mapping, clear=True):
            from database import SupabaseClient
            
            client = SupabaseClient()
            
            # Test create operation
            result = client.create_client_record(sample_client_data)
            assert result == sample_client_data
            
            # Test read operation
            result = client.get_client(sample_client_data["id"])
            assert result == sample_client_data
    
    @patch('database.create_client')
    def test_session_management(self, mock_create_client, new_env_vars, sample_session_data):
        """Test session management operations with new authentication."""
        # Mock successful session operations
        mock_client = MagicMock()
        mock_client.table.return_value.insert.return_value.execute.return_value.data = [sample_session_data]
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [sample_session_data]
        mock_client.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [sample_session_data]
        mock_create_client.return_value = mock_client
        
        env_mapping = {
            "SUPABASE_URL": new_env_vars["SUPABASE_URL"],
            "SUPABASE_PUBLISHABLE_KEY": new_env_vars["SUPABASE_PUBLISHABLE_KEY"],
            "SUPABASE_SECRET_KEY": new_env_vars["SUPABASE_SECRET_KEY"],
        }
        
        with patch.dict(os.environ, env_mapping, clear=True):
            from database import SupabaseClient
            
            client = SupabaseClient()
            
            # Test create session
            result = client.create_lead_session(sample_session_data)
            assert result == sample_session_data
            
            # Test get session
            result = client.get_lead_session(sample_session_data["session_id"])
            assert result == sample_session_data
            
            # Test update session
            updates = {"completed": True}
            result = client.update_lead_session(sample_session_data["session_id"], updates)
            assert result == sample_session_data
    
    @patch('database.create_client')
    def test_response_management(self, mock_create_client, new_env_vars, sample_response_data):
        """Test response management operations with new authentication."""
        # Mock successful response operations
        mock_client = MagicMock()
        mock_client.table.return_value.insert.return_value.execute.return_value.data = [sample_response_data]
        mock_client.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data = [sample_response_data]
        mock_create_client.return_value = mock_client
        
        env_mapping = {
            "SUPABASE_URL": new_env_vars["SUPABASE_URL"],
            "SUPABASE_PUBLISHABLE_KEY": new_env_vars["SUPABASE_PUBLISHABLE_KEY"],
            "SUPABASE_SECRET_KEY": new_env_vars["SUPABASE_SECRET_KEY"],
        }
        
        with patch.dict(os.environ, env_mapping, clear=True):
            from database import SupabaseClient
            
            client = SupabaseClient()
            
            # Test create response
            result = client.create_response(sample_response_data)
            assert result == sample_response_data
            
            # Test get session responses
            result = client.get_session_responses(sample_response_data["session_id"])
            assert result == [sample_response_data]


class TestDatabaseSingletonBehavior:
    """Test the singleton database instance behavior."""
    
    def test_singleton_instance_consistency(self, new_env_vars):
        """Test that the singleton db instance is consistent."""
        env_mapping = {
            "SUPABASE_URL": new_env_vars["SUPABASE_URL"],
            "SUPABASE_PUBLISHABLE_KEY": new_env_vars["SUPABASE_PUBLISHABLE_KEY"],
            "SUPABASE_SECRET_KEY": new_env_vars["SUPABASE_SECRET_KEY"],
        }
        
        with patch.dict(os.environ, env_mapping, clear=True):
            from database import db
            
            # Multiple imports should return the same instance
            from database import db as db2
            assert db is db2
            
            # Both should have the same configuration
            assert db.url == db2.url
            assert db.publishable_key == db2.publishable_key
            assert db.secret_key == db2.secret_key
    
    @patch('database.create_client')
    def test_singleton_connection_state(self, mock_create_client, new_env_vars):
        """Test that singleton maintains connection state."""
        mock_client = MagicMock()
        mock_client.table.return_value.select.return_value.execute.return_value = MagicMock()
        mock_create_client.return_value = mock_client
        
        env_mapping = {
            "SUPABASE_URL": new_env_vars["SUPABASE_URL"],
            "SUPABASE_PUBLISHABLE_KEY": new_env_vars["SUPABASE_PUBLISHABLE_KEY"],
            "SUPABASE_SECRET_KEY": new_env_vars["SUPABASE_SECRET_KEY"],
        }
        
        with patch.dict(os.environ, env_mapping, clear=True):
            # Create a fresh instance to test creation behavior
            from database import SupabaseClient
            
            client = SupabaseClient()
            
            # First connection test should work
            result1 = client.test_connection()
            assert result1 is True
            
            # Second connection test should reuse the same client
            result2 = client.test_connection()
            assert result2 is True
            
            # Client should be created once during initialization
            mock_create_client.assert_called_once()


class TestKeyValidation:
    """Test suite for key validation and format checking."""
    
    def test_new_key_format_validation(self, new_env_vars):
        """Test that new keys have the expected format."""
        publishable_key = new_env_vars["SUPABASE_PUBLISHABLE_KEY"]
        secret_key = new_env_vars["SUPABASE_SECRET_KEY"]
        
        # New keys have specific prefixes
        assert publishable_key.startswith("sb_publishable_")
        assert secret_key.startswith("sb_secret_")
        
        # Keys should have content after the prefix
        assert len(publishable_key) > len("sb_publishable_")
        assert len(secret_key) > len("sb_secret_")
        
        # Keys should not contain JWT-like dots
        assert '.' not in publishable_key
        assert '.' not in secret_key