"""Engagement Node for LangGraph.

Creates compelling headlines and motivational content to maximize
form completion and prevent abandonment.

Replaces the old AgentExecutor pattern with direct function calls for better performance.
"""

from typing import Dict, Any
from ...state import SurveyState


def engagement_node(state: SurveyState, client_info: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generate engaging headline and motivational content for current step.
    
    Args:
        state: Current SurveyState
        client_info: Optional business information for personalization
        
    Returns:
        Dict with step_headline and step_motivation updates for state
    """
    try:
        step = state.get('step', 0) + 1  # Display step (1-based)
        response_count = len(state.get('responses', []))
        
        # Extract business information for personalization
        business_name = "Our Business"
        if client_info and 'information' in client_info:
            business_name = client_info['information'].get('name', 'Our Business')
        
        # Generate contextual content based on progress
        headline, motivation = _generate_step_content(step, response_count, business_name)
        
        # Add progress encouragement for later steps
        if response_count >= 3:
            motivation += " You're making excellent progress!"
        
        return {
            "step_headline": headline,
            "step_motivation": motivation
        }
        
    except Exception as e:
        print(f"Error in engagement node: {e}")
        # Return fallback content on error
        return {
            "step_headline": "Let's continue! 🚀",
            "step_motivation": "Thanks for taking the time to share with us."
        }


def _generate_step_content(step: int, response_count: int, business_name: str) -> tuple[str, str]:
    """
    Generate step-specific headline and motivation content.
    
    Args:
        step: Current step number (1-based)
        response_count: Number of responses collected so far  
        business_name: Name of the business for personalization
        
    Returns:
        Tuple of (headline, motivation) strings
    """
    # Generate contextual content based on progress
    if step == 1:
        headline = f"Let's find the perfect plan for you! 🎯"
        motivation = f"Your satisfaction is {business_name}'s top priority."
    elif step == 2:
        headline = "Tell us more about your needs 💭"
        motivation = "Every customer is unique - help us personalize your experience."
    elif step == 3:
        headline = "Almost there! Just a few more details... ✨"
        motivation = "We're building something amazing together!"
    elif response_count >= 3:
        headline = f"Perfect! Let's make sure we're the right fit 🎯"
        motivation = "Great answers so far - you're clearly thoughtful about your needs."
    else:
        headline = f"Step {step} - You're doing great! 🌟"
        motivation = "Thanks for sharing these important details with us."
    
    return headline, motivation


def analyze_abandonment_risk(state: SurveyState) -> Dict[str, Any]:
    """
    Analyze risk of form abandonment based on current state.
    
    Args:
        state: Current SurveyState
        
    Returns:
        Dict with risk_level and recommendations
    """
    try:
        step = state.get('step', 0)
        response_count = len(state.get('responses', []))
        current_questions = state.get('current_step_questions', [])
        
        # Analyze question types
        question_types = []
        for q in current_questions:
            question_text = q.get('question', '').lower()
            if any(word in question_text for word in ['name', 'phone', 'email', 'contact']):
                question_types.append('contact')
            elif any(word in question_text for word in ['dog', 'pet', 'breed']):
                question_types.append('personal')
            else:
                question_types.append('general')
        
        # Calculate abandonment risk
        risk_level = "low"
        recommendations = []
        
        if step > 4:
            risk_level = "medium"
            recommendations.extend([
                "Add progress indicator",
                "Emphasize value proposition"
            ])
        
        if "contact" in question_types and response_count < 3:
            risk_level = "high"
            recommendations.append("Delay contact questions until more engagement")
        
        if step > 6:
            risk_level = "high"
            recommendations.extend([
                "Consider completion incentive",
                "Show progress completion percentage"
            ])
        
        return {
            "risk_level": risk_level,
            "recommendations": recommendations,
            "step": step,
            "response_count": response_count
        }
        
    except Exception as e:
        print(f"Error analyzing abandonment risk: {e}")
        return {
            "risk_level": "unknown",
            "recommendations": ["Monitor user engagement"],
            "step": 0,
            "response_count": 0
        }