# LangGraph Survey Flow - Standalone Test Implementation

This is a standalone, simplified version of the production LangGraph survey flow designed for testing and debugging with LangSmith integration.

## Features

- ✅ **Exact Graph Logic**: Maintains the same flow as production
- ✅ **Tool Integration**: Tavily search and Google Maps validation
- ✅ **Score Calculation**: Mathematical scoring with tool-based boosts
- ✅ **Personalized Messages**: LLM-generated completion messages
- ✅ **LangSmith Support**: Full tracing and debugging capabilities
- ✅ **SQLite Storage**: Local database for test data

## Architecture

```
Initialize Session
    ↓
Survey Admin Supervisor (LLM)
  - Selects 1-4 questions
  - Rephrases for engagement
  - Creates motivational messages
    ↓
Lead Intelligence Agent (LLM)
  - Processes responses
  - Calculates scores
  - Executes tools (Tavily/Maps)
  - Generates completion message
    ↓
Complete or Continue
```

## Setup

### 1. Install Dependencies with uv

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -e .
# OR
uv sync
```

### 2. Set Environment Variables

Create a `.env` file:

```bash
# Required (at least one)
OPENAI_API_KEY=your_openai_key
# OR
ANTHROPIC_API_KEY=your_anthropic_key

# Optional (for real tool calls)
TAVILY_API_KEY=your_tavily_key
GOOGLE_MAPS_API_KEY=your_google_maps_key

# Optional (for LangSmith tracing)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=survey-graph-test
LANGCHAIN_API_KEY=your_langsmith_key
```

### 3. Load Test Data

```bash
uv run python load_test_data.py
```

This creates a SQLite database with:
- 2 test businesses (Dog Walking, Real Estate)
- 18 total questions with scoring rubrics
- Ready-to-use form IDs

## Running Tests

### Run All Test Scenarios

```bash
uv run python test_runner.py --load-data
```

### Run with LangSmith Tracing

```bash
LANGCHAIN_TRACING_V2=true \
LANGCHAIN_PROJECT="survey-test" \
uv run python test_runner.py
```

### Run Individual Scenario

```bash
uv run python test_runner.py --scenario high  # High-quality lead
uv run python test_runner.py --scenario maybe # Maybe lead
uv run python test_runner.py --scenario low   # Unqualified lead
```

### Using LangGraph Studio

The `langgraph.json` file enables running this graph in LangGraph Studio:

```bash
# Open in LangGraph Studio
langgraph studio langgraph_test/
```

## Test Scenarios

### 1. High-Quality Lead (Downtown Austin)
- Location: Downtown Austin (close to service area)
- Urgency: Immediate need
- Budget: Good ($40/walk)
- **Expected**: QUALIFIED status with tool validation boosts

### 2. Maybe Lead (Round Rock)
- Location: Round Rock (borderline distance)
- Timeline: Next month
- Budget: Lower ($25/walk)
- **Expected**: MAYBE status with distance concerns

### 3. Unqualified Lead (Houston)
- Location: Wrong city (Houston)
- No dogs currently
- Just browsing
- **Expected**: NO status with helpful alternatives

## Output Example

```
=== SURVEY FLOW TEST ===
Session: abc-123-def
Form: Dog Walking Service

--- Step 1 ---
Questions Asked: 
  Q1: What's your name?
  Q2: What's your email?
User Responses: John Smith, john@email.com
Score Change: 0 → 0

--- Step 2 ---
Questions Asked:
  Q4: Where are you located?
  Q8: When would you like to start?
User Responses: Downtown Austin, Immediately
Score Change: 0 → 35

🔧 TOOLS EXECUTED:
  ✅ TAVILY:
    Query: Pawsome Dog Walking Austin TX legitimate business
    Result: Verified established business
    Score Impact: +15 points
  
  ✅ MAPS:
    Distance: 2.3 miles
    In Service Area: True
    Score Impact: +20 points

=== FINAL RESULTS ===
Lead Status: QUALIFIED
Final Score: 85/100
  - Base Score: 50
  - Tool Boost: +35

💬 COMPLETION MESSAGE TO USER:
Excellent news, John! We've verified that Pawsome Dog Walking is a 
trusted service in your area. You're only 2.3 miles from our service 
zone! Based on your immediate need and location, you're a perfect fit. 
We'll contact you within 24 hours to get your pups walking!
```

## Key Components

### Graph State (`graph/state.py`)
- Maintains survey state throughout flow
- Tracks questions, responses, scores
- Stores tool results and routing flags

### Supervisors
- **Survey Admin**: Question selection and phrasing (LLM-based)
- **Lead Intelligence**: Response processing and scoring (LLM-based)

### Toolbelts
- **Tavily Integration**: Business verification (+10-20 points)
- **Maps Integration**: Distance validation (+/-20 points)

### Database (`database/sqlite_db.py`)
- SQLite implementation matching production schema
- Stores forms, questions, sessions, responses

## Debugging with LangSmith

1. Enable tracing in environment
2. Run tests
3. View in LangSmith UI: https://smith.langchain.com
4. See complete execution trace:
   - All LLM calls and responses
   - Tool executions
   - State transitions
   - Score calculations

## Tool Impact on Scoring

### Tavily Search
- Positive verification: +15 points
- Neutral results: +5 points
- No results/error: 0 points

### Google Maps
- Within 5 miles: +20 points
- 5-10 miles: +15 points
- 10-25 miles: +10 points
- Over 25 miles: -10 points

## Customization

### Add New Test Scenarios

Edit `test_runner.py`:

```python
new_scenario_responses = [
    {"answer": "Your Name"},
    {"answer": "your@email.com"},
    # ... more responses
]

runner.run_test_scenario(
    "Scenario Name",
    "f1111111-1111-1111-1111-111111111111",  # Form ID
    new_scenario_responses
)
```

### Modify Scoring Logic

Edit `graph/toolbelts/lead_intelligence_toolbelt.py`:
- Adjust score thresholds
- Modify tool boost values
- Change classification rules

### Custom Completion Messages

Edit `graph/supervisors/consolidated_lead_intelligence.py`:
- Modify message templates
- Adjust tone by status
- Add business-specific content

## Troubleshooting

### No API Keys
- At least one LLM key required (OpenAI or Anthropic)
- Tool keys optional (will use mocks if missing)

### Database Errors
- Run `python load_test_data.py` to reset database
- Check `test_survey.db` exists in root directory

### LangSmith Not Showing Traces
- Verify `LANGCHAIN_TRACING_V2=true`
- Check `LANGCHAIN_API_KEY` is set
- Ensure project name is valid

## Files Generated

- `test_survey.db` - SQLite database with test data
- `test_results_[timestamp].json` - Test run results
- LangSmith traces (in cloud)

## Next Steps

1. Run tests to verify graph logic
2. Review LangSmith traces for debugging
3. Adjust scoring/messages as needed
4. Export results for analysis