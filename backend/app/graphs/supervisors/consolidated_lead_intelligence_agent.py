"""Consolidated Lead Intelligence Agent - All lead processing in one place."""

from __future__ import annotations
from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime

from .base_supervisor import SupervisorAgent, SupervisorDecision
from ...state import SurveyState
from ...models import get_chat_model
from ..toolbelts.lead_intelligence_toolbelt import lead_intelligence_toolbelt

logger = logging.getLogger(__name__)


class ConsolidatedLeadIntelligenceAgent(SupervisorAgent):
    """Consolidated agent handling all lead intelligence and processing tasks."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="ConsolidatedLeadIntelligenceAgent",
            model_name="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=1500,  # Reduced for faster responses
            timeout_seconds=10,  # Reduced timeout for faster responses
            **kwargs
        )
        self.llm = get_chat_model(model_name="gpt-3.5-turbo", temperature=0.2)
        self.toolbelt = lead_intelligence_toolbelt
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for lead intelligence processing."""
        return """You are a Lead Intelligence Agent responsible for processing customer responses and determining lead qualification.

Your responsibilities:
1. Save customer responses to database
2. Calculate lead scores based on responses
3. Determine if external verification tools are needed
4. Analyze business fit for the customer
5. Generate completion messages for qualified leads
6. Make routing decisions for survey continuation

Always provide clear, data-driven assessments and maintain professional communication."""
    
    def make_decision(self, state: SurveyState, context: Dict[str, Any] = None) -> SupervisorDecision:
        """Make lead intelligence decision - delegates to process_lead_responses."""
        # This method is required by base class but we use process_lead_responses instead
        # Create a simple decision wrapper
        result = self.process_lead_responses(state)
        
        return SupervisorDecision(
            decision=result.get("lead_status", "continue"),
            reasoning=result.get("business_reasoning", "Lead intelligence processing completed"),
            confidence=result.get("confidence", 0.5),
            recommendations=result.get("next_actions", []),
            metadata=result
        )
    
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

CRITICAL INSTRUCTIONS:
- Write ONLY for the customer who filled out the form (B2C perspective)
- Do NOT include business-to-business language like "help your business grow"
- Focus on the SERVICE being provided TO the customer
- Use customer details from their responses to personalize
- The business context describes the SERVICE PROVIDER, not the customer

Keep it:
- {lead_status.upper()} tone: {"Enthusiastic and welcoming" if lead_status == "yes" else "Encouraging but not pushy" if lead_status == "maybe" else "Kind and helpful"}
- Customer-focused (the person who filled out the form)
- Personal (use their specific responses like names, needs, preferences)
- Professional but friendly
- 2-3 sentences max

WRONG: "Let's work together to help your business grow!"
RIGHT: "We're excited to help you with your dog walking needs!"

