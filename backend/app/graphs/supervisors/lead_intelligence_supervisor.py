"""Lead Intelligence Supervisor - Advanced lead scoring and qualification analysis."""

from __future__ import annotations
from typing import Dict, Any, List, Optional, Tuple
import json
import logging
import statistics
from datetime import datetime

from .base_supervisor import SupervisorAgent, SupervisorDecision
from ...state import LeadIntelligenceState

logger = logging.getLogger(__name__)


class LeadIntelligenceSupervisor(SupervisorAgent):
    """Supervisor for advanced lead scoring, qualification, and intelligence analysis."""
    
    def __init__(self, **kwargs):
        super().__init__(name="LeadIntelligenceSupervisor", **kwargs)
        # Internal state for lead intelligence
        self.internal_state = {
            "scoring_model": {
                "weights": self._initialize_scoring_weights(),
                "thresholds": {"yes": 80, "maybe": 40, "no": 25},
                "calibration_history": []
            },
            "lead_patterns": {},
            "qualification_cache": {},
            "performance_metrics": {
                "accuracy_history": [],
                "prediction_confidence": []
            },
            "historical_comparisons": []
        }
        
    def get_system_prompt(self) -> str:
        """System prompt for lead intelligence supervisor."""
        return """You are the Lead Intelligence Supervisor for an advanced lead qualification system.

Your responsibilities:
1. Analyze lead quality using conversation context and response patterns
2. Calculate dynamic lead scores based on multiple factors
3. Provide detailed qualification reasoning and confidence assessments
4. Identify risk factors and positive indicators
5. Make real-time classification decisions (yes/maybe/no)
6. Learn from historical data to improve accuracy

Analysis factors:
- Response quality and depth
- Business need indicators
- Engagement level and authenticity
- Fit with service requirements
- Historical patterns from similar leads

Provide nuanced assessments with:
- Detailed reasoning for scores
- Confidence levels for predictions
- Specific risk factors and positive indicators
- Recommendations for lead handling

Focus on accurate qualification while minimizing false positives and negatives."""
    
    def make_decision(self, state: LeadIntelligenceState, context: Dict[str, Any] = None) -> SupervisorDecision:
        """Make intelligent lead scoring and qualification decision."""
        try:
            # Analyze current lead intelligence
            intelligence_analysis = self._analyze_lead_intelligence(state)
            
            # Get context from other supervisors if available
            shared_context = context or {}
            question_context = shared_context.get('question_strategy', {})
            engagement_context = shared_context.get('engagement', {})
            
            # Make comprehensive lead assessment
            decision = self._make_lead_assessment_decision(
                state, intelligence_analysis, question_context, engagement_context
            )
            
            # Update internal state and learning
            self._update_internal_state(decision, state)
            
            return decision
            
        except Exception as e:
            return self.handle_error(e, "lead intelligence decision")
    
    def _analyze_lead_intelligence(self, state: LeadIntelligenceState) -> Dict[str, Any]:
        """Analyze current lead intelligence state."""
        responses = state.get('responses', [])
        score_history = state.get('score_history', [])
        current_score = state.get('current_score', 0)
        
        analysis = {
            "response_analysis": self._analyze_responses(responses),
            "score_trend": self._analyze_score_trend(score_history),
            "qualification_signals": self._identify_qualification_signals(responses),
            "risk_assessment": self._assess_risk_factors(responses, state),
            "confidence_factors": self._calculate_confidence_factors(state)
        }
        
        return analysis
    
    def _make_lead_assessment_decision(self, 
                                     state: LeadIntelligenceState,
                                     intelligence_analysis: Dict[str, Any],
                                     question_context: Dict[str, Any],
                                     engagement_context: Dict[str, Any]) -> SupervisorDecision:
        """Make comprehensive lead assessment using LLM analysis."""
        
        # Prepare context for LLM
        context_summary = self._prepare_intelligence_context(
            state, intelligence_analysis, question_context, engagement_context
        )
        
        messages = [
            {
                "role": "user",
                "content": f"""Analyze the lead intelligence data and make a comprehensive qualification decision.

CONTEXT:
{context_summary}

QUALIFICATION LEVELS:
1. YES - High-quality lead, strong fit, likely to convert
2. MAYBE - Moderate potential, needs nurturing or more information
3. NO - Poor fit, unlikely to convert, or disqualified

Provide your assessment in JSON format:
{{
    "qualification": "YES|MAYBE|NO",
    "score": 75,
    "confidence": 0.85,
    "reasoning": "detailed analysis of lead quality",
    "positive_indicators": ["specific positive factors"],
    "risk_factors": ["specific risk factors or concerns"],
    "score_breakdown": {{
        "response_quality": 20,
        "business_fit": 25,
        "engagement": 15,
        "requirements_match": 15
    }},
    "next_steps": ["recommended actions for this lead"],
    "comparable_leads": "how this lead compares to similar profiles"
}}

Base your assessment on response quality, business fit, and engagement patterns."""
            }
        ]
        
        try:
            response = self.invoke_llm(messages)
            assessment_data = json.loads(response)
            
            return self.create_decision(
                decision=assessment_data.get("qualification", "MAYBE"),
                reasoning=assessment_data.get("reasoning", "Default assessment"),
                confidence=assessment_data.get("confidence", 0.7),
                recommendations=assessment_data.get("next_steps", []),
                metadata={
                    "score": assessment_data.get("score", 50),
                    "positive_indicators": assessment_data.get("positive_indicators", []),
                    "risk_factors": assessment_data.get("risk_factors", []),
                    "score_breakdown": assessment_data.get("score_breakdown", {}),
                    "comparable_leads": assessment_data.get("comparable_leads", ""),
                    "intelligence_analysis": intelligence_analysis
                }
            )
            
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"Failed to parse LLM assessment: {e}")
            return self._make_fallback_assessment(state, intelligence_analysis)
    
    def _prepare_intelligence_context(self, 
                                    state: LeadIntelligenceState,
                                    intelligence_analysis: Dict[str, Any],
                                    question_context: Dict[str, Any],
                                    engagement_context: Dict[str, Any]) -> str:
        """Prepare comprehensive context for intelligence analysis."""
        
        context_parts = [
            "=== LEAD INTELLIGENCE STATE ===",
            f"Current Score: {state.get('current_score', 0)}",
            f"Current Status: {state.get('lead_status', 'unknown')}",
            f"Total Responses: {len(state.get('responses', []))}",
            "",
            "=== RESPONSE ANALYSIS ==="
        ]
        
        response_analysis = intelligence_analysis['response_analysis']
        context_parts.extend([
            f"Response Quality Score: {response_analysis.get('quality_score', 0):.2f}",
            f"Average Response Length: {response_analysis.get('avg_length', 0)}",
            f"Engagement Indicators: {len(response_analysis.get('engagement_indicators', []))}",
            f"Business Need Signals: {len(response_analysis.get('business_signals', []))}"
        ])
        
        # Add recent responses context
        responses = state.get('responses', [])
        if responses:
            context_parts.extend([
                "",
                "=== RECENT RESPONSES ==="
            ])
            for i, response in enumerate(responses[-3:], 1):
                answer = response.get('answer', 'No answer')[:150]
                context_parts.append(f"{i}. Q: {response.get('question_text', 'Unknown')[:50]}...")
                context_parts.append(f"   A: {answer}..." if len(response.get('answer', '')) > 150 else f"   A: {answer}")
        
        context_parts.extend([
            "",
            "=== QUALIFICATION SIGNALS ==="
        ])
        
        qual_signals = intelligence_analysis['qualification_signals']
        for signal_type, signals in qual_signals.items():
            if signals:
                context_parts.append(f"{signal_type.upper()}: {', '.join(signals)}")
        
        context_parts.extend([
            "",
            "=== RISK ASSESSMENT ==="
        ])
        
        risk_assessment = intelligence_analysis['risk_assessment']
        for risk_type, risks in risk_assessment.items():
            if risks:
                context_parts.append(f"{risk_type.upper()}: {', '.join(risks)}")
        
        # Add context from other supervisors
        if question_context:
            context_parts.extend([
                "",
                "=== QUESTIONING CONTEXT ===",
                f"Current Strategy: {question_context.get('current_strategy', 'unknown')}",
                f"Performance Trend: {question_context.get('performance_trend', 'unknown')}"
            ])
        
        if engagement_context:
            context_parts.extend([
                "",
                "=== ENGAGEMENT CONTEXT ===",
                f"Abandonment Risk: {engagement_context.get('abandonment_risk', 'unknown')}",
                f"Engagement Level: {engagement_context.get('engagement_level', 'unknown')}"
            ])
        
        return "\n".join(context_parts)
    
    def _analyze_responses(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze response patterns and quality."""
        if not responses:
            return {
                "quality_score": 0.0,
                "avg_length": 0,
                "engagement_indicators": [],
                "business_signals": []
            }
        
        # Calculate response metrics
        response_lengths = [len(r.get('answer', '')) for r in responses]
        avg_length = statistics.mean(response_lengths) if response_lengths else 0
        
        quality_score = self._calculate_response_quality_score(responses)
        engagement_indicators = self._identify_engagement_indicators(responses)
        business_signals = self._identify_business_signals(responses)
        
        return {
            "quality_score": quality_score,
            "avg_length": avg_length,
            "engagement_indicators": engagement_indicators,
            "business_signals": business_signals,
            "response_count": len(responses)
        }
    
    def _calculate_response_quality_score(self, responses: List[Dict[str, Any]]) -> float:
        """Calculate overall response quality score."""
        if not responses:
            return 0.0
        
        quality_factors = []
        
        for response in responses:
            answer = response.get('answer', '')
            
            # Length factor (not too short, not too long)
            length_score = min(len(answer) / 50, 1.0) * 0.3
            
            # Specificity factor (contains specific details)
            specificity_score = self._calculate_specificity(answer) * 0.4
            
            # Relevance factor (answers the question appropriately)
            relevance_score = self._calculate_relevance(answer, response.get('question_text', '')) * 0.3
            
            quality_factors.append(length_score + specificity_score + relevance_score)
        
        return statistics.mean(quality_factors) if quality_factors else 0.0
    
    def _calculate_specificity(self, answer: str) -> float:
        """Calculate specificity score of an answer."""
        if not answer:
            return 0.0
        
        answer_lower = answer.lower()
        
        # Check for specific indicators
        specific_indicators = [
            # Numbers and quantities
            any(char.isdigit() for char in answer),
            # Specific locations
            any(word in answer_lower for word in ['street', 'avenue', 'road', 'city', 'town']),
            # Specific times/frequencies  
            any(word in answer_lower for word in ['daily', 'weekly', 'monthly', 'morning', 'evening']),
            # Specific details
            any(word in answer_lower for word in ['because', 'since', 'due to', 'specifically'])
        ]
        
        return sum(specific_indicators) / len(specific_indicators)
    
    def _calculate_relevance(self, answer: str, question: str) -> float:
        """Calculate relevance of answer to question."""
        if not answer or not question:
            return 0.5  # Default neutral relevance
        
        # Simple keyword matching for relevance
        answer_words = set(answer.lower().split())
        question_words = set(question.lower().split())
        
        # Remove common words
        common_words = {'the', 'is', 'are', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with'}
        answer_words -= common_words
        question_words -= common_words
        
        if not question_words:
            return 0.5
        
        # Calculate overlap
        overlap = len(answer_words & question_words)
        relevance = min(overlap / len(question_words), 1.0)
        
        return relevance
    
    def _identify_engagement_indicators(self, responses: List[Dict[str, Any]]) -> List[str]:
        """Identify indicators of strong engagement."""
        indicators = []
        
        for response in responses:
            answer = response.get('answer', '').lower()
            
            if len(answer) > 100:
                indicators.append("detailed_responses")
            
            if any(word in answer for word in ['excited', 'interested', 'looking forward', 'definitely']):
                indicators.append("enthusiasm_expressions")
            
            if any(word in answer for word in ['question', 'wondering', 'curious', 'tell me']):
                indicators.append("active_inquiry")
                
            if answer.count('!') > 1:
                indicators.append("high_enthusiasm_punctuation")
        
        return list(set(indicators))  # Remove duplicates
    
    def _identify_business_signals(self, responses: List[Dict[str, Any]]) -> List[str]:
        """Identify business need and qualification signals."""
        signals = []
        
        for response in responses:
            answer = response.get('answer', '').lower()
            
            if any(word in answer for word in ['need', 'require', 'looking for', 'want']):
                signals.append("explicit_need")
            
            if any(word in answer for word in ['budget', 'afford', 'cost', 'price', 'expensive']):
                signals.append("budget_awareness")
            
            if any(word in answer for word in ['soon', 'immediately', 'urgent', 'asap']):
                signals.append("urgency_indicators")
                
            if any(word in answer for word in ['experience', 'before', 'previously', 'used to']):
                signals.append("prior_experience")
        
        return list(set(signals))
    
    def _analyze_score_trend(self, score_history: List[Dict[str, Any]]) -> str:
        """Analyze the trend in lead scoring."""
        if len(score_history) < 2:
            return "insufficient_data"
        
        recent_scores = [s.get('score', 0) for s in score_history[-3:]]
        
        if len(recent_scores) < 2:
            return "insufficient_data"
        
        if recent_scores[-1] > recent_scores[0] + 5:
            return "improving"
        elif recent_scores[-1] < recent_scores[0] - 5:
            return "declining"
        else:
            return "stable"
    
    def _identify_qualification_signals(self, responses: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Identify various qualification signals from responses."""
        signals = {
            "positive": [],
            "negative": [],
            "neutral": []
        }
        
        for response in responses:
            answer = response.get('answer', '').lower()
            
            # Positive signals
            if any(word in answer for word in ['yes', 'definitely', 'absolutely', 'perfect']):
                signals["positive"].append("strong_affirmation")
            
            if any(phrase in answer for phrase in ['very interested', 'sounds great', 'exactly what']):
                signals["positive"].append("high_interest")
            
            # Negative signals
            if any(word in answer for word in ['no', 'not', 'never', 'can\'t', 'won\'t']):
                signals["negative"].append("resistance_language")
            
            if any(phrase in answer for phrase in ['too expensive', 'can\'t afford', 'out of budget']):
                signals["negative"].append("budget_concerns")
            
            # Neutral signals
            if any(word in answer for word in ['maybe', 'perhaps', 'might', 'possibly']):
                signals["neutral"].append("uncertainty")
        
        return signals
    
    def _assess_risk_factors(self, responses: List[Dict[str, Any]], state: LeadIntelligenceState) -> Dict[str, List[str]]:
        """Assess various risk factors for lead qualification."""
        risks = {
            "engagement": [],
            "qualification": [],
            "conversion": []
        }
        
        # Engagement risks
        response_lengths = [len(r.get('answer', '')) for r in responses]
        if response_lengths and statistics.mean(response_lengths) < 20:
            risks["engagement"].append("short_responses")
        
        # Qualification risks
        risk_factors = state.get('risk_factors', [])
        for risk in risk_factors:
            if 'budget' in risk.lower():
                risks["qualification"].append("budget_constraints")
            elif 'location' in risk.lower():
                risks["qualification"].append("location_mismatch")
        
        # Conversion risks
        current_score = state.get('current_score', 0)
        if current_score < 40:
            risks["conversion"].append("low_qualification_score")
        
        return risks
    
    def _calculate_confidence_factors(self, state: LeadIntelligenceState) -> Dict[str, float]:
        """Calculate factors that affect confidence in assessment."""
        responses = state.get('responses', [])
        score_history = state.get('score_history', [])
        
        factors = {
            "data_sufficiency": min(len(responses) / 4.0, 1.0),  # More responses = higher confidence
            "score_stability": self._calculate_score_stability(score_history),
            "response_quality": self._analyze_responses(responses).get('quality_score', 0.0),
            "pattern_recognition": self._calculate_pattern_confidence(state)
        }
        
        return factors
    
    def _calculate_score_stability(self, score_history: List[Dict[str, Any]]) -> float:
        """Calculate stability of score over time."""
        if len(score_history) < 2:
            return 0.5  # Neutral stability with insufficient data
        
        scores = [s.get('score', 0) for s in score_history]
        if len(scores) < 2:
            return 0.5
        
        # Calculate coefficient of variation (lower = more stable)
        mean_score = statistics.mean(scores)
        if mean_score == 0:
            return 0.5
        
        std_dev = statistics.stdev(scores) if len(scores) > 1 else 0
        cv = std_dev / mean_score
        
        # Convert to stability score (lower CV = higher stability)
        stability = max(0, 1 - cv)
        return min(stability, 1.0)
    
    def _calculate_pattern_confidence(self, state: LeadIntelligenceState) -> float:
        """Calculate confidence based on pattern recognition."""
        # This would integrate with historical data in a real system
        # For now, use simple heuristics
        
        responses = state.get('responses', [])
        positive_indicators = state.get('positive_indicators', [])
        risk_factors = state.get('risk_factors', [])
        
        # Pattern strength based on clear indicators
        pattern_strength = 0.5  # Default neutral
        
        if len(positive_indicators) > len(risk_factors):
            pattern_strength += 0.2
        elif len(risk_factors) > len(positive_indicators):
            pattern_strength -= 0.2
        
        if len(responses) >= 4:  # Sufficient data for pattern recognition
            pattern_strength += 0.1
        
        return max(0.0, min(1.0, pattern_strength))
    
    def _make_fallback_assessment(self, state: LeadIntelligenceState, intelligence_analysis: Dict[str, Any]) -> SupervisorDecision:
        """Make rule-based fallback assessment when LLM fails."""
        current_score = state.get('current_score', 0)
        responses = state.get('responses', [])
        risk_factors = state.get('risk_factors', [])
        
        # Simple rule-based qualification
        if current_score >= 70 and len(responses) >= 3:
            qualification = "YES"
            reasoning = "High score with sufficient responses"
        elif current_score >= 40 and len(responses) >= 4:
            qualification = "MAYBE"
            reasoning = "Moderate score with good engagement"
        elif len(risk_factors) > 2:
            qualification = "NO"
            reasoning = "Multiple risk factors identified"
        else:
            qualification = "MAYBE"
            reasoning = "Insufficient data for clear qualification"
        
        return self.create_decision(
            decision=qualification,
            reasoning=f"Fallback assessment: {reasoning}",
            confidence=0.6,
            recommendations=["Gather more data for better assessment"],
            metadata={
                "score": current_score,
                "fallback": True,
                "intelligence_analysis": intelligence_analysis
            }
        )
    
    def _update_internal_state(self, decision: SupervisorDecision, state: LeadIntelligenceState):
        """Update internal learning and performance tracking."""
        try:
            # Update scoring model calibration
            self._update_scoring_calibration(decision, state)
            
            # Track performance metrics
            self._track_performance_metrics(decision, state)
            
            # Update lead patterns
            self._update_lead_patterns(decision, state)
            
            # Cache qualification decision
            session_key = f"{datetime.now().isoformat()}_{decision.decision}"
            self.internal_state["qualification_cache"][session_key] = {
                "decision": decision.to_dict(),
                "state_snapshot": {
                    "score": state.get('current_score', 0),
                    "responses_count": len(state.get('responses', []))
                }
            }
            
            # Limit cache size
            cache = self.internal_state["qualification_cache"]
            if len(cache) > 100:
                # Keep most recent 50
                recent_keys = sorted(cache.keys())[-50:]
                self.internal_state["qualification_cache"] = {k: cache[k] for k in recent_keys}
            
            logger.debug(f"Updated internal state for qualification: {decision.decision}")
            
        except Exception as e:
            logger.error(f"Failed to update internal state: {e}")
    
    def _initialize_scoring_weights(self) -> Dict[str, float]:
        """Initialize scoring model weights."""
        return {
            "response_quality": 0.25,
            "business_fit": 0.30,
            "engagement": 0.20,
            "requirements_match": 0.25
        }
    
    def _update_scoring_calibration(self, decision: SupervisorDecision, state: LeadIntelligenceState):
        """Update scoring model based on decision outcomes."""
        # In a real system, this would use actual conversion outcomes
        # For now, track decision confidence vs actual scores
        
        calibration_point = {
            "timestamp": decision.timestamp,
            "predicted_score": decision.metadata.get('score', 0),
            "confidence": decision.confidence,
            "qualification": decision.decision,
            "actual_response_quality": self._analyze_responses(state.get('responses', [])).get('quality_score', 0)
        }
        
        self.internal_state["scoring_model"]["calibration_history"].append(calibration_point)
        
        # Keep last 200 calibration points
        if len(self.internal_state["scoring_model"]["calibration_history"]) > 200:
            self.internal_state["scoring_model"]["calibration_history"] = \
                self.internal_state["scoring_model"]["calibration_history"][-200:]
    
    def _track_performance_metrics(self, decision: SupervisorDecision, state: LeadIntelligenceState):
        """Track performance metrics for continuous improvement."""
        metrics = self.internal_state["performance_metrics"]
        
        # Track prediction confidence
        metrics["prediction_confidence"].append({
            "timestamp": decision.timestamp,
            "confidence": decision.confidence,
            "qualification": decision.decision
        })
        
        # Keep last 100 predictions
        if len(metrics["prediction_confidence"]) > 100:
            metrics["prediction_confidence"] = metrics["prediction_confidence"][-100:]
    
    def _update_lead_patterns(self, decision: SupervisorDecision, state: LeadIntelligenceState):
        """Update recognized lead patterns."""
        # Extract pattern signature from lead
        pattern_key = self._create_pattern_signature(state)
        
        if pattern_key not in self.internal_state["lead_patterns"]:
            self.internal_state["lead_patterns"][pattern_key] = {
                "count": 0,
                "qualifications": [],
                "avg_score": 0.0
            }
        
        pattern_data = self.internal_state["lead_patterns"][pattern_key]
        pattern_data["count"] += 1
        pattern_data["qualifications"].append(decision.decision)
        
        # Update average score
        current_score = state.get('current_score', 0)
        pattern_data["avg_score"] = (
            (pattern_data["avg_score"] * (pattern_data["count"] - 1) + current_score) 
            / pattern_data["count"]
        )
    
    def _create_pattern_signature(self, state: LeadIntelligenceState) -> str:
        """Create a signature for pattern recognition."""
        responses = state.get('responses', [])
        response_count = len(responses)
        avg_length = statistics.mean([len(r.get('answer', '')) for r in responses]) if responses else 0
        
        # Create simple pattern signature
        signature_parts = [
            f"responses:{response_count//2 * 2}",  # Bucket by 2s
            f"length:{int(avg_length//20) * 20}"    # Bucket by 20s
        ]
        
        return "|".join(signature_parts)
    
    def get_state_summary(self) -> Dict[str, Any]:
        """Get summary of internal state for coordination."""
        recent_decisions = self.decision_history[-5:] if self.decision_history else []
        
        return {
            "recent_qualifications": [d.decision for d in recent_decisions],
            "average_confidence": self._calculate_average_confidence(),
            "scoring_accuracy_trend": self._calculate_accuracy_trend(),
            "top_patterns": self._get_top_patterns(),
            "risk_alerts": self._get_current_risk_alerts()
        }
    
    def _calculate_average_confidence(self) -> float:
        """Calculate average confidence of recent decisions."""
        recent_decisions = self.decision_history[-10:] if self.decision_history else []
        if not recent_decisions:
            return 0.5
        
        confidences = [d.confidence for d in recent_decisions]
        return statistics.mean(confidences)
    
    def _calculate_accuracy_trend(self) -> str:
        """Calculate trend in scoring accuracy."""
        # Simplified accuracy calculation based on confidence trends
        recent_decisions = self.decision_history[-5:] if self.decision_history else []
        if len(recent_decisions) < 3:
            return "insufficient_data"
        
        recent_confidences = [d.confidence for d in recent_decisions]
        if recent_confidences[-1] > recent_confidences[0]:
            return "improving"
        elif recent_confidences[-1] < recent_confidences[0]:
            return "declining"
        else:
            return "stable"
    
    def _get_top_patterns(self) -> List[Dict[str, Any]]:
        """Get top recognized lead patterns."""
        patterns = self.internal_state["lead_patterns"]
        
        # Sort by count and return top 3
        sorted_patterns = sorted(patterns.items(), key=lambda x: x[1]["count"], reverse=True)[:3]
        
        return [
            {
                "pattern": pattern_key,
                "count": data["count"],
                "avg_score": round(data["avg_score"], 2)
            }
            for pattern_key, data in sorted_patterns
        ]
    
    def _get_current_risk_alerts(self) -> List[str]:
        """Get current risk alerts based on internal state."""
        alerts = []
        
        # Check confidence trend
        avg_confidence = self._calculate_average_confidence()
        if avg_confidence < 0.6:
            alerts.append("Low confidence in recent assessments")
        
        # Check scoring stability
        accuracy_trend = self._calculate_accuracy_trend()
        if accuracy_trend == "declining":
            alerts.append("Declining assessment accuracy trend")
        
        return alerts