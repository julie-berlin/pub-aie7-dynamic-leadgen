"""
Lead Scoring Agent

Advanced lead qualification using LLM reasoning combined with 
scoring rubrics and business rules.
"""

from langchain.tools import tool
from langchain_core.messages import HumanMessage
from typing import List, Dict, Any
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from agent_factory import create_agent, create_llm

@tool
def analyze_lead_quality(
    responses: str,
    scoring_rubrics: str,
    business_requirements: str,
    min_questions_met: str
) -> str:
    """
    Analyze lead quality using responses and scoring rubrics.
    
    Args:
        responses: JSON string of user responses
        scoring_rubrics: JSON string of scoring rubrics for each question
        business_requirements: Business-specific qualification criteria
        min_questions_met: Whether minimum question threshold is met
    
    Returns:
        JSON string with score, status, and reasoning
    """
    try:
        response_list = json.loads(responses)
        rubrics = json.loads(scoring_rubrics)
        min_met = json.loads(min_questions_met)
        
        total_score = 0
        scoring_details = []
        red_flags = []
        positive_indicators = []
        
        # Process each response against its rubric
        for response in response_list:
            question_id = response['question_id']
            answer = response['answer'].lower()
            rubric = rubrics.get(str(question_id), {})
            
            if not rubric:
                continue
                
            points = 0
            detail = f"Q{question_id}: "
            
            # Apply rubric-based scoring
            rubric_text = rubric.get('scoring_rubric', '').lower()
            
            if 'location' in rubric_text or question_id == 1:
                if any(city in answer for city in ['somerville', 'cambridge', 'boston']):
                    points = 20
                    positive_indicators.append("Located in service area")
                elif 'ma' in answer or 'massachusetts' in answer:
                    points = 10
                else:
                    points = -10
                    red_flags.append("Outside preferred service area")
            
            elif 'breed' in rubric_text or question_id == 2:
                if 'german shepherd' in answer:
                    points = 25
                    positive_indicators.append("Ideal dog breed")
                elif any(difficult in answer for difficult in ['pit bull', 'rottweiler']):
                    points = -20
                    red_flags.append("Challenging breed")
                else:
                    points = 15
            
            elif 'vaccination' in rubric_text or question_id == 5:
                if 'yes' in answer or 'up to date' in answer:
                    points = 25
                    positive_indicators.append("Dog is vaccinated")
                else:
                    points = -50
                    red_flags.append("Dog not vaccinated - CRITICAL")
            
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
            
            # Add more rubric logic as needed
            
            total_score += points
            detail += f"{points} points"
            scoring_details.append(detail)
        
        # Determine lead status based on business rules
        final_score = max(0, total_score)
        
        # Check for critical failures
        has_critical_failure = any("CRITICAL" in flag for flag in red_flags)
        
        if has_critical_failure:
            status = "no"
            reasoning = "Failed critical requirement"
        elif not min_met:
            status = "unknown"
            reasoning = "Need more information to qualify"
        elif final_score >= 80:
            status = "yes"
            reasoning = "High-quality lead with strong indicators"
        elif final_score <= 25:
            status = "no"
            reasoning = "Low score with multiple concerns"
        else:
            status = "maybe"
            reasoning = "Moderate potential, needs review"
        
        return json.dumps({
            "score": final_score,
            "status": status,
            "reasoning": reasoning,
            "positive_indicators": positive_indicators,
            "red_flags": red_flags,
            "scoring_details": scoring_details
        })
        
    except Exception as e:
        print(f"Error in lead analysis: {e}")
        return json.dumps({
            "score": 50,
            "status": "unknown",
            "reasoning": "Error in analysis",
            "positive_indicators": [],
            "red_flags": [],
            "scoring_details": []
        })

@tool
def recommend_next_questions(
    current_score: str,
    missing_info: str,
    available_questions: str
) -> str:
    """
    Recommend which questions to ask next based on current lead status.
    
    Args:
        current_score: Current lead score
        missing_info: Information still needed for qualification
        available_questions: Questions not yet asked
    
    Returns:
        JSON string with question recommendations and priority
    """
    try:
        score = int(current_score)
        questions = json.loads(available_questions)
        
        recommendations = []
        
        # Prioritize questions based on current score and missing info
        if score < 30:
            # Low score - need positive indicators
            high_value_questions = [q for q in questions 
                                  if 'benefit' in q.get('question', '').lower()
                                  or 'frequency' in q.get('question', '').lower()]
            recommendations.extend([q['id'] for q in high_value_questions[:2]])
        
        elif score > 70:
            # High score - confirm with contact info
            contact_questions = [q for q in questions
                               if any(word in q.get('question', '').lower()
                                     for word in ['name', 'phone', 'email'])]
            recommendations.extend([q['id'] for q in contact_questions[:2]])
        
        else:
            # Medium score - gather more qualifying info
            qualifying_questions = [q for q in questions
                                  if q.get('scoring_rubric', '')]
            recommendations.extend([q['id'] for q in qualifying_questions[:2]])
        
        return json.dumps({
            "recommended_question_ids": recommendations[:3],  # Max 3
            "reasoning": f"Based on current score of {score}, focusing on qualification"
        })
        
    except Exception as e:
        print(f"Error in question recommendations: {e}")
        return json.dumps({
            "recommended_question_ids": [],
            "reasoning": "Unable to make recommendations"
        })

