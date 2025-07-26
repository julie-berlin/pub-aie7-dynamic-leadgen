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
- **Notebooks**: Development and experimentation in `/notebooks/`
  - `poc_chain.ipynb` - Main proof of concept using LangGraph
  - `PoC_Survey_Agents.ipynb` - Survey agents implementation
- **Source code**: `/src/` - Core application modules
  - `handlers/` - Request/response handlers
  - `llm/` - Language model integrations
  - `ml/` - Machine learning components
  - `prompt_engineering/` - Prompt templates and engineering
  - `utils/` - Utility functions and configuration loading
- **Configuration**: `/config/` - YAML configuration files
- **Data**: `/data/` - Input data, outputs, and cached results
  - Survey questions and client data in JSON format
  - Embeddings and cached LLM responses

## Development Setup
```bash
# Install dependencies
uv sync

# Run notebooks
uv run jupyter notebook

# Run main application
uv run python3 main.py
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
- `leads` table: Complete lead records with final status
- `responses` table: Individual question-answer pairs with timestamps
- `form_sessions` table: Session state and progression tracking
- `historical_outcomes` table: Past lead success data for ML learning

## Current Implementation Status
- **PoC Complete**: Basic LangGraph flow in `poc_chain.ipynb`
- **Next Priority**: Question selection agent with JSON integration
- **Data Integration**: Questions loaded from JSON with rich metadata
- **Frontend**: React.js + Tailwind v4 (planned)
- **Admin Interface**: Configuration/notebook-based (current), web-based (planned)

## Business Rules
- Required questions have `required: true` AND scoring rubrics
- Contact info (name, email) only required for qualified leads
- Users must see minimum 4 questions before failure (unless hard fail)
- Tough qualifying questions should not appear early in flow
- Form abandonment data must be tracked and analyzed

## Development Notes
- Use `python3` in all commands
- Prefer editing existing files over creating new ones
- Configuration is centralized in `/config/` directory
- All LLM interactions should be mockable for testing
- Design for future multilingual support
- Tailwind v4 configuration required for theming

## Testing Strategy
- Test flow with different lead quality scenarios
- Validate scoring logic against business requirements  
- Test abandonment prevention and re-engagement
- Verify database state consistency
- Test real-time vs batch notification systems