"""Unified Completion Message Node - Single LLM node for all completion messages."""

from typing import Dict, Any, List
import json
import logging
from datetime import datetime

from ...models import get_chat_model
from ...state import SurveyState

logger = logging.getLogger(__name__)


def unified_completion_message_node(state: SurveyState) -> Dict[str, Any]:
    """
    Single LLM node that generates custom completion messages based on lead status.
    
    Args:
        state: Current SurveyState with final lead classification
        
    Returns:
        Dict with personalized completion message and metadata
    """
    try:
        # Extract state information
        lead_status = state.get("lead_status", "no")
        final_score = state.get("final_score", 0)
        confidence = state.get("confidence", 0.5)
        all_responses = state.get("all_responses", [])
        client_info = state.get("client_info", {})
        business_reasoning = state.get("business_reasoning", "")
        key_factors = state.get("key_factors", [])
        tool_results = state.get("tool_results", {})
        
        # Initialize LLM
        llm = get_chat_model(
            model_name="gpt-4o-mini",
            temperature=0.3  # Creative but consistent messaging
        )
        
        # Get business context
        business_name = client_info.get("business_name", "our team")
        industry = client_info.get("industry", "service business")
        contact_info = client_info.get("contact_info", {})
        value_proposition = client_info.get("value_proposition", "excellent service")
        
        # Create status-specific system prompts
        system_prompts = {
            "qualified": f"""You are creating a completion message for a QUALIFIED lead for {business_name}.

This lead has scored {final_score}/100 and shows strong potential as a customer.

TONE: Enthusiastic, welcoming, action-oriented
GOALS: 
- Celebrate their qualification
- Set clear next steps
- Provide contact information
- Create urgency for follow-up
- Reinforce value proposition

STRUCTURE:
1. Congratulations/excitement
2. Brief summary of why they're a great fit
3. Clear next steps and timeline
4. Contact information
5. Call to action""",

            "maybe": f"""You are creating a completion message for a MAYBE lead for {business_name}.

This lead scored {final_score}/100 and shows potential but needs follow-up to determine fit.

TONE: Encouraging, helpful, non-pushy
GOALS:
- Thank them for their interest
- Acknowledge they're worth consideration
- Set expectations for follow-up
- Leave door open for more information
- Maintain positive relationship

STRUCTURE:
1. Appreciation for their time
2. Acknowledgment of potential fit
3. Explanation of review process
4. Timeline for follow-up
5. Invitation to provide more info""",

            "no": f"""You are creating a completion message for an UNQUALIFIED lead for {business_name}.

This lead scored {final_score}/100 and is not a good fit for the service.

TONE: Kind, respectful, helpful
GOALS:
- Thank them graciously
- Be honest but gentle about fit
- Offer alternatives if possible
- Leave positive impression
- Maintain professional relationship

STRUCTURE:
1. Sincere thanks
2. Gentle explanation of service focus
3. Possible referrals or alternatives
4. Well wishes
5. Future contact option"""
        }
        
        system_prompt = system_prompts.get(lead_status, system_prompts["no"])
        
        # Prepare user context
        response_summary = _summarize_responses(all_responses)
        tool_summary = _summarize_tool_results(tool_results)
        
        user_prompt = f"""Create a personalized completion message for this lead:

LEAD CLASSIFICATION: {lead_status.upper()}
FINAL SCORE: {final_score}/100 (Confidence: {confidence:.1f})

BUSINESS CONTEXT:
- Business: {business_name}
- Industry: {industry}
- Value Proposition: {value_proposition}

CONTACT INFORMATION:
{json.dumps(contact_info, indent=2) if contact_info else "Standard contact process"}

LEAD RESPONSES SUMMARY:
{response_summary}

QUALIFICATION FACTORS:
- Key Strengths: {key_factors[:3] if key_factors else ['General interest']}
- Business Reasoning: {business_reasoning[:200]}...

EXTERNAL VALIDATION:
{tool_summary}

Create a message that feels personal, acknowledges their specific situation, and provides appropriate next steps for a {lead_status} lead."""

        # Get LLM response
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = llm.invoke(messages)
        
        # Parse response
        if hasattr(response, 'content'):
            completion_message = response.content.strip()
        else:
            completion_message = str(response).strip()
        
        # Determine next actions based on lead status
        next_actions = _determine_next_actions(lead_status, confidence, client_info)
        
        return {
            "completion_message": completion_message,
            "lead_status": lead_status,
            "final_score": final_score,
            "confidence": confidence,
            "next_actions": next_actions,
            "requires_follow_up": lead_status in ["qualified", "maybe"],
            "message_metadata": {
                "message_type": lead_status,
                "personalized": True,
                "llm_generated": True,
                "business_context_used": bool(client_info),
                "tool_insights_included": bool(tool_results),
                "response_count": len(all_responses),
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Completion message generation error: {e}")
        # Fallback to status-based standard messages
        lead_status = state.get("lead_status", "no")
        return _fallback_completion_message(lead_status, state)


def _summarize_responses(responses: List[Dict]) -> str:
    """Create a brief summary of user responses."""
    if not responses:
        return "No responses provided"
    
    summary_parts = []
    
    # Count and characterize responses
    total_responses = len(responses)
    summary_parts.append(f"{total_responses} responses provided")
    
    # Analyze response depth
    avg_length = sum(len(r.get("answer", "")) for r in responses) / total_responses
    if avg_length > 50:
        summary_parts.append("detailed responses")
    elif avg_length > 15:
        summary_parts.append("moderate detail")
    else:
        summary_parts.append("brief responses")
    
    # Include most recent key responses
    recent_answers = []
    for response in responses[-3:]:
        answer = response.get("answer", "")
        if len(answer.strip()) > 5:
            recent_answers.append(answer[:50] + ("..." if len(answer) > 50 else ""))
    
    if recent_answers:
        summary_parts.append(f"Recent: {'; '.join(recent_answers)}")
    
    return " | ".join(summary_parts)


def _summarize_tool_results(tool_results: Dict) -> str:
    """Summarize external validation results."""
    if not tool_results:
        return "No external validation performed"
    
    summary_parts = []
    
    if "tavily_search" in tool_results:
        tavily_data = tool_results["tavily_search"]
        query = tavily_data.get("query", "Unknown")
        summary_parts.append(f"Web research: {query}")
    
    if "google_maps" in tool_results:
        maps_data = tool_results["google_maps"]
        if maps_data.get("in_service_area"):
            distance = maps_data.get("distance", "unknown")
            summary_parts.append(f"Location validated: {distance}")
        else:
            summary_parts.append("Location outside service area")
    
    return " | ".join(summary_parts) if summary_parts else "External validation completed"


def _determine_next_actions(lead_status: str, confidence: float, client_info: Dict) -> List[str]:
    """Determine appropriate next actions based on lead classification."""
    actions = []
    
    if lead_status == "qualified":
        actions = [
            "immediate_contact",
            "schedule_consultation",
            "send_service_details",
            "add_to_priority_queue"
        ]
        if confidence > 0.9:
            actions.append("premium_service_offering")
    
    elif lead_status == "maybe":
        actions = [
            "add_to_review_queue",
            "schedule_follow_up_call",
            "send_additional_information",
            "manual_qualification_review"
        ]
        if confidence > 0.6:
            actions.append("expedited_review")
    
    elif lead_status == "no":
        actions = [
            "polite_decline_record",
            "referral_suggestions",
            "newsletter_signup_option",
            "future_contact_consent"
        ]
    
    return actions


def _fallback_completion_message(lead_status: str, state: SurveyState) -> Dict[str, Any]:
    """Fallback completion messages when LLM fails."""
    logger.info("Using fallback completion message")
    
    client_name = state.get("client_info", {}).get("business_name", "our team")
    
    messages = {
        "qualified": f"Thank you for your interest! Based on your responses, you appear to be an excellent fit for our services. {client_name} will contact you within 24 hours to discuss next steps.",
        
        "maybe": f"Thank you for taking the time to complete our form. We're reviewing your information and will get back to you within 2-3 business days to discuss how {client_name} might be able to help.",
        
        "no": f"Thank you for your interest in {client_name}. While we may not be the best fit for your current needs, we appreciate you taking the time to learn about our services."
    }
    
    return {
        "completion_message": messages.get(lead_status, messages["no"]),
        "lead_status": lead_status,
        "final_score": state.get("final_score", 0),
        "confidence": state.get("confidence", 0.5),
        "next_actions": _determine_next_actions(lead_status, 0.5, state.get("client_info", {})),
        "requires_follow_up": lead_status in ["qualified", "maybe"],
        "message_metadata": {
            "fallback": True,
            "personalized": False,
            "llm_generated": False
        }
    }