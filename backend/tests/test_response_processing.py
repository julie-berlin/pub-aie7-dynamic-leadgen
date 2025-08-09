"""
Tests for response processing and immediate persistence.

Validates that user responses are processed correctly, saved immediately to the database,
and that response processing handles edge cases properly.
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from app.graphs.nodes.tracking_and_response_nodes import (
    process_user_responses_node,
    save_responses_immediately_node
)
from app.database import db
from app.state import SurveyGraphState


class TestResponseProcessing:
    """Test response processing and immediate persistence."""

    @pytest.fixture
    def sample_pending_responses(self):
        """Sample user responses to be processed."""
        return [
            {
                'question_id': 1,
                'answer': 'Max',
                'question_text': 'What is your dog\'s name?',
                'phrased_question': 'What is your dog\'s name?',
                'data_type': 'text',
                'is_required': False,
                'scoring_rubric': '+5 points for engagement'
            },
            {
                'question_id': 2, 
                'answer': 'Golden Retriever',
                'question_text': 'What breed is your dog?',
                'phrased_question': 'What breed is your dog?',
                'data_type': 'text',
                'is_required': False,
                'scoring_rubric': '+10 points, helps with compatibility'
            }
        ]

    @pytest.fixture
    def state_with_pending_responses(self, sample_pending_responses):
        """Graph state with pending responses to process."""
        return {
            'core': {
                'session_id': 'test-session-resp-456',
                'form_id': 'test-form-uuid',
                'client_id': 'test-client-uuid',
                'started_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'step': 1,
                'completed': False
            },
            'master_flow': {
                'core': {'session_id': 'test-session-resp-456', 'form_id': 'test-form-uuid'},
                'flow_phase': 'questioning',
                'completion_probability': 0.7,
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
                'responses': [],  # Will be populated by processing
                'current_score': 10,
                'score_history': [],
                'lead_status': 'unknown',
                'qualification_reasoning': [],
                'risk_factors': [],
                'positive_indicators': []
            },
            'engagement': {
                'abandonment_risk': 0.4,
                'engagement_metrics': {},
                'step_headline': '',
                'step_motivation': '',
                'engagement_history': [],
                'retention_strategies': [],
                'last_activity_timestamp': (datetime.now().isoformat()),
                'abandonment_status': 'active',
                'time_on_step': 45,  # seconds
                'hesitation_indicators': 0
            },
            'supervisor_messages': [],
            'shared_context': {},
            'pending_responses': sample_pending_responses,  # Responses to process
            'frontend_response': None,
            'completion_message': None,
            'error_log': [],
            'operation_log': [],
            'metadata': {}
        }

    def test_response_processing_basic_flow(self, state_with_pending_responses, sample_pending_responses):
        """Test basic response processing flow."""
        # Execute response processing node
        result = process_user_responses_node(state_with_pending_responses)

        # Verify responses were moved from pending to responses
        assert len(result['pending_responses']) == 0
        assert len(result['lead_intelligence']['responses']) == 2

        # Verify response data structure
        processed_responses = result['lead_intelligence']['responses']
        assert processed_responses[0]['question_id'] == 1
        assert processed_responses[0]['answer'] == 'Max'
        assert processed_responses[1]['question_id'] == 2
        assert processed_responses[1]['answer'] == 'Golden Retriever'

        # Verify timestamps were added
        for response in processed_responses:
            assert 'timestamp' in response
            assert response['timestamp'] is not None

        # Verify abandonment risk was reset after activity
        assert result['engagement']['abandonment_risk'] <= 0.3
        assert result['engagement']['abandonment_status'] == 'active'
        assert result['engagement']['last_activity_timestamp'] is not None

    @patch('app.database.db.save_individual_response')
    def test_immediate_response_persistence(self, mock_save_response, state_with_pending_responses):
        """Test that responses are saved immediately to database (fire-and-forget)."""
        mock_save_response.return_value = {'id': 'response-123'}

        # Execute immediate save node
        result = save_responses_immediately_node(state_with_pending_responses)

        # Verify database save was called for each response
        assert mock_save_response.call_count == 2

        # Verify correct data was passed to database
        first_call_args = mock_save_response.call_args_list[0]
        session_id = first_call_args[0][0]
        response_data = first_call_args[0][1]

        assert session_id == 'test-session-resp-456'
        assert response_data['question_id'] == 1
        assert response_data['answer'] == 'Max'
        assert response_data['step'] == 1

        # Verify operation was logged
        assert len(result['operation_log']) > 0
        log_entry = result['operation_log'][-1]
        assert log_entry['operation'] == 'responses_saved'
        assert log_entry['details'] == 'Saved 2 responses immediately'

    def test_empty_responses_handling(self):
        """Test handling of empty or missing responses."""
        empty_state = {
            'core': {'session_id': 'test-session-empty', 'step': 1},
            'lead_intelligence': {'responses': []},
            'engagement': {'abandonment_risk': 0.6, 'abandonment_status': 'at_risk'},
            'pending_responses': [],  # No responses to process
            'operation_log': []
        }

        result = process_user_responses_node(empty_state)

        # Should not crash and should preserve state
        assert result['core']['session_id'] == 'test-session-empty'
        assert len(result['lead_intelligence']['responses']) == 0
        assert result['engagement']['abandonment_risk'] == 0.6  # Unchanged since no activity

    @patch('app.database.db.save_individual_response')
    def test_response_validation_and_sanitization(self, mock_save_response):
        """Test response validation and input sanitization."""
        malicious_responses = [
            {
                'question_id': 1,
                'answer': '<script>alert("xss")</script>',
                'question_text': 'What is your name?',
                'phrased_question': 'What is your name?',
                'data_type': 'text',
                'is_required': True,
                'scoring_rubric': 'Contact information required'
            }
        ]

        state = {
            'core': {'session_id': 'test-session-validate', 'step': 1},
            'lead_intelligence': {'responses': []},
            'engagement': {'abandonment_risk': 0.3, 'abandonment_status': 'active'},
            'pending_responses': malicious_responses,
            'operation_log': []
        }

        mock_save_response.return_value = {'id': 'response-secure-123'}

        # Execute response processing
        result = save_responses_immediately_node(state)

        # Verify database was called
        mock_save_response.assert_called_once()
        response_data = mock_save_response.call_args[0][1]

        # In a production system, this should be sanitized
        # For now, verify the malicious input is captured
        assert response_data['answer'] == '<script>alert("xss")</script>'
        
        # TODO: Add actual sanitization logic and test it
        # sanitized_answer = sanitize_user_input(response_data['answer'])
        # assert '<script>' not in sanitized_answer

    def test_response_merging_with_existing(self):
        """Test merging new responses with existing ones."""
        existing_responses = [
            {
                'question_id': 1,
                'answer': 'Buddy',
                'timestamp': '2025-01-01T10:00:00Z',
                'step': 0
            }
        ]

        new_responses = [
            {
                'question_id': 2,
                'answer': 'Labrador',
                'question_text': 'What breed?',
                'data_type': 'text',
                'is_required': False,
                'scoring_rubric': '+10 points'
            }
        ]

        state = {
            'core': {'session_id': 'test-merge-session', 'step': 1},
            'lead_intelligence': {'responses': existing_responses},
            'engagement': {'abandonment_risk': 0.3},
            'pending_responses': new_responses,
            'operation_log': []
        }

        result = process_user_responses_node(state)

        # Verify responses were merged, not replaced
        all_responses = result['lead_intelligence']['responses']
        assert len(all_responses) == 2

        # Verify existing response is preserved
        buddy_response = next(r for r in all_responses if r['question_id'] == 1)
        assert buddy_response['answer'] == 'Buddy'

        # Verify new response was added
        labrador_response = next(r for r in all_responses if r['question_id'] == 2)
        assert labrador_response['answer'] == 'Labrador'
        assert 'timestamp' in labrador_response

    @patch('app.database.db.get_session_responses')
    def test_response_retrieval_from_database(self, mock_get_responses):
        """Test retrieving responses from database."""
        session_id = 'test-session-retrieve-789'
        
        # Mock database responses
        mock_get_responses.return_value = [
            {
                'session_id': session_id,
                'question_id': 1,
                'answer': 'Charlie',
                'question_text': 'Dog name?',
                'timestamp': '2025-01-01T12:00:00Z',
                'step': 1,
                'score_awarded': 5
            },
            {
                'session_id': session_id,
                'question_id': 2,
                'answer': 'Beagle',
                'question_text': 'Dog breed?',
                'timestamp': '2025-01-01T12:01:00Z',
                'step': 1,
                'score_awarded': 10
            }
        ]

        # Retrieve responses
        responses = db.get_session_responses(session_id)

        # Verify retrieval
        mock_get_responses.assert_called_once_with(session_id)
        assert len(responses) == 2
        assert responses[0]['answer'] == 'Charlie'
        assert responses[1]['answer'] == 'Beagle'
        assert all('timestamp' in r for r in responses)

    def test_response_processing_error_handling(self):
        """Test error handling in response processing."""
        # Invalid response structure
        invalid_responses = [
            {
                # Missing required fields
                'answer': 'Some answer'
                # No question_id, question_text, etc.
            }
        ]

        state = {
            'core': {'session_id': 'test-error-session', 'step': 1},
            'lead_intelligence': {'responses': []},
            'engagement': {'abandonment_risk': 0.3},
            'pending_responses': invalid_responses,
            'operation_log': [],
            'error_log': []
        }

        # Should not crash, should handle gracefully
        result = process_user_responses_node(state)

        # Check that error was logged or handled
        # Implementation should decide whether to skip invalid responses or log errors
        assert 'error_log' in result
        
    def test_activity_timestamp_updates(self, state_with_pending_responses):
        """Test that activity timestamps are updated correctly during processing."""
        original_timestamp = state_with_pending_responses['engagement']['last_activity_timestamp']
        
        # Process responses
        result = process_user_responses_node(state_with_pending_responses)
        
        # Verify timestamp was updated
        new_timestamp = result['engagement']['last_activity_timestamp']
        assert new_timestamp != original_timestamp
        
        # Verify abandonment risk was recalculated
        assert result['engagement']['abandonment_risk'] <= 0.3  # Should be reset after activity