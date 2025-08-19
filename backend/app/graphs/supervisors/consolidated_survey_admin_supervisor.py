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
- CRITICAL: Each question must ask for EXACTLY ONE piece of information only
- NEVER combine multiple data points in a single question (e.g., "name and breed")

PHRASING GUIDELINES:
- Make questions conversational and natural
- Use "you" language to be personal
- Show why each question matters
- Remove jargon and technical terms
- CRITICAL: If a question asks for multiple pieces of information, split it into separate questions
- Each input field should capture exactly one data point

ENGAGEMENT TACTICS:
- Show progress indicators when appropriate
- Add value reinforcement messages  
- Provide encouragement for at-risk users
- Create urgency only when abandonment risk is high
- Include company personality and service details
- Reference specific products/services that benefit the user
- Make it feel personal and conversational
- NEVER suggest this is the "last step" or "final questions"
- Always encourage completion with positive, forward-looking language

OUTPUT FORMAT:
Return a structured markdown response with sections:

## DECISION
Action: continue
Reasoning: [strategic explanation]
Confidence: [0.0-1.0]

## SELECTED QUESTIONS
### Question 1: [number]
- Original: [original text]
- Phrased: [engaging rewritten version]
- Required: [true/false]

### Question 2: [number]
- Original: [original text] 
- Phrased: [engaging rewritten version]
- Required: [true/false]

## ENGAGEMENT
### Headline
[Compelling H2 headline about this step]

### Message
[Rich paragraph with company personality, services, and motivation to continue]

## METADATA
- Questions Selected: [count]
- Risk Level: [low/medium/high]
- Approach: [motivational/casual/urgent]"""
    
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
            logger.info(f"About to call _make_comprehensive_decision with {len(available_questions)} questions")
            
            # Make comprehensive decision
            logger.info("🔥 CALLING _make_comprehensive_decision")
            decision = self._make_comprehensive_decision(state, available_questions, analysis)
            logger.info("🔥 RETURNED FROM _make_comprehensive_decision")
            logger.info(f"Decision completed: action={decision.get('action', 'unknown')}, questions={len(decision.get('selected_questions', []))}")
            logger.debug(f"Decision metadata: {decision.get('metadata', {})}")
            
            # Prepare frontend response
            frontend_data = self._prepare_frontend_response(decision, state)
            logger.info(f"Survey admin processing completed successfully")
            
            return frontend_data
            
        except Exception as e:
            logger.error(f"Survey admin processing error: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return self._create_error_response(str(e))
    
    def _load_form_details(self, form_id: str) -> Dict[str, Any]:
        """Load form details from database."""
        try:
            from ...database import db
            form_config = db.get_form(form_id)
            if form_config:
                return {
                    "id": form_id,
                    "title": form_config.get('title', 'Survey Form'),
                    "description": form_config.get('description'),
                    "client_id": form_config.get('client_id')
                }
            else:
                logger.warning(f"Form {form_id} not found in database")
                return {
                    "id": form_id,
                    "title": "Survey Form",
                    "description": None,
                    "client_id": None
                }
        except Exception as e:
            logger.error(f"Failed to load form details for {form_id}: {e}")
            return {
                "id": form_id,
                "title": "Survey Form", 
                "description": None,
                "client_id": None
            }
    
    def _load_available_questions(self, state: SurveyState) -> List[Dict]:
        """Load and filter available questions."""
        try:
            # Get form_id from state
            core = state.get('core', {})
            form_id = core.get('form_id', 'default_form')
            
            logger.debug(f"Loading questions for form_id: {form_id}")
            
            # Load all questions
            from ...utils.cached_data_loader import data_loader
            logger.debug(f"Data loader type: {type(data_loader)}")
            
            try:
                all_questions = data_loader.get_questions(form_id)
                logger.debug(f"Questions returned: {type(all_questions)}, length: {len(all_questions) if all_questions else 0}")
                if all_questions:
                    logger.debug(f"Sample question: {all_questions[0] if len(all_questions) > 0 else 'None'}")
            except Exception as e:
                logger.error(f"Error loading questions: {e}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                all_questions = []
            
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
        
        logger.info("🔥 ENTERED _make_comprehensive_decision")
        logger.info("Starting comprehensive decision making...")
        
        try:
            # Prepare context for LLM
            responses = state.get('lead_intelligence', {}).get('responses', [])
            
            # Load client info if not already in state
            core = state.get('core', {})
            form_id = core.get('form_id')
            client_info = state.get('client_info', {})
            if not client_info:
                try:
                    from ...tools import load_client_info
                    client_json = load_client_info.invoke({'form_id': form_id})
                    client_info = json.loads(client_json) if client_json else {}
                    logger.debug(f"Loaded client info: {bool(client_info)}")
                except Exception as e:
                    logger.warning(f"Failed to load client info: {e}")
                    client_info = {}
                    # Continue with default values instead of failing
            
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
            
            # Get detailed client info for engagement
            client_data = client_info.get('client', {}) if client_info else {}
            business_background = client_data.get('background', '')
            business_goals = client_data.get('goals', '')
            target_audience = client_data.get('target_audience', '')
            
            user_prompt = f"""Process this survey step comprehensively:

