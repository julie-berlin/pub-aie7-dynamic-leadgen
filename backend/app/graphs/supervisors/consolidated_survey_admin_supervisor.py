"""Consolidated Survey Administration Supervisor - All survey flow logic in one place."""

from __future__ import annotations
from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime

from .base_supervisor import SupervisorAgent, SupervisorDecision
from ...state import SurveyState
from ...models import get_chat_model

logger = logging.getLogger(__name__)


class ConsolidatedSurveyAdminSupervisor(SupervisorAgent):
    """Consolidated supervisor handling all survey administration tasks."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="ConsolidatedSurveyAdminSupervisor",
            model_name="gpt-4o-mini",
            temperature=0.3,
            max_tokens=4000,
            timeout_seconds=60,
            **kwargs
        )
        self.llm = get_chat_model(model_name="gpt-4o-mini", temperature=0.3)
    
    def make_decision(self, state: SurveyState, context: Dict[str, Any] = None) -> SupervisorDecision:
        """Make strategic survey administration decision - delegates to process_survey_step."""
        # This method is required by base class but we use process_survey_step instead
        # Create a simple decision wrapper
        result = self.process_survey_step(state)
        
        return SupervisorDecision(
            decision=result.get("step_type", "continue"),
            reasoning="Survey administration processing completed",
            confidence=0.8,
            recommendations=[],
            metadata=result
        )
    
    def get_system_prompt(self) -> str:
        """Comprehensive system prompt for all survey administration tasks."""
        return """You are an advanced Survey Administration AI that handles all aspects of intelligent survey flow.

Your integrated responsibilities include:
1. STRATEGIC DECISIONS: Analyze responses and decide survey continuation
2. QUESTION SELECTION: Choose optimal 1-3 questions from available pool
3. QUESTION PHRASING: Rewrite questions for better engagement
4. ENGAGEMENT MESSAGING: Add motivational elements to prevent abandonment
5. FRONTEND PREPARATION: Format everything for user presentation

SELECTION CRITERIA:
- Never repeat already-asked questions
- Follow business rules and requirements
- Maintain logical conversation flow
- Balance information gain with user experience
- Respect required questions but time them well

PHRASING GUIDELINES:
- Make questions conversational and natural
- Use "you" language to be personal
- Show why each question matters
- Remove jargon and technical terms

ENGAGEMENT TACTICS:
- Show progress indicators when appropriate
- Add value reinforcement messages
- Provide encouragement for at-risk users
- Create urgency only when abandonment risk is high

