# Survey System LangGraph Architecture Diagram

## Current Implementation: `survey_graph_v2.py`

### Visual Flow Diagram

```
                                     ╔════════════════════════════════════════╗
                                     ║              API ENTRY POINTS          ║
                                     ╠════════════════════════════════════════╣
                                     ║  1. POST /api/survey/start             ║
                                     ║  2. POST /api/survey/step              ║
                                     ║  3. Timeout/Cron Jobs                  ║
                                     ╚════════════════════════════════════════╝
                                                         │
                                                         ▼
                              ╔═══════════════════════════════════════════════════╗
                              ║                 ENTRY POINT 1                     ║
                              ║          🚀 INITIALIZE_WITH_TRACKING              ║
                              ║                                                   ║
                              ║ • Create session ID                               ║
                              ║ • Capture UTM parameters                          ║
                              ║ • Save tracking data (fire-and-forget)            ║
                              ║ • Initialize all state sections                   ║
                              ╚═══════════════════════════════════════════════════╝
                                                         │
                                                         ▼
                              ╔═══════════════════════════════════════════════════╗
                              ║              🎯 QUESTION_SELECTION                ║
                              ║                                                   ║
                              ║ • Load questions from cache/database              ║
                              ║ • Apply business rules (required, asked)          ║
                              ║ • Select 1-3 logically related questions          ║
                              ║ • Update asked_questions history                  ║
                              ╚═══════════════════════════════════════════════════╝
                                                         │
                                                         ▼
                              ╔═══════════════════════════════════════════════════╗
                              ║              ✍️  QUESTION_PHRASING                ║
                              ║                                                   ║
                              ║ • Load client info from cache                     ║
                              ║ • Use LLM to adapt question tone                  ║
                              ║ • Apply business branding/context                 ║
                              ║ • Generate engaging question variants             ║
                              ╚═══════════════════════════════════════════════════╝
                                                         │
                                                         ▼
                              ╔═══════════════════════════════════════════════════╗
                              ║            📋 PREPARE_STEP_FOR_FRONTEND           ║
                              ║                                                   ║
                              ║ • Format questions for API response               ║
                              ║ • Add progress indicators                         ║
                              ║ • Include engagement headline/motivation          ║
                              ║ • Structure data for frontend consumption         ║
                              ╚═══════════════════════════════════════════════════╝
                                                         │
                                                         ▼
                              ╔═══════════════════════════════════════════════════╗
                              ║              🤔 SHOULD_WAIT_OR_CONTINUE           ║
                              ║                 (Conditional Router)              ║
                              ╚═══════════════════════════════════════════════════╝
                                        │               │                     │
                                       END         continue_flow      process_responses
                                 (Wait for User)        │                     │
                                        │               ▼                     ▼
                                        │    ┌──────────────────────┐         │
                                        │    │  Loop back to        │         │
                                        │    │  QUESTION_SELECTION  │         │
                                        │    └──────────────────────┘         │
                                        │                                     │
                ╔═══════════════════════════════════════════════════════════════════════════════╗
                ║                              ENTRY POINT 2                                    ║
                ║                           💬 PROCESS_RESPONSES                                ║
                ║                                                                               ║
                ║ • Accept pending responses from API                                           ║
                ║ • Add timestamps to each response                                             ║
                ║ • Merge with existing responses in state                                      ║
                ║ • Reset abandonment risk after activity                                       ║
                ╚═══════════════════════════════════════════════════════════════════════════════╝
                                                         │
                                                         ▼
                ╔═══════════════════════════════════════════════════════════════════════════════╗
                ║                        💾 SAVE_RESPONSES_IMMEDIATELY                          ║
                ║                                                                               ║
                ║ • Filter new responses (by timestamp)                                         ║
                ║ • Save to database (fire-and-forget batch operation)                          ║
                ║ • Non-blocking operation for performance                                      ║
                ║ • Error handling doesn't fail the flow                                        ║
                ╚═══════════════════════════════════════════════════════════════════════════════╝
                                                         │
                                                         ▼
                ╔═══════════════════════════════════════════════════════════════════════════════╗
                ║                     🎯 SHOULD_CONTINUE_OR_COMPLETE                            ║
                ║                        (Conditional Router)                                   ║
                ╚═══════════════════════════════════════════════════════════════════════════════╝
                                       │                               │
                                   continue                        complete
                           (Back to QUESTION_SELECTION)                │
                                                                       ▼
                               ╔═══════════════════════════════════════════════════╗
                               ║              🛤️  ROUTE_TO_COMPLETION              ║
                               ║                 (Pass-through Node)               ║
                               ╚═══════════════════════════════════════════════════╝
                                                         │
                                                         ▼
                               ╔═══════════════════════════════════════════════════╗
                               ║              📊 ROUTE_COMPLETION_TYPE             ║
                               ║                (Conditional Router)               ║
                               ╚═══════════════════════════════════════════════════╝
                          │                        │                              │
                 qualified_completion    unqualified_completion        abandoned_completion
                          │                        │                              │
                          ▼                        ▼                              ▼
    ╔═══════════════════════════╗    ╔═══════════════════════════╗    ╔═══════════════════════════╗
    ║  ✅ QUALIFIED_MESSAGE     ║    ║ ❌ UNQUALIFIED_COMPLETION ║    ║ 🚪 MARK_ABANDONED         ║
    ║      _GENERATION          ║    ║                           ║    ║                           ║
    ║                           ║    ║ • Simple completion       ║    ║ • Set completion_type     ║
    ║ • Generate personalized   ║    ║ • No LLM usage            ║    ║ • Set abandonment_status  ║
    ║   completion message      ║    ║ • Mark as complete        ║    ║ • Set abandonment_risk    ║
    ║ • Use lead intelligence   ║    ║ • Generic message         ║    ║ • Mark as completed       ║
    ║ • Include call-to-action  ║    ╚═══════════════════════════╝    ╚═══════════════════════════╝
    ╚═══════════════════════════╝                    │                              │
                  │                                  │                              │
                  │                                  ▼                              │
                  │                                 END                             │
                  │                                                                 │
                  ▼                                                                 │
                 END ◄──────────────────────────────────────────────────────────────┘


                ╔═══════════════════════════════════════════════════════════════════════════════╗
                ║                              ENTRY POINT 3                                    ║
                ║                         ⏰ CHECK_ABANDONMENT                                  ║
                ║                                                                               ║
                ║ • Calculate time since last activity                                          ║
                ║ • Set abandonment risk levels based on inactivity                             ║
                ║ • Mark session as abandoned if threshold exceeded                             ║
                ╚═══════════════════════════════════════════════════════════════════════════════╝
                                                         │
                                                         ▼
                ╔═══════════════════════════════════════════════════════════════════════════════╗
                ║                           🔍 IS_ABANDONED                                     ║
                ║                        (Conditional Router)                                   ║
                ╚═══════════════════════════════════════════════════════════════════════════════╝
                                       │                               │
                                   abandoned                        active
                                       │                               │
                                       ▼                               ▼
                         (Route to MARK_ABANDONED)                    END
```

