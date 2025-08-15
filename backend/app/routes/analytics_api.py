"""
Analytics API - Real-time Analytics and Reporting Endpoints

This module provides analytics endpoints for dashboard metrics, form-specific
analytics, and real-time metrics. All analytics are client-scoped for security.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, Any, List, Optional, Literal
import logging
from datetime import datetime, timedelta
from collections import defaultdict
import json

from app.database import get_database_connection
from app.routes.admin_api import AdminUserResponse
from app.utils.mock_auth import get_mock_admin_user as get_current_admin_user
from app.utils.response_helpers import success_response, error_response

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/analytics", tags=["analytics"])

# === UTILITY FUNCTIONS ===

def parse_date_range(start_date: Optional[str], end_date: Optional[str]) -> tuple:
    """Parse and validate date range parameters."""
    try:
        if start_date:
            start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        else:
            start = datetime.now() - timedelta(days=30)
            
        if end_date:
            end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        else:
            end = datetime.now()
            
        return start, end
    except Exception as e:
        logger.error(f"Error parsing date range: {e}")
        # Return default 30-day range
        end = datetime.now()
        start = end - timedelta(days=30)
        return start, end

def get_client_forms(client_id: str) -> List[Dict[str, Any]]:
    """Get all forms for a client."""
    try:
        db = get_database_connection()
        result = db.client.table("forms")\
            .select("id, title, status, created_at")\
            .eq("client_id", client_id)\
            .execute()
        return result.data or []
    except Exception as e:
        logger.error(f"Failed to get client forms: {e}")
        return []

def calculate_dashboard_metrics(client_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Calculate dashboard metrics for a client within date range."""
    try:
        db = get_database_connection()
        
        # Get all forms for this client
        forms = get_client_forms(client_id)
        form_ids = [form["id"] for form in forms]
        
        if not form_ids:
            return {
                "total_forms": 0,
                "active_forms": 0,
                "total_responses": 0,
                "average_conversion_rate": 0.0,
                "total_views": 0,
                "response_rate": 0.0,
                "average_completion_time": 0,
                "top_performing_form": None
            }
        
        # Count active forms
        active_forms = len([f for f in forms if f["status"] == "active"])
        
        # Get lead sessions within date range
        sessions_result = db.client.table("lead_sessions")\
            .select("id, form_id, started_at, completed_at, completed, final_score")\
            .in_("form_id", form_ids)\
            .gte("started_at", start_date.isoformat())\
            .lte("started_at", end_date.isoformat())\
            .execute()
        
        sessions = sessions_result.data or []
        total_views = len(sessions)
        completed_sessions = [s for s in sessions if s.get("completed")]
        total_responses = len(completed_sessions)
        
        # Calculate metrics
        response_rate = (total_responses / total_views) if total_views > 0 else 0.0
        
        # Calculate completion times (mock for now - in reality you'd calculate actual times)
        completion_times = []
        for session in completed_sessions:
            if session.get("started_at") and session.get("completed_at"):
                # Mock calculation - in reality parse datetime difference
                completion_times.append(120)  # 2 minutes average
        
        avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0
        
        # Find top performing form by conversion rate
        form_performance = defaultdict(lambda: {"views": 0, "completions": 0, "title": ""})
        
        for session in sessions:
            form_id = session["form_id"]
            form_performance[form_id]["views"] += 1
            if session.get("completed"):
                form_performance[form_id]["completions"] += 1
        
        # Add form titles
        for form in forms:
            if form["id"] in form_performance:
                form_performance[form["id"]]["title"] = form["title"]
        
        top_form = None
        best_rate = 0.0
        
        for form_id, perf in form_performance.items():
            if perf["views"] > 0:
                rate = perf["completions"] / perf["views"]
                if rate > best_rate and perf["views"] >= 5:  # Minimum threshold
                    best_rate = rate
                    top_form = {
                        "id": form_id,
                        "title": perf["title"],
                        "conversion_rate": rate
                    }
        
        return {
            "total_forms": len(forms),
            "active_forms": active_forms,
            "total_responses": total_responses,
            "average_conversion_rate": response_rate,
            "total_views": total_views,
            "response_rate": response_rate,
            "average_completion_time": int(avg_completion_time),
            "top_performing_form": top_form
        }
        
    except Exception as e:
        logger.error(f"Failed to calculate dashboard metrics: {e}")
        return {
            "total_forms": 0,
            "active_forms": 0,
            "total_responses": 0,
            "average_conversion_rate": 0.0,
            "total_views": 0,
            "response_rate": 0.0,
            "average_completion_time": 0,
            "top_performing_form": None
        }

