"""
Tests for database operations using legacy authentication (ANON_KEY + SERVICE_KEY).
These tests should pass with the current authentication system.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))


class TestDatabaseLegacyAuthentication:
    """Test suite for legacy authentication system."""
    
    def test_legacy_env_vars_available(self, legacy_env_vars):
        """Test that legacy environment variables are available."""
        assert legacy_env_vars["SUPABASE_URL"] is not None
        assert legacy_env_vars["SUPABASE_ANON_KEY"] is not None
        assert legacy_env_vars["SUPABASE_SERVICE_KEY"] is not None
        
        # Verify key formats
        assert legacy_env_vars["SUPABASE_URL"].startswith("https://")
        assert legacy_env_vars["SUPABASE_ANON_KEY"].startswith("eyJ")  # JWT format
        assert legacy_env_vars["SUPABASE_SERVICE_KEY"].startswith("eyJ")  # JWT format
    
    def test_legacy_client_initialization(self, legacy_env_vars):
        """Test that SupabaseClient can be initialized with legacy keys."""
        with patch.dict(os.environ, legacy_env_vars):
            # Import here to use patched environment
            from database import SupabaseClient
            
            client = SupabaseClient()
            
            assert client.url == legacy_env_vars["SUPABASE_URL"]
            assert client.anon_key == legacy_env_vars["SUPABASE_ANON_KEY"]
            assert client.service_key == legacy_env_vars["SUPABASE_SERVICE_KEY"]
            assert client.client is not None
    
    def test_legacy_missing_env_vars_raises_error(self):
        """Test that missing legacy environment variables raise ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            from database import SupabaseClient
            
            with pytest.raises(ValueError, match="Missing Supabase environment variables"):
                SupabaseClient()
    
    @patch('database.create_client')
    def test_legacy_connection_test(self, mock_create_client, legacy_env_vars):
        """Test connection testing with legacy authentication."""
        # Mock successful connection
        mock_client = MagicMock()
        mock_client.table.return_value.select.return_value.execute.return_value = MagicMock()
        mock_create_client.return_value = mock_client
        
        with patch.dict(os.environ, legacy_env_vars):
            from database import SupabaseClient
            
            client = SupabaseClient()
            result = client.test_connection()
            
            assert result is True
            mock_client.table.assert_called_with("clients")
            mock_client.table.return_value.select.assert_called_with("count", count="exact")
    
    @patch('database.create_client')
    def test_legacy_connection_legacy_keys_disabled_error(self, mock_create_client, legacy_env_vars):
        """Test handling of 'Legacy API keys are disabled' error."""
        # Mock legacy keys disabled error
        mock_client = MagicMock()
        mock_client.table.return_value.select.return_value.execute.side_effect = Exception(
            "Legacy API keys are disabled"
        )
        mock_create_client.return_value = mock_client
        
        with patch.dict(os.environ, legacy_env_vars), patch('builtins.print') as mock_print:
            from database import SupabaseClient
            
            client = SupabaseClient()
            result = client.test_connection()
            
            assert result is False
            mock_print.assert_called()
            # Check that the specific error message is printed
            error_msg = mock_print.call_args_list[0][0][0]
            assert "Legacy API keys are disabled" in error_msg
    
    @patch('database.create_client')
    def test_legacy_crud_operations(self, mock_create_client, legacy_env_vars, sample_client_data):
        """Test basic CRUD operations with legacy authentication."""
        # Mock successful database operations
        mock_client = MagicMock()
        mock_client.table.return_value.insert.return_value.execute.return_value.data = [sample_client_data]
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [sample_client_data]
        mock_create_client.return_value = mock_client
        
        with patch.dict(os.environ, legacy_env_vars):
            from database import SupabaseClient
            
            client = SupabaseClient()
            
            # Test create operation
            result = client.create_client_record(sample_client_data)
            assert result == sample_client_data
            
            # Test read operation
            result = client.get_client(sample_client_data["id"])
            assert result == sample_client_data
    
    @patch('database.create_client')
    def test_legacy_session_management(self, mock_create_client, legacy_env_vars, sample_session_data):
        """Test session management operations with legacy authentication."""
        # Mock successful session operations
        mock_client = MagicMock()
        mock_client.table.return_value.insert.return_value.execute.return_value.data = [sample_session_data]
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [sample_session_data]
        mock_client.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [sample_session_data]
        mock_create_client.return_value = mock_client
        
        with patch.dict(os.environ, legacy_env_vars):
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
    def test_legacy_response_management(self, mock_create_client, legacy_env_vars, sample_response_data):
        """Test response management operations with legacy authentication."""
        # Mock successful response operations
        mock_client = MagicMock()
        mock_client.table.return_value.insert.return_value.execute.return_value.data = [sample_response_data]
        mock_client.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data = [sample_response_data]
        mock_create_client.return_value = mock_client
        
        with patch.dict(os.environ, legacy_env_vars):
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
    
    def test_singleton_instance_consistency(self, legacy_env_vars):
        """Test that the singleton db instance is consistent."""
        with patch.dict(os.environ, legacy_env_vars):
            from database import db
            
            # Multiple imports should return the same instance
            from database import db as db2
            assert db is db2
            
            # Both should have the same configuration
            assert db.url == db2.url
            assert db.anon_key == db2.anon_key
            assert db.service_key == db2.service_key
    
    @patch('database.create_client')
    def test_singleton_connection_state(self, mock_create_client, legacy_env_vars):
        """Test that singleton maintains connection state."""
        mock_client = MagicMock()
        mock_client.table.return_value.select.return_value.execute.return_value = MagicMock()
        mock_create_client.return_value = mock_client
        
        with patch.dict(os.environ, legacy_env_vars):
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