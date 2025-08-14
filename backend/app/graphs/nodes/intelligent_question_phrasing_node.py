"""Intelligent Question Phrasing Node - LLM rewrites questions for better engagement."""

from typing import Dict, Any, List
import json
import logging
from datetime import datetime

from ...models import get_chat_model
from ...state import SurveyState

logger = logging.getLogger(__name__)


def intelligent_question_phrasing_node(state: SurveyState) -> Dict[str, Any]:
    """
    LLM-driven question phrasing that adapts language for better user engagement.
    
    Args:
        state: Current SurveyState with selected questions and context
        
    Returns:
        Dict with phrased questions optimized for engagement
    """
    try:
        # Extract state information
        selected_questions = state.get("selected_questions", [])
        responses_so_far = state.get("all_responses", [])
        client_info = state.get("client_info", {})
        supervisor_decision = state.get("survey_admin_decision", {})
        engagement_analysis = state.get("engagement_analysis", {})
        
        if not selected_questions:
            logger.warning("No selected questions to phrase")
            return {
                "phrased_questions": [],
                "phrasing_metadata": {"error": "no_questions_to_phrase"}
            }
        
        # Get supervisor guidance
        strategy = supervisor_decision.get("strategy", {})
        phrasing_tone = strategy.get("phrasing_tone", "friendly")
        engagement_approach = strategy.get("engagement_approach", "conversational")
        
        # Analyze user engagement level
        risk_score = engagement_analysis.get("risk_score", 0.3)
        
        # Initialize LLM
        llm = get_chat_model(
            model_name="gpt-4o-mini",
            temperature=0.4  # Higher temperature for creative phrasing
        )
        
        # Create context for phrasing
        business_context = f"{client_info.get('business_name', 'Our business')} - {client_info.get('industry', 'Service business')}"
        user_context = _analyze_user_context(responses_so_far)
        
        system_prompt = f"""You are an expert at phrasing survey questions to maximize user engagement and completion rates.

Your role is to rewrite questions to be more engaging, conversational, and appropriate for the user context while maintaining their core purpose.

PHRASING GUIDELINES:
- Tone: {phrasing_tone}
- Engagement approach: {engagement_approach}
- Business context: {business_context}
- User engagement risk: {risk_score:.1f} (0=low risk, 1=high risk)

PHRASING PRINCIPLES:
1. Make questions conversational and natural
2. Use "you" language to be personal
3. Add context that shows why the question matters
4. Remove jargon and technical terms
5. Make the value exchange clear
6. Add gentle motivation if user shows fatigue
7. Keep questions concise but engaging

TONE ADAPTATION:
- Professional: Clear, respectful, business-focused
- Friendly: Warm, approachable, helpful
- Conversational: Casual, natural, like talking to a friend
- Urgent: Time-sensitive, action-oriented (use sparingly)

OUTPUT FORMAT:
Return valid JSON only:
{{
  "phrased_questions": [
    {{
      "id": 1,
      "original_text": "original question",
      "phrased_text": "rewritten engaging version",
      "phrasing_notes": "explanation of changes made"
    }}
  ],
  "overall_approach": "description of phrasing strategy",
  "engagement_adjustments": ["list of specific engagement tactics used"]
}}"""

        # Prepare user prompt with questions to phrase
        questions_to_phrase = []
        for q in selected_questions:
            questions_to_phrase.append({
                "id": q.get("id"),
                "original_text": q.get("question_text", ""),
                "question_type": q.get("question_type", ""),
                "is_required": q.get("is_required", False),
                "options": q.get("options", [])
            })

        user_prompt = f"""Please rephrase these questions for better engagement:

USER CONTEXT:
- Questions answered so far: {len(responses_so_far)}
- User engagement level: {'High risk of abandonment' if risk_score > 0.6 else 'Good engagement' if risk_score < 0.3 else 'Moderate engagement'}
- Previous response quality: {user_context['response_quality']}
- Conversation tone so far: {user_context['conversation_tone']}

QUESTIONS TO REPHRASE:
{json.dumps(questions_to_phrase, indent=2)}

Make these questions more engaging while preserving their core purpose and ensuring they flow naturally from the previous conversation."""

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
            phrasing_data = json.loads(llm_content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM phrasing response: {e}")
            # Fallback to original questions
            return _fallback_question_phrasing(selected_questions)
        
        # Process phrased questions
        phrased_questions = []
        phrased_lookup = {q.get("id"): q for q in phrasing_data.get("phrased_questions", [])}
        
        for original_q in selected_questions:
            original_id = original_q.get("id")
            phrased_info = phrased_lookup.get(original_id, {})
            
            # Create phrased question object
            phrased_q = {
                **original_q,  # Keep all original data
                "phrased_text": phrased_info.get("phrased_text", original_q.get("question_text")),
                "original_text": original_q.get("question_text"),
                "phrasing_notes": phrased_info.get("phrasing_notes", "No phrasing applied"),
                "phrased": True
            }
            phrased_questions.append(phrased_q)
        
        return {
            "phrased_questions": phrased_questions,
            "phrasing_approach": phrasing_data.get("overall_approach", "Engagement-focused phrasing"),
            "engagement_adjustments": phrasing_data.get("engagement_adjustments", []),
            "phrasing_metadata": {
                "tone_used": phrasing_tone,
                "engagement_approach": engagement_approach,
                "risk_level": risk_score,
                "questions_phrased": len(phrased_questions),
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Intelligent question phrasing error: {e}")
        # Fallback to original questions
        selected_questions = state.get("selected_questions", [])
        return _fallback_question_phrasing(selected_questions)


def _analyze_user_context(responses: List[Dict]) -> Dict[str, str]:
    """Analyze user's response patterns to inform phrasing."""
    if not responses:
        return {
            "response_quality": "unknown",
            "conversation_tone": "neutral"
        }
    
    # Analyze response lengths and quality
    avg_length = sum(len(r.get("answer", "")) for r in responses) / len(responses)
    
    response_quality = "high" if avg_length > 50 else "medium" if avg_length > 15 else "low"
    
    # Simple tone analysis (can be enhanced)
    recent_responses = [r.get("answer", "") for r in responses[-3:]]
    combined_text = " ".join(recent_responses).lower()
    
    if any(word in combined_text for word in ["excited", "great", "love", "perfect"]):
        conversation_tone = "enthusiastic"
    elif any(word in combined_text for word in ["maybe", "not sure", "depends"]):
        conversation_tone = "hesitant"
    else:
        conversation_tone = "neutral"
    
    return {
        "response_quality": response_quality,
        "conversation_tone": conversation_tone
    }


def _fallback_question_phrasing(selected_questions: List[Dict]) -> Dict[str, Any]:
    """Fallback when LLM phrasing fails - return original questions."""
    logger.info("Using fallback question phrasing (original questions)")
    
    phrased_questions = []
    for q in selected_questions:
        phrased_q = {
            **q,
            "phrased_text": q.get("question_text", ""),
            "original_text": q.get("question_text", ""),
            "phrasing_notes": "Fallback - original question used",
            "phrased": False
        }
        phrased_questions.append(phrased_q)
    
    return {
        "phrased_questions": phrased_questions,
        "phrasing_approach": "Fallback - original questions",
        "engagement_adjustments": [],
        "phrasing_metadata": {
            "fallback": True,
            "error": "LLM phrasing failed"
        }
    }