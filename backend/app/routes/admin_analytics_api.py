"""
Admin Analytics API - Analytics Dashboard and Reporting for Admin Interface

This module provides API endpoints for:
1. Dashboard-level analytics across all forms
2. Client-wide performance metrics
3. Analytics data export functionality
4. Real-time metrics and monitoring
"""

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Literal
import logging
from datetime import datetime, date, timedelta
from decimal import Decimal
import csv
import io
import json
from dataclasses import asdict

from app.database import get_database_connection
from app.routes.admin_api import get_current_admin_user, AdminUserResponse
from app.utils.response_helpers import create_success_response

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin/analytics", tags=["admin-analytics"])

# === PYDANTIC MODELS FOR ADMIN ANALYTICS ===

class DashboardMetrics(BaseModel):
    """High-level dashboard metrics for admin interface."""
    total_forms: int
    active_forms: int
    draft_forms: int
    paused_forms: int
    archived_forms: int
    
    total_responses: int
    total_views: int
    average_conversion_rate: float
    total_qualified_leads: int
    total_maybe_leads: int
    total_unqualified_leads: int
    
    response_rate: float
    average_completion_time: int  # seconds
    
    # Performance indicators
    top_performing_form: Optional[Dict[str, Any]] = None
    worst_performing_form: Optional[Dict[str, Any]] = None
    
    # Time comparisons
    responses_change_percent: float = 0.0
    conversion_change_percent: float = 0.0

class FormPerformanceSummary(BaseModel):
    """Summary performance data for a form."""
    form_id: str
    form_title: str
    status: str
    total_views: int
    total_responses: int
    conversion_rate: float
    average_completion_time: int
    qualified_leads: int
    maybe_leads: int
    unqualified_leads: int
    last_response_at: Optional[datetime]
    created_at: datetime

class RealTimeMetrics(BaseModel):
    """Real-time metrics for monitoring."""
    active_sessions: int
    sessions_last_hour: int
    responses_last_hour: int
    current_conversion_rate: float
    
    active_forms: List[Dict[str, Any]]
    recent_responses: List[Dict[str, Any]]
    
    system_health: Dict[str, Any]

class AnalyticsExportRequest(BaseModel):
    """Request for analytics data export."""
    form_ids: Optional[List[str]] = None  # None = all forms
    start_date: date
    end_date: date
    format: Literal["csv", "xlsx", "json"] = "csv"
    include_responses: bool = False
    include_events: bool = False
    
class DateRangeAnalytics(BaseModel):
    """Analytics data for a specific date range."""
    start_date: date
    end_date: date
    daily_metrics: List[Dict[str, Any]]
    summary: DashboardMetrics

# === DASHBOARD ANALYTICS ENDPOINTS ===

