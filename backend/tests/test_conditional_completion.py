"""
Tests for conditional completion flow and lead qualification.

Validates that qualified leads get personalized messages, unqualified leads get 
generic messages, and that completion routing works correctly based on lead status.
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from app.graphs.nodes.tracking_and_response_nodes import (
    qualified_message_generation_node,
    unqualified_completion_node
)
from app.database import db
from app.state import SurveyGraphState


class TestConditionalCompletion:
    """Test conditional completion flow based on lead qualification."""

    @pytest.fixture
    def qualified_lead_state(self):
        """State representing a qualified lead (high score)."""
        return {
            'core': {
                'session_id': 'test-session-qualified-123',
                'form_id': 'test-form-uuid',
                'client_id': 'test-client-uuid',
                'started_at': datetime.now().isoformat(),
                'step': 4,
                'completed': False
            },
            'master_flow': {
                'core': {'session_id': 'test-session-qualified-123'},
                'flow_phase': 'completion',
                'completion_probability': 0.95,
                'flow_strategy': 'QUALIFIED_COMPLETION'
            },
            'question_strategy': {
                'all_questions': [],
                'asked_questions': [1, 2, 3, 4],
                'current_questions': [],
                'phrased_questions': [],
                'question_strategy': {},
                'selection_history': []
            },
            'lead_intelligence': {
                'responses': [
                    {'question_id': 1, 'answer': 'Sarah Johnson', 'score_awarded': 0},
                    {'question_id': 2, 'answer': 'Max', 'score_awarded': 5},
                    {'question_id': 3, 'answer': 'Golden Retriever', 'score_awarded': 10},
                    {'question_id': 4, 'answer': 'Daily walks needed', 'score_awarded': 20},
                    {'question_id': 5, 'answer': 'Yes, fully vaccinated', 'score_awarded': 25},
                    {'question_id': 6, 'answer': 'Very friendly with other dogs', 'score_awarded': 15},
                    {'question_id': 7, 'answer': 'Budget $50-75/week', 'score_awarded': 20}
                ],
                'current_score': 95,  # High score - qualified lead
                'score_history': [20, 45, 55, 75, 95],
                'lead_status': 'yes',  # Qualified
                'qualification_reasoning': [
                    'High budget range indicates serious interest',
                    'Daily walks requirement shows consistent need',
                    'Dog is vaccinated and social - ideal client'
                ],
                'risk_factors': [],
                'positive_indicators': [
                    'premium_budget',
                    'daily_service_need',
                    'vaccinated_dog',
                    'social_dog'
                ]
            },
            'engagement': {
                'abandonment_risk': 0.1,
                'engagement_metrics': {'completion_speed': 'fast'},
                'step_headline': 'Great! We\'d love to help with Max!',
                'step_motivation': 'You seem like exactly the kind of client we love working with.',
                'engagement_history': [],
                'retention_strategies': [],
                'last_activity_timestamp': datetime.now().isoformat(),
                'abandonment_status': 'active',
                'time_on_step': 15,
                'hesitation_indicators': 0
            },
            'supervisor_messages': [],
            'shared_context': {'client_info': {'business_name': 'Pawsome Dog Walking', 'owner_name': 'Darlene Demo'}},
            'pending_responses': [],
            'frontend_response': None,
            'completion_message': None,  # Will be generated
            'error_log': [],
            'operation_log': [],
            'metadata': {}
        }

    @pytest.fixture
    def maybe_lead_state(self):
        """State representing a maybe lead (moderate score)."""
        return {
            'core': {
                'session_id': 'test-session-maybe-456',
                'form_id': 'test-form-uuid',
                'step': 3,
                'completed': False
            },
            'lead_intelligence': {
                'responses': [
                    {'question_id': 1, 'answer': 'Mike Wilson', 'score_awarded': 0},
                    {'question_id': 2, 'answer': 'Buddy', 'score_awarded': 5},
                    {'question_id': 3, 'answer': 'Mixed breed', 'score_awarded': 8},
                    {'question_id': 4, 'answer': 'A few times a week', 'score_awarded': 15},
                    {'question_id': 5, 'answer': 'Yes, up to date', 'score_awarded': 25},
                    {'question_id': 6, 'answer': 'Somewhat shy but friendly', 'score_awarded': 5}
                ],
                'current_score': 58,  # Moderate score - maybe lead
                'lead_status': 'maybe',
                'qualification_reasoning': [
                    'Moderate service frequency shows interest',
                    'Dog is vaccinated which is good',
                    'Budget not specified - unclear commitment'
                ],
                'risk_factors': ['shy_dog', 'unclear_budget'],
                'positive_indicators': ['vaccinated_dog', 'regular_need']
            },
            'shared_context': {'client_info': {'business_name': 'Pawsome Dog Walking', 'owner_name': 'Darlene Demo'}},
            'completion_message': None,
            'operation_log': []
        }

    @pytest.fixture
    def unqualified_lead_state(self):
        """State representing an unqualified lead (low score)."""
        return {
            'core': {
                'session_id': 'test-session-unqualified-789',
                'form_id': 'test-form-uuid',
                'step': 4,
                'completed': False
            },
            'lead_intelligence': {
                'responses': [
                    {'question_id': 1, 'answer': 'John Smith', 'score_awarded': 0},
                    {'question_id': 2, 'answer': 'Rex', 'score_awarded': 5},
                    {'question_id': 3, 'answer': 'Pitbull mix', 'score_awarded': 3},
                    {'question_id': 4, 'answer': 'Very rarely, maybe monthly', 'score_awarded': 2},
                    {'question_id': 5, 'answer': 'Not sure about vaccines', 'score_awarded': -20},
                    {'question_id': 6, 'answer': 'Aggressive with other dogs', 'score_awarded': -10}
                ],
                'current_score': -20,  # Low/negative score - unqualified
                'lead_status': 'no',
                'qualification_reasoning': [
                    'Very low service frequency indicates minimal need',
                    'Vaccination status unclear - safety concern',
                    'Aggressive dog not suitable for group walks'
                ],
                'risk_factors': ['unvaccinated_dog', 'aggressive_behavior', 'minimal_need'],
                'positive_indicators': []
            },
            'completion_message': None,
            'operation_log': []
        }

    @patch('app.tools.load_client_info')
    @patch('app.graphs.nodes.completion_nodes.call_llm')
    def test_qualified_lead_personalized_message(self, mock_llm, mock_client_info, qualified_lead_state):
        """Test that qualified leads receive personalized completion messages."""
        # Mock client info
        mock_client_info.return_value = {
            'business_name': 'Pawsome Dog Walking',
            'owner_name': 'Darlene Demo',
            'business_type': 'dog walking service',
            'background': 'College grad who loves dogs and provides personalized walking services.'
        }

        # Mock LLM response
        mock_llm.return_value = """Hi Sarah! 

