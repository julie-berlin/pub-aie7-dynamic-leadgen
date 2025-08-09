"""
Test configuration and fixtures for authentication tests.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env_vars():
    """Load environment variables for testing."""
    load_dotenv()


@pytest.fixture
def legacy_env_vars():
    """Environment variables for legacy authentication."""
    return {
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_ANON_KEY": os.getenv("SUPABASE_ANON_KEY"),
        "SUPABASE_SERVICE_KEY": os.getenv("SUPABASE_SERVICE_KEY"),
    }


@pytest.fixture
def new_env_vars():
    """Environment variables for new authentication system."""
    return {
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_PUBLISHABLE_KEY": os.getenv("SUPABASE_PUBLISHABLE_KEY"),
        "SUPABASE_SECRET_KEY": os.getenv("SUPABASE_SECRET_KEY"),
    }


@pytest.fixture
def mock_supabase_client():
    """Mock Supabase client for testing."""
    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.execute.return_value.data = []
    return mock_client


@pytest.fixture
def sample_client_data():
    """Sample client data for testing."""
    return {
        "id": "test-client-123",
        "name": "Test Dog Walker",
        "business_type": "dog_walking",
        "created_at": "2025-01-01T00:00:00Z"
    }


@pytest.fixture
def sample_session_data():
    """Sample session data for testing."""
    return {
        "session_id": "test-session-456",
        "form_id": "dogwalk_demo_form",
        "client_id": "test-client-123",
        "final_score": 0,
        "lead_status": "unknown",
        "completed": False,
        "step_count": 0,
        "started_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z"
    }


@pytest.fixture
def sample_response_data():
    """Sample response data for testing."""
    return {
        "session_id": "test-session-456",
        "question_id": "1",
        "answer": "Golden Retriever",
        "data_type": "text",
        "is_required": False,
        "original_question": "What breed is your dog?",
        "phrased_question": "What breed is your dog?",
        "scoring_rubric": "dog_breed",
        "step": 1,
        "timestamp": "2025-01-01T00:00:00Z"
    }