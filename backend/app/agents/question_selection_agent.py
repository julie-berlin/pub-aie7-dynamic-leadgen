"""
Question Selection Agent

Intelligently selects 1-3 logically related questions for each form step,
avoiding repetition and following business rules.
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
def select_questions_tool(
    available_questions: str,
    asked_question_ids: str,
    step_number: str,
    total_responses: str,
    client_context: str
) -> str:
    """
    Select 1-3 logically related questions for the next form step.
    
    Args:
        available_questions: JSON string of all questions
        asked_question_ids: JSON string of already asked question IDs
        step_number: Current step number
        total_responses: Number of responses collected so far
        client_context: Business context information
    
    Returns:
        JSON string of selected question IDs
    """
    try:
        questions = json.loads(available_questions)
        asked_ids = json.loads(asked_question_ids)
        step = int(step_number)
        response_count = int(total_responses)
        
        # Filter available questions
        available = [q for q in questions if q['id'] not in asked_ids]
        
        if not available:
            return json.dumps([])
        
        # Business rules for selection
        tough_questions = [q for q in available
                          if 'dangerous' in q.get('scoring_rubric', '').lower()
                          or 'must be' in q.get('scoring_rubric', '').lower()
                          or 'required' in q.get('scoring_rubric', '').lower()]
        
        easy_questions = [q for q in available if q not in tough_questions]
        
        # Select based on step and response count
        if step < 2 or response_count < 4:
            # Early steps - use easy questions
            candidates = easy_questions if easy_questions else available
        else:
            # Can now ask tough questions
            candidates = available
        
        # Group related questions
        contact_questions = [q for q in candidates
                           if any(word in q['question'].lower()
                                 for word in ['name', 'phone', 'email', 'contact'])]
        
        dog_questions = [q for q in candidates
                        if any(word in q['question'].lower()
                              for word in ['dog', 'breed', 'walk', 'vaccination'])]
        
        service_questions = [q for q in candidates
                           if any(word in q['question'].lower()
                                 for word in ['times', 'frequency', 'benefit', 'training'])]
        
        # Select 1-3 questions from same category when possible
        selected = []
        if contact_questions and response_count >= 3:
            selected = contact_questions[:2]
        elif dog_questions:
            selected = dog_questions[:2]
        elif service_questions:
            selected = service_questions[:2]
        else:
            selected = candidates[:2]
        
        # Ensure we don't exceed 3 questions and have at least 1
        selected = selected[:3]
        if not selected and candidates:
            selected = [candidates[0]]
        
        return json.dumps([q['id'] for q in selected])
        
    except Exception as e:
        print(f"Error in question selection: {e}")
        return json.dumps([])

def create_question_selection_agent():
    """Create the question selection agent"""
    
    system_prompt = """You are a Question Selection Agent for a dynamic lead generation form.

Your specialty is intelligently selecting 1-3 logically related questions for each form step.

Key responsibilities:
- Select questions that haven't been asked yet
- Group related questions together (contact info, dog details, service preferences)
- Avoid tough qualifying questions in early steps (first 4 responses)
- Ensure maximum 3 questions per step
- Prioritize user experience and flow

Business rules:
- Early steps (steps 1-2): Use easy, engaging questions
- Before 4 responses: Avoid "dangerous" or "required" qualifying questions
- After 4 responses: Can include tough qualifying questions
- Group contact info questions together later in the flow
- Always select at least 1 question if any are available

Use the select_questions_tool to make your selections based on the current form state."""

    llm = create_llm(temperature=0.3)  # Lower temperature for consistent selection
    tools = [select_questions_tool]
    
    return create_agent(llm, tools, system_prompt)

def invoke_question_selection(state: Dict[str, Any]) -> List[int]:
    """
    Invoke the question selection agent with form state
    
    Args:
        state: Current form state with questions, responses, etc.
    
    Returns:
        List of selected question IDs
    """
    agent = create_question_selection_agent()
    
    # Prepare input for the agent
    messages = [
        HumanMessage(content=f"""
Please select questions for the next form step.

Available questions: {json.dumps(state.get('all_questions', []))}
Already asked question IDs: {json.dumps(state.get('asked_questions', []))}
Current step number: {state.get('step', 0) + 1}
Total responses so far: {len(state.get('responses', []))}
Client context: Dynamic lead generation form
        """)
    ]
    
    try:
        result = agent.invoke({"messages": messages})
        
        # Extract question IDs from the result
        if 'output' in result:
            selected_ids = json.loads(result['output'])
            return selected_ids
        else:
            print("No output from question selection agent")
            return []
            
    except Exception as e:
        print(f"Error invoking question selection agent: {e}")
        return []

if __name__ == "__main__":
    # Test the agent
    test_state = {
        'all_questions': [
            {'id': 1, 'question': 'What is your location?', 'scoring_rubric': 'Basic question'},
            {'id': 2, 'question': 'What is your dog breed?', 'scoring_rubric': 'Basic question'},
            {'id': 5, 'question': 'Is your dog vaccinated?', 'scoring_rubric': 'Required - must be vaccinated'}
        ],
        'asked_questions': [],
        'step': 0,
        'responses': []
    }
    
    selected = invoke_question_selection(test_state)
    print(f"Selected question IDs: {selected}")