# Production Graph Changes Required

This document outlines all changes that need to be applied to the production graph based on the standalone test implementation.

## 1. Lead Status Classification vs Routing Separation

**Issue**: The production graph was mixing lead classification statuses with routing decisions.

**Files to Update**:
- `backend/app/graphs/supervisors/consolidated_lead_intelligence.py`
- `backend/app/graphs/simplified_survey_graph.py`

### Changes in `consolidated_lead_intelligence.py`:

1. **Update `_determine_lead_status` method** to only return classification statuses:
```python
def _determine_lead_status(self, final_score: int, num_responses: int) -> str:
    """Determine lead status based on score and responses."""
    # Lead status should be one of: unknown, maybe, yes, no
    # Routing is handled separately
    
    if num_responses < 3:
        return "unknown"  # Insufficient data
    
    if final_score >= 75:
        return "yes"  # Qualified
    elif final_score >= 40:
        return "maybe"  # Maybe qualified
    else:
        return "no"  # Not qualified
```

2. **Add routing logic in `process_lead_responses`** (around line 167):
```python
# Step 8: Determine routing based on lead status and available questions
from database.supabase_db import db  # Use production database
available_questions = db.get_form_questions(state.get("core", {}).get("form_id"))
asked_questions = db.get_asked_questions(session_id)
remaining_questions = len(available_questions) - len(asked_questions)

# Routing logic: separate from lead classification
if lead_status == "unknown" and remaining_questions > 0:
    route_decision = "continue"  # Need more data
elif lead_status in ["yes", "maybe", "no"] or remaining_questions == 0:
    route_decision = "end"  # Classification complete or no more questions
else:
    route_decision = "end"  # Default to end

logger.info(f"🔀 Routing decision: {route_decision} (status: {lead_status}, remaining questions: {remaining_questions})")
```

3. **Return route_decision in state update**:
```python
return {
    "lead_status": lead_status,
    "completed": route_decision == "end",
    "completion_message": completion_message,
    "pending_responses": [],  # Clear after processing
    # ... other fields ...
    "route_decision": route_decision,  # Add this field
    # ... rest of return
}
```

### Changes in `simplified_survey_graph.py`:

1. **Update `route_after_lead_intelligence` function**:
```python
def route_after_lead_intelligence(state: SurveyState) -> str:
    """Determine routing after lead intelligence processing."""
    
    lead_status = state.get("lead_status", "unknown")
    completed = state.get("completed", False)
    route_decision = state.get("route_decision", "end")  # Use route_decision instead of lead_status
    
    logger.info(f"🔀 Routing after lead_intelligence: status={lead_status}, completed={completed}, route={route_decision}")
    
    # Use the route decision from lead intelligence
    if route_decision == "end" or completed:
        logger.info("🔀 Survey complete!")
        return END
    
    # Check for too many iterations (safety check)
    core = state.get("core", {})
    step = core.get("step", 0)
    if step > 20:
        logger.warning(f"🔀 Forcing END (too many steps: {step})")
        return END
    
    # Continue survey if route decision is continue
    if route_decision == "continue":
        logger.info("🔀 Continuing to survey_administration")
        return "survey_administration"
    
    # Default to end
    logger.info("🔀 Default to END")
    return END
```

## 2. Lead Intelligence Agent System Prompt Enhancement

**File**: `backend/app/graphs/supervisors/consolidated_lead_intelligence.py`

**Update the `get_system_prompt` method** to include business context and score adjustment authority:

