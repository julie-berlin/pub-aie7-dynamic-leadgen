"""Tracking and Response Processing Nodes for real-world survey flow."""

from __future__ import annotations
from typing import Dict, Any, Optional
import json
import logging
from datetime import datetime

# Import Pydantic models for type safety
from pydantic_models import (
    SurveyGraphState,
    CoreSurveyState,
    ResponseData,
    OperationLogEntry,
    LeadStatus,
    AbandonmentStatus,
    create_initial_state
)
from ...utils.async_operations import async_db

logger = logging.getLogger(__name__)


def initialize_session_with_tracking_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Initialize session with UTM parameters and tracking data.
    
    Args:
        state: Raw state dictionary (will be validated)
        
    Returns:
        Updated state dictionary with validated Pydantic models
    """
    try:
        logger.info(f"🔥 INIT NODE DEBUG: Input state keys = {list(state.keys())}")
        logger.info(f"🔥 INIT NODE DEBUG: pending_responses = {state.get('pending_responses')}")
        
        # Create proper Pydantic state if we have minimal data
        if 'core' not in state and 'metadata' in state:
            # This is likely an initial API call, create proper state
            metadata = state.get('metadata', {})
            
            # Create validated initial state
            survey_state = create_initial_state(
                session_id=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                form_id=metadata.get('form_id', ''),
                client_id=metadata.get('client_id'),
                utm_data={
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
            )
            
            # Convert to dict for LangGraph compatibility
            state = survey_state.model_dump()
        
        # Validate existing state with Pydantic
        try:
            validated_state = SurveyGraphState(**state)
        except Exception as e:
            logger.warning(f"State validation failed, using raw state: {e}")
            validated_state = None
        
        # Extract core data (use validated if available)
        core_data = validated_state.core if validated_state else state.get('core', {})
        session_id = core_data.session_id if hasattr(core_data, 'session_id') else core_data.get('session_id')
        
        # Extract tracking data from metadata or core
        metadata = state.get('metadata', {})
        
        # Try to get form_id from multiple possible locations
        form_id = (
            metadata.get('form_id') or  # Original metadata
            core_data.get('form_id') if isinstance(core_data, dict) else None or  # Core data as dict
            (core_data.form_id if hasattr(core_data, 'form_id') else None)  # Core data as object
        )
        
        # Log for debugging
        logger.debug(f"Extracting form_id - metadata: {metadata.get('form_id')}, core_data: {core_data}, final form_id: {form_id}")
        
        tracking_data = {
            'utm_source': metadata.get('utm_source'),
            'utm_medium': metadata.get('utm_medium'),
            'utm_campaign': metadata.get('utm_campaign'),
            'utm_content': metadata.get('utm_content'),
            'utm_term': metadata.get('utm_term'),
            'referrer': metadata.get('referrer'),
            'user_agent': metadata.get('user_agent'),
            'ip_address': metadata.get('ip_address'),
            'landing_page': metadata.get('landing_page')
            # Note: session_started removed - not in tracking_data schema, use created_at instead
        }
        
        # Create session ID
        import uuid
        session_id = str(uuid.uuid4())
        
        # Validate form exists in database
        if not form_id:
            raise ValueError("form_id is required but not found in state")
        from ...database import db
        form_config = db.get_form(form_id)
        if not form_config:
            raise ValueError(f"Form {form_id} not found in database")
        
        # Initialize core state with all tracking fields
        core_state = {
            'session_id': session_id,
            'form_id': form_id,
            'client_id': form_config.get('client_id') or metadata.get('client_id'),
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
        
        # Save session to database immediately
        session_data = {
            'session_id': session_id,
            'form_id': form_id,
            'client_id': core_state.get('client_id'),
            'started_at': core_state['started_at'],
            'last_updated': core_state['last_updated'],
            'step': core_state['step'],
            'completed': core_state['completed'],
            'lead_status': 'unknown',
            'abandonment_status': 'active',
            'abandonment_risk': 0.3
        }
        
        # Create lead session in database
        from ...database import db
        try:
            db.create_lead_session(session_data)
            logger.info(f"Created lead session in database: {session_id}")
        except Exception as e:
            logger.error(f"Failed to create lead session: {e}")
        
        # Save tracking data immediately to database (fire-and-forget)
        async_db.save_tracking_data(session_id, tracking_data)
        
        logger.info(f"Initialized session {session_id} with tracking")
        
        # Check if this is a fresh initialization or continuing with existing state
        existing_question_strategy = state.get('question_strategy', {})
        existing_lead_intelligence = state.get('lead_intelligence', {})
        
        # Only preserve existing state if it has meaningful data
        preserve_questions = bool(existing_question_strategy.get('asked_questions'))
        preserve_responses = bool(existing_lead_intelligence.get('responses'))
        
        logger.info(f"🔥 INIT: preserve_questions={preserve_questions}, preserve_responses={preserve_responses}")
        
        # Initialize all state sections
        return {
            'core': core_state,
            'master_flow': {
                'core': core_state,
                'flow_phase': 'initialization',
                'completion_probability': 0.5,
                'flow_strategy': 'STANDARD'
            },
            'question_strategy': {
                'all_questions': [],  # Will be loaded
                'asked_questions': existing_question_strategy.get('asked_questions', []) if preserve_questions else [],
                'current_questions': existing_question_strategy.get('current_questions', []) if preserve_questions else [],
                'phrased_questions': existing_question_strategy.get('phrased_questions', []) if preserve_questions else [],
                'question_strategy': existing_question_strategy.get('question_strategy', {}),
                'selection_history': existing_question_strategy.get('selection_history', []) if preserve_questions else []
            },
            'lead_intelligence': {
                'responses': existing_lead_intelligence.get('responses', []) if preserve_responses else [],
                'current_score': existing_lead_intelligence.get('current_score', 0),
                'score_history': existing_lead_intelligence.get('score_history', []),
                'lead_status': existing_lead_intelligence.get('lead_status', 'unknown'),
                'qualification_reasoning': existing_lead_intelligence.get('qualification_reasoning', []),
                'risk_factors': existing_lead_intelligence.get('risk_factors', []),
                'positive_indicators': existing_lead_intelligence.get('positive_indicators', [])
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
            'pending_responses': state.get('pending_responses', []),
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
        
        # Get only responses that have just been submitted (have submitted_at timestamp)
        # Filter to just the newest responses from this step
        current_timestamp = datetime.now().isoformat()[:19]  # YYYY-MM-DDTHH:MM:SS
        new_responses = [r for r in responses if r.get('submitted_at', '').startswith(current_timestamp[:16])]  # Same minute
        
        if not new_responses:
            # Fallback: save last few responses if timestamp matching fails
            new_responses = responses[-3:] if len(responses) >= 3 else responses
        
        # Save responses to database (fire-and-forget)
        response_batch = []
        for response in new_responses:
            response_data = {
                'session_id': session_id,
                'question_id': response.get('question_id'),
                'question_text': response.get('question_text'),
                'answer': response.get('answer'),
                'submitted_at': response.get('submitted_at'),
                'step': response.get('step')
            }
            response_batch.append(response_data)
        
        # Use batched fire-and-forget operation
        async_db.save_response_batch(session_id, response_batch)
        
        logger.info(f"Saved {len(new_responses)} new responses for session {session_id}")
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
        # Convert Pydantic object to dict if needed
        if hasattr(state, 'model_dump'):
            state_dict = state.model_dump()
        else:
            state_dict = state
        
        # Extract data for frontend
        question_strategy = state_dict.get('question_strategy', {})
        engagement = state_dict.get('engagement', {})
        core = state_dict.get('core', {})
        
        # Convert QuestionDataInternal to QuestionData format for API
        phrased_questions = question_strategy.get('phrased_questions', [])
        frontend_questions = []
        
        for q in phrased_questions:
            if isinstance(q, dict):
                frontend_question = {
                    'id': q.get('question_id', 0),
                    'question': q.get('question_text', ''),
                    'phrased_question': q.get('phrased_question', q.get('question_text', '')),
                    'data_type': q.get('data_type', 'text'),
                    'is_required': q.get('is_required', False),
                    'options': q.get('options'),
                    'scoring_rubric': q.get('scoring_rubric')
                }
                frontend_questions.append(frontend_question)
        
        # Prepare frontend response
        frontend_data = {
            'session_id': core.get('session_id'),
            'step': core.get('step', 0) + 1,
            'questions': frontend_questions,
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


def qualified_message_generation_node(state: SurveyGraphState) -> Dict[str, Any]:
    """
    Generate personalized completion message for qualified/maybe leads.
    Uses LLM to create engaging, business-specific completion messages.
    """
    try:
        # Extract state components
        core = state.get('core', {})
        lead_intelligence = state.get('lead_intelligence', {})
        
        form_id = core.get('form_id')
        session_id = core.get('session_id')
        lead_status = lead_intelligence.get('lead_status', 'unknown')
        responses = lead_intelligence.get('responses', [])
        
        # Only generate for qualified/maybe leads
        if lead_status not in ['yes', 'maybe']:
            logger.warning(f"Qualified message generation called for {lead_status} lead")
            return {}
        
        # Load client information for personalization
        from ...tools import load_client_info
        client_json = load_client_info.invoke({'form_id': form_id})
        client_info = json.loads(client_json) if client_json else {}
        
        # Extract business context
        business_name = "Our Business"
        business_type = "service provider" 
        owner_name = "The Team"
        
        if client_info.get('client'):
            client_data = client_info['client']
            business_name = client_data.get('business_name', client_data.get('name', business_name))
            business_type = client_data.get('business_type', client_data.get('industry', business_type))
            owner_name = client_data.get('owner_name', client_data.get('contact_name', owner_name))
        
        # Extract personalization data from responses
        user_name = ""
        key_interests = []
        specific_needs = []
        
        for response in responses:
            answer = str(response.get('answer', '')).lower()
            question = str(response.get('question_text', '')).lower()
            
            # Extract name
            if 'name' in question and not user_name:
                user_name = str(response.get('answer', '')).strip()
            
            # Extract interests and needs
            if any(word in question for word in ['service', 'need', 'looking', 'want']):
                if len(answer) > 3:
                    specific_needs.append(answer)
            
            if any(word in answer for word in ['yes', 'interested', 'definitely', 'absolutely']):
                key_interests.append(question.split('?')[0])
        
        # Generate personalized message using LLM
        completion_message = _generate_qualified_message_with_llm(
            business_name=business_name,
            business_type=business_type, 
            owner_name=owner_name,
            lead_status=lead_status,
            user_name=user_name,
            key_interests=key_interests[:3],  # Top 3
            specific_needs=specific_needs[:2]  # Top 2
        )
        
        logger.info(f"Generated qualified completion message for {lead_status} lead {session_id}")
        
        return {
            'completion_message': completion_message,
            'core': {
                **core,
                'completed': True,
                'completed_at': datetime.now().isoformat(),
                'completion_type': 'qualified'
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to generate qualified message: {e}")
        # Fallback message
        fallback = "Thank you for your interest! We'll be in touch soon with next steps."
        return {
            'completion_message': fallback,
            'core': {
                **state.get('core', {}),
                'completed': True,
                'completed_at': datetime.now().isoformat(),
                'completion_type': 'qualified_fallback'
            }
        }


def unqualified_completion_node(state: SurveyGraphState) -> Dict[str, Any]:
    """
    Simple completion for unqualified leads without LLM personalization.
    Efficient and direct completion for leads that don't meet criteria.
    """
    try:
        core = state.get('core', {})
        lead_intelligence = state.get('lead_intelligence', {})
        
        session_id = core.get('session_id')
        lead_status = lead_intelligence.get('lead_status', 'unknown')
        
        # Simple completion message - no LLM needed
        completion_message = "Thank you for your time and interest."
        
        logger.info(f"Completed unqualified lead {session_id} with status {lead_status}")
        
        return {
            'completion_message': completion_message,
            'core': {
                **core,
                'completed': True,
                'completed_at': datetime.now().isoformat(),
                'completion_type': 'unqualified'
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to complete unqualified lead: {e}")
        return {
            'completion_message': "Thank you for your time.",
            'core': {
                **state.get('core', {}),
                'completed': True,
                'completed_at': datetime.now().isoformat(),
                'completion_type': 'unqualified_error'
            }
        }


def _generate_qualified_message_with_llm(
    business_name: str,
    business_type: str,
    owner_name: str, 
    lead_status: str,
    user_name: str = "",
    key_interests: list = None,
    specific_needs: list = None
) -> str:
    """Generate personalized completion message using LLM for qualified leads."""
    try:
        from ...models import get_chat_model
        
        key_interests = key_interests or []
        specific_needs = specific_needs or []
        
        # Create personalization context
        personalization = ""
        if user_name:
            personalization += f"The user's name is {user_name}. "
        if key_interests:
            personalization += f"They showed interest in: {', '.join(key_interests)}. "
        if specific_needs:
            personalization += f"Their specific needs include: {', '.join(specific_needs)}. "
        
        lead_quality = "high-quality" if lead_status == "yes" else "potential"
        
        prompt = f"""Write a personalized completion message for a {lead_quality} lead for {business_name}, a {business_type}.

Business owner: {owner_name}
Lead quality: {lead_status}
{personalization}

Requirements:
- Thank them for their time and interest
- Reference specific interests/needs they mentioned if available
- Create excitement about working together
- Mention next steps (we'll contact them soon)
- Keep it warm, professional, and personal
- 2-3 sentences maximum
- Use their name if provided

Write the message as if {owner_name} is speaking directly to them."""

        # Get chat model and generate response
        model = get_chat_model(temperature=0.7)
        messages = [
            {"role": "system", "content": "You write personalized, warm completion messages for service businesses that make leads excited to work with the company."},
            {"role": "user", "content": prompt}
        ]
        
        response = model.invoke(messages)
        
        if hasattr(response, 'content'):
            return response.content.strip()
        else:
            return str(response).strip()
            
    except Exception as e:
        logger.error(f"LLM message generation failed: {e}")
        # Fallback message
        name_part = f"{user_name}, " if user_name else ""
        return f"Thank you {name_part}for your interest in {business_name}! We're excited about the possibility of working together and will be in touch soon."