BUSINESS CONTEXT:
- Business: {business_name}
- Industry: {industry}
- Background: {business_background[:200]}...
- Business Goals: {business_goals[:200]}...
- Target Audience: {target_audience[:200]}...
- Questions asked so far: {analysis['questions_asked']}
- User engagement risk: {analysis['risk_level']}
- Progress: {analysis['progress_percentage']:.0f}%

RECENT RESPONSES (last 3):
{json.dumps(responses[-3:] if responses else [], indent=2)}

AVAILABLE QUESTIONS (numbered):
{json.dumps(numbered_questions, indent=2)}

REQUIREMENTS:
1. SELECT {recommended_count} questions that best advance the conversation
2. ENSURE each question asks for EXACTLY ONE piece of information only
3. REPHRASE them to be engaging and personal for {business_name}
4. SPLIT any compound questions into separate single-purpose questions
5. CREATE an engaging H2 headline that relates to this step and {business_name}'s services
6. WRITE a compelling paragraph that:
   - Mentions specific services/benefits from {business_name}
   - Shows personality and builds trust
   - Encourages completion with positive language
   - References the business background/goals appropriately
   - NEVER suggests this is the "last step" or ending soon
7. Use {phrasing_tone} tone and {engagement_approach} engagement approach

CRITICAL RULES: 
- Never ask for multiple data points in one question (e.g., "name and breed" should be two separate questions)
- Always sound encouraging and forward-looking, never like the survey is ending