@router.get("/dashboard", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    days: int = Query(30, ge=1, le=365, description="Number of days for metrics"),
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get high-level dashboard metrics for the client."""
    try:
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Get form counts by status
            cursor.execute("""
                SELECT 
                    status,
                    COUNT(*) as count
                FROM forms 
                WHERE client_id = %s
                GROUP BY status
            """, (current_user.client_id,))
            
            form_counts = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Get aggregated metrics from performance table
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(fpm.total_views), 0) as total_views,
                    COALESCE(SUM(fpm.total_starts), 0) as total_starts,
                    COALESCE(SUM(fpm.total_completions), 0) as total_completions,
                    COALESCE(AVG(fpm.conversion_rate), 0) as avg_conversion_rate,
                    COALESCE(AVG(fpm.avg_completion_time_seconds), 0) as avg_completion_time,
                    COALESCE(SUM(fpm.mobile_views + fpm.desktop_views + fpm.tablet_views), 0) as total_device_views
                FROM form_performance_metrics fpm
                JOIN forms f ON f.id = fpm.form_id
                WHERE f.client_id = %s 
                AND fpm.date_recorded BETWEEN %s AND %s
            """, (current_user.client_id, start_date, end_date))
            
            perf_result = cursor.fetchone()
            
            # Get lead quality metrics from sessions
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_responses,
                    COUNT(CASE WHEN lead_status = 'yes' THEN 1 END) as qualified_leads,
                    COUNT(CASE WHEN lead_status = 'maybe' THEN 1 END) as maybe_leads,
                    COUNT(CASE WHEN lead_status = 'no' THEN 1 END) as unqualified_leads
                FROM lead_sessions ls
                JOIN forms f ON f.id = ls.form_id
                WHERE f.client_id = %s 
                AND ls.started_at::date BETWEEN %s AND %s
                AND ls.status = 'completed'
            """, (current_user.client_id, start_date, end_date))
            
            lead_result = cursor.fetchone()
            
            # Get top performing form
            cursor.execute("""
                SELECT 
                    f.id,
                    f.title,
                    AVG(fpm.conversion_rate) as avg_conversion
                FROM forms f
                JOIN form_performance_metrics fpm ON f.id = fpm.form_id
                WHERE f.client_id = %s 
                AND fpm.date_recorded BETWEEN %s AND %s
                GROUP BY f.id, f.title
                HAVING SUM(fpm.total_starts) > 10  -- Only forms with meaningful traffic
                ORDER BY avg_conversion DESC
                LIMIT 1
            """, (current_user.client_id, start_date, end_date))
            
            top_form_result = cursor.fetchone()
            
            # Get worst performing form
            cursor.execute("""
                SELECT 
                    f.id,
                    f.title,
                    AVG(fpm.conversion_rate) as avg_conversion
                FROM forms f
                JOIN form_performance_metrics fpm ON f.id = fpm.form_id
                WHERE f.client_id = %s 
                AND fpm.date_recorded BETWEEN %s AND %s
                GROUP BY f.id, f.title
                HAVING SUM(fpm.total_starts) > 10  -- Only forms with meaningful traffic
                ORDER BY avg_conversion ASC
                LIMIT 1
            """, (current_user.client_id, start_date, end_date))
            
            worst_form_result = cursor.fetchone()
            
            # Calculate period-over-period changes
            prev_start_date = start_date - timedelta(days=days)
            prev_end_date = start_date - timedelta(days=1)
            
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(fpm.total_completions), 0) as prev_responses,
                    COALESCE(AVG(fpm.conversion_rate), 0) as prev_conversion
                FROM form_performance_metrics fpm
                JOIN forms f ON f.id = fpm.form_id
                WHERE f.client_id = %s 
                AND fpm.date_recorded BETWEEN %s AND %s
            """, (current_user.client_id, prev_start_date, prev_end_date))
            
            prev_result = cursor.fetchone()
            
            # Calculate changes
            current_responses = lead_result[0] if lead_result else 0
            prev_responses = prev_result[0] if prev_result else 0
            responses_change = ((current_responses - prev_responses) / prev_responses * 100) if prev_responses > 0 else 0
            
            current_conversion = perf_result[3] if perf_result else 0
            prev_conversion = prev_result[1] if prev_result else 0
            conversion_change = ((current_conversion - prev_conversion) / prev_conversion * 100) if prev_conversion > 0 else 0
            
            # Build response
            top_form = None
            if top_form_result:
                top_form = {
                    "id": str(top_form_result[0]),
                    "title": top_form_result[1],
                    "conversion_rate": float(top_form_result[2])
                }
            
            worst_form = None
            if worst_form_result:
                worst_form = {
                    "id": str(worst_form_result[0]),
                    "title": worst_form_result[1],
                    "conversion_rate": float(worst_form_result[2])
                }
            
            return DashboardMetrics(
                total_forms=sum(form_counts.values()),
                active_forms=form_counts.get('active', 0),
                draft_forms=form_counts.get('draft', 0),
                paused_forms=form_counts.get('paused', 0),
                archived_forms=form_counts.get('archived', 0),
                
                total_responses=current_responses,
                total_views=perf_result[0] if perf_result else 0,
                average_conversion_rate=float(perf_result[3]) if perf_result else 0.0,
                total_qualified_leads=lead_result[1] if lead_result else 0,
                total_maybe_leads=lead_result[2] if lead_result else 0,
                total_unqualified_leads=lead_result[3] if lead_result else 0,
                
                response_rate=float(perf_result[3]) if perf_result else 0.0,
                average_completion_time=int(perf_result[4]) if perf_result else 0,
                
                top_performing_form=top_form,
                worst_performing_form=worst_form,
                
                responses_change_percent=responses_change,
                conversion_change_percent=conversion_change
            )
            
    except Exception as e:
        logger.error(f"Failed to get dashboard metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve dashboard metrics")

