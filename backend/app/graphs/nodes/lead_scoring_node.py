"""Lead Scoring Node for LangGraph.

Advanced lead qualification using scoring rubrics and business rules.
Determines lead status (yes/maybe/no) and calculates scores based on responses.

Replaces the old AgentExecutor pattern with direct function calls for better performance.
"""

from typing import Dict, Any, List
from ...state import SurveyState


def lead_scoring_node(state: SurveyState) -> Dict[str, Any]:
    """
    Calculate lead score and determine qualification status based on responses.
    
    Args:
        state: Current SurveyState containing responses and questions
        
    Returns:
        Dict with score, lead_status, min_questions_met, and failed_required updates
    """
    try:
        responses = state.get('responses', [])
        all_questions = state.get('all_questions', [])
        min_questions_met = len(responses) >= 4
        
        # Build scoring rubrics lookup
        rubrics = {}
        for question in all_questions:
            if question.get('scoring_rubric'):
                rubrics[question['id']] = {
                    'scoring_rubric': question['scoring_rubric'],
                    'question': question['question']
                }
        
        # Analyze responses and calculate score
        scoring_result = _analyze_lead_quality(responses, rubrics)
        
        # Apply business rules to determine final status
        final_score = scoring_result['score']
        red_flags = scoring_result['red_flags']
        
        # Check for critical failures
        has_critical_failure = any("CRITICAL" in flag for flag in red_flags)
        failed_required = has_critical_failure
        
        if has_critical_failure:
            lead_status = "no"
        elif not min_questions_met:
            lead_status = "unknown"
        elif final_score >= 80:
            lead_status = "yes"
        elif final_score <= 25:
            lead_status = "no"
        else:
            lead_status = "maybe"
        
        return {
            "score": final_score,
            "lead_status": lead_status,
            "min_questions_met": min_questions_met,
            "failed_required": failed_required
        }
        
    except Exception as e:
        print(f"Error in lead scoring node: {e}")
        # Fallback scoring based on participation
        response_count = len(state.get('responses', []))
        return {
            "score": response_count * 15,  # Basic participation score
            "lead_status": "unknown",
            "min_questions_met": response_count >= 4,
            "failed_required": False
        }


def _analyze_lead_quality(responses: List[Dict[str, Any]], rubrics: Dict[int, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze lead quality using responses and scoring rubrics.
    
    Args:
        responses: List of user responses
        rubrics: Scoring rubrics mapped by question ID
        
    Returns:
        Dict with score, positive indicators, red flags, and scoring details
    """
    total_score = 0
    scoring_details = []
    red_flags = []
    positive_indicators = []
    
    # Process each response against its rubric
    for response in responses:
        question_id = response.get('question_id')
        answer = response.get('answer', '').lower()
        rubric = rubrics.get(question_id, {})
        
        if not rubric:
            continue
            
        points = 0
        detail = f"Q{question_id}: "
        
        # Apply rubric-based scoring with business-specific logic
        points, flags, indicators = _score_response(question_id, answer, rubric)
        
        total_score += points
        detail += f"{points} points"
        scoring_details.append(detail)
        red_flags.extend(flags)
        positive_indicators.extend(indicators)
    
    final_score = max(0, total_score)
    
    return {
        "score": final_score,
        "positive_indicators": positive_indicators,
        "red_flags": red_flags,
        "scoring_details": scoring_details
    }


def _score_response(question_id: int, answer: str, rubric: Dict[str, Any]) -> tuple[int, List[str], List[str]]:
    """
    Score individual response based on question-specific business logic.
    
    Args:
        question_id: ID of the question being scored
        answer: User's answer (lowercase)
        rubric: Scoring rubric information
        
    Returns:
        Tuple of (points, red_flags, positive_indicators)
    """
    points = 0
    red_flags = []
    positive_indicators = []
    
    rubric_text = rubric.get('scoring_rubric', '').lower()
    
    # Location scoring (Q1)
    if 'location' in rubric_text or question_id == 1:
        if any(city in answer for city in ['somerville', 'cambridge', 'boston']):
            points = 20
            positive_indicators.append("Located in service area")
        elif 'ma' in answer or 'massachusetts' in answer:
            points = 10
        else:
            points = -10
            red_flags.append("Outside preferred service area")
    
    # Dog breed scoring (Q2)
    elif 'breed' in rubric_text or question_id == 2:
        if 'german shepherd' in answer:
            points = 25
            positive_indicators.append("Ideal dog breed")
        elif any(difficult in answer for difficult in ['pit bull', 'rottweiler']):
            points = -20
            red_flags.append("Challenging breed")
        else:
            points = 15
    
    # Vaccination status (Q5) - Critical requirement
    elif 'vaccination' in rubric_text or question_id == 5:
        if 'yes' in answer or 'up to date' in answer:
            points = 25
            positive_indicators.append("Dog is vaccinated")
        else:
            points = -50
            red_flags.append("Dog not vaccinated - CRITICAL")
    
    # Service frequency (Q4)
    elif 'frequency' in rubric_text or question_id == 4:
        if '3' in answer or '4' in answer:
            points = 20
            positive_indicators.append("Ideal service frequency")
        elif '5' in answer:
            points = 10
        elif 'once' in answer:
            points = 5
        else:
            points = 15
    
    # Default scoring for other questions with rubrics
    else:
        # Basic participation points for any question with a rubric
        points = 10
        positive_indicators.append(f"Answered Q{question_id}")
    
    return points, red_flags, positive_indicators


def recommend_next_questions(state: SurveyState) -> Dict[str, Any]:
    """
    Recommend which questions to ask next based on current lead status.
    
    Args:
        state: Current SurveyState
        
    Returns:
        Dict with question recommendations and reasoning
    """
    try:
        current_score = state.get('score', 0)
        asked_ids = state.get('asked_questions', [])
        all_questions = state.get('all_questions', [])
        
        # Filter available questions
        available_questions = [q for q in all_questions if q['id'] not in asked_ids]
        
        recommendations = []
        
        # Prioritize questions based on current score
        if current_score < 30:
            # Low score - need positive indicators
            high_value_questions = [q for q in available_questions 
                                  if 'benefit' in q.get('question', '').lower()
                                  or 'frequency' in q.get('question', '').lower()]
            recommendations.extend([q['id'] for q in high_value_questions[:2]])
        
        elif current_score > 70:
            # High score - confirm with contact info
            contact_questions = [q for q in available_questions
                               if any(word in q.get('question', '').lower()
                                     for word in ['name', 'phone', 'email'])]
            recommendations.extend([q['id'] for q in contact_questions[:2]])
        
        else:
            # Medium score - gather more qualifying info
            qualifying_questions = [q for q in available_questions
                                  if q.get('scoring_rubric', '')]
            recommendations.extend([q['id'] for q in qualifying_questions[:2]])
        
        return {
            "recommended_question_ids": recommendations[:3],  # Max 3
            "reasoning": f"Based on current score of {current_score}, focusing on qualification"
        }
        
    except Exception as e:
        print(f"Error in question recommendations: {e}")
        return {
            "recommended_question_ids": [],
            "reasoning": "Unable to make recommendations"
        }