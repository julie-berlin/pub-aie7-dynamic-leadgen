"""Tracking and Response Processing Nodes for real-world survey flow."""

from __future__ import annotations
from typing import Dict, Any, Optional
import json
import logging
from datetime import datetime

from ...state import SurveyGraphState, CoreSurveyState
from ..toolbelts.persistence_toolbelt import persistence_toolbelt

logger = logging.getLogger(__name__)


def initialize_session_with_tracking_node(state: SurveyGraphState) -> Dict[str, Any]:
    """
    Initialize session with UTM parameters and tracking data.
    
    Expected input in state:
    - utm_source, utm_medium, utm_campaign, utm_content, utm_term
    - referrer (from HTTP headers)
    - user_agent
    - ip_address (for geographic data)
    - form_id/client_id
    """
    try:
        # Extract tracking data from initial request
        metadata = state.get('metadata', {})
        tracking_data = {
            'utm_source': metadata.get('utm_source'),
            'utm_medium': metadata.get('utm_medium'),
            'utm_campaign': metadata.get('utm_campaign'),
            'utm_content': metadata.get('utm_content'),
            'utm_term': metadata.get('utm_term'),
            'referrer': metadata.get('referrer'),
            'user_agent': metadata.get('user_agent'),
            'ip_address': metadata.get('ip_address'),
            'landing_page': metadata.get('landing_page'),
            'session_started': datetime.now().isoformat()
        }
        
        # Create session ID
        import uuid
        session_id = str(uuid.uuid4())
        
        # Initialize core state with all tracking fields
        core_state = {
            'session_id': session_id,
            'form_id': metadata.get('form_id', 'default'),
            'client_id': metadata.get('client_id'),
            'started_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'step': 0,
            'completed': False,
            # Add all UTM and tracking fields
            'utm_source': metadata.get('utm_source'),
            'utm_medium': metadata.get('utm_medium'),
            'utm_campaign': metadata.get('utm_campaign'),
            'utm_content': metadata.get('utm_content'),
            'utm_term': metadata.get('utm_term'),
            'referrer': metadata.get('referrer'),
            'user_agent': metadata.get('user_agent'),
            'ip_address': metadata.get('ip_address'),
            'landing_page': metadata.get('landing_page')
        }
        
        # Save tracking data immediately to database
        tracking_json = json.dumps(tracking_data)
        persistence_toolbelt.save_tracking_data.invoke({
            "session_id": session_id,
            "tracking_data": tracking_json
        })
        
        logger.info(f"Initialized session {session_id} with tracking")
        
        # Initialize all state sections
        return {
            'core': core_state,
            'master_flow': {
                'core': core_state,
                'flow_phase': 'initializing',
                'completion_probability': 0.5,
                'flow_strategy': 'EXPLORATORY'
            },
            'question_strategy': {
                'all_questions': [],  # Will be loaded
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
            # Communication and API fields
            'supervisor_messages': [],
            'shared_context': {},
            'pending_responses': [],
            'frontend_response': None,
            # Session management
            'session_recovery_data': None,
            'completion_message': None,
            # Logging
            'error_log': [],
            'operation_log': [],
            # Metadata
            'metadata': {**metadata, **tracking_data}
        }
        
    except Exception as e:
        logger.error(f"Failed to initialize session with tracking: {e}")
        raise


def process_user_responses_node(state: SurveyGraphState) -> Dict[str, Any]:
    """
    Process user responses when they submit answers.
    
    Expected input:
    - New responses in a 'pending_responses' field
    """
    try:
        # Get pending responses from API request
        pending_responses = state.get('pending_responses', [])
        
        if not pending_responses:
            logger.warning("No pending responses to process")
            return {}
        
        # Get current state
        lead_intelligence = state.get('lead_intelligence', {})
        existing_responses = lead_intelligence.get('responses', [])
        
        # Add timestamps to responses
        for response in pending_responses:
            response['submitted_at'] = datetime.now().isoformat()
            response['step'] = state.get('core', {}).get('step', 0)
        
        # Merge with existing responses
        all_responses = existing_responses + pending_responses
        
        # Update activity timestamp
        engagement_updates = {
            'last_activity_timestamp': datetime.now().isoformat(),
            'abandonment_risk': 0.2  # Reset risk after activity
        }
        
        logger.info(f"Processed {len(pending_responses)} new responses")
        
        return {
            'lead_intelligence': {
                **lead_intelligence,
                'responses': all_responses
            },
            'engagement': {
                **state.get('engagement', {}),
                **engagement_updates
            },
            'pending_responses': []  # Clear pending
        }
        
    except Exception as e:
        logger.error(f"Failed to process responses: {e}")
        return {}


def save_responses_immediately_node(state: SurveyGraphState) -> Dict[str, Any]:
    """
    Save responses to database immediately after processing.
    Fire-and-forget operation.
    """
    try:
        core = state.get('core', {})
        session_id = core.get('session_id')
        
        lead_intelligence = state.get('lead_intelligence', {})
        responses = lead_intelligence.get('responses', [])
        
        if not responses:
            return {}
        
        # Get only the most recent responses to save
        # (In production, track which are already saved)
        recent_responses = responses[-5:]  # Last 5 responses
        
        # Save each response
        for response in recent_responses:
            response_data = {
                'session_id': session_id,
                'question_id': response.get('question_id'),
                'question_text': response.get('question_text'),
                'answer': response.get('answer'),
                'submitted_at': response.get('submitted_at'),
                'step': response.get('step')
            }
            
            response_json = json.dumps(response_data)
            persistence_toolbelt.save_response.invoke({
                "session_id": session_id,
                "response_data": response_json
            })
        
        logger.info(f"Saved {len(recent_responses)} responses for session {session_id}")
        return {}
        
    except Exception as e:
        logger.error(f"Failed to save responses: {e}")
        return {}  # Don't fail the flow


def check_abandonment_node(state: SurveyGraphState) -> Dict[str, Any]:
    """
    Check if user has abandoned the survey based on inactivity.
    """
    try:
        engagement = state.get('engagement', {})
        last_activity = engagement.get('last_activity_timestamp')
        
        if not last_activity:
            return {}
        
        # Calculate time since last activity
        from datetime import datetime, timedelta
        last_time = datetime.fromisoformat(last_activity)
        time_since = datetime.now() - last_time
        
        # Abandonment thresholds
        if time_since > timedelta(minutes=15):
            abandonment_risk = 0.95
            status = 'abandoned'
        elif time_since > timedelta(minutes=10):
            abandonment_risk = 0.8
            status = 'high_risk'
        elif time_since > timedelta(minutes=5):
            abandonment_risk = 0.6
            status = 'medium_risk'
        else:
            abandonment_risk = 0.3
            status = 'active'
        
        logger.info(f"Abandonment check: {status} (risk: {abandonment_risk})")
        
        return {
            'engagement': {
                **engagement,
                'abandonment_risk': abandonment_risk,
                'abandonment_status': status
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to check abandonment: {e}")
        return {}


def prepare_step_for_frontend_node(state: SurveyGraphState) -> Dict[str, Any]:
    """
    Prepare the step data for the frontend API response.
    
    Returns a clean structure for /session/step endpoint.
    """
    try:
        # Extract data for frontend
        question_strategy = state.get('question_strategy', {})
        engagement = state.get('engagement', {})
        core = state.get('core', {})
        
        # Prepare frontend response
        frontend_data = {
            'session_id': core.get('session_id'),
            'step': core.get('step', 0) + 1,
            'questions': question_strategy.get('phrased_questions', []),
            'question_metadata': question_strategy.get('current_questions', []),
            'headline': engagement.get('step_headline', 'Let\'s continue!'),
            'motivation': engagement.get('step_motivation', 'Thank you for your time.'),
            'progress': {
                'current_step': core.get('step', 0) + 1,
                'estimated_remaining': 3  # Could be calculated
            }
        }
        
        # Store for API response
        return {
            'frontend_response': frontend_data
        }
        
    except Exception as e:
        logger.error(f"Failed to prepare frontend data: {e}")
        return {}