@router.get("/forms", response_model=List[FormPerformanceSummary])
async def get_forms_performance_summary(
    days: int = Query(30, ge=1, le=365, description="Number of days for metrics"),
    status: Optional[str] = Query(None, description="Filter by form status"),
    sort_by: str = Query("conversion_rate", description="Sort by field"),
    sort_order: Literal["asc", "desc"] = Query("desc", description="Sort order"),
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get performance summary for all forms."""
    try:
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Build WHERE clause
            where_conditions = ["f.client_id = %s"]
            params = [current_user.client_id]
            
            if status:
                where_conditions.append("f.status = %s")
                params.append(status)
            
            where_clause = " AND ".join(where_conditions)
            
            # Map sort fields to actual columns
            sort_field_map = {
                "conversion_rate": "avg_conversion_rate",
                "total_responses": "total_responses",
                "total_views": "total_views",
                "completion_time": "avg_completion_time",
                "created_at": "f.created_at"
            }
            actual_sort_field = sort_field_map.get(sort_by, "avg_conversion_rate")
            
            query = f"""
                SELECT 
                    f.id,
                    f.title,
                    f.status,
                    COALESCE(SUM(fpm.total_views), 0) as total_views,
                    COALESCE(SUM(fpm.total_completions), 0) as total_responses,
                    COALESCE(AVG(fpm.conversion_rate), 0) as avg_conversion_rate,
                    COALESCE(AVG(fpm.avg_completion_time_seconds), 0) as avg_completion_time,
                    COALESCE(SUM(ls_agg.qualified_leads), 0) as qualified_leads,
                    COALESCE(SUM(ls_agg.maybe_leads), 0) as maybe_leads,
                    COALESCE(SUM(ls_agg.unqualified_leads), 0) as unqualified_leads,
                    ls_agg.last_response_at,
                    f.created_at
                FROM forms f
                LEFT JOIN form_performance_metrics fpm ON f.id = fpm.form_id 
                    AND fpm.date_recorded BETWEEN %s AND %s
                LEFT JOIN (
                    SELECT 
                        form_id,
                        COUNT(CASE WHEN lead_status = 'yes' THEN 1 END) as qualified_leads,
                        COUNT(CASE WHEN lead_status = 'maybe' THEN 1 END) as maybe_leads,
                        COUNT(CASE WHEN lead_status = 'no' THEN 1 END) as unqualified_leads,
                        MAX(completed_at) as last_response_at
                    FROM lead_sessions 
                    WHERE started_at::date BETWEEN %s AND %s
                    AND status = 'completed'
                    GROUP BY form_id
                ) ls_agg ON f.id = ls_agg.form_id
                WHERE {where_clause}
                GROUP BY f.id, f.title, f.status, f.created_at, ls_agg.last_response_at
                ORDER BY {actual_sort_field} {sort_order.upper()}
            """
            
            params = [start_date, end_date, start_date, end_date] + params
            cursor.execute(query, params)
            
            forms = []
            for row in cursor.fetchall():
                forms.append(FormPerformanceSummary(
                    form_id=str(row[0]),
                    form_title=row[1],
                    status=row[2],
                    total_views=row[3],
                    total_responses=row[4],
                    conversion_rate=float(row[5]),
                    average_completion_time=int(row[6]),
                    qualified_leads=row[7],
                    maybe_leads=row[8],
                    unqualified_leads=row[9],
                    last_response_at=row[10],
                    created_at=row[11]
                ))
            
            return forms
            
    except Exception as e:
        logger.error(f"Failed to get forms performance summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve forms performance")

@router.get("/realtime", response_model=RealTimeMetrics)
async def get_realtime_metrics(
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get real-time metrics for monitoring dashboard."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Get active sessions (last 5 minutes)
            cursor.execute("""
                SELECT COUNT(DISTINCT ls.session_id)
                FROM lead_sessions ls
                JOIN forms f ON f.id = ls.form_id
                WHERE f.client_id = %s
                AND ls.last_activity_at > NOW() - INTERVAL '5 minutes'
                AND ls.status = 'active'
            """, (current_user.client_id,))
            
            active_sessions = cursor.fetchone()[0] or 0
            
            # Get sessions last hour
            cursor.execute("""
                SELECT COUNT(*)
                FROM lead_sessions ls
                JOIN forms f ON f.id = ls.form_id
                WHERE f.client_id = %s
                AND ls.started_at > NOW() - INTERVAL '1 hour'
            """, (current_user.client_id,))
            
            sessions_last_hour = cursor.fetchone()[0] or 0
            
            # Get responses last hour
            cursor.execute("""
                SELECT COUNT(*)
                FROM lead_sessions ls
                JOIN forms f ON f.id = ls.form_id
                WHERE f.client_id = %s
                AND ls.completed_at > NOW() - INTERVAL '1 hour'
                AND ls.status = 'completed'
            """, (current_user.client_id,))
            
            responses_last_hour = cursor.fetchone()[0] or 0
            
            # Calculate current conversion rate
            current_conversion_rate = (responses_last_hour / sessions_last_hour * 100) if sessions_last_hour > 0 else 0
            
            # Get active forms with recent activity
            cursor.execute("""
                SELECT 
                    f.id,
                    f.title,
                    COUNT(DISTINCT ls.session_id) as active_users,
                    COUNT(CASE WHEN ls.completed_at > NOW() - INTERVAL '1 hour' THEN 1 END) as responses_last_hour
                FROM forms f
                LEFT JOIN lead_sessions ls ON f.id = ls.form_id 
                    AND ls.last_activity_at > NOW() - INTERVAL '10 minutes'
                WHERE f.client_id = %s AND f.status = 'active'
                GROUP BY f.id, f.title
                HAVING COUNT(DISTINCT ls.session_id) > 0
                ORDER BY active_users DESC
                LIMIT 5
            """, (current_user.client_id,))
            
            active_forms = [
                {
                    "form_id": str(row[0]),
                    "form_title": row[1],
                    "active_users": row[2],
                    "responses_last_hour": row[3]
                }
                for row in cursor.fetchall()
            ]
            
            # Get recent responses
            cursor.execute("""
                SELECT 
                    f.title,
                    ls.completed_at,
                    ls.lead_status,
                    td.utm_source
                FROM lead_sessions ls
                JOIN forms f ON f.id = ls.form_id
                LEFT JOIN tracking_data td ON ls.session_id = td.session_id
                WHERE f.client_id = %s
                AND ls.completed_at > NOW() - INTERVAL '1 hour'
                AND ls.status = 'completed'
                ORDER BY ls.completed_at DESC
                LIMIT 10
            """, (current_user.client_id,))
            
            recent_responses = [
                {
                    "form_title": row[0],
                    "completed_at": row[1].isoformat() if row[1] else None,
                    "lead_status": row[2],
                    "source": row[3] or "direct"
                }
                for row in cursor.fetchall()
            ]
            
            # System health (simplified)
            system_health = {
                "status": "healthy",
                "api_response_time": 150,  # ms (would be measured)
                "db_response_time": 25,    # ms (would be measured)
                "error_rate": 0.01,        # % (would be calculated)
                "uptime": 99.9             # % (would be monitored)
            }
            
            return RealTimeMetrics(
                active_sessions=active_sessions,
                sessions_last_hour=sessions_last_hour,
                responses_last_hour=responses_last_hour,
                current_conversion_rate=current_conversion_rate,
                active_forms=active_forms,
                recent_responses=recent_responses,
                system_health=system_health
            )
            
    except Exception as e:
        logger.error(f"Failed to get real-time metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve real-time metrics")

@router.get("/date-range", response_model=DateRangeAnalytics)
async def get_date_range_analytics(
    start_date: date = Query(..., description="Start date for analytics"),
    end_date: date = Query(..., description="End date for analytics"),
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get analytics data for a specific date range."""
    try:
        if start_date > end_date:
            raise HTTPException(status_code=400, detail="Start date must be before end date")
        
        # Get daily metrics for the date range
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    fpm.date_recorded,
                    SUM(fpm.total_views) as daily_views,
                    SUM(fpm.total_starts) as daily_starts,
                    SUM(fpm.total_completions) as daily_completions,
                    AVG(fpm.conversion_rate) as daily_conversion_rate,
                    SUM(fpm.mobile_views) as mobile_views,
                    SUM(fpm.desktop_views) as desktop_views,
                    COUNT(DISTINCT fpm.form_id) as active_forms
                FROM form_performance_metrics fpm
                JOIN forms f ON f.id = fpm.form_id
                WHERE f.client_id = %s 
                AND fpm.date_recorded BETWEEN %s AND %s
                GROUP BY fpm.date_recorded
                ORDER BY fpm.date_recorded
            """, (current_user.client_id, start_date, end_date))
            
            daily_metrics = []
            for row in cursor.fetchall():
                daily_metrics.append({
                    "date": row[0].isoformat(),
                    "views": row[1] or 0,
                    "starts": row[2] or 0,
                    "completions": row[3] or 0,
                    "conversion_rate": float(row[4]) if row[4] else 0.0,
                    "mobile_views": row[5] or 0,
                    "desktop_views": row[6] or 0,
                    "active_forms": row[7] or 0
                })
        
        # Get summary metrics for the period
        days_diff = (end_date - start_date).days + 1
        summary = await get_dashboard_metrics(days_diff, current_user)
        
        return DateRangeAnalytics(
            start_date=start_date,
            end_date=end_date,
            daily_metrics=daily_metrics,
            summary=summary
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get date range analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve date range analytics")

# === ANALYTICS EXPORT ENDPOINTS ===

@router.post("/export")
async def export_analytics(
    export_request: AnalyticsExportRequest,
    background_tasks: BackgroundTasks,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Export analytics data in various formats."""
    try:
        conn = get_database_connection()
        
        # Validate date range
        if export_request.start_date > export_request.end_date:
            raise HTTPException(status_code=400, detail="Start date must be before end date")
        
        # Build query for forms data
        if export_request.form_ids:
            form_filter = "AND f.id = ANY(%s)"
            form_params = [export_request.form_ids]
        else:
            form_filter = ""
            form_params = []
        
        with conn.cursor() as cursor:
            # Get analytics data
            query = f"""
                SELECT 
                    f.id as form_id,
                    f.title as form_title,
                    f.status,
                    fpm.date_recorded,
                    fpm.total_views,
                    fpm.total_starts,
                    fpm.total_completions,
                    fpm.conversion_rate,
                    fpm.abandonment_rate,
                    fpm.avg_completion_time_seconds,
                    fpm.mobile_views,
                    fpm.desktop_views,
                    fpm.tablet_views
                FROM forms f
                LEFT JOIN form_performance_metrics fpm ON f.id = fpm.form_id
                    AND fpm.date_recorded BETWEEN %s AND %s
                WHERE f.client_id = %s {form_filter}
                ORDER BY f.title, fpm.date_recorded
            """
            
            params = [export_request.start_date, export_request.end_date, current_user.client_id] + form_params
            cursor.execute(query, params)
            
            analytics_data = cursor.fetchall()
            
            # Generate export based on format
            if export_request.format == "csv":
                return await generate_csv_export(analytics_data)
            elif export_request.format == "json":
                return await generate_json_export(analytics_data)
            else:
                raise HTTPException(status_code=400, detail="Unsupported export format")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to export analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to export analytics")

async def generate_csv_export(data: List) -> StreamingResponse:
    """Generate CSV export of analytics data."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    headers = [
        "Form ID", "Form Title", "Status", "Date", "Views", "Starts", 
        "Completions", "Conversion Rate", "Abandonment Rate", 
        "Avg Completion Time (s)", "Mobile Views", "Desktop Views", "Tablet Views"
    ]
    writer.writerow(headers)
    
    # Write data
    for row in data:
        writer.writerow([
            str(row[0]) if row[0] else "",
            row[1] or "",
            row[2] or "",
            row[3].isoformat() if row[3] else "",
            row[4] or 0,
            row[5] or 0,
            row[6] or 0,
            f"{float(row[7]):.2f}" if row[7] else "0.00",
            f"{float(row[8]):.2f}" if row[8] else "0.00",
            row[9] or 0,
            row[10] or 0,
            row[11] or 0,
            row[12] or 0
        ])
    
    output.seek(0)
    content = output.getvalue()
    output.close()
    
    return StreamingResponse(
        io.StringIO(content),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=analytics_export.csv"}
    )

async def generate_json_export(data: List) -> Dict[str, Any]:
    """Generate JSON export of analytics data."""
    json_data = []
    
    for row in data:
        json_data.append({
            "form_id": str(row[0]) if row[0] else None,
            "form_title": row[1],
            "status": row[2],
            "date": row[3].isoformat() if row[3] else None,
            "total_views": row[4] or 0,
            "total_starts": row[5] or 0,
            "total_completions": row[6] or 0,
            "conversion_rate": float(row[7]) if row[7] else 0.0,
            "abandonment_rate": float(row[8]) if row[8] else 0.0,
            "avg_completion_time_seconds": row[9] or 0,
            "mobile_views": row[10] or 0,
            "desktop_views": row[11] or 0,
            "tablet_views": row[12] or 0
        })
    
    return {
        "export_date": datetime.now().isoformat(),
        "total_records": len(json_data),
        "data": json_data
    }

# === ANALYTICS UTILITIES ===

@router.post("/calculate-metrics/{form_id}")
async def calculate_form_metrics(
    form_id: str,
    target_date: Optional[date] = Query(None, description="Date to calculate (default: today)"),
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Manually trigger calculation of form metrics for a specific date."""
    try:
        if not target_date:
            target_date = date.today()
        
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Verify form belongs to client
            cursor.execute(
                "SELECT id FROM forms WHERE id = %s AND client_id = %s",
                (form_id, current_user.client_id)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Form not found")
            
            # Use the calculate_daily_form_metrics function from our migration
            cursor.execute("SELECT calculate_daily_form_metrics(%s, %s)", (form_id, target_date))
            conn.commit()
            
            return create_success_response(
                message="Form metrics calculated successfully",
                data={
                    "form_id": form_id,
                    "date": target_date.isoformat()
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to calculate form metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to calculate form metrics")