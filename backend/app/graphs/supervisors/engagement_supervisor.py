"""Engagement Supervisor - User engagement, retention, and abandonment prevention."""

from __future__ import annotations
from typing import Dict, Any, List, Optional
import json
import logging
import statistics
from datetime import datetime, timedelta

from .base_supervisor import SupervisorAgent, SupervisorDecision
from ...state import EngagementState

logger = logging.getLogger(__name__)


class EngagementSupervisor(SupervisorAgent):
    """Supervisor for user engagement optimization and abandonment prevention."""
    
    def __init__(self, **kwargs):
        super().__init__(name="EngagementSupervisor", **kwargs)
        # Internal state for engagement management
        self.internal_state = {
            "engagement_model": {
                "risk_factors": self._initialize_risk_factors(),
                "engagement_indicators": self._initialize_engagement_indicators(),
                "retention_strategies": self._initialize_retention_strategies()
            },
            "user_behavior_patterns": {},
            "content_effectiveness": {
                "headlines": {},
                "motivations": {},
                "strategies": {}
            },
            "abandonment_predictions": [],
            "engagement_history": []
        }
        
    def get_system_prompt(self) -> str:
        """System prompt for engagement supervisor."""
        return """You are the Engagement Supervisor for an intelligent lead generation survey system.

Your responsibilities:
1. Monitor user engagement levels and predict abandonment risk
2. Generate compelling headlines and motivational content
3. Implement dynamic retention strategies based on user behavior
4. Optimize content for maximum completion rates
5. Adapt engagement approach based on lead quality and progress
6. Coordinate with other supervisors to balance engagement with qualification

Engagement principles:
- Create emotional connection and momentum
- Use progress psychology and gamification
- Personalize content based on user responses
- Balance encouragement with urgency
- Prevent form fatigue and cognitive overload
- Celebrate milestones and progress

Provide strategic engagement decisions with:
- Clear reasoning for content choices
- Risk assessments for abandonment
- Specific retention tactics
- Content optimization recommendations

Focus on maximizing completion while maintaining lead quality."""
    
    def make_decision(self, state: EngagementState, context: Dict[str, Any] = None) -> SupervisorDecision:
        """Make intelligent engagement and retention decision."""
        try:
            # Analyze current engagement state
            engagement_analysis = self._analyze_engagement_state(state)
            
            # Get context from other supervisors
            shared_context = context or {}
            question_context = shared_context.get('question_strategy', {})
            lead_context = shared_context.get('lead_intelligence', {})
            
            # Make engagement strategy decision
            decision = self._make_engagement_strategy_decision(
                state, engagement_analysis, question_context, lead_context
            )
            
            # Update internal state
            self._update_internal_state(decision, state)
            
            return decision
            
        except Exception as e:
            return self.handle_error(e, "engagement strategy decision")
    
    def _analyze_engagement_state(self, state: EngagementState) -> Dict[str, Any]:
        """Analyze current engagement state and risk factors."""
        engagement_metrics = state.get('engagement_metrics', {})
        engagement_history = state.get('engagement_history', [])
        abandonment_risk = state.get('abandonment_risk', 0.5)
        
        analysis = {
            "current_risk_level": self._assess_current_risk_level(state),
            "engagement_trends": self._analyze_engagement_trends(engagement_history),
            "content_performance": self._analyze_content_performance(state),
            "retention_opportunities": self._identify_retention_opportunities(state),
            "psychological_factors": self._assess_psychological_factors(state)
        }
        
        return analysis
    
    def _make_engagement_strategy_decision(self, 
                                         state: EngagementState,
                                         engagement_analysis: Dict[str, Any],
                                         question_context: Dict[str, Any],
                                         lead_context: Dict[str, Any]) -> SupervisorDecision:
        """Make strategic engagement decision using LLM analysis."""
        
        # Prepare context for LLM
        context_summary = self._prepare_engagement_context(
            state, engagement_analysis, question_context, lead_context
        )
        
        messages = [
            {
                "role": "user",
                "content": f"""Analyze the user engagement state and create an optimal engagement strategy.

CONTEXT:
{context_summary}

ENGAGEMENT STRATEGIES:
1. MOMENTUM_BUILDING - Build excitement and forward momentum
2. REASSURANCE - Reduce anxiety and build confidence
3. URGENCY - Create appropriate urgency without pressure
4. PERSONALIZATION - Highly personalized content based on responses
5. GAMIFICATION - Progress indicators and achievement celebration
6. RECOVERY - Re-engage users showing abandonment signals

Provide your strategy in JSON format:
{{
    "strategy": "MOMENTUM_BUILDING|REASSURANCE|URGENCY|PERSONALIZATION|GAMIFICATION|RECOVERY",
    "headline": "Compelling headline for this step",
    "motivation": "Motivational message to encourage continuation",
    "abandonment_risk": 0.25,
    "reasoning": "detailed reasoning for strategy choice",
    "confidence": 0.85,
    "retention_tactics": ["specific tactics to improve retention"],
    "content_adaptations": ["adaptations based on user behavior"],
    "success_indicators": ["metrics to track success"],
    "fallback_content": {{
        "headline": "Fallback headline if strategy fails",
        "motivation": "Fallback motivation message"
    }}
}}

Create content that maximizes completion while maintaining authenticity."""
            }
        ]
        
        try:
            response = self.invoke_llm(messages)
            strategy_data = json.loads(response)
            
            return self.create_decision(
                decision=strategy_data.get("strategy", "PERSONALIZATION"),
                reasoning=strategy_data.get("reasoning", "Default engagement strategy"),
                confidence=strategy_data.get("confidence", 0.7),
                recommendations=strategy_data.get("retention_tactics", []),
                metadata={
                    "headline": strategy_data.get("headline", "Let's continue!"),
                    "motivation": strategy_data.get("motivation", "Thanks for sharing with us."),
                    "abandonment_risk": strategy_data.get("abandonment_risk", 0.5),
                    "content_adaptations": strategy_data.get("content_adaptations", []),
                    "success_indicators": strategy_data.get("success_indicators", []),
                    "fallback_content": strategy_data.get("fallback_content", {}),
                    "engagement_analysis": engagement_analysis
                }
            )
            
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"Failed to parse LLM engagement strategy: {e}")
            return self._make_fallback_engagement_decision(state, engagement_analysis)
    
    def _prepare_engagement_context(self, 
                                  state: EngagementState,
                                  engagement_analysis: Dict[str, Any],
                                  question_context: Dict[str, Any],
                                  lead_context: Dict[str, Any]) -> str:
        """Prepare comprehensive context for engagement decision."""
        
        context_parts = [
            "=== ENGAGEMENT STATE ===",
            f"Current Abandonment Risk: {state.get('abandonment_risk', 0.5):.2f}",
            f"Risk Level: {engagement_analysis['current_risk_level']}",
            f"Engagement Trend: {engagement_analysis['engagement_trends']}",
            "",
            "=== ENGAGEMENT METRICS ==="
        ]
        
        engagement_metrics = state.get('engagement_metrics', {})
        for metric, value in engagement_metrics.items():
            context_parts.append(f"{metric}: {value}")
        
        context_parts.extend([
            "",
            "=== CONTENT PERFORMANCE ==="
        ])
        
        content_performance = engagement_analysis['content_performance']
        for content_type, performance in content_performance.items():
            context_parts.append(f"{content_type}: {performance}")
        
        context_parts.extend([
            "",
            "=== RETENTION OPPORTUNITIES ==="
        ])
        
        for opportunity in engagement_analysis['retention_opportunities']:
            context_parts.append(f"- {opportunity}")
        
        context_parts.extend([
            "",
            "=== PSYCHOLOGICAL FACTORS ==="
        ])
        
        psychological_factors = engagement_analysis['psychological_factors']
        for factor, assessment in psychological_factors.items():
            context_parts.append(f"{factor}: {assessment}")
        
        # Add context from other supervisors
        if question_context:
            context_parts.extend([
                "",
                "=== QUESTION STRATEGY CONTEXT ===",
                f"Current Strategy: {question_context.get('current_strategy', 'unknown')}",
                f"Performance Trend: {question_context.get('performance_trend', 'unknown')}"
            ])
        
        if lead_context:
            context_parts.extend([
                "",
                "=== LEAD INTELLIGENCE CONTEXT ===",
                f"Lead Quality: {lead_context.get('recent_qualifications', ['unknown'])[-1] if lead_context.get('recent_qualifications') else 'unknown'}",
                f"Assessment Confidence: {lead_context.get('average_confidence', 'unknown')}"
            ])
        
        return "\n".join(context_parts)
    
    def _assess_current_risk_level(self, state: EngagementState) -> str:
        """Assess current abandonment risk level."""
        abandonment_risk = state.get('abandonment_risk', 0.5)
        
        if abandonment_risk >= 0.7:
            return "high"
        elif abandonment_risk >= 0.4:
            return "medium"
        else:
            return "low"
    
    def _analyze_engagement_trends(self, engagement_history: List[Dict[str, Any]]) -> str:
        """Analyze trends in user engagement."""
        if len(engagement_history) < 2:
            return "insufficient_data"
        
        # Get recent engagement scores
        recent_scores = []
        for entry in engagement_history[-3:]:
            if 'engagement_score' in entry:
                recent_scores.append(entry['engagement_score'])
        
        if len(recent_scores) < 2:
            return "insufficient_data"
        
        if recent_scores[-1] > recent_scores[0]:
            return "improving"
        elif recent_scores[-1] < recent_scores[0]:
            return "declining"
        else:
            return "stable"
    
    def _analyze_content_performance(self, state: EngagementState) -> Dict[str, str]:
        """Analyze performance of current content strategy."""
        engagement_history = state.get('engagement_history', [])
        
        performance = {
            "headlines": "unknown",
            "motivations": "unknown",
            "overall_strategy": "unknown"
        }
        
        if engagement_history:
            # Analyze based on engagement history patterns
            recent_entries = engagement_history[-3:]
            
            engagement_scores = []
            for entry in recent_entries:
                if 'engagement_score' in entry:
                    engagement_scores.append(entry['engagement_score'])
            
            if engagement_scores:
                avg_score = statistics.mean(engagement_scores)
                if avg_score >= 0.7:
                    performance["overall_strategy"] = "effective"
                elif avg_score >= 0.4:
                    performance["overall_strategy"] = "moderate"
                else:
                    performance["overall_strategy"] = "needs_improvement"
        
        return performance
    
    def _identify_retention_opportunities(self, state: EngagementState) -> List[str]:
        """Identify specific opportunities to improve retention."""
        opportunities = []
        
        abandonment_risk = state.get('abandonment_risk', 0.5)
        engagement_metrics = state.get('engagement_metrics', {})
        
        # High-risk specific opportunities
        if abandonment_risk > 0.6:
            opportunities.extend([
                "Implement progress indicators",
                "Add motivational milestone celebration",
                "Reduce perceived form length"
            ])
        
        # Engagement metrics-based opportunities
        if engagement_metrics.get('time_on_step', 0) > 60:  # More than 1 minute
            opportunities.append("Simplify current step complexity")
        
        if engagement_metrics.get('hesitation_indicators', 0) > 2:
            opportunities.append("Address user concerns proactively")
        
        # Always include basic opportunities
        opportunities.extend([
            "Personalize content based on responses",
            "Optimize emotional resonance"
        ])
        
        return list(set(opportunities))  # Remove duplicates
    
    def _assess_psychological_factors(self, state: EngagementState) -> Dict[str, str]:
        """Assess psychological factors affecting engagement."""
        engagement_metrics = state.get('engagement_metrics', {})
        abandonment_risk = state.get('abandonment_risk', 0.5)
        
        factors = {
            "cognitive_load": "medium",  # Default
            "emotional_state": "neutral",
            "motivation_level": "moderate",
            "trust_level": "building"
        }
        
        # Assess cognitive load
        if engagement_metrics.get('time_on_step', 0) > 90:
            factors["cognitive_load"] = "high"
        elif engagement_metrics.get('time_on_step', 0) < 20:
            factors["cognitive_load"] = "low"
        
        # Assess emotional state based on abandonment risk
        if abandonment_risk > 0.7:
            factors["emotional_state"] = "frustrated"
        elif abandonment_risk < 0.3:
            factors["emotional_state"] = "positive"
        
        # Assess motivation level
        if engagement_metrics.get('engagement_score', 0.5) > 0.7:
            factors["motivation_level"] = "high"
        elif engagement_metrics.get('engagement_score', 0.5) < 0.3:
            factors["motivation_level"] = "low"
        
        return factors
    
    def _make_fallback_engagement_decision(self, state: EngagementState, engagement_analysis: Dict[str, Any]) -> SupervisorDecision:
        """Make rule-based fallback engagement decision when LLM fails."""
        risk_level = engagement_analysis['current_risk_level']
        
        # Rule-based strategy selection
        if risk_level == "high":
            strategy = "RECOVERY"
            headline = "You're almost there! 🎯"
            motivation = "Just a few more questions and you'll be all set!"
            reasoning = "High abandonment risk - implement recovery strategy"
        elif risk_level == "medium":
            strategy = "REASSURANCE"
            headline = "You're doing great! ⭐"
            motivation = "Thanks for taking the time to share these important details."
            reasoning = "Medium risk - provide reassurance and encouragement"
        else:
            strategy = "MOMENTUM_BUILDING"
            headline = "Let's keep this momentum going! 🚀"
            motivation = "Your answers are helping us create the perfect experience for you."
            reasoning = "Low risk - build momentum for completion"
        
        return self.create_decision(
            decision=strategy,
            reasoning=f"Fallback strategy: {reasoning}",
            confidence=0.6,
            recommendations=["Monitor engagement closely"],
            metadata={
                "headline": headline,
                "motivation": motivation,
                "abandonment_risk": state.get('abandonment_risk', 0.5),
                "fallback": True
            }
        )
    
    def _initialize_risk_factors(self) -> Dict[str, float]:
        """Initialize abandonment risk factor weights."""
        return {
            "time_on_step": 0.25,
            "hesitation_indicators": 0.20,
            "progress_perception": 0.20,
            "question_difficulty": 0.15,
            "emotional_state": 0.20
        }
    
    def _initialize_engagement_indicators(self) -> Dict[str, float]:
        """Initialize engagement indicator weights."""
        return {
            "response_enthusiasm": 0.30,
            "response_length": 0.20,
            "interaction_speed": 0.20,
            "progress_momentum": 0.30
        }
    
    def _initialize_retention_strategies(self) -> Dict[str, Dict[str, Any]]:
        """Initialize retention strategies library."""
        return {
            "progress_celebration": {
                "triggers": ["milestone_reached", "good_engagement"],
                "effectiveness": 0.8
            },
            "urgency_without_pressure": {
                "triggers": ["medium_risk", "slow_progress"],
                "effectiveness": 0.7
            },
            "personalization_boost": {
                "triggers": ["declining_engagement", "generic_responses"],
                "effectiveness": 0.75
            },
            "reassurance_building": {
                "triggers": ["high_risk", "hesitation_detected"],
                "effectiveness": 0.85
            }
        }
    
    def _update_internal_state(self, decision: SupervisorDecision, state: EngagementState):
        """Update internal engagement learning and tracking."""
        try:
            # Track content effectiveness
            self._track_content_effectiveness(decision, state)
            
            # Update user behavior patterns
            self._update_behavior_patterns(decision, state)
            
            # Record abandonment prediction
            self._record_abandonment_prediction(decision, state)
            
            # Update engagement history
            engagement_entry = {
                "timestamp": decision.timestamp,
                "strategy": decision.decision,
                "abandonment_risk": decision.metadata.get('abandonment_risk', 0.5),
                "confidence": decision.confidence,
                "content": {
                    "headline": decision.metadata.get('headline', ''),
                    "motivation": decision.metadata.get('motivation', '')
                }
            }
            
            self.internal_state["engagement_history"].append(engagement_entry)
            
            # Limit history size
            if len(self.internal_state["engagement_history"]) > 100:
                self.internal_state["engagement_history"] = self.internal_state["engagement_history"][-100:]
            
            logger.debug(f"Updated internal state for engagement strategy: {decision.decision}")
            
        except Exception as e:
            logger.error(f"Failed to update internal state: {e}")
    
    def _track_content_effectiveness(self, decision: SupervisorDecision, state: EngagementState):
        """Track effectiveness of content strategies."""
        strategy = decision.decision
        headline = decision.metadata.get('headline', '')
        motivation = decision.metadata.get('motivation', '')
        
        content_effectiveness = self.internal_state["content_effectiveness"]
        
        # Track strategy effectiveness
        if strategy not in content_effectiveness["strategies"]:
            content_effectiveness["strategies"][strategy] = {
                "uses": 0,
                "success_rate": 0.5,
                "avg_confidence": 0.5
            }
        
        strategy_data = content_effectiveness["strategies"][strategy]
        strategy_data["uses"] += 1
        
        # Update average confidence
        strategy_data["avg_confidence"] = (
            (strategy_data["avg_confidence"] * (strategy_data["uses"] - 1) + decision.confidence)
            / strategy_data["uses"]
        )
        
        # Track headline patterns (simplified)
        headline_key = self._extract_content_pattern(headline)
        if headline_key:
            if headline_key not in content_effectiveness["headlines"]:
                content_effectiveness["headlines"][headline_key] = {"uses": 0, "avg_confidence": 0.5}
            
            headline_data = content_effectiveness["headlines"][headline_key]
            headline_data["uses"] += 1
            headline_data["avg_confidence"] = (
                (headline_data["avg_confidence"] * (headline_data["uses"] - 1) + decision.confidence)
                / headline_data["uses"]
            )
    
    def _extract_content_pattern(self, content: str) -> Optional[str]:
        """Extract pattern from content for tracking."""
        if not content:
            return None
        
        content_lower = content.lower()
        
        # Identify key patterns
        if any(word in content_lower for word in ['almost', 'close', 'nearly']):
            return "completion_proximity"
        elif any(word in content_lower for word in ['great', 'excellent', 'amazing']):
            return "positive_reinforcement"
        elif any(word in content_lower for word in ['continue', 'keep', 'moving']):
            return "momentum_building"
        elif any(word in content_lower for word in ['help', 'support', 'together']):
            return "collaborative_tone"
        else:
            return "generic"
    
    def _update_behavior_patterns(self, decision: SupervisorDecision, state: EngagementState):
        """Update recognized user behavior patterns."""
        # Create behavior signature
        behavior_signature = self._create_behavior_signature(state)
        
        if behavior_signature not in self.internal_state["user_behavior_patterns"]:
            self.internal_state["user_behavior_patterns"][behavior_signature] = {
                "count": 0,
                "strategies_used": [],
                "avg_success_rate": 0.5
            }
        
        pattern_data = self.internal_state["user_behavior_patterns"][behavior_signature]
        pattern_data["count"] += 1
        pattern_data["strategies_used"].append(decision.decision)
        
        # Keep only recent strategies
        if len(pattern_data["strategies_used"]) > 10:
            pattern_data["strategies_used"] = pattern_data["strategies_used"][-10:]
    
    def _create_behavior_signature(self, state: EngagementState) -> str:
        """Create a signature for behavior pattern recognition."""
        abandonment_risk = state.get('abandonment_risk', 0.5)
        engagement_metrics = state.get('engagement_metrics', {})
        
        # Create simple behavior signature
        risk_bucket = "high" if abandonment_risk > 0.6 else "medium" if abandonment_risk > 0.3 else "low"
        time_bucket = "fast" if engagement_metrics.get('avg_time_per_step', 30) < 20 else "slow" if engagement_metrics.get('avg_time_per_step', 30) > 60 else "normal"
        
        return f"risk:{risk_bucket}|time:{time_bucket}"
    
    def _record_abandonment_prediction(self, decision: SupervisorDecision, state: EngagementState):
        """Record abandonment risk prediction for learning."""
        prediction = {
            "timestamp": decision.timestamp,
            "predicted_risk": decision.metadata.get('abandonment_risk', 0.5),
            "strategy_applied": decision.decision,
            "confidence": decision.confidence,
            "actual_outcome": None  # Would be updated later with actual outcome
        }
        
        self.internal_state["abandonment_predictions"].append(prediction)
        
        # Keep last 200 predictions
        if len(self.internal_state["abandonment_predictions"]) > 200:
            self.internal_state["abandonment_predictions"] = self.internal_state["abandonment_predictions"][-200:]
    
    def get_state_summary(self) -> Dict[str, Any]:
        """Get summary of internal state for coordination."""
        recent_decisions = self.decision_history[-5:] if self.decision_history else []
        
        return {
            "recent_strategies": [d.decision for d in recent_decisions],
            "average_engagement_confidence": self._calculate_average_engagement_confidence(),
            "content_effectiveness_trend": self._calculate_content_effectiveness_trend(),
            "top_behavior_patterns": self._get_top_behavior_patterns(),
            "abandonment_alerts": self._get_abandonment_alerts(),
            "retention_recommendations": self._get_retention_recommendations()
        }
    
    def _calculate_average_engagement_confidence(self) -> float:
        """Calculate average confidence in recent engagement decisions."""
        recent_decisions = self.decision_history[-10:] if self.decision_history else []
        if not recent_decisions:
            return 0.5
        
        confidences = [d.confidence for d in recent_decisions]
        return statistics.mean(confidences)
    
    def _calculate_content_effectiveness_trend(self) -> str:
        """Calculate trend in content effectiveness."""
        engagement_history = self.internal_state["engagement_history"]
        if len(engagement_history) < 3:
            return "insufficient_data"
        
        recent_confidences = [entry['confidence'] for entry in engagement_history[-3:]]
        if recent_confidences[-1] > recent_confidences[0]:
            return "improving"
        elif recent_confidences[-1] < recent_confidences[0]:
            return "declining"
        else:
            return "stable"
    
    def _get_top_behavior_patterns(self) -> List[Dict[str, Any]]:
        """Get top recognized behavior patterns."""
        patterns = self.internal_state["user_behavior_patterns"]
        
        # Sort by count and return top 3
        sorted_patterns = sorted(patterns.items(), key=lambda x: x[1]["count"], reverse=True)[:3]
        
        return [
            {
                "pattern": pattern_key,
                "count": data["count"],
                "common_strategies": list(set(data["strategies_used"]))[-3:]  # Last 3 unique strategies
            }
            for pattern_key, data in sorted_patterns
        ]
    
    def _get_abandonment_alerts(self) -> List[str]:
        """Get current abandonment risk alerts."""
        alerts = []
        
        # Check recent predictions
        recent_predictions = self.internal_state["abandonment_predictions"][-5:]
        if recent_predictions:
            avg_risk = statistics.mean([p['predicted_risk'] for p in recent_predictions])
            if avg_risk > 0.7:
                alerts.append("High abandonment risk trend detected")
        
        # Check content effectiveness
        effectiveness_trend = self._calculate_content_effectiveness_trend()
        if effectiveness_trend == "declining":
            alerts.append("Content effectiveness declining")
        
        return alerts
    
    def _get_retention_recommendations(self) -> List[str]:
        """Get strategic retention recommendations."""
        recommendations = []
        
        # Based on recent patterns
        recent_strategies = [d.decision for d in self.decision_history[-3:]] if self.decision_history else []
        if len(set(recent_strategies)) == 1 and recent_strategies:
            recommendations.append(f"Consider varying from {recent_strategies[0]} strategy")
        
        # Based on content effectiveness
        content_effectiveness = self.internal_state["content_effectiveness"]["strategies"]
        if content_effectiveness:
            best_strategy = max(content_effectiveness.items(), key=lambda x: x[1]["avg_confidence"])
            recommendations.append(f"Consider using {best_strategy[0]} strategy more frequently")
        
        # Always include basic recommendation
        recommendations.append("Monitor user behavior signals closely")
        
        return recommendations