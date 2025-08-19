"""Question Strategy Supervisor - Intelligent question selection and flow management."""

from __future__ import annotations
from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime

from .base_supervisor import SupervisorAgent, SupervisorDecision
from ...state import QuestionStrategyState, CoreSurveyState

logger = logging.getLogger(__name__)


class QuestionStrategySupervisor(SupervisorAgent):
    """Supervisor for intelligent question selection and questioning strategy."""
    
    def __init__(self, **kwargs):
        super().__init__(name="QuestionStrategySupervisor", **kwargs)
        # Internal state specific to this supervisor
        self.internal_state = {
            "strategy_cache": {},
            "performance_history": [],
            "question_effectiveness": {},
            "current_strategy_id": None
        }
        
    def get_system_prompt(self) -> str:
        """System prompt for question strategy supervisor."""
        return """You are the Question Strategy Supervisor for an intelligent lead generation survey.

Your responsibilities:
1. Select optimal questions based on lead progression and engagement
2. Determine questioning strategy (exploratory, qualifying, contact-gathering)
3. Adapt question flow based on response quality and lead status
4. Coordinate with Lead Intelligence Supervisor for optimal qualification
5. Balance engagement with lead qualification efficiency

Principles:
- Start with engaging, easy questions to build momentum
- Ask qualifying questions after establishing engagement
- Gather contact info only for promising leads
- Adapt strategy based on real-time lead assessment
- Consider abandonment risk in question selection

Provide strategic decisions with clear reasoning and confidence scores."""
    
    def make_decision(self, state: QuestionStrategyState, context: Dict[str, Any] = None) -> SupervisorDecision:
        """Make intelligent question selection decision."""
        try:
            # Analyze current question strategy state
            strategy_analysis = self._analyze_current_strategy(state)
            
            # Get context from shared state if needed
            shared_context = context or {}
            lead_intelligence_context = shared_context.get('lead_intelligence', {})
            engagement_context = shared_context.get('engagement', {})
            
            # Make strategic decision about next questions
            decision = self._make_question_strategy_decision(
                state, strategy_analysis, lead_intelligence_context, engagement_context
            )
            
            # Update internal state
            self._update_internal_state(decision, state)
            
            return decision
            
        except Exception as e:
            return self.handle_error(e, "question strategy decision")
    
    def _analyze_current_strategy(self, state: QuestionStrategyState) -> Dict[str, Any]:
        """Analyze the current questioning strategy and effectiveness."""
        asked_questions = state.get('asked_questions', [])
        current_questions = state.get('current_questions', [])
        selection_history = state.get('selection_history', [])
        
        analysis = {
            "questions_asked_count": len(asked_questions),
            "current_step_count": len(current_questions),
            "strategy_effectiveness": self._calculate_strategy_effectiveness(selection_history),
            "question_categories_used": self._analyze_question_categories(state),
            "remaining_opportunities": self._assess_remaining_opportunities(state)
        }
        
        return analysis
    
    def _make_question_strategy_decision(self, 
                                       state: QuestionStrategyState, 
                                       strategy_analysis: Dict[str, Any],
                                       lead_context: Dict[str, Any],
                                       engagement_context: Dict[str, Any]) -> SupervisorDecision:
        """Make strategic decision using LLM analysis."""
        
        # Prepare context for LLM
        context_summary = self._prepare_strategy_context(
            state, strategy_analysis, lead_context, engagement_context
        )
        
        messages = [
            {
                "role": "user",
                "content": f"""Analyze the current question strategy state and make a strategic decision.

CONTEXT:
{context_summary}

STRATEGY OPTIONS:
1. EXPLORATORY - Ask engaging questions to build rapport and gather basic info
2. QUALIFYING - Focus on lead qualification and business need assessment  
3. CONTACT_GATHERING - Collect contact information from promising leads
4. ADAPTIVE - Mix strategies based on real-time assessment
5. COMPLETION_PREP - Final questions before survey completion

Provide your decision in JSON format:
{{
    "strategy": "EXPLORATORY|QUALIFYING|CONTACT_GATHERING|ADAPTIVE|COMPLETION_PREP",
    "question_ids": [1, 2, 3],
    "question_count": 2,
    "reasoning": "detailed reasoning for strategy choice",
    "confidence": 0.85,
    "adaptations": ["specific adaptations to make"],
    "success_metrics": ["metrics to track success"],
    "fallback_plan": "strategy if this approach fails"
}}

Select 1-3 questions that align with your chosen strategy."""
            }
        ]
        
        try:
            response = self.invoke_llm(messages)
            decision_data = json.loads(response)
            
            return self.create_decision(
                decision=decision_data.get("strategy", "ADAPTIVE"),
                reasoning=decision_data.get("reasoning", "Default strategy selection"),
                confidence=decision_data.get("confidence", 0.7),
                recommendations=decision_data.get("adaptations", []),
                metadata={
                    "question_ids": decision_data.get("question_ids", []),
                    "question_count": decision_data.get("question_count", 2),
                    "success_metrics": decision_data.get("success_metrics", []),
                    "fallback_plan": decision_data.get("fallback_plan", ""),
                    "strategy_analysis": strategy_analysis
                }
            )
            
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"Failed to parse LLM strategy decision: {e}")
            return self._make_fallback_strategy_decision(state, strategy_analysis)
    
    def _prepare_strategy_context(self, 
                                state: QuestionStrategyState,
                                strategy_analysis: Dict[str, Any], 
                                lead_context: Dict[str, Any],
                                engagement_context: Dict[str, Any]) -> str:
        """Prepare comprehensive context for strategy decision."""
        
        context_parts = [
            "=== CURRENT STRATEGY STATE ===",
            f"Questions Asked: {strategy_analysis['questions_asked_count']}",
            f"Current Step Questions: {strategy_analysis['current_step_count']}",
            f"Strategy Effectiveness: {strategy_analysis['strategy_effectiveness']:.2f}",
            "",
            "=== AVAILABLE QUESTIONS ==="
        ]
        
        # Show available questions by category
        all_questions = state.get('all_questions', [])
        asked_questions = state.get('asked_questions', [])
        available_questions = [q for q in all_questions if q.get('question_id', q.get('id')) not in asked_questions]
        
        question_categories = {}
        for q in available_questions:
            category = self._categorize_question(q)
            if category not in question_categories:
                question_categories[category] = []
            question_categories[category].append(q)
        
        for category, questions in question_categories.items():
            context_parts.append(f"{category.upper()}: {len(questions)} questions")
            for q in questions[:3]:  # Show first 3 questions in each category
                context_parts.append(f"  Q{q['id']}: {q['question'][:80]}...")
        
        context_parts.extend([
            "",
            "=== LEAD INTELLIGENCE CONTEXT ===",
            f"Current Score: {lead_context.get('current_score', 'unknown')}",
            f"Lead Status: {lead_context.get('lead_status', 'unknown')}",
            f"Risk Factors: {', '.join(lead_context.get('risk_factors', []))}"
        ])
        
        context_parts.extend([
            "",
            "=== ENGAGEMENT CONTEXT ===",
            f"Abandonment Risk: {engagement_context.get('abandonment_risk', 'unknown')}",
            f"Engagement Level: {engagement_context.get('engagement_level', 'unknown')}"
        ])
        
        return "\n".join(context_parts)
    
    def _calculate_strategy_effectiveness(self, selection_history: List[Dict[str, Any]]) -> float:
        """Calculate effectiveness of recent strategy decisions."""
        if not selection_history:
            return 0.5  # Default neutral effectiveness
        
        recent_decisions = selection_history[-3:]  # Last 3 decisions
        total_effectiveness = 0.0
        
        for decision in recent_decisions:
            # Simple effectiveness based on confidence and outcomes
            confidence = decision.get('confidence', 0.5)
            # In a real system, this would include actual performance metrics
            effectiveness = confidence * 0.8  # Placeholder calculation
            total_effectiveness += effectiveness
        
        return total_effectiveness / len(recent_decisions)
    
    def _analyze_question_categories(self, state: QuestionStrategyState) -> Dict[str, int]:
        """Analyze which question categories have been used."""
        asked_questions = state.get('asked_questions', [])
        all_questions = state.get('all_questions', [])
        
        categories_used = {}
        
        for q in all_questions:
            if q['id'] in asked_questions:
                category = self._categorize_question(q)
                categories_used[category] = categories_used.get(category, 0) + 1
        
        return categories_used
    
    def _categorize_question(self, question: Dict[str, Any]) -> str:
        """Categorize a question based on its content and purpose."""
        question_text = question.get('question', '').lower()
        
        if any(word in question_text for word in ['name', 'email', 'phone', 'contact']):
            return 'contact'
        elif any(word in question_text for word in ['dog', 'pet', 'breed', 'animal']):
            return 'personal'
        elif any(word in question_text for word in ['service', 'frequency', 'times', 'often']):
            return 'service'
        elif any(word in question_text for word in ['location', 'where', 'area', 'city']):
            return 'location'
        else:
            return 'general'
    
    def _assess_remaining_opportunities(self, state: QuestionStrategyState) -> Dict[str, Any]:
        """Assess remaining opportunities for different strategies."""
        all_questions = state.get('all_questions', [])
        asked_questions = state.get('asked_questions', [])
        available_questions = [q for q in all_questions if q.get('question_id', q.get('id')) not in asked_questions]
        
        opportunities = {
            "total_remaining": len(available_questions),
            "by_category": {},
            "high_value_remaining": 0
        }
        
        for q in available_questions:
            category = self._categorize_question(q)
            opportunities["by_category"][category] = opportunities["by_category"].get(category, 0) + 1
            
            # Check for high-value questions (those with scoring rubrics)
            if q.get('scoring_rubric'):
                opportunities["high_value_remaining"] += 1
        
        return opportunities
    
    def _make_fallback_strategy_decision(self, state: QuestionStrategyState, strategy_analysis: Dict[str, Any]) -> SupervisorDecision:
        """Make rule-based fallback decision when LLM fails."""
        asked_count = strategy_analysis['questions_asked_count']
        
        # Simple rule-based strategy selection
        if asked_count < 2:
            strategy = "EXPLORATORY"
            reasoning = "Early stage - build engagement with exploratory questions"
        elif asked_count < 4:
            strategy = "QUALIFYING"
            reasoning = "Mid-stage - focus on lead qualification"
        elif asked_count < 6:
            strategy = "ADAPTIVE"
            reasoning = "Late stage - adapt based on lead quality"
        else:
            strategy = "COMPLETION_PREP"
            reasoning = "Final stage - prepare for completion"
        
        # Select 2 questions using simple logic
        all_questions = state.get('all_questions', [])
        asked_questions = state.get('asked_questions', [])
        available = [q for q in all_questions if q.get('question_id', q.get('id')) not in asked_questions]
        selected_ids = [q.get('question_id', q.get('id')) for q in available[:2]] if available else []
        
        return self.create_decision(
            decision=strategy,
            reasoning=f"Fallback strategy: {reasoning}",
            confidence=0.6,
            recommendations=["Monitor for LLM recovery"],
            metadata={
                "question_ids": selected_ids,
                "question_count": len(selected_ids),
                "fallback": True
            }
        )
    
    def _update_internal_state(self, decision: SupervisorDecision, state: QuestionStrategyState):
        """Update internal supervisor state based on decision."""
        try:
            # Update strategy cache
            strategy_id = f"{decision.decision}_{decision.timestamp}"
            self.internal_state["strategy_cache"][strategy_id] = {
                "decision": decision.to_dict(),
                "state_snapshot": {
                    "questions_asked": len(state.get('asked_questions', [])),
                    "strategy": decision.decision
                }
            }
            
            # Update current strategy
            self.internal_state["current_strategy_id"] = strategy_id
            
            # Track performance (would be updated with actual outcomes)
            self.internal_state["performance_history"].append({
                "timestamp": decision.timestamp,
                "strategy": decision.decision,
                "confidence": decision.confidence,
                "question_ids": decision.metadata.get('question_ids', [])
            })
            
            # Limit history size
            if len(self.internal_state["performance_history"]) > 50:
                self.internal_state["performance_history"] = self.internal_state["performance_history"][-50:]
            
            logger.debug(f"Updated internal state for strategy: {decision.decision}")
            
        except Exception as e:
            logger.error(f"Failed to update internal state: {e}")
    
    def get_state_summary(self) -> Dict[str, Any]:
        """Get summary of internal state for coordination."""
        return {
            "current_strategy": self.internal_state.get("current_strategy_id"),
            "performance_trend": self._calculate_performance_trend(),
            "strategy_recommendations": self._get_strategy_recommendations(),
            "question_effectiveness": dict(list(self.internal_state["question_effectiveness"].items())[-5:])
        }
    
    def _calculate_performance_trend(self) -> str:
        """Calculate recent performance trend."""
        history = self.internal_state["performance_history"]
        if len(history) < 3:
            return "insufficient_data"
        
        recent_confidence = [h['confidence'] for h in history[-3:]]
        if recent_confidence[-1] > recent_confidence[0]:
            return "improving"
        elif recent_confidence[-1] < recent_confidence[0]:
            return "declining"
        else:
            return "stable"
    
    def _get_strategy_recommendations(self) -> List[str]:
        """Get strategic recommendations based on internal state."""
        recommendations = []
        
        performance_trend = self._calculate_performance_trend()
        if performance_trend == "declining":
            recommendations.append("Consider strategy adaptation")
        
        recent_decisions = self.decision_history[-3:] if self.decision_history else []
        if len(set(d.decision for d in recent_decisions)) == 1:
            recommendations.append("Explore alternative strategies")
        
        return recommendations