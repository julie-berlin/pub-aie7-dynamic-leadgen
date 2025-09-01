"""Consolidated Survey Administration Supervisor."""

from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime
import random

from graph.supervisors.base_supervisor import SupervisorAgent, SupervisorDecision
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from models import get_chat_model

logger = logging.getLogger(__name__)

class ConsolidatedSurveyAdminSupervisor(SupervisorAgent):
    """Consolidated supervisor handling all survey administration tasks."""

    def __init__(self, **kwargs):
        super().__init__(
            name="ConsolidatedSurveyAdminSupervisor",
            model_name="gpt-3.5-turbo",
            temperature=0.3,
            max_tokens=2000,
            timeout_seconds=15,
            **kwargs
        )
        self.llm = get_chat_model(model_name="o4-mini", temperature=0.3)

    def get_system_prompt(self) -> str:
        """System prompt for survey administration."""
        return """You are a Survey Administration AI with exactly 3 responsibilities:

1. QUESTION SELECTION: Choose 1-4 questions from the available pool
   - Consider conversation context and user responses
   - Vary count: 1 for sensitive topics, 2-3 standard, 4 for quick gathering
   - Never repeat already-asked questions
   - Early steps: 1-2 questions to build trust
   - Later steps: 3-4 questions when momentum established

2. QUESTION REPHRASING: Make questions engaging and personal
   - Use user's name if known
   - Reference previous responses when relevant
   - Make conversational and natural
   - Each question asks for exactly ONE piece of information

3. ENGAGEMENT MESSAGING: Business context + completion encouragement
   - Include specific business services/benefits
   - Show company personality
   - Encourage completion (never suggest ending)
   - Keep message under 50 words

OUTPUT FORMAT (exactly this structure):
SELECTED: [comma-separated question numbers]
QUESTION_[number]: [rephrased question text]
HEADLINE: [engaging headline]
MESSAGE: [business context + encouragement, under 50 words]

Example:
SELECTED: 2,7,9
QUESTION_2: Hi Sarah, what's your budget range for this project?
QUESTION_7: How soon are you looking to get started?
QUESTION_9: What's your biggest concern about choosing a service provider?
HEADLINE: Let's find the perfect solution for you!
MESSAGE: At Pawsome Dog Walking, we've helped over 500 pet owners. Tell us more so we can create a custom plan that fits your needs perfectly."""

    def process_survey_step(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Main entry point - processes entire survey administration step."""
        try:
            logger.info(f"🎯 Survey Admin: Processing step {state.get('core', {}).get('step', 0)}")

            # Check if we have pending responses to route to lead intelligence
            pending_responses = state.get("pending_responses")
            if pending_responses and len(pending_responses) > 0:
                logger.info("Found pending responses - routing to lead intelligence")
                return {
                    "route_to_lead_intelligence": True,
                    "pending_responses": pending_responses
                }

            # Load available questions
            available_questions = self._load_available_questions(state)
            if not available_questions:
                logger.warning("No available questions found, completing survey")
                return self._create_completion_response("No more questions available")

            # Make comprehensive decision
            logger.info(f"📊 Available questions: {len(available_questions)}")
            decision = self._make_comprehensive_decision(state, available_questions)

            # Prepare frontend response
            frontend_data = self._prepare_frontend_response(decision, state)
            logger.info(f"✅ Survey admin prepared {len(decision.get('selected_questions', []))} questions")

            return frontend_data

        except Exception as e:
            logger.error(f"Survey admin processing error: {e}")
            return self._create_error_response(str(e))

    def _load_available_questions(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Load questions that haven't been asked yet."""
        from database.sqlite_db import db

        form_id = state.get("core", {}).get("form_id")
        session_id = state.get("core", {}).get("session_id")

        # Get all questions for the form
        all_questions = db.get_form_questions(form_id)

        # Get already asked questions
        asked_questions = db.get_asked_questions(session_id) if session_id else []
        asked_questions.extend(state.get("question_strategy", {}).get("asked_questions", []))

        # Filter out asked questions
        available = [q for q in all_questions if q["question_id"] not in asked_questions]

        return available

    def _make_comprehensive_decision(self, state: Dict[str, Any], available_questions: List[Dict]) -> Dict[str, Any]:
        """Make comprehensive decision using LLM."""
        try:
            # Prepare context for LLM
            step = state.get("core", {}).get("step", 0)
            responses = state.get("lead_intelligence", {}).get("responses", [])

            # Build context
            context = f"""
            Current step: {step}
            Questions answered so far: {len(responses)}
            Available questions: {len(available_questions)}

            Available questions to choose from:
            """

            for q in available_questions[:10]:  # Limit to first 10 for context
                context += f"\n{q['question_id']}: {q['question_text']}"

            if responses:
                context += "\n\nPrevious responses:"
                for r in responses[-3:]:  # Last 3 responses for context
                    context += f"\n- {r.get('answer', '')}"

            # Call LLM
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": context}
            ]

            response = self.llm.invoke(messages)
            llm_output = response.content

            # Parse LLM output
            selected_ids = []
            phrased_questions = {}
            headline = "Let's continue!"
            message = "Just a few more questions to help us serve you better."

            for line in llm_output.split('\n'):
                if line.startswith("SELECTED:"):
                    ids_str = line.replace("SELECTED:", "").strip()
                    selected_ids = [int(id.strip()) for id in ids_str.split(',') if id.strip().isdigit()]
                elif line.startswith("QUESTION_"):
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        q_id = int(parts[0].replace("QUESTION_", "").strip())
                        phrased_questions[q_id] = parts[1].strip()
                elif line.startswith("HEADLINE:"):
                    headline = line.replace("HEADLINE:", "").strip()
                elif line.startswith("MESSAGE:"):
                    message = line.replace("MESSAGE:", "").strip()

            # Fallback if LLM didn't select questions
            if not selected_ids:
                num_to_select = min(3, len(available_questions))
                selected_ids = [q['question_id'] for q in available_questions[:num_to_select]]

            # Get selected question objects
            selected_questions = [q for q in available_questions if q['question_id'] in selected_ids]

            # Add phrased versions
            for q in selected_questions:
                if q['question_id'] in phrased_questions:
                    q['phrased_question'] = phrased_questions[q['question_id']]
                else:
                    q['phrased_question'] = q['question_text']

            return {
                "action": "continue",
                "selected_questions": selected_questions,
                "engagement": {
                    "headline": headline,
                    "message": message
                },
                "metadata": {
                    "selection_strategy": "llm_based",
                    "questions_available": len(available_questions),
                    "questions_selected": len(selected_questions)
                }
            }

        except Exception as e:
            logger.error(f"LLM decision error: {e}, using fallback")
            # Fallback selection
            num_to_select = min(2, len(available_questions))
            selected = available_questions[:num_to_select]

            return {
                "action": "continue",
                "selected_questions": selected,
                "engagement": {
                    "headline": "Let's continue!",
                    "message": "Just a few more questions to help us understand your needs."
                },
                "metadata": {
                    "selection_strategy": "fallback",
                    "error": str(e)
                }
            }

    def _prepare_frontend_response(self, decision: Dict, state: Dict) -> Dict[str, Any]:
        """Prepare response for frontend/next node."""
        selected_questions = decision.get("selected_questions", [])

        # Update asked questions
        current_asked = state.get("question_strategy", {}).get("asked_questions", [])
        new_asked = current_asked + [q['question_id'] for q in selected_questions]

        return {
            "step_type": "questions",
            "questions": selected_questions,
            "engagement": decision.get("engagement", {}),
            "question_strategy": {
                "asked_questions": new_asked,
                "all_questions": state.get("question_strategy", {}).get("all_questions", []),
                "current_questions": selected_questions,
                "phrased_questions": [q.get('phrased_question', q['question_text']) for q in selected_questions]
            },
            "frontend_response": {
                "step_type": "questions",
                "questions": [
                    {
                        "id": q['question_id'],
                        "text": q.get('phrased_question', q['question_text']),
                        "type": q.get('input_type', 'text'),
                        "required": q.get('is_required', False)
                    }
                    for q in selected_questions
                ],
                "headline": decision.get("engagement", {}).get("headline"),
                "message": decision.get("engagement", {}).get("message"),
                "progress": {
                    "current_step": state.get("core", {}).get("step", 0) + 1,
                    "questions_answered": len(state.get("lead_intelligence", {}).get("responses", []))
                }
            }
        }

    def _create_completion_response(self, reason: str) -> Dict[str, Any]:
        """Create completion response when no more questions."""
        return {
            "step_type": "completion",
            "completed": True,
            "reason": reason,
            "frontend_response": {
                "step_type": "completion",
                "message": "Thank you for completing the survey!"
            }
        }

    def _create_error_response(self, error: str) -> Dict[str, Any]:
        """Create error response."""
        return {
            "step_type": "error",
            "error": error,
            "frontend_response": {
                "step_type": "error",
                "message": "An error occurred. Please try again."
            }
        }

def consolidated_survey_admin_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Node function for survey administration."""
    supervisor = ConsolidatedSurveyAdminSupervisor()
    return supervisor.process_survey_step(state)