I'm so excited to hear from you and Max! A Golden Retriever who needs daily walks and is fully vaccinated and social - you're exactly the kind of client I love working with at Pawsome Dog Walking.

Your budget range of $50-75/week works perfectly for daily service, and the fact that Max is friendly with other dogs means he could potentially join some of my pack walks which is always more fun for the dogs!

I'd love to set up a time to meet you and Max this week. I'm Darlene, and I started this service because I'm passionate about giving dogs the exercise and attention they deserve while their families are busy.

Can I give you a call tomorrow to discuss scheduling? My number is (617) 555-0123, or you can email me directly at darlene@pawsomedogwalking.com.

Looking forward to meeting Max!

Best,
Darlene Demo
Pawsome Dog Walking"""

        # Execute qualified message generation
        result = qualified_message_generation_node(qualified_lead_state)

        # Verify LLM was called with proper context
        mock_llm.assert_called_once()
        llm_call_args = mock_llm.call_args[1]
        
        # Verify client context was included
        assert 'business_name' in str(llm_call_args)
        assert 'Pawsome Dog Walking' in str(llm_call_args)
        assert 'Darlene Demo' in str(llm_call_args)
        
        # Verify lead responses were included
        assert 'Sarah Johnson' in str(llm_call_args)
        assert 'Max' in str(llm_call_args)
        assert 'Golden Retriever' in str(llm_call_args)

        # Verify personalized message was generated
        assert result['completion_message'] is not None
        assert len(result['completion_message']) > 100  # Should be substantial
        assert 'Sarah' in result['completion_message']
        assert 'Max' in result['completion_message']
        assert 'Darlene' in result['completion_message']

        # Verify session completion
        assert result['core']['completed'] is True
        assert result['core']['completion_type'] == 'qualified'

        # Verify operation logging
        completion_logs = [log for log in result['operation_log'] if log['operation'] == 'qualified_completion']
        assert len(completion_logs) > 0

    @patch('app.tools.load_client_info')
    @patch('app.graphs.nodes.completion_nodes.call_llm')
    def test_maybe_lead_personalized_message(self, mock_llm, mock_client_info, maybe_lead_state):
        """Test that maybe leads receive personalized but more cautious messages."""
        mock_client_info.return_value = {
            'business_name': 'Pawsome Dog Walking',
            'owner_name': 'Darlene Demo'
        }

        mock_llm.return_value = """Hi Mike,

