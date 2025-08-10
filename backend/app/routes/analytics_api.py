"""
Analytics API - Form Performance and Event Tracking

This module provides API endpoints for:
1. Form performance metrics and analytics
2. Event tracking for user interactions
3. A/B testing metrics and management
4. Detailed form analytics for admin dashboards
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Literal
import logging
from datetime import datetime, date, timedelta
from decimal import Decimal

from app.database import get_database_connection

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/analytics", tags=["analytics"])

# === PYDANTIC MODELS FOR ANALYTICS ===

class EventTrackingRequest(BaseModel):
    """Request to track a form interaction event."""
    session_id: str
    event_type: Literal[
        'form_view', 'question_view', 'question_answer', 'form_submit', 
        'form_abandon', 'step_back', 'step_forward', 'field_focus', 'field_blur'
    ]
    event_category: Literal['interaction', 'navigation', 'completion', 'error']
    event_action: Literal['click', 'input', 'focus', 'blur', 'scroll', 'resize', 'submit']
    event_label: Optional[str] = None
    event_value: Optional[int] = None
    question_id: Optional[int] = None
    step_number: Optional[int] = None
    form_element: Optional[str] = None
    viewport_size: Optional[Dict[str, int]] = None
    device_info: Optional[Dict[str, Any]] = None
    interaction_data: Optional[Dict[str, Any]] = None
    session_duration_ms: Optional[int] = None
    step_duration_ms: Optional[int] = None
    page_load_time_ms: Optional[int] = None
    form_render_time_ms: Optional[int] = None

class FormMetrics(BaseModel):
    """Basic form performance metrics."""
    total_views: int
    unique_visitors: int
    returning_visitors: int
    total_starts: int
    total_completions: int
    completion_rate: Decimal
    avg_completion_time: int
    median_completion_time: int
    avg_questions_answered: int
    bounce_rate: Decimal
    qualified_leads: int
    unqualified_leads: int
    maybe_leads: int
    avg_lead_score: Decimal

class FormPerformanceResponse(BaseModel):
    """Comprehensive form performance data."""
    form_id: str
    metrics: FormMetrics
    step_dropout_rates: Dict[str, float]
    device_breakdown: Dict[str, int]
    traffic_sources: Dict[str, int]
    time_period: str
    start_date: date
    end_date: date

class AnalyticsTimeSeriesData(BaseModel):
    """Time series data point."""
    date: date
    value: int
    label: str

class FormAnalyticsDashboard(BaseModel):
    """Complete analytics dashboard data."""
    form_id: str
    form_title: str
    summary_metrics: FormMetrics
    performance_trend: List[AnalyticsTimeSeriesData]
    completion_funnel: List[Dict[str, Any]]
    top_exit_questions: List[Dict[str, Any]]
    device_analytics: Dict[str, int]
    traffic_analytics: Dict[str, int]
    lead_quality_breakdown: Dict[str, int]
    conversion_by_source: List[Dict[str, Any]]

class EventAnalyticsResponse(BaseModel):
    """Event analytics summary."""
    total_events: int
    events_by_type: Dict[str, int]
    events_by_category: Dict[str, int]
    events_timeline: List[AnalyticsTimeSeriesData]
    top_interactions: List[Dict[str, Any]]

# === EVENT TRACKING ENDPOINTS ===

@router.post("/events/track")
async def track_event(event: EventTrackingRequest):
    """Track a user interaction event."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Get form_id from session
            cursor.execute("SELECT form_id FROM lead_sessions WHERE session_id = %s", (event.session_id,))
            result = cursor.fetchone()
            if not result:
                logger.warning(f"Session {event.session_id} not found for event tracking")
                return {"status": "warning", "message": "Session not found"}
            
            form_id = result[0]
            
            # Insert event
            cursor.execute("""
                INSERT INTO form_analytics_events (
                    session_id, form_id, event_type, event_category, event_action,
                    event_label, event_value, question_id, step_number, form_element,
                    viewport_size, device_info, interaction_data,
                    session_duration_ms, step_duration_ms, page_load_time_ms, form_render_time_ms
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                event.session_id, form_id, event.event_type, event.event_category, event.event_action,
                event.event_label, event.event_value, event.question_id, event.step_number,
                event.form_element, 
                event.viewport_size, event.device_info, event.interaction_data,
                event.session_duration_ms, event.step_duration_ms, 
                event.page_load_time_ms, event.form_render_time_ms
            ))
            
            conn.commit()
            return {"status": "success", "message": "Event tracked successfully"}
            
    except Exception as e:
        logger.error(f"Failed to track event: {e}")
        return {"status": "error", "message": "Failed to track event"}

@router.post("/events/track/batch")
async def track_events_batch(events: List[EventTrackingRequest]):
    """Track multiple events in a batch for better performance."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Prepare batch insert data
            batch_data = []
            for event in events:
                # Get form_id from session (could be optimized with a session cache)
                cursor.execute("SELECT form_id FROM lead_sessions WHERE session_id = %s", (event.session_id,))
                result = cursor.fetchone()
                if result:
                    form_id = result[0]
                    batch_data.append((
                        event.session_id, form_id, event.event_type, event.event_category, event.event_action,
                        event.event_label, event.event_value, event.question_id, event.step_number,
                        event.form_element, event.viewport_size, event.device_info, event.interaction_data,
                        event.session_duration_ms, event.step_duration_ms, 
                        event.page_load_time_ms, event.form_render_time_ms
                    ))
            
            if batch_data:
                cursor.executemany("""
                    INSERT INTO form_analytics_events (
                        session_id, form_id, event_type, event_category, event_action,
                        event_label, event_value, question_id, step_number, form_element,
                        viewport_size, device_info, interaction_data,
                        session_duration_ms, step_duration_ms, page_load_time_ms, form_render_time_ms
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, batch_data)
                
                conn.commit()
            
            return {
                "status": "success", 
                "message": f"Tracked {len(batch_data)} events successfully",
                "processed": len(batch_data),
                "total_submitted": len(events)
            }
            
    except Exception as e:
        logger.error(f"Failed to track events batch: {e}")
        raise HTTPException(status_code=500, detail="Failed to track events")

# === FORM ANALYTICS ENDPOINTS ===

@router.get("/form/{form_id}/performance", response_model=FormPerformanceResponse)
async def get_form_performance(
    form_id: str,
    start_date: Optional[date] = Query(None, description="Start date for metrics"),
    end_date: Optional[date] = Query(None, description="End date for metrics"),
    period: Literal["daily", "weekly", "monthly"] = Query("daily", description="Aggregation period")
):
    """Get comprehensive performance metrics for a form."""
    try:
        # Set default date range if not provided
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
            
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Get aggregated metrics for the date range
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(total_views), 0) as total_views,
                    COALESCE(SUM(unique_visitors), 0) as unique_visitors,
                    COALESCE(SUM(returning_visitors), 0) as returning_visitors,
                    COALESCE(SUM(total_starts), 0) as total_starts,
                    COALESCE(SUM(total_completions), 0) as total_completions,
                    COALESCE(AVG(completion_rate), 0) as completion_rate,
                    COALESCE(AVG(avg_completion_time), 0) as avg_completion_time,
                    COALESCE(AVG(median_completion_time), 0) as median_completion_time,
                    COALESCE(AVG(avg_questions_answered), 0) as avg_questions_answered,
                    COALESCE(AVG(bounce_rate), 0) as bounce_rate,
                    COALESCE(SUM(qualified_leads), 0) as qualified_leads,
                    COALESCE(SUM(unqualified_leads), 0) as unqualified_leads,
                    COALESCE(SUM(maybe_leads), 0) as maybe_leads,
                    COALESCE(AVG(avg_lead_score), 0) as avg_lead_score,
                    COALESCE(AVG(step_dropout_rates), '{}') as step_dropout_rates,
                    COALESCE(AVG(device_breakdown), '{}') as device_breakdown,
                    COALESCE(AVG(traffic_sources), '{}') as traffic_sources
                FROM form_performance_metrics
                WHERE form_id = %s 
                AND metric_date BETWEEN %s AND %s
                AND metric_period = %s
            """, (form_id, start_date, end_date, period))
            
            result = cursor.fetchone()
            if not result or result[0] == 0:  # No data found
                # Return empty metrics structure
                empty_metrics = FormMetrics(
                    total_views=0, unique_visitors=0, returning_visitors=0,
                    total_starts=0, total_completions=0, completion_rate=Decimal('0.00'),
                    avg_completion_time=0, median_completion_time=0,
                    avg_questions_answered=0, bounce_rate=Decimal('0.00'),
                    qualified_leads=0, unqualified_leads=0, maybe_leads=0,
                    avg_lead_score=Decimal('0.00')
                )
                
                return FormPerformanceResponse(
                    form_id=form_id,
                    metrics=empty_metrics,
                    step_dropout_rates={},
                    device_breakdown={},
                    traffic_sources={},
                    time_period=period,
                    start_date=start_date,
                    end_date=end_date
                )
            
            metrics = FormMetrics(
                total_views=int(result[0]),
                unique_visitors=int(result[1]),
                returning_visitors=int(result[2]),
                total_starts=int(result[3]),
                total_completions=int(result[4]),
                completion_rate=Decimal(str(result[5])),
                avg_completion_time=int(result[6]),
                median_completion_time=int(result[7]),
                avg_questions_answered=int(result[8]),
                bounce_rate=Decimal(str(result[9])),
                qualified_leads=int(result[10]),
                unqualified_leads=int(result[11]),
                maybe_leads=int(result[12]),
                avg_lead_score=Decimal(str(result[13]))
            )
            
            return FormPerformanceResponse(
                form_id=form_id,
                metrics=metrics,
                step_dropout_rates=result[14] or {},
                device_breakdown=result[15] or {},
                traffic_sources=result[16] or {},
                time_period=period,
                start_date=start_date,
                end_date=end_date
            )
            
    except Exception as e:
        logger.error(f"Failed to get form performance: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve form performance")

@router.get("/form/{form_id}/dashboard", response_model=FormAnalyticsDashboard)
async def get_form_analytics_dashboard(
    form_id: str,
    days: int = Query(30, description="Number of days for analytics data")
):
    """Get comprehensive analytics dashboard data for a form."""
    try:
        start_date = date.today() - timedelta(days=days)
        end_date = date.today()
        
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Get form title
            cursor.execute("SELECT title FROM forms WHERE id = %s", (form_id,))
            form_result = cursor.fetchone()
            if not form_result:
                raise HTTPException(status_code=404, detail="Form not found")
            form_title = form_result[0]
            
            # Get summary metrics (reuse the performance endpoint logic)
            performance_data = await get_form_performance(form_id, start_date, end_date, "daily")
            
            # Get performance trend
            cursor.execute("""
                SELECT metric_date, total_completions
                FROM form_performance_metrics
                WHERE form_id = %s AND metric_date BETWEEN %s AND %s
                ORDER BY metric_date
            """, (form_id, start_date, end_date))
            
            trend_data = [
                AnalyticsTimeSeriesData(
                    date=row[0], 
                    value=row[1], 
                    label="Completions"
                ) for row in cursor.fetchall()
            ]
            
            # Get completion funnel (step-by-step completion rates)
            cursor.execute("""
                SELECT 
                    step,
                    COUNT(*) as reached_step,
                    COUNT(CASE WHEN completed = true THEN 1 END) as completed_from_step
                FROM lead_sessions
                WHERE form_id = %s AND started_at::date BETWEEN %s AND %s
                GROUP BY step
                ORDER BY step
            """, (form_id, start_date, end_date))
            
            funnel_data = [
                {
                    "step": row[0],
                    "reached": row[1],
                    "completed": row[2],
                    "completion_rate": (row[2] / row[1] * 100) if row[1] > 0 else 0
                } for row in cursor.fetchall()
            ]
            
            # Get top exit questions (questions where users most commonly abandon)
            cursor.execute("""
                SELECT 
                    r.question_id,
                    r.question_text,
                    COUNT(*) as abandonment_count,
                    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as abandonment_percentage
                FROM responses r
                JOIN lead_sessions ls ON r.session_id = ls.session_id
                WHERE ls.form_id = %s 
                AND ls.completed = false 
                AND ls.abandonment_status = 'abandoned'
                AND r.submitted_at::date BETWEEN %s AND %s
                GROUP BY r.question_id, r.question_text
                ORDER BY abandonment_count DESC
                LIMIT 5
            """, (form_id, start_date, end_date))
            
            exit_questions = [
                {
                    "question_id": row[0],
                    "question_text": row[1],
                    "abandonment_count": row[2],
                    "abandonment_percentage": float(row[3])
                } for row in cursor.fetchall()
            ]
            
            # Get conversion by traffic source
            cursor.execute("""
                SELECT 
                    COALESCE(td.utm_source, 'direct') as source,
                    COUNT(DISTINCT ls.session_id) as total_sessions,
                    COUNT(CASE WHEN ls.lead_status = 'yes' THEN 1 END) as conversions,
                    ROUND(
                        COUNT(CASE WHEN ls.lead_status = 'yes' THEN 1 END) * 100.0 / 
                        COUNT(DISTINCT ls.session_id), 2
                    ) as conversion_rate
                FROM lead_sessions ls
                LEFT JOIN tracking_data td ON ls.session_id = td.session_id
                WHERE ls.form_id = %s AND ls.started_at::date BETWEEN %s AND %s
                GROUP BY COALESCE(td.utm_source, 'direct')
                ORDER BY total_sessions DESC
            """, (form_id, start_date, end_date))
            
            conversion_by_source = [
                {
                    "source": row[0],
                    "total_sessions": row[1],
                    "conversions": row[2],
                    "conversion_rate": float(row[3])
                } for row in cursor.fetchall()
            ]
            
            # Lead quality breakdown
            lead_quality = {
                "qualified": performance_data.metrics.qualified_leads,
                "maybe": performance_data.metrics.maybe_leads,
                "unqualified": performance_data.metrics.unqualified_leads
            }
            
            return FormAnalyticsDashboard(
                form_id=form_id,
                form_title=form_title,
                summary_metrics=performance_data.metrics,
                performance_trend=trend_data,
                completion_funnel=funnel_data,
                top_exit_questions=exit_questions,
                device_analytics=performance_data.device_breakdown,
                traffic_analytics=performance_data.traffic_sources,
                lead_quality_breakdown=lead_quality,
                conversion_by_source=conversion_by_source
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get dashboard data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve dashboard data")

@router.get("/form/{form_id}/events", response_model=EventAnalyticsResponse)
async def get_form_events_analytics(
    form_id: str,
    days: int = Query(7, description="Number of days for event data"),
    event_type: Optional[str] = Query(None, description="Filter by event type")
):
    """Get event analytics for a form."""
    try:
        start_date = datetime.now() - timedelta(days=days)
        
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # Base query conditions
            where_conditions = ["form_id = %s", "event_timestamp >= %s"]
            query_params = [form_id, start_date]
            
            if event_type:
                where_conditions.append("event_type = %s")
                query_params.append(event_type)
            
            where_clause = " AND ".join(where_conditions)
            
            # Get total event count
            cursor.execute(f"SELECT COUNT(*) FROM form_analytics_events WHERE {where_clause}", query_params)
            total_events = cursor.fetchone()[0]
            
            # Get events by type
            cursor.execute(f"""
                SELECT event_type, COUNT(*) 
                FROM form_analytics_events 
                WHERE {where_clause}
                GROUP BY event_type
                ORDER BY COUNT(*) DESC
            """, query_params)
            events_by_type = dict(cursor.fetchall())
            
            # Get events by category
            cursor.execute(f"""
                SELECT event_category, COUNT(*) 
                FROM form_analytics_events 
                WHERE {where_clause}
                GROUP BY event_category
                ORDER BY COUNT(*) DESC
            """, query_params)
            events_by_category = dict(cursor.fetchall())
            
            # Get events timeline (daily)
            cursor.execute(f"""
                SELECT 
                    event_timestamp::date as event_date,
                    COUNT(*) as event_count
                FROM form_analytics_events 
                WHERE {where_clause}
                GROUP BY event_timestamp::date
                ORDER BY event_date
            """, query_params)
            
            events_timeline = [
                AnalyticsTimeSeriesData(
                    date=row[0],
                    value=row[1],
                    label="Events"
                ) for row in cursor.fetchall()
            ]
            
            # Get top interactions
            cursor.execute(f"""
                SELECT 
                    event_action,
                    form_element,
                    COUNT(*) as interaction_count
                FROM form_analytics_events 
                WHERE {where_clause} AND form_element IS NOT NULL
                GROUP BY event_action, form_element
                ORDER BY COUNT(*) DESC
                LIMIT 10
            """, query_params)
            
            top_interactions = [
                {
                    "action": row[0],
                    "element": row[1],
                    "count": row[2]
                } for row in cursor.fetchall()
            ]
            
            return EventAnalyticsResponse(
                total_events=total_events,
                events_by_type=events_by_type,
                events_by_category=events_by_category,
                events_timeline=events_timeline,
                top_interactions=top_interactions
            )
            
    except Exception as e:
        logger.error(f"Failed to get event analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve event analytics")

# === ANALYTICS UTILITIES ===

@router.post("/form/{form_id}/performance/recalculate")
async def recalculate_form_metrics(form_id: str):
    """Manually trigger recalculation of form performance metrics."""
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            # This would typically be handled by a background job
            # For now, we'll calculate today's metrics
            today = date.today()
            
            cursor.execute("""
                INSERT INTO form_performance_metrics (
                    form_id, metric_date, metric_period,
                    total_views, unique_visitors, total_starts, total_completions,
                    completion_rate, qualified_leads, unqualified_leads, maybe_leads
                )
                SELECT 
                    %s,
                    %s,
                    'daily',
                    COUNT(*) as total_views,
                    COUNT(DISTINCT session_id) as unique_visitors,
                    COUNT(*) as total_starts,
                    COUNT(CASE WHEN completed = true THEN 1 END) as total_completions,
                    CASE 
                        WHEN COUNT(*) > 0 
                        THEN ROUND(COUNT(CASE WHEN completed = true THEN 1 END) * 100.0 / COUNT(*), 2)
                        ELSE 0 
                    END as completion_rate,
                    COUNT(CASE WHEN lead_status = 'yes' THEN 1 END) as qualified_leads,
                    COUNT(CASE WHEN lead_status = 'no' THEN 1 END) as unqualified_leads,
                    COUNT(CASE WHEN lead_status = 'maybe' THEN 1 END) as maybe_leads
                FROM lead_sessions
                WHERE form_id = %s AND started_at::date = %s
                ON CONFLICT (form_id, metric_date, metric_period) 
                DO UPDATE SET
                    total_views = EXCLUDED.total_views,
                    unique_visitors = EXCLUDED.unique_visitors,
                    total_starts = EXCLUDED.total_starts,
                    total_completions = EXCLUDED.total_completions,
                    completion_rate = EXCLUDED.completion_rate,
                    qualified_leads = EXCLUDED.qualified_leads,
                    unqualified_leads = EXCLUDED.unqualified_leads,
                    maybe_leads = EXCLUDED.maybe_leads,
                    updated_at = NOW()
            """, (form_id, today, form_id, today))
            
            conn.commit()
            return {"status": "success", "message": "Metrics recalculated successfully"}
            
    except Exception as e:
        logger.error(f"Failed to recalculate metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to recalculate metrics")