# LangGraph Implementation Architecture

This diagram represents the current simplified LangGraph implementation for the dynamic survey system.

```mermaid
graph TB
    Start([Start: User Session]) --> Init["initialize_session_with_tracking<br/>📊 LOGIC - Database ops + UTM tracking"]

    Init --> Route1{"Has Pending<br/>Responses?"}
    
    Route1 -->|Yes| LI["consolidated_lead_intelligence<br/>🤖 LLM AGENT - ALL lead processing"]
    Route1 -->|No| SA["consolidated_survey_admin<br/>🤖 LLM AGENT - ALL survey functions"]
    
    SA --> Route2{Admin Decision}
    Route2 -->|Questions Ready| WaitEnd[END - Wait for User Input]
    Route2 -->|Route to Intelligence| LI
    Route2 -->|Check Abandonment| Abandon["check_abandonment<br/>📊 LOGIC - Time-based detection"]
    Route2 -->|Complete| CompleteEnd[END - Survey Complete]
    
    LI --> Route3{Lead Status}
    Route3 -->|Continue Survey| SA
    Route3 -->|Complete - qualified/maybe/no| CompleteEnd
    
    Abandon --> AbandonEnd[END - Abandoned]
    
    WaitEnd -.->|User Submits Responses| NewReq["New API Request<br/>with Responses"]
    NewReq --> Init
    
    style Init fill:#e1f5fe
    style SA fill:#f3e5f5
    style LI fill:#e8f5e8
    style Abandon fill:#fff3e0
    style WaitEnd fill:#f5f5f5
    style CompleteEnd fill:#e8f5e8
    style AbandonEnd fill:#ffebee
    
    classDef logic fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef llm fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef endpoint fill:#f5f5f5,stroke:#424242,stroke-width:2px
```

## Architecture Overview

### Consolidated Supervisors Architecture

The system has been simplified from a complex multi-node architecture to a streamlined design with two main AI agents:

| Component | Type | Integrated Functions |
|-----------|------|---------------------|
| **initialize_session_with_tracking** | 📊 LOGIC | Database operations, UTM tracking, session setup |
| **Consolidated Survey Admin Supervisor** | 🤖 LLM AGENT | • Question selection (AI-driven)<br/>• Question phrasing & engagement<br/>• Frontend preparation<br/>• Progress tracking<br/>• Routing decisions |
| **Consolidated Lead Intelligence Agent** | 🤖 LLM AGENT | • Response saving<br/>• Score calculation<br/>• Tool usage decisions (Tavily/Maps)<br/>• Score validation & adjustment<br/>• Message generation<br/>• Status determination |
| **check_abandonment** | 📊 LOGIC | Time-based detection + database update |

### Key Features

✅ **Intelligent Question Selection**: AI-driven question ordering based on user responses  
✅ **Question Flow Strategy**: Non-deterministic flow that adapts to each user  
✅ **Score Validation**: Integrated validation with external tool support  
✅ **Tool Integration**: External validation (Tavily/Maps) for lead qualification  
✅ **Session Persistence**: State preserved between interactions via snapshots  
✅ **Abandonment Detection**: Time-based detection with automatic handling  
✅ **Business Rule Compliance**: AI selection within defined business constraints  
✅ **Performance Optimized**: Fewer LLM calls, consolidated processing  

### Routing Logic

The system uses intelligent routing based on:
- **Pending Responses**: Direct routing to lead intelligence when responses need processing
- **Lead Status**: Conditional continuation or completion based on qualification
- **Abandonment Risk**: Time-based detection triggers abandonment handling
- **Business Rules**: Survey continuation based on minimum question thresholds

### Session Management

- **HTTP-only Cookies**: Secure session management
- **Redis Backend**: Fast session state storage
- **Session Snapshots**: Complete state preservation in Supabase
- **State Recovery**: Automatic restoration of survey progress

## Implementation Files

- `/backend/app/graphs/simplified_survey_graph.py` - Main graph definition
- `/backend/app/graphs/supervisors/consolidated_survey_admin_supervisor.py` - Survey management
- `/backend/app/graphs/supervisors/consolidated_lead_intelligence_agent.py` - Lead processing
- `/backend/app/graphs/nodes/tracking_and_response_nodes.py` - Initialization logic
- `/backend/app/routes/survey_api.py` - API integration