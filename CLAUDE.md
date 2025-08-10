# Dynamic Lead Gen with Agents - Project Context

## Project Overview
This application helps client users create multi-step forms for lead generation with two key AI-powered capabilities:
1. **Adaptive Question Selection**: Questions are ordered and selected based on user responses
2. **Lead Qualification**: Automated assessment of whether answers indicate a qualified lead

The system uses AI agents to create intelligent, engaging forms that maximize conversion and lead quality.

## Application Architecture

### Core Capabilities
1. **Form Creation**: Marketers set up lead gen forms (initially manual config, later agent-assisted)
2. **Adaptive Forms**: Public-facing multi-step forms with AI-driven question flow
3. **Lead Scoring & Messaging**: Automated lead qualification with personalized responses
4. **Analytics & Reporting**: Daily insights and strategy recommendations for marketers

### Technology Stack
- **Backend**: Python 3.12+ with LangChain & LangGraph
- **Database**: Supabase for data storage and real-time updates
- **Frontend**: React.js with Tailwind CSS v4 for theming
- **Package Manager**: uv (modern Python package manager)
- **Configuration**: YAML-based configuration management

### Project Structure
- **Main application**: `main.py` - Entry point for the application
- **Backend**: `/backend/app/` - Core application modules
  - `handlers/` - Request/response handlers
  - `llm/` - Language model integrations
  - `ml/` - Machine learning components
  - `prompt_engineering/` - Prompt templates and engineering
  - `utils/` - Utility functions and configuration loading
  - `routes/` - API endpoints for survey operations
  - `graphs/` - LangGraph implementations for survey flow
- **Database**: `/database/` - Database migrations and population scripts
  - `001_initial_schema.sql` - Complete database schema with all tables
  - `002_populate_example_data.sql` - 5 example business scenarios with 52 questions
  - `business_scenarios.md` - Documentation of all business cases
  - `test_database_population.py` - Comprehensive test suite
- **Notebooks**: Development and experimentation in `/notebooks/`
  - `poc_chain.ipynb` - Main proof of concept using LangGraph
  - `PoC_Survey_Agents.ipynb` - Survey agents implementation
- **Configuration**: `/config/` - YAML configuration files
- **Data**: `/data/` - Input data, outputs, and cached results
  - Survey questions and client data (now primarily database-driven)
  - Embeddings and cached LLM responses

## Development Setup
```bash
# Install dependencies
uv sync

# Set up database (run in Supabase SQL Editor)
# 1. Run: database/001_initial_schema.sql
# 2. Run: database/002_populate_example_data.sql

# Test database setup
uv run python3 database/test_database_population.py

# Run notebooks
uv run jupyter notebook

# Run main application
uv run python3 main.py
```

## Database Setup
The system includes comprehensive database population with 5 example business scenarios:

1. **Pawsome Dog Walking** - Pet services (10 questions)
2. **Metro Realty Group** - Real estate (12 questions)  
3. **TechSolve Consulting** - Software consulting (11 questions)
4. **FitLife Personal Training** - Health & fitness (10 questions)
5. **Sparkle Clean Solutions** - Home cleaning (9 questions)

**Total: 52 questions** across all forms with proper scoring rubrics and business logic.

### Quick Database Setup
```bash
# Run setup script for guided database initialization
uv run python3 database/setup_and_test.py
```

## LangGraph Flow Architecture

### Core Flow Design
Current focus is on capabilities #2 and #3 (Adaptive Forms and Lead Scoring):

```
Start → Question Selection Agent → Question Phrasing Node → Engagement Agent → Present Step
   ↑                                                                              ↓
   ←── Continue Flow ←── Engagement Check ←── More Questions? ←── Save State ← Score Lead
                              ↓
                        Completion Flow → Message Generation → Save Final State
```

### Agent & Node Responsibilities

**Question Selection Agent**:
- Selects 1-3 logically related questions per step (max 3)
- Avoids repeating previously asked questions
- Ensures required questions are asked for lead qualification
- Can add follow-up questions based on previous responses

