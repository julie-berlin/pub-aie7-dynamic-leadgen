"""Lead Intelligence Toolbelt - Utilities for lead processing and analysis."""

from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class LeadIntelligenceToolbelt:
    """Comprehensive toolbelt for lead intelligence operations."""
    
    def __init__(self):
        self.tavily_tool = None
        self.maps_tool = None
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize external tools if available."""
        try:
            from langchain_tavily import TavilySearchResults
            self.tavily_tool = TavilySearchResults(max_results=3)
            logger.info("Tavily tool initialized")
        except ImportError:
            logger.warning("Tavily tool not available")
        except Exception as e:
            logger.error(f"Failed to initialize Tavily: {e}")
    
    # ========== DATABASE OPERATIONS ==========
    
    def save_responses_to_database(
        self, 
        session_id: str, 
        responses: List[Dict],
        form_id: str
    ) -> Dict[str, Any]:
        """Save user responses to database."""
        try:
            from ...database import db
            
            saved_count = 0
            errors = []
            
            for response in responses:
                try:
                    # Save individual response
                    response_data = {
                        "session_id": session_id,
                        "form_id": form_id,
                        "question_id": response.get("question_id"),
                        "answer": response.get("answer"),
                        "answered_at": datetime.now().isoformat()
                    }
                    
                    db.save_response(response_data)
                    saved_count += 1
                    
                except Exception as e:
                    errors.append(f"Failed to save response {response.get('question_id')}: {e}")
                    logger.error(f"Response save error: {e}")
            
            # Update session with latest activity
            db.update_lead_session(session_id, {
                "last_activity_time": datetime.now().isoformat(),
                "responses_count": saved_count
            })
            
            return {
                "success": saved_count > 0,
                "saved_count": saved_count,
                "total_attempted": len(responses),
                "errors": errors
            }
            
        except Exception as e:
            logger.error(f"Database save error: {e}")
            return {
                "success": False,
                "error": str(e),
                "saved_count": 0
            }
    
    # ========== SCORING CALCULATIONS ==========
    
    def calculate_lead_score(
        self, 
        responses: List[Dict], 
        scoring_rubrics: Dict,
        business_rules: Dict = None
    ) -> Dict[str, Any]:
        """Calculate mathematical lead score based on responses."""
        try:
            total_score = 0
            max_possible_score = 0
            scoring_details = []
            
            for response in responses:
                question_id = response.get("question_id")
                answer = response.get("answer", "")
                
                # Get scoring rubric for this question
                rubric = scoring_rubrics.get(str(question_id), {})
                if not rubric:
                    continue
                
                # Calculate score for this response
                question_score = self._score_single_response(answer, rubric)
                max_score = rubric.get("max_score", 10)
                
                total_score += question_score
                max_possible_score += max_score
                
                scoring_details.append({
                    "question_id": question_id,
                    "score": question_score,
                    "max_score": max_score,
                    "answer_snippet": answer[:50]
                })
            
            # Normalize to 0-100 scale
            if max_possible_score > 0:
                normalized_score = int((total_score / max_possible_score) * 100)
            else:
                normalized_score = 0
            
            # Apply business rule adjustments
            if business_rules:
                normalized_score = self._apply_business_rule_adjustments(
                    normalized_score, 
                    responses, 
                    business_rules
                )
            
            return {
                "calculated_score": normalized_score,
                "raw_score": total_score,
                "max_possible": max_possible_score,
                "scoring_details": scoring_details,
                "responses_scored": len(scoring_details)
            }
            
        except Exception as e:
            logger.error(f"Score calculation error: {e}")
            return {
                "calculated_score": 0,
                "error": str(e)
            }
    
    def _score_single_response(self, answer: str, rubric: Dict) -> float:
        """Score a single response based on its rubric."""
        try:
            # Check for keyword-based scoring
            if "keywords" in rubric:
                score = 0
                answer_lower = answer.lower()
                for keyword, points in rubric["keywords"].items():
                    if keyword.lower() in answer_lower:
                        score += points
                return min(score, rubric.get("max_score", 10))
            
            # Check for length-based scoring
            if "min_length" in rubric:
                if len(answer.strip()) >= rubric["min_length"]:
                    return rubric.get("base_score", 5)
                else:
                    return rubric.get("penalty_score", 2)
            
            # Check for exact match scoring
            if "exact_matches" in rubric:
                answer_lower = answer.lower().strip()
                for match, points in rubric["exact_matches"].items():
                    if match.lower() == answer_lower:
                        return points
            
            # Default scoring
            if answer.strip():
                return rubric.get("default_score", 3)
            else:
                return 0
                
        except Exception as e:
            logger.error(f"Single response scoring error: {e}")
            return 0
    
    def _apply_business_rule_adjustments(
        self, 
        score: int, 
        responses: List[Dict], 
        rules: Dict
    ) -> int:
        """Apply business-specific rule adjustments to score."""
        adjusted_score = score
        
        # Check for required questions
        if "required_questions" in rules:
            required_ids = set(rules["required_questions"])
            answered_ids = {r.get("question_id") for r in responses}
            
            if not required_ids.issubset(answered_ids):
                # Penalty for missing required questions
                adjusted_score = max(0, adjusted_score - 20)
        
        # Check for disqualifying answers
        if "disqualifiers" in rules:
            for response in responses:
                answer_lower = response.get("answer", "").lower()
                for disqualifier in rules["disqualifiers"]:
                    if disqualifier.lower() in answer_lower:
                        adjusted_score = min(adjusted_score, 25)  # Cap at low score
        
        # Check for bonus conditions
        if "bonus_conditions" in rules:
            for condition in rules["bonus_conditions"]:
                if self._check_bonus_condition(responses, condition):
                    adjusted_score = min(100, adjusted_score + condition.get("bonus", 10))
        
        return max(0, min(100, adjusted_score))
    
    def _check_bonus_condition(self, responses: List[Dict], condition: Dict) -> bool:
        """Check if bonus condition is met."""
        # Simple implementation - can be extended
        return False
    
    # ========== EXTERNAL TOOL INTEGRATION ==========
    
    def execute_tavily_search(self, query: str) -> Dict[str, Any]:
        """Execute Tavily web search for lead validation."""
        try:
            if not self.tavily_tool:
                return {
                    "success": False,
                    "error": "Tavily tool not available"
                }
            
            logger.info(f"Executing Tavily search: {query}")
            results = self.tavily_tool.run(query)
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "executed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Tavily search error: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }
    
    def execute_maps_validation(
        self, 
        origin: str, 
        destination: str,
        service_area_radius: float = 25.0
    ) -> Dict[str, Any]:
        """Execute Google Maps distance validation."""
        try:
            # For now, simulate Maps API call (implement actual API later)
            logger.info(f"Maps validation: {origin} to {destination}")
            
            # Simulated response
            import random
            distance = random.uniform(5, 30)
            duration = int(distance * 1.8)
            
            return {
                "success": True,
                "origin": origin,
                "destination": destination,
                "distance": f"{distance:.1f} miles",
                "duration": f"{duration} minutes",
                "in_service_area": distance <= service_area_radius,
                "executed_at": datetime.now().isoformat(),
                "simulated": True  # Remove when real API implemented
            }
            
        except Exception as e:
            logger.error(f"Maps validation error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def analyze_tool_requirements(
        self, 
        responses: List[Dict], 
        client_info: Dict,
        business_rules: Dict = None
    ) -> Dict[str, Any]:
        """Analyze if external tools would be valuable for this lead."""
        analysis = {
            "tavily_recommended": False,
            "maps_recommended": False,
            "tavily_reasons": [],
            "maps_reasons": [],
            "suggested_queries": {}
        }
        
        business_type = client_info.get('industry', '').lower()
        service_area = client_info.get('service_area', '')
        
        # Analyze for Tavily search needs
        for response in responses:
            answer = response.get('answer', '').lower()
            question_text = response.get('question_text', '').lower()
            
            # Pet/animal related searches
            if any(term in business_type for term in ['pet', 'dog', 'animal']):
                if any(breed_word in answer for breed_word in ['breed', 'dog', 'puppy', 'aggressive']):
                    analysis["tavily_recommended"] = True
                    analysis["tavily_reasons"].append("Breed safety validation")
                    analysis["suggested_queries"]["tavily"] = f"{answer} dog breed safety temperament"
                    break
            
            # Real estate searches
            if 'real estate' in business_type or 'property' in business_type:
                if any(term in answer for term in ['market', 'price', 'value', 'investment']):
                    analysis["tavily_recommended"] = True
                    analysis["tavily_reasons"].append("Market research validation")
                    analysis["suggested_queries"]["tavily"] = f"real estate market {answer}"
                    break
            
            # Location-based validation
            if any(loc_word in question_text for loc_word in ['address', 'location', 'where', 'area']):
                if len(answer.strip()) > 5 and service_area:
                    analysis["maps_recommended"] = True
                    analysis["maps_reasons"].append("Service area distance validation")
                    analysis["suggested_queries"]["maps"] = {
                        "origin": answer,
                        "destination": service_area
                    }
        
        return analysis
    
    # ========== MESSAGE GENERATION UTILITIES ==========
    
    def generate_default_messages(self, lead_status: str, client_name: str) -> Dict[str, str]:
        """Generate default completion messages by status."""
        messages = {
            "qualified": f"Excellent news! Based on your responses, you're an ideal match for {client_name}'s services. We're excited to work with you and will be in touch within 24 hours to discuss next steps and schedule your first consultation.",
            
            "maybe": f"Thank you for your interest in {client_name}! We're carefully reviewing your information to ensure we can provide the best possible service for your needs. Our team will reach out within 2-3 business days with more information.",
            
            "no": f"Thank you for taking the time to learn about {client_name}. While we may not be the perfect fit for your current needs, we genuinely appreciate your interest and wish you the best in finding the right solution.",
            
            "continue": f"Thanks for your responses so far! We have a few more questions to better understand your needs and how {client_name} can help you."
        }
        
        return messages
    
    def determine_next_actions(
        self, 
        lead_status: str, 
        confidence: float,
        score: int
    ) -> List[str]:
        """Determine appropriate next actions based on lead classification."""
        actions = []
        
        if lead_status == "qualified":
            actions = [
                "immediate_contact",
                "schedule_consultation",
                "send_service_details",
                "add_to_priority_queue"
            ]
            if confidence > 0.9 and score > 85:
                actions.append("premium_service_offering")
                actions.append("assign_senior_representative")
        
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
                "add_to_nurture_campaign",
                "newsletter_signup_option",
                "future_contact_consent"
            ]
            if score > 30:
                actions.append("referral_suggestions")
        
        elif lead_status == "continue":
            actions = [
                "prepare_next_questions",
                "maintain_session_state",
                "update_progress_tracking"
            ]
        
        return actions
    
    def update_lead_status_in_database(
        self,
        session_id: str,
        lead_status: str,
        final_score: int,
        confidence: float,
        completion_message: str = None
    ) -> Dict[str, Any]:
        """Update lead status and final information in database."""
        try:
            from ...database import db
            
            update_data = {
                "lead_status": lead_status,
                "final_score": final_score,
                "confidence": confidence,
                "status": "completed" if lead_status != "continue" else "active",
                "updated_at": datetime.now().isoformat()
            }
            
            if completion_message:
                update_data["completion_message"] = completion_message
            
            if lead_status == "maybe":
                update_data["requires_review"] = True
                update_data["review_priority"] = "normal" if confidence < 0.5 else "high"
            
            if lead_status in ["qualified", "no"]:
                update_data["completed_at"] = datetime.now().isoformat()
            
            # Update database
            db.update_lead_session(session_id, update_data)
            
            # Add to notification queue if qualified
            if lead_status == "qualified":
                db.add_to_notification_queue(session_id, "immediate")
            elif lead_status == "maybe":
                db.add_to_notification_queue(session_id, "daily_batch")
            
            return {
                "success": True,
                "session_id": session_id,
                "lead_status": lead_status,
                "database_updated": True
            }
            
        except Exception as e:
            logger.error(f"Database status update error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Singleton instance
lead_intelligence_toolbelt = LeadIntelligenceToolbelt()