Provide the complete JSON response with selected, phrased, and engagement-enhanced questions."""
            
            # Get LLM response
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": user_prompt}
            ]
            
            logger.info("Calling LLM for question selection and rephrasing...")
            response = self.llm.invoke(messages)
            
            if hasattr(response, 'content'):
                llm_content = response.content
            else:
                llm_content = str(response)
            
            logger.info(f"LLM response received, length: {len(llm_content)}")
            # Log first 1000 chars to avoid truncation in logs
            logger.info(f"🔥 LLM RAW START: {llm_content[:1000]}")
            if len(llm_content) > 1000:
                logger.info(f"🔥 LLM RAW MIDDLE: {llm_content[1000:2000]}")
            if len(llm_content) > 2000:
                logger.info(f"🔥 LLM RAW END: {llm_content[2000:]}")
            logger.debug(f"LLM response content: {llm_content[:500]}...")
            
            if not llm_content or not llm_content.strip():
                logger.error("LLM returned empty response")
                return self._create_fallback_decision(available_questions, analysis)
            
            # Parse markdown response from LLM
            logger.info("Parsing LLM markdown response...")
            decision_data = self._parse_markdown_response(llm_content, available_questions)
            logger.info(f"Parsed {len(decision_data.get('selected_questions', []))} questions from LLM")
            
            # Debug parsed questions
            for i, q in enumerate(decision_data.get('selected_questions', [])):
                original_text = q.get('question_text', 'NO_ORIGINAL')
                final_text = q.get('final_text', 'NO_FINAL')
                phrased_text = q.get('phrased_text', 'NO_PHRASED')
                logger.info(f"🔥 Q{i+1}: orig='{original_text}', final='{final_text}', phrased='{phrased_text}'")
            
            return {
                "action": decision_data.get("action", "continue"),
                "selected_questions": decision_data.get("selected_questions", []),
                "engagement_headline": decision_data.get("engagement_headline", "Let's get to know you better!"),
                "engagement_message": decision_data.get("engagement_message", ""),
                "progress_indicator": decision_data.get("progress_indicator", f"{analysis['progress_percentage']:.0f}% complete"),
                "completion_motivation": decision_data.get("completion_motivation", "Thank you for your responses!"),
                "metadata": {
                    **decision_data.get("metadata", {}),
                    "analysis": analysis,
                    "llm_decision": True
                }
            }
            
        except Exception as e:
            logger.error(f"Comprehensive decision error: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return self._create_fallback_decision(available_questions, analysis)
    
    def _parse_markdown_response(self, content: str, available_questions: List[Dict]) -> Dict[str, Any]:
        """Parse structured markdown response from LLM."""
        import re
        
        result = {
            "action": "continue",
            "selected_questions": [],
            "engagement_headline": "Let's get to know you better!",
            "engagement_message": "Help us understand your needs better.",
            "metadata": {}
        }
        
        try:
            # Extract decision section
            decision_match = re.search(r'## DECISION\s*\nAction:\s*(\w+)', content, re.IGNORECASE)
            if decision_match:
                result["action"] = decision_match.group(1).lower()
            
            # Extract selected questions
            questions_section = re.search(r'## SELECTED QUESTIONS\s*\n(.*?)(?=##|$)', content, re.DOTALL | re.IGNORECASE)
            if questions_section:
                question_blocks = re.findall(r'### Question \d+:\s*(\d+)\s*\n- Original:\s*(.*?)\n- Phrased:\s*(.*?)\n- Required:\s*(.*?)(?=\n|$)', questions_section.group(1), re.DOTALL)
                
                for block in question_blocks:
                    question_num, original, phrased, required = block
                    question_num = int(question_num)
                    
                    # Find the original question from available questions
                    if 1 <= question_num <= len(available_questions):
                        original_q = available_questions[question_num - 1]
                        result["selected_questions"].append({
                            **original_q,
                            "phrased_text": phrased.strip(),
                            "final_text": phrased.strip()
                        })
            
            # Extract engagement headline
            headline_match = re.search(r'### Headline\s*\n(.*?)(?=\n###|\n##|$)', content, re.DOTALL | re.IGNORECASE)
            if headline_match:
                result["engagement_headline"] = headline_match.group(1).strip()
            
            # Extract engagement message
            message_match = re.search(r'### Message\s*\n(.*?)(?=\n##|$)', content, re.DOTALL | re.IGNORECASE)
            if message_match:
                result["engagement_message"] = message_match.group(1).strip()
            
            # Extract metadata
            metadata_match = re.search(r'## METADATA\s*\n(.*?)(?=##|$)', content, re.DOTALL | re.IGNORECASE)
            if metadata_match:
                metadata_text = metadata_match.group(1)
                
                risk_match = re.search(r'- Risk Level:\s*(\w+)', metadata_text, re.IGNORECASE)
                if risk_match:
                    result["metadata"]["risk_level"] = risk_match.group(1).lower()
                
                approach_match = re.search(r'- Approach:\s*(\w+)', metadata_text, re.IGNORECASE)
                if approach_match:
                    result["metadata"]["engagement_approach"] = approach_match.group(1).lower()
            
            # If no questions were extracted, fall back to first 2 available
            if not result["selected_questions"] and available_questions:
                result["selected_questions"] = available_questions[:min(2, len(available_questions))]
                for q in result["selected_questions"]:
                    q["phrased_text"] = q.get("question_text", "")
                    q["final_text"] = q.get("question_text", "")
            
            logger.debug(f"Parsed {len(result['selected_questions'])} questions from markdown")
            return result
            
        except Exception as e:
            logger.error(f"Failed to parse markdown response: {e}")
            # Return fallback with first 2 questions
            return {
                "action": "continue",
                "selected_questions": available_questions[:min(2, len(available_questions))],
                "engagement_headline": "Let's get to know you better!",
                "engagement_message": "Help us understand your needs better.",
                "metadata": {"fallback": True}
            }
    
    def _create_fallback_decision(self, available_questions: List[Dict], analysis: Dict) -> Dict[str, Any]:
        """Create fallback decision when LLM fails."""
        # Simple rule-based selection
        count = 2 if analysis["risk_level"] != "high" else 1
        selected = available_questions[:count]
        
        for q in selected:
            q["phrased_text"] = q.get("question_text")
            q["final_text"] = q.get("question_text")
        
        engagement_headline = "Let's learn more about you!"
        engagement_message = "Help us understand your needs so we can provide you with the best possible service."
        
        if analysis["risk_level"] == "high":
            engagement_headline = "Just a quick question!"
            engagement_message = "We're almost ready to help you get exactly what you need."
        
        return {
            "action": "continue",
            "selected_questions": selected,
            "engagement_headline": engagement_headline,
            "engagement_message": engagement_message,
            "progress_indicator": f"{analysis['progress_percentage']:.0f}% complete",
            "completion_motivation": "Thank you for your responses! This helps us serve you better.",
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
        
        # Format questions for frontend API client (using backend format that frontend transforms)
        # NOTE: Never expose scoring_rubric to frontend - that's sensitive business logic
        frontend_questions = []
        for q in decision["selected_questions"]:
            frontend_questions.append({
                "question": q.get("question_text", ""),
                "phrased_question": q.get("final_text", q.get("question_text", "")),
                "data_type": q.get("question_type", "text"),
                "is_required": q.get("is_required", False),
                "options": q.get("options"),
                "description": q.get("description"),
                "placeholder": q.get("placeholder", "")
                # scoring_rubric intentionally excluded - sensitive data
            })
        
        # Get session_id from core state
        core = state.get('core', {})
        session_id = core.get('session_id')
        
        # Load form details for proper title/description
        form_id = core.get('form_id')
        form_details = self._load_form_details(form_id)
        
        # Prepare the frontend response data
        frontend_data = {
            "session_id": session_id,
            "step": 1,  # Will be updated by the system
            "questions": frontend_questions,
            "question_metadata": frontend_questions,
            "headline": decision.get("engagement_headline", "Let's get to know you better!"),
            "motivation": decision.get("engagement_message", "Help us provide you with the best possible service."),
            "progress": {
                "current_step": 1,
                "estimated_remaining": 3
            }
        }
        
        return {
            # This is the key the API is looking for
            "frontend_response": {
                **frontend_data,
                "form_details": form_details  # Add form details to frontend response
            },
            
            # Core response
            "step_type": "questions" if decision["action"] == "continue" else "completion",
            "questions": frontend_questions,
            "engagement": {
                "message": decision.get("engagement_message", ""),
                "progress": decision.get("progress_indicator", ""),
                "motivation": decision.get("completion_motivation", "")
            },
            
            # State updates
            "question_strategy": {
                **question_strategy,
                "asked_questions": asked_questions,
                "current_questions": frontend_questions,
                "selection_confidence": decision.get("confidence", 0.7)
            },
            
            # Add form details to core state
            "form_details": form_details,
            
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
    logger.info("🔥 consolidated_survey_admin_node called by LangGraph!")
    logger.debug(f"🔥 State keys: {list(state.keys()) if isinstance(state, dict) else 'Not a dict'}")
    
    supervisor = ConsolidatedSurveyAdminSupervisor()
    result = supervisor.process_survey_step(state)
    
    logger.info(f"🔥 Node result: {type(result)}, keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
    if isinstance(result, dict) and 'supervisor_metadata' in result:
        metadata = result['supervisor_metadata']
        logger.info(f"🔥 LLM decision used: {metadata.get('llm_decision', 'unknown')}")
    
    return result