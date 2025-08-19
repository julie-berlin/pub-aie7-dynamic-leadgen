"""LangGraph Studio compatible graph with absolute imports."""

import sys
import os
from typing import Dict, Any

# Add the backend directory to the path for absolute imports
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

try:
    # Try to import the actual simplified survey graph
    from app.graphs.simplified_survey_graph import simplified_survey_graph as graph
    print("✅ Successfully imported simplified_survey_graph")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Creating fallback dummy graph for LangGraph Studio...")
    
    # Fallback - create a simple dummy graph for development
    from langgraph.graph import StateGraph, END
    
    def dummy_node(state: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "message": "Dummy node for LangGraph Studio development",
            "frontend_response": {
                "session_id": "demo-session",
                "step": 1,
                "questions": [
                    {
                        "id": 1,
                        "text": "This is a demo question for LangGraph Studio",
                        "type": "text",
                        "required": False
                    }
                ],
                "headline": "Demo Survey Step",
                "motivation": "This is a fallback demo for development"
            }
        }
    
    # Create a minimal graph for development
    dummy_graph = StateGraph(dict)
    dummy_graph.add_node("demo_step", dummy_node)
    dummy_graph.set_entry_point("demo_step")
    dummy_graph.add_edge("demo_step", END)
    
    graph = dummy_graph.compile()

# Make sure the graph is exported as 'graph' for LangGraph Studio
__all__ = ['graph']