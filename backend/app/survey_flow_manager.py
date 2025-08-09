"""
Survey Flow Manager for LangGraph Integration

This replaces FlowEngine completely with a LangGraph-based manager that uses
the compiled survey graph for all operations.
"""

import uuid
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from .graphs.survey_graph import survey_graph
from .state import SurveyState
from .tools import create_session


class SurveyFlowManager:
    """
    LangGraph-based flow manager that orchestrates survey sessions.
    
    Replaces the old FlowEngine with proper state management and graph execution.
    No backward compatibility - clean slate approach.
    """

    def __init__(self):
        """Initialize the flow manager with compiled graph."""
        self.graph = survey_graph
        
    def _create_initial_state(
        self, 
        session_id: str, 
        form_id: str, 
        client_id: Optional[str] = None, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> SurveyState:
        """
        Create initial SurveyState for new session.
        
        Args:
            session_id: Unique session identifier
            form_id: Form configuration identifier
            client_id: Optional client identifier
            metadata: Additional session metadata
            
        Returns:
            Initialized SurveyState with minimal required fields
        """
        return {
            'session_id': session_id,
            'form_id': form_id,
            'client_id': client_id,
            'metadata': metadata or {},
            'step': 0,
            'completed': False,
            'last_updated': datetime.now().isoformat(),
            'started_at': datetime.now().isoformat(),
            
            # Collections - will be populated by graph
            'all_questions': [],
            'asked_questions': [],
            'current_step_questions': [],
            'phrased_questions': [],
            'responses': [],
            
            # Scoring and status
            'score': 0,
            'lead_status': 'unknown',
            'min_questions_met': False,
            'failed_required': False,
            
            # Engagement content
            'step_headline': '',
            'step_motivation': '',
            
            # Completion data
            'completion_message': '',
            'next_steps': [],
            'completed_at': None
        }

    async def start_session(
        self, 
        form_id: str, 
        client_id: Optional[str] = None, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Start a new survey session using LangGraph.
        
        Args:
            form_id: Form configuration identifier
            client_id: Optional client identifier  
            metadata: Additional session metadata
            
        Returns:
            Dict with session_id, first step questions, and content
        """
        try:
            # Generate unique session ID
            session_id = str(uuid.uuid4())
            
            # Create initial state
            initial_state = self._create_initial_state(session_id, form_id, client_id, metadata)
            
            # Create session in database using our tool
            session_data = {
                'session_id': session_id,
                'form_id': form_id,
                'client_id': client_id,
                'started_at': initial_state['started_at'],
                'metadata': json.dumps(metadata or {})
            }
            create_session.invoke({
                'session_data': json.dumps(session_data)
            })
            
            # Execute graph to prepare first step
            # Graph will initialize, select questions, phrase them, create engagement
            final_state = self.graph.invoke(initial_state)
            
            # Extract questions for API response
            questions_with_phrasing = []
            current_questions = final_state.get('current_step_questions', [])
            phrased_questions = final_state.get('phrased_questions', [])
            
            for i, question in enumerate(current_questions):
                phrased_text = phrased_questions[i] if i < len(phrased_questions) else question.get('question', '')
                questions_with_phrasing.append({
                    **question,
                    'phrased_question': phrased_text
                })
            
            return {
                'session_id': session_id,
                'step': final_state.get('step', 1),
                'headline': final_state.get('step_headline', ''),
                'motivation': final_state.get('step_motivation', ''),
                'questions': questions_with_phrasing
            }
            
        except Exception as e:
            print(f"Error starting session: {e}")
            # Return fallback response
            return {
                'session_id': session_id,
                'step': 1,
                'headline': 'Let\'s get started! 🚀',
                'motivation': 'Help us understand your needs better.',
                'questions': [],
                'error': str(e)
            }

    async def advance_session_step(
        self, 
        session_id: str, 
        responses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Advance session to next step with user responses.
        
        Args:
            session_id: Session identifier
            responses: List of user responses for current step
            
        Returns:
            Dict with next step questions and content, or completion flag
        """
        try:
            # Load current session state (in production, this would come from database)
            # For now, we'll create a state with the responses
            current_state = self._reconstruct_session_state(session_id, responses)
            
            # Execute graph with updated state
            final_state = self.graph.invoke(current_state)
            
            # Check if session completed
            if final_state.get('completed', False):
                return {
                    'completed': True,
                    'session_id': session_id,
                    'completion_message': final_state.get('completion_message', ''),
                    'next_steps': final_state.get('next_steps', []),
                    'final_score': final_state.get('score', 0),
                    'lead_status': final_state.get('lead_status', 'unknown')
                }
            
            # Prepare next step questions
            questions_with_phrasing = []
            current_questions = final_state.get('current_step_questions', [])
            phrased_questions = final_state.get('phrased_questions', [])
            
            for i, question in enumerate(current_questions):
                phrased_text = phrased_questions[i] if i < len(phrased_questions) else question.get('question', '')
                questions_with_phrasing.append({
                    **question,
                    'phrased_question': phrased_text
                })
            
            return {
                'session_id': session_id,
                'step': final_state.get('step', 1),
                'headline': final_state.get('step_headline', ''),
                'motivation': final_state.get('step_motivation', ''),
                'questions': questions_with_phrasing,
                'total_responses': len(final_state.get('responses', []))
            }
            
        except Exception as e:
            print(f"Error advancing session: {e}")
            return {
                'completed': True,
                'session_id': session_id,
                'error': str(e)
            }

    def _reconstruct_session_state(
        self, 
        session_id: str, 
        new_responses: List[Dict[str, Any]]
    ) -> SurveyState:
        """
        Reconstruct session state with new responses.
        
        In production, this would load from database and merge with new responses.
        For now, we create a minimal state with the responses.
        
        Args:
            session_id: Session identifier
            new_responses: New responses to add to state
            
        Returns:
            SurveyState with current responses and session data
        """
        # In production, load existing session data from database
        # For now, create minimal state
        return {
            'session_id': session_id,
            'form_id': 'dogwalk_demo_form',  # Default for demo
            'client_id': None,
            'metadata': {},
            'step': len(new_responses),  # Estimate based on responses
            'completed': False,
            'last_updated': datetime.now().isoformat(),
            'started_at': datetime.now().isoformat(),
            
            # Add new responses
            'responses': new_responses,
            'asked_questions': [r.get('question_id') for r in new_responses],
            
            # Collections - will be updated by graph
            'all_questions': [],
            'current_step_questions': [],
            'phrased_questions': [],
            
            # Scoring and status - will be calculated by graph
            'score': 0,
            'lead_status': 'unknown',
            'min_questions_met': len(new_responses) >= 4,
            'failed_required': False,
            
            # Engagement content - will be generated by graph
            'step_headline': '',
            'step_motivation': '',
            
            # Completion data
            'completion_message': '',
            'next_steps': [],
            'completed_at': None
        }

    async def finalize_session(
        self, 
        session_id: str, 
        final_responses: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Finalize session and generate completion results.
        
        Args:
            session_id: Session identifier
            final_responses: Optional final responses to process
            
        Returns:
            Dict with completion message and final status
        """
        try:
            # Reconstruct state with any final responses
            current_state = self._reconstruct_session_state(
                session_id, 
                final_responses or []
            )
            
            # Force completion by setting completed flag
            current_state['completed'] = True
            current_state['last_updated'] = datetime.now().isoformat()
            
            # Execute graph one final time to generate completion message
            final_state = self.graph.invoke(current_state)
            
            return {
                'session_id': session_id,
                'completed_at': final_state.get('last_updated', datetime.now().isoformat()),
                'completion_message': final_state.get('completion_message', 'Thank you for your time!'),
                'next_steps': final_state.get('next_steps', []),
                'final_score': final_state.get('score', 0),
                'lead_status': final_state.get('lead_status', 'unknown')
            }
            
        except Exception as e:
            print(f"Error finalizing session: {e}")
            return {
                'session_id': session_id,
                'completed_at': datetime.now().isoformat(),
                'completion_message': 'Thank you for your time!',
                'next_steps': [],
                'final_score': 0,
                'lead_status': 'unknown',
                'error': str(e)
            }

    async def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current session status.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dict with session status information or None if not found
        """
        try:
            # In production, this would query the database
            # For now, return basic status structure
            return {
                'session_id': session_id,
                'completed': False,
                'form_id': 'dogwalk_demo_form',
                'last_updated': datetime.now().isoformat(),
                'lead_status': 'unknown',
                'responses_count': 0,
                'score': 0,
                'started_at': datetime.now().isoformat(),
                'step': 0
            }
            
        except Exception as e:
            print(f"Error getting session status: {e}")
            return None

    async def mark_session_abandoned(self, session_id: str) -> Dict[str, Any]:
        """
        Mark session as abandoned for analytics.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dict with abandonment details
        """
        try:
            abandoned_at = datetime.now().isoformat()
            
            # In production, this would update the database
            return {
                'session_id': session_id,
                'abandoned_at': abandoned_at,
                'responses_collected': 0,  # Would be loaded from DB
                'step_abandoned': 0  # Would be loaded from DB
            }
            
        except Exception as e:
            print(f"Error marking session abandoned: {e}")
            return {
                'session_id': session_id,
                'abandoned_at': datetime.now().isoformat(),
                'error': str(e)
            }