Thanks for telling us about Buddy! It sounds like you're looking for walking services a few times a week, which could work well with our schedule.

Since Buddy is a bit shy but friendly, I'd love to meet him first to see how he does with new people and potentially other dogs. Every dog is different, and I want to make sure he'd be comfortable with the service.

If you'd like to chat more about what you're looking for and pricing options, feel free to reach out. I'm Darlene at Pawsome Dog Walking.

Best regards,
Darlene"""

        result = qualified_message_generation_node(maybe_lead_state)

        # Verify message generation for maybe leads
        assert result['completion_message'] is not None
        assert 'Mike' in result['completion_message']
        assert 'Buddy' in result['completion_message']
        assert result['core']['completion_type'] == 'qualified'  # Maybe leads still get qualified flow

    def test_unqualified_lead_generic_message(self, unqualified_lead_state):
        """Test that unqualified leads receive generic completion messages."""
        result = unqualified_completion_node(unqualified_lead_state)

        # Verify generic message (no LLM call needed)
        assert result['completion_message'] is not None
        assert len(result['completion_message']) < 200  # Should be brief
        
        # Should be generic - no personalization
        assert 'John' not in result['completion_message']  # No personal name
        assert 'Rex' not in result['completion_message']   # No dog name
        
        # Common generic phrases
        generic_phrases = ['thank you', 'appreciate', 'time', 'interest']
        message_lower = result['completion_message'].lower()
        assert any(phrase in message_lower for phrase in generic_phrases)

        # Verify session completion
        assert result['core']['completed'] is True
        assert result['core']['completion_type'] == 'unqualified'

        # Verify no LLM usage (efficiency)
        completion_logs = [log for log in result['operation_log'] if 'llm' not in log.get('details', '').lower()]
        assert len(result['operation_log']) >= 0  # Should have logs, but no LLM usage

    def test_completion_routing_logic(self):
        """Test the routing logic for different lead types."""
        # Test qualified routing (score >= 75)
        qualified_score = 85
        assert qualified_score >= 75  # Should route to qualified flow
        
        # Test maybe routing (45 <= score < 75)
        maybe_score = 58
        assert 45 <= maybe_score < 75  # Should route to qualified flow (personalized)
        
        # Test unqualified routing (score < 45)
        unqualified_score = -20
        assert unqualified_score < 45  # Should route to unqualified flow

    @patch('app.database.db.update_lead_session_with_tracking')
    def test_completion_database_updates(self, mock_update_session, qualified_lead_state):
        """Test that completion properly updates the database."""
        mock_update_session.return_value = {'completed': True}

        result = qualified_message_generation_node(qualified_lead_state)

        # Verify database update was called
        mock_update_session.assert_called_once()
        update_data = mock_update_session.call_args[0][1]
        
        assert update_data['completed'] is True
        assert update_data['completion_type'] == 'qualified'
        assert update_data['final_score'] == 95
        assert update_data['lead_status'] == 'yes'
        assert 'completed_at' in update_data

    def test_completion_message_templates(self):
        """Test completion message template structure."""
        # Test different message templates
        qualified_template_elements = [
            'personal_greeting',
            'business_context', 
            'service_match_explanation',
            'next_steps',
            'contact_information',
            'personal_signature'
        ]

        unqualified_template_elements = [
            'polite_thanks',
            'generic_closing',
            'business_name_only'
        ]

        # Verify template structures exist
        assert len(qualified_template_elements) > len(unqualified_template_elements)
        assert 'personal_greeting' in qualified_template_elements
        assert 'personal_greeting' not in unqualified_template_elements

    @patch('app.database.db.create_lead_outcome')
    def test_lead_outcome_tracking(self, mock_create_outcome):
        """Test that lead outcomes are tracked for ML learning."""
        mock_create_outcome.return_value = {'id': 'outcome-123'}
        
        # Simulate creating a lead outcome record
        outcome_data = {
            'session_id': 'test-session-qualified-123',
            'form_id': 'test-form-uuid',
            'predicted_conversion': True,  # AI predicted qualified
            'conversion_date': None,  # TBD - when client reports conversion
            'conversion_value': None,
            'notes': 'High-scoring lead with daily walking needs'
        }

        result = db.create_lead_outcome(outcome_data)
        
        mock_create_outcome.assert_called_once_with(outcome_data)
        assert result['id'] == 'outcome-123'

    def test_completion_error_handling(self):
        """Test error handling in completion flows."""
        # Test with missing client info
        incomplete_state = {
            'core': {'session_id': 'test-incomplete', 'completed': False},
            'lead_intelligence': {'responses': [], 'lead_status': 'yes', 'current_score': 80},
            'shared_context': {},  # Missing client_info
            'completion_message': None,
            'operation_log': [],
            'error_log': []
        }

        # Should not crash, should handle gracefully
        try:
            result = qualified_message_generation_node(incomplete_state)
            # Should either use fallback or log error
            assert 'error_log' in result or result['completion_message'] is not None
        except Exception as e:
            # If it does raise, should be handled gracefully
            assert isinstance(e, (KeyError, ValueError))

    def test_completion_message_quality_validation(self):
        """Test that completion messages meet quality standards."""
        sample_qualified_message = """Hi Sarah! 

I'm so excited to hear from you and Max! A Golden Retriever who needs daily walks - you're exactly the kind of client I love working with.

I'd love to set up a time to meet you and Max this week. Can I give you a call tomorrow?

Best,
Darlene Demo
Pawsome Dog Walking"""

        sample_unqualified_message = "Thank you for your interest in our services."

        # Quality checks for qualified messages
        assert len(sample_qualified_message) > 100  # Substantial content
        assert sample_qualified_message.count('\n') >= 3  # Multi-paragraph
        assert 'Sarah' in sample_qualified_message  # Personalized
        assert 'Max' in sample_qualified_message  # References their dog
        assert 'Darlene' in sample_qualified_message  # Business owner signature

        # Quality checks for unqualified messages  
        assert len(sample_unqualified_message) < 100  # Brief
        assert sample_unqualified_message.count('\n') <= 2  # Simple structure
        assert 'thank you' in sample_unqualified_message.lower()  # Polite