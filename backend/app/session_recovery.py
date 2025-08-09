"""Session Recovery System for Survey Flow

Handles recovery of interrupted sessions, state restoration, and continuation logic.
Enables users to resume where they left off even after browser crashes or timeouts.
"""

from typing import Optional, Dict, Any, Tuple
import logging
from datetime import datetime, timedelta

from .database import db
from .state import SurveyGraphState

logger = logging.getLogger(__name__)


class SessionRecoveryManager:
    """Manages session recovery and state restoration"""
    
    def __init__(self):
        self.db = db
    
    def can_recover_session(self, session_id: str) -> Tuple[bool, str]:
        """
        Check if a session can be recovered.
        
        Returns:
            Tuple of (can_recover: bool, reason: str)
        """
        try:
            # Get session data
            session = self.db.get_lead_session(session_id)
            if not session:
                return False, "Session not found"
            
            # Check if already completed
            if session.get('completed', False):
                completion_type = session.get('completion_type', 'unknown')
                return False, f"Session already completed ({completion_type})"
            
            # Check if too much time has passed
            last_activity = session.get('last_activity_timestamp')
            if last_activity:
                try:
                    last_time = datetime.fromisoformat(last_activity)
                    time_since = datetime.now() - last_time
                    
                    # Don't recover if abandoned for more than 1 hour
                    if time_since > timedelta(hours=1):
                        return False, "Session too old to recover"
                except:
                    pass
            
            # Check if marked as abandoned
            abandonment_status = session.get('abandonment_status', 'active')
            if abandonment_status == 'abandoned':
                return False, "Session was marked as abandoned"
            
            # Check if we have responses (some progress made)
            responses = self.db.get_session_responses(session_id)
            if not responses:
                return True, "Can recover from beginning"
            
            return True, f"Can recover with {len(responses)} responses"
            
        except Exception as e:
            logger.error(f"Error checking session recovery for {session_id}: {e}")
            return False, f"Error checking recovery: {str(e)}"
    
    def recover_session_state(self, session_id: str) -> Optional[SurveyGraphState]:
        """
        Recover complete session state from database.
        
        Returns:
            Restored SurveyGraphState or None if recovery fails
        """
        try:
            # Check if recovery is possible
            can_recover, reason = self.can_recover_session(session_id)
            if not can_recover:
                logger.warning(f"Cannot recover session {session_id}: {reason}")
                return None
            
            # Try to get saved snapshot first
            snapshot = self.db.get_latest_session_snapshot(session_id)
            if snapshot:
                logger.info(f"Recovering session {session_id} from snapshot")
                return self._restore_from_snapshot(snapshot)
            
            # Fallback: reconstruct from database records
            logger.info(f"Reconstructing session {session_id} from database")
            return self._reconstruct_from_database(session_id)
            
        except Exception as e:
            logger.error(f"Error recovering session {session_id}: {e}")
            return None
    
    def _restore_from_snapshot(self, snapshot: Dict[str, Any]) -> SurveyGraphState:
        """Restore state from saved snapshot"""
        full_state = snapshot.get('full_state', {})
        
        # Ensure we have the right type structure
        if not isinstance(full_state, dict):
            raise ValueError("Invalid snapshot state format")
        
        # Update activity timestamp to now
        if 'engagement' in full_state:
            full_state['engagement']['last_activity_timestamp'] = datetime.now().isoformat()
            full_state['engagement']['abandonment_risk'] = 0.3  # Reset risk
        
        return full_state
    
    def _reconstruct_from_database(self, session_id: str) -> SurveyGraphState:
        """Reconstruct state from individual database records"""
        # Get session data
        session = self.db.get_lead_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Get responses
        responses = self.db.get_session_responses(session_id)
        
        # Get tracking data
        tracking = self.db.get_tracking_data(session_id)
        
        # Get form and client info
        form_id = session.get('form_id')
        form = self.db.get_form(form_id) if form_id else {}
        client = self.db.get_client_by_form(form_id) if form_id else {}
        
        # Get questions asked so far
        asked_question_ids = [r.get('question_id') for r in responses if r.get('question_id')]
        
        # Reconstruct hierarchical state
        reconstructed_state = {
            'core': {
                'session_id': session_id,
                'form_id': form_id,
                'client_id': session.get('client_id'),
                'started_at': session.get('started_at'),
                'last_updated': datetime.now().isoformat(),
                'step': session.get('step', 0),
                'completed': False,
                # Add tracking fields from tracking table
                'utm_source': tracking.get('utm_source') if tracking else None,
                'utm_medium': tracking.get('utm_medium') if tracking else None,
                'utm_campaign': tracking.get('utm_campaign') if tracking else None,
                'utm_content': tracking.get('utm_content') if tracking else None,
                'utm_term': tracking.get('utm_term') if tracking else None,
                'referrer': tracking.get('referrer') if tracking else None,
                'user_agent': tracking.get('user_agent') if tracking else None,
                'ip_address': tracking.get('ip_address') if tracking else None,
                'landing_page': tracking.get('landing_page') if tracking else None,
            },
            'master_flow': {
                'core': {
                    'session_id': session_id,
                    'form_id': form_id,
                    'step': session.get('step', 0),
                    'completed': False
                },
                'flow_phase': 'questioning',
                'completion_probability': 0.6,  # Moderate since they're continuing
                'flow_strategy': 'RECOVERY'
            },
            'question_strategy': {
                'all_questions': [],  # Will be loaded by question selection node
                'asked_questions': asked_question_ids,
                'current_questions': [],
                'phrased_questions': [],
                'question_strategy': {'recovery_mode': True},
                'selection_history': []
            },
            'lead_intelligence': {
                'responses': responses,
                'current_score': session.get('current_score', 0),
                'score_history': [],
                'lead_status': session.get('lead_status', 'unknown'),
                'qualification_reasoning': [],
                'risk_factors': [],
                'positive_indicators': []
            },
            'engagement': {
                'abandonment_risk': 0.3,  # Reset for recovery
                'engagement_metrics': {},
                'step_headline': 'Welcome back! Let\'s continue where you left off.',
                'step_motivation': 'We saved your progress - just a few more questions to go.',
                'engagement_history': [],
                'retention_strategies': ['recovery_welcome'],
                'last_activity_timestamp': datetime.now().isoformat(),
                'abandonment_status': 'active',
                'time_on_step': None,
                'hesitation_indicators': 0
            },
            'supervisor_messages': [],
            'shared_context': {'recovered_session': True},
            'pending_responses': [],
            'frontend_response': None,
            'session_recovery_data': {
                'recovered_at': datetime.now().isoformat(),
                'recovery_method': 'database_reconstruction',
                'responses_recovered': len(responses)
            },
            'completion_message': None,
            'error_log': [],
            'operation_log': [
                {
                    'operation': 'session_recovery',
                    'timestamp': datetime.now().isoformat(),
                    'details': f'Recovered session with {len(responses)} responses'
                }
            ],
            'metadata': tracking or {}
        }
        
        logger.info(f"Reconstructed session {session_id} with {len(responses)} responses")
        return reconstructed_state
    
    def save_recovery_snapshot(self, session_id: str, state: SurveyGraphState, reason: str = "auto_save") -> bool:
        """
        Save current state as recovery snapshot.
        
        Args:
            session_id: Session identifier
            state: Current state to save
            reason: Reason for saving (auto_save, abandonment_risk, etc.)
            
        Returns:
            True if saved successfully
        """
        try:
            core = state.get('core', {})
            step = core.get('step', 0)
            
            # Save snapshot
            self.db.save_session_snapshot(
                session_id=session_id,
                full_state=state,
                step=step,
                recovery_reason=reason
            )
            
            # Also update session table with current data
            session_updates = {
                'step': step,
                'current_score': state.get('lead_intelligence', {}).get('current_score', 0),
                'lead_status': state.get('lead_intelligence', {}).get('lead_status', 'unknown'),
                'abandonment_status': state.get('engagement', {}).get('abandonment_status', 'active'),
                'abandonment_risk': state.get('engagement', {}).get('abandonment_risk', 0.3),
                'last_activity_timestamp': datetime.now().isoformat()
            }
            
            self.db.update_lead_session_with_tracking(session_id, session_updates)
            
            logger.debug(f"Saved recovery snapshot for {session_id} at step {step}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save recovery snapshot for {session_id}: {e}")
            return False
    
    def cleanup_old_snapshots(self, days_old: int = 7) -> int:
        """
        Clean up old recovery snapshots.
        
        Args:
            days_old: Delete snapshots older than this many days
            
        Returns:
            Number of snapshots deleted
        """
        try:
            cutoff_date = (datetime.now() - timedelta(days=days_old)).isoformat()
            
            # This would need a custom SQL query in a real implementation
            # For now, just log the intent
            logger.info(f"Would clean up snapshots older than {cutoff_date}")
            return 0
            
        except Exception as e:
            logger.error(f"Error cleaning up old snapshots: {e}")
            return 0


# Global instance
recovery_manager = SessionRecoveryManager()


# Convenience functions for API usage
def can_recover_session(session_id: str) -> Tuple[bool, str]:
    """Check if session can be recovered"""
    return recovery_manager.can_recover_session(session_id)


def recover_session(session_id: str) -> Optional[SurveyGraphState]:
    """Recover session state"""
    return recovery_manager.recover_session_state(session_id)


def save_recovery_checkpoint(session_id: str, state: SurveyGraphState, reason: str = "checkpoint") -> bool:
    """Save recovery checkpoint"""
    return recovery_manager.save_recovery_snapshot(session_id, state, reason)