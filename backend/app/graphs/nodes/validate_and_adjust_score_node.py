"""Validate and Adjust Score Node - LLM validates mathematical scores make business sense."""

from typing import Dict, Any, List
import json
import logging
from datetime import datetime

from ...models import get_chat_model
from ...state import SurveyState

logger = logging.getLogger(__name__)


def validate_and_adjust_score_node(state: SurveyState) -> Dict[str, Any]:
    """
    LLM validates the mathematical lead score and adjusts if needed based on business logic.
    
    Args:
        state: Current SurveyState with calculated score and tool results
        
    Returns:
        Dict with validated score, final classification, and reasoning
    """
    try:
        # Extract state information
        calculated_score = state.get("calculated_score", 0)
        all_responses = state.get("all_responses", [])
        tool_results = state.get("tool_results", {})
        client_info = state.get("client_info", {})
        business_rules = state.get("business_rules", {})
        lead_intel_decision = state.get("lead_intel_decision", {})
        
        if not all_responses:
            logger.warning("No responses available for score validation")
            return _fallback_score_validation(calculated_score, "no_responses")
        
        # Initialize LLM
        llm = get_chat_model(
            model="gpt-4o-mini",
            temperature=0.1,  # Low temperature for consistent scoring
            max_tokens=1500
        )
        
        # Analyze tool results impact
        tool_insights = _analyze_tool_results(tool_results)
        
        system_prompt = f"""You are a lead qualification validation expert for {client_info.get('business_name', 'a service business')}.

Your role is to review the mathematical lead score and determine if it makes business sense based on:
1. Response quality and engagement
2. Business-specific qualification criteria  
3. External validation results (if any)
4. Industry standards and patterns

BUSINESS CONTEXT:
- Industry: {client_info.get('industry', 'Service business')}
- Service Area: {client_info.get('service_area', 'Local')}
- Target Customer: {client_info.get('target_customer', 'General public')}

VALIDATION ACTIONS:
- APPROVE: Score accurately reflects lead quality
- ADJUST_UP: Score too low, increase by 10-30 points with reasoning
- ADJUST_DOWN: Score too high, decrease by 10-30 points with reasoning  
- MAYBE_RECLASSIFY: Score is borderline, mark as "maybe" for manual review
- NEED_MORE_DATA: Insufficient information, continue survey

CLASSIFICATION THRESHOLDS:
- Qualified: 75+ points with high confidence
- Maybe: 40-75 points OR any score with low confidence
- Not Qualified: <40 points with high confidence

OUTPUT FORMAT:
Return valid JSON only:
{{
  "validation_action": "APPROVE" | "ADJUST_UP" | "ADJUST_DOWN" | "MAYBE_RECLASSIFY" | "NEED_MORE_DATA",
  "final_score": 85,
  "score_adjustment": 0,
  "final_classification": "qualified" | "maybe" | "no" | "continue",
  "confidence": 0.85,
  "business_reasoning": "detailed explanation of why this score makes business sense",
  "key_factors": ["factor1", "factor2"],
  "red_flags": ["concern1"] | [],
  "tool_impact": "how external validation affected the decision"
}}"""

        # Prepare detailed user prompt
        user_prompt = f"""Validate this lead qualification score:

CALCULATED SCORE: {calculated_score}/100

USER RESPONSES ({len(all_responses)} total):
{json.dumps(all_responses, indent=2)}

EXTERNAL VALIDATION RESULTS:
{json.dumps(tool_results, indent=2) if tool_results else "No external validation performed"}

TOOL INSIGHTS:
{json.dumps(tool_insights, indent=2)}

BUSINESS RULES:
{json.dumps(business_rules, indent=2)}

PRELIMINARY SUPERVISOR ASSESSMENT:
{json.dumps(lead_intel_decision, indent=2)}

Does the calculated score of {calculated_score} accurately reflect this lead's qualification level for this business? Consider response quality, business fit, and any external validation results."""

        # Get LLM validation
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = llm.invoke(messages)
        
        # Parse LLM response
        if hasattr(response, 'content'):
            llm_content = response.content
        else:
            llm_content = str(response)
            
        try:
            validation_data = json.loads(llm_content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM validation response: {e}")
            return _fallback_score_validation(calculated_score, "parse_error")
        
        # Process validation results
        final_score = validation_data.get("final_score", calculated_score)
        score_adjustment = validation_data.get("score_adjustment", 0)
        final_classification = validation_data.get("final_classification", "continue")
        confidence = validation_data.get("confidence", 0.5)
        
        # Ensure score is within bounds
        final_score = max(0, min(100, final_score))
        
        # Final classification logic with confidence consideration
        if final_classification == "continue":
            status = "continue"
        elif final_score >= 75 and confidence >= 0.8:
            status = "qualified"
        elif final_score <= 35 and confidence >= 0.7:
            status = "no"
        else:
            status = "maybe"  # Borderline cases or low confidence
        
        return {
            "final_score": final_score,
            "original_score": calculated_score,
            "score_adjustment": score_adjustment,
            "lead_status": status,
            "confidence": confidence,
            "validation_action": validation_data.get("validation_action", "APPROVE"),
            "business_reasoning": validation_data.get("business_reasoning", "Score validation completed"),
            "key_factors": validation_data.get("key_factors", []),
            "red_flags": validation_data.get("red_flags", []),
            "tool_impact": validation_data.get("tool_impact", "No external validation"),
            "validation_metadata": {
                "llm_validation": True,
                "original_score": calculated_score,
                "score_changed": final_score != calculated_score,
                "tool_results_used": bool(tool_results),
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Score validation error: {e}")
        calculated_score = state.get("calculated_score", 50)
        return _fallback_score_validation(calculated_score, f"error: {str(e)}")


def _analyze_tool_results(tool_results: Dict) -> Dict[str, Any]:
    """Analyze tool results to understand their impact on lead qualification."""
    insights = {
        "tavily_impact": "none",
        "maps_impact": "none", 
        "key_findings": [],
        "concerns": []
    }
    
    # Analyze Tavily search results
    if "tavily_search" in tool_results:
        tavily_data = tool_results["tavily_search"]
        results = tavily_data.get("results", [])
        
        if results:
            insights["tavily_impact"] = "informative"
            insights["key_findings"].append("External research conducted")
            
            # Simple analysis of search results
            combined_text = " ".join(str(result) for result in results).lower()
            
            if any(concern in combined_text for concern in ["dangerous", "aggressive", "illegal", "banned"]):
                insights["concerns"].append("Potential safety/legal concerns found")
                insights["tavily_impact"] = "concerning"
            elif any(positive in combined_text for positive in ["safe", "recommended", "certified", "licensed"]):
                insights["key_findings"].append("Positive validation found")
                insights["tavily_impact"] = "positive"
    
    # Analyze Google Maps results
    if "google_maps" in tool_results:
        maps_data = tool_results["google_maps"]
        
        if maps_data.get("in_service_area"):
            insights["maps_impact"] = "positive"
            insights["key_findings"].append("Location within service area")
        else:
            insights["maps_impact"] = "negative"
            insights["concerns"].append("Location outside service area")
        
        distance = maps_data.get("distance", "")
        if "mile" in str(distance):
            try:
                distance_num = float(distance.split()[0])
                if distance_num > 25:
                    insights["concerns"].append("Long distance service")
            except (ValueError, IndexError):
                pass
    
    return insights


def _fallback_score_validation(calculated_score: int, reason: str) -> Dict[str, Any]:
    """Fallback score validation when LLM fails."""
    logger.info(f"Using fallback score validation: {reason}")
    
    # Simple rule-based classification
    if calculated_score >= 75:
        status = "qualified"
        confidence = 0.6
    elif calculated_score <= 35:
        status = "no"
        confidence = 0.6
    else:
        status = "maybe"
        confidence = 0.4
    
    return {
        "final_score": calculated_score,
        "original_score": calculated_score,
        "score_adjustment": 0,
        "lead_status": status,
        "confidence": confidence,
        "validation_action": "APPROVE",
        "business_reasoning": f"Fallback validation due to: {reason}",
        "key_factors": ["mathematical_score"],
        "red_flags": [],
        "tool_impact": "No validation performed",
        "validation_metadata": {
            "llm_validation": False,
            "fallback": True,
            "reason": reason
        }
    }