"""
LangSmith Tracing Configuration for LangGraph Operations

Integrates LangSmith tracing with our survey graph to provide:
- Graph execution tracing and performance monitoring
- LLM call tracking and token usage monitoring
- Node-level performance metrics
- Error tracking and debugging support
"""

import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from functools import wraps
import time

from langsmith import Client
from langchain_core.tracers import BaseTracer
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.messages import BaseMessage

class SurveyGraphTracer:
    """LangSmith tracer specifically configured for survey graph operations"""
    
    def __init__(self):
        self.client = None
        self.enabled = self._setup_langsmith()
        
    def _setup_langsmith(self) -> bool:
        """Configure LangSmith client if environment variables are present"""
        api_key = os.getenv('LANGSMITH_API_KEY')
        project_name = os.getenv('LANGSMITH_PROJECT', 'survey-system')
        
        if not api_key:
            print("⚠️  LangSmith API key not found - tracing disabled")
            return False
            
        try:
            # Set environment variables for LangChain integration
            os.environ['LANGCHAIN_TRACING_V2'] = 'true'
            os.environ['LANGCHAIN_API_KEY'] = api_key
            os.environ['LANGCHAIN_PROJECT'] = project_name
            
            # Initialize LangSmith client
            self.client = Client(api_key=api_key)
            
            print(f"✅ LangSmith tracing enabled for project: {project_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup LangSmith: {e}")
            return False
    
    def trace_survey_session(
        self,
        session_id: str,
        form_id: str,
        operation_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Create a trace context for survey operations"""
        if not self.enabled:
            return SurveyTraceContext(None, session_id, form_id, operation_name)
            
        trace_metadata = {
            "session_id": session_id,
            "form_id": form_id,
            "operation": operation_name,
            "timestamp": datetime.utcnow().isoformat(),
            **(metadata or {})
        }
        
        return SurveyTraceContext(self.client, session_id, form_id, operation_name, trace_metadata)

class SurveyTraceContext:
    """Context manager for tracing survey operations"""
    
    def __init__(
        self,
        client: Optional[Client],
        session_id: str,
        form_id: str,
        operation_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.client = client
        self.session_id = session_id
        self.form_id = form_id
        self.operation_name = operation_name
        self.metadata = metadata or {}
        self.start_time = None
        self.run_id = None
        
    def __enter__(self):
        if self.client:
            self.start_time = time.time()
            # Create trace run
            try:
                from langsmith import trace
                self._trace_decorator = trace(
                    name=self.operation_name,
                    metadata=self.metadata
                )
            except ImportError:
                pass
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client and self.start_time:
            duration = (time.time() - self.start_time) * 1000
            
            # Log completion metrics
            completion_metadata = {
                **self.metadata,
                "duration_ms": duration,
                "success": exc_type is None
            }
            
            if exc_type:
                completion_metadata["error"] = {
                    "type": exc_type.__name__,
                    "message": str(exc_val)
                }
    
    def add_metadata(self, **kwargs):
        """Add metadata to the current trace"""
        self.metadata.update(kwargs)
        
    def log_node_execution(self, node_name: str, input_data: Any, output_data: Any, duration_ms: float):
        """Log individual node execution within the trace"""
        if self.client:
            node_metadata = {
                "node_name": node_name,
                "session_id": self.session_id,
                "duration_ms": duration_ms,
                "input_size": len(str(input_data)) if input_data else 0,
                "output_size": len(str(output_data)) if output_data else 0
            }
            
            # Could log to LangSmith as child run if needed
            print(f"🔍 Node {node_name} executed in {duration_ms:.2f}ms")

class SurveyLLMCallbackHandler(BaseCallbackHandler):
    """Callback handler to track LLM operations with additional survey context"""
    
    def __init__(self, session_id: str, form_id: str):
        super().__init__()
        self.session_id = session_id
        self.form_id = form_id
        self.llm_calls = []
    
    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        **kwargs: Any,
    ) -> None:
        """Track LLM call start"""
        call_info = {
            "session_id": self.session_id,
            "form_id": self.form_id,
            "model": serialized.get("name", "unknown"),
            "prompt_count": len(prompts),
            "prompt_tokens": sum(len(p.split()) for p in prompts),  # Rough estimate
            "start_time": time.time()
        }
        self.llm_calls.append(call_info)
    
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Track LLM call completion"""
        if self.llm_calls:
            call_info = self.llm_calls[-1]
            duration = (time.time() - call_info["start_time"]) * 1000
            
            # Estimate completion tokens
            total_completion_tokens = 0
            if response.generations:
                for generation_list in response.generations:
                    for generation in generation_list:
                        total_completion_tokens += len(generation.text.split())
            
            call_info.update({
                "duration_ms": duration,
                "completion_tokens": total_completion_tokens,
                "total_generations": len(response.generations) if response.generations else 0,
                "success": True
            })
            
            print(f"🤖 LLM call completed in {duration:.2f}ms - {call_info['completion_tokens']} tokens")
    
    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        """Track LLM call errors"""
        if self.llm_calls:
            call_info = self.llm_calls[-1]
            duration = (time.time() - call_info["start_time"]) * 1000
            
            call_info.update({
                "duration_ms": duration,
                "success": False,
                "error": str(error)
            })
            
            print(f"❌ LLM call failed after {duration:.2f}ms: {error}")

# Decorators for tracing graph operations

def trace_graph_operation(operation_name: str):
    """Decorator to trace graph operations with LangSmith"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract session and form info from args/kwargs
            session_id = kwargs.get('session_id')
            form_id = kwargs.get('form_id')
            
            # Try to extract from state if available
            if not session_id and args:
                state = args[0] if args else {}
                if isinstance(state, dict):
                    session_id = state.get('session_id')
                    form_id = state.get('form_id')
            
            # Use tracer if we have session info
            if session_id:
                with tracer.trace_survey_session(
                    session_id=session_id,
                    form_id=form_id or 'unknown',
                    operation_name=operation_name,
                    metadata={"function": func.__name__}
                ) as trace_ctx:
                    start_time = time.time()
                    try:
                        result = func(*args, **kwargs)
                        duration_ms = (time.time() - start_time) * 1000
                        trace_ctx.add_metadata(duration_ms=duration_ms, success=True)
                        return result
                    except Exception as e:
                        duration_ms = (time.time() - start_time) * 1000
                        trace_ctx.add_metadata(duration_ms=duration_ms, success=False, error=str(e))
                        raise
            else:
                # Execute without tracing if no session context
                return func(*args, **kwargs)
                
        return wrapper
    return decorator

def trace_node_execution(node_name: str):
    """Decorator specifically for LangGraph nodes"""
    return trace_graph_operation(f"node_{node_name}")

def trace_supervisor_execution(supervisor_name: str):
    """Decorator for supervisor operations"""
    return trace_graph_operation(f"supervisor_{supervisor_name}")

# Performance monitoring helpers

class GraphPerformanceMonitor:
    """Monitor graph execution performance and identify bottlenecks"""
    
    def __init__(self):
        self.execution_times = {}
        self.node_call_counts = {}
        
    def record_node_execution(self, node_name: str, duration_ms: float, session_id: str):
        """Record node execution time for analysis"""
        if node_name not in self.execution_times:
            self.execution_times[node_name] = []
            self.node_call_counts[node_name] = 0
            
        self.execution_times[node_name].append(duration_ms)
        self.node_call_counts[node_name] += 1
        
        # Log slow operations
        if duration_ms > 5000:  # 5 seconds
            print(f"⚠️  Slow node execution: {node_name} took {duration_ms:.2f}ms in session {session_id}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for monitoring dashboard"""
        summary = {}
        
        for node_name, times in self.execution_times.items():
            if times:
                summary[node_name] = {
                    "call_count": len(times),
                    "avg_duration_ms": sum(times) / len(times),
                    "max_duration_ms": max(times),
                    "min_duration_ms": min(times),
                    "total_duration_ms": sum(times)
                }
        
        return summary
    
    def identify_bottlenecks(self, threshold_ms: float = 2000) -> List[str]:
        """Identify nodes that are consistently slow"""
        slow_nodes = []
        
        for node_name, times in self.execution_times.items():
            if times:
                avg_time = sum(times) / len(times)
                if avg_time > threshold_ms:
                    slow_nodes.append(f"{node_name}: {avg_time:.2f}ms avg")
        
        return slow_nodes

# Global instances
tracer = SurveyGraphTracer()
performance_monitor = GraphPerformanceMonitor()

# Helper functions for common operations

def create_llm_callback_handler(session_id: str, form_id: str) -> SurveyLLMCallbackHandler:
    """Create LLM callback handler with survey context"""
    return SurveyLLMCallbackHandler(session_id, form_id)

def get_langchain_callbacks(session_id: str, form_id: str) -> List[BaseCallbackHandler]:
    """Get list of LangChain callbacks for tracing"""
    callbacks = []
    
    # Add LLM tracking callback
    callbacks.append(create_llm_callback_handler(session_id, form_id))
    
    return callbacks

def setup_graph_tracing():
    """Initialize tracing for the entire graph"""
    if tracer.enabled:
        print("✅ Graph tracing configured with LangSmith")
        return True
    else:
        print("⚠️  Graph tracing disabled - LangSmith not configured")
        return False

# Usage examples and documentation
LANGSMITH_SETUP_DOCS = """
# LangSmith Setup for Survey System

## Environment Variables
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=survey-system  # Optional, defaults to 'survey-system'

## Usage in Nodes

```python
from utils.langsmith_tracing import trace_node_execution, get_langchain_callbacks

@trace_node_execution("question_selection")
def question_selection_agent_node(state: SurveyGraphState) -> SurveyGraphState:
    session_id = state.core.session_id
    form_id = state.core.form_id
    
    # Get callbacks for LLM calls
    callbacks = get_langchain_callbacks(session_id, form_id)
    
    # Use callbacks in LLM chain
    result = llm_chain.invoke(
        {"input": "select questions"},
        config={"callbacks": callbacks}
    )
    
    return state
```

## Usage in API Endpoints

```python
from utils.langsmith_tracing import tracer

@app.post("/api/survey/start")
async def start_survey(request: StartSessionRequest):
    session_id = str(uuid.uuid4())
    
    with tracer.trace_survey_session(
        session_id=session_id,
        form_id=request.form_id,
        operation_name="start_session",
        metadata={"utm_source": request.utm_source}
    ):
        # Execute graph with tracing
        result = await survey_graph.ainvoke(initial_state)
        return result
```

## Performance Monitoring

```python
from utils.langsmith_tracing import performance_monitor

# Get performance summary
summary = performance_monitor.get_performance_summary()

# Identify bottlenecks
slow_nodes = performance_monitor.identify_bottlenecks(threshold_ms=1000)
print(f"Slow nodes: {slow_nodes}")
```
"""

# Export main components
__all__ = [
    'tracer',
    'performance_monitor',
    'trace_graph_operation',
    'trace_node_execution', 
    'trace_supervisor_execution',
    'get_langchain_callbacks',
    'setup_graph_tracing',
    'SurveyLLMCallbackHandler',
    'GraphPerformanceMonitor'
]