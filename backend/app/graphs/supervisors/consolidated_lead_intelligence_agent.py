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
    
    def get_system_prompt(self) -> str:
        """Comprehensive system prompt for all lead intelligence tasks."""
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
- Use Tavily for: Industry research, service validation, safety checks
- Use Google Maps for: Distance validation, service area checks
- Only use tools when they add significant value to qualification

MESSAGE TONE BY STATUS:
- Qualified: Enthusiastic, welcoming, action-oriented
- Maybe: Encouraging, helpful, non-pushy
- No: Kind, respectful, helpful with alternatives
- Continue: Motivational, progress-focused

OUTPUT FORMAT:
Return comprehensive JSON with all processing results:
{
  "lead_status": "qualified" | "maybe" | "no" | "continue",
  "final_score": 85,
  "confidence": 0.85,
  "score_adjustment": 0,
  "validation_action": "APPROVE" | "ADJUST_UP" | "ADJUST_DOWN",
  "tools_needed": ["tavily_search", "google_maps"] | [],
  "tool_queries": {
    "tavily_search": "search query",
    "google_maps": {"origin": "address", "destination": "address"}
  },
  "completion_message": "personalized message based on status",
  "business_reasoning": "detailed explanation",
  "key_factors": ["positive1", "positive2"],
  "red_flags": ["concern1"] | [],
  "next_actions": ["action1", "action2"],
  "requires_follow_up": true | false
}"""
    
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
        """Make comprehensive decision including tool usage and classification."""
        
        responses = state.get("lead_intelligence", {}).get("responses", [])
        client_info = state.get("client_info", {})
        business_rules = state.get("business_rules", {})
        
        # Analyze tool requirements
        tool_analysis = self.toolbelt.analyze_tool_requirements(
            responses=responses,
            client_info=client_info,
            business_rules=business_rules
        )
        
        # Prepare LLM prompt
        user_prompt = f"""Analyze this lead comprehensively and make all processing decisions:

LEAD DATA:
- Calculated Score: {calculated_score}/100
- Total Responses: {len(responses)}
- Business: {client_info.get('business_name', 'Unknown')} ({client_info.get('industry', 'Unknown')})
- Service Area: {client_info.get('service_area', 'Not specified')}

RESPONSES:
{json.dumps(responses, indent=2)}

TOOL ANALYSIS:
{json.dumps(tool_analysis, indent=2)}

BUSINESS RULES:
{json.dumps(business_rules, indent=2)}

Make a comprehensive decision including:
1. Whether to use external validation tools
2. Initial lead classification
3. Score validation (does {calculated_score} make sense?)
4. Personalized completion message
5. Next actions for this lead"""
        
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = self.llm.invoke(messages)
            
            if hasattr(response, 'content'):
                llm_content = response.content
            else:
                llm_content = str(response)
            
            decision_data = json.loads(llm_content)
            
            # Ensure all required fields
            return {
                "lead_status": decision_data.get("lead_status", "continue"),
                "final_score": decision_data.get("final_score", calculated_score),
                "confidence": decision_data.get("confidence", 0.5),
                "score_adjustment": decision_data.get("score_adjustment", 0),
                "validation_action": decision_data.get("validation_action", "APPROVE"),
                "tools_needed": decision_data.get("tools_needed", []),
                "tool_queries": decision_data.get("tool_queries", {}),
                "completion_message": decision_data.get("completion_message", ""),
                "business_reasoning": decision_data.get("business_reasoning", ""),
                "key_factors": decision_data.get("key_factors", []),
                "red_flags": decision_data.get("red_flags", []),
                "next_actions": decision_data.get("next_actions", []),
                "requires_follow_up": decision_data.get("requires_follow_up", False)
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return self._create_fallback_decision(calculated_score, responses)
        except Exception as e:
            logger.error(f"LLM decision error: {e}")
            return self._create_fallback_decision(calculated_score, responses)
    
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
            messages = self.toolbelt.generate_default_messages(lead_status, client_name)
            decision["completion_message"] = messages.get(lead_status, "Thank you for your responses.")
        
        # Determine next actions
        if not decision.get("next_actions"):
            decision["next_actions"] = self.toolbelt.determine_next_actions(
                lead_status, confidence, final_score
            )
        
        return {
            **decision,
            "lead_status": lead_status,
            "final_score": final_score,
            "confidence": confidence,
            "tool_results": tool_results,
            "completed": lead_status != "continue"
        }
    
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
            lead_status = "continue"
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