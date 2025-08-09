"""Supervisor Integration Nodes - Connect supervisors to LangGraph flow."""

from __future__ import annotations
from typing import Dict, Any, Optional
import logging
from datetime import datetime

from ...state import (
    SurveyGraphState,
    CoreSurveyState,
    MasterFlowState,
    QuestionStrategyState,
    LeadIntelligenceState,
    EngagementState
)
from ..supervisors import (
    MasterFlowSupervisor,
    QuestionStrategySupervisor,
    LeadIntelligenceSupervisor,
    EngagementSupervisor,
    SupervisorCoordinator
)

logger = logging.getLogger(__name__)

# Initialize supervisors (singleton pattern)
_supervisors_initialized = False
_master_supervisor: Optional[MasterFlowSupervisor] = None
_question_supervisor: Optional[QuestionStrategySupervisor] = None
_lead_supervisor: Optional[LeadIntelligenceSupervisor] = None
_engagement_supervisor: Optional[EngagementSupervisor] = None
_coordinator: Optional[SupervisorCoordinator] = None


def initialize_supervisors():
    """Initialize all supervisor instances."""
    global _supervisors_initialized, _master_supervisor, _question_supervisor
    global _lead_supervisor, _engagement_supervisor, _coordinator
    
    if _supervisors_initialized:
        return
    
    logger.info("Initializing supervisor hierarchy...")
    
    # Create coordinator
    _coordinator = SupervisorCoordinator()
    
    # Create supervisors
    _master_supervisor = MasterFlowSupervisor()
    _question_supervisor = QuestionStrategySupervisor()
    _lead_supervisor = LeadIntelligenceSupervisor()
    _engagement_supervisor = EngagementSupervisor()
    
    # Register domain supervisors with master
    _master_supervisor.register_domain_supervisor(_question_supervisor)
    _master_supervisor.register_domain_supervisor(_lead_supervisor)
    _master_supervisor.register_domain_supervisor(_engagement_supervisor)
    
    # Register all supervisors with coordinator
    _coordinator.register_supervisor(_master_supervisor)
    _coordinator.register_supervisor(_question_supervisor)
    _coordinator.register_supervisor(_lead_supervisor)
    _coordinator.register_supervisor(_engagement_supervisor)
    
    _supervisors_initialized = True
    logger.info("Supervisor hierarchy initialized successfully")


def master_flow_coordination_node(state: SurveyGraphState) -> Dict[str, Any]:
    """Master flow coordination node that orchestrates the survey flow."""
    initialize_supervisors()
    
    try:
        # Extract master flow state
        master_state = state.get('master_flow', {})
        
        # Get shared context from other supervisors
        shared_context = {
            'question_strategy': _question_supervisor.get_state_summary() if _question_supervisor else {},
            'lead_intelligence': _lead_supervisor.get_state_summary() if _lead_supervisor else {},
            'engagement': _engagement_supervisor.get_state_summary() if _engagement_supervisor else {}
        }
        
        # Make master flow decision
        decision = _master_supervisor.make_decision(master_state, shared_context)
        
        # Update state with decision
        flow_updates = {
            'flow_phase': _determine_flow_phase(decision),
            'flow_strategy': decision.decision,
            'completion_probability': _calculate_completion_probability(state, decision)
        }
        
        # Add coordination messages
        coordination_message = {
            'timestamp': datetime.utcnow().isoformat(),
            'from': 'MasterFlowSupervisor',
            'decision': decision.decision,
            'reasoning': decision.reasoning,
            'confidence': decision.confidence
        }
        
        return {
            'master_flow': {**master_state, **flow_updates},
            'supervisor_messages': state.get('supervisor_messages', []) + [coordination_message]
        }
        
    except Exception as e:
        logger.error(f"Master flow coordination failed: {e}")
        return {'master_flow': master_state}


