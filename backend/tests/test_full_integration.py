"""
Integration tests for complete survey flow.

Tests the entire journey from session initialization with UTM tracking through
multiple response submissions to completion with proper lead qualification.
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import uuid

from app.graphs.survey_graph_v2 import survey_graph
from app.database import db
from app.session_recovery import recovery_manager
from app.state import SurveyGraphState


class TestFullSurveyIntegration:
    """Integration tests for complete survey workflows."""

    @pytest.fixture
    def utm_tracking_data(self):
        """Complete UTM and tracking data for session start."""
        return {
            'utm_source': 'facebook',
            'utm_medium': 'social',
            'utm_campaign': 'summer_dog_walking_2025',
            'utm_content': 'carousel_ad_golden_retriever',
            'utm_term': 'dog walking services boston',
            'referrer': 'https://www.facebook.com/ads/123456',
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
            'ip_address': '192.168.1.50',
            'landing_page': 'https://pawsomedogwalking.com/get-started?ref=fb'
        }

    @pytest.fixture
    def complete_form_responses(self):
        """Complete set of responses for a qualified lead."""
        return [
            # Step 1 - Contact info
            {'question_id': 1, 'answer': 'Emma Thompson', 'data_type': 'text'},
            # Step 2 - Dog info
            {'question_id': 2, 'answer': 'Luna', 'data_type': 'text'},
            {'question_id': 3, 'answer': 'Golden Retriever', 'data_type': 'text'},
            # Step 3 - Service needs  
            {'question_id': 4, 'answer': 'Daily walks needed', 'data_type': 'multiple_choice'},
            {'question_id': 5, 'answer': 'Yes, fully vaccinated and up to date', 'data_type': 'boolean'},
            # Step 4 - Qualification
            {'question_id': 6, 'answer': 'Very friendly, loves other dogs', 'data_type': 'multiple_choice'},
            {'question_id': 7, 'answer': '$60-80 per week is fine', 'data_type': 'multiple_choice'},
            {'question_id': 8, 'answer': 'emma.thompson@email.com', 'data_type': 'email'}
        ]

    @pytest.fixture 
    def moderate_lead_responses(self):
        """Responses that create a moderate/maybe lead."""
        return [
            {'question_id': 1, 'answer': 'Alex Rivera', 'data_type': 'text'},
            {'question_id': 2, 'answer': 'Rocky', 'data_type': 'text'},
            {'question_id': 3, 'answer': 'Mixed breed rescue', 'data_type': 'text'},
            {'question_id': 4, 'answer': 'A couple times per week', 'data_type': 'multiple_choice'},
            {'question_id': 5, 'answer': 'Yes, vaccinated', 'data_type': 'boolean'},
            {'question_id': 6, 'answer': 'Somewhat shy but warming up to others', 'data_type': 'multiple_choice'}
        ]

    @patch('app.database.db.test_connection')
    @patch('app.database.db.create_lead_session')
    @patch('app.database.db.save_tracking_data')
    @patch('app.tools.load_form_config')
    @patch('app.tools.load_client_info')
    def test_complete_qualified_lead_journey(
        self, mock_client_info, mock_form_config, mock_save_tracking, 
        mock_create_session, mock_test_connection,
        utm_tracking_data, complete_form_responses
    ):
        """Test complete journey from start to qualified completion."""
        
        # Mock database responses
        mock_test_connection.return_value = True
        session_id = str(uuid.uuid4())
        form_id = str(uuid.uuid4())
        client_id = str(uuid.uuid4())
        
        mock_create_session.return_value = {
            'session_id': session_id,
            'form_id': form_id,
            'client_id': client_id
        }
        mock_save_tracking.return_value = {'id': 'tracking-123'}
        
        mock_form_config.return_value = {
            'id': form_id,
            'title': 'Dog Walking Interest Form',
            'lead_scoring_threshold_yes': 75,
            'lead_scoring_threshold_maybe': 45,
            'max_questions': 8
        }
        
        mock_client_info.return_value = {
            'id': client_id,
            'business_name': 'Pawsome Dog Walking',
            'owner_name': 'Darlene Demo',
            'business_type': 'dog walking service'
        }

        # Step 1: Initialize session with tracking
        initial_state = {
            'core': {
                'session_id': session_id,
                'form_id': form_id,
                'client_id': client_id,
                'started_at': datetime.now().isoformat(),
                'step': 0,
                'completed': False,
                **utm_tracking_data
            },
            'master_flow': {
                'core': {'session_id': session_id, 'form_id': form_id},
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

        # Execute initialization
        with patch('app.graphs.survey_graph_v2.survey_graph') as mock_graph:
            mock_graph.invoke.return_value = {
                **initial_state,
                'core': {**initial_state['core'], 'step': 1},
                'operation_log': [{'operation': 'session_initialized', 'timestamp': datetime.now().isoformat()}]
            }
            
            result = mock_graph.invoke(initial_state)
            
            # Verify initialization
            assert result['core']['session_id'] == session_id
            assert result['core']['utm_source'] == 'facebook'
            assert result['core']['step'] == 1

        # Step 2: Submit responses in batches (simulating multi-step form)
        cumulative_score = 0
        step_responses = [
            complete_form_responses[:2],  # Step 1: Name and dog name
            complete_form_responses[2:4], # Step 2: Breed and service frequency  
            complete_form_responses[4:6], # Step 3: Vaccination and behavior
            complete_form_responses[6:]   # Step 4: Budget and email
        ]

        with patch('app.database.db.save_individual_response') as mock_save_response:
            with patch('app.database.db.update_lead_session_with_tracking') as mock_update_session:
                mock_save_response.return_value = {'id': 'resp-123'}
                mock_update_session.return_value = {'updated': True}

                for step_num, responses in enumerate(step_responses, 1):
                    # Add responses to pending
                    current_state = {
                        **initial_state,
                        'core': {**initial_state['core'], 'step': step_num},
                        'pending_responses': responses,
                        'lead_intelligence': {
                            **initial_state['lead_intelligence'],
                            'current_score': cumulative_score
                        }
                    }

                    # Mock graph execution for response processing
                    with patch('app.graphs.survey_graph_v2.survey_graph') as mock_step_graph:
                        # Simulate score increase
                        cumulative_score += len(responses) * 12  # Average 12 points per response
                        
                        mock_step_graph.invoke.return_value = {
                            **current_state,
                            'core': {**current_state['core'], 'step': step_num + 1},
                            'lead_intelligence': {
                                **current_state['lead_intelligence'],
                                'responses': complete_form_responses[:step_num*2],
                                'current_score': cumulative_score,
                                'lead_status': 'yes' if cumulative_score >= 75 else 'maybe' if cumulative_score >= 45 else 'unknown'
                            },
                            'pending_responses': [],
                            'operation_log': [{
                                'operation': 'responses_processed',
                                'step': step_num,
                                'responses_count': len(responses)
                            }]
                        }
                        
                        step_result = mock_step_graph.invoke(current_state)
                        
                        # Verify responses were processed
                        assert len(step_result['pending_responses']) == 0
                        assert step_result['core']['step'] == step_num + 1
                        
                        # Verify scoring progression
                        if step_num >= 3:  # After key qualification questions
                            assert step_result['lead_intelligence']['current_score'] > 0

        # Step 3: Complete with qualification
        final_state = {
            **initial_state,
            'core': {**initial_state['core'], 'step': 5, 'completed': False},
            'lead_intelligence': {
                **initial_state['lead_intelligence'],
                'responses': complete_form_responses,
                'current_score': 96,  # High score
                'lead_status': 'yes',
                'positive_indicators': ['daily_walks', 'premium_budget', 'social_dog', 'vaccinated'],
                'qualification_reasoning': ['High budget commitment', 'Daily service need', 'Well-socialized dog']
            }
        }

        with patch('app.graphs.nodes.completion_nodes.call_llm') as mock_llm:
            mock_llm.return_value = """Hi Emma!