Just write the message, no other text."""
    
    def process_lead_responses(self, state: SurveyState) -> Dict[str, Any]:
        """Main entry point - processes all lead intelligence tasks."""
        try:
            # Step 1: Save responses to database
            save_result = self._save_responses(state)
            if not save_result["success"]:
                logger.error(f"Failed to save responses: {save_result.get('error')}")
            
            # Step 2: Calculate initial mathematical score
            score_result = self._calculate_lead_score(state)
            
            # Step 3: Analyze if tools are needed and make comprehensive decision
            comprehensive_decision = self._make_comprehensive_lead_decision(
                state, 
                score_result["calculated_score"]
            )
            
            # Step 4: Execute tools if recommended
            tool_results = {}
            if comprehensive_decision["tools_needed"]:
                tool_results = self._execute_tools(comprehensive_decision)
            
            # Step 5: Validate and adjust score with tool results
            final_classification = self._finalize_lead_classification(
                state,
                score_result["calculated_score"],
                comprehensive_decision,
                tool_results
            )
            
            # Step 6: Update database with final status
            self._update_database_status(state, final_classification)
            
            # Step 7: Mark questions as asked (convert question_id to question UUID)
            asked_question_uuids = self._mark_questions_as_asked(state)
            
            # Step 8: Return proper state update with cleared pending responses
            current_question_strategy = state.get('question_strategy', {})
            # Don't pollute asked_questions with UUIDs - keep only integer question IDs
            # Database tracking handles the actual question marking
            
            return {
                **final_classification,
                'pending_responses': [],  # Clear after processing
                'question_strategy': {
                    **current_question_strategy,
                    # Keep asked_questions unchanged - Survey Admin manages this with database
                    'asked_questions': current_question_strategy.get('asked_questions', [])
                },
                'lead_intelligence': {
                    **state.get('lead_intelligence', {}),
                    'last_classification': final_classification,
                    'classification_timestamp': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Lead intelligence processing error: {e}")
            return self._create_error_response(str(e))
    
    def _mark_questions_as_asked(self, state: SurveyState) -> List[str]:
        """Convert question_id numbers from responses to question UUIDs for tracking."""
        try:
            pending_responses = state.get("pending_responses", [])
            if not pending_responses:
                return []
            
            # Get form_id to load questions
            form_id = state.get("core", {}).get("form_id")
            if not form_id:
                logger.warning("No form_id found, cannot mark questions as asked")
                return []
            
            # Load all questions for this form to create mapping
            from ...utils.cached_data_loader import data_loader
            all_questions = data_loader.get_questions(form_id)
            if not all_questions:
                logger.warning(f"No questions found for form {form_id}")
                return []
            
            # Create mapping from question_id (number) to id (UUID)
            question_id_to_uuid = {}
            for q in all_questions:
                question_id = q.get('question_id')
                question_uuid = q.get('id')
                if question_id is not None and question_uuid:
                    question_id_to_uuid[question_id] = question_uuid
            
            # Convert response question_ids to UUIDs
            asked_uuids = []
            for response in pending_responses:
                question_id = response.get('question_id')
                if question_id in question_id_to_uuid:
                    question_uuid = question_id_to_uuid[question_id]
                    if question_uuid not in asked_uuids:
                        asked_uuids.append(question_uuid)
                        logger.debug(f"Marking question as asked: question_id={question_id} -> uuid={question_uuid}")
                else:
                    logger.warning(f"Could not find UUID for question_id {question_id}")
            
            logger.info(f"Marked {len(asked_uuids)} questions as asked: {asked_uuids}")
            return asked_uuids
            
        except Exception as e:
            logger.error(f"Failed to mark questions as asked: {e}")
            return []
    
    def _save_responses(self, state: SurveyState) -> Dict[str, Any]:
        """Save user responses to database."""
        try:
            session_id = state.get("core", {}).get("session_id")
            form_id = state.get("core", {}).get("form_id")
            pending_responses = state.get("pending_responses", [])
            
            if not pending_responses:
                return {"success": True, "saved_count": 0}
            
            return self.toolbelt.save_responses_to_database(
                session_id=session_id,
                responses=pending_responses,
                form_id=form_id
            )
        except Exception as e:
            logger.error(f"Response save error: {e}")
            return {"success": False, "error": str(e)}
    
    def _calculate_lead_score(self, state: SurveyState) -> Dict[str, Any]:
        """Calculate mathematical lead score."""
        try:
            responses = state.get("lead_intelligence", {}).get("responses", [])
            
            # Get scoring rubrics (simplified for now)
            scoring_rubrics = {}
            for response in responses:
                question_id = response.get("question_id")
                # Simple scoring: longer answers = higher scores
                scoring_rubrics[str(question_id)] = {
                    "min_length": 10,
                    "base_score": 8,
                    "penalty_score": 3,
                    "max_score": 10
                }
            
            business_rules = state.get("business_rules", {})
            
            return self.toolbelt.calculate_lead_score(
                responses=responses,
                scoring_rubrics=scoring_rubrics,
                business_rules=business_rules
            )
        except Exception as e:
            logger.error(f"Score calculation error: {e}")
            return {"calculated_score": 0, "error": str(e)}
    
    def _make_comprehensive_lead_decision(
        self, 
        state: SurveyState,
        calculated_score: int
    ) -> Dict[str, Any]:
        """Make comprehensive decision using simple LLM calls instead of complex JSON."""
        
        pending_responses = state.get("pending_responses", [])
        
        # Step 1: Get business context from database  
        form_id = state.get("core", {}).get("form_id")
        business_context = self._get_business_context_from_db(form_id)
        logger.info(f"📋 Business context: {business_context}")
        
        # Step 2: Get tool recommendations from LLM (simple prompt)
        tool_recommendation = self._get_tool_recommendations(pending_responses)
        
        # Step 3: Get business fit weighting from LLM (simple prompt)
        business_fit = self._get_business_fit_assessment(pending_responses, business_context)
        logger.info(f"🤖 LLM Business Fit Assessment: {business_fit}")
        
        # Step 4: Calculate business fit adjustment (pure logic)
        business_adjustment = self._calculate_business_adjustment(business_fit, calculated_score)
        logger.info(f"🤖 Business Fit Adjustment: {business_adjustment:+d} points (fit: {business_fit})")
        
        # Step 5: Calculate final score with all adjustments (pure logic)
        final_score = calculated_score + business_adjustment
        logger.info(f"🎯 Final score: {calculated_score} + {business_adjustment} = {final_score}")
        
        # Step 6: Determine final classification based on final score
        # Get total responses from database
        session_id = state.get("core", {}).get("session_id")
        total_responses = self._get_total_responses_count(session_id)
        lead_status = self._determine_lead_status(final_score, total_responses)
        logger.info(f"🎯 Lead status determined: {lead_status} (score: {final_score}, total responses: {total_responses})")
        
        # Step 7: Generate tools needed based on tool recommendation
        tools_needed = []
        tool_queries = {}
        if tool_recommendation in ["tavily", "both"]:
            tools_needed.append("tavily_search")
            tool_queries["tavily_search"] = self._generate_tavily_query(pending_responses)
        if tool_recommendation in ["maps", "both"]:
            tools_needed.append("google_maps")
            origin, destination = self._extract_locations(pending_responses)
            tool_queries["google_maps"] = {"origin": origin, "destination": destination}
        
        return {
            "lead_status": lead_status,
            "final_score": final_score,
            "confidence": 0.8,  # High confidence in our logic-based approach
            "score_adjustment": business_adjustment,
            "validation_action": "APPROVE",
            "tools_needed": tools_needed,
            "tool_queries": tool_queries,
            "completion_message": "",  # Will be generated later if needed
            "business_reasoning": f"Score: {final_score} (base: {calculated_score} + business fit: {business_adjustment}). Fit: {business_fit}",
            "key_factors": [f"business_fit_{business_fit.lower()}", f"score_{final_score}"],
            "red_flags": [],
            "next_actions": [],
            "requires_follow_up": lead_status in ["maybe", "qualified"]
        }
    
    def _execute_tools(self, decision: Dict) -> Dict[str, Any]:
        """Execute recommended external tools."""
        tool_results = {}
        tools_needed = decision.get("tools_needed", [])
        tool_queries = decision.get("tool_queries", {})
        
        try:
            # Execute Tavily search if needed
            if "tavily_search" in tools_needed and "tavily_search" in tool_queries:
                query = tool_queries["tavily_search"]
                tool_results["tavily_search"] = self.toolbelt.execute_tavily_search(query)
            
            # Execute Google Maps if needed
            if "google_maps" in tools_needed and "google_maps" in tool_queries:
                maps_query = tool_queries["google_maps"]
                if isinstance(maps_query, dict):
                    tool_results["google_maps"] = self.toolbelt.execute_maps_validation(
                        origin=maps_query.get("origin", ""),
                        destination=maps_query.get("destination", "")
                    )
            
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            tool_results["error"] = str(e)
        
        return tool_results
    
    def _finalize_lead_classification(
        self,
        state: SurveyState,
        calculated_score: int,
        decision: Dict,
        tool_results: Dict
    ) -> Dict[str, Any]:
        """Finalize lead classification with all information."""
        
        # If no tool results, use the initial decision
        if not tool_results:
            return decision
        
        # Re-evaluate with tool results
        client_info = state.get("client_info", {})
        client_name = client_info.get("business_name", "our team")
        
        # Adjust score based on tool results
        final_score = decision["final_score"]
        confidence = decision["confidence"]
        
        # Analyze tool impact
        if "tavily_search" in tool_results:
            if tool_results["tavily_search"].get("success"):
                # Positive validation increases confidence
                confidence = min(1.0, confidence + 0.1)
        
        if "google_maps" in tool_results:
            maps_result = tool_results["google_maps"]
            if maps_result.get("success"):
                if not maps_result.get("in_service_area"):
                    # Outside service area - reduce score
                    final_score = max(0, final_score - 20)
                    decision["red_flags"].append("Outside service area")
        
        # Final status determination
        if final_score >= 75 and confidence >= 0.7:
            lead_status = "qualified"
        elif final_score <= 35 and confidence >= 0.6:
            lead_status = "no"
        elif len(state.get("lead_intelligence", {}).get("responses", [])) < 4:
            lead_status = "continue"
        else:
            lead_status = "maybe"
        
        # Generate final completion message if not continuing
        if lead_status != "continue" and not decision.get("completion_message"):
            # Get business context and responses for personalized message
            form_id = state.get("core", {}).get("form_id")
            business_context = self._get_business_context_from_db(form_id)
            pending_responses = state.get("pending_responses", [])
            
            decision["completion_message"] = self._generate_completion_message_llm(
                lead_status, pending_responses, business_context
            )
        
        # Determine next actions
        if not decision.get("next_actions"):
            decision["next_actions"] = self.toolbelt.determine_next_actions(
                lead_status, confidence, final_score
            )
        
        # CRITICAL: Add routing logic separate from lead classification
        # This determines whether to continue or end the survey flow
        route_decision = self._determine_route_decision(state, lead_status)
        
        return {
            **decision,
            "lead_status": lead_status,
            "final_score": final_score,
            "confidence": confidence,
            "tool_results": tool_results,
            "completed": lead_status != "continue",
            "route_decision": route_decision  # ← CRITICAL: Add this field
        }
    
    def _determine_route_decision(self, state: SurveyState, lead_status: str) -> str:
        """Determine routing decision based on lead status and available questions."""
        try:
            # Get session info for database queries
            session_id = state.get("core", {}).get("session_id")
            form_id = state.get("core", {}).get("form_id")
            
            if not session_id or not form_id:
                logger.warning("Missing session_id or form_id for routing decision")
                return "end"
            
            # Get available questions and asked questions from database
            from ...database.supabase_client import supabase_client as db
            available_questions = db.get_form_questions(form_id)
            asked_questions = db.get_asked_questions(session_id)
            remaining_questions = len(available_questions) - len(asked_questions)
            
            logger.info(f"🔀 Routing decision: lead_status={lead_status}, remaining_questions={remaining_questions}")
            
            # Routing logic: separate from lead classification
            if lead_status == "unknown" and remaining_questions > 0:
                route_decision = "continue"  # Need more data
            elif lead_status == "maybe" and remaining_questions > 0:
                route_decision = "continue"  # Maybe leads need more information to become yes/no
            elif lead_status in ["qualified", "yes", "no"] or remaining_questions == 0:
                route_decision = "end"  # Definitive classification or no more questions
            else:
                route_decision = "end"  # Default to end
                
            logger.info(f"🔀 Routing decision: {route_decision} (status: {lead_status}, remaining questions: {remaining_questions})")
            return route_decision
            
        except Exception as e:
            logger.error(f"Error determining route decision: {e}")
            return "end"  # Safe default
    
    def _get_tool_recommendations(self, responses: List[Dict]) -> str:
        """Get tool recommendations from LLM."""
        try:
            context = "Recent customer responses:\\n"
            for r in responses[-5:]:  # Last 5 responses
                context += f"Q: {r.get('question_text', '')}\\n"
                context += f"A: {r.get('answer', '')}\\n\\n"
            
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
            context = f"BUSINESS CONTEXT: {business_context}\\n\\n"
            context += "Customer responses to analyze:\\n"
            for r in responses:
                context += f"Q: {r.get('question_text', '')}\\n"
                context += f"A: {r.get('answer', '')}\\n\\n"
            
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
            context = f"BUSINESS CONTEXT: {business_context}\\n\\n"
            context += "Customer information from their responses:\\n"
            for r in responses:
                context += f"Q: {r.get('question_text', '')}\\n"
                context += f"A: {r.get('answer', '')}\\n\\n"
            
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
            from ...database.supabase_client import supabase_client as db
            
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
        # Lead status should be one of: unknown, maybe, qualified, no
        # Routing is handled separately
        
        if num_responses < 3:
            return "unknown"  # Insufficient data
        
        if final_score >= 75:
            return "qualified"  # Qualified
        elif final_score >= 40:
            return "maybe"  # Maybe qualified
        else:
            return "no"  # Not qualified
    
    def _get_total_responses_count(self, session_id: str) -> int:
        """Get total response count from database."""
        try:
            from ...database.supabase_client import supabase_client as db
            responses = db.get_responses(session_id)
            return len(responses) if responses else 0
        except Exception as e:
            logger.error(f"Error getting response count: {e}")
            return 0
    
    def _update_database_status(self, state: SurveyState, classification: Dict):
        """Update database with final lead status."""
        try:
            session_id = state.get("core", {}).get("session_id")
            
            self.toolbelt.update_lead_status_in_database(
                session_id=session_id,
                lead_status=classification["lead_status"],
                final_score=classification["final_score"],
                confidence=classification["confidence"],
                completion_message=classification.get("completion_message")
            )
        except Exception as e:
            logger.error(f"Database update error: {e}")
    
    def _create_fallback_decision(self, score: int, responses: List[Dict]) -> Dict[str, Any]:
        """Create fallback decision when LLM fails."""
        # Simple rule-based classification  
        if score >= 75:
            lead_status = "qualified"
            confidence = 0.6
        elif score <= 35:
            lead_status = "no"
            confidence = 0.6
        elif len(responses) < 4:
            lead_status = "unknown"  # Changed from "continue" - continue is routing, not status
            confidence = 0.8
        else:
            lead_status = "maybe"
            confidence = 0.4
        
        messages = self.toolbelt.generate_default_messages(lead_status, "our team")
        
        return {
            "lead_status": lead_status,
            "final_score": score,
            "confidence": confidence,
            "score_adjustment": 0,
            "validation_action": "APPROVE",
            "tools_needed": [],
            "tool_queries": {},
            "completion_message": messages.get(lead_status, ""),
            "business_reasoning": "Fallback classification based on score",
            "key_factors": ["mathematical_score"],
            "red_flags": [],
            "next_actions": self.toolbelt.determine_next_actions(lead_status, confidence, score),
            "requires_follow_up": lead_status in ["qualified", "maybe"]
        }
    
    def _create_error_response(self, error: str) -> Dict[str, Any]:
        """Create an error response."""
        return {
            "lead_status": "error",
            "error": error,
            "final_score": 0,
            "confidence": 0,
            "completed": False,
            "timestamp": datetime.now().isoformat(),
            "pending_responses": []  # Clear pending responses even on error
        }


def consolidated_lead_intelligence_node(state: SurveyState) -> Dict[str, Any]:
    """Node function for Consolidated Lead Intelligence Agent."""
    agent = ConsolidatedLeadIntelligenceAgent()
    return agent.process_lead_responses(state)