**Question Phrasing Node**:
- Adapts question tone for business context and user type
- Ensures questions are clear and engaging
- Not an agent - always executed as part of flow

**Engagement Agent**:
- Reviews each step after questions and phrasing
- Adds compelling headlines and 1-2 motivational sentences
- Uses expert marketer strategies to prevent abandonment
- Applies persuasion tactics appropriate to business context

**Lead Scoring Agent**:
- Recalculates score after every step
- Uses both JSON scoring rubrics AND historical success data from database
- Enforces minimum 4-question rule before lead can fail (unless outright failure)
- Places leads in 3 categories: "yes", "no", "maybe"

### Lead Classification & Actions
- **"Yes" leads**: Real-time notification + personalized completion message + email
- **"Maybe" leads**: Daily batch email to client + personalized completion message
- **"No" leads**: Database storage only + generic completion message
- **Failed required questions**: Immediate routing to "no" completion flow

### Data Management

**Auto-save Strategy**:
- Form state saved automatically after each step
- Individual question responses stored for analytics
- Complete state maintained for form resumption
- Final status update when form completed/abandoned

**Database Schema (Supabase)**:
- `clients` table: Business profiles and AI context information
- `forms` table: Form configurations with scoring thresholds
- `form_questions` table: Individual questions with scoring rubrics
- `lead_sessions` table: Session tracking with abandonment detection
- `responses` table: Individual question-answer pairs with timestamps
- `tracking_data` table: UTM parameters and marketing attribution
- `session_snapshots` table: State recovery and resumption
- `lead_outcomes` table: Conversion tracking for ML learning

## Current Implementation Status
- **✅ Core System**: Complete LangGraph flow with all phases implemented
- **✅ Database Integration**: Full database schema with 5 example business scenarios
- **✅ API Layer**: REST endpoints for survey start, step, abandon, and status
- **✅ Data Population**: 52 questions across 5 diverse business types
- **✅ Testing Suite**: Comprehensive validation with 100% pass rate
- **✅ UTM Tracking**: Marketing attribution and abandonment detection
- **✅ Lead Scoring**: Automated qualification with personalized messaging
- **🚧 Frontend**: React.js + Tailwind v4 (in development)
- **🚧 Admin Interface**: Web-based form management (planned)

### Available Test Forms
Ready-to-use form IDs for testing:
- `f1111111-1111-1111-1111-111111111111` - Pawsome Dog Walking
- `f2222222-2222-2222-2222-222222222222` - Metro Realty Group
- `f3333333-3333-3333-3333-333333333333` - TechSolve Consulting
- `f4444444-4444-4444-4444-444444444444` - FitLife Personal Training
- `f5555555-5555-5555-5555-555555555555` - Sparkle Clean Solutions

## Business Rules
- Required questions have `required: true` AND scoring rubrics
- Contact info (name, email) only required for qualified leads
- Users must see minimum 4 questions before failure (unless hard fail)
- Tough qualifying questions should not appear early in flow
- Form abandonment data must be tracked and analyzed

## Development Notes
- Use `python3` in all commands
- Prefer editing existing files over creating new ones
- Database-first approach: All questions and client data stored in Supabase
- Configuration is centralized in `/config/` directory
- All LLM interactions should be mockable for testing
- Design for future multilingual support
- Tailwind v4 configuration required for theming

## API Testing Examples

### Start a Survey Session
```bash
curl -X POST http://localhost:8000/api/survey/start \
  -H "Content-Type: application/json" \
  -d '{
    "form_id": "f1111111-1111-1111-1111-111111111111",
    "utm_source": "google",
    "utm_campaign": "dog_walking_test"
  }'
```

### Submit Responses
```bash
curl -X POST http://localhost:8000/api/survey/step \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your_session_id",
    "responses": [
      {
        "question_id": 1,
        "answer": "John Smith"
      }
    ]
  }'
```

## Testing Strategy
- Test flow with different lead quality scenarios
- Validate scoring logic against business requirements
- Test abandonment prevention and re-engagement
- Verify database state consistency
- Test real-time vs batch notification systems