def create_lead_scoring_agent():
    """Create the lead scoring agent"""
    
    system_prompt = """You are a Lead Scoring Agent specialized in customer qualification and business fit assessment.

Your specialty is analyzing customer responses to determine lead quality, conversion potential, and business fit using both quantitative scoring and qualitative reasoning.

Key responsibilities:
- Apply scoring rubrics to customer responses
- Identify positive indicators and red flags
- Determine lead status: yes (80+), maybe (26-79), no (≤25)
- Provide reasoning for scoring decisions
- Recommend next questions based on current assessment
- Enforce business rules and critical requirements

Scoring approach:
- Use provided rubrics as base scoring
- Apply business logic and experience
- Consider response quality and completeness
- Flag critical failures (e.g., unvaccinated pets)
- Balance quantitative scores with qualitative assessment

Always provide clear reasoning for your scoring decisions and recommendations."""

    llm = create_llm(temperature=0.3)  # Lower temperature for consistent scoring
    tools = [analyze_lead_quality, recommend_next_questions]
    
    return create_agent(llm, tools, system_prompt)

def invoke_lead_scoring_agent(state: Dict[str, Any], all_questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Invoke the lead scoring agent to analyze current responses
    
    Args:
        state: Current form state with responses
        all_questions: All available questions for rubric lookup
    
    Returns:
        Dict with score, status, reasoning, and recommendations
    """
    agent = create_lead_scoring_agent()
    
    responses = state.get('responses', [])
    min_questions_met = len(responses) >= 4
    
    # Build scoring rubrics lookup
    rubrics = {}
    for question in all_questions:
        if question.get('scoring_rubric'):
            rubrics[str(question['id'])] = {
                'scoring_rubric': question['scoring_rubric'],
                'question': question['question']
            }
    
    messages = [
        HumanMessage(content=f"""
Please analyze this lead's quality based on their responses.

Responses: {json.dumps(responses)}
Scoring rubrics: {json.dumps(rubrics)}
Business requirements: Dog walking service - requires vaccination, prefers local clients, values regular customers
Minimum questions met: {json.dumps(min_questions_met)}

Provide a comprehensive lead assessment with score, status, and reasoning.
        """)
    ]
    
    try:
        result = agent.invoke({"messages": messages})
        
        if 'output' in result:
            analysis = json.loads(result['output'])
            return {
                'score': analysis.get('score', 50),
                'status': analysis.get('status', 'unknown'),
                'reasoning': analysis.get('reasoning', 'Analysis completed'),
                'positive_indicators': analysis.get('positive_indicators', []),
                'red_flags': analysis.get('red_flags', []),
                'scoring_details': analysis.get('scoring_details', [])
            }
        else:
            print("No output from lead scoring agent")
            return {
                'score': 50,
                'status': 'unknown',
                'reasoning': 'Agent analysis failed',
                'positive_indicators': [],
                'red_flags': [],
                'scoring_details': []
            }
            
    except Exception as e:
        print(f"Error invoking lead scoring agent: {e}")
        # Fallback scoring
        return {
            'score': len(responses) * 15,  # Basic participation score
            'status': 'unknown',
            'reasoning': 'Fallback scoring due to agent error',
            'positive_indicators': ['User completed questions'],
            'red_flags': [],
            'scoring_details': [f'Basic score: {len(responses)} responses']
        }

if __name__ == "__main__":
    # Test the agent
    test_state = {
        'responses': [
            {
                'question_id': 1,
                'answer': 'Somerville, MA',
                'original_question': 'What is your location?'
            },
            {
                'question_id': 5,
                'answer': 'Yes, up to date',
                'original_question': 'Is your dog vaccinated?'
            }
        ]
    }
    
    test_questions = [
        {'id': 1, 'question': 'What is your location?', 'scoring_rubric': 'Somerville/Cambridge: 20 points, MA: 10 points, other: -10 points'},
        {'id': 5, 'question': 'Is your dog vaccinated?', 'scoring_rubric': 'Yes: 25 points, No: -50 points (critical failure)'}
    ]
    
    result = invoke_lead_scoring_agent(test_state, test_questions)
    print(f"Lead scoring result: {result}")