```python
def get_system_prompt(self) -> str:
    """Comprehensive system prompt for lead intelligence with score adjustment authority."""
    # Get business context from database
    form_id = getattr(self, '_current_form_id', None)
    business_context = self._get_business_context(form_id) if form_id else {}
    
    return f"""You are an advanced Lead Intelligence AI with SCORE ADJUSTMENT AUTHORITY.

Your integrated responsibilities include:
1. RESPONSE PROCESSING: Save and validate user responses
2. SCORE CALCULATION: Compute mathematical lead scores
3. TOOL DECISIONS: Determine if external validation is needed (Tavily/Maps)
4. SCORE VALIDATION & ADJUSTMENT: Make significant score adjustments based on business context
5. LEAD CLASSIFICATION: Decide final lead status (yes/maybe/no/unknown)
6. MESSAGE GENERATION: Create personalized completion messages
7. NEXT ACTIONS: Determine appropriate follow-up steps

SCORE ADJUSTMENT AUTHORITY:
You have the authority to make significant score adjustments (+/-50 points) when the mathematical score doesn't align with business reality. Consider:

BUSINESS CONTEXT:
- Business: {business_context.get('business_name', 'Service Business')}
- Industry: {business_context.get('industry', 'Service Industry')}
- Service Area: {business_context.get('service_area', 'Local area')}
- Target Audience: {business_context.get('target_audience', 'General customers')}
- Business Goals: {business_context.get('goals', 'Generate qualified leads')}

SCORING RUBRICS:
{self._format_scoring_rubrics(business_context)}

CLASSIFICATION THRESHOLDS (after your adjustments):
- Yes (Qualified): 75+ points with high confidence
- Maybe: 40-75 points OR any score with low confidence  
- No (Not Qualified): <40 points with high confidence
- Unknown: Insufficient data, need more questions

SCORE ADJUSTMENT EXAMPLES:
- Distance too far but only -10 penalty → Make it -30 or -50
- Perfect business fit but low mathematical score → Add +20 to +40
- Red flags in responses → Subtract -30 to -50
- Exceptional enthusiasm/urgency → Add +15 to +30

TOOL USAGE GUIDELINES:
- Use Tavily for: Business verification, reputation check, legitimacy validation
- Use Google Maps for: Distance validation, service area checks  
- Tools can add/subtract 10-50 points based on validation results

MESSAGE TONE BY STATUS:
- Yes: Enthusiastic, welcoming, action-oriented
- Maybe: Encouraging, helpful, non-pushy
- No: Kind, respectful, helpful with alternatives
- Unknown: Motivational, progress-focused

Your primary job is to ensure lead classifications make business sense by weighing all factors and making appropriate score adjustments that reflect the true lead quality.

OUTPUT FORMAT:
Return JSON for tool execution and analysis (NO lead_status - calculated separately):
{{
  "tools_needed": ["tavily_search", "google_maps"] | [],
  "tool_queries": {{
    "tavily_search": "business verification query",
    "google_maps": {{"origin": "customer location", "destination": "service location"}}
  }},
  "score_adjustments": {{
    "adjustment_amount": 0,
    "adjustment_reason": "explanation for any score changes",
    "business_fit_analysis": "how well this lead fits the business"
  }},
  "completion_message": "personalized message for this lead quality level",
  "business_reasoning": "detailed analysis considering business goals and rubrics",
  "key_factors": ["positive indicators"],
  "red_flags": ["concerns or issues"],
  "confidence_notes": "factors that could affect classification"
}}"""

def _get_business_context(self, form_id: str) -> Dict[str, Any]:
    """Get business context for scoring decisions."""
    try:
        # This would need to be implemented to fetch from production database
        from backend.app.database.supabase_db import db
        form = db.get_form(form_id)
        if form and form.get('client_id'):
            client = db.get_client(form['client_id'])
            return client or {}
    except Exception as e:
        logger.error(f"Failed to get business context: {e}")
    
    return {}

def _format_scoring_rubrics(self, business_context: Dict[str, Any]) -> str:
    """Format scoring rubrics for the prompt."""
    # This would format the specific scoring criteria for the business
    return """
    - Location within service area: Critical factor
    - Immediate need vs future consideration: High impact
    - Budget alignment: Important for qualification
    - Specific service requirements: Must match capabilities
    - Customer type fit: Should align with target audience
    """
```

## 3. Google Maps API Integration Update

**File**: `backend/app/graphs/toolbelts/lead_intelligence_toolbelt.py`

**Update the Google Maps integration** to use the Routes API instead of Distance Matrix API:

