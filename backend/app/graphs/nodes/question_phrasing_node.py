"""Question Phrasing Node for LangGraph.

Adapts question tone for business context and user type using LLM.
Ensures questions are clear, engaging, and brand-appropriate.

Replaces the old direct LLM call pattern with a proper LangGraph node.
"""

import os
from typing import Dict, Any, List
from ...state import SurveyState
from ...models import get_chat_model


def question_phrasing_node(state: SurveyState, client_info: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Rephrase questions for business context and user engagement.
    
    Args:
        state: Current SurveyState containing current_step_questions
        client_info: Optional business information for context
        
    Returns:
        Dict with phrased_questions update for state
    """
    try:
        current_questions = state.get('current_step_questions', [])
        
        if not current_questions:
            return {"phrased_questions": []}
        
        # Extract business information for context
        business_name = "Our Business"
        business_type = "service provider"
        
        if client_info and 'information' in client_info:
            business_name = client_info['information'].get('name', 'Our Business')
            business_type = client_info['information'].get('business_type', 'service provider')
        
        # Rephrase questions using LLM
        phrased_questions = _rephrase_questions_with_llm(
            current_questions, 
            business_name, 
            business_type
        )
        
        return {"phrased_questions": phrased_questions}
        
    except Exception as e:
        print(f"Error in question phrasing node: {e}")
        # Fallback to original questions on error
        original_questions = [q.get('question', '') for q in state.get('current_step_questions', [])]
        return {"phrased_questions": original_questions}


def _rephrase_questions_with_llm(
    questions: List[Dict[str, Any]], 
    business_name: str, 
    business_type: str
) -> List[str]:
    """
    Use LLM to rephrase questions for business context.
    
    Args:
        questions: List of question objects
        business_name: Name of the business
        business_type: Type of business (e.g., "dog walking service")
        
    Returns:
        List of rephrased question strings
    """
    if not questions:
        return []
    
    try:
        # Create question list for prompt
        questions_text = "\n".join([
            f"{i+1}. {q['question']}" for i, q in enumerate(questions)
        ])
        
        # Create engaging prompt for rephrasing
        prompt = f"""Rephrase these form questions for {business_name}, a {business_type}.

Make them:
- Friendly and conversational 
- Use "you" and "your"
- Appropriate for {business_name}'s brand
- Clear and engaging
- Professional but approachable

Original questions:
{questions_text}

Return only the rephrased questions, one per line, no numbers."""

        # Get chat model and make LLM call
        model = get_chat_model(temperature=0.7)
        
        # Create messages for the model
        messages = [
            {"role": "system", "content": "You rephrase form questions to be friendly and engaging while maintaining their original meaning."},
            {"role": "user", "content": prompt}
        ]
        
        # Use LangChain model to get response
        response = model.invoke(messages)
        
        # Extract and process the response
        if hasattr(response, 'content'):
            response_content = response.content
        else:
            response_content = str(response)
        
        phrased_questions = response_content.strip().split('\n')
        
        # Ensure we have the same number of questions
        if len(phrased_questions) != len(questions):
            print(f"⚠️ Question count mismatch ({len(phrased_questions)} vs {len(questions)}). Using original questions.")
            return [q['question'] for q in questions]
        
        # Clean up the phrased questions
        cleaned_questions = []
        for q in phrased_questions:
            cleaned = q.strip()
            # Remove any numbering that might have been added
            if cleaned.startswith(('1.', '2.', '3.', '4.', '5.')):
                cleaned = cleaned[2:].strip()
            if cleaned:
                cleaned_questions.append(cleaned)
        
        # Final validation
        if len(cleaned_questions) != len(questions):
            print(f"⚠️ Final question count mismatch. Using original questions.")
            return [q['question'] for q in questions]
        
        return cleaned_questions
        
    except Exception as e:
        print(f"❌ Question phrasing failed: {e}")
        # Fallback to original questions
        return [q['question'] for q in questions]


def validate_phrased_questions(
    original_questions: List[Dict[str, Any]], 
    phrased_questions: List[str]
) -> bool:
    """
    Validate that phrased questions match original questions in count and basic structure.
    
    Args:
        original_questions: List of original question objects
        phrased_questions: List of phrased question strings
        
    Returns:
        True if validation passes, False otherwise
    """
    try:
        # Check count match
        if len(original_questions) != len(phrased_questions):
            return False
        
        # Check that all phrased questions are non-empty
        if not all(q.strip() for q in phrased_questions):
            return False
        
        # Check reasonable length (not too short, not too long)
        for phrased in phrased_questions:
            if len(phrased.strip()) < 5 or len(phrased.strip()) > 200:
                return False
        
        return True
        
    except Exception:
        return False