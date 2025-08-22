"""Consolidated Lead Intelligence Agent with tool integration."""

from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime

from .base_supervisor import SupervisorAgent, SupervisorDecision
from ..toolbelts.lead_intelligence_toolbelt import lead_intelligence_toolbelt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from models import get_chat_model

logger = logging.getLogger(__name__)

class ConsolidatedLeadIntelligenceAgent(SupervisorAgent):
    """Consolidated agent handling all lead intelligence and processing tasks."""

    def __init__(self, **kwargs):
        super().__init__(
            name="ConsolidatedLeadIntelligenceAgent",
            model_name="gpt-5-mini",
            temperature=0.1,
            max_tokens=1500,
            timeout_seconds=10,
            **kwargs
        )
        self.llm = get_chat_model(model_name="gpt-3.5-turbo", temperature=0.2)
        self.toolbelt = lead_intelligence_toolbelt

    def _get_tool_recommendation_prompt(self) -> str:
        """Simple prompt for tool recommendations."""
        return """You are analyzing customer responses to recommend verification tools.

Based on the customer responses, should we verify anything externally?

AVAILABLE TOOLS:
- Tavily Search: Check business legitimacy, verify company names, reputation
- Google Maps: Validate distances, check if location is in service area

Respond with ONLY one of these options:
- "tavily" - if we should verify a business name or check legitimacy
- "maps" - if we should check distance/location
- "both" - if we need both verifications
- "none" - if no external verification needed

Consider: Do they mention a business name to verify? Do they provide a location that might need distance checking?"""

    def _get_business_weight_prompt(self) -> str:
        """Simple prompt for business fit weighting."""
        return """You are analyzing how well a customer fits the business based on their responses.

Rate the overall customer fit:

PERFECT_FIT: Ideal customer (meets all key criteria, strong indicators)
GOOD_FIT: Solid prospect (meets most criteria, minor concerns)
OKAY_FIT: Average prospect (meets some criteria, some concerns)
POOR_FIT: Weak prospect (few criteria met, major concerns)
BAD_FIT: Wrong customer (major misalignment, clear red flags)

Consider factors like:
- Location fit for service area
- Budget alignment
- Service needs matching offerings
- Urgency and commitment level
- Overall engagement quality

Respond with ONLY the fit level: PERFECT_FIT, GOOD_FIT, OKAY_FIT, POOR_FIT, or BAD_FIT"""

    def _get_completion_message_prompt(self, lead_status: str) -> str:
        """Simple prompt for completion message."""
        return f"""Write a personalized completion message for a {lead_status.upper()} lead.

STATUS: {lead_status.upper()}

Keep it:
- {lead_status.upper()} tone: {"Enthusiastic and welcoming" if lead_status == "yes" else "Encouraging but not pushy" if lead_status == "maybe" else "Kind and helpful"}
- Personal (use customer details from their responses)
- Professional
- 2-3 sentences max

Just write the message, no other text."""

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

            # Step 3: Get business context once from database
            business_context = self._get_business_context_from_db(form_id)
            logger.info(f"📋 Business context: {business_context}")

            # Step 4: Get tool recommendations from LLM (simple prompt)
            tool_recommendation = self._get_tool_recommendations(pending_responses)

            # Step 5: Get business fit weighting from LLM (simple prompt)
            business_fit = self._get_business_fit_assessment(pending_responses, business_context)
            logger.info(f"🤖 LLM Business Fit Assessment: {business_fit}")

            # Step 6: Execute tools if recommended (pure logic)
            tool_results = {}
            total_tool_boost = 0

            if tool_recommendation in ["tavily", "both"]:
                query = self._generate_tavily_query(pending_responses)
                tavily_result = self.toolbelt.execute_tavily_search(query)
                tool_results["tavily"] = tavily_result
                total_tool_boost += tavily_result.get("score_boost", 0)
                logger.info(f"🔍 Tavily boost: +{tavily_result.get('score_boost', 0)}")

            if tool_recommendation in ["maps", "both"]:
                origin, destination = self._extract_locations(pending_responses)
                maps_result = self.toolbelt.execute_maps_validation(origin, destination)
                tool_results["maps"] = maps_result
                total_tool_boost += maps_result.get("score_boost", 0)
                logger.info(f"📍 Maps boost: +{maps_result.get('score_boost', 0)}")

            # Step 7: Calculate business fit adjustment (pure logic based on LLM weight)
            business_adjustment = self._calculate_business_adjustment(business_fit, initial_score)
            logger.info(f"🤖 Business Fit Adjustment: {business_adjustment:+d} points (fit: {business_fit})")

            # Step 8: Calculate final score with all adjustments (pure logic)
            final_score = initial_score + total_tool_boost + business_adjustment
            logger.info(f"🎯 Final score: {initial_score} + {total_tool_boost} + {business_adjustment} = {final_score}")

            # Step 9: Determine final classification based on final score
            # Get total responses from database
            from database.sqlite_db import db
            total_responses = len(db.get_responses(session_id))
            lead_status = self._determine_lead_status(final_score, total_responses)
            logger.info(f"🎯 Lead status determined: {lead_status} (score: {final_score}, total responses: {total_responses})")

            # Step 10: Generate personalized completion message (LLM call)
            completion_message = ""
            if lead_status != "unknown":
                completion_message = self._generate_completion_message_llm(lead_status, pending_responses, business_context)

            # Step 11: Determine routing based on lead status and available questions
            from database.sqlite_db import db
            available_questions = db.get_form_questions(state.get("core", {}).get("form_id"))
            asked_questions = db.get_asked_questions(session_id)
            remaining_questions = len(available_questions) - len(asked_questions)

            # Routing logic: separate from lead classification
            if lead_status == "unknown" and remaining_questions > 0:
                route_decision = "continue"  # Need more data
            elif lead_status == "maybe" and remaining_questions > 0:
                route_decision = "continue"  # Maybe leads need more information to become yes/no
            elif lead_status in ["yes", "no"] or remaining_questions == 0:
                route_decision = "end"  # Definitive classification or no more questions
            else:
                route_decision = "end"  # Default to end

            logger.info(f"🔀 Routing decision: {route_decision} (status: {lead_status}, remaining questions: {remaining_questions})")

            # Step 12: Update database with final status if ending
            if route_decision == "end":
                self.toolbelt.update_lead_session_status(
                    session_id, lead_status, final_score, completion_message
                )

            # Step 13: Return state update
            logger.info(f"✅ Lead Intelligence complete: {lead_status} (score: {final_score})")

            return {
                "lead_status": lead_status,
                "completed": route_decision == "end",
                "completion_message": completion_message,
                "pending_responses": [],  # Clear after processing
                "lead_intelligence": {
                    **state.get("lead_intelligence", {}),
                    "current_score": final_score,
                    "lead_status": lead_status,
                    "last_classification": {
                        "status": lead_status,
                        "score": final_score,
                        "initial_score": initial_score,
                        "tool_boost": total_tool_boost,
                        "business_adjustment": business_adjustment,
                        "business_fit": business_fit,
                        "timestamp": datetime.now().isoformat()
                    }
                },
                "tool_results": tool_results,
                "tool_score_boost": total_tool_boost,
                "llm_score_adjustment": business_adjustment,
                "route_decision": route_decision,
                "frontend_response": {
                    "step_type": "completion" if route_decision == "end" else "continue",
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

    def _get_tool_recommendations(self, responses: List[Dict]) -> str:
        """Get tool recommendations from LLM."""
        try:
            context = "Recent customer responses:\n"
            for r in responses[-5:]:  # Last 5 responses
                context += f"Q: {r.get('question_text', '')}\n"
                context += f"A: {r.get('answer', '')}\n\n"

            messages = [
                {"role": "system", "content": self._get_tool_recommendation_prompt()},
                {"role": "user", "content": context}
            ]

            response = self.llm.invoke(messages)
            result = response.content.strip().lower()

            # Validate response
            if result in ["tavily", "maps", "both", "none"]:
                return result
            else:
                logger.warning(f"Invalid tool recommendation: {result}, defaulting to 'none'")
                return "none"

        except Exception as e:
            logger.error(f"Tool recommendation error: {e}")
            return "none"

    def _get_business_fit_assessment(self, responses: List[Dict], business_context: str) -> str:
        """Get business fit assessment from LLM."""
        try:
            context = f"BUSINESS CONTEXT: {business_context}\n\n"
            context += "Customer responses to analyze:\n"
            for r in responses:
                context += f"Q: {r.get('question_text', '')}\n"
                context += f"A: {r.get('answer', '')}\n\n"

            logger.info(f"🔍 Evaluating responses: {[(r.get('question_text'), r.get('answer')) for r in responses]}")

            messages = [
                {"role": "system", "content": self._get_business_weight_prompt()},
                {"role": "user", "content": context}
            ]

            response = self.llm.invoke(messages)
            result = response.content.strip().upper()

            # Validate response
            valid_fits = ["PERFECT_FIT", "GOOD_FIT", "OKAY_FIT", "POOR_FIT", "BAD_FIT"]
            if result in valid_fits:
                return result
            else:
                logger.warning(f"Invalid business fit: {result}, defaulting to 'OKAY_FIT'")
                return "OKAY_FIT"

        except Exception as e:
            logger.error(f"Business fit assessment error: {e}")
            return "OKAY_FIT"

    def _generate_completion_message_llm(self, lead_status: str, responses: List[Dict], business_context: str) -> str:
        """Generate completion message using LLM."""
        try:
            context = f"BUSINESS CONTEXT: {business_context}\n\n"
            context += "Customer information from their responses:\n"
            for r in responses:
                context += f"Q: {r.get('question_text', '')}\n"
                context += f"A: {r.get('answer', '')}\n\n"

            messages = [
                {"role": "system", "content": self._get_completion_message_prompt(lead_status)},
                {"role": "user", "content": context}
            ]

            response = self.llm.invoke(messages)
            return response.content.strip()

        except Exception as e:
            logger.error(f"Completion message generation error: {e}")
            return f"Thank you for your interest! We'll be in touch soon."

    def _generate_tavily_query(self, responses: List[Dict]) -> str:
        """Generate Tavily search query from responses (pure logic)."""
        # Look for business names or companies mentioned
        for r in responses:
            answer = r.get('answer', '').lower()
            if any(word in answer for word in ['company', 'business', 'corp', 'llc', 'inc']):
                return f"{r.get('answer', '')} business verification"

        # Default query
        return "business verification and reputation check"

    def _extract_locations(self, responses: List[Dict]) -> tuple:
        """Extract origin and destination from responses (pure logic)."""
        customer_location = "Austin, TX"  # Default
        business_location = "Downtown Austin, TX"  # Default business location

        # Look for location/address in responses
        for r in responses:
            question = r.get('question_text', '').lower()
            if 'location' in question or 'address' in question or 'where' in question:
                answer = r.get('answer', '').strip()
                if answer:
                    customer_location = answer
                break

        return customer_location, business_location

    def _calculate_business_adjustment(self, business_fit: str, initial_score: int) -> int:
        """Calculate score adjustment based on business fit (pure logic)."""
        # Business fit weights (mathematical, not LLM)
        fit_adjustments = {
            "PERFECT_FIT": 30,
            "GOOD_FIT": 15,
            "OKAY_FIT": 0,
            "POOR_FIT": -20,
            "BAD_FIT": -40
        }

        base_adjustment = fit_adjustments.get(business_fit, 0)

        # Scale adjustment based on initial score
        # If score is already high, don't boost as much
        # If score is low but great fit, boost more
        if business_fit in ["PERFECT_FIT", "GOOD_FIT"] and initial_score < 50:
            base_adjustment += 10  # Extra boost for good fit with low initial score
        elif business_fit in ["POOR_FIT", "BAD_FIT"] and initial_score > 70:
            base_adjustment -= 10  # Extra penalty for bad fit with high initial score

        return base_adjustment

    def _get_business_context_from_db(self, form_id: str) -> str:
        """Get business context from database for LLM prompts."""
        try:
            from database.sqlite_db import db

            # Get form and client info
            form = db.get_form(form_id)
            if not form or not form.get('client_id'):
                return "General service business"

            client = db.get_client(form['client_id'])
            if not client:
                return "General service business"

            # Build context string
            context_parts = []

            if client.get('business_name'):
                context_parts.append(f"Business: {client['business_name']}")

            if client.get('business_type'):
                context_parts.append(f"Type: {client['business_type']}")

            if client.get('industry'):
                context_parts.append(f"Industry: {client['industry']}")

            if client.get('target_audience'):
                context_parts.append(f"Target: {client['target_audience']}")

            if client.get('goals'):
                context_parts.append(f"Goals: {client['goals']}")

            return " | ".join(context_parts) if context_parts else "General service business"

        except Exception as e:
            logger.error(f"Failed to get business context: {e}")
            return "General service business"

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

    def _generate_completion_message(
        self,
        lead_status: str,
        state: Dict[str, Any],
        tool_results: Dict[str, Any],
        final_score: int
    ) -> str:
        """Generate personalized completion message."""

        # Get business name
        from database.sqlite_db import db
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
