"""Master Flow Supervisor - Main orchestrator for intelligent survey flow management."""

from __future__ import annotations
from typing import Dict, Any, List, Optional, Tuple
import json
import logging
from datetime import datetime

from .base_supervisor import SupervisorAgent, SupervisorDecision, SupervisorError
from ...state import SurveyState

logger = logging.getLogger(__name__)


class MasterFlowSupervisor(SupervisorAgent):
    """Master supervisor that orchestrates the entire survey flow and coordinates other supervisors."""
    
    def __init__(self, **kwargs):
        super().__init__(name="MasterFlowSupervisor", **kwargs)
        self.domain_supervisors: Dict[str, SupervisorAgent] = {}
        
    def register_domain_supervisor(self, supervisor: SupervisorAgent):
        """Register a domain-specific supervisor."""
        self.domain_supervisors[supervisor.name] = supervisor
        logger.info(f"Master supervisor registered domain supervisor: {supervisor.name}")
    
    def get_system_prompt(self) -> str:
        """System prompt for the master flow supervisor."""
        return """You are the Master Flow Supervisor for an intelligent lead generation survey system.

Your role is to:
1. Orchestrate the overall survey flow and progression
2. Coordinate between specialized domain supervisors
3. Make high-level decisions about flow continuation, completion, and adaptation
4. Handle supervisor conflicts and prioritize decisions
5. Ensure optimal lead qualification and user engagement

You have access to:
- Current survey state and user responses
- Decisions and recommendations from domain supervisors
- Business rules and completion criteria
- Historical performance data

Make decisions that balance:
- Lead qualification accuracy
- User engagement and completion rates
- Efficient resource utilization
- Business objectives

Always provide clear reasoning for your decisions and confidence scores."""
    
    def make_decision(self, state: SurveyState, context: Dict[str, Any] = None) -> SupervisorDecision:
        """Make high-level flow decision based on current state and domain supervisor input."""
        try:
            if not self.validate_state(state):
                return self.handle_error(
                    Exception("Invalid state provided"), 
                    "state validation"
                )
            
            # Gather context from domain supervisors
            supervisor_context = self._gather_supervisor_context(state)
            
            # Analyze current flow state
            flow_analysis = self._analyze_flow_state(state, supervisor_context)
            
            # Make strategic decision
            decision = self._make_strategic_decision(state, flow_analysis, supervisor_context)
            
            return decision
            
        except Exception as e:
            return self.handle_error(e, "master flow decision")
    
    def _gather_supervisor_context(self, state: SurveyState) -> Dict[str, Any]:
        """Gather input and recommendations from all domain supervisors."""
        context = {
            "supervisor_inputs": {},
            "recommendations": [],
            "conflicts": [],
            "consensus_areas": []
        }
        
        # Get recent decisions from each domain supervisor
        supervisor_decisions = state.get('supervisor_decisions', {})
        
        for supervisor_name, decisions in supervisor_decisions.items():
            if decisions:
                latest_decision = decisions[-1]  # Most recent decision
                context["supervisor_inputs"][supervisor_name] = latest_decision
                
                if latest_decision.get("recommendations"):
                    context["recommendations"].extend(latest_decision["recommendations"])
        
        # Identify conflicts and consensus
        context["conflicts"] = self._identify_conflicts(supervisor_decisions)
        context["consensus_areas"] = self._identify_consensus(supervisor_decisions)
        
        return context
    
    def _analyze_flow_state(self, state: SurveyState, supervisor_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the current state of the survey flow."""
        responses = state.get('responses', [])
        asked_questions = state.get('asked_questions', [])
        score = state.get('score', 0)
        lead_status = state.get('lead_status', 'unknown')
        step = state.get('step', 0)
        completion_probability = state.get('completion_probability', 0.5)
        
        analysis = {
            "progress_metrics": {
                "total_responses": len(responses),
                "questions_asked": len(asked_questions),
                "current_step": step,
                "completion_probability": completion_probability
            },
            "lead_assessment": {
                "current_score": score,
                "status": lead_status,
                "qualification_trend": self._analyze_qualification_trend(state)
            },
            "engagement_indicators": {
                "abandonment_risk": state.get('abandonment_risk', {}),
                "engagement_metrics": state.get('engagement_metrics', {})
            },
            "business_rules_status": self._check_business_rules(state)
        }
        
        return analysis
    
    def _make_strategic_decision(self, state: SurveyState, flow_analysis: Dict[str, Any], supervisor_context: Dict[str, Any]) -> SupervisorDecision:
        """Make the strategic flow decision using LLM analysis."""
        # Prepare context for LLM
        context_summary = self._prepare_llm_context(state, flow_analysis, supervisor_context)
        
        # Create LLM prompt
        messages = [
            {
                "role": "user",
                "content": f"""Analyze the current survey flow state and make a strategic decision.

CONTEXT:
{context_summary}

DECISION OPTIONS:
1. CONTINUE - Continue with current flow strategy
2. ADAPT - Modify flow strategy based on current state
3. COMPLETE - End survey and proceed to completion
4. RECOVER - Implement recovery strategy for issues

Provide your decision in JSON format:
{{
    "decision": "CONTINUE|ADAPT|COMPLETE|RECOVER",
    "reasoning": "detailed reasoning for the decision",
    "confidence": 0.85,
    "adaptations": ["list of specific adaptations if ADAPT chosen"],
    "priority_actions": ["high priority actions to take"],
    "risk_factors": ["identified risk factors"],
    "success_indicators": ["indicators that decision is working"]
}}"""
            }
        ]
        
        try:
            # Get LLM response
            response = self.invoke_llm(messages)
            
            # Parse JSON response
            decision_data = json.loads(response)
            
            # Create supervisor decision
            return self.create_decision(
                decision=decision_data.get("decision", "CONTINUE"),
                reasoning=decision_data.get("reasoning", "Default reasoning"),
                confidence=decision_data.get("confidence", 0.7),
                recommendations=(
                    decision_data.get("adaptations", []) + 
                    decision_data.get("priority_actions", [])
                ),
                metadata={
                    "risk_factors": decision_data.get("risk_factors", []),
                    "success_indicators": decision_data.get("success_indicators", []),
                    "flow_analysis": flow_analysis,
                    "supervisor_context": supervisor_context
                }
            )
            
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"Failed to parse LLM decision, using fallback: {e}")
            return self._make_fallback_decision(state, flow_analysis)
    
    def _prepare_llm_context(self, state: SurveyState, flow_analysis: Dict[str, Any], supervisor_context: Dict[str, Any]) -> str:
        """Prepare comprehensive context summary for LLM decision making."""
        context_parts = [
            "=== SURVEY PROGRESS ===",
            f"Step: {flow_analysis['progress_metrics']['current_step']}",
            f"Responses: {flow_analysis['progress_metrics']['total_responses']}",
            f"Questions Asked: {flow_analysis['progress_metrics']['questions_asked']}",
            f"Completion Probability: {flow_analysis['progress_metrics']['completion_probability']:.2f}",
            "",
            "=== LEAD ASSESSMENT ===",
            f"Current Score: {flow_analysis['lead_assessment']['current_score']}",
            f"Status: {flow_analysis['lead_assessment']['status']}",
            f"Trend: {flow_analysis['lead_assessment']['qualification_trend']}",
            "",
            "=== BUSINESS RULES ==="
        ]
        
        business_rules = flow_analysis['business_rules_status']
        for rule, status in business_rules.items():
            context_parts.append(f"{rule}: {status}")
        
        context_parts.extend([
            "",
            "=== SUPERVISOR RECOMMENDATIONS ==="
        ])
        
        for recommendation in supervisor_context.get('recommendations', []):
            context_parts.append(f"- {recommendation}")
        
        if supervisor_context.get('conflicts'):
            context_parts.extend([
                "",
                "=== SUPERVISOR CONFLICTS ==="
            ])
            for conflict in supervisor_context['conflicts']:
                context_parts.append(f"- {conflict}")
        
        # Add recent responses context
        responses = state.get('responses', [])
        if responses:
            context_parts.extend([
                "",
                "=== RECENT RESPONSES ==="
            ])
            for response in responses[-3:]:  # Last 3 responses
                answer = response.get('answer', 'No answer')[:100]
                context_parts.append(f"Q: {response.get('question_text', 'Unknown')}")
                context_parts.append(f"A: {answer}..." if len(response.get('answer', '')) > 100 else f"A: {answer}")
        
        return "\n".join(context_parts)
    
    def _analyze_qualification_trend(self, state: SurveyState) -> str:
        """Analyze the trend in lead qualification over time."""
        scoring_reasoning = state.get('scoring_reasoning', [])
        
        if len(scoring_reasoning) < 2:
            return "insufficient_data"
        
        # Get last few scores to determine trend
        recent_scores = []
        for reasoning in scoring_reasoning[-3:]:
            if 'score' in reasoning:
                recent_scores.append(reasoning['score'])
        
        if len(recent_scores) < 2:
            return "insufficient_data"
        
        if recent_scores[-1] > recent_scores[0]:
            return "improving"
        elif recent_scores[-1] < recent_scores[0]:
            return "declining"
        else:
            return "stable"
    
    def _check_business_rules(self, state: SurveyState) -> Dict[str, bool]:
        """Check status of key business rules."""
        responses = state.get('responses', [])
        asked_questions = state.get('asked_questions', [])
        
        return {
            "min_questions_met": len(responses) >= 4,
            "max_questions_limit": len(responses) < 10,
            "has_responses": len(responses) > 0,
            "failed_required": state.get('failed_required', False),
            "within_step_limit": state.get('step', 0) < 8,
            "completion_viable": state.get('completion_probability', 0) > 0.3
        }
    
    def _identify_conflicts(self, supervisor_decisions: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        """Identify conflicts between supervisor recommendations."""
        conflicts = []
        
        # Get latest decisions from each supervisor
        latest_decisions = {}
        for supervisor, decisions in supervisor_decisions.items():
            if decisions:
                latest_decisions[supervisor] = decisions[-1]
        
        # Check for conflicting recommendations
        all_recommendations = []
        for supervisor, decision in latest_decisions.items():
            recommendations = decision.get('recommendations', [])
            for rec in recommendations:
                all_recommendations.append((supervisor, rec))
        
        # Simple conflict detection (can be enhanced)
        conflicting_patterns = [
            ("continue", "complete"),
            ("ask_more", "finish_now"),
            ("engage", "disengage")
        ]
        
        for pattern1, pattern2 in conflicting_patterns:
            has_pattern1 = any(pattern1 in rec[1].lower() for rec in all_recommendations)
            has_pattern2 = any(pattern2 in rec[1].lower() for rec in all_recommendations)
            if has_pattern1 and has_pattern2:
                conflicts.append(f"Conflict detected: {pattern1} vs {pattern2}")
        
        return conflicts
    
    def _identify_consensus(self, supervisor_decisions: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        """Identify areas of consensus between supervisors."""
        consensus = []
        
        # Get latest decisions from each supervisor
        latest_decisions = {}
        for supervisor, decisions in supervisor_decisions.items():
            if decisions:
                latest_decisions[supervisor] = decisions[-1]
        
        if len(latest_decisions) < 2:
            return consensus
        
        # Check for common themes in recommendations
        all_recommendations = []
        for decision in latest_decisions.values():
            all_recommendations.extend(decision.get('recommendations', []))
        
        # Simple consensus detection
        common_themes = [
            "quality", "engagement", "completion", "scoring", "questions"
        ]
        
        for theme in common_themes:
            theme_count = sum(1 for rec in all_recommendations if theme in rec.lower())
            if theme_count >= len(latest_decisions) / 2:  # Majority consensus
                consensus.append(f"Consensus on {theme} strategy")
        
        return consensus
    
    def _make_fallback_decision(self, state: SurveyState, flow_analysis: Dict[str, Any]) -> SupervisorDecision:
        """Make a rule-based fallback decision when LLM fails."""
        business_rules = flow_analysis['business_rules_status']
        
        # Simple rule-based decision logic
        if not business_rules['has_responses']:
            decision = "CONTINUE"
            reasoning = "No responses yet, continue with current flow"
        elif business_rules['failed_required']:
            decision = "COMPLETE"
            reasoning = "Required questions failed, complete survey"
        elif not business_rules['min_questions_met']:
            decision = "CONTINUE"
            reasoning = "Minimum questions not met, continue collecting responses"
        elif not business_rules['completion_viable']:
            decision = "RECOVER"
            reasoning = "Low completion probability, implement recovery strategy"
        elif business_rules['max_questions_limit'] and business_rules['min_questions_met']:
            decision = "COMPLETE"
            reasoning = "Sufficient data collected, proceed to completion"
        else:
            decision = "CONTINUE"
            reasoning = "Standard flow continuation"
        
        return self.create_decision(
            decision=decision,
            reasoning=f"Fallback decision: {reasoning}",
            confidence=0.6,
            recommendations=["Monitor for LLM recovery"],
            metadata={"fallback": True, "flow_analysis": flow_analysis}
        )
    
    def coordinate_supervisors(self, state: SurveyState) -> Dict[str, Any]:
        """Coordinate between domain supervisors and resolve conflicts."""
        coordination_result = {
            "decisions": {},
            "conflicts_resolved": [],
            "consensus_achieved": [],
            "coordination_success": True
        }
        
        try:
            # Get decisions from all domain supervisors
            for supervisor_name, supervisor in self.domain_supervisors.items():
                try:
                    decision = supervisor.make_decision(state)
                    coordination_result["decisions"][supervisor_name] = decision.to_dict()
                except Exception as e:
                    logger.error(f"Error getting decision from {supervisor_name}: {e}")
                    coordination_result["coordination_success"] = False
            
            return coordination_result
            
        except Exception as e:
            logger.error(f"Supervisor coordination failed: {e}")
            coordination_result["coordination_success"] = False
            return coordination_result