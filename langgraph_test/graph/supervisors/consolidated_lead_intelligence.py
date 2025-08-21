"""Consolidated Lead Intelligence Agent with tool integration."""

from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime

from .base_supervisor import SupervisorAgent, SupervisorDecision
from ..toolbelts.lead_intelligence_toolbelt import lead_intelligence_toolbelt
from ...models import get_chat_model

logger = logging.getLogger(__name__)

class ConsolidatedLeadIntelligenceAgent(SupervisorAgent):
    """Consolidated agent handling all lead intelligence and processing tasks."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="ConsolidatedLeadIntelligenceAgent",
            model_name="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=1500,
            timeout_seconds=10,
            **kwargs
        )
        self.llm = get_chat_model(model_name="gpt-3.5-turbo", temperature=0.2)
        self.toolbelt = lead_intelligence_toolbelt
    
    def get_system_prompt(self) -> str:
        """Comprehensive system prompt for lead intelligence."""
        return """You are an advanced Lead Intelligence AI that processes and qualifies leads comprehensively.

Your integrated responsibilities include:
1. RESPONSE PROCESSING: Save and validate user responses
2. SCORE CALCULATION: Compute mathematical lead scores
3. TOOL DECISIONS: Determine if external validation is needed (Tavily/Maps)
4. SCORE VALIDATION: Ensure scores make business sense
5. LEAD CLASSIFICATION: Decide final lead status (qualified/maybe/no/continue)
6. MESSAGE GENERATION: Create personalized completion messages
7. NEXT ACTIONS: Determine appropriate follow-up steps

CLASSIFICATION THRESHOLDS:
- Qualified: 75+ points with high confidence
- Maybe: 40-75 points OR any score with low confidence
- Not Qualified: <40 points with high confidence
- Continue: Insufficient data, need more questions

TOOL USAGE GUIDELINES:
- Use Tavily for: Business verification, reputation check, legitimacy validation
- Use Google Maps for: Distance validation, service area checks
- Tools can add 10-20 points each if validation is positive

MESSAGE TONE BY STATUS:
- Qualified: Enthusiastic, welcoming, action-oriented
- Maybe: Encouraging, helpful, non-pushy
- No: Kind, respectful, helpful with alternatives
- Continue: Motivational, progress-focused

