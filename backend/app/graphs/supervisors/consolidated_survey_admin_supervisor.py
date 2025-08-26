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
            model_name="gpt-4.1-nano",
            temperature=0.3,
            max_tokens=2000,  # Reduced for faster responses
            timeout_seconds=15,  # Reduced timeout for faster responses
            **kwargs
        )
        self.llm = get_chat_model(model_name="gpt-4.1-nano")

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
        """System prompt defining the Marketing & Engagement Specialist role."""
        return """# MARKETING & ENGAGEMENT SPECIALIST
You are a Marketing Copywriting Expert specializing in survey engagement and customer attraction for service businesses.

## YOUR EXPERTISE
You excel at classic marketing copywriting techniques to project business benefits in the best light and attract ideal customers through engaging survey experiences.

## CORE SPECIALIZATIONS

### 1. STRATEGIC QUESTION SELECTION - Optimize visitor engagement
- Select 1-3 questions that build momentum and trust
- Vary count based on visitor engagement signals
- Choose questions that showcase business value
- Progress visitors through an engaging discovery journey

### 2. MARKETING COPYWRITING - Transform questions into compelling conversation
- Rephrase questions using proven copywriting techniques
- Make every question feel valuable and worth answering
- Use conversational, benefit-focused language
- Maintain original question intent while maximizing engagement

### 3. CUSTOMER ATTRACTION - Project business benefits strategically
- Highlight unique business strengths and qualifications
- Emphasize value propositions and customer success stories
- Create desire for the business's services
- Position the business as the ideal solution

### 4. ENGAGEMENT OPTIMIZATION - Create irresistible survey experiences
- Craft compelling headlines that encourage participation
- Write benefit-driven messages that build excitement
- Use psychological triggers to maintain visitor interest
- Balance information gathering with value delivery

## MARKETING PRINCIPLES
- **Benefit-Focused**: Always emphasize what's in it for the customer
- **Trust-Building**: Use credentials, experience, and social proof
- **Conversational**: Make questions feel like helpful consultation, not interrogation  
- **Value-Driven**: Every interaction should feel valuable to the visitor
- **Customer-Centric**: Focus on solving visitor problems, not business needs

## OUTPUT FORMAT REQUIREMENTS
SELECTED: [comma-separated question numbers]
QUESTION_[number]: [rephrased with marketing copywriting]
QUESTION_[number]: [rephrased with marketing copywriting]
HEADLINE: [compelling, benefit-focused headline]
MESSAGE: [marketing message highlighting business benefits under 50 words]

You create survey experiences that visitors genuinely enjoy while strategically attracting the ideal customers the business seeks."""

    def process_survey_step(self, state: SurveyState) -> Dict[str, Any]:
        """Main entry point - processes entire survey administration step."""
        try:
            logger.info(f"Starting survey administration processing for state: {type(state)}")
            logger.debug(f"State keys: {list(state.keys()) if isinstance(state, dict) else 'Not a dict'}")

            # Check if we have pending responses - if so, signal to route to lead intelligence
            # This should only happen on the first entry, not after lead intelligence processes them
            pending_responses = state.get("pending_responses")
            if pending_responses and len(pending_responses) > 0:
                logger.info("Found pending responses - survey admin will route to lead intelligence")
                return {
                    "route_to_lead_intelligence": True,
                    "pending_responses": state.get("pending_responses"),
                    "supervisor_metadata": {
                        "supervisor_name": self.name,
                        "action": "route_to_lead_intelligence",
                        "decision_timestamp": datetime.now().isoformat()
                    }
                }

            # Load available questions
            available_questions = self._load_available_questions(state)
            if not available_questions:
                logger.warning("No available questions found, routing to lead intelligence for completion check")
                return {
                    "route_to_lead_intelligence": True,
                    "pending_responses": [],  # Empty responses to trigger completion check
                    "supervisor_metadata": {
                        "supervisor_name": self.name,
                        "action": "route_to_completion_check",
                        "decision_timestamp": datetime.now().isoformat()
                    }
                }

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
            session_id = state.get('core', {}).get('session_id')

            logger.debug(f"Loading questions for form_id: {form_id}")

            # Load all questions directly from database (same as test implementation)
            from ...database import db
            all_questions = db.get_form_questions(form_id)
            logger.debug(f"Loaded {len(all_questions) if all_questions else 0} total questions from database")

            if all_questions:
                logger.debug(f"Sample question: {all_questions[0] if len(all_questions) > 0 else 'None'}")

            # CRITICAL FIX: Get already asked questions from TWO sources (like langgraph_test)
            # 1. Database tracking (persistent)
            asked_ids_db = db.get_asked_questions(session_id) if session_id else []

            # 2. State-based tracking (current session)
            asked_ids_state = state.get("question_strategy", {}).get("asked_questions", [])

            # Combine both sources (this is what makes langgraph_test work!)
            asked_ids = list(set(asked_ids_db + asked_ids_state))

            logger.info(f"🔥 DUAL TRACKING: DB asked questions: {asked_ids_db}")
            logger.info(f"🔥 DUAL TRACKING: State asked questions: {asked_ids_state}")
            logger.info(f"🔥 DUAL TRACKING: Combined asked questions: {asked_ids}")

            # Filter to available questions using question_id (not database id)
            available_questions = []
            for q in all_questions:
                question_id = q.get('question_id')
                if question_id is not None:
                    if question_id not in asked_ids:
                        available_questions.append(q)
                    else:
                        logger.debug(f"🔥 FILTERING: Question ID {question_id} already asked, skipping")

            logger.info(f"🔥 DATABASE TRACKING: Loaded {len(available_questions)} available questions for form {form_id} (filtered from {len(all_questions)} total, {len(asked_ids)} already asked)")
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

            business_name = client_info.get('name', 'our business')
            industry = client_info.get('industry', 'service business')

            # Create numbered question list for LLM using original question_id as the number
            numbered_questions = []
            for q in available_questions[:15]:  # Limit to 15 for context
                question_id = q.get("question_id")
                if question_id is not None:
                    numbered_questions.append({
                        "number": question_id,  # Use original question_id as number
                        "question_text": q.get("question_text", ""),
                        "input_type": q.get("input_type", ""),
                        "is_required": q.get("is_required", False),
                        "category": q.get("category", "")
                    })

            # Note: Approach logic now handled by system prompt based on user context

            # Extract user information from responses for personalization
            user_name = None
            user_info = {}
            for resp in responses:
                answer = resp.get('answer', '').strip()
                question_text = resp.get('question_text', '').lower()

                # Look for name in responses
                if 'name' in question_text and answer and len(answer.split()) <= 3:
                    user_name = answer.split()[0]  # First name only

                # Collect other user info for context
                if answer and answer != "ASKED_PLACEHOLDER":
                    user_info[question_text] = answer

            # Get detailed client info for engagement (using correct database column names)
            business_background = client_info.get('background', '')
            business_goals = client_info.get('goals', '')
            target_audience = client_info.get('target_audience', '')

            # USER PROMPT: Simple data + task (no duplicate instructions)
            user_context = f"User: {user_name or 'unknown'}"
            if analysis['questions_asked'] > 0:
                user_context += f" | {analysis['questions_asked']} answered"
            if analysis['risk_level'] != 'low':
                user_context += f" | {analysis['risk_level']} engagement"
            
            # Build comprehensive business context using all available database data
            business_context = f"Business: {business_name} ({industry})"
            if business_background:
                business_context += f"\nBackground: {business_background[:100]}"
            if business_goals:
                business_context += f"\nGoals: {business_goals[:100]}"
            if target_audience:
                business_context += f"\nTarget: {target_audience[:100]}"
            
            user_prompt = f"""# DATA FOR THIS REQUEST
{business_context}
{user_context}

# AVAILABLE QUESTIONS
{chr(10).join([f"{q['number']}. {q['question_text']}" for q in numbered_questions])}

# TASK
Select and rephrase questions for this survey step. Follow your system instructions for format and rules."""

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

            # Parse simple response from LLM
            logger.info("Parsing LLM simple response...")
            decision_data = self._parse_simple_response(llm_content, available_questions)
            logger.info(f"Parsed {len(decision_data.get('selected_questions', []))} questions from LLM")

            # If parsing failed or no questions selected, use fallback
            if not decision_data.get('selected_questions'):
                logger.warning("Simple parser returned no questions, using fallback")
                return self._create_fallback_decision(available_questions, analysis)

            # Debug parsed questions
            for i, q in enumerate(decision_data.get('selected_questions', [])):
                original_text = q.get('question', q.get('question_text', 'NO_ORIGINAL'))
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

    def _parse_simple_response(self, content: str, available_questions: List[Dict]) -> Dict[str, Any]:
        """Parse structured response from LLM with robust error handling."""
        result = {
            "action": "continue",
            "selected_questions": [],
            "engagement_headline": "Let's get to know you better!",
            "engagement_message": "Help us understand your needs better.",
            "metadata": {}
        }

        try:
            import re
            
            # More flexible parsing using regex patterns
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            selected_numbers = []
            rephrased_questions = {}

            for line in lines:
                # Parse SELECTED with flexible matching
                selected_match = re.match(r'^SELECTED\s*:\s*(.+)$', line, re.IGNORECASE)
                if selected_match:
                    numbers_text = selected_match.group(1).strip()
                    try:
                        # Handle various separators: comma, semicolon, space
                        number_strings = re.split(r'[,;\s]+', numbers_text)
                        selected_numbers = [int(n.strip()) for n in number_strings if n.strip().isdigit()]
                        logger.info(f"🔥 PARSED SELECTION: {selected_numbers}")
                    except ValueError as e:
                        logger.error(f"Failed to parse selected numbers: {numbers_text}, error: {e}")
                        # Try to extract any numbers found
                        numbers = re.findall(r'\d+', numbers_text)
                        selected_numbers = [int(n) for n in numbers[:4]]  # Max 4 questions
                        logger.info(f"🔥 FALLBACK SELECTION: {selected_numbers}")

                # Parse QUESTION_ with flexible matching
                question_match = re.match(r'^QUESTION[_\s]*(\d+)\s*:\s*(.+)$', line, re.IGNORECASE)
                if question_match:
                    try:
                        question_num = int(question_match.group(1))
                        question_text = question_match.group(2).strip()
                        rephrased_questions[question_num] = question_text
                        logger.info(f"🔥 PARSED REPHRASE: Q{question_num} = '{question_text[:50]}...'")
                    except (ValueError, IndexError) as e:
                        logger.error(f"Failed to parse question line: {line}, error: {e}")

                # Parse HEADLINE with flexible matching
                headline_match = re.match(r'^HEADLINE\s*:\s*(.+)$', line, re.IGNORECASE)
                if headline_match:
                    result["engagement_headline"] = headline_match.group(1).strip()

                # Parse MESSAGE with flexible matching  
                message_match = re.match(r'^MESSAGE\s*:\s*(.+)$', line, re.IGNORECASE)
                if message_match:
                    result["engagement_message"] = message_match.group(1).strip()

            # Build selected questions list using question_id matching
            for num in selected_numbers:
                # Find question by question_id in available_questions
                found_question = None
                for q in available_questions:
                    if q.get("question_id") == num:
                        found_question = q
                        break

                if found_question:
                    rephrased_text = rephrased_questions.get(num, found_question.get("question_text", ""))

                    result["selected_questions"].append({
                        **found_question,
                        "phrased_text": rephrased_text,
                        "final_text": rephrased_text
                    })
                    logger.info(f"🔥 ADDED QUESTION: {num} -> '{rephrased_text[:50]}...'")
                else:
                    logger.warning(f"Question ID {num} not found in available questions")

            logger.info(f"🔥 SIMPLE PARSER SUCCESS: {len(result['selected_questions'])} questions selected")
            return result

        except Exception as e:
            logger.error(f"Failed to parse simple response: {e}")
            logger.error(f"Content was: {content[:500]}...")
            # Return fallback
            return {
                "action": "continue",
                "selected_questions": [],
                "engagement_headline": "Let's get to know you better!",
                "engagement_message": "Help us understand your needs better.",
                "metadata": {"fallback": True, "parse_error": str(e)}
            }

    def _clean_engagement_message(self, message: str) -> str:
        """Clean engagement message by removing any accidental metadata."""
        import re

        # Remove lines that look like metadata (- Key: value pattern)
        lines = message.split('\n')
        cleaned_lines = []

        for line in lines:
            line = line.strip()
            # Skip lines that match metadata patterns
            if re.match(r'^\s*-\s*(Questions Selected|Risk Level|Approach|Total.*Steps):', line, re.IGNORECASE):
                continue
            # Skip empty lines at the end
            if line:
                cleaned_lines.append(line)

        # Join back and clean up
        cleaned_message = '\n'.join(cleaned_lines).strip()

        # Remove any trailing metadata that might be at the end
        # Look for patterns like "- Questions: X - Risk: Y - Approach: Z"
        cleaned_message = re.sub(r'\s*-\s*(Questions Selected|Risk Level|Approach):\s*\w+(\s*-\s*(Questions Selected|Risk Level|Approach):\s*\w+)*\s*$', '', cleaned_message, flags=re.IGNORECASE)

        # Clean up any remaining metadata patterns
        cleaned_message = re.sub(r'\s*Total\s+\w+\s+Steps:\s*\d+\s*', '', cleaned_message, flags=re.IGNORECASE)
        cleaned_message = re.sub(r'\s*Risk\s+Level:\s*\w+\s*', '', cleaned_message, flags=re.IGNORECASE)
        cleaned_message = re.sub(r'\s*Approach:\s*\w+\s*', '', cleaned_message, flags=re.IGNORECASE)

        return cleaned_message.strip()

    def _create_fallback_decision(self, available_questions: List[Dict], analysis: Dict) -> Dict[str, Any]:
        """Create fallback decision when LLM fails with randomized selection."""
        import random

        # Randomized rule-based selection to vary question count
        if analysis["risk_level"] == "high":
            count = 1  # Always 1 for high risk
        else:
            # Vary between 1-4 questions based on context
            questions_asked = analysis.get("questions_asked", 0)
            if questions_asked == 0:
                count = random.choice([1, 2])  # First step: 1-2 questions
            elif questions_asked < 4:
                count = random.choice([2, 3])  # Early steps: 2-3 questions
            else:
                count = random.choice([1, 2, 3, 4])  # Later steps: vary widely

        # Don't select more questions than available
        count = min(count, len(available_questions))

        # Random selection instead of always taking first N
        if len(available_questions) > count:
            selected = random.sample(available_questions, count)
        else:
            selected = available_questions[:count]

        logger.info(f"🔥 FALLBACK: Selected {count} questions randomly (risk: {analysis['risk_level']}, asked: {analysis.get('questions_asked', 0)})")

        for q in selected:
            q["phrased_text"] = q.get("question", q.get("question_text"))
            q["final_text"] = q.get("question", q.get("question_text"))

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
                "analysis": analysis,
                "fallback_count": count
            }
        }

    def _prepare_frontend_response(self, decision: Dict, state: SurveyState) -> Dict[str, Any]:
        """Prepare the final response for frontend consumption.

        CRITICAL: This method MUST include question IDs in the response to prevent
        questions from repeating. See FIX_DOCUMENTATION.md for details on the
        recurring question repetition bug and its fix.
        """
        # CRITICAL FIX: Update state asked_questions (like langgraph_test does)
        question_strategy = state.get('question_strategy', {})
        current_asked = question_strategy.get('asked_questions', [])

        # Add newly selected questions to asked_questions (prevents repetition!)
        selected_questions = decision.get("selected_questions", [])
        new_question_ids = [q.get('question_id') for q in selected_questions if q.get('question_id') is not None]
        updated_asked = current_asked + new_question_ids

        logger.info(f"🔥 STATE UPDATE: Adding {new_question_ids} to asked_questions")
        logger.info(f"🔥 STATE UPDATE: {current_asked} -> {updated_asked}")

        # Mark newly selected questions as asked in database
        from ...database import db
        session_id = state.get('core', {}).get('session_id')
        new_question_ids = []

        for q in decision["selected_questions"]:
            q_id = q.get("question_id")
            if q_id is not None:
                new_question_ids.append(q_id)
                logger.info(f"🔥 DATABASE TRACKING: Marking question ID {q_id} as asked")
            else:
                logger.error(f"🔥 ERROR: Question missing question_id: {q}")

        # Questions will be tracked when actual responses are saved by lead intelligence agent
        # No need to pre-mark questions as asked - tracking happens via real response records

        # Get current asked questions from database (source of truth) and state
        db_asked_questions = db.get_asked_questions(session_id) if session_id else []
        state_asked_questions = question_strategy.get('asked_questions', [])

        # Combine database and state (state should now only contain integers)
        all_asked_questions = list(set(db_asked_questions + state_asked_questions))
        logger.info(f"🔥 STATE SYNC: DB={db_asked_questions}, State={state_asked_questions}, Final={all_asked_questions}")

        # Format questions for frontend API client (using backend format that frontend transforms)
        # NOTE: Never expose scoring_rubric to frontend - that's sensitive business logic
        # CRITICAL FIX: Include question ID for proper tracking
        frontend_questions = []
        for q in decision["selected_questions"]:
            q_id = q.get("question_id")  # Use question_id instead of id
            if q_id is None:
                logger.error(f"🔥 ERROR: Question missing question_id: {q.get('question_text', 'unknown')}")
            frontend_questions.append({
                "question_id": q_id,  # CRITICAL: Include question_id for tracking
                "question": q.get("question", q.get("question_text", "")),
                "phrased_question": q.get("final_text", q.get("phrased_text", q.get("question", q.get("question_text", "")))),
                "input_type": q.get("input_type", q.get("question_type", "text")),  # Frontend input type (text, textarea, radio, select, etc.)
                "data_type": q.get("data_type", "text"),  # Backend data type (text, integer, float, boolean, etc.)
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

        result = {
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
                "all_questions": question_strategy.get("all_questions", []),
                "asked_questions": updated_asked,  # CRITICAL: Include newly selected questions
                "current_questions": frontend_questions,
                "selection_history": question_strategy.get("selection_history", []),
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

        # Debug: Log what we're returning
        logger.info(f"🔥 SUPERVISOR RETURN: asked_questions = {all_asked_questions}")
        return result

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
