"""
Flow Engine for API Integration

Integrates the LangGraph form flow with the FastAPI backend.
"""

import uuid
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.append(os.path.dirname(__file__))

# Import our existing flow components
from database import db
from llm_utils import rephrase_questions_simple
from agents.question_selection_agent import invoke_question_selection
from agents.engagement_agent import invoke_engagement_agent
from agents.lead_scoring_agent import invoke_lead_scoring_agent

# TODO: Refactor session state representation
# - Consider using a proper Session class with validation
# - Separate core state from UI state
# - Add state versioning for backward compatibility
# - Implement state serialization/deserialization

class FormFlowEngine:
    """
    Engine that orchestrates the form flow for API consumption
    
    Converts the notebook-based LangGraph flow into API-callable methods.
    """
    
    def __init__(self):
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        
    def load_questions(self, form_id: str = "dogwalk_demo_form") -> List[Dict[str, Any]]:
        """Load questions from JSON file based on form_id"""
        # For now, use the dogwalk demo data
        questions_file = Path("data/input/dogwalk_34397/questions.json")
        with open(questions_file, 'r') as f:
            data = json.load(f)
        return data['questions']
    
    def load_client_info(self, form_id: str = "dogwalk_demo_form") -> Dict[str, Any]:
        """Load client information based on form_id"""
        # For now, use the dogwalk demo data
        client_file = Path("data/input/dogwalk_34397/client.json")
        with open(client_file, 'r') as f:
            data = json.load(f)
        return data['client']
    
    def _create_initial_state(self, session_id: str, form_id: str, client_id: Optional[str], metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Create initial session state with alphabetically ordered keys"""
        return {
            'all_questions': self.load_questions(form_id),
            'asked_questions': [],
            'client_id': client_id,
            'completed': False,
            'current_step_questions': [],
            'failed_required': False,
            'form_id': form_id,
            'last_updated': datetime.now().isoformat(),
            'lead_status': "unknown",
            'metadata': metadata or {},
            'min_questions_met': False,
            'phrased_questions': [],
            'responses': [],
            'score': 0,
            'session_id': session_id,
            'started_at': datetime.now().isoformat(),
            'step': 0,
            'step_headline': "",
            'step_motivation': ""
        }
    
    async def start_session(self, form_id: str, client_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Start a new form session
        
        Args:
            form_id: Form configuration identifier
            client_id: Optional client identifier
            metadata: Additional session metadata
            
        Returns:
            Dict with session_id, first step questions, and content
        """
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Initialize session state with alphabetically ordered keys
        state = self._create_initial_state(session_id, form_id, client_id, metadata)
        
        # Store session in memory and database
        self.active_sessions[session_id] = state
        
        # Get first step questions using our agent
        try:
            selected_question_ids = invoke_question_selection(state)
            selected_questions = [q for q in state['all_questions'] 
                                if q['id'] in selected_question_ids]
        except Exception as e:
            print(f"Question selection failed: {e}, using fallback")
            # Fallback to first 2 questions
            selected_questions = state['all_questions'][:2]
        
        state['current_step_questions'] = selected_questions
        
        # Phrase questions using LLM
        try:
            client_info = self.load_client_info(form_id)
            phrased_questions = rephrase_questions_simple(selected_questions, client_info)
            state['phrased_questions'] = phrased_questions
        except Exception as e:
            print(f"Question phrasing failed: {e}, using original questions")
            state['phrased_questions'] = [q['question'] for q in selected_questions]
        
        # Generate engagement content
        try:
            client_info = self.load_client_info(form_id)
            engagement_content = invoke_engagement_agent(state, client_info)
            state['step_headline'] = engagement_content['headline']
            state['step_motivation'] = engagement_content['motivation']
        except Exception as e:
            print(f"Engagement generation failed: {e}, using fallback")
            state['step_headline'] = "Let's get started! 🚀"
            state['step_motivation'] = "Help us understand your needs better."
        
        # Save initial state to database
        try:
            session_data = {
                'session_id': session_id,
                'form_id': form_id,
                'final_score': 0,
                'lead_status': 'unknown',
                'completed': False,
                'step_count': 0,
                'started_at': state['started_at'],
                'updated_at': state['last_updated']
            }
            db.create_lead_session(session_data)
        except Exception as e:
            print(f"Database save failed: {e}")
        
        # Prepare questions for API response
        questions_with_phrasing = []
        for i, (question, phrased) in enumerate(zip(selected_questions, state['phrased_questions'])):
            questions_with_phrasing.append({
                **question,
                'phrased_question': phrased
            })
        
        return {
            'session_id': session_id,
            'step': 1,
            'headline': state['step_headline'],
            'motivation': state['step_motivation'],
            'questions': questions_with_phrasing
        }
    
    async def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get current session status"""
        if session_id not in self.active_sessions:
            # Try to load from database
            try:
                session_data = db.get_lead_session(session_id)
                if not session_data:
                    return None
                
                responses = db.get_session_responses(session_id)
                
                return {
                    'completed': session_data.get('completed', False),
                    'form_id': session_data.get('form_id', ''),
                    'last_updated': session_data.get('updated_at', ''),
                    'lead_status': session_data.get('lead_status', 'unknown'),
                    'responses_count': len(responses),
                    'score': session_data.get('final_score', 0),
                    'session_id': session_id,
                    'started_at': session_data.get('started_at', ''),
                    'step': session_data.get('step_count', 0)
                }
            except Exception as e:
                print(f"Failed to load session from database: {e}")
                return None
        
        state = self.active_sessions[session_id]
        return {
            'completed': state['completed'],
            'form_id': state['form_id'],
            'last_updated': state['last_updated'],
            'lead_status': state['lead_status'],
            'responses_count': len(state['responses']),
            'score': state['score'],
            'session_id': session_id,
            'started_at': state['started_at'],
            'step': state['step']
        }
    
    def _collect_user_responses(self, state: Dict[str, Any], responses: List[Dict[str, Any]]) -> None:
        """Collect and store user responses in session state"""
        for response in responses:
            question_data = next((q for q in state['current_step_questions'] 
                                if q['id'] == response['question_id']), None)
            
            if question_data:
                response_record = {
                    'answer': response['answer'],
                    'data_type': question_data.get('data_type', ''),
                    'is_required': question_data.get('is_required', False),
                    'original_question': question_data['question'],
                    'phrased_question': response.get('phrased_question', question_data['question']),
                    'question_id': response['question_id'],
                    'scoring_rubric': question_data.get('scoring_rubric', ''),
                    'step': state['step'] + 1,
                    'timestamp': datetime.now().isoformat()
                }
                state['responses'].append(response_record)
                state['asked_questions'].append(response['question_id'])
        
        state['last_updated'] = datetime.now().isoformat()
        state['step'] += 1

    def _persist_responses_to_database(self, session_id: str, new_responses: List[Dict[str, Any]]) -> None:
        """Save new responses to database"""
        try:
            for response in new_responses:
                response_data = {
                    'answer': response['answer'],
                    'data_type': response['data_type'],
                    'is_required': response['is_required'],
                    'original_question': response['original_question'],
                    'phrased_question': response['phrased_question'],
                    'question_id': response['question_id'],
                    'scoring_rubric': response['scoring_rubric'],
                    'session_id': session_id,
                    'step': response['step'],
                    'timestamp': response['timestamp']
                }
                db.create_response(response_data)
        except Exception as e:
            print(f"Database persistence failed: {e}")

    def _calculate_lead_score(self, state: Dict[str, Any]) -> None:
        """Calculate lead score and update qualification status"""
        try:
            scoring_result = invoke_lead_scoring_agent(state, state['all_questions'])
            state['min_questions_met'] = len(state['responses']) >= 4
            state['score'] = scoring_result['score']
            
            # Determine lead status
            if any("CRITICAL" in flag for flag in scoring_result.get('red_flags', [])):
                state['failed_required'] = True
                state['lead_status'] = "no"
            elif not state['min_questions_met']:
                state['lead_status'] = "unknown"
            elif state['score'] >= 80:
                state['lead_status'] = "yes"
            elif state['score'] <= 25:
                state['lead_status'] = "no"
            else:
                state['lead_status'] = "maybe"
                
        except Exception as e:
            print(f"Lead scoring calculation failed: {e}, using fallback")
            state['min_questions_met'] = len(state['responses']) >= 4
            state['score'] = len(state['responses']) * 15
            if state['score'] >= 80:
                state['lead_status'] = "yes"
            elif state['score'] <= 25:
                state['lead_status'] = "no"
            else:
                state['lead_status'] = "maybe"

    def _check_completion_criteria(self, state: Dict[str, Any]) -> bool:
        """Check if session meets completion criteria"""
        available_questions = [q for q in state['all_questions']
                             if q['id'] not in state['asked_questions']]
        
        return (
            not available_questions or
            state['failed_required'] or
            len(state['responses']) >= 6 or
            (state['lead_status'] in ['yes', 'no'] and len(state['responses']) >= 4)
        )

    def _select_next_questions(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Select questions for next step using AI agent"""
        try:
            selected_question_ids = invoke_question_selection(state)
            return [q for q in state['all_questions'] 
                   if q['id'] in selected_question_ids]
        except Exception as e:
            print(f"Question selection failed: {e}, using fallback")
            available_questions = [q for q in state['all_questions']
                                 if q['id'] not in state['asked_questions']]
            return available_questions[:2]

    def _adapt_question_phrasing(self, state: Dict[str, Any], selected_questions: List[Dict[str, Any]]) -> None:
        """Adapt question phrasing for business context using LLM"""
        try:
            client_info = self.load_client_info(state['form_id'])
            phrased_questions = rephrase_questions_simple(selected_questions, client_info)
            state['phrased_questions'] = phrased_questions
        except Exception as e:
            print(f"Question phrasing adaptation failed: {e}")
            state['phrased_questions'] = [q['question'] for q in selected_questions]

    def _create_engagement_content(self, state: Dict[str, Any]) -> None:
        """Create engaging headlines and motivational content"""
        try:
            client_info = self.load_client_info(state['form_id'])
            engagement_content = invoke_engagement_agent(state, client_info)
            state['step_headline'] = engagement_content['headline']
            state['step_motivation'] = engagement_content['motivation']
        except Exception as e:
            print(f"Engagement content creation failed: {e}")
            state['step_headline'] = f"Step {state['step']} - You're doing great! ✨"
            state['step_motivation'] = "Thanks for sharing these details with us."

    def _format_questions_for_api(self, selected_questions: List[Dict[str, Any]], phrased_questions: List[str]) -> List[Dict[str, Any]]:
        """Format questions with phrasing for API response"""
        questions_with_phrasing = []
        for question, phrased in zip(selected_questions, phrased_questions):
            questions_with_phrasing.append({
                **question,
                'phrased_question': phrased
            })
        return questions_with_phrasing

    async def advance_session_step(self, session_id: str, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Advance session to next step with user responses
        
        Args:
            session_id: Session identifier
            responses: List of user responses for current step
            
        Returns:
            Dict with next step questions and content, or completion flag
        """
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        state = self.active_sessions[session_id]
        
        # Collect and store user responses
        self._collect_user_responses(state, responses)
        
        # Persist responses to database
        new_responses = state['responses'][-len(responses):] if responses else []
        self._persist_responses_to_database(session_id, new_responses)
        
        # Calculate lead score and status
        self._calculate_lead_score(state)
        
        # Check if session should be completed
        if self._check_completion_criteria(state):
            state['completed'] = True
            return {'completed': True, 'session_id': session_id}
        
        # Select questions for next step
        selected_questions = self._select_next_questions(state)
        state['current_step_questions'] = selected_questions
        
        # Adapt question phrasing
        self._adapt_question_phrasing(state, selected_questions)
        
        # Create engagement content
        self._create_engagement_content(state)
        
        # Format response
        questions_with_phrasing = self._format_questions_for_api(
            selected_questions, state['phrased_questions']
        )
        
        return {
            'headline': state['step_headline'],
            'motivation': state['step_motivation'],
            'questions': questions_with_phrasing,
            'session_id': session_id,
            'step': state['step'],
            'total_responses': len(state['responses'])
        }
    
    def _extract_personalization_data(self, responses: List[Dict[str, Any]]) -> Dict[str, str]:
        """Extract user name and dog info for personalization"""
        # TODO: Refactor hardcoded question IDs for real app
        # - Use question metadata/tags instead of hardcoded IDs
        # - Make personalization configurable per form
        # - Support different question types (name, contact, subject, etc.)
        dog_info = "your pup"
        user_name = ""
        
        for response in responses:
            if response['question_id'] == 7:  # HARDCODED: Name question
                user_name = response['answer'].split()[0]
            elif response['question_id'] == 2:  # HARDCODED: Breed question
                dog_info = f"your {response['answer']}"
        
        greeting = f"Hi {user_name}!" if user_name else "Hello!"
        return {'dog_info': dog_info, 'greeting': greeting, 'user_name': user_name}
    
    def _generate_completion_message(self, state: Dict[str, Any], personalization: Dict[str, str]) -> Dict[str, Any]:
        """Generate personalized completion message based on lead status"""
        client_info = self.load_client_info(state['form_id'])
        business_name = client_info['information']['name']
        owner_name = client_info['information']['owner']
        
        greeting = personalization['greeting']
        dog_info = personalization['dog_info']
        
        if state['lead_status'] == "yes":
            completion_message = f"""🎉 {greeting} Wonderful news!

Based on your responses, {business_name} would be thrilled to provide walking services for {dog_info}!

{owner_name} will personally reach out within 24 hours to discuss scheduling and answer any questions you might have.

We're excited to meet you both and provide the best care for your furry family member! 🐾"""
            next_steps = [
                "Expect a call within 24 hours",
                "Prepare any additional questions about our services",
                "Get ready to meet your dedicated dog walker!"
            ]
            
        elif state['lead_status'] == "maybe":
            completion_message = f"""🤔 {greeting} Thank you for your interest!

We'd love to learn a bit more about {dog_info} to ensure we're the perfect fit.

{owner_name} will review your responses and get back to you within 48 hours with next steps.

We appreciate you considering {business_name} for your dog walking needs! 🐕"""
            next_steps = [
                "Expect follow-up within 48 hours",
                "Consider additional services you might need",
                "Review our service areas and scheduling"
            ]
            
        else:  # "no" status
            completion_message = f"""🙏 {greeting} Thank you for your time!

While we may not be the perfect fit for {dog_info} at this time, we appreciate you considering {business_name}.

We'd be happy to provide recommendations for other services that might better meet your needs.

Best wishes to you and your furry friend! 🐾"""
            next_steps = [
                "Consider other local dog walking services",
                "Check our referral network for alternatives",
                "Feel free to contact us if your needs change"
            ]
        
        return {
            'completion_message': completion_message,
            'next_steps': next_steps
        }
    
    def _finalize_session_in_database(self, session_id: str, state: Dict[str, Any]) -> None:
        """Update database with final session completion data"""
        try:
            db.update_lead_session(session_id, {
                'completed': True,
                'completed_at': state['last_updated'],
                'final_score': state['score'],
                'lead_status': state['lead_status']
            })
        except Exception as e:
            print(f"Database finalization failed: {e}")
    
    async def finalize_session(self, session_id: str, final_responses: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Finalize session and generate completion results
        
        Args:
            session_id: Session identifier
            final_responses: Optional final responses to process
            
        Returns:
            Dict with completion message and final status
        """
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        state = self.active_sessions[session_id]
        
        # Collect any final responses
        if final_responses:
            self._collect_user_responses(state, final_responses)
            new_responses = state['responses'][-len(final_responses):] if final_responses else []
            self._persist_responses_to_database(session_id, new_responses)
            self._calculate_lead_score(state)
        
        # Mark session as completed
        state['completed'] = True
        state['last_updated'] = datetime.now().isoformat()
        
        # Extract personalization data
        personalization = self._extract_personalization_data(state['responses'])
        
        # Generate completion message
        completion_data = self._generate_completion_message(state, personalization)
        
        # Update database
        self._finalize_session_in_database(session_id, state)
        
        # Clean up active session
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        
        return {
            'completed_at': state['last_updated'],
            'completion_message': completion_data['completion_message'],
            'final_score': state['score'],
            'lead_status': state['lead_status'],
            'next_steps': completion_data['next_steps'],
            'session_id': session_id
        }
    
    def _record_abandonment_in_database(self, session_id: str, abandoned_at: str) -> None:
        """Record session abandonment in database"""
        try:
            db.update_lead_session(session_id, {
                'abandoned_at': abandoned_at,
                'completed': False,
                'updated_at': abandoned_at
            })
        except Exception as e:
            print(f"Database abandonment recording failed: {e}")
    
    async def mark_session_abandoned(self, session_id: str) -> Dict[str, Any]:
        """
        Mark session as abandoned for analytics
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dict with abandonment details
        """
        if session_id in self.active_sessions:
            state = self.active_sessions[session_id]
            abandoned_at = datetime.now().isoformat()
            
            # Record abandonment in database
            self._record_abandonment_in_database(session_id, abandoned_at)
            
            result = {
                'abandoned_at': abandoned_at,
                'responses_collected': len(state['responses']),
                'step_abandoned': state['step']
            }
            
            # Clean up active session
            del self.active_sessions[session_id]
            
            return result
        else:
            raise ValueError(f"Session {session_id} not found")