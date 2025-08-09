"""
Analytics Queries for Survey System

Provides SQL queries and Python helpers for tracking:
- Conversion rates by UTM source/campaign
- Abandonment rates by step and form
- Lead quality metrics
- Performance analytics
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ConversionMetrics:
    """Metrics for conversion analysis"""
    utm_source: str
    utm_campaign: str
    total_sessions: int
    completed_sessions: int
    qualified_leads: int
    conversion_rate: float
    qualification_rate: float
    avg_completion_time_minutes: float

@dataclass
class AbandonmentMetrics:
    """Metrics for abandonment analysis"""
    form_id: str
    step_number: int
    total_sessions: int
    abandoned_sessions: int
    abandonment_rate: float
    avg_time_to_abandon_minutes: float

@dataclass
class PerformanceMetrics:
    """Performance metrics for monitoring"""
    metric_name: str
    avg_value: float
    max_value: float
    min_value: float
    sample_count: int
    threshold_exceeded: int

class SurveyAnalytics:
    """Analytics query builder and executor for survey system"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    # Conversion Rate Queries
    
    def get_conversion_by_utm_source(
        self,
        days_back: int = 30,
        utm_sources: Optional[List[str]] = None
    ) -> List[ConversionMetrics]:
        """Get conversion metrics broken down by UTM source"""
        
        source_filter = ""
        if utm_sources:
            sources_str = "', '".join(utm_sources)
            source_filter = f"AND t.utm_source IN ('{sources_str}')"
        
        query = f"""
        WITH session_metrics AS (
            SELECT 
                COALESCE(t.utm_source, 'direct') as utm_source,
                COALESCE(t.utm_campaign, 'none') as utm_campaign,
                ls.session_id,
                ls.completed,
                ls.lead_status,
                ls.started_at,
                ls.completed_at,
                CASE 
                    WHEN ls.completed_at IS NOT NULL AND ls.started_at IS NOT NULL
                    THEN EXTRACT(EPOCH FROM (ls.completed_at - ls.started_at)) / 60.0
                    ELSE NULL 
                END as completion_time_minutes
            FROM lead_sessions ls
            LEFT JOIN tracking_data t ON ls.session_id = t.session_id
            WHERE ls.started_at >= NOW() - INTERVAL '{days_back} days'
            {source_filter}
        )
        SELECT 
            utm_source,
            utm_campaign,
            COUNT(*) as total_sessions,
            SUM(CASE WHEN completed THEN 1 ELSE 0 END) as completed_sessions,
            SUM(CASE WHEN lead_status IN ('yes', 'maybe') THEN 1 ELSE 0 END) as qualified_leads,
            ROUND(
                (SUM(CASE WHEN completed THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 
                2
            ) as conversion_rate,
            ROUND(
                (SUM(CASE WHEN lead_status IN ('yes', 'maybe') THEN 1 ELSE 0 END) * 100.0) / 
                GREATEST(SUM(CASE WHEN completed THEN 1 ELSE 0 END), 1), 
                2
            ) as qualification_rate,
            ROUND(AVG(completion_time_minutes), 2) as avg_completion_time_minutes
        FROM session_metrics
        GROUP BY utm_source, utm_campaign
        ORDER BY total_sessions DESC, conversion_rate DESC
        """
        
        try:
            results = self.db.execute_query(query)
            return [
                ConversionMetrics(
                    utm_source=row[0],
                    utm_campaign=row[1], 
                    total_sessions=row[2],
                    completed_sessions=row[3],
                    qualified_leads=row[4],
                    conversion_rate=row[5],
                    qualification_rate=row[6],
                    avg_completion_time_minutes=row[7] or 0.0
                )
                for row in results
            ]
        except Exception as e:
            logger.error(f"Failed to get conversion metrics: {e}")
            return []
    
    def get_abandonment_by_step(
        self,
        form_id: Optional[str] = None,
        days_back: int = 30
    ) -> List[AbandonmentMetrics]:
        """Get abandonment rates by step number"""
        
        form_filter = ""
        if form_id:
            form_filter = f"AND ls.form_id = '{form_id}'"
        
        query = f"""
        WITH step_analysis AS (
            SELECT 
                ls.form_id,
                ls.current_step as step_number,
                ls.session_id,
                ls.completed,
                ls.abandonment_status,
                ls.started_at,
                CASE 
                    WHEN ls.abandonment_status = 'abandoned' AND ls.completed_at IS NOT NULL
                    THEN EXTRACT(EPOCH FROM (ls.completed_at - ls.started_at)) / 60.0
                    ELSE NULL
                END as time_to_abandon_minutes
            FROM lead_sessions ls
            WHERE ls.started_at >= NOW() - INTERVAL '{days_back} days'
            {form_filter}
        )
        SELECT 
            form_id,
            step_number,
            COUNT(*) as total_sessions,
            SUM(CASE WHEN abandonment_status = 'abandoned' THEN 1 ELSE 0 END) as abandoned_sessions,
            ROUND(
                (SUM(CASE WHEN abandonment_status = 'abandoned' THEN 1 ELSE 0 END) * 100.0) / COUNT(*),
                2
            ) as abandonment_rate,
            ROUND(AVG(time_to_abandon_minutes), 2) as avg_time_to_abandon_minutes
        FROM step_analysis
        WHERE step_number > 0
        GROUP BY form_id, step_number
        ORDER BY form_id, step_number
        """
        
        try:
            results = self.db.execute_query(query)
            return [
                AbandonmentMetrics(
                    form_id=row[0],
                    step_number=row[1],
                    total_sessions=row[2],
                    abandoned_sessions=row[3],
                    abandonment_rate=row[4],
                    avg_time_to_abandon_minutes=row[5] or 0.0
                )
                for row in results
            ]
        except Exception as e:
            logger.error(f"Failed to get abandonment metrics: {e}")
            return []
    
    def get_campaign_performance(
        self,
        days_back: int = 30,
        min_sessions: int = 10
    ) -> List[Dict[str, Any]]:
        """Get performance metrics by campaign with statistical significance"""
        
        query = f"""
        WITH campaign_stats AS (
            SELECT 
                COALESCE(t.utm_campaign, 'none') as campaign,
                COALESCE(t.utm_source, 'direct') as source,
                COALESCE(t.utm_medium, 'none') as medium,
                COUNT(*) as total_sessions,
                SUM(CASE WHEN ls.completed THEN 1 ELSE 0 END) as completed_sessions,
                SUM(CASE WHEN ls.lead_status = 'yes' THEN 1 ELSE 0 END) as qualified_leads,
                SUM(CASE WHEN ls.lead_status = 'maybe' THEN 1 ELSE 0 END) as maybe_leads,
                AVG(CASE WHEN ls.completed THEN ls.final_score ELSE NULL END) as avg_final_score,
                AVG(CASE 
                    WHEN ls.completed_at IS NOT NULL AND ls.started_at IS NOT NULL
                    THEN EXTRACT(EPOCH FROM (ls.completed_at - ls.started_at)) / 60.0
                    ELSE NULL 
                END) as avg_session_duration_minutes,
                MIN(ls.started_at) as first_session,
                MAX(ls.started_at) as last_session
            FROM lead_sessions ls
            LEFT JOIN tracking_data t ON ls.session_id = t.session_id
            WHERE ls.started_at >= NOW() - INTERVAL '{days_back} days'
            GROUP BY t.utm_campaign, t.utm_source, t.utm_medium
            HAVING COUNT(*) >= {min_sessions}
        )
        SELECT 
            campaign,
            source,
            medium,
            total_sessions,
            completed_sessions,
            qualified_leads,
            maybe_leads,
            ROUND((completed_sessions * 100.0) / total_sessions, 2) as conversion_rate,
            ROUND((qualified_leads * 100.0) / GREATEST(completed_sessions, 1), 2) as qualification_rate,
            ROUND(((qualified_leads + maybe_leads) * 100.0) / GREATEST(completed_sessions, 1), 2) as potential_rate,
            ROUND(avg_final_score, 2) as avg_final_score,
            ROUND(avg_session_duration_minutes, 2) as avg_duration_minutes,
            first_session,
            last_session,
            EXTRACT(DAYS FROM (last_session - first_session)) as campaign_duration_days
        FROM campaign_stats
        ORDER BY total_sessions DESC, conversion_rate DESC
        """
        
        try:
            results = self.db.execute_query(query)
            return [
                {
                    "campaign": row[0],
                    "source": row[1], 
                    "medium": row[2],
                    "total_sessions": row[3],
                    "completed_sessions": row[4],
                    "qualified_leads": row[5],
                    "maybe_leads": row[6],
                    "conversion_rate": row[7],
                    "qualification_rate": row[8],
                    "potential_rate": row[9],
                    "avg_final_score": row[10],
                    "avg_duration_minutes": row[11],
                    "first_session": row[12],
                    "last_session": row[13],
                    "campaign_duration_days": row[14]
                }
                for row in results
            ]
        except Exception as e:
            logger.error(f"Failed to get campaign performance: {e}")
            return []
    
    # Performance Monitoring Queries
    
    def get_daily_performance_summary(
        self,
        days_back: int = 7
    ) -> List[Dict[str, Any]]:
        """Get daily performance summary for dashboard"""
        
        query = f"""
        WITH daily_stats AS (
            SELECT 
                DATE(ls.started_at) as session_date,
                COUNT(*) as total_sessions,
                SUM(CASE WHEN ls.completed THEN 1 ELSE 0 END) as completed_sessions,
                SUM(CASE WHEN ls.lead_status = 'yes' THEN 1 ELSE 0 END) as qualified_leads,
                SUM(CASE WHEN ls.abandonment_status = 'abandoned' THEN 1 ELSE 0 END) as abandoned_sessions,
                AVG(CASE 
                    WHEN ls.completed_at IS NOT NULL AND ls.started_at IS NOT NULL
                    THEN EXTRACT(EPOCH FROM (ls.completed_at - ls.started_at)) / 60.0
                    ELSE NULL 
                END) as avg_completion_time,
                AVG(ls.current_step) as avg_steps_reached,
                COUNT(DISTINCT ls.form_id) as active_forms
            FROM lead_sessions ls
            WHERE ls.started_at >= NOW() - INTERVAL '{days_back} days'
            GROUP BY DATE(ls.started_at)
        )
        SELECT 
            session_date,
            total_sessions,
            completed_sessions,
            qualified_leads,
            abandoned_sessions,
            ROUND((completed_sessions * 100.0) / total_sessions, 2) as conversion_rate,
            ROUND((qualified_leads * 100.0) / GREATEST(completed_sessions, 1), 2) as qualification_rate,
            ROUND((abandoned_sessions * 100.0) / total_sessions, 2) as abandonment_rate,
            ROUND(avg_completion_time, 2) as avg_completion_minutes,
            ROUND(avg_steps_reached, 1) as avg_steps_reached,
            active_forms
        FROM daily_stats
        ORDER BY session_date DESC
        """
        
        try:
            results = self.db.execute_query(query)
            return [
                {
                    "date": row[0].strftime("%Y-%m-%d"),
                    "total_sessions": row[1],
                    "completed_sessions": row[2],
                    "qualified_leads": row[3],
                    "abandoned_sessions": row[4],
                    "conversion_rate": row[5],
                    "qualification_rate": row[6], 
                    "abandonment_rate": row[7],
                    "avg_completion_minutes": row[8],
                    "avg_steps_reached": row[9],
                    "active_forms": row[10]
                }
                for row in results
            ]
        except Exception as e:
            logger.error(f"Failed to get daily performance summary: {e}")
            return []
    
    # Alert Queries
    
    def check_abandonment_alerts(
        self,
        abandonment_threshold: float = 50.0,
        min_sessions: int = 20,
        hours_back: int = 24
    ) -> List[Dict[str, Any]]:
        """Check for high abandonment rates that require alerting"""
        
        query = f"""
        WITH recent_abandonment AS (
            SELECT 
                ls.form_id,
                COUNT(*) as total_sessions,
                SUM(CASE WHEN ls.abandonment_status = 'abandoned' THEN 1 ELSE 0 END) as abandoned_sessions,
                ROUND(
                    (SUM(CASE WHEN ls.abandonment_status = 'abandoned' THEN 1 ELSE 0 END) * 100.0) / COUNT(*),
                    2
                ) as abandonment_rate
            FROM lead_sessions ls
            WHERE ls.started_at >= NOW() - INTERVAL '{hours_back} hours'
            GROUP BY ls.form_id
            HAVING COUNT(*) >= {min_sessions}
        )
        SELECT 
            form_id,
            total_sessions,
            abandoned_sessions,
            abandonment_rate
        FROM recent_abandonment
        WHERE abandonment_rate > {abandonment_threshold}
        ORDER BY abandonment_rate DESC
        """
        
        try:
            results = self.db.execute_query(query)
            alerts = []
            
            for row in results:
                alert = {
                    "form_id": row[0],
                    "total_sessions": row[1],
                    "abandoned_sessions": row[2],
                    "abandonment_rate": row[3],
                    "alert_type": "high_abandonment",
                    "severity": "high" if row[3] > 75 else "medium",
                    "timestamp": datetime.utcnow().isoformat()
                }
                alerts.append(alert)
                
                # Log the alert
                logger.warning(
                    f"High abandonment rate alert: Form {row[0]} has {row[3]}% abandonment rate "
                    f"({row[2]}/{row[1]} sessions in last {hours_back} hours)"
                )
            
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to check abandonment alerts: {e}")
            return []
    
    def check_performance_alerts(
        self,
        slow_completion_threshold_minutes: float = 10.0,
        min_sessions: int = 10,
        hours_back: int = 6
    ) -> List[Dict[str, Any]]:
        """Check for performance issues requiring alerts"""
        
        query = f"""
        WITH recent_performance AS (
            SELECT 
                ls.form_id,
                COUNT(*) as completed_sessions,
                AVG(EXTRACT(EPOCH FROM (ls.completed_at - ls.started_at)) / 60.0) as avg_completion_minutes,
                MAX(EXTRACT(EPOCH FROM (ls.completed_at - ls.started_at)) / 60.0) as max_completion_minutes
            FROM lead_sessions ls
            WHERE ls.completed = true 
            AND ls.started_at >= NOW() - INTERVAL '{hours_back} hours'
            AND ls.completed_at IS NOT NULL
            GROUP BY ls.form_id
            HAVING COUNT(*) >= {min_sessions}
        )
        SELECT 
            form_id,
            completed_sessions,
            ROUND(avg_completion_minutes, 2) as avg_completion_minutes,
            ROUND(max_completion_minutes, 2) as max_completion_minutes
        FROM recent_performance
        WHERE avg_completion_minutes > {slow_completion_threshold_minutes}
        ORDER BY avg_completion_minutes DESC
        """
        
        try:
            results = self.db.execute_query(query)
            alerts = []
            
            for row in results:
                alert = {
                    "form_id": row[0],
                    "completed_sessions": row[1],
                    "avg_completion_minutes": row[2],
                    "max_completion_minutes": row[3],
                    "alert_type": "slow_completion",
                    "severity": "high" if row[2] > 15 else "medium",
                    "timestamp": datetime.utcnow().isoformat()
                }
                alerts.append(alert)
                
                logger.warning(
                    f"Slow completion alert: Form {row[0]} average completion time "
                    f"{row[2]} minutes (max: {row[3]} minutes) in last {hours_back} hours"
                )
            
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to check performance alerts: {e}")
            return []
    
    # Utility Methods
    
    def get_form_health_summary(self, form_id: str, days_back: int = 7) -> Dict[str, Any]:
        """Get comprehensive health summary for a specific form"""
        
        conversion_metrics = self.get_conversion_by_utm_source(days_back=days_back)
        form_conversions = [m for m in conversion_metrics if form_id in str(m)]
        
        abandonment_metrics = self.get_abandonment_by_step(form_id=form_id, days_back=days_back)
        
        # Get basic stats
        basic_query = f"""
        SELECT 
            COUNT(*) as total_sessions,
            SUM(CASE WHEN completed THEN 1 ELSE 0 END) as completed_sessions,
            SUM(CASE WHEN lead_status = 'yes' THEN 1 ELSE 0 END) as qualified_leads,
            AVG(final_score) as avg_score,
            MAX(current_step) as max_steps
        FROM lead_sessions
        WHERE form_id = '{form_id}' 
        AND started_at >= NOW() - INTERVAL '{days_back} days'
        """
        
        try:
            result = self.db.execute_query(basic_query)[0]
            
            return {
                "form_id": form_id,
                "period_days": days_back,
                "total_sessions": result[0] or 0,
                "completed_sessions": result[1] or 0,
                "qualified_leads": result[2] or 0,
                "conversion_rate": round((result[1] or 0) * 100.0 / max(result[0] or 1, 1), 2),
                "qualification_rate": round((result[2] or 0) * 100.0 / max(result[1] or 1, 1), 2),
                "avg_score": round(result[3] or 0, 2),
                "max_steps": result[4] or 0,
                "abandonment_by_step": [
                    {
                        "step": a.step_number,
                        "abandonment_rate": a.abandonment_rate,
                        "sessions": a.total_sessions
                    }
                    for a in abandonment_metrics
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to get form health summary for {form_id}: {e}")
            return {"form_id": form_id, "error": str(e)}

# Analytics helper functions

def create_analytics_dashboard_data(analytics: SurveyAnalytics, days_back: int = 7) -> Dict[str, Any]:
    """Create dashboard data structure for frontend consumption"""
    
    return {
        "overview": analytics.get_daily_performance_summary(days_back),
        "conversions": analytics.get_conversion_by_utm_source(days_back),
        "campaigns": analytics.get_campaign_performance(days_back),
        "abandonment_alerts": analytics.check_abandonment_alerts(),
        "performance_alerts": analytics.check_performance_alerts(),
        "generated_at": datetime.utcnow().isoformat(),
        "period_days": days_back
    }

# Export main components
__all__ = [
    'SurveyAnalytics',
    'ConversionMetrics',
    'AbandonmentMetrics',
    'PerformanceMetrics',
    'create_analytics_dashboard_data'
]