OUTPUT FORMAT:
Return comprehensive JSON with all processing results:
{
  "lead_status": "yes" | "maybe" | "no" | "continue",
  "final_score": 85,
  "confidence": 0.85,
  "tools_needed": ["tavily_search", "google_maps"] | [],
  "tool_queries": {
    "tavily_search": "search query",
    "google_maps": {"origin": "address", "destination": "address"}
  },
  "completion_message": "personalized message based on status",
  "business_reasoning": "detailed explanation",
  "key_factors": ["positive1", "positive2"],
  "red_flags": ["concern1"] | [],
  "next_actions": ["action1", "action2"]
}"""
    
    def process_lead_responses(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Main entry point - processes all lead intelligence tasks."""
        try:
            logger.info("🤖 Lead Intelligence: Starting processing")
            
            # Get pending responses
            pending_responses = state.get("pending_responses", [])
            if not pending_responses:
                logger.info("No pending responses to process")
                return {"lead_status": "continue"}
            
            # Step 1: Save responses to database
            session_id = state.get("core", {}).get("session_id")
            form_id = state.get("core", {}).get("form_id")
            
            save_result = self.toolbelt.save_responses_to_database(
                session_id, pending_responses, form_id
            )
            logger.info(f"💾 Saved {save_result['saved_count']} responses")
            
            # Step 2: Calculate initial mathematical score
            # Create simple scoring rubrics
            scoring_rubrics = {}
            for response in pending_responses:
                q_id = str(response.get("question_id"))
                scoring_rubrics[q_id] = {
                    "positive_keywords": ["yes", "immediately", "urgent", "asap", "definitely"],
                    "negative_keywords": ["no", "never", "not interested", "maybe later"]
                }
            
            score_result = self.toolbelt.calculate_lead_score(
                pending_responses, scoring_rubrics
            )
            initial_score = score_result["calculated_score"]
            logger.info(f"📊 Initial score: {initial_score}")
            
            # Step 3: Analyze if tools are needed and make comprehensive decision
            comprehensive_decision = self._make_comprehensive_lead_decision(
                state, initial_score, pending_responses
            )
            
            # Step 4: Execute tools if recommended
            tool_results = {}
            total_tool_boost = 0
            
            if comprehensive_decision.get("tools_needed"):
                logger.info(f"🔧 Executing tools: {comprehensive_decision['tools_needed']}")
                
                # Execute Tavily if needed
                if "tavily_search" in comprehensive_decision["tools_needed"]:
                    query = comprehensive_decision.get("tool_queries", {}).get("tavily_search")
                    if query:
                        tavily_result = self.toolbelt.execute_tavily_search(query)
                        tool_results["tavily"] = tavily_result
                        total_tool_boost += tavily_result.get("score_boost", 0)
                        logger.info(f"🔍 Tavily boost: +{tavily_result.get('score_boost', 0)}")
                
                # Execute Maps if needed
                if "google_maps" in comprehensive_decision["tools_needed"]:
                    maps_params = comprehensive_decision.get("tool_queries", {}).get("google_maps", {})
                    if maps_params:
                        maps_result = self.toolbelt.execute_maps_validation(
                            maps_params.get("origin", ""),
                            maps_params.get("destination", "")
                        )
                        tool_results["maps"] = maps_result
                        total_tool_boost += maps_result.get("score_boost", 0)
                        logger.info(f"📍 Maps boost: +{maps_result.get('score_boost', 0)}")
            
            # Step 5: Calculate final score with tool boosts
            final_score = initial_score + total_tool_boost
            logger.info(f"🎯 Final score: {initial_score} + {total_tool_boost} = {final_score}")
            
            # Step 6: Determine final classification
            lead_status = self._determine_lead_status(final_score, len(pending_responses))
            
            # Step 7: Generate personalized completion message
            completion_message = comprehensive_decision.get("completion_message")
            if not completion_message and lead_status != "continue":
                completion_message = self._generate_completion_message(
                    lead_status, state, tool_results, final_score
                )
            
            # Step 8: Update database with final status
            if lead_status != "continue":
                self.toolbelt.update_lead_session_status(
                    session_id, lead_status, final_score, completion_message
                )
            
            # Step 9: Return state update
            logger.info(f"✅ Lead Intelligence complete: {lead_status} (score: {final_score})")
            
            return {
                "lead_status": lead_status,
                "completed": lead_status != "continue",
                "completion_message": completion_message,
                "pending_responses": [],  # Clear after processing
                "lead_intelligence": {
                    **state.get("lead_intelligence", {}),
                    "current_score": final_score,
                    "lead_status": lead_status,
                    "last_classification": {
                        "status": lead_status,
                        "score": final_score,
                        "tool_boost": total_tool_boost,
                        "timestamp": datetime.now().isoformat()
                    }
                },
                "tool_results": tool_results,
                "tool_score_boost": total_tool_boost,
                "frontend_response": {
                    "step_type": "completion" if lead_status != "continue" else "continue",
                    "lead_status": lead_status,
                    "score": final_score,
                    "message": completion_message
                }
            }
            
        except Exception as e:
            logger.error(f"Lead intelligence processing error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return {
                "lead_status": "continue",
                "error": str(e)
            }
    
    def _make_comprehensive_lead_decision(
        self, 
        state: Dict[str, Any], 
        initial_score: int,
        responses: List[Dict]
    ) -> Dict[str, Any]:
        """Use LLM to make comprehensive lead decision."""
        try:
            # Build context for LLM
            context = f"""
            Current score: {initial_score}
            Number of responses: {len(responses)}
            
            Recent responses:
            """
            
            for r in responses[-5:]:  # Last 5 responses
                context += f"\n- Q: {r.get('question_text', '')}"
                context += f"\n  A: {r.get('answer', '')}"
            
            context += f"""
            
            Business context: Dog walking service in Austin, TX
            Service area: 15 mile radius
            
            Based on the responses, determine:
            1. Should we use Tavily to verify business legitimacy?
            2. Should we use Maps to check distance/location?
            3. What's the appropriate lead status?
            4. Generate a personalized completion message if not continuing.
            """
            
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": context}
            ]
            
            response = self.llm.invoke(messages)
            
            # Parse LLM response
            try:
                decision_data = json.loads(response.content)
            except:
                # Fallback if JSON parsing fails
                decision_data = {
                    "lead_status": "continue" if initial_score < 40 else "maybe" if initial_score < 75 else "yes",
                    "tools_needed": [],
                    "completion_message": ""
                }
            
            # Add tool queries if tools are needed
            if "tavily_search" in decision_data.get("tools_needed", []):
                decision_data.setdefault("tool_queries", {})
                decision_data["tool_queries"]["tavily_search"] = "Pawsome Dog Walking Austin TX legitimate business"
            
            if "google_maps" in decision_data.get("tools_needed", []):
                # Extract location from responses if available
                location = "Austin, TX"  # Default
                for r in responses:
                    if "location" in r.get("question_text", "").lower() or "address" in r.get("question_text", "").lower():
                        location = r.get("answer", "Austin, TX")
                        break
                
                decision_data.setdefault("tool_queries", {})
                decision_data["tool_queries"]["google_maps"] = {
                    "origin": location,
                    "destination": "Downtown Austin, TX"  # Business location
                }
            
            return decision_data
            
        except Exception as e:
            logger.error(f"LLM decision error: {e}")
            # Fallback decision
            return {
                "lead_status": "continue" if initial_score < 40 else "maybe",
                "tools_needed": [],
                "completion_message": "",
                "error": str(e)
            }
    
    def _determine_lead_status(self, final_score: int, num_responses: int) -> str:
        """Determine lead status based on score and responses."""
        if num_responses < 3:
            return "continue"  # Need more data
        
        if final_score >= 75:
            return "yes"  # Qualified
        elif final_score >= 40:
            return "maybe"  # Maybe qualified
        elif num_responses >= 5:
            return "no"  # Not qualified (enough data)
        else:
            return "continue"  # Need more data to be sure
    
    def _generate_completion_message(
        self, 
        lead_status: str, 
        state: Dict[str, Any],
        tool_results: Dict[str, Any],
        final_score: int
    ) -> str:
        """Generate personalized completion message."""
        
        # Get business name
        from ...database.sqlite_db import db
        form_id = state.get("core", {}).get("form_id")
        form = db.get_form(form_id)
        
        if form and form.get("client_id"):
            client = db.get_client(form["client_id"])
            business_name = client.get("business_name", "our team") if client else "our team"
        else:
            business_name = "Pawsome Dog Walking"
        
        # Check for user name in responses
        user_name = ""
        responses = state.get("lead_intelligence", {}).get("responses", [])
        for r in responses:
            if "name" in r.get("question_text", "").lower():
                user_name = r.get("answer", "").split()[0] if r.get("answer") else ""
                break
        
        # Build message based on status and tool results
        if lead_status == "yes":
            message = f"Excellent news{', ' + user_name if user_name else ''}! "
            
            # Add tool validation info
            if tool_results.get("tavily", {}).get("success"):
                message += f"We've verified that {business_name} is a trusted, established service. "
            
            if tool_results.get("maps", {}).get("in_service_area"):
                distance = tool_results["maps"].get("distance", "your area")
                message += f"Great news - you're {distance} from our service area! "
            
            message += f"Based on your responses (score: {final_score}/100), you're a perfect fit for our services. "
            message += "We'll contact you within 24 hours to get started. Welcome to the Pawsome family!"
            
        elif lead_status == "maybe":
            message = f"Thank you for your interest{', ' + user_name if user_name else ''}! "
            
            if tool_results.get("maps", {}).get("distance_miles", 0) > 10:
                message += "While you're slightly outside our primary service area, we may still be able to help. "
            
            message += f"Based on your responses (score: {final_score}/100), we need to review a few more details. "
            message += f"Someone from {business_name} will reach out within 48 hours to discuss options."
            
        else:  # no
            message = f"Thank you for considering {business_name}{', ' + user_name if user_name else ''}. "
            
            if tool_results.get("maps") and not tool_results["maps"].get("in_service_area"):
                message += "Unfortunately, you're outside our current service area. "
            
            message += "Based on your needs, we may not be the perfect fit right now. "
            message += "We recommend checking out Rover.com or Care.com for alternative pet care services in your area."
        
        return message

def consolidated_lead_intelligence_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Node function for lead intelligence processing."""
    agent = ConsolidatedLeadIntelligenceAgent()
    return agent.process_lead_responses(state)