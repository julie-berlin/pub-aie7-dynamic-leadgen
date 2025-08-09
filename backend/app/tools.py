"""Toolbelt assembly for agents.

Collects third-party tools and local tools (like RAG) into a single list that
graphs can bind to their language models.
"""
from __future__ import annotations
from typing import List, Dict, Any, Optional
import os
import json
from pathlib import Path
from langchain_tavily import TavilySearch
from langchain.tools import tool
from .database import db

# Survey-specific tools for LangGraph nodes

@tool
def load_questions(form_id: str = "dogwalk_demo_form") -> str:
    """Load questions from JSON file based on form_id.
    
    Args:
        form_id: Form configuration identifier
        
    Returns:
        JSON string of questions array
    """
    try:
        # For now, use the dogwalk demo data
        questions_file = Path("data/input/dogwalk_34397/questions.json")
        with open(questions_file, 'r') as f:
            data = json.load(f)
        return json.dumps(data['questions'])
    except Exception as e:
        return json.dumps([])

@tool 
def load_client_info(form_id: str = "dogwalk_demo_form") -> str:
    """Load client information based on form_id.
    
    Args:
        form_id: Form configuration identifier
        
    Returns:
        JSON string of client information
    """
    try:
        # For now, use the dogwalk demo data
        client_file = Path("data/input/dogwalk_34397/client.json")
        with open(client_file, 'r') as f:
            data = json.load(f)
        return json.dumps(data['client'])
    except Exception as e:
        return json.dumps({})

@tool
def save_responses(session_id: str, responses_data: str) -> str:
    """Save user responses to database.
    
    Args:
        session_id: Session identifier
        responses_data: JSON string of response data array
        
    Returns:
        JSON string with success status
    """
    try:
        responses = json.loads(responses_data)
        results = []
        for response in responses:
            result = db.create_response(response)
            results.append(result)
        return json.dumps({"success": True, "count": len(results)})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def update_session(session_id: str, updates_data: str) -> str:
    """Update session data in database.
    
    Args:
        session_id: Session identifier  
        updates_data: JSON string of update fields
        
    Returns:
        JSON string with success status
    """
    try:
        updates = json.loads(updates_data)
        result = db.update_lead_session(session_id, updates)
        return json.dumps({"success": True, "result": result})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def finalize_session(session_id: str, final_data: str) -> str:
    """Finalize session with completion data.
    
    Args:
        session_id: Session identifier
        final_data: JSON string of final session data
        
    Returns:
        JSON string with success status
    """
    try:
        final_updates = json.loads(final_data)
        # Update session as completed
        final_updates["completed"] = True
        result = db.update_lead_session(session_id, final_updates)
        return json.dumps({"success": True, "result": result})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def create_session(session_data: str) -> str:
    """Create new lead session in database.
    
    Args:
        session_data: JSON string of session data
        
    Returns:
        JSON string with session creation result
    """
    try:
        data = json.loads(session_data)
        result = db.create_lead_session(data)
        return json.dumps({"success": True, "session": result})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def validate_responses(responses_data: str, questions_data: str) -> str:
    """Validate user responses against question requirements.
    
    Args:
        responses_data: JSON string of user responses
        questions_data: JSON string of question definitions
        
    Returns:
        JSON string with validation results
    """
    try:
        responses = json.loads(responses_data)
        questions = json.loads(questions_data)
        
        # Create question lookup
        question_map = {q['id']: q for q in questions}
        
        validation_results = []
        for response in responses:
            question_id = response.get('question_id')
            question = question_map.get(question_id)
            
            if not question:
                validation_results.append({
                    "question_id": question_id,
                    "valid": False,
                    "error": "Question not found"
                })
                continue
                
            # Basic validation - can be extended
            is_required = question.get('is_required', False)
            answer = response.get('answer', '').strip()
            
            if is_required and not answer:
                validation_results.append({
                    "question_id": question_id,
                    "valid": False,
                    "error": "Required question not answered"
                })
            else:
                validation_results.append({
                    "question_id": question_id,
                    "valid": True
                })
        
        all_valid = all(r["valid"] for r in validation_results)
        return json.dumps({
            "all_valid": all_valid,
            "results": validation_results
        })
    except Exception as e:
        return json.dumps({
            "all_valid": False,
            "error": str(e)
        })


def get_tool_belt() -> List:
    """Return the list of tools available to agents and LangGraph nodes."""
    tools = []
    
    # Add survey-specific tools
    survey_tools = [
        load_questions,
        load_client_info,
        save_responses,
        update_session,
        finalize_session,
        create_session,
        validate_responses
    ]
    tools.extend(survey_tools)
    
    # Add Tavily search tool if configured
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if tavily_api_key:
        tavily_tool = TavilySearch(
            tavily_api_key=tavily_api_key,
            max_results=5,  # Hard-coded default
            search_depth="basic",  # Hard-coded default
            include_domains=["akc.org", "breedmap.com"]  # Hard-coded defaults
        )
        tools.append(tavily_tool)
    
    # google_maps_tool = TODO
    
    return tools
