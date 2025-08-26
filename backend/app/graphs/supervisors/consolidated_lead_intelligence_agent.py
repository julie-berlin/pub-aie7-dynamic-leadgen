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
            model_name="gpt-4.1-nano",
            temperature=0.1,
            max_tokens=1500,  # Reduced for faster responses
            timeout_seconds=10,  # Reduced timeout for faster responses
            **kwargs
        )
        self.llm = get_chat_model(model_name="gpt-4.1-nano", temperature=0.1)
        self.toolbelt = lead_intelligence_toolbelt
    
    def get_system_prompt(self) -> str:
        """System prompt defining the Lead Qualification Specialist role."""
        return """# LEAD QUALIFICATION SPECIALIST
You are a Lead Qualification Expert specializing in customer response analysis and lead assessment for service businesses.

## YOUR EXPERTISE
You excel at analyzing customer survey responses to determine lead quality and make strategic decisions about survey flow continuation.

## CORE COMPETENCIES

### 1. LEAD ASSESSMENT - Evaluate customer-business fit
- Analyze responses against business criteria (location, budget, needs, engagement)
- Identify red flags and qualification indicators
- Score lead quality using multiple factors
- Classify leads as: qualified, maybe, or unqualified

### 2. SURVEY FLOW DECISIONS - Optimize lead capture strategy
- Determine when to continue gathering information vs end survey
- Balance lead quality assessment with survey completion rates
- Route qualified leads through optimal question paths
- End surveys appropriately for poor-fit prospects

### 3. RESPONSE INTELLIGENCE - Extract insights from customer answers
- Identify information requiring external research (breed safety, location validation)
- Detect engagement patterns and response quality
- Recognize qualifying vs disqualifying information
- Assess authenticity and commitment level

### 4. PERSONALIZED MESSAGING - Craft appropriate completion communications
- Generate tailored messages based on lead classification
- Match tone and content to qualification level
- Use customer-specific details for personalization
- Focus on customer benefits (B2C perspective)

## DECISION-MAKING APPROACH
- **Data-driven**: Base assessments on objective response analysis
- **Strategic**: Consider business goals and lead quality thresholds
- **Customer-focused**: Maintain positive experience even for unqualified leads
- **Efficient**: Balance thoroughness with survey completion optimization

You make intelligent lead qualification decisions that maximize business ROI while maintaining excellent customer experience."""
    
    def make_decision(self, state: SurveyState, context: Dict[str, Any] = None) -> SupervisorDecision:
        """Make lead intelligence decision - delegates to process_lead_responses."""
        # This method is required by base class but we use process_lead_responses instead
        # Create a simple decision wrapper
        result = self.process_lead_responses(state)
        
        return SupervisorDecision(
            decision=result.get("lead_status", "unknown"),  # Default to unknown, not continue
            reasoning=result.get("business_reasoning", "Lead intelligence processing completed"),
            confidence=result.get("confidence", 0.5),
            recommendations=result.get("next_actions", []),
            metadata=result
        )
    
    def _get_tool_recommendation_prompt(self) -> str:
        """Clear prompt for tool recommendations with correct use cases."""
        return """# TOOL RECOMMENDATION TASK
Analyze customer responses to recommend research tools for lead scoring.

# AVAILABLE TOOLS
- **tavily**: Research information that affects lead scoring (e.g., dangerous dog breeds, product safety, industry regulations)
- **maps**: Validate locations and check if customer is in service area
- **both**: Use both tools when needed  
- **none**: No external research required

# DECISION EXAMPLES
Customer says "I have a Pit Bull" → **tavily** (research breed for scoring)
Customer mentions "I'm in Austin, TX" → **maps** (check service area)
Customer says "I have a Rottweiler in Dallas" → **both** (research breed + check location)
Customer says "I need help with my project" → **none** (no research needed)

# RESPONSE FORMAT
Respond with exactly ONE word: tavily, maps, both, or none

# DECISION CRITERIA
- Use **tavily** when answers mention things that need research for lead scoring (breeds, products, regulations, etc.)
- Use **maps** when customer provides location that needs service area validation
- Use **both** when you need research AND location checking
- Use **none** when responses don't require external research or location validation"""

    def _get_business_weight_prompt(self) -> str:
        """Business fit assessment with clear criteria and examples."""
        return """# BUSINESS FIT ASSESSMENT TASK
Analyze how well the customer fits this business based on their responses.

# FIT LEVELS & CRITERIA

**PERFECT_FIT**: Ideal customer - meets all major criteria
- In service area with reasonable budget
- Clear immediate need matching services offered  
- High engagement, detailed responses
- No obvious red flags or restrictions

**GOOD_FIT**: Strong prospect - meets most criteria  
- Good location/budget fit
- Clear need with minor concerns
- Engaged responses
- Few or minor red flags

**OKAY_FIT**: Average prospect - mixed signals
- Acceptable location/budget 
- Some service alignment
- Moderate engagement
- Some concerns but manageable

**POOR_FIT**: Weak prospect - significant issues
- Budget/location challenges
- Limited service need alignment
- Low engagement or concerning responses
- Multiple red flags

**BAD_FIT**: Wrong customer - major disqualifiers
- Outside service area or budget
- No service need alignment  
- Very low engagement or hostile
- Serious red flags (safety, legal, etc.)

# ASSESSMENT FACTORS
1. **Location**: Within service area vs too far
2. **Budget**: Aligns with service pricing vs too low
3. **Need Match**: Services needed match what's offered
4. **Engagement**: Response quality and detail level
5. **Red Flags**: Safety issues, difficult customers, legal concerns

# RESPONSE FORMAT
Respond with exactly ONE fit level: PERFECT_FIT, GOOD_FIT, OKAY_FIT, POOR_FIT, or BAD_FIT"""

    def _get_completion_message_prompt(self, lead_status: str) -> str:
        """Completion message prompt without complex conditionals."""
        # Map lead status to tone descriptions
        tone_map = {
            "yes": "Enthusiastic and welcoming",
            "maybe": "Encouraging but not pushy", 
            "no": "Kind and helpful"
        }
        tone = tone_map.get(lead_status, "Professional and friendly")
        
        return f"""# COMPLETION MESSAGE TASK
Write a personalized completion message for a {lead_status.upper()} lead.

# LEAD STATUS
{lead_status.upper()} - Use {tone.lower()} tone

# CRITICAL REQUIREMENTS
- Write for the CUSTOMER who filled out the form (B2C perspective)
- Do NOT use business-to-business language like "help your business grow"
- Focus on the SERVICE being provided TO the customer
- Use customer details from their responses to personalize
- The business context describes the SERVICE PROVIDER, not the customer

# MESSAGE GUIDELINES
- Tone: {tone}
- Audience: Customer who filled out the form
- Length: 2-3 sentences maximum
- Style: Personal using their specific responses (names, needs, preferences)
- Approach: Professional but friendly

# EXAMPLES
❌ WRONG: "Let's work together to help your business grow!"
✅ RIGHT: "We're excited to help you with your dog walking needs!"

# RESPONSE FORMAT
Write only the completion message, no other text."""
    
    def process_lead_responses(self, state: SurveyState) -> Dict[str, Any]:
        """Main entry point - processes all lead intelligence tasks."""
        try:
            logger.info("🤖 Lead Intelligence: Starting processing")
            
            # Get pending responses - but always check for completion even if no responses
            pending_responses = state.get("pending_responses", [])
            if not pending_responses:
                logger.info("No pending responses to process, checking for completion")
                # Still need to check if survey should be completed (no more questions)
                route_decision = self._determine_route_decision(state, "unknown")
                completed = route_decision == "end"
                
                if completed:
                    # Form is complete - generate completion data even without new responses
                    session_id = state.get("core", {}).get("session_id")
                    
                    # Get current lead status from database since we have no new responses to process
                    from ...database import db
                    db_session_data = db.get_lead_session(session_id)
                    current_lead_status = db_session_data.get('lead_status', 'unknown') if db_session_data else 'unknown'
                    current_score = db_session_data.get('final_score', 0) if db_session_data else 0
                    
                    # Generate completion message
                    form_id = state.get("core", {}).get("form_id")
                    business_context = self._get_business_context_from_db(form_id)
                    completion_message = self._generate_completion_message_llm(
                        current_lead_status, [], business_context  # No new responses
                    )
                    
                    # Update database with final completion
                    self.toolbelt.update_lead_status_in_database(
                        session_id=session_id,
                        lead_status=current_lead_status,
                        final_score=current_score,
                        confidence=0.8,  # Default confidence for completion
                        completion_message=completion_message
                    )
                    
                    return {
                        "lead_status": current_lead_status,
                        "final_score": current_score,
                        "completion_message": completion_message,
                        "route_decision": route_decision,
                        "completed": True,
                        "next_steps": []  # Could generate these too if needed
                    }
                
                return {
                    "lead_status": "unknown", 
                    "route_decision": route_decision,
                    "completed": completed
                }
            
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
            logger.info(f"🔥 SCORING DEBUG: score_result = {score_result}")
            final_classification = self._finalize_lead_classification(
                state,
                score_result["calculated_score"],
                comprehensive_decision,
                tool_results
            )
            logger.info(f"🔥 SCORING DEBUG: final_classification = {final_classification}")
            
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
                    # CRITICAL FIX: Update current values in addition to last_classification
                    'lead_status': final_classification.get('lead_status', 'unknown'),
                    'final_score': final_classification.get('final_score', 0),
                    'confidence': final_classification.get('confidence', 0),
                    'completion_message': final_classification.get('completion_message', ''),
                    'last_classification': final_classification,
                    'classification_timestamp': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Lead intelligence processing error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return {
                "lead_status": "unknown",
                "route_decision": "continue", 
                "error": str(e)
            }
    
    def _mark_questions_as_asked(self, state: SurveyState) -> List[int]:
        """Extract integer question_ids from responses for tracking."""
        try:
            pending_responses = state.get("pending_responses", [])
            if not pending_responses:
                return []
            
            # Simply extract integer question_ids from responses (like langgraph test does)
            asked_question_ids = []
            for response in pending_responses:
                question_id = response.get('question_id')
                if question_id is not None and question_id not in asked_question_ids:
                    asked_question_ids.append(question_id)
            
            logger.info(f"Marked {len(asked_question_ids)} questions as asked: {asked_question_ids}")
            return asked_question_ids
            
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
            # CRITICAL FIX: Use pending_responses, not lead_intelligence.responses
            # pending_responses contains the current form submission we need to score
            pending_responses = state.get("pending_responses", [])
            logger.info(f"🔥 SCORING DEBUG: pending_responses = {pending_responses}")
            
            # Also get historical responses from lead_intelligence for context
            historical_responses = state.get("lead_intelligence", {}).get("responses", [])
            logger.info(f"🔥 SCORING DEBUG: historical_responses = {historical_responses}")
            
            # Combine both for complete scoring
            all_responses = historical_responses + pending_responses
            logger.info(f"🔥 SCORING DEBUG: all_responses count = {len(all_responses)}")
            
            # Get scoring rubrics (simplified for now)
            scoring_rubrics = {}
            for response in all_responses:
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
                responses=all_responses,
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
        logger.info(f"🔥 STATUS DEBUG: session_id={session_id}, total_responses={total_responses}, final_score={final_score}")
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
        client_name = client_info.get("name", "our team")
        
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
            lead_status = "yes"
        elif final_score <= 35 and confidence >= 0.6:
            lead_status = "no"
        else:
            # Check total responses from database to determine if we need more data
            session_id = state.get("core", {}).get("session_id")
            if session_id:
                from ...database import db
                asked_questions = db.get_asked_questions(session_id)
                if len(asked_questions) < 4:  # Need at least 4 responses before classification
                    lead_status = "unknown"  # Need more data
                else:
                    lead_status = "maybe"  # Have enough data but not definitively qualified/unqualified
            else:
                lead_status = "unknown"  # No session data, need more info
        
        # Generate final completion message for definitive status
        if lead_status in ["yes", "maybe", "no"] and not decision.get("completion_message"):
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
            "completed": lead_status in ["yes", "no"] or route_decision == "end",
            "route_decision": route_decision
        }
    
    def _determine_route_decision(self, state: SurveyState, lead_status: str) -> str:
        """Determine routing decision based on lead status and available questions."""
        logger.info(f"🔀 _determine_route_decision called with lead_status={lead_status}")
        try:
            # Get session info for database queries
            session_id = state.get("core", {}).get("session_id")
            form_id = state.get("core", {}).get("form_id")
            
            if not session_id or not form_id:
                logger.warning("Missing session_id or form_id for routing decision")
                return "end"
            
            # CRITICAL FIX: Use state data instead of database queries for immediate availability
            
            # Get currently asked questions from state
            question_strategy = state.get("question_strategy", {})
            asked_questions_from_state = set(question_strategy.get("asked_questions", []))
            
            # Add newly answered questions from current pending responses
            newly_asked = self._mark_questions_as_asked(state)
            asked_questions_from_state.update(newly_asked)
            
            # Get available questions from state (provided by Survey Admin)
            all_questions_from_state = question_strategy.get("all_questions", [])
            if not all_questions_from_state:
                # Fallback to database if not in state
                from ...database import db
                all_questions_from_state = db.get_form_questions(form_id)
            
            # Calculate remaining questions
            total_questions = len(all_questions_from_state)
            asked_count = len(asked_questions_from_state)
            remaining_questions = total_questions - asked_count
            
            logger.info(f"🔀 Routing decision analysis (using state):")
            logger.info(f"   - Total questions: {total_questions}")
            logger.info(f"   - Asked questions: {sorted(list(asked_questions_from_state))}")
            logger.info(f"   - Remaining questions: {remaining_questions}")
            logger.info(f"   - Lead status: {lead_status}")
            
            # CONSOLIDATED COMPLETION LOGIC - All completion criteria in one place
            
            # Get current step for business rules
            db_session = self.toolbelt.get_lead_session(session_id) if session_id else None
            current_step = db_session.get("step", 0) if db_session else 0
            
            logger.info(f"🔍 Completion analysis - step: {current_step}, lead_status: {lead_status}, remaining: {remaining_questions}")
            
            # Rule 1: If step < 2, always continue (need minimum engagement)
            if current_step < 2:
                route_decision = "continue"
                logger.info("📋 Step < 2 - continue for minimum engagement")
            
            # Rule 2: If step 2+ and lead_status is "no", end (qualified out)
            elif current_step >= 2 and lead_status == "no":
                route_decision = "end"
                logger.info("🏁 Step 2+ and 'no' lead - end (qualified out)")
            
            # Rule 3: If no questions remain, end (survey exhausted)
            elif remaining_questions == 0:
                route_decision = "end"
                logger.info("🏁 No more questions available - end")
            
            # Rule 4: If definitive classification (yes/no), end
            elif lead_status in ["yes", "no"]:
                route_decision = "end"
                logger.info(f"🏁 Definitive lead status ({lead_status}) - end")
            
            # Rule 5: Otherwise continue (unknown/maybe with questions remaining)
            else:
                route_decision = "continue"
                logger.info(f"📋 {lead_status} status with {remaining_questions} questions - continue")
                
            logger.info(f"🔀 Routing decision: {route_decision}")
            return route_decision
            
        except Exception as e:
            logger.error(f"Error determining route decision: {e}")
            return "end"  # Safe default
    
    def _get_completion_decision(self, state: SurveyState, lead_status: str) -> str:
        """Determine if survey should continue or end based on step number and required questions."""
        try:
            # Get current step number
            session_id = state.get("core", {}).get("session_id")
            if not session_id:
                logger.warning("No session_id - defaulting to continue")
                return "continue"
            
            db_session = self.toolbelt.get_lead_session(session_id)
            if not db_session:
                logger.warning(f"No database session found for {session_id} - defaulting to continue")
                return "continue"
            
            current_step = db_session.get("step", 0)
            logger.info(f"🔍 Completion decision - step: {current_step}, lead_status: {lead_status}")
            
            # Rule 1: If step number is less than 2, always continue
            if current_step < 2:
                logger.info("📋 Step < 2 - continue")
                return "continue"
            
            # Rule 2: If step 2+ and lead_status is "no", end and show message
            if current_step >= 2 and lead_status == "no":
                logger.info("🏁 Step 2+ and 'no' lead - end")
                return "end"
            
            # Rule 3: If step 2+ and required questions remain, always continue
            if current_step >= 2:
                all_required_answered = self._all_required_questions_answered(state)
                if not all_required_answered:
                    logger.info("📋 Required questions remain - continue")
                    return "continue"
            
            # Rule 4: If step 2+, all required answered, continue if maybe/unknown
            if current_step >= 2 and lead_status in ["maybe", "unknown"]:
                logger.info("🤔 Step 2+, all required done, maybe/unknown - continue")
                return "continue"
            
            # Default: end
            logger.info("🏁 Default case - end")
            return "end"
            
        except Exception as e:
            logger.error(f"Error in completion decision: {e}")
            return "continue"  # Safe default
    
    def _all_required_questions_answered(self, state: SurveyState) -> bool:
        """Check if all required questions have been answered."""
        try:
            # Get form_id and load questions
            form_id = state.get("core", {}).get("form_id")
            if not form_id:
                logger.warning("No form_id found - cannot check required questions")
                return False
            
            # Load all questions for this form
            all_questions = self.toolbelt.load_questions({"form_id": form_id})
            if not all_questions:
                logger.warning(f"No questions found for form {form_id}")
                return True  # If no questions, consider complete
            
            # Get questions that have been asked
            asked_questions = state.get("question_strategy", {}).get("asked_questions", [])
            asked_question_ids = set()
            for q_id in asked_questions:
                if isinstance(q_id, (int, str)):
                    asked_question_ids.add(int(q_id))
            
            # Check required questions
            required_questions = []
            for question in all_questions:
                if question.get("required", False):
                    required_questions.append(question.get("question_id"))
            
            unanswered_required = []
            for req_id in required_questions:
                if req_id not in asked_question_ids:
                    unanswered_required.append(req_id)
            
            all_answered = len(unanswered_required) == 0
            logger.info(f"📋 Required questions check:")
            logger.info(f"   - Total required: {len(required_questions)}")
            logger.info(f"   - Asked: {len(required_questions) - len(unanswered_required)}")
            logger.info(f"   - Unanswered required: {unanswered_required}")
            logger.info(f"   - All answered: {all_answered}")
            
            return all_answered
            
        except Exception as e:
            logger.error(f"Error checking required questions: {e}")
            return False  # Conservative - don't complete if we can't verify
    
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
            from ...database import db
            
            # Get form and client info
            form = db.get_form(form_id)
            if not form or not form.get('client_id'):
                return "General service business"
            
            client = db.get_client(form['client_id'])
            if not client:
                return "General service business"
            
            # Build context string
            context_parts = []
            
            if client.get('name'):
                context_parts.append(f"Business: {client['name']}")
            
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
        # Lead status should be one of: unknown, maybe, yes, no (matching langgraph_test)
        # Routing is handled separately
        
        if num_responses < 3:
            return "unknown"  # Insufficient data
        
        if final_score >= 75:
            return "yes"  # Qualified (changed from "qualified" to match test)
        elif final_score >= 40:
            return "maybe"  # Maybe qualified
        else:
            return "no"  # Not qualified
    
    def _get_total_responses_count(self, session_id: str) -> int:
        """Get total response count from database."""
        try:
            from ...database import db
            # Use get_asked_questions as a proxy for response count
            asked_questions = db.get_asked_questions(session_id)
            return len(asked_questions) if asked_questions else 0
        except Exception as e:
            logger.error(f"Error getting response count: {e}")
            return 0
    
    def _update_database_status(self, state: SurveyState, classification: Dict):
        """Update database with final lead status and create lead outcome record when ending."""
        try:
            session_id = state.get("core", {}).get("session_id")
            
            # Always update the lead session status
            self.toolbelt.update_lead_status_in_database(
                session_id=session_id,
                lead_status=classification["lead_status"],
                final_score=classification["final_score"],
                confidence=classification["confidence"],
                completion_message=classification.get("completion_message")
            )
            
            # CRITICAL FIX: Create lead outcome record when survey is ending
            route_decision = classification.get("route_decision", "continue")
            if route_decision == "end" or classification.get("completed", False):
                self._create_lead_outcome_record(state, classification)
                
        except Exception as e:
            logger.error(f"Database update error: {e}")
    
    def _create_lead_outcome_record(self, state: SurveyState, classification: Dict):
        """Create a lead outcome record for completed surveys."""
        try:
            from ...database import db
            
            # Get session and form information
            core = state.get("core", {})
            session_id = core.get("session_id")
            form_id = core.get("form_id")
            
            # Get session record from database for client_id and session database ID
            session_record = db.get_lead_session(session_id)
            if not session_record:
                logger.error(f"No session record found for {session_id} - cannot create lead outcome")
                return
            
            session_db_id = session_record.get("id")  # Database UUID
            client_id = session_record.get("client_id")
            
            # Map lead status to outcome status for lead_outcomes table
            lead_status = classification["lead_status"]
            if lead_status == "yes":
                final_status = "qualified"
            elif lead_status == "maybe":
                final_status = "maybe"
            elif lead_status == "no":
                final_status = "unqualified"
            else:  # unknown or error states
                # Keep unknown status as unknown, don't default to unqualified
                logger.warning(f"Survey ended with unknown lead status: {lead_status}")
                return  # Don't create lead outcome for unknown status
            
            # Extract contact information from responses
            contact_info = self._extract_contact_info(state)
            
            # Determine notification requirements
            notification_required = final_status in ["qualified", "maybe"]
            notification_method = "email" if notification_required else None
            
            # Create lead outcome record
            outcome_data = {
                "session_id": session_db_id,  # Use database UUID, not session_id string
                "client_id": client_id,
                "form_id": form_id,
                "final_status": final_status,
                "contact_info": contact_info,
                "lead_score": classification["final_score"],
                "confidence_score": classification.get("confidence", 0.0),
                "notification_sent": False,  # Will be updated when notification is actually sent
                "notification_method": notification_method,
                "follow_up_required": notification_required,
                "follow_up_date": None  # Can be set by business logic later
            }
            
            result = db.create_lead_outcome(outcome_data)
            logger.info(f"✅ Created lead outcome record: {result.get('id')} for session {session_id} with status {final_status}")
            
        except Exception as e:
            logger.error(f"Failed to create lead outcome record: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
    
    def _extract_contact_info(self, state: SurveyState) -> Dict[str, Any]:
        """Extract contact information from survey responses."""
        try:
            contact_info = {}
            
            # Get all responses from the lead intelligence state
            all_responses = state.get("lead_intelligence", {}).get("responses", [])
            
            for response in all_responses:
                question_text = response.get("question_text", "").lower()
                answer = response.get("answer", "").strip()
                
                if not answer:
                    continue
                
                # Extract common contact fields
                if "name" in question_text and not contact_info.get("name"):
                    contact_info["name"] = answer
                elif "email" in question_text and not contact_info.get("email"):
                    contact_info["email"] = answer
                elif "phone" in question_text and not contact_info.get("phone"):
                    contact_info["phone"] = answer
                elif "address" in question_text and not contact_info.get("address"):
                    contact_info["address"] = answer
                elif "company" in question_text and not contact_info.get("company"):
                    contact_info["company"] = answer
            
            return contact_info
            
        except Exception as e:
            logger.error(f"Failed to extract contact info: {e}")
            return {}
    
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