def question_strategy_node(state: SurveyGraphState) -> Dict[str, Any]:
    """Question strategy supervision node."""
    initialize_supervisors()
    
    try:
        # Extract question strategy state
        question_state = state.get('question_strategy', {})
        
        # Get shared context
        shared_context = state.get('shared_context', {})
        
        # Make question strategy decision
        decision = _question_supervisor.make_decision(question_state, shared_context)
        
        # Extract question selection from decision
        selected_question_ids = decision.metadata.get('question_ids', [])
        
        # Get selected questions from all questions
        all_questions = question_state.get('all_questions', [])
        selected_questions = [q for q in all_questions if q['id'] in selected_question_ids]
        
        # Update state
        strategy_updates = {
            'current_questions': selected_questions,
            'question_strategy': {
                'type': decision.decision,
                'reasoning': decision.reasoning,
                'confidence': decision.confidence
            },
            'selection_history': question_state.get('selection_history', []) + [decision.to_dict()]
        }
        
        # Add supervisor message
        message = {
            'timestamp': datetime.utcnow().isoformat(),
            'from': 'QuestionStrategySupervisor',
            'decision': decision.decision,
            'selected_questions': len(selected_questions)
        }
        
        return {
            'question_strategy': {**question_state, **strategy_updates},
            'supervisor_messages': state.get('supervisor_messages', []) + [message]
        }
        
    except Exception as e:
        logger.error(f"Question strategy supervision failed: {e}")
        # Fallback to simple selection
        return _fallback_question_selection(state)


def lead_intelligence_node(state: SurveyGraphState) -> Dict[str, Any]:
    """Lead intelligence supervision node."""
    initialize_supervisors()
    
    try:
        # Extract lead intelligence state
        lead_state = state.get('lead_intelligence', {})
        
        # Get shared context
        shared_context = state.get('shared_context', {})
        
        # Make lead assessment decision
        decision = _lead_supervisor.make_decision(lead_state, shared_context)
        
        # Update state
        intelligence_updates = {
            'current_score': decision.metadata.get('score', 0),
            'lead_status': decision.decision.lower() if decision.decision in ['YES', 'MAYBE', 'NO'] else 'unknown',
            'score_history': lead_state.get('score_history', []) + [{
                'timestamp': decision.timestamp,
                'score': decision.metadata.get('score', 0),
                'qualification': decision.decision
            }],
            'qualification_reasoning': lead_state.get('qualification_reasoning', []) + [{
                'timestamp': decision.timestamp,
                'reasoning': decision.reasoning,
                'confidence': decision.confidence
            }],
            'risk_factors': decision.metadata.get('risk_factors', []),
            'positive_indicators': decision.metadata.get('positive_indicators', [])
        }
        
        # Add supervisor message
        message = {
            'timestamp': datetime.utcnow().isoformat(),
            'from': 'LeadIntelligenceSupervisor',
            'qualification': decision.decision,
            'score': decision.metadata.get('score', 0),
            'confidence': decision.confidence
        }
        
        return {
            'lead_intelligence': {**lead_state, **intelligence_updates},
            'supervisor_messages': state.get('supervisor_messages', []) + [message]
        }
        
    except Exception as e:
        logger.error(f"Lead intelligence supervision failed: {e}")
        return {'lead_intelligence': lead_state}


def engagement_supervision_node(state: SurveyGraphState) -> Dict[str, Any]:
    """Engagement supervision node."""
    initialize_supervisors()
    
    try:
        # Extract engagement state
        engagement_state = state.get('engagement', {})
        
        # Get shared context
        shared_context = state.get('shared_context', {})
        
        # Make engagement decision
        decision = _engagement_supervisor.make_decision(engagement_state, shared_context)
        
        # Update state
        engagement_updates = {
            'abandonment_risk': decision.metadata.get('abandonment_risk', 0.5),
            'step_headline': decision.metadata.get('headline', 'Let\'s continue!'),
            'step_motivation': decision.metadata.get('motivation', 'Thanks for sharing with us.'),
            'engagement_history': engagement_state.get('engagement_history', []) + [{
                'timestamp': decision.timestamp,
                'strategy': decision.decision,
                'confidence': decision.confidence
            }],
            'retention_strategies': decision.recommendations
        }
        
        # Calculate engagement metrics
        engagement_metrics = _calculate_engagement_metrics(state, decision)
        engagement_updates['engagement_metrics'] = engagement_metrics
        
        # Add supervisor message
        message = {
            'timestamp': datetime.utcnow().isoformat(),
            'from': 'EngagementSupervisor',
            'strategy': decision.decision,
            'abandonment_risk': decision.metadata.get('abandonment_risk', 0.5)
        }
        
        return {
            'engagement': {**engagement_state, **engagement_updates},
            'supervisor_messages': state.get('supervisor_messages', []) + [message]
        }
        
    except Exception as e:
        logger.error(f"Engagement supervision failed: {e}")
        return _fallback_engagement_content(state)


