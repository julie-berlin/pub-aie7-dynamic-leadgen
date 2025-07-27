"""
Engagement Agent

Creates compelling headlines and motivational content to maximize
form completion and prevent abandonment.
"""

from langchain.tools import tool
from langchain_core.messages import HumanMessage
from typing import Dict, Any
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from agent_factory import create_agent, create_llm

@tool
def generate_engagement_content(
    step_number: str,
    total_responses: str,
    business_name: str,
    business_type: str,
    questions_preview: str
) -> str:
    """
    Generate engaging headline and motivational content for a form step.
    
    Args:
        step_number: Current step number
        total_responses: Number of responses collected so far
        business_name: Name of the business
        business_type: Type of business (e.g., "dog walking service")
        questions_preview: Preview of questions being asked this step
    
    Returns:
        JSON string with headline and motivation
    """
    try:
        step = int(step_number)
        response_count = int(total_responses)
        
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
        
        # Add progress encouragement for later steps
        if response_count >= 3:
            motivation += " You're making excellent progress!"
        
        return json.dumps({
            "headline": headline,
            "motivation": motivation
        })
        
    except Exception as e:
        print(f"Error generating engagement content: {e}")
        return json.dumps({
            "headline": "Let's continue! 🚀",
            "motivation": "Thanks for taking the time to share with us."
        })

@tool
def analyze_abandonment_risk(
    step_number: str,
    total_responses: str,
    question_types: str
) -> str:
    """
    Analyze risk of form abandonment and suggest engagement strategies.
    
    Args:
        step_number: Current step number
        total_responses: Number of responses collected so far
        question_types: Types of questions being asked (contact, personal, etc.)
    
    Returns:
        JSON string with risk assessment and engagement recommendations
    """
    try:
        step = int(step_number)
        response_count = int(total_responses)
        
        # Calculate abandonment risk
        risk_level = "low"
        recommendations = []
        
        if step > 4:
            risk_level = "medium"
            recommendations.append("Add progress indicator")
            recommendations.append("Emphasize value proposition")
        
        if "contact" in question_types.lower() and response_count < 3:
            risk_level = "high"
            recommendations.append("Delay contact questions until more engagement")
        
        if step > 6:
            risk_level = "high"
            recommendations.append("Consider completion incentive")
            recommendations.append("Show progress completion percentage")
        
        return json.dumps({
            "risk_level": risk_level,
            "recommendations": recommendations
        })
        
    except Exception as e:
        print(f"Error analyzing abandonment risk: {e}")
        return json.dumps({
            "risk_level": "unknown",
            "recommendations": ["Monitor user engagement"]
        })

def create_engagement_agent():
    """Create the engagement agent"""
    
    system_prompt = """You are an Engagement Agent specialized in conversion optimization and user psychology.

Your specialty is creating compelling form content that maximizes completion rates and prevents abandonment.

Key responsibilities:
- Generate catchy, encouraging headlines for each form step
- Create motivational content that builds trust and momentum
- Apply marketing psychology principles to reduce abandonment
- Adapt messaging based on user progress and question types
- Maintain professional yet friendly tone throughout

Engagement strategies:
- Early steps: Build excitement and trust
- Middle steps: Acknowledge progress and maintain momentum  
- Later steps: Emphasize near completion and value
- Contact questions: Reassure about privacy and next steps
- Tough questions: Frame as partnership and mutual fit

Use your tools to generate content that keeps users engaged and moving forward."""

    llm = create_llm(temperature=0.8)  # Higher temperature for creative content
    tools = [generate_engagement_content, analyze_abandonment_risk]
    
    return create_agent(llm, tools, system_prompt)

def invoke_engagement_agent(state: Dict[str, Any], client_info: Dict[str, Any]) -> Dict[str, str]:
    """
    Invoke the engagement agent to generate step content
    
    Args:
        state: Current form state
        client_info: Business information
    
    Returns:
        Dict with headline and motivation content
    """
    agent = create_engagement_agent()
    
    business_name = client_info.get('information', {}).get('name', 'Our Business')
    business_type = client_info.get('information', {}).get('business_type', 'service provider')
    
    # Preview questions for context
    questions = state.get('current_step_questions', [])
    questions_preview = ", ".join([q.get('question', '')[:50] for q in questions])
    
    messages = [
        HumanMessage(content=f"""
Please generate engaging content for this form step.

Step number: {state.get('step', 0) + 1}
Total responses so far: {len(state.get('responses', []))}
Business name: {business_name}
Business type: {business_type}
Questions being asked: {questions_preview}

Generate a compelling headline and motivational content that will encourage the user to complete this step and continue with the form.
        """)
    ]
    
    try:
        result = agent.invoke({"messages": messages})
        
        if 'output' in result:
            content = json.loads(result['output'])
            return {
                'headline': content.get('headline', 'Continue your journey! 🚀'),
                'motivation': content.get('motivation', 'Thanks for sharing with us.')
            }
        else:
            print("No output from engagement agent")
            return {
                'headline': 'Let\'s continue! 🌟',
                'motivation': 'Thanks for taking the time to share with us.'
            }
            
    except Exception as e:
        print(f"Error invoking engagement agent: {e}")
        return {
            'headline': 'You\'re doing great! ✨',
            'motivation': 'Thanks for sharing these important details.'
        }

if __name__ == "__main__":
    # Test the agent
    test_state = {
        'step': 1,
        'responses': [{'question_id': 1, 'answer': 'Boston'}],
        'current_step_questions': [
            {'question': 'What is your dog breed?'},
            {'question': 'How often do you need walking?'}
        ]
    }
    
    test_client = {
        'information': {
            'name': 'Darlene\'s Doggie Daywalks',
            'business_type': 'dog walking service'
        }
    }
    
    content = invoke_engagement_agent(test_state, test_client)
    print(f"Generated content: {content}")