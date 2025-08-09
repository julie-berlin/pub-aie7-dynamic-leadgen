"""
Tests for Pydantic model integration and type safety.

Demonstrates the benefits of using Pydantic models throughout the survey system
including validation, type safety, and error handling.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

# Import Pydantic models
from ..pydantic_models import (
    SurveyGraphState,
    CoreSurveyState,
    StartSessionRequest,
    SubmitResponsesRequest,
    ResponseData,
    LeadStatus,
    AbandonmentStatus,
    create_initial_state
)

# Import validation helpers
from ..pydantic_validation_helpers import (
    validate_and_extract_state,
    validate_responses,
    create_operation_log_entry,
    safe_state_update,
    extract_api_response_data
)


class TestPydanticValidation:
    """Test Pydantic validation and type safety features."""

    def test_start_session_request_validation(self):
        """Test StartSessionRequest validation."""
        
        # Valid request
        valid_data = {
            'form_id': 'test-form-123',
            'utm_source': 'facebook',
            'utm_campaign': 'summer_2025',
            'landing_page': 'https://example.com'
        }
        
        request = StartSessionRequest(**valid_data)
        assert request.form_id == 'test-form-123'
        assert request.utm_source == 'facebook'
        assert request.utm_campaign == 'summer_2025'

    def test_start_session_request_validation_errors(self):
        """Test StartSessionRequest validation catches errors."""
        
        # Missing required form_id
        with pytest.raises(ValidationError) as exc_info:
            StartSessionRequest()
        
        assert 'form_id' in str(exc_info.value)
        
        # Empty form_id should be caught by validator
        with pytest.raises(ValidationError):
            StartSessionRequest(form_id='   ')  # Whitespace only

    def test_submit_responses_request_validation(self):
        """Test SubmitResponsesRequest validation."""
        
        valid_data = {
            'session_id': 'session-123',
            'responses': [
                {
                    'question_id': 1,
                    'answer': 'Test answer',
                    'question_text': 'Test question?'
                }
            ]
        }
        
        request = SubmitResponsesRequest(**valid_data)
        assert request.session_id == 'session-123'
        assert len(request.responses) == 1

    def test_submit_responses_validation_errors(self):
        """Test SubmitResponsesRequest validation catches errors."""
        
        # Invalid responses - missing required fields
        invalid_data = {
            'session_id': 'session-123',
            'responses': [
                {'answer': 'Missing question_id'}  # Missing question_id
            ]
        }
        
        with pytest.raises(ValidationError) as exc_info:
            SubmitResponsesRequest(**invalid_data)
        
        assert 'question_id' in str(exc_info.value).lower()

    def test_create_initial_state(self):
        """Test create_initial_state utility function."""
        
        state = create_initial_state(
            session_id='test-session-123',
            form_id='test-form-456',
            utm_data={'utm_source': 'google', 'utm_campaign': 'test'}
        )
        
        # Verify state structure
        assert isinstance(state, SurveyGraphState)
        assert state.core.session_id == 'test-session-123'
        assert state.core.form_id == 'test-form-456'
        assert state.core.utm_source == 'google'
        assert state.core.utm_campaign == 'test'
        
        # Verify default values
        assert state.core.step == 0
        assert state.core.completed is False
        assert state.lead_intelligence.lead_status == LeadStatus.UNKNOWN
        assert state.engagement.abandonment_status == AbandonmentStatus.ACTIVE

    def test_response_data_validation(self):
        """Test ResponseData model validation."""
        
        # Valid response
        response_data = {
            'question_id': 1,
            'question_text': 'What is your name?',
            'answer': 'John Doe',
            'timestamp': datetime.now().isoformat(),
            'step': 1
        }
        
        response = ResponseData(**response_data)
        assert response.question_id == 1
        assert response.answer == 'John Doe'
        assert response.step == 1

    def test_enum_validation(self):
        """Test enum validation for LeadStatus and AbandonmentStatus."""
        
        # Valid enum values
        assert LeadStatus.YES == 'yes'
        assert LeadStatus.MAYBE == 'maybe'
        assert AbandonmentStatus.ACTIVE == 'active'
        assert AbandonmentStatus.HIGH_RISK == 'high_risk'
        
        # Test enum validation in models
        core_state = CoreSurveyState(
            session_id='test-123',
            form_id='form-456',
            started_at=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat()
        )
        
        # Should use enum values
        assert core_state.session_id == 'test-123'

    def test_validate_and_extract_state_helper(self):
        """Test the validate_and_extract_state helper function."""
        
        # Create valid state
        initial_state = create_initial_state(
            session_id='test-session',
            form_id='test-form'
        )
        
        raw_dict = initial_state.model_dump()
        
        # Test validation helper
        validated, raw = validate_and_extract_state(raw_dict)
        
        assert validated is not None
        assert isinstance(validated, SurveyGraphState)
        assert raw == raw_dict
        
        # Test with invalid state
        invalid_state = {'invalid': 'structure'}
        validated_invalid, raw_invalid = validate_and_extract_state(invalid_state)
        
        assert validated_invalid is None  # Should fail validation
        assert raw_invalid == invalid_state  # But preserve raw data

    def test_validate_responses_helper(self):
        """Test the validate_responses helper function."""
        
        raw_responses = [
            {
                'question_id': 1,
                'question_text': 'Name?',
                'answer': 'John'
            },
            {
                'question_id': 2,
                'question_text': 'Age?',
                'answer': '25'
            },
            {
                # Invalid response - missing required fields
                'answer': 'No question_id'
            }
        ]
        
        validated_responses = validate_responses(raw_responses)
        
        # Should validate the first 2, skip the invalid one
        assert len(validated_responses) == 2
        assert all(isinstance(r, ResponseData) for r in validated_responses)
        assert validated_responses[0].question_id == 1
        assert validated_responses[1].question_id == 2

    def test_operation_log_entry_creation(self):
        """Test operation log entry creation."""
        
        log_entry = create_operation_log_entry(
            operation='test_operation',
            details='Testing log entry creation',
            step=2
        )
        
        assert log_entry.operation == 'test_operation'
        assert log_entry.details == 'Testing log entry creation'
        assert log_entry.step == 2
        assert log_entry.timestamp is not None

    def test_safe_state_update(self):
        """Test safe state update function."""
        
        # Create initial state
        initial_state = create_initial_state('session-123', 'form-456')
        raw_state = initial_state.model_dump()
        
        # Update with new data
        updates = {
            'core': {'step': 2},
            'lead_intelligence': {'current_score': 50}
        }
        
        updated_state = safe_state_update(raw_state, updates)
        
        # Verify updates were applied
        assert updated_state['core']['step'] == 2
        assert updated_state['lead_intelligence']['current_score'] == 50
        
        # Verify other data preserved
        assert updated_state['core']['session_id'] == 'session-123'

    def test_extract_api_response_data(self):
        """Test API response data extraction."""
        
        # Create state with data
        state = create_initial_state('session-123', 'form-456')
        state.lead_intelligence.current_score = 75
        state.engagement.step_headline = 'Great job!'
        state.engagement.abandonment_risk = 0.2
        
        raw_state = state.model_dump()
        
        # Extract API response data
        api_data = extract_api_response_data(raw_state)
        
        assert api_data['session_id'] == 'session-123'
        assert api_data['current_score'] == 75
        assert api_data['headline'] == 'Great job!'
        assert api_data['abandonment_risk'] == 0.2
        assert api_data['lead_status'] == 'unknown'

    def test_type_safety_benefits(self):
        """Demonstrate type safety benefits of Pydantic models."""
        
        # This would be caught at validation time, not runtime
        with pytest.raises(ValidationError):
            CoreSurveyState(
                session_id=123,  # Should be string, not int
                form_id='form-123',
                started_at=datetime.now().isoformat(),
                last_updated=datetime.now().isoformat(),
                step='invalid',  # Should be int, not string
            )

    def test_default_values_and_optional_fields(self):
        """Test that default values and optional fields work correctly."""
        
        # Create state with minimal required fields
        core_state = CoreSurveyState(
            session_id='test-123',
            form_id='form-456',
            started_at=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat()
        )
        
        # Verify defaults
        assert core_state.step == 0  # Default value
        assert core_state.completed is False  # Default value
        assert core_state.utm_source is None  # Optional field
        assert core_state.client_id is None  # Optional field

    def test_model_serialization(self):
        """Test that models can be properly serialized and deserialized."""
        
        # Create state
        original_state = create_initial_state('session-123', 'form-456')
        
        # Serialize to dict
        serialized = original_state.model_dump()
        
        # Deserialize back to model
        deserialized = SurveyGraphState(**serialized)
        
        # Verify equality
        assert deserialized.core.session_id == original_state.core.session_id
        assert deserialized.core.form_id == original_state.core.form_id
        assert deserialized.lead_intelligence.lead_status == original_state.lead_intelligence.lead_status

    def test_model_validation_catches_data_corruption(self):
        """Test that validation catches data corruption issues."""
        
        # Simulate corrupted state data
        corrupted_state = {
            'core': {
                'session_id': None,  # Should not be None
                'form_id': '',  # Could be invalid
                'started_at': 'invalid-date',  # Invalid format
                'last_updated': datetime.now().isoformat(),
                'step': -1,  # Invalid step number
                'completed': 'yes'  # Should be boolean
            },
            'lead_intelligence': {
                'current_score': 'high',  # Should be int
                'lead_status': 'invalid_status'  # Invalid enum value
            }
        }
        
        # Validation should catch these issues
        validated, raw = validate_and_extract_state(corrupted_state)
        assert validated is None  # Validation should fail
        assert raw == corrupted_state  # But raw data preserved for fallback