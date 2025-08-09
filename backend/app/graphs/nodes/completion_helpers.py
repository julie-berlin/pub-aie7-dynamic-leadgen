"""
Completion Helper Functions for LangGraph Survey Flow

Helper functions for LLM-generated personalized completion messages.
Uses business context and client info for dynamic message generation.
"""

from __future__ import annotations
from typing import List, Dict, Any

from ..toolbelts.completion_toolbelt import completion_toolbelt


def extract_personalization_data(responses: List[Dict[str, Any]]) -> Dict[str, str]:
    """Extract user name and subject info for personalization."""
    subject_info = "you"  # Generic fallback
    user_name = ""
    contact_info = {}
    
    for response in responses:
        question_id = response.get('question_id')
        answer = response.get('answer', '')
        original_question = response.get('original_question', '').lower()
        
        # Look for name-related questions
        if 'name' in original_question and 'full' in original_question:
            user_name = answer.split()[0] if answer else ""
        # Look for subject-related questions (breed, product, service, etc.)
        elif any(keyword in original_question for keyword in ['breed', 'product', 'service', 'type']):
            if answer:
                subject_info = answer
        # Extract contact information
        elif 'phone' in original_question:
            contact_info['phone'] = answer
        elif 'email' in original_question:
            contact_info['email'] = answer
    
    greeting = f"Hi {user_name}!" if user_name else "Hello!"
    return {
        'subject_info': subject_info, 
        'greeting': greeting, 
        'user_name': user_name,
        'contact_info': contact_info
    }


def generate_completion_message_with_llm(
    lead_status: str, 
    personalization: Dict[str, str], 
    business_name: str, 
    owner_name: str,
    business_context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate completion message using LLM based on business context and lead status.
    
    Args:
        lead_status: 'yes', 'maybe', or 'no'
        personalization: Extracted user data
        business_name: Name of the business
        owner_name: Name of the business owner
        business_context: Full business background, goals, and context
        
    Returns:
        Dict with completion_message and next_steps
    """
    try:
        chat_model = completion_toolbelt.get_llm_model(temperature=0.7)
        
        # Build context for the LLM
        business_background = business_context.get('background', '')
        business_goals = business_context.get('goals', '')
        
        greeting = personalization['greeting']
        subject_info = personalization['subject_info']
        user_name = personalization.get('user_name', '')
        
        # Create dynamic prompt based on lead status
        if lead_status == "yes":
            status_context = "This is a QUALIFIED LEAD who meets our criteria"
            tone_instruction = "excited, welcoming, and professional"
            action_needed = "next steps for onboarding and immediate contact"
        elif lead_status == "maybe":
            status_context = "This is a POTENTIAL LEAD who needs follow-up"
            tone_instruction = "encouraging, helpful, and patient"
            action_needed = "follow-up timeline and additional information gathering"
        else:  # "no"
            status_context = "This lead does not meet our current criteria"
            tone_instruction = "gracious, helpful, and maintaining goodwill"
            action_needed = "alternative recommendations or future contact options"
        
        prompt = f"""You are writing a personalized completion message for {business_name}.

BUSINESS CONTEXT:
- Business Name: {business_name}
- Owner: {owner_name}
- Background: {business_background}
- Goals: {business_goals}

LEAD STATUS: {status_context}
USER INFO:
- Greeting: {greeting}
- Subject: {subject_info}
- Name: {user_name}

REQUIREMENTS:
1. Write a completion message that is {tone_instruction}
2. Incorporate the business's personality and values
3. Reference the subject ({subject_info}) naturally
4. Include {action_needed}
5. Keep it conversational and authentic to {business_name}
6. Include 2-4 relevant emojis that fit the business tone

Generate:
1. A completion message (2-4 sentences)
2. 3 specific next steps as a bulleted list

Format your response as:
COMPLETION_MESSAGE:
[your message here]

NEXT_STEPS:
- [step 1]
- [step 2] 
- [step 3]"""

        response = chat_model.invoke([{"role": "user", "content": prompt}])
        content = response.content.strip()
        
        # Parse the LLM response
        if "COMPLETION_MESSAGE:" in content and "NEXT_STEPS:" in content:
            parts = content.split("NEXT_STEPS:")
            completion_message = parts[0].replace("COMPLETION_MESSAGE:", "").strip()
            next_steps_text = parts[1].strip()
            
            # Parse next steps
            next_steps = []
            for line in next_steps_text.split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    next_steps.append(line[2:])
                elif line.startswith('• '):
                    next_steps.append(line[2:])
                elif line and not line.startswith('['):
                    next_steps.append(line)
            
            return {
                'completion_message': completion_message,
                'next_steps': next_steps[:3]  # Limit to 3 steps
            }
        
        # Fallback parsing if format is different
        lines = content.split('\n')
        completion_message = content
        return {
            'completion_message': completion_message,
            'next_steps': [f"We'll follow up with you about next steps regarding {subject_info}"]
        }
        
    except Exception as e:
        print(f"Error generating completion message with LLM: {e}")
        # Fallback to simple template
        return _fallback_completion_message(lead_status, personalization, business_name, owner_name)


def _fallback_completion_message(lead_status: str, personalization: Dict[str, str], business_name: str, owner_name: str) -> Dict[str, Any]:
    """Fallback completion message if LLM generation fails."""
    greeting = personalization['greeting']
    subject_info = personalization['subject_info']
    
    if lead_status == "yes":
        message = f"{greeting} Great news! {business_name} would love to work with you regarding {subject_info}. {owner_name} will be in touch within 24 hours."
        steps = ["Expect contact within 24 hours", "Prepare any questions", "Get ready for next steps"]
    elif lead_status == "maybe":
        message = f"{greeting} Thank you for your interest! {owner_name} will review your information and follow up within 48 hours about {subject_info}."
        steps = ["Expect follow-up within 48 hours", "Consider additional details to share", "Review our services"]
    else:
        message = f"{greeting} Thank you for your time! While {subject_info} may not be the right fit right now, we appreciate your interest in {business_name}."
        steps = ["Consider alternative options", "Check back if needs change", "Thank you for your interest"]
    
    return {
        'completion_message': message,
        'next_steps': steps
    }