def supervisor_coordination_node(state: SurveyGraphState) -> Dict[str, Any]:
    """Coordinate between all supervisors and share context."""
    initialize_supervisors()
    
    try:
        # Gather state summaries from each supervisor
        question_summary = _question_supervisor.get_state_summary() if _question_supervisor else {}
        lead_summary = _lead_supervisor.get_state_summary() if _lead_supervisor else {}
        engagement_summary = _engagement_supervisor.get_state_summary() if _engagement_supervisor else {}
        
        # Create shared context for next iteration
        shared_context = {
            'question_strategy': question_summary,
            'lead_intelligence': lead_summary,
            'engagement': engagement_summary,
            'coordination_timestamp': datetime.utcnow().isoformat()
        }
        
        # Get coordination messages from coordinator
        coordination_messages = _coordinator.get_coordination_context() if _coordinator else []
        
        return {
            'shared_context': shared_context,
            'supervisor_messages': state.get('supervisor_messages', []) + coordination_messages
        }
        
    except Exception as e:
        logger.error(f"Supervisor coordination failed: {e}")
        return {'shared_context': state.get('shared_context', {})}


# Helper functions

def _determine_flow_phase(decision) -> str:
    """Determine current flow phase based on master decision."""
    decision_type = decision.decision
    
    if decision_type == "CONTINUE":
        return "questioning"
    elif decision_type == "COMPLETE":
        return "completing"
    elif decision_type == "RECOVER":
        return "recovering"
    elif decision_type == "ADAPT":
        return "adapting"
    else:
        return "questioning"


def _calculate_completion_probability(state: SurveyGraphState, decision) -> float:
    """Calculate probability of survey completion."""
    # Simple calculation based on multiple factors
    lead_state = state.get('lead_intelligence', {})
    engagement_state = state.get('engagement', {})
    question_state = state.get('question_strategy', {})
    
    # Base probability
    probability = 0.5
    
    # Adjust based on lead score
    current_score = lead_state.get('current_score', 50)
    if current_score > 70:
        probability += 0.2
    elif current_score < 30:
        probability -= 0.2
    
    # Adjust based on abandonment risk
    abandonment_risk = engagement_state.get('abandonment_risk', 0.5)
    probability -= (abandonment_risk * 0.3)
    
    # Adjust based on questions remaining
    all_questions = question_state.get('all_questions', [])
    asked_questions = question_state.get('asked_questions', [])
    completion_ratio = len(asked_questions) / len(all_questions) if all_questions else 0
    probability += (completion_ratio * 0.2)
    
    # Factor in supervisor confidence
    probability *= decision.confidence
    
    return max(0.0, min(1.0, probability))


def _calculate_engagement_metrics(state: SurveyGraphState, decision) -> Dict[str, Any]:
    """Calculate current engagement metrics."""
    lead_state = state.get('lead_intelligence', {})
    responses = lead_state.get('responses', [])
    
    metrics = {
        'response_count': len(responses),
        'engagement_score': 1.0 - decision.metadata.get('abandonment_risk', 0.5),
        'strategy_confidence': decision.confidence,
        'time_on_survey': 0  # Would be calculated from timestamps in real system
    }
    
    return metrics


def _fallback_question_selection(state: SurveyGraphState) -> Dict[str, Any]:
    """Fallback question selection when supervisor fails."""
    question_state = state.get('question_strategy', {})
    all_questions = question_state.get('all_questions', [])
    asked_questions = question_state.get('asked_questions', [])
    
    # Simple selection of next 2 available questions
    available = [q for q in all_questions if q['id'] not in asked_questions]
    selected = available[:2] if available else []
    
    return {
        'question_strategy': {
            **question_state,
            'current_questions': selected,
            'question_strategy': {'type': 'fallback', 'reasoning': 'Supervisor failure'}
        }
    }


def _fallback_engagement_content(state: SurveyGraphState) -> Dict[str, Any]:
    """Fallback engagement content when supervisor fails."""
    engagement_state = state.get('engagement', {})
    
    return {
        'engagement': {
            **engagement_state,
            'step_headline': 'Let\'s continue! 🚀',
            'step_motivation': 'Thanks for taking the time to share with us.',
            'abandonment_risk': 0.5
        }
    }