## Node Responsibilities

### 🚀 **initialize_with_tracking_node**
**Purpose**: Session initialization with UTM tracking
**Operations**:
- Generate unique session ID
- Capture and save UTM parameters (fire-and-forget)
- Extract headers (referrer, user-agent, IP)
- Initialize hierarchical state structure

### 🎯 **question_selection_node**
**Purpose**: Intelligent question selection with business rules
**Operations**:
- Load questions from cache/database
- Filter by asked questions and business rules
- Select 1-3 logically related questions
- Apply categorization (required, optional, follow-up)

### ✍️ **question_phrasing_node**
**Purpose**: LLM-powered question adaptation
**Operations**:
- Load cached client info for business context
- Use LLM to rephrase questions for tone/brand
- Ensure questions are engaging and clear
- Maintain question IDs and metadata

### 📋 **prepare_step_for_frontend_node**
**Purpose**: API response formatting
**Operations**:
- Structure questions for frontend consumption
- Add progress indicators and step information
- Include engagement content (headlines, motivation)
- Format for survey_api.py response

### 💬 **process_user_responses_node**
**Purpose**: Response processing and validation
**Operations**:
- Accept pending responses from API
- Add timestamps and metadata
- Merge with existing responses in state
- Reset abandonment risk after user activity

### 💾 **save_responses_immediately_node**
**Purpose**: Fire-and-forget response persistence
**Operations**:
- Filter new responses by timestamp
- Use batched database operations (non-blocking)
- Error handling that doesn't fail the flow
- Performance optimized for real-time surveys

