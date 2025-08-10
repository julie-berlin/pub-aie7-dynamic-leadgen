"""Intelligent Question Selection Node - LLM-driven question selection within business rules."""

from typing import Dict, Any, List
import json
import logging
from datetime import datetime

from ...models import get_chat_model
from ...state import SurveyState

logger = logging.getLogger(__name__)


def intelligent_question_selection_node(state: SurveyState) -> Dict[str, Any]:
    """
    LLM-driven question selection that adapts to user responses while respecting business rules.
    
    Args:
        state: Current SurveyState with responses and available questions
        
    Returns:
        Dict with selected questions and reasoning
    """
    try:
        # Extract state information
        available_questions = state.get("available_questions", [])
        responses_so_far = state.get("all_responses", [])
        questions_asked = state.get("questions_asked", [])
        business_rules = state.get("business_rules", {})
        supervisor_decision = state.get("survey_admin_decision", {})
        form_config = state.get("form_config", {})
        
        # Get supervisor guidance if available
        strategy = supervisor_decision.get("strategy", {})
        recommended_count = strategy.get("question_count", 2)
        question_types = strategy.get("question_types", ["qualification"])
        
        # Filter available questions (remove already asked)
        asked_ids = set(questions_asked)
        available = [q for q in available_questions if q.get("id") not in asked_ids]
        
        if not available:
            logger.warning("No available questions for selection")
            return {
                "selected_questions": [],
                "selection_reasoning": "No more questions available",
                "selection_metadata": {"error": "no_questions_available"}
            }
        
        # Initialize LLM
        llm = get_chat_model(
            model="gpt-4o-mini",
            temperature=0.3,
            max_tokens=1500
        )
        
        # Create LLM prompt
        system_prompt = """You are an intelligent question selection agent for lead generation surveys.

Your role is to select the optimal 1-3 questions from available options to maximize lead qualification while maintaining user engagement.

SELECTION CRITERIA:
1. Never repeat questions already asked
2. Follow business rules and requirements
3. Maintain logical conversation flow
4. Consider user's previous responses
5. Balance information gain with user experience
6. Respect supervisor strategy guidance

BUSINESS RULES TO FOLLOW:
- Required questions must be asked before completion
- Don't ask qualifying questions too early (warm up first)
- Consider question difficulty progression
- Maximum 3 questions per step
- Ensure questions are relevant to previous responses

OUTPUT FORMAT:
Respond with valid JSON only:
{
  "selected_question_ids": [1, 5, 8],
  "reasoning": "detailed explanation for selection",
  "confidence": 0.85,
  "flow_logic": "explanation of conversation flow",
  "metadata": {
    "primary_goal": "qualification" | "engagement" | "information_gathering",
    "difficulty_level": "easy" | "medium" | "hard",
    "expected_response_time": "30-60 seconds"
  }
}"""

        user_prompt = f"""Select the next questions for this lead generation survey:

SUPERVISOR GUIDANCE:
- Recommended question count: {recommended_count}
- Target question types: {question_types}
- Strategy: {strategy}

CONVERSATION CONTEXT:
- Questions asked so far: {len(responses_so_far)}
- Previous responses: {responses_so_far[-3:] if responses_so_far else "None"}
- Questions already asked: {questions_asked}

BUSINESS RULES:
{json.dumps(business_rules, indent=2)}

AVAILABLE QUESTIONS:
{json.dumps(available[:15], indent=2)}  # Limit to first 15 for context

Select {recommended_count} questions that create the best conversation flow and maximize lead qualification information."""

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
            selection_data = json.loads(llm_content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            # Fallback to rule-based selection
            return _fallback_question_selection(available, recommended_count, responses_so_far)
        
        # Validate and get selected questions
        selected_ids = selection_data.get("selected_question_ids", [])
        selected_questions = []
        
        # Create lookup for available questions
        question_lookup = {q.get("id"): q for q in available}
        
        for q_id in selected_ids:
            if q_id in question_lookup:
                selected_questions.append(question_lookup[q_id])
            else:
                logger.warning(f"Selected question ID {q_id} not found in available questions")
        
        # Ensure we don't exceed the limit
        if len(selected_questions) > 3:
            selected_questions = selected_questions[:3]
            logger.info(f"Trimmed selection to 3 questions (was {len(selected_ids)})")
        
        # Apply business rule validation
        validated_questions = _apply_business_rule_validation(
            selected_questions, 
            business_rules, 
            responses_so_far
        )
        
        return {
            "selected_questions": validated_questions,
            "selection_reasoning": selection_data.get("reasoning", "Intelligent LLM selection"),
            "selection_confidence": selection_data.get("confidence", 0.7),
            "flow_logic": selection_data.get("flow_logic", "Optimized conversation flow"),
            "selection_metadata": {
                "llm_decision": True,
                "supervisor_guidance": strategy,
                "questions_considered": len(available),
                "questions_selected": len(validated_questions),
                "timestamp": datetime.now().isoformat(),
                **selection_data.get("metadata", {})
            }
        }
        
    except Exception as e:
        logger.error(f"Intelligent question selection error: {e}")
        # Fallback to simple rule-based selection
        available_questions = state.get("available_questions", [])
        responses_so_far = state.get("all_responses", [])
        return _fallback_question_selection(available_questions, 2, responses_so_far)


def _apply_business_rule_validation(
    questions: List[Dict], 
    business_rules: Dict, 
    responses: List[Dict]
) -> List[Dict]:
    """Apply business rule validation to selected questions."""
    validated = []
    
    for question in questions:
        # Check if question violates any business rules
        if _is_question_valid(question, business_rules, responses):
            validated.append(question)
        else:
            logger.info(f"Question {question.get('id')} failed business rule validation")
    
    return validated


def _is_question_valid(question: Dict, business_rules: Dict, responses: List[Dict]) -> bool:
    """Check if a question passes business rule validation."""
    # Example business rule checks
    question_type = question.get("question_type", "")
    responses_count = len(responses)
    
    # Don't ask qualifying questions too early
    if question_type == "qualifying" and responses_count < 2:
        return False
    
    # Check required question timing
    if question.get("is_required") and business_rules.get("defer_required_until", 3) > responses_count:
        return False
    
    # Add more business rule checks as needed
    return True


def _fallback_question_selection(
    available_questions: List[Dict], 
    count: int, 
    responses: List[Dict]
) -> Dict[str, Any]:
    """Fallback rule-based question selection when LLM fails."""
    logger.info("Using fallback rule-based question selection")
    
    # Simple rule: select first available questions, prioritizing non-qualifying
    selected = []
    responses_count = len(responses)
    
    # First, add non-qualifying questions for early engagement
    for q in available_questions:
        if len(selected) >= count:
            break
        if q.get("question_type") != "qualifying" or responses_count >= 3:
            selected.append(q)
    
    # Fill remaining slots with any available questions
    for q in available_questions:
        if len(selected) >= count:
            break
        if q not in selected:
            selected.append(q)
    
    return {
        "selected_questions": selected[:count],
        "selection_reasoning": "Fallback rule-based selection due to LLM error",
        "selection_confidence": 0.3,
        "flow_logic": "Basic rule-based flow",
        "selection_metadata": {
            "llm_decision": False,
            "fallback": True,
            "questions_selected": len(selected[:count])
        }
    }