"""
LLM Utilities for Simple Node Operations

Simple LLM functions for nodes that need AI but don't require full agent capabilities.
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

class LLMUtils:
    """Simple LLM utilities for node operations"""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = model
    
    def rephrase_questions(self, questions: List[Dict[str, Any]], client_info: Dict[str, Any]) -> List[str]:
        """
        Simple LLM call to rephrase questions for business context
        
        Args:
            questions: List of question objects
            client_info: Business information for context
            
        Returns:
            List of rephrased question strings
        """
        if not questions:
            return []
        
        business_name = client_info.get('information', {}).get('name', 'Our Business')
        business_type = client_info.get('information', {}).get('business_type', 'service provider')
        
        # Create simple prompt
        questions_text = "\n".join([f"{i+1}. {q['question']}" for i, q in enumerate(questions)])
        
        prompt = f"""Rephrase these form questions for {business_name}, a {business_type}.

Make them:
- Friendly and conversational 
- Use "you" and "your"
- Appropriate for {business_name}'s brand
- Clear and engaging

Original questions:
{questions_text}

Return only the rephrased questions, one per line, no numbers."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You rephrase form questions to be friendly and engaging."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            phrased_questions = response.choices[0].message.content.strip().split('\n')
            
            # Ensure we have the same number of questions
            if len(phrased_questions) != len(questions):
                print(f"⚠️ Question count mismatch. Using original questions.")
                return [q['question'] for q in questions]
            
            return [q.strip() for q in phrased_questions if q.strip()]
            
        except Exception as e:
            print(f"❌ Question phrasing failed: {e}")
            # Fallback to original questions
            return [q['question'] for q in questions]

# Create global instance
llm_utils = LLMUtils()

def rephrase_questions_simple(questions: List[Dict[str, Any]], client_info: Dict[str, Any]) -> List[str]:
    """Simple function for question rephrasing node"""
    return llm_utils.rephrase_questions(questions, client_info)