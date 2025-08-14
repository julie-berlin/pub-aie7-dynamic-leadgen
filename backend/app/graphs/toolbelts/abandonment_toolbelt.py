"""Abandonment Toolbelt - Utilities for detecting and handling survey abandonment."""

from typing import Dict, Any, Optional
import json
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AbandonmentToolbelt:
    """Toolbelt for abandonment detection and handling."""
    
    def __init__(self):
        self.default_timeout_minutes = 10
        self.warning_threshold_minutes = 5
    
    def check_abandonment(
        self, 
        session_id: str,
        last_activity_time: Optional[datetime] = None,
        custom_timeout_minutes: Optional[int] = None
    ) -> Dict[str, Any]:
        """Check if a session should be considered abandoned."""
        try:
            timeout_minutes = custom_timeout_minutes or self.default_timeout_minutes
            
            if not last_activity_time:
                # Try to get from database
                last_activity_time = self._get_last_activity_from_db(session_id)
            
            if not last_activity_time:
                return {
                    "is_abandoned": False,
                    "reason": "no_activity_time",
                    "status": "active"
                }
            
            # Calculate time since last activity
            if isinstance(last_activity_time, str):
                last_activity_time = datetime.fromisoformat(last_activity_time.replace('Z', '+00:00'))
            
            time_since_activity = datetime.now() - last_activity_time
            minutes_inactive = time_since_activity.total_seconds() / 60
            
            # Determine status
            if minutes_inactive > timeout_minutes:
                return {
                    "is_abandoned": True,
                    "reason": "timeout",
                    "status": "abandoned",
                    "minutes_inactive": minutes_inactive,
                    "timeout_threshold": timeout_minutes,
                    "abandonment_type": "timeout"
                }
            elif minutes_inactive > self.warning_threshold_minutes:
                return {
                    "is_abandoned": False,
                    "reason": "warning_threshold",
                    "status": "at_risk",
                    "minutes_inactive": minutes_inactive,
                    "minutes_until_timeout": timeout_minutes - minutes_inactive
                }
            else:
                return {
                    "is_abandoned": False,
                    "reason": "active",
                    "status": "active",
                    "minutes_inactive": minutes_inactive
                }
                
        except Exception as e:
            logger.error(f"Abandonment check error: {e}")
            return {
                "is_abandoned": False,
                "error": str(e),
                "status": "error"
            }
    
    def _get_last_activity_from_db(self, session_id: str) -> Optional[datetime]:
        """Get last activity time from database."""
        try:
            from ...database import db
            session_data = db.get_lead_session(session_id)
            if session_data:
                return session_data.get("last_activity_time")
            return None
        except Exception as e:
            logger.error(f"Failed to get last activity from DB: {e}")
            return None
    
    def mark_session_abandoned(
        self,
        session_id: str,
        abandonment_reason: str = "timeout",
        abandonment_details: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Mark a session as abandoned in the database."""
        try:
            from ...database import db
            
            # Prepare abandonment data
            update_data = {
                "status": "abandoned",
                "abandoned_at": datetime.now().isoformat(),
                "abandonment_reason": abandonment_reason,
                "completion_type": "abandoned"
            }
            
            # Add details if provided
            if abandonment_details:
                update_data["abandonment_details"] = json.dumps(abandonment_details)
            
            # Update database
            db.update_lead_session(session_id, update_data)
            
            # Log abandonment for analytics
            self._log_abandonment_analytics(session_id, abandonment_reason, abandonment_details)
            
            return {
                "success": True,
                "session_id": session_id,
                "marked_abandoned": True,
                "abandonment_reason": abandonment_reason,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to mark session abandoned: {e}")
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id
            }
    
    def _log_abandonment_analytics(
        self,
        session_id: str,
        reason: str,
        details: Dict[str, Any] = None
    ):
        """Log abandonment for analytics purposes."""
        try:
            from ...database import db
            
            analytics_data = {
                "session_id": session_id,
                "event_type": "abandonment",
                "abandonment_reason": reason,
                "timestamp": datetime.now().isoformat()
            }
            
            if details:
                analytics_data.update({
                    "questions_answered": details.get("questions_answered", 0),
                    "last_question_id": details.get("last_question_id"),
                    "time_on_form": details.get("time_on_form", 0),
                    "abandonment_point": details.get("abandonment_point", "unknown")
                })
            
            db.log_analytics_event(analytics_data)
            
        except Exception as e:
            logger.error(f"Failed to log abandonment analytics: {e}")
    
    def calculate_abandonment_risk(
        self,
        responses_count: int,
        time_on_form_minutes: float,
        response_depth: float,
        last_response_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Calculate risk score for potential abandonment."""
        try:
            risk_score = 0.0
            risk_factors = []
            recommendations = []
            
            # Factor 1: Number of questions answered
            if responses_count > 10:
                risk_score += 0.4
                risk_factors.append("high_question_count")
                recommendations.append("Consider survey completion")
            elif responses_count > 7:
                risk_score += 0.2
                risk_factors.append("moderate_question_count")
                recommendations.append("Limit to 1-2 more questions")
            
            # Factor 2: Time on form
            if time_on_form_minutes > 10:
                risk_score += 0.3
                risk_factors.append("long_duration")
                recommendations.append("Use urgent engagement messaging")
            elif time_on_form_minutes > 5:
                risk_score += 0.15
                risk_factors.append("moderate_duration")
                recommendations.append("Add motivational messaging")
            
            # Factor 3: Response depth (quality)
            if response_depth < 0.3:
                risk_score += 0.2
                risk_factors.append("low_engagement")
                recommendations.append("Simplify questions")
            
            # Factor 4: Time since last response
            if last_response_time:
                if isinstance(last_response_time, str):
                    last_response_time = datetime.fromisoformat(last_response_time.replace('Z', '+00:00'))
                
                minutes_since_response = (datetime.now() - last_response_time).total_seconds() / 60
                if minutes_since_response > 3:
                    risk_score += 0.1
                    risk_factors.append("slow_response_time")
                    recommendations.append("Consider re-engagement prompt")
            
            # Normalize risk score
            risk_score = min(1.0, risk_score)
            
            # Determine risk level
            if risk_score > 0.7:
                risk_level = "high"
                recommendations.insert(0, "URGENT: High abandonment risk")
            elif risk_score > 0.4:
                risk_level = "medium"
                recommendations.insert(0, "Moderate abandonment risk")
            else:
                risk_level = "low"
                recommendations.insert(0, "Low abandonment risk")
            
            return {
                "risk_score": risk_score,
                "risk_level": risk_level,
                "risk_factors": risk_factors,
                "recommendations": recommendations,
                "metrics": {
                    "responses_count": responses_count,
                    "time_on_form_minutes": time_on_form_minutes,
                    "response_depth": response_depth
                }
            }
            
        except Exception as e:
            logger.error(f"Risk calculation error: {e}")
            return {
                "risk_score": 0.5,
                "risk_level": "unknown",
                "error": str(e)
            }
    
    def get_re_engagement_strategy(
        self,
        risk_level: str,
        responses_count: int,
        client_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Get re-engagement strategy based on risk level."""
        strategies = {
            "high": {
                "approach": "urgent",
                "tactics": [
                    "show_progress_bar",
                    "emphasize_almost_done",
                    "offer_immediate_value",
                    "simplify_remaining_questions"
                ],
                "message_suggestions": [
                    "You're almost there! Just 2 more quick questions.",
                    "Great progress! Let's finish this up in under a minute.",
                    "Almost done! Your responses help us serve you better."
                ],
                "ui_changes": [
                    "highlight_submit_button",
                    "reduce_visual_clutter",
                    "show_completion_percentage"
                ]
            },
            "medium": {
                "approach": "motivational",
                "tactics": [
                    "provide_encouragement",
                    "show_value_proposition",
                    "maintain_conversational_tone"
                ],
                "message_suggestions": [
                    "Thanks for your responses so far! A few more will help us customize our service for you.",
                    "You're doing great! Your input is really valuable to us.",
                    "We appreciate your time. Just a couple more questions to go."
                ],
                "ui_changes": [
                    "show_progress_indicator",
                    "add_encouraging_icons",
                    "maintain_visual_interest"
                ]
            },
            "low": {
                "approach": "standard",
                "tactics": [
                    "maintain_current_flow",
                    "focus_on_value_exchange",
                    "keep_professional_tone"
                ],
                "message_suggestions": [
                    "Let's continue to see how we can help you.",
                    "Next, we'd like to know more about your specific needs.",
                    "Your responses help us provide the best service possible."
                ],
                "ui_changes": [
                    "standard_ui",
                    "clear_navigation",
                    "professional_design"
                ]
            }
        }
        
        strategy = strategies.get(risk_level, strategies["low"])
        
        # Customize based on client info if available
        if client_info:
            business_name = client_info.get("business_name", "we")
            strategy["message_suggestions"] = [
                msg.replace("us", business_name).replace("we", business_name)
                for msg in strategy["message_suggestions"]
            ]
        
        # Add response count specific adjustments
        if responses_count > 8:
            strategy["tactics"].append("consider_early_completion")
            strategy["message_suggestions"].append("Would you like to submit what you have so far?")
        
        return strategy
    
    def handle_session_recovery(
        self,
        session_id: str,
        recovery_reason: str = "user_returned"
    ) -> Dict[str, Any]:
        """Handle recovery of an abandoned or at-risk session."""
        try:
            from ...database import db
            
            # Update session status
            update_data = {
                "status": "recovered",
                "recovered_at": datetime.now().isoformat(),
                "recovery_reason": recovery_reason,
                "last_activity_time": datetime.now().isoformat()
            }
            
            db.update_lead_session(session_id, update_data)
            
            # Log recovery event
            db.log_analytics_event({
                "session_id": session_id,
                "event_type": "session_recovery",
                "recovery_reason": recovery_reason,
                "timestamp": datetime.now().isoformat()
            })
            
            return {
                "success": True,
                "session_id": session_id,
                "recovered": True,
                "recovery_reason": recovery_reason
            }
            
        except Exception as e:
            logger.error(f"Session recovery error: {e}")
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id
            }


# Singleton instance
abandonment_toolbelt = AbandonmentToolbelt()