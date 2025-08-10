"""Intelligent Engagement Node - LLM generates motivational messages to prevent abandonment."""

from typing import Dict, Any, List
import json
import logging
from datetime import datetime

from ...models import get_chat_model
from ...state import SurveyState

logger = logging.getLogger(__name__)


def intelligent_engagement_node(state: SurveyState) -> Dict[str, Any]:
    """
    LLM-driven engagement messaging that adds motivation and prevents abandonment.
    
    Args:
        state: Current SurveyState with phrased questions and engagement context
        
    Returns:
        Dict with engagement-enhanced questions and motivational messaging
    """
    try:
        # Extract state information
        phrased_questions = state.get("phrased_questions", [])
        responses_so_far = state.get("all_responses", [])
        client_info = state.get("client_info", {})
        supervisor_decision = state.get("survey_admin_decision", {})
        engagement_analysis = state.get("engagement_analysis", {})
        
        if not phrased_questions:
            logger.warning("No phrased questions for engagement enhancement")
            return {
                "final_questions": [],
                "engagement_message": "",
                "engagement_metadata": {"error": "no_questions_for_engagement"}
            }
        
        # Get engagement strategy
        strategy = supervisor_decision.get("strategy", {})
        engagement_approach = strategy.get("engagement_approach", "motivational")
        risk_score = engagement_analysis.get("risk_score", 0.3)
        risk_recommendations = engagement_analysis.get("recommendations", [])
        
        # Initialize LLM
        llm = get_chat_model(
            model="gpt-4o-mini",
            temperature=0.3,
            max_tokens=1000
        )
        
        # Determine engagement urgency
        engagement_urgency = _determine_engagement_urgency(risk_score, len(responses_so_far))
        
        system_prompt = f"""You are an expert at creating engaging survey experiences that motivate users to complete forms.

Your role is to add motivational elements that prevent abandonment while maintaining a natural conversation flow.

ENGAGEMENT STRATEGY:
- Approach: {engagement_approach}
- Urgency level: {engagement_urgency}
- User risk score: {risk_score:.1f} (0=engaged, 1=high abandonment risk)
- Business: {client_info.get('business_name', 'Our business')}

ENGAGEMENT TACTICS BY APPROACH:
- Motivational: Show progress, emphasize value, encourage completion
- Casual: Keep it light, use friendly language, minimal pressure
- Urgent: Time-sensitive language, emphasize importance (use sparingly)

ENGAGEMENT ELEMENTS TO ADD:
1. Progress indicators ("Almost done!", "Just a few more questions")
2. Value reinforcement ("This helps us serve you better")
3. Social proof ("Most people find this helpful")
4. Encouragement ("You're doing great!")
5. Next step preview ("After this, we'll show you...")

OUTPUT FORMAT:
Return valid JSON only:
{{
  "engagement_message": "Motivational message to display before questions",
  "enhanced_questions": [
    {{
      "id": 1,
      "question_with_engagement": "question text with engagement elements",
      "engagement_elements": ["progress", "value", "encouragement"]
    }}
  ],
  "completion_motivation": "Message about what happens after completion",
  "engagement_tactics": ["list of tactics used"]
}}"""

        # Calculate progress for engagement
        total_expected_questions = _estimate_total_questions(
            client_info.get("business_type", ""), 
            len(responses_so_far)
        )
        progress_percentage = min(90, (len(responses_so_far) / total_expected_questions) * 100)
        
        user_prompt = f"""Create engaging elements for this survey step:

CONTEXT:
- Questions answered: {len(responses_so_far)}
- Estimated progress: {progress_percentage:.0f}%
- Risk factors: {risk_recommendations}
- Business value: {client_info.get('value_proposition', 'Better service for you')}

QUESTIONS TO ENHANCE:
{json.dumps([{
    'id': q.get('id'),
    'phrased_text': q.get('phrased_text', ''),
    'question_type': q.get('question_type', '')
} for q in phrased_questions], indent=2)}

Create engagement elements that will motivate the user to continue while feeling natural and not pushy."""

        # Get LLM response
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = llm.invoke(messages)
        
        # Parse LLM response
        if hasattr(response, 'content'):
            llm_content = response.content
        else:
            llm_content = str(response)
            
        try:
            engagement_data = json.loads(llm_content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM engagement response: {e}")
            # Fallback to minimal engagement
            return _fallback_engagement(phrased_questions, progress_percentage)
        
        # Process enhanced questions
        enhanced_questions = []
        enhanced_lookup = {q.get("id"): q for q in engagement_data.get("enhanced_questions", [])}
        
        for phrased_q in phrased_questions:
            question_id = phrased_q.get("id")
            enhanced_info = enhanced_lookup.get(question_id, {})
            
            # Create final question object
            final_q = {
                **phrased_q,  # Keep all phrasing data
                "final_text": enhanced_info.get("question_with_engagement", phrased_q.get("phrased_text")),
                "engagement_elements": enhanced_info.get("engagement_elements", []),
                "enhanced": bool(enhanced_info)
            }
            enhanced_questions.append(final_q)
        
        return {
            "final_questions": enhanced_questions,
            "engagement_message": engagement_data.get("engagement_message", ""),
            "completion_motivation": engagement_data.get("completion_motivation", ""),
            "engagement_tactics": engagement_data.get("engagement_tactics", []),
            "engagement_metadata": {
                "approach": engagement_approach,
                "urgency": engagement_urgency,
                "risk_score": risk_score,
                "progress_shown": f"{progress_percentage:.0f}%",
                "questions_enhanced": len(enhanced_questions),
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Intelligent engagement error: {e}")
        # Fallback to basic engagement
        phrased_questions = state.get("phrased_questions", [])
        progress = (len(state.get("all_responses", [])) / 10) * 100
        return _fallback_engagement(phrased_questions, progress)


def _determine_engagement_urgency(risk_score: float, questions_asked: int) -> str:
    """Determine the urgency level for engagement messaging."""
    if risk_score > 0.7 or questions_asked > 8:
        return "high"
    elif risk_score > 0.4 or questions_asked > 5:
        return "medium"
    else:
        return "low"


def _estimate_total_questions(business_type: str, current_count: int) -> int:
    """Estimate total questions for progress calculation."""
    # Business type based estimates
    estimates = {
        "dog_walking": 8,
        "real_estate": 10,
        "consulting": 12,
        "fitness": 8,
        "cleaning": 7
    }
    
    base_estimate = estimates.get(business_type, 9)
    
    # Adjust based on current progress
    if current_count > base_estimate * 0.8:
        return current_count + 2  # Almost done
    else:
        return max(base_estimate, current_count + 3)


def _fallback_engagement(phrased_questions: List[Dict], progress_percentage: float) -> Dict[str, Any]:
    """Fallback engagement when LLM fails."""
    logger.info("Using fallback engagement messaging")
    
    # Simple progress-based engagement
    if progress_percentage > 70:
        engagement_message = "Great progress! Just a few more quick questions."
    elif progress_percentage > 40:
        engagement_message = "Thanks for your responses so far. Let's continue!"
    else:
        engagement_message = "This will help us provide you with the best service."
    
    # Create final questions with minimal engagement
    final_questions = []
    for q in phrased_questions:
        final_q = {
            **q,
            "final_text": q.get("phrased_text", q.get("question_text", "")),
            "engagement_elements": ["basic"],
            "enhanced": False
        }
        final_questions.append(final_q)
    
    return {
        "final_questions": final_questions,
        "engagement_message": engagement_message,
        "completion_motivation": "We'll review your information and get back to you soon!",
        "engagement_tactics": ["progress", "basic_motivation"],
        "engagement_metadata": {
            "fallback": True,
            "progress_shown": f"{progress_percentage:.0f}%"
        }
    }