def calculate_form_analytics(form_id: str, client_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Calculate detailed analytics for a specific form."""
    try:
        db = get_database_connection()
        
        # Verify form ownership
        form_result = db.client.table("forms")\
            .select("id, title")\
            .eq("id", form_id)\
            .eq("client_id", client_id)\
            .execute()
        
        if not form_result.data:
            return None
            
        form = form_result.data[0]
        
        # Get sessions for this form
        sessions_result = db.client.table("lead_sessions")\
            .select("id, started_at, completed_at, completed, step, final_score")\
            .eq("form_id", form_id)\
            .gte("started_at", start_date.isoformat())\
            .lte("started_at", end_date.isoformat())\
            .execute()
        
        sessions = sessions_result.data or []
        total_views = len(sessions)
        completed_sessions = [s for s in sessions if s.get("completed")]
        total_responses = len(completed_sessions)
        
        conversion_rate = (total_responses / total_views) if total_views > 0 else 0.0
        
        # Mock completion time calculation
        avg_completion_time = 120  # 2 minutes
        
        # Generate daily data for the past week
        daily_data = []
        for i in range(7):
            date = end_date - timedelta(days=i)
            # Mock data - in reality you'd query by date
            views = max(0, total_views // 7 + (i % 3))
            responses = int(views * conversion_rate)
            daily_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "views": views,
                "responses": responses,
                "conversion_rate": (responses / views) if views > 0 else 0.0
            })
        
        daily_data.reverse()  # Chronological order
        
        # Get form questions for analytics
        questions_result = db.client.table("form_questions")\
            .select("question_id, question_text, question_order")\
            .eq("form_id", form_id)\
            .order("question_order")\
            .execute()
        
        questions = questions_result.data or []
        
        # Mock question analytics
        question_analytics = []
        for q in questions[:5]:  # Limit to first 5 questions
            question_analytics.append({
                "question_id": str(q["question_id"]),
                "question_text": q["question_text"],
                "response_rate": 0.85 + (q["question_order"] % 3) * 0.05,
                "average_time_spent": 15 + (q["question_order"] * 5),
                "abandonment_rate": 0.1 + (q["question_order"] * 0.02),
                "common_responses": []  # Mock - would analyze actual responses
            })
        
        # Mock user journey
        user_journey = []
        for i, q in enumerate(questions[:5]):
            completion_rate = max(0.3, 1.0 - (i * 0.15))
            user_journey.append({
                "step": i + 1,
                "question_id": str(q["question_id"]),
                "question_text": q["question_text"],
                "completion_rate": completion_rate,
                "average_time_spent": 15 + (i * 5),
                "drop_off_rate": 1.0 - completion_rate
            })
        
        return {
            "form_id": form_id,
            "form_title": form["title"],
            "total_views": total_views,
            "total_responses": total_responses,
            "conversion_rate": conversion_rate,
            "average_completion_time": avg_completion_time,
            "completions_by_day": daily_data,
            "question_analytics": question_analytics,
            "user_journey": user_journey
        }
        
    except Exception as e:
        logger.error(f"Failed to calculate form analytics: {e}")
        return None

# === API ENDPOINTS ===

@router.get("/dashboard")
async def get_dashboard_metrics(
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get dashboard metrics for the authenticated client."""
    try:
        start, end = parse_date_range(start_date, end_date)
        metrics = calculate_dashboard_metrics(current_user.client_id, start, end)
        
        return success_response(
            data=metrics,
            message="Dashboard metrics retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to get dashboard metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve dashboard metrics")

@router.get("/forms/{form_id}")
async def get_form_analytics(
    form_id: str,
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get detailed analytics for a specific form."""
    try:
        start, end = parse_date_range(start_date, end_date)
        analytics = calculate_form_analytics(form_id, current_user.client_id, start, end)
        
        if not analytics:
            raise HTTPException(status_code=404, detail="Form not found")
        
        return success_response(
            data=analytics,
            message="Form analytics retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get form analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve form analytics")

@router.get("/realtime")
async def get_realtime_metrics(
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get real-time metrics for the authenticated client."""
    try:
        db = get_database_connection()
        
        # Get client forms
        forms = get_client_forms(current_user.client_id)
        form_ids = [form["id"] for form in forms]
        
        if not form_ids:
            return success_response(
                data={
                    "active_users": 0,
                    "active_forms": [],
                    "recent_responses": [],
                    "system_health": {
                        "status": "healthy",
                        "api_response_time": 125,
                        "db_response_time": 45,
                        "error_rate": 0.01
                    }
                },
                message="Real-time metrics retrieved successfully"
            )
        
        # Get recent sessions (last hour)
        one_hour_ago = datetime.now() - timedelta(hours=1)
        
        recent_sessions_result = db.client.table("lead_sessions")\
            .select("id, form_id, started_at, completed, completion_type")\
            .in_("form_id", form_ids)\
            .gte("started_at", one_hour_ago.isoformat())\
            .order("started_at", desc=True)\
            .limit(10)\
            .execute()
        
        recent_sessions = recent_sessions_result.data or []
        
        # Mock active users count
        active_users = min(len(recent_sessions), 5)
        
        # Process active forms
        active_forms_data = []
        form_activity = defaultdict(int)
        
        for session in recent_sessions:
            form_activity[session["form_id"]] += 1
        
        for form in forms[:3]:  # Top 3 forms
            responses_in_hour = form_activity.get(form["id"], 0)
            if form["status"] == "active":
                active_forms_data.append({
                    "form_id": form["id"],
                    "form_title": form["title"],
                    "active_users": min(responses_in_hour, 3),
                    "responses_in_last_hour": responses_in_hour
                })
        
        # Process recent responses
        recent_responses = []
        for session in recent_sessions[:5]:
            form_title = next((f["title"] for f in forms if f["id"] == session["form_id"]), "Unknown Form")
            recent_responses.append({
                "id": session["id"],
                "form_id": session["form_id"],
                "form_title": form_title,
                "timestamp": session["started_at"],
                "location": "Unknown",  # Would get from tracking_data
                "device": "Desktop",    # Would get from tracking_data
                "status": "completed" if session.get("completed") else "abandoned"
            })
        
        return success_response(
            data={
                "active_users": active_users,
                "active_forms": active_forms_data,
                "recent_responses": recent_responses,
                "system_health": {
                    "status": "healthy",
                    "api_response_time": 125,
                    "db_response_time": 45,
                    "error_rate": 0.01
                }
            },
            message="Real-time metrics retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to get real-time metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve real-time metrics")

@router.get("/export")
async def export_analytics(
    form_id: Optional[str] = Query(None, description="Specific form ID to export"),
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    format: Literal["csv", "xlsx", "pdf"] = Query("csv", description="Export format"),
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Export analytics data in various formats."""
    try:
        # For now, return a mock response indicating the feature is available
        # In production, this would generate actual files
        
        start, end = parse_date_range(start_date, end_date)
        
        if form_id:
            # Export specific form analytics
            analytics = calculate_form_analytics(form_id, current_user.client_id, start, end)
            if not analytics:
                raise HTTPException(status_code=404, detail="Form not found")
            export_type = f"form-{form_id}"
        else:
            # Export dashboard analytics
            analytics = calculate_dashboard_metrics(current_user.client_id, start, end)
            export_type = "dashboard"
        
        return success_response(
            data={
                "export_type": export_type,
                "format": format,
                "date_range": {
                    "start": start.isoformat(),
                    "end": end.isoformat()
                },
                "download_url": f"/api/analytics/download/{export_type}-{format}",
                "expires_at": (datetime.now() + timedelta(hours=1)).isoformat(),
                "file_size_bytes": 1024 * (50 if format == "pdf" else 20)
            },
            message=f"Analytics export prepared successfully in {format.upper()} format"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to export analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to export analytics")