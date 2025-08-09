"""
Database Performance Monitoring

Monitors database query performance, connection health, and provides
optimization insights for the survey system.
"""

import time
import logging
from typing import Dict, List, Optional, Any, Callable
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import wraps
import threading
import statistics

logger = logging.getLogger(__name__)

@dataclass
class QueryMetrics:
    """Metrics for individual database queries"""
    query_hash: str
    query_type: str  # SELECT, INSERT, UPDATE, DELETE
    table_name: Optional[str]
    duration_ms: float
    timestamp: datetime
    success: bool
    error_message: Optional[str] = None
    row_count: Optional[int] = None

@dataclass 
class ConnectionMetrics:
    """Database connection pool metrics"""
    active_connections: int
    idle_connections: int
    total_connections: int
    failed_connections: int
    avg_connection_time_ms: float
    timestamp: datetime

@dataclass
class SlowQueryAlert:
    """Alert for slow database queries"""
    query_hash: str
    query_type: str
    table_name: Optional[str]
    duration_ms: float
    threshold_ms: float
    timestamp: datetime
    frequency_1h: int  # How many times in last hour
    avg_duration_1h: float

class DatabaseMonitor:
    """Database performance monitoring and alerting"""
    
    def __init__(
        self,
        slow_query_threshold_ms: float = 1000.0,
        connection_timeout_threshold_ms: float = 5000.0,
        max_metrics_history: int = 1000
    ):
        self.slow_query_threshold_ms = slow_query_threshold_ms
        self.connection_timeout_threshold_ms = connection_timeout_threshold_ms
        self.max_metrics_history = max_metrics_history
        
        # Thread-safe storage
        self._lock = threading.Lock()
        self._query_metrics: List[QueryMetrics] = []
        self._connection_metrics: List[ConnectionMetrics] = []
        self._slow_query_counts: Dict[str, List[datetime]] = {}
        
        # Performance statistics cache
        self._stats_cache: Dict[str, Any] = {}
        self._cache_timestamp = datetime.min
        self._cache_ttl_seconds = 60  # 1 minute cache
    
    def log_query(
        self,
        query_hash: str,
        query_type: str,
        table_name: Optional[str],
        duration_ms: float,
        success: bool,
        error_message: Optional[str] = None,
        row_count: Optional[int] = None
    ):
        """Log query execution metrics"""
        
        metric = QueryMetrics(
            query_hash=query_hash,
            query_type=query_type,
            table_name=table_name,
            duration_ms=duration_ms,
            timestamp=datetime.utcnow(),
            success=success,
            error_message=error_message,
            row_count=row_count
        )
        
        with self._lock:
            self._query_metrics.append(metric)
            
            # Keep only recent metrics
            if len(self._query_metrics) > self.max_metrics_history:
                self._query_metrics = self._query_metrics[-self.max_metrics_history:]
        
        # Check for slow queries
        if duration_ms > self.slow_query_threshold_ms:
            self._handle_slow_query(metric)
        
        # Log structured message
        logger.info(
            f"Database query: {query_type} on {table_name or 'unknown'} - {duration_ms:.2f}ms",
            extra={
                "event_type": "database_query",
                "query_type": query_type,
                "table_name": table_name,
                "duration_ms": duration_ms,
                "success": success,
                "query_hash": query_hash[:16],  # First 16 chars for correlation
                "row_count": row_count,
                "error": error_message
            }
        )
    
    def log_connection(
        self,
        active: int,
        idle: int,
        total: int,
        failed: int,
        connection_time_ms: float
    ):
        """Log connection pool metrics"""
        
        metric = ConnectionMetrics(
            active_connections=active,
            idle_connections=idle,
            total_connections=total,
            failed_connections=failed,
            avg_connection_time_ms=connection_time_ms,
            timestamp=datetime.utcnow()
        )
        
        with self._lock:
            self._connection_metrics.append(metric)
            
            # Keep only recent metrics
            if len(self._connection_metrics) > self.max_metrics_history:
                self._connection_metrics = self._connection_metrics[-self.max_metrics_history:]
        
        # Check for connection issues
        if connection_time_ms > self.connection_timeout_threshold_ms:
            logger.warning(
                f"Slow database connection: {connection_time_ms:.2f}ms",
                extra={
                    "event_type": "slow_connection",
                    "connection_time_ms": connection_time_ms,
                    "threshold_ms": self.connection_timeout_threshold_ms,
                    "active_connections": active,
                    "total_connections": total
                }
            )
    
    def _handle_slow_query(self, metric: QueryMetrics):
        """Handle slow query detection and alerting"""
        
        query_key = f"{metric.query_type}_{metric.table_name}_{metric.query_hash[:8]}"
        now = datetime.utcnow()
        
        # Track slow query frequency
        with self._lock:
            if query_key not in self._slow_query_counts:
                self._slow_query_counts[query_key] = []
            
            self._slow_query_counts[query_key].append(now)
            
            # Remove old entries (older than 1 hour)
            hour_ago = now - timedelta(hours=1)
            self._slow_query_counts[query_key] = [
                ts for ts in self._slow_query_counts[query_key]
                if ts > hour_ago
            ]
            
            frequency_1h = len(self._slow_query_counts[query_key])
        
        # Calculate average duration for this query in last hour
        recent_metrics = [
            m for m in self._query_metrics[-100:]  # Last 100 queries
            if m.query_hash == metric.query_hash
            and m.timestamp > hour_ago
        ]
        
        avg_duration_1h = statistics.mean([m.duration_ms for m in recent_metrics]) if recent_metrics else metric.duration_ms
        
        # Create alert
        alert = SlowQueryAlert(
            query_hash=metric.query_hash,
            query_type=metric.query_type,
            table_name=metric.table_name,
            duration_ms=metric.duration_ms,
            threshold_ms=self.slow_query_threshold_ms,
            timestamp=now,
            frequency_1h=frequency_1h,
            avg_duration_1h=avg_duration_1h
        )
        
        # Log slow query alert
        severity = "high" if frequency_1h >= 10 or metric.duration_ms > 5000 else "medium"
        
        logger.warning(
            f"Slow query detected: {metric.query_type} on {metric.table_name} - "
            f"{metric.duration_ms:.2f}ms (avg: {avg_duration_1h:.2f}ms, frequency: {frequency_1h}/hour)",
            extra={
                "event_type": "slow_query_alert",
                "query_type": metric.query_type,
                "table_name": metric.table_name,
                "duration_ms": metric.duration_ms,
                "threshold_ms": self.slow_query_threshold_ms,
                "frequency_1h": frequency_1h,
                "avg_duration_1h": avg_duration_1h,
                "severity": severity,
                "query_hash": metric.query_hash[:16]
            }
        )
    
    def get_performance_summary(self, minutes_back: int = 60) -> Dict[str, Any]:
        """Get performance summary for the specified time window"""
        
        # Check cache
        now = datetime.utcnow()
        if (now - self._cache_timestamp).seconds < self._cache_ttl_seconds and self._stats_cache:
            return self._stats_cache
        
        cutoff_time = now - timedelta(minutes=minutes_back)
        
        with self._lock:
            recent_queries = [m for m in self._query_metrics if m.timestamp > cutoff_time]
            recent_connections = [m for m in self._connection_metrics if m.timestamp > cutoff_time]
        
        if not recent_queries:
            return {"error": "No recent query data available"}
        
        # Query statistics
        successful_queries = [m for m in recent_queries if m.success]
        failed_queries = [m for m in recent_queries if not m.success]
        
        query_durations = [m.duration_ms for m in successful_queries]
        
        # Query type breakdown
        query_types = {}
        for metric in recent_queries:
            query_types[metric.query_type] = query_types.get(metric.query_type, 0) + 1
        
        # Table access patterns
        table_access = {}
        for metric in recent_queries:
            if metric.table_name:
                table_access[metric.table_name] = table_access.get(metric.table_name, 0) + 1
        
        # Slow queries
        slow_queries = [m for m in recent_queries if m.duration_ms > self.slow_query_threshold_ms]
        
        summary = {
            "period_minutes": minutes_back,
            "timestamp": now.isoformat(),
            "query_stats": {
                "total_queries": len(recent_queries),
                "successful_queries": len(successful_queries),
                "failed_queries": len(failed_queries),
                "success_rate": round(len(successful_queries) / len(recent_queries) * 100, 2) if recent_queries else 0,
                "avg_duration_ms": round(statistics.mean(query_durations), 2) if query_durations else 0,
                "median_duration_ms": round(statistics.median(query_durations), 2) if query_durations else 0,
                "max_duration_ms": round(max(query_durations), 2) if query_durations else 0,
                "min_duration_ms": round(min(query_durations), 2) if query_durations else 0
            },
            "query_types": query_types,
            "table_access": dict(sorted(table_access.items(), key=lambda x: x[1], reverse=True)[:10]),  # Top 10
            "slow_queries": {
                "count": len(slow_queries),
                "percentage": round(len(slow_queries) / len(recent_queries) * 100, 2) if recent_queries else 0,
                "avg_duration_ms": round(statistics.mean([m.duration_ms for m in slow_queries]), 2) if slow_queries else 0
            }
        }
        
        # Connection stats
        if recent_connections:
            latest_connection = recent_connections[-1]
            summary["connection_stats"] = {
                "active_connections": latest_connection.active_connections,
                "idle_connections": latest_connection.idle_connections,
                "total_connections": latest_connection.total_connections,
                "failed_connections": latest_connection.failed_connections,
                "avg_connection_time_ms": round(latest_connection.avg_connection_time_ms, 2)
            }
        
        # Cache the result
        self._stats_cache = summary
        self._cache_timestamp = now
        
        return summary
    
    def get_slow_query_report(self, hours_back: int = 24) -> List[Dict[str, Any]]:
        """Get detailed report of slow queries"""
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
        
        with self._lock:
            slow_queries = [
                m for m in self._query_metrics
                if m.timestamp > cutoff_time and m.duration_ms > self.slow_query_threshold_ms
            ]
        
        # Group by query pattern
        query_patterns = {}
        for metric in slow_queries:
            pattern_key = f"{metric.query_type}_{metric.table_name}"
            if pattern_key not in query_patterns:
                query_patterns[pattern_key] = []
            query_patterns[pattern_key].append(metric)
        
        # Create report
        report = []
        for pattern, metrics in query_patterns.items():
            durations = [m.duration_ms for m in metrics]
            
            report.append({
                "query_pattern": pattern,
                "query_type": metrics[0].query_type,
                "table_name": metrics[0].table_name,
                "occurrences": len(metrics),
                "avg_duration_ms": round(statistics.mean(durations), 2),
                "max_duration_ms": round(max(durations), 2),
                "min_duration_ms": round(min(durations), 2),
                "total_time_ms": round(sum(durations), 2),
                "first_occurrence": min(m.timestamp for m in metrics).isoformat(),
                "last_occurrence": max(m.timestamp for m in metrics).isoformat(),
                "sample_query_hash": metrics[0].query_hash
            })
        
        return sorted(report, key=lambda x: x["total_time_ms"], reverse=True)