### ⏰ **check_abandonment_node**
**Purpose**: Abandonment detection and risk assessment
**Operations**:
- Calculate inactivity time since last response
- Set risk levels (active, at_risk, high_risk, abandoned)
- Configurable thresholds for different risk levels

### ✅ **qualified_message_generation_node**
**Purpose**: Personalized completion for qualified leads
**Operations**:
- Generate personalized completion messages
- Use lead intelligence and response history
- Include next steps and call-to-action
- Tailored messaging based on qualification level

### ❌ **unqualified_completion_node**
**Purpose**: Simple completion without personalization
**Operations**:
- Generic completion message
- No LLM usage for efficiency
- Mark session as complete with reason
- Minimal processing for unqualified leads

## State Management

### **SurveyGraphState Structure**
```python
{
    'core': {
        'session_id': str,
        'form_id': str,
        'client_id': str,
        'step': int,
        'completed': bool,
        'completion_type': str,
        'last_updated': str
    },
    'master_flow': {
        'flow_phase': str,
        'flow_strategy': str,
        'completion_probability': float
    },
    'question_strategy': {
        'all_questions': List[Dict],
        'asked_questions': List[int],
        'current_questions': List[Dict],
        'phrased_questions': List[str]
    },
    'lead_intelligence': {
        'responses': List[Dict],
        'current_score': float,
        'lead_status': str,
        'scoring_history': List[Dict]
    },
    'engagement': {
        'last_activity_timestamp': str,
        'abandonment_status': str,
        'abandonment_risk': float
    },
    'frontend_response': {
        'session_id': str,
        'questions': List[Dict],
        'headline': str,
        'motivation': str,
        'step': int,
        'completed': bool,
        'completion_message': str
    }
}
```

## Routing Logic

### **should_wait_or_continue**
- `END`: No pending responses, wait for user input
- `"process_responses"`: Has pending responses to process
- `"continue_flow"`: Continue to next question set

### **should_continue_or_complete**
- `"continue"`: More questions needed, loop back to question selection
- `"complete"`: Survey ready for completion, route to completion flow

### **route_completion_type**
- `"qualified_completion"`: Lead status 'yes' or 'maybe'
- `"unqualified_completion"`: Lead status 'no'
- `"abandoned_completion"`: Abandonment detected

### **is_abandoned**
- `"abandoned"`: Inactivity threshold exceeded
- `"active"`: Still within activity window

## Performance Optimizations

### **Fire-and-Forget Operations**
- ✅ Tracking data saves (non-blocking)
- ✅ Response batch processing (non-blocking)
- ✅ Session state updates (non-blocking)

### **Caching Layer**
- ✅ Questions cache (30-minute TTL)
- ✅ Client info cache (1-hour TTL)
- ✅ Form config cache (30-minute TTL)

### **Database Optimizations**
- ✅ Connection pooling (15 max connections)
- ✅ Batch operations (25 operations per batch)
- ✅ Performance monitoring with alerts

## API Integration Points

### **POST /api/survey/start**
**Flow**: `initialize_with_tracking` → `question_selection` → `question_phrasing` → `prepare_step_for_frontend` → `END`
**Returns**: First questions with engagement content

### **POST /api/survey/step**
**Flow**: `process_responses` → `save_responses_immediately` → `question_selection` (loop) OR completion flow
**Returns**: Next questions OR completion message

### **Timeout/Abandonment Jobs**
**Flow**: `check_abandonment` → `mark_abandoned` OR `END`
**Purpose**: Detect and handle session abandonment

## Error Handling & Resilience

- **Non-blocking persistence**: Database operations don't fail the graph
- **Graceful degradation**: Cache misses fall back to database
- **Error recovery**: Individual node failures are logged but contained
- **State consistency**: Core state always maintained even on partial failures

---

*Generated: January 9, 2025*
*Graph Version: survey_graph_v2.py*
*Status: Phases 1-11 Complete, Optimized for Production*