OUTPUT FORMAT:
Return a comprehensive JSON response with ALL components:
{
  "action": "continue" | "complete",
  "reasoning": "strategic explanation",
  "confidence": 0.0-1.0,
  "selected_questions": [
    {
      "id": 1,
      "original_text": "original question",
      "phrased_text": "engaging rewritten version",
      "engagement_enhanced": "final version with motivation",
      "question_type": "type",
      "is_required": false
    }
  ],
  "engagement_message": "motivational message before questions",
  "completion_motivation": "what happens after completion",
  "progress_indicator": "X% complete",
  "metadata": {
    "questions_selected": 2,
    "risk_level": "low|medium|high",
    "engagement_approach": "motivational|casual|urgent",
    "expected_response_time": "30-60 seconds"
  }
}"""
    
    def process_survey_step(self, state: SurveyState) -> Dict[str, Any]:
        """Main entry point - processes entire survey administration step."""
        try:
            logger.info(f"Starting survey administration processing for state: {type(state)}")
            logger.debug(f"State keys: {list(state.keys()) if isinstance(state, dict) else 'Not a dict'}")
            
            # Load available questions
            available_questions = self._load_available_questions(state)
            if not available_questions:
                logger.warning("No available questions found, completing survey")
                return self._create_completion_response("No more questions available")
            
            # Analyze current state
            analysis = self._analyze_survey_state(state, available_questions)
            logger.debug(f"State analysis: {analysis}")
            
            # Make comprehensive decision
            decision = self._make_comprehensive_decision(state, available_questions, analysis)
            logger.debug(f"Decision made: {decision.get('action', 'unknown')}")
            
            # Prepare frontend response
            frontend_data = self._prepare_frontend_response(decision, state)
            logger.info(f"Survey admin processing completed successfully")
            
            return frontend_data
            
        except Exception as e:
            logger.error(f"Survey admin processing error: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return self._create_error_response(str(e))
    
    def _load_available_questions(self, state: SurveyState) -> List[Dict]:
        """Load and filter available questions."""
        try:
            # Get form_id from state
            core = state.get('core', {})
            form_id = core.get('form_id', 'default_form')
            
            logger.debug(f"Loading questions for form_id: {form_id}")
            
            # Load all questions
            from ...utils.cached_data_loader import data_loader
            all_questions = data_loader.get_questions(form_id)
            
            logger.debug(f"Loaded {len(all_questions) if all_questions else 0} total questions")
            
            # Get already asked questions
            question_strategy = state.get('question_strategy', {})
            asked_ids = question_strategy.get('asked_questions', [])
            
            logger.debug(f"Already asked question IDs: {asked_ids}")
            
            # Filter to available questions
            available_questions = [q for q in all_questions if q.get('id') not in asked_ids]
            
            logger.info(f"Loaded {len(available_questions)} available questions for form {form_id}")
            return available_questions
            
        except Exception as e:
            logger.error(f"Failed to load questions: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return []
    
    def _analyze_survey_state(self, state: SurveyState, available_questions: List[Dict]) -> Dict[str, Any]:
        """Analyze current survey state for decision making."""
        responses = state.get('lead_intelligence', {}).get('responses', [])
        timing_data = state.get('timing_data', {})
        
        # Calculate engagement metrics
        questions_asked = len(responses)
        response_depth = self._calculate_response_depth(responses)
        time_on_form = timing_data.get('total_time', 0)
        
        # Calculate abandonment risk
        risk_score = 0.0
        if questions_asked > 8:
            risk_score += 0.3
        if response_depth < 0.5:
            risk_score += 0.4
        if time_on_form > 300:  # 5 minutes
            risk_score += 0.3
        
        risk_level = "high" if risk_score > 0.7 else "medium" if risk_score > 0.4 else "low"
        
        # Determine progress
        estimated_total = 10  # Default estimate
        progress_percentage = min(90, (questions_asked / estimated_total) * 100)
        
        return {
            "questions_asked": questions_asked,
            "available_count": len(available_questions),
            "response_depth": response_depth,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "progress_percentage": progress_percentage,
            "time_on_form": time_on_form
        }
    
    def _calculate_response_depth(self, responses: List[Dict]) -> float:
        """Calculate average response depth/quality."""
        if not responses:
            return 0.0
        
        total_depth = 0.0
        for response in responses:
            answer = response.get("answer", "")
            if len(answer.strip()) > 50:
                total_depth += 1.0
            elif len(answer.strip()) > 15:
                total_depth += 0.5
            else:
                total_depth += 0.1
        
        return total_depth / len(responses)
    
    def _make_comprehensive_decision(
        self, 
        state: SurveyState, 
        available_questions: List[Dict],
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Make comprehensive decision including selection, phrasing, and engagement."""
        
        # Prepare context for LLM
        responses = state.get('lead_intelligence', {}).get('responses', [])
        client_info = state.get('client_info', {})
        business_name = client_info.get('business_name', 'our business')
        industry = client_info.get('industry', 'service business')
        
        # Create numbered question list for LLM
        numbered_questions = []
        for i, q in enumerate(available_questions[:15], 1):  # Limit to 15 for context
            numbered_questions.append({
                "number": i,
                "question_text": q.get("question_text", ""),
                "question_type": q.get("question_type", ""),
                "is_required": q.get("is_required", False),
                "category": q.get("category", "")
            })
        
        # Determine recommended approach based on analysis
        if analysis["risk_level"] == "high":
            recommended_count = 1
            engagement_approach = "urgent"
            phrasing_tone = "encouraging"
        elif analysis["risk_level"] == "medium":
            recommended_count = 2
            engagement_approach = "motivational"
            phrasing_tone = "friendly"
        else:
            recommended_count = 2 if analysis["questions_asked"] < 5 else 3
            engagement_approach = "casual"
            phrasing_tone = "conversational"
        
        user_prompt = f"""Process this survey step comprehensively:

BUSINESS CONTEXT:
- Business: {business_name}
- Industry: {industry}
- Questions asked so far: {analysis['questions_asked']}
- User engagement risk: {analysis['risk_level']}
- Progress: {analysis['progress_percentage']:.0f}%

RECENT RESPONSES (last 3):
{json.dumps(responses[-3:] if responses else [], indent=2)}

AVAILABLE QUESTIONS (numbered):
{json.dumps(numbered_questions, indent=2)}

REQUIREMENTS:
1. SELECT {recommended_count} questions that best advance the conversation
2. REPHRASE them to be engaging and personal for {business_name}
3. ADD engagement elements based on {analysis['risk_level']} risk level
4. CREATE a motivational message for this step
5. Use {phrasing_tone} tone and {engagement_approach} engagement approach

Provide the complete JSON response with selected, phrased, and engagement-enhanced questions."""
        
        # Get LLM response
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
            
            logger.debug(f"LLM response content: {llm_content}")
            
            if not llm_content or not llm_content.strip():
                logger.error("LLM returned empty response")
                return self._create_fallback_decision(available_questions, analysis)
            
            decision_data = json.loads(llm_content)
            
            # Map selected question numbers to actual questions
            selected_questions = []
            for q_data in decision_data.get("selected_questions", []):
                # Handle both formats: direct questions and numbered references
                if "number" in q_data:
                    # Map from number to actual question
                    number = q_data["number"]
                    if 1 <= number <= len(available_questions):
                        original_q = available_questions[number - 1]
                        selected_questions.append({
                            **original_q,
                            "phrased_text": q_data.get("phrased_text", original_q.get("question_text")),
                            "final_text": q_data.get("engagement_enhanced", q_data.get("phrased_text", original_q.get("question_text")))
                        })
                else:
                    # Direct question data
                    selected_questions.append(q_data)
            
            # Ensure we have valid questions
            if not selected_questions and available_questions:
                # Fallback: select first 1-2 questions
                selected_questions = available_questions[:min(2, len(available_questions))]
                for q in selected_questions:
                    q["phrased_text"] = q.get("question_text")
                    q["final_text"] = q.get("question_text")
            
            return {
                "action": decision_data.get("action", "continue"),
                "selected_questions": selected_questions,
                "engagement_message": decision_data.get("engagement_message", ""),
                "completion_motivation": decision_data.get("completion_motivation", ""),
                "progress_indicator": decision_data.get("progress_indicator", f"{analysis['progress_percentage']:.0f}% complete"),
                "metadata": {
                    **decision_data.get("metadata", {}),
                    "analysis": analysis,
                    "llm_decision": True
                }
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return self._create_fallback_decision(available_questions, analysis)
        except Exception as e:
            logger.error(f"LLM decision error: {e}")
            return self._create_fallback_decision(available_questions, analysis)
    
    def _create_fallback_decision(self, available_questions: List[Dict], analysis: Dict) -> Dict[str, Any]:
        """Create fallback decision when LLM fails."""
        # Simple rule-based selection
        count = 2 if analysis["risk_level"] != "high" else 1
        selected = available_questions[:count]
        
        for q in selected:
            q["phrased_text"] = q.get("question_text")
            q["final_text"] = q.get("question_text")
        
        engagement_message = "Let's continue with a few more questions."
        if analysis["risk_level"] == "high":
            engagement_message = "Almost done! Just one more quick question."
        
        return {
            "action": "continue",
            "selected_questions": selected,
            "engagement_message": engagement_message,
            "completion_motivation": "We'll review your information and get back to you soon!",
            "progress_indicator": f"{analysis['progress_percentage']:.0f}% complete",
            "metadata": {
                "fallback": True,
                "analysis": analysis
            }
        }
    
    def _prepare_frontend_response(self, decision: Dict, state: SurveyState) -> Dict[str, Any]:
        """Prepare the final response for frontend consumption."""
        # Update state with selected questions
        question_strategy = state.get('question_strategy', {})
        asked_questions = question_strategy.get('asked_questions', [])
        
        # Add newly selected question IDs to asked list
        for q in decision["selected_questions"]:
            if q.get("id") not in asked_questions:
                asked_questions.append(q.get("id"))
        
        # Format questions for frontend
        frontend_questions = []
        for q in decision["selected_questions"]:
            frontend_questions.append({
                "id": q.get("id"),
                "text": q.get("final_text", q.get("question_text")),
                "type": q.get("question_type", "text"),
                "options": q.get("options", []),
                "required": q.get("is_required", False),
                "placeholder": q.get("placeholder", ""),
                "validation": q.get("validation", {})
            })
        
        # Get session_id from core state
        core = state.get('core', {})
        session_id = core.get('session_id')
        
        # Prepare the frontend response data
        frontend_data = {
            "session_id": session_id,
            "step": 1,  # Will be updated by the system
            "questions": frontend_questions,
            "question_metadata": frontend_questions,
            "headline": decision.get("engagement_message", "Let's continue!"),
            "motivation": decision.get("completion_motivation", "Thank you for your time."),
            "progress": {
                "current_step": 1,
                "estimated_remaining": 3
            }
        }
        
        return {
            # This is the key the API is looking for
            "frontend_response": frontend_data,
            
            # Core response
            "step_type": "questions" if decision["action"] == "continue" else "completion",
            "questions": frontend_questions,
            "engagement": {
                "message": decision["engagement_message"],
                "progress": decision["progress_indicator"],
                "motivation": decision["completion_motivation"]
            },
            
            # State updates
            "question_strategy": {
                **question_strategy,
                "asked_questions": asked_questions,
                "current_questions": frontend_questions,
                "selection_confidence": decision.get("confidence", 0.7)
            },
            
            # Metadata
            "supervisor_metadata": {
                "supervisor_name": self.name,
                "model_used": self.model_name,
                "decision_timestamp": datetime.now().isoformat(),
                "action": decision["action"],
                "analysis": decision["metadata"].get("analysis", {}),
                "llm_decision": decision["metadata"].get("llm_decision", False)
            }
        }
    
    def _create_completion_response(self, reason: str) -> Dict[str, Any]:
        """Create a completion response when survey should end."""
        return {
            "step_type": "completion",
            "questions": [],
            "engagement": {
                "message": "Thank you for completing our survey!",
                "progress": "100% complete",
                "motivation": reason
            },
            "supervisor_metadata": {
                "supervisor_name": self.name,
                "completion_reason": reason,
                "decision_timestamp": datetime.now().isoformat()
            }
        }
    
    def _create_error_response(self, error: str) -> Dict[str, Any]:
        """Create an error response."""
        return {
            "step_type": "error",
            "questions": [],
            "error": error,
            "supervisor_metadata": {
                "supervisor_name": self.name,
                "error_timestamp": datetime.now().isoformat()
            }
        }


def consolidated_survey_admin_node(state: SurveyState) -> Dict[str, Any]:
    """Node function for Consolidated Survey Administration Supervisor."""
    supervisor = ConsolidatedSurveyAdminSupervisor()
    return supervisor.process_survey_step(state)