1. **Update the `execute_maps_validation` method**:
```python
def execute_maps_validation(self, origin: str, destination: str) -> Dict[str, Any]:
    """Execute Google Maps validation using Routes API."""
    try:
        import requests
        import os
        
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not api_key:
            return self._mock_maps_response()
        
        # Use Routes API endpoint
        url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "routes.duration,routes.distanceMeters"
        }
        
        data = {
            "origin": {
                "address": origin
            },
            "destination": {
                "address": destination
            },
            "travelMode": "DRIVE"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("routes"):
                route = result["routes"][0]
                distance_meters = route.get("distanceMeters", 0)
                distance_miles = distance_meters * 0.000621371
                
                # Calculate score impact based on distance
                if distance_miles <= 5:
                    score_boost = 20
                    in_service_area = True
                elif distance_miles <= 15:
                    score_boost = 0
                    in_service_area = True
                elif distance_miles <= 25:
                    score_boost = -20
                    in_service_area = False
                else:
                    score_boost = -50
                    in_service_area = False
                
                return {
                    "success": True,
                    "distance": f"{distance_miles:.1f} miles",
                    "distance_miles": distance_miles,
                    "in_service_area": in_service_area,
                    "score_boost": score_boost,
                    "api_used": "google_routes",
                    "raw_response": route
                }
            else:
                logger.warning("No routes found in Google Maps response")
                return self._mock_maps_response()
        
        else:
            logger.error(f"Google Maps API error: {response.status_code} - {response.text}")
            return self._mock_maps_response()
            
    except Exception as e:
        logger.error(f"Maps validation error: {e}")
        return self._mock_maps_response()
```

## 4. Database Concurrency Improvements

**File**: `backend/app/database/supabase_db.py` (if using similar retry patterns)

**Add retry decorators** for database operations that might have concurrency issues:

```python
import time
import random
from functools import wraps

def retry_db_operation(max_retries=3, delay_range=(0.1, 0.5)):
    """Decorator to retry database operations on transient errors."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if "timeout" in str(e).lower() or "connection" in str(e).lower():
                        if attempt < max_retries - 1:
                            delay = random.uniform(*delay_range)
                            logger.warning(f"Database operation failed, retrying in {delay:.2f}s (attempt {attempt + 1}/{max_retries})")
                            time.sleep(delay)
                            continue
                    raise e
            return None
        return wrapper
    return decorator

# Apply to critical database operations
@retry_db_operation()
def save_response(self, session_id: str, response_data: Dict[str, Any]) -> bool:
    # existing implementation
    pass

@retry_db_operation()
def update_lead_session(self, session_id: str, update_data: Dict[str, Any]) -> bool:
    # existing implementation
    pass
```

## 5. Enhanced Error Handling and Logging

**File**: `backend/app/graphs/supervisors/consolidated_lead_intelligence.py`

**Improve error handling** in the `process_lead_responses` method:

```python
# Add more detailed logging around line 157 where lead status is determined
lead_status = self._determine_lead_status(final_score, len(pending_responses))
logger.info(f"🎯 Lead status determined: {lead_status} (score: {final_score}, responses: {len(pending_responses)})")

# Add validation
if lead_status not in ["unknown", "maybe", "yes", "no"]:
    logger.error(f"Invalid lead status returned: {lead_status}. Defaulting to 'unknown'")
    lead_status = "unknown"
```

## Summary of Critical Changes

1. **Separation of Lead Classification from Routing**: Lead status should only be classification (unknown/maybe/yes/no), routing decisions are separate (continue/end)

2. **Enhanced Lead Intelligence Agent**: Give the agent authority to make significant score adjustments (+/-50) based on business context and scoring rubrics

3. **Google Routes API Migration**: Update from Distance Matrix API to Routes API for better reliability

4. **Database Concurrency**: Add retry mechanisms for transient database errors

5. **Improved Error Handling**: Better validation and logging for lead status determination

## Testing Requirements

After implementing these changes, test with:
- Various score scenarios to ensure proper classification
- Distance validation with different locations
- Edge cases where mathematical scores don't match business reality
- Multiple concurrent sessions to verify database stability

## Migration Notes

- Test changes in staging environment first
- Update API documentation if response formats change
- Monitor lead classification accuracy after deployment
- Verify tool integrations work with production API keys