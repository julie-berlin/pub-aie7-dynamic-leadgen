# Dynamic Survey LangGraph Refactor Plan

## Overview
Complete refactor from agent-based flow to LangGraph orchestration. No backward compatibility required - clean slate approach.

## Phase 1: Foundation Setup

- [x] Create get_chat_model function in models.py
  - ✅ Added get_chat_model() function 
  - ✅ Renamed original models.py to py_models.py for Pydantic models

- [ ] Fix tools.py import issue
  - Remove settings import, use environment variables directly
  - Ensure tools.py can be imported without errors

- [ ] Extend state.py for survey-specific state
  - Add SurveyState class with all necessary fields from FlowEngine
  - Include: session_id, form_id, step, questions, responses, scores, lead_status, etc.
  - Use TypedDict and proper type annotations

- [ ] Update tools.py to include survey-specific tools
  - Add database tools: save_responses, update_session, finalize_session
  - Add question loading tools
  - Add scoring/validation tools

## Phase 2: Convert Agents to LangGraph Nodes

- [ ] Create app/graphs/nodes/ directory structure

- [ ] Convert question_selection_agent.py to question_selection_node.py
  - Extract logic from agent, create pure node function
  - Return state updates compatible with SurveyState
  - Remove AgentExecutor pattern completely

- [ ] Convert engagement_agent.py to engagement_node.py
  - Create node function for headline/motivation generation
  - Remove AgentExecutor pattern completely

- [ ] Convert lead_scoring_agent.py to lead_scoring_node.py
  - Create node function for score calculation
  - Remove AgentExecutor pattern completely

- [ ] Create question_phrasing_node.py
  - Extract phrasing logic from FlowEngine
  - Create node function with LLM integration

## Phase 3: Build Main Survey Graph

- [ ] Create app/graphs/survey_graph.py
  - Define complete survey orchestration graph
  - Implement flow: Question Selection → Phrasing → Engagement → Score → Continue/Complete

- [ ] Add conditional routing logic
  - should_continue function for completion criteria
  - Route between question flow and completion flow
  - Handle all business rules (min questions, scoring thresholds)

- [ ] Add database persistence nodes
  - save_responses_node
  - update_session_node  
  - save_completion_node

- [ ] Create completion flow nodes
  - message_generation_node
  - finalization_node

## Phase 4: Create New Flow Manager

- [ ] Create app/survey_flow_manager.py
  - Replace FlowEngine completely with LangGraph-based manager
  - Use compiled graph for all operations
  - New API interface - no compatibility needed

- [ ] Implement start_session method
  - Initialize SurveyState
  - Invoke graph with initial state
  - Return formatted response

- [ ] Implement advance_session_step method
  - Update state with responses
  - Continue graph execution
  - Handle completion routing

- [ ] Implement finalize_session method
  - Complete graph execution
  - Return completion data

## Phase 5: Update API Integration

- [ ] Completely rewrite app/routes/sessions.py
  - Use SurveyFlowManager instead of FlowEngine
  - Update all endpoint logic
  - Import py_models for Pydantic models

- [ ] Update app/main.py
  - Remove FlowEngine references
  - Update health checks if needed

## Phase 6: Complete Cleanup

- [ ] Delete old agent files
  - Delete entire app/agents/ directory
  - Delete app/flow_engine.py completely
  - Delete app/agent_factory.py

- [ ] Clean up imports throughout codebase
  - Remove all old agent imports
  - Update any remaining references

- [ ] Add comprehensive error handling
  - Graph-level error handling
  - Node-level fallbacks
  - Clean error responses for API

## Phase 7: Testing and Validation

- [ ] Create new test suite for LangGraph implementation
  - Test complete survey flow
  - Test state transitions
  - Test error conditions

- [ ] Performance testing
  - Verify new system performance
  - Test concurrent sessions

- [ ] Documentation updates
  - Update CLAUDE.md with new architecture
  - Document graph structure and nodes

## Implementation Notes

### File Organization (Final State)
- `app/models.py` - LangChain model utilities
- `app/py_models.py` - Pydantic models for API
- `app/state.py` - SurveyState definition
- `app/tools.py` - Survey-specific LangGraph tools
- `app/graphs/survey_graph.py` - Main graph definition
- `app/graphs/nodes/` - Individual node functions
- `app/survey_flow_manager.py` - Graph-based flow manager
- `app/routes/sessions.py` - Updated API routes

### Files to Delete
- `app/flow_engine.py` - Replace with survey_flow_manager.py
- `app/agent_factory.py` - No longer needed
- `app/agents/` - Entire directory, replaced with nodes/
- `app/llm_utils.py` - Move logic to nodes if needed

### State Management
- SurveyState as single source of truth
- Immutable state updates
- All nodes return proper state updates

### No Backward Compatibility
- Clean break from old system
- New API interface
- Fresh start with best practices