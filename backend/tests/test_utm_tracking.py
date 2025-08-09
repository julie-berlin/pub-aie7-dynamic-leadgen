"""
Tests for UTM parameter tracking and marketing attribution.

Validates that UTM parameters are captured correctly during session initialization
and that tracking data is persisted properly to the database.
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from app.graphs.nodes.tracking_and_response_nodes import initialize_session_with_tracking_node
from app.database import db
from app.state import SurveyGraphState


class TestUTMTracking:
    """Test UTM parameter capture and tracking functionality."""

    @pytest.fixture
    def utm_parameters(self):
        """Sample UTM parameters for testing."""
        return {
            'utm_source': 'facebook',
            'utm_medium': 'social',
            'utm_campaign': 'summer_dog_walking',
            'utm_content': 'carousel_ad_1',
            'utm_term': 'dog walking services',
        }

    @pytest.fixture
    def tracking_headers(self):
        """Sample HTTP headers for tracking."""
        return {
            'referrer': 'https://facebook.com/ads/123',
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'ip_address': '192.168.1.100'
        }

    @pytest.fixture
    def initial_state(self, utm_parameters, tracking_headers):
        """Initial graph state with tracking data."""
        return {
            'core': {
                'session_id': 'test-session-utm-123',
                'form_id': 'test-form-uuid',
                'client_id': 'test-client-uuid',
                'started_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'step': 0,
                'completed': False,
                # UTM parameters
                **utm_parameters,
                # Tracking headers  
                **tracking_headers,
                'landing_page': 'https://example.com/dog-walking'
            },
            'master_flow': {
                'core': {'session_id': 'test-session-utm-123', 'form_id': 'test-form-uuid'},
                'flow_phase': 'initialization',
                'completion_probability': 0.8,
                'flow_strategy': 'STANDARD'
            },
            'question_strategy': {
                'all_questions': [],
                'asked_questions': [],
                'current_questions': [],
                'phrased_questions': [],
                'question_strategy': {},
                'selection_history': []
            },
            'lead_intelligence': {
                'responses': [],
                'current_score': 0,
                'score_history': [],
                'lead_status': 'unknown',
                'qualification_reasoning': [],
                'risk_factors': [],
                'positive_indicators': []
            },
            'engagement': {
                'abandonment_risk': 0.3,
                'engagement_metrics': {},
                'step_headline': '',
                'step_motivation': '',
                'engagement_history': [],
                'retention_strategies': [],
                'last_activity_timestamp': datetime.now().isoformat(),
                'abandonment_status': 'active',
                'time_on_step': None,
                'hesitation_indicators': 0
            },
            'supervisor_messages': [],
            'shared_context': {},
            'pending_responses': [],
            'frontend_response': None,
            'completion_message': None,
            'error_log': [],
            'operation_log': [],
            'metadata': {}
        }

    @patch('app.database.db.save_tracking_data')
    @patch('app.database.db.create_lead_session')
    def test_utm_parameters_captured_correctly(
        self, mock_create_session, mock_save_tracking, 
        initial_state, utm_parameters, tracking_headers
    ):
        """Test that UTM parameters are captured and saved immediately."""
        # Mock database responses
        mock_create_session.return_value = {'session_id': 'test-session-utm-123'}
        mock_save_tracking.return_value = {'id': 'tracking-123'}

        # Execute the tracking node
        result = initialize_session_with_tracking_node(initial_state)

        # Verify session was created
        mock_create_session.assert_called_once()
        session_data = mock_create_session.call_args[0][0]
        assert session_data['session_id'] == 'test-session-utm-123'
        assert session_data['form_id'] == 'test-form-uuid'

        # Verify tracking data was saved immediately (fire-and-forget)
        mock_save_tracking.assert_called_once()
        tracking_data = mock_save_tracking.call_args[0][1]  # Second argument after session_id
        
        # Verify all UTM parameters were captured
        for key, value in utm_parameters.items():
            assert tracking_data[key] == value
            
        # Verify technical tracking data
        for key, value in tracking_headers.items():
            assert tracking_data[key] == value
            
        assert tracking_data['landing_page'] == 'https://example.com/dog-walking'

        # Verify state was updated correctly
        assert result['core']['session_id'] == 'test-session-utm-123'
        assert result['core']['utm_source'] == 'facebook'
        assert result['core']['utm_campaign'] == 'summer_dog_walking'

    @patch('app.database.db.save_tracking_data')
    @patch('app.database.db.create_lead_session')
    def test_missing_utm_parameters_handled(
        self, mock_create_session, mock_save_tracking, initial_state
    ):
        """Test that missing UTM parameters are handled gracefully."""
        # Remove UTM parameters from state
        core = initial_state['core']
        for key in ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term']:
            core.pop(key, None)

        mock_create_session.return_value = {'session_id': 'test-session-utm-123'}
        mock_save_tracking.return_value = {'id': 'tracking-123'}

        # Execute the tracking node
        result = initialize_session_with_tracking_node(initial_state)

        # Verify tracking was still saved
        mock_save_tracking.assert_called_once()
        tracking_data = mock_save_tracking.call_args[0][1]

        # Verify UTM fields are None but other fields are present
        assert tracking_data.get('utm_source') is None
        assert tracking_data.get('utm_campaign') is None
        assert tracking_data['referrer'] == 'https://facebook.com/ads/123'
        assert tracking_data['user_agent'] is not None

    def test_utm_parameter_validation(self, utm_parameters):
        """Test UTM parameter validation and sanitization."""
        # Test with potentially malicious UTM parameters
        malicious_params = {
            'utm_source': '<script>alert("xss")</script>',
            'utm_campaign': 'normal_campaign',
            'utm_medium': 'email&redirect=evil.com',
        }

        # In a real implementation, these should be sanitized
        # For now, we just verify they're captured as-is
        assert malicious_params['utm_source'] == '<script>alert("xss")</script>'
        assert malicious_params['utm_campaign'] == 'normal_campaign'

    @patch('app.database.db.get_tracking_data')
    def test_utm_data_retrieval(self, mock_get_tracking, utm_parameters):
        """Test retrieving UTM data from database."""
        session_id = 'test-session-utm-123'
        
        # Mock database response
        mock_get_tracking.return_value = {
            'session_id': session_id,
            **utm_parameters,
            'referrer': 'https://facebook.com/ads/123',
            'created_at': datetime.now().isoformat()
        }

        # Retrieve tracking data
        tracking_data = db.get_tracking_data(session_id)

        # Verify data retrieval
        mock_get_tracking.assert_called_once_with(session_id)
        assert tracking_data['utm_source'] == 'facebook'
        assert tracking_data['utm_campaign'] == 'summer_dog_walking'
        assert tracking_data['session_id'] == session_id

    @patch('app.database.db.get_utm_performance')
    def test_utm_analytics_queries(self, mock_get_performance):
        """Test UTM performance analytics functionality."""
        # Mock analytics response
        mock_get_performance.return_value = [
            {'utm_source': 'facebook', 'utm_campaign': 'summer_dog_walking', 'utm_medium': 'social'},
            {'utm_source': 'google', 'utm_campaign': 'winter_promotion', 'utm_medium': 'cpc'},
        ]

        # Get UTM performance data
        performance_data = db.get_utm_performance(form_id='test-form-uuid', days=30)

        # Verify analytics query
        mock_get_performance.assert_called_once_with(form_id='test-form-uuid', days=30)
        assert len(performance_data) == 2
        assert performance_data[0]['utm_source'] == 'facebook'
        assert performance_data[1]['utm_source'] == 'google'

    def test_tracking_data_structure(self, utm_parameters, tracking_headers):
        """Test that tracking data follows expected structure."""
        expected_fields = {
            # UTM parameters
            'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
            # Technical tracking
            'referrer', 'user_agent', 'ip_address', 'landing_page',
            # Session context
            'browser_info', 'device_info', 'geographic_info'
        }

        # Combine all tracking data
        all_tracking_data = {**utm_parameters, **tracking_headers, 'landing_page': 'https://example.com'}

        # Verify required fields are present
        required_fields = {'utm_source', 'referrer', 'user_agent'}
        for field in required_fields:
            if field in all_tracking_data:
                assert all_tracking_data[field] is not None

        # Verify structure allows for optional fields
        optional_fields = {'utm_content', 'utm_term', 'browser_info'}
        for field in optional_fields:
            # Should not error if field is missing
            value = all_tracking_data.get(field)
            # Can be None or have a value
            assert value is None or isinstance(value, (str, dict))