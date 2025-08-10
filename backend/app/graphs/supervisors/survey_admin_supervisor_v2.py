"""Survey Administration Supervisor V2 - Intelligent survey orchestration with GPT-4o-mini."""

from __future__ import annotations
from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime

from .base_supervisor import SupervisorAgent, SupervisorDecision
from ...state import SurveyState

logger = logging.getLogger(__name__)


class SurveyAdministrationSupervisor(SupervisorAgent):
    """Supervisor for intelligent survey flow orchestration."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="SurveyAdministrationSupervisor",
            model_name="gpt-4o-mini",
            temperature=0.2,
            max_tokens=2000,
            timeout_seconds=45,
            **kwargs
        )
    
    def get_system_prompt(self) -> str:
        """System prompt for survey administration decisions."""
        return """You are the Survey Administration Supervisor for an intelligent lead generation system.

Your role is to make strategic decisions about survey flow, question selection, phrasing, and engagement.

CORE RESPONSIBILITIES:
1. Analyze user responses and engagement patterns
2. Decide survey continuation vs completion
3. Coordinate question selection strategy
4. Determine appropriate engagement tactics
5. Balance information gain with user experience

DECISION FACTORS:
- Response quality and depth
- User engagement signals (time spent, completion rate)
- Information gaps for lead qualification
- Survey fatigue and abandonment risk
- Business objectives and conversion goals

OUTPUT FORMAT:
Always respond with valid JSON containing:
{
  "action": "continue" | "complete",
  "reasoning": "detailed explanation",
  "confidence": 0.0-1.0,
  "strategy": {
    "question_count": 1-3,
    "question_types": ["qualification", "engagement", "demographic"],
    "engagement_approach": "motivational" | "casual" | "urgent",
    "phrasing_tone": "professional" | "friendly" | "conversational"
  },
  "recommendations": ["specific guidance for nodes"]
}

Be strategic, data-driven, and focused on both lead quality and user experience."""

    def make_decision(self, state: SurveyState, context: Dict[str, Any] = None) -> SupervisorDecision:
        """Make strategic survey administration decision."""
        try:
            # Extract relevant state information
            responses = state.get("all_responses", [])
            questions_asked = len(responses)
            available_questions = state.get("available_questions", [])
            engagement_metrics = state.get("engagement_metrics", {})
            business_rules = state.get("business_rules", {})
            
            # Prepare context for LLM
            user_message = {
                "role": "user",
                "content": f"""Analyze the current survey state and make strategic decisions:

CURRENT STATE:
- Questions asked: {questions_asked}
- Available questions: {len(available_questions)}
- Recent responses: {responses[-3:] if responses else "None"}
- Engagement metrics: {engagement_metrics}
- Business rules: {business_rules}

AVAILABLE QUESTIONS:
{json.dumps(available_questions[:10], indent=2)}  # First 10 for context

Make a strategic decision about survey continuation and provide guidance for question selection, phrasing, and engagement."""
            }
            
            # Get LLM decision
            llm_response = self.invoke_llm([user_message])
            
            # Parse response
            if isinstance(llm_response, str):
                decision_data = json.loads(llm_response)
            else:
                decision_data = llm_response
            
            # Create supervisor decision
            decision = SupervisorDecision(
                decision=decision_data.get("action", "continue"),
                reasoning=decision_data.get("reasoning", "Strategic survey continuation"),
                confidence=decision_data.get("confidence", 0.7),
                recommendations=decision_data.get("recommendations", []),
                metadata={
                    "strategy": decision_data.get("strategy", {}),
                    "questions_analyzed": questions_asked,
                    "available_pool": len(available_questions)
                }
            )
            
            # Store in history
            self.decision_history.append(decision)
            
            logger.info(f"Survey Admin decision: {decision.decision} (confidence: {decision.confidence})")
            return decision
            
        except Exception as e:
            logger.error(f"Survey Administration Supervisor error: {e}")
            # Fallback decision
            return SupervisorDecision(
                decision="continue",
                reasoning=f"Fallback due to error: {str(e)}",
                confidence=0.3,
                recommendations=["Use default question selection strategy"],
                metadata={"error": str(e), "fallback": True}
            )

    def analyze_engagement_risk(self, state: SurveyState) -> Dict[str, Any]:
        """Analyze risk of user abandonment."""
        responses = state.get("all_responses", [])
        timing_data = state.get("timing_data", {})
        
        risk_factors = {
            "question_count": len(responses),
            "response_depth": self._analyze_response_depth(responses),
            "completion_time": timing_data.get("total_time", 0),
            "last_response_time": timing_data.get("last_response_time", 0)
        }
        
        # Simple risk calculation (can be enhanced)
        risk_score = 0.0
        if risk_factors["question_count"] > 8:
            risk_score += 0.3
        if risk_factors["response_depth"] < 0.5:
            risk_score += 0.4
        if risk_factors["completion_time"] > 300:  # 5 minutes
            risk_score += 0.3
            
        return {
            "risk_score": min(risk_score, 1.0),
            "factors": risk_factors,
            "recommendations": self._get_risk_mitigation_recommendations(risk_score)
        }
    
    def _analyze_response_depth(self, responses: List[Dict]) -> float:
        """Analyze depth/quality of user responses."""
        if not responses:
            return 0.0
        
        total_depth = 0.0
        for response in responses:
            answer = response.get("answer", "")
            # Simple depth calculation based on length and content
            if len(answer.strip()) > 20:
                total_depth += 1.0
            elif len(answer.strip()) > 5:
                total_depth += 0.5
            else:
                total_depth += 0.1
        
        return total_depth / len(responses)
    
    def _get_risk_mitigation_recommendations(self, risk_score: float) -> List[str]:
        """Get recommendations for mitigating abandonment risk."""
        if risk_score > 0.7:
            return [
                "Consider survey completion - user may be fatigued",
                "Use urgent engagement messaging",
                "Ask only 1-2 critical questions",
                "Emphasize value proposition"
            ]
        elif risk_score > 0.4:
            return [
                "Add motivational engagement",
                "Limit to 2-3 questions this step",
                "Use encouraging tone",
                "Show progress indicators"
            ]
        else:
            return [
                "Normal survey flow",
                "Can ask 2-3 questions",
                "Maintain conversational tone"
            ]


def survey_admin_supervisor_node(state: SurveyState) -> Dict[str, Any]:
    """Node function for Survey Administration Supervisor."""
    supervisor = SurveyAdministrationSupervisor()
    
    # Make strategic decision
    decision = supervisor.make_decision(state)
    
    # Analyze engagement risk
    engagement_analysis = supervisor.analyze_engagement_risk(state)
    
    return {
        "survey_admin_decision": decision.to_dict(),
        "engagement_analysis": engagement_analysis,
        "supervisor_metadata": {
            "supervisor_name": supervisor.name,
            "model_used": supervisor.model_name,
            "decision_timestamp": decision.timestamp
        }
    }