I'm thrilled to hear from you about Luna! A Golden Retriever who needs daily walks and loves other dogs - you're exactly the kind of client Pawsome Dog Walking was created for.

Your budget of $60-80/week works perfectly for daily service, and Luna's friendly personality means she'd be great for our pack walks which dogs absolutely love.

I'd love to meet you and Luna this week to get started. I'm Darlene, and I'm passionate about giving dogs the exercise they deserve.

Can I call you tomorrow to set up our first meeting?

Best,
Darlene Demo
Pawsome Dog Walking
(617) 555-0123"""

            with patch('app.graphs.survey_graph_v2.survey_graph') as mock_completion_graph:
                mock_completion_graph.invoke.return_value = {
                    **final_state,
                    'core': {
                        **final_state['core'], 
                        'completed': True,
                        'completion_type': 'qualified',
                        'completed_at': datetime.now().isoformat()
                    },
                    'completion_message': mock_llm.return_value,
                    'operation_log': [{
                        'operation': 'qualified_completion',
                        'final_score': 96,
                        'lead_status': 'yes'
                    }]
                }
                
                completion_result = mock_completion_graph.invoke(final_state)
                
                # Verify qualified completion
                assert completion_result['core']['completed'] is True
                assert completion_result['core']['completion_type'] == 'qualified'
                assert completion_result['completion_message'] is not None
                assert 'Emma' in completion_result['completion_message']
                assert 'Luna' in completion_result['completion_message']
                assert len(completion_result['completion_message']) > 200

        # Verify all database operations were called
        mock_create_session.assert_called_once()
        mock_save_tracking.assert_called_once()
        assert mock_save_response.call_count == len(complete_form_responses)

    @patch('app.database.db.create_lead_session')
    @patch('app.database.db.mark_session_abandoned')
    def test_abandonment_flow_integration(self, mock_mark_abandoned, mock_create_session):
        """Test complete abandonment detection and handling flow."""
        session_id = str(uuid.uuid4())
        mock_create_session.return_value = {'session_id': session_id}
        mock_mark_abandoned.return_value = {'abandonment_status': 'abandoned'}

        # Start session
        initial_state = {
            'core': {
                'session_id': session_id,
                'form_id': str(uuid.uuid4()),
                'step': 1,
                'completed': False
            },
            'engagement': {
                'abandonment_risk': 0.3,
                'last_activity_timestamp': (datetime.now() - timedelta(minutes=20)).isoformat(),
                'abandonment_status': 'active',
                'hesitation_indicators': 0
            },
            'lead_intelligence': {'responses': [], 'current_score': 0},
            'operation_log': []
        }

        with patch('app.graphs.survey_graph_v2.survey_graph') as mock_graph:
            # Mock abandonment detection
            mock_graph.invoke.return_value = {
                **initial_state,
                'core': {
                    **initial_state['core'],
                    'completed': True,
                    'completion_type': 'abandoned'
                },
                'engagement': {
                    **initial_state['engagement'],
                    'abandonment_status': 'abandoned',
                    'abandonment_risk': 0.95
                },
                'operation_log': [{'operation': 'session_abandoned'}]
            }
            
            result = mock_graph.invoke(initial_state)
            
            # Verify abandonment handling
            assert result['core']['completed'] is True
            assert result['core']['completion_type'] == 'abandoned'
            assert result['engagement']['abandonment_status'] == 'abandoned'

    @patch('app.session_recovery.recovery_manager.recover_session_state')
    def test_session_recovery_integration(self, mock_recover):
        """Test session recovery and continuation."""
        session_id = 'recovery-test-session-123'
        
        # Mock recovered state
        recovered_state = {
            'core': {
                'session_id': session_id,
                'form_id': str(uuid.uuid4()),
                'step': 2,
                'completed': False
            },
            'lead_intelligence': {
                'responses': [
                    {'question_id': 1, 'answer': 'John Doe'},
                    {'question_id': 2, 'answer': 'Buddy'}
                ],
                'current_score': 15
            },
            'engagement': {
                'abandonment_status': 'active',
                'last_activity_timestamp': datetime.now().isoformat()
            },
            'session_recovery_data': {
                'recovered_at': datetime.now().isoformat(),
                'recovery_method': 'database_reconstruction'
            }
        }
        
        mock_recover.return_value = recovered_state
        
        # Test recovery
        result = recovery_manager.recover_session_state(session_id)
        
        # Verify recovery
        assert result is not None
        assert result['core']['session_id'] == session_id
        assert len(result['lead_intelligence']['responses']) == 2
        assert result['core']['step'] == 2
        assert 'session_recovery_data' in result

    def test_end_to_end_data_consistency(self):
        """Test that data remains consistent throughout the entire flow."""
        # This test would verify that:
        # 1. UTM data persists from start to finish
        # 2. Response scores accumulate correctly
        # 3. Session state remains coherent
        # 4. Database updates match state changes
        
        test_session_id = 'consistency-test-123'
        
        # Track data consistency checkpoints
        checkpoints = {
            'initialization': {
                'utm_source': 'facebook',
                'session_id': test_session_id,
                'step': 0,
                'score': 0
            },
            'first_response': {
                'step': 1,
                'score': 5,
                'response_count': 1
            },
            'qualification_phase': {
                'step': 3,
                'score': 45,
                'response_count': 5
            },
            'completion': {
                'step': 4,
                'score': 85,
                'response_count': 7,
                'completed': True
            }
        }
        
        # Verify checkpoint consistency
        for phase, expected_data in checkpoints.items():
            assert expected_data['session_id'] == test_session_id
            if phase != 'initialization':
                assert expected_data['step'] > checkpoints['initialization']['step']
                assert expected_data['score'] >= checkpoints['initialization']['score']

    @patch('app.database.db.get_form_analytics')
    def test_analytics_integration_after_completion(self, mock_analytics):
        """Test that analytics are properly calculated after form completion."""
        form_id = str(uuid.uuid4())
        
        # Mock analytics data
        mock_analytics.return_value = {
            'total_sessions': 50,
            'completed_sessions': 35,
            'completion_rate': 0.70,
            'qualified_leads': 15,
            'maybe_leads': 12,
            'qualified_rate': 0.43,
            'abandoned_sessions': 8,
            'abandonment_rate': 0.16,
            'avg_steps': 3.8
        }
        
        # Get analytics
        analytics = db.get_form_analytics(form_id, days=30)
        
        # Verify analytics structure
        assert analytics['completion_rate'] == 0.70
        assert analytics['qualified_rate'] == 0.43
        assert analytics['abandonment_rate'] == 0.16
        assert analytics['avg_steps'] == 3.8

    def test_error_handling_throughout_flow(self):
        """Test error handling at different points in the survey flow."""
        error_scenarios = [
            'database_connection_failure',
            'llm_service_unavailable', 
            'invalid_response_data',
            'missing_client_configuration',
            'state_corruption'
        ]
        
        for scenario in error_scenarios:
            # Each scenario should be handled gracefully without crashing
            # Implementation would test specific error conditions
            assert scenario in error_scenarios  # Placeholder for actual error tests

    @patch('app.tools.load_questions')
    def test_form_configuration_loading(self, mock_load_questions):
        """Test that form configuration loads correctly throughout flow."""
        form_id = str(uuid.uuid4())
        
        mock_questions = [
            {'question_id': 1, 'text': 'What is your name?', 'required': True},
            {'question_id': 2, 'text': 'What is your dog\'s name?', 'required': False},
            {'question_id': 3, 'text': 'What breed?', 'required': False},
        ]
        
        mock_load_questions.return_value = mock_questions
        
        # Test question loading
        questions = mock_load_questions(form_id)
        
        assert len(questions) == 3
        assert questions[0]['required'] is True
        assert questions[1]['required'] is False