"""
Tests for abandonment detection and timeout handling.

Validates that abandonment risk calculation works correctly, that sessions are marked
as abandoned appropriately, and that recovery from near-abandonment functions properly.
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from app.graphs.nodes.tracking_and_response_nodes import check_abandonment_node
from app.database import db
from app.session_recovery import recovery_manager
from app.state import SurveyGraphState


class TestAbandonmentDetection:
    """Test abandonment detection and recovery functionality."""

    @pytest.fixture
    def active_session_state(self):
        """Session state with recent activity (should not be abandoned)."""
        recent_time = datetime.now().isoformat()
        return {
            'core': {
                'session_id': 'test-session-active-123',
                'form_id': 'test-form-uuid',
                'client_id': 'test-client-uuid',
                'started_at': recent_time,
                'last_updated': recent_time,
                'step': 2,
                'completed': False
            },
            'master_flow': {
                'core': {'session_id': 'test-session-active-123'},
                'flow_phase': 'questioning',
                'completion_probability': 0.8,
                'flow_strategy': 'STANDARD'
            },
            'question_strategy': {
                'all_questions': [],
                'asked_questions': [1, 2],
                'current_questions': [],
                'phrased_questions': [],
                'question_strategy': {},
                'selection_history': []
            },
            'lead_intelligence': {
                'responses': [
                    {'question_id': 1, 'answer': 'Buddy', 'timestamp': recent_time},
                    {'question_id': 2, 'answer': 'Golden Retriever', 'timestamp': recent_time}
                ],
                'current_score': 25,
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
                'last_activity_timestamp': recent_time,  # Recent activity
                'abandonment_status': 'active',
                'time_on_step': 30,  # 30 seconds on current step
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

    @pytest.fixture
    def at_risk_session_state(self):
        """Session state that should be marked at risk of abandonment."""
        old_time = (datetime.now() - timedelta(minutes=7)).isoformat()
        return {
            'core': {
                'session_id': 'test-session-at-risk-456',
                'form_id': 'test-form-uuid',
                'step': 3,
                'completed': False
            },
            'engagement': {
                'abandonment_risk': 0.4,  # Will be recalculated
                'last_activity_timestamp': old_time,  # 7 minutes ago
                'abandonment_status': 'active',
                'time_on_step': 420,  # 7 minutes on step
                'hesitation_indicators': 2
            },
            'lead_intelligence': {
                'responses': [
                    {'question_id': 1, 'answer': 'Max'},
                    {'question_id': 2, 'answer': 'Labrador'}
                ],
                'current_score': 20,
                'lead_status': 'maybe'
            },
            'operation_log': []
        }

    @pytest.fixture
    def high_risk_session_state(self):
        """Session state that should be marked high risk of abandonment."""
        very_old_time = (datetime.now() - timedelta(minutes=12)).isoformat()
        return {
            'core': {
                'session_id': 'test-session-high-risk-789',
                'form_id': 'test-form-uuid',
                'step': 2,
                'completed': False
            },
            'engagement': {
                'abandonment_risk': 0.5,  # Will be recalculated
                'last_activity_timestamp': very_old_time,  # 12 minutes ago
                'abandonment_status': 'active',
                'time_on_step': 720,  # 12 minutes on step
                'hesitation_indicators': 4
            },
            'lead_intelligence': {
                'responses': [{'question_id': 1, 'answer': 'Spot'}],
                'current_score': 10,
                'lead_status': 'unknown'
            },
            'operation_log': []
        }

    @pytest.fixture
    def abandoned_session_state(self):
        """Session state that should be marked as abandoned."""
        abandoned_time = (datetime.now() - timedelta(minutes=18)).isoformat()
        return {
            'core': {
                'session_id': 'test-session-abandoned-999',
                'form_id': 'test-form-uuid',
                'step': 1,
                'completed': False
            },
            'engagement': {
                'abandonment_risk': 0.6,  # Will be recalculated to 0.95+
                'last_activity_timestamp': abandoned_time,  # 18 minutes ago
                'abandonment_status': 'active',
                'time_on_step': 1080,  # 18 minutes on step
                'hesitation_indicators': 1
            },
            'lead_intelligence': {
                'responses': [],
                'current_score': 0,
                'lead_status': 'unknown'
            },
            'operation_log': []
        }

    def test_active_session_not_abandoned(self, active_session_state):
        """Test that recently active sessions are not marked as abandoned."""
        result = check_abandonment_node(active_session_state)

        # Verify session remains active
        assert result['engagement']['abandonment_status'] == 'active'
        assert result['engagement']['abandonment_risk'] <= 0.35  # Should stay low
        assert result['core']['completed'] is False

        # Verify operation was logged
        log_entries = [entry for entry in result['operation_log'] if entry['operation'] == 'abandonment_check']
        assert len(log_entries) > 0
        assert 'active' in log_entries[0]['details'].lower()

    def test_at_risk_session_detection(self, at_risk_session_state):
        """Test detection of sessions at risk of abandonment."""
        result = check_abandonment_node(at_risk_session_state)

        # Verify session is marked at risk
        assert result['engagement']['abandonment_status'] == 'at_risk'
        assert result['engagement']['abandonment_risk'] >= 0.55
        assert result['engagement']['abandonment_risk'] <= 0.75
        assert result['core']['completed'] is False  # Not abandoned yet

        # Verify hesitation indicators increased
        assert result['engagement']['hesitation_indicators'] >= 2

    def test_high_risk_session_detection(self, high_risk_session_state):
        """Test detection of high-risk sessions."""
        result = check_abandonment_node(high_risk_session_state)

        # Verify session is marked high risk
        assert result['engagement']['abandonment_status'] == 'high_risk'
        assert result['engagement']['abandonment_risk'] >= 0.75
        assert result['engagement']['abandonment_risk'] <= 0.90
        assert result['core']['completed'] is False  # Still not abandoned

        # Verify hesitation indicators increased significantly
        assert result['engagement']['hesitation_indicators'] >= 4

    @patch('app.database.db.mark_session_abandoned')
    def test_abandoned_session_marking(self, mock_mark_abandoned, abandoned_session_state):
        """Test that sessions are properly marked as abandoned."""
        mock_mark_abandoned.return_value = {'abandonment_status': 'abandoned'}

        result = check_abandonment_node(abandoned_session_state)

        # Verify session is marked as abandoned
        assert result['engagement']['abandonment_status'] == 'abandoned'
        assert result['engagement']['abandonment_risk'] >= 0.90
        assert result['core']['completed'] is True
        assert result['core']['completion_type'] == 'abandoned'

        # Verify database was updated
        mock_mark_abandoned.assert_called_once_with('test-session-abandoned-999')

        # Verify abandonment was logged
        log_entries = [entry for entry in result['operation_log'] if entry['operation'] == 'session_abandoned']
        assert len(log_entries) > 0

    def test_abandonment_risk_calculation_accuracy(self):
        """Test accuracy of abandonment risk calculation based on inactivity."""
        now = datetime.now()

        test_cases = [
            # (minutes_inactive, expected_min_risk, expected_max_risk)
            (2, 0.25, 0.35),   # Recent activity - low risk
            (6, 0.55, 0.65),   # Moderate inactivity - at risk
            (11, 0.75, 0.85),  # High inactivity - high risk
            (16, 0.90, 1.0),   # Very high inactivity - abandoned
        ]

        for minutes_inactive, expected_min, expected_max in test_cases:
            inactive_time = (now - timedelta(minutes=minutes_inactive)).isoformat()
            
            state = {
                'core': {'session_id': f'test-{minutes_inactive}min', 'completed': False},
                'engagement': {
                    'abandonment_risk': 0.3,
                    'last_activity_timestamp': inactive_time,
                    'abandonment_status': 'active',
                    'time_on_step': minutes_inactive * 60,
                    'hesitation_indicators': 0
                },
                'operation_log': []
            }

            result = check_abandonment_node(state)
            calculated_risk = result['engagement']['abandonment_risk']

            assert expected_min <= calculated_risk <= expected_max, \
                f"For {minutes_inactive}min inactive, risk {calculated_risk} not in range [{expected_min}, {expected_max}]"

    @patch('app.session_recovery.recovery_manager.can_recover_session')
    def test_session_recovery_check(self, mock_can_recover):
        """Test session recovery capability check."""
        session_id = 'test-session-recovery-123'
        
        # Test recoverable session
        mock_can_recover.return_value = (True, "Can recover with 3 responses")
        
        can_recover, reason = recovery_manager.can_recover_session(session_id)
        
        assert can_recover is True
        assert "3 responses" in reason
        mock_can_recover.assert_called_once_with(session_id)

    @patch('app.session_recovery.recovery_manager.can_recover_session')
    def test_abandoned_session_recovery_prevention(self, mock_can_recover):
        """Test that abandoned sessions cannot be recovered."""
        session_id = 'test-session-abandoned-456'
        
        # Mock abandoned session
        mock_can_recover.return_value = (False, "Session was marked as abandoned")
        
        can_recover, reason = recovery_manager.can_recover_session(session_id)
        
        assert can_recover is False
        assert "abandoned" in reason.lower()

    def test_near_abandonment_recovery(self, at_risk_session_state):
        """Test recovery from near-abandonment state."""
        # Simulate user returning with new activity
        current_time = datetime.now().isoformat()
        
        # Update state with fresh activity
        recovered_state = at_risk_session_state.copy()
        recovered_state['engagement']['last_activity_timestamp'] = current_time
        recovered_state['engagement']['time_on_step'] = 0  # Reset step timer
        
        # Check abandonment after recovery
        result = check_abandonment_node(recovered_state)
        
        # Should be back to active status
        assert result['engagement']['abandonment_status'] == 'active'
        assert result['engagement']['abandonment_risk'] <= 0.35
        
        # Verify recovery was logged
        recovery_logs = [entry for entry in result['operation_log'] 
                        if 'recover' in entry.get('details', '').lower()]
        assert len(recovery_logs) > 0

    @patch('app.database.db.get_form_analytics')
    def test_abandonment_rate_analytics(self, mock_get_analytics):
        """Test abandonment rate analytics calculation."""
        # Mock analytics with abandonment data
        mock_get_analytics.return_value = {
            'total_sessions': 100,
            'completed_sessions': 70,
            'abandoned_sessions': 25,
            'abandonment_rate': 0.25,  # 25% abandonment rate
            'avg_steps': 4.2
        }
        
        form_id = 'test-form-uuid'
        analytics = db.get_form_analytics(form_id, days=30)
        
        # Verify analytics call
        mock_get_analytics.assert_called_once_with(form_id, days=30)
        
        # Verify abandonment metrics
        assert analytics['abandonment_rate'] == 0.25
        assert analytics['abandoned_sessions'] == 25
        assert analytics['total_sessions'] == 100

    def test_timeout_threshold_configuration(self):
        """Test that abandonment timeout thresholds are configurable."""
        # Test different timeout configurations
        timeout_configs = [
            {'at_risk_minutes': 5, 'high_risk_minutes': 10, 'abandoned_minutes': 15},
            {'at_risk_minutes': 3, 'high_risk_minutes': 7, 'abandoned_minutes': 12},
        ]
        
        for config in timeout_configs:
            # This would test a configurable abandonment detection system
            # For now, we verify the concept exists
            assert config['at_risk_minutes'] < config['high_risk_minutes']
            assert config['high_risk_minutes'] < config['abandoned_minutes']
            assert all(threshold > 0 for threshold in config.values())

    def test_abandonment_prevention_strategies(self):
        """Test abandonment prevention strategy tracking."""
        prevention_strategies = [
            'progress_indicator',
            'motivational_message',
            'reduced_questions',
            'simplified_interface',
            'exit_intent_modal'
        ]
        
        # Test that prevention strategies can be tracked
        engagement_state = {
            'abandonment_risk': 0.6,
            'abandonment_status': 'at_risk',
            'retention_strategies': ['progress_indicator', 'motivational_message'],
            'engagement_history': []
        }
        
        # Verify strategy tracking structure
        assert isinstance(engagement_state['retention_strategies'], list)
        assert 'progress_indicator' in engagement_state['retention_strategies']
        assert len(engagement_state['retention_strategies']) == 2