# Decorator for monitoring database operations

def monitor_db_query(query_type: str, table_name: Optional[str] = None):
    """Decorator to monitor database query performance"""
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate query hash for correlation
            query_hash = f"{func.__name__}_{hash(str(args) + str(kwargs)) % 1000000:06d}"
            
            start_time = time.time()
            success = True
            error_message = None
            result = None
            row_count = None
            
            try:
                result = func(*args, **kwargs)
                
                # Try to get row count from result
                if hasattr(result, '__len__'):
                    row_count = len(result)
                elif hasattr(result, 'rowcount'):
                    row_count = result.rowcount
                
                return result
                
            except Exception as e:
                success = False
                error_message = str(e)
                raise
                
            finally:
                duration_ms = (time.time() - start_time) * 1000
                
                # Log to monitor
                monitor.log_query(
                    query_hash=query_hash,
                    query_type=query_type,
                    table_name=table_name or "unknown",
                    duration_ms=duration_ms,
                    success=success,
                    error_message=error_message,
                    row_count=row_count
                )
        
        return wrapper
    return decorator

@contextmanager
def monitor_db_operation(query_type: str, table_name: Optional[str] = None):
    """Context manager for monitoring database operations"""
    
    query_hash = f"{query_type}_{table_name}_{int(time.time() * 1000) % 1000000:06d}"
    start_time = time.time()
    success = True
    error_message = None
    
    try:
        yield query_hash
        
    except Exception as e:
        success = False
        error_message = str(e)
        raise
        
    finally:
        duration_ms = (time.time() - start_time) * 1000
        
        monitor.log_query(
            query_hash=query_hash,
            query_type=query_type,
            table_name=table_name or "unknown",
            duration_ms=duration_ms,
            success=success,
            error_message=error_message
        )

# Global monitor instance
monitor = DatabaseMonitor()

# Helper functions for integration with existing database layer

def track_query_performance(func: Callable) -> Callable:
    """Generic decorator to track any database function performance"""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Try to infer query type and table from function name
        func_name = func.__name__.lower()
        
        if 'select' in func_name or 'get' in func_name or 'load' in func_name:
            query_type = 'SELECT'
        elif 'insert' in func_name or 'create' in func_name or 'save' in func_name:
            query_type = 'INSERT'
        elif 'update' in func_name:
            query_type = 'UPDATE'
        elif 'delete' in func_name:
            query_type = 'DELETE'
        else:
            query_type = 'UNKNOWN'
        
        # Try to infer table name from function name
        table_name = None
        common_tables = ['sessions', 'responses', 'clients', 'forms', 'tracking']
        for table in common_tables:
            if table in func_name:
                table_name = table
                break
        
        return monitor_db_query(query_type, table_name)(func)(*args, **kwargs)
    
    return wrapper

# Export main components
__all__ = [
    'DatabaseMonitor',
    'QueryMetrics',
    'ConnectionMetrics', 
    'SlowQueryAlert',
    'monitor',
    'monitor_db_query',
    'monitor_db_operation',
    'track_query_performance'
]