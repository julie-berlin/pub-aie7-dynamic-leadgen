"""Lead Intelligence Toolbelt with Tavily and Maps integration."""

from typing import Dict, Any, List, Optional
import json
import logging
import os
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class LeadIntelligenceToolbelt:
    """Toolbelt for lead intelligence operations with external tools."""
    
    def __init__(self):
        self.tavily_tool = None
        self.maps_enabled = False
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize external tools if available."""
        try:
            # Initialize Tavily if API key is available
            tavily_key = os.getenv("TAVILY_API_KEY")
            if tavily_key:
                from tavily import TavilyClient
                self.tavily_client = TavilyClient(api_key=tavily_key)
                logger.info("✅ Tavily tool initialized with real API")
            else:
                logger.info("⚠️ Tavily API key not found - will use mock responses")
                self.tavily_client = None
        except ImportError:
            logger.warning("Tavily library not installed - will use mock responses")
            self.tavily_client = None
        except Exception as e:
            logger.error(f"Failed to initialize Tavily: {e}")
            self.tavily_client = None
        
        # Check for Google Maps API
        maps_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if maps_key:
            self.maps_enabled = True
            logger.info("✅ Google Maps API key found")
        else:
            logger.info("⚠️ Google Maps API key not found - will use mock responses")
    
    def save_responses_to_database(
        self, 
        session_id: str, 
        responses: List[Dict],
        form_id: str
    ) -> Dict[str, Any]:
        """Save user responses to database."""
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            from database.sqlite_db import db
            
            saved_count = 0
            errors = []
            
            for response in responses:
                try:
                    response_data = {
                        "session_id": session_id,
                        "question_id": response.get("question_id"),
                        "question_text": response.get("question_text", ""),
                        "phrased_question": response.get("phrased_question", ""),
                        "answer": response.get("answer"),
                        "step": response.get("step", 0),
                        "score_awarded": 0
                    }
                    
                    if db.save_response(session_id, response_data):
                        saved_count += 1
                    
                except Exception as e:
                    errors.append(f"Failed to save response {response.get('question_id')}: {e}")
                    logger.error(f"Response save error: {e}")
            
            # Update session
            db.update_lead_session(session_id, {
                "last_updated": datetime.now().isoformat()
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
                answer = response.get("answer", "").lower()
                
                # Get scoring rubric for this question
                rubric = scoring_rubrics.get(str(question_id), {})
                if not rubric:
                    continue
                
                # Simple scoring based on keywords
                question_score = 0
                max_score = 10
                
                # Check for positive indicators
                positive_keywords = rubric.get("positive_keywords", ["yes", "immediately", "urgent", "asap"])
                negative_keywords = rubric.get("negative_keywords", ["no", "never", "not interested"])
                
                for keyword in positive_keywords:
                    if keyword in answer:
                        question_score = max_score
                        break
                
                for keyword in negative_keywords:
                    if keyword in answer:
                        question_score = 0
                        break
                
                # Default middle score if no keywords match
                if question_score == 0 and not any(kw in answer for kw in negative_keywords):
                    question_score = max_score // 2
                
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
    
    def execute_tavily_search(self, query: str) -> Dict[str, Any]:
        """Execute Tavily web search for lead validation."""
        try:
            logger.info(f"🔍 Executing Tavily search: {query}")
            
            if self.tavily_client:
                # Real Tavily API call
                search_result = self.tavily_client.search(query, max_results=3)
                
                # Extract relevant information
                results = []
                for result in search_result.get('results', []):
                    results.append({
                        'title': result.get('title'),
                        'content': result.get('content')[:200],
                        'url': result.get('url')
                    })
                
                # Determine score boost based on results
                score_boost = 0
                if results:
                    # Check for positive validation
                    positive_found = any(
                        'legitimate' in str(r).lower() or 
                        'established' in str(r).lower() or
                        'trusted' in str(r).lower()
                        for r in results
                    )
                    if positive_found:
                        score_boost = 15
                        logger.info(f"✅ Tavily validation successful: +{score_boost} points")
                    else:
                        score_boost = 5
                        logger.info(f"ℹ️ Tavily found results but neutral: +{score_boost} points")
                
                return {
                    "success": True,
                    "query": query,
                    "results": results,
                    "score_boost": score_boost,
                    "executed_at": datetime.now().isoformat(),
                    "source": "real_api"
                }
            else:
                # Mock response for testing
                logger.info("📦 Using mock Tavily response")
                mock_results = [
                    {
                        'title': f'Business Profile: {query}',
                        'content': f'Established business with good reputation. Verified and legitimate operation.',
                        'url': 'https://example.com/business-profile'
                    }
                ]
                
                return {
                    "success": True,
                    "query": query,
                    "results": mock_results,
                    "score_boost": 10,
                    "executed_at": datetime.now().isoformat(),
                    "source": "mock"
                }
            
        except Exception as e:
            logger.error(f"❌ Tavily search error: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "score_boost": 0
            }
    
    def execute_maps_validation(
        self, 
        origin: str, 
        destination: str,
        service_area_radius: float = 25.0
    ) -> Dict[str, Any]:
        """Execute Google Maps distance validation."""
        try:
            logger.info(f"📍 Maps validation: {origin} to {destination}")
            
            if self.maps_enabled:
                # Real Google Maps API call would go here
                # For now, simulate with realistic data
                import googlemaps
                gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))
                
                result = gmaps.distance_matrix(
                    origins=[origin],
                    destinations=[destination],
                    units="imperial"
                )
                
                if result['status'] == 'OK':
                    element = result['rows'][0]['elements'][0]
                    if element['status'] == 'OK':
                        distance_text = element['distance']['text']
                        distance_value = element['distance']['value'] / 1609.34  # Convert to miles
                        duration_text = element['duration']['text']
                        
                        # Calculate score boost based on distance
                        if distance_value <= 5:
                            score_boost = 20
                        elif distance_value <= 10:
                            score_boost = 15
                        elif distance_value <= service_area_radius:
                            score_boost = 10
                        else:
                            score_boost = -10
                        
                        logger.info(f"✅ Maps validation: {distance_text}, score boost: {score_boost}")
                        
                        return {
                            "success": True,
                            "origin": origin,
                            "destination": destination,
                            "distance": distance_text,
                            "duration": duration_text,
                            "distance_miles": distance_value,
                            "in_service_area": distance_value <= service_area_radius,
                            "score_boost": score_boost,
                            "executed_at": datetime.now().isoformat(),
                            "source": "real_api"
                        }
            
            # Mock response
            logger.info("📦 Using mock Maps response")
            distance = random.uniform(3, 30)
            duration = int(distance * 2.5)
            
            # Calculate score boost
            if distance <= 5:
                score_boost = 20
            elif distance <= 10:
                score_boost = 15
            elif distance <= service_area_radius:
                score_boost = 10
            else:
                score_boost = -5
            
            return {
                "success": True,
                "origin": origin,
                "destination": destination,
                "distance": f"{distance:.1f} miles",
                "duration": f"{duration} minutes",
                "distance_miles": distance,
                "in_service_area": distance <= service_area_radius,
                "score_boost": score_boost,
                "executed_at": datetime.now().isoformat(),
                "source": "mock"
            }
            
        except Exception as e:
            logger.error(f"❌ Maps validation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "score_boost": 0
            }
    
    def generate_default_messages(self, lead_status: str, client_name: str) -> Dict[str, str]:
        """Generate default completion messages by status."""
        messages = {
            "yes": f"Excellent news! {client_name} is excited to work with you. We'll be in touch within 24 hours to discuss your needs and get started right away.",
            "maybe": f"Thank you for your interest in {client_name}! While we need to review a few more details, we're optimistic about finding a solution that works for you. Expect to hear from us within 48 hours.",
            "no": f"Thank you for considering {client_name}. Based on your responses, we may not be the perfect fit right now, but we appreciate your time and wish you the best in finding the right solution.",
            "continue": "Let's continue with a few more questions to better understand your needs."
        }
        return messages
    
    def update_lead_session_status(
        self,
        session_id: str,
        lead_status: str,
        final_score: int,
        completion_message: str = None
    ) -> Dict[str, Any]:
        """Update lead session with final status."""
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            from database.sqlite_db import db
            
            update_data = {
                "lead_status": lead_status,
                "final_score": final_score,
                "completed": lead_status != "continue",
                "completion_type": "qualified" if lead_status == "yes" else "unqualified" if lead_status == "no" else "maybe"
            }
            
            if completion_message:
                update_data["completion_message"] = completion_message
            
            if lead_status != "continue":
                update_data["completed_at"] = datetime.now().isoformat()
            
            success = db.update_lead_session(session_id, update_data)
            
            return {
                "success": success,
                "session_id": session_id,
                "status_updated": lead_status
            }
            
        except Exception as e:
            logger.error(f"Failed to update session status: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Global toolbelt instance
lead_intelligence_toolbelt = LeadIntelligenceToolbelt()