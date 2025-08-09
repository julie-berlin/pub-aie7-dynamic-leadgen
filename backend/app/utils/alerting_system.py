"""
Alerting System for Survey Operations

Provides real-time monitoring and alerting for:
- High abandonment rates
- Performance degradation
- System health issues
- Conversion anomalies
"""

import logging
import asyncio
import json
from typing import Dict, List, Optional, Any, Callable, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import smtplib
import os
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.base import MimeBase
from email import encoders
import requests
import threading
import time

logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertType(Enum):
    """Types of alerts"""
    HIGH_ABANDONMENT = "high_abandonment"
    SLOW_PERFORMANCE = "slow_performance"
    SYSTEM_ERROR = "system_error"
    CONVERSION_DROP = "conversion_drop"
    DATABASE_ISSUE = "database_issue"
    API_FAILURE = "api_failure"
    HEALTH_CHECK_FAILURE = "health_check_failure"

@dataclass
class Alert:
    """Alert data structure"""
    alert_id: str
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    message: str
    timestamp: datetime
    data: Dict[str, Any] = field(default_factory=dict)
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    notification_sent: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary for serialization"""
        return {
            "alert_id": self.alert_id,
            "alert_type": self.alert_type.value,
            "severity": self.severity.value,
            "title": self.title,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "resolved": self.resolved,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "notification_sent": self.notification_sent
        }

class AlertChannel:
    """Base class for alert notification channels"""
    
    def __init__(self, name: str):
        self.name = name
    
    async def send_alert(self, alert: Alert) -> bool:
        """Send alert notification. Return True if successful."""
        raise NotImplementedError

class EmailAlertChannel(AlertChannel):
    """Email notification channel"""
    
    def __init__(
        self,
        name: str = "email",
        smtp_server: str = None,
        smtp_port: int = 587,
        smtp_username: str = None,
        smtp_password: str = None,
        from_email: str = None,
        to_emails: List[str] = None
    ):
        super().__init__(name)
        self.smtp_server = smtp_server or os.getenv('SMTP_SERVER')
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username or os.getenv('SMTP_USERNAME')
        self.smtp_password = smtp_password or os.getenv('SMTP_PASSWORD')
        self.from_email = from_email or os.getenv('ALERT_FROM_EMAIL')
        self.to_emails = to_emails or (os.getenv('ALERT_TO_EMAILS', '').split(',') if os.getenv('ALERT_TO_EMAILS') else [])
        
    async def send_alert(self, alert: Alert) -> bool:
        """Send email alert"""
        
        if not all([self.smtp_server, self.smtp_username, self.smtp_password, self.from_email, self.to_emails]):
            logger.warning("Email configuration incomplete - skipping email alert")
            return False
        
        try:
            # Create email message
            msg = MimeMultipart()
            msg['From'] = self.from_email
            msg['To'] = ', '.join(self.to_emails)
            msg['Subject'] = f"[{alert.severity.value.upper()}] {alert.title}"
            
            # Create email body
            body = self._create_email_body(alert)
            msg.attach(MimeText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            
            text = msg.as_string()
            server.sendmail(self.from_email, self.to_emails, text)
            server.quit()
            
            logger.info(f"Email alert sent successfully: {alert.alert_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email alert {alert.alert_id}: {e}")
            return False
    
    def _create_email_body(self, alert: Alert) -> str:
        """Create HTML email body"""
        
        severity_colors = {
            AlertSeverity.LOW: "#28a745",
            AlertSeverity.MEDIUM: "#ffc107", 
            AlertSeverity.HIGH: "#fd7e14",
            AlertSeverity.CRITICAL: "#dc3545"
        }
        
        color = severity_colors.get(alert.severity, "#6c757d")
        
        html = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: {color}; color: white; padding: 20px; border-radius: 5px 5px 0 0;">
                    <h1 style="margin: 0;">Survey System Alert</h1>
                    <h2 style="margin: 10px 0 0 0;">{alert.title}</h2>
                </div>
                
                <div style="background-color: #f8f9fa; padding: 20px; border: 1px solid #dee2e6; border-top: none;">
                    <p><strong>Severity:</strong> <span style="color: {color}; font-weight: bold;">{alert.severity.value.upper()}</span></p>
                    <p><strong>Type:</strong> {alert.alert_type.value.replace('_', ' ').title()}</p>
                    <p><strong>Time:</strong> {alert.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")}</p>
                    <p><strong>Alert ID:</strong> {alert.alert_id}</p>
                </div>
                
                <div style="padding: 20px; border: 1px solid #dee2e6; border-top: none;">
                    <h3>Message</h3>
                    <p>{alert.message}</p>
                    
                    {self._format_alert_data(alert.data) if alert.data else ""}
                </div>
                
                <div style="background-color: #e9ecef; padding: 15px; border: 1px solid #dee2e6; border-top: none; border-radius: 0 0 5px 5px;">
                    <p style="margin: 0; font-size: 12px; color: #6c757d;">
                        This alert was generated by the Survey System monitoring service.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _format_alert_data(self, data: Dict[str, Any]) -> str:
        """Format alert data for email display"""
        
        if not data:
            return ""
        
        html = "<h4>Details</h4><ul>"
        
        for key, value in data.items():
            if isinstance(value, (int, float)):
                html += f"<li><strong>{key.replace('_', ' ').title()}:</strong> {value}</li>"
            elif isinstance(value, str):
                html += f"<li><strong>{key.replace('_', ' ').title()}:</strong> {value}</li>"
            elif isinstance(value, dict):
                html += f"<li><strong>{key.replace('_', ' ').title()}:</strong><ul>"
                for sub_key, sub_value in value.items():
                    html += f"<li>{sub_key}: {sub_value}</li>"
                html += "</ul></li>"
        
        html += "</ul>"
        return html

class SlackAlertChannel(AlertChannel):
    """Slack webhook notification channel"""
    
    def __init__(
        self,
        name: str = "slack",
        webhook_url: str = None,
        channel: str = None,
        username: str = "Survey System"
    ):
        super().__init__(name)
        self.webhook_url = webhook_url or os.getenv('SLACK_WEBHOOK_URL')
        self.channel = channel or os.getenv('SLACK_CHANNEL', '#alerts')
        self.username = username
    
    async def send_alert(self, alert: Alert) -> bool:
        """Send Slack alert"""
        
        if not self.webhook_url:
            logger.warning("Slack webhook URL not configured - skipping Slack alert")
            return False
        
        try:
            # Create Slack message
            color_map = {
                AlertSeverity.LOW: "good",
                AlertSeverity.MEDIUM: "warning",
                AlertSeverity.HIGH: "danger", 
                AlertSeverity.CRITICAL: "danger"
            }
            
            payload = {
                "username": self.username,
                "channel": self.channel,
                "attachments": [
                    {
                        "color": color_map.get(alert.severity, "warning"),
                        "title": alert.title,
                        "text": alert.message,
                        "fields": [
                            {"title": "Severity", "value": alert.severity.value.upper(), "short": True},
                            {"title": "Type", "value": alert.alert_type.value.replace('_', ' ').title(), "short": True},
                            {"title": "Time", "value": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"), "short": True},
                            {"title": "Alert ID", "value": alert.alert_id, "short": True}
                        ],
                        "footer": "Survey System Monitoring",
                        "ts": int(alert.timestamp.timestamp())
                    }
                ]
            }
            
            # Add data fields if present
            if alert.data:
                for key, value in alert.data.items():
                    if len(payload["attachments"][0]["fields"]) < 10:  # Slack limit
                        payload["attachments"][0]["fields"].append({
                            "title": key.replace('_', ' ').title(),
                            "value": str(value),
                            "short": True
                        })
            
            # Send to Slack
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Slack alert sent successfully: {alert.alert_id}")
                return True
            else:
                logger.error(f"Slack API returned {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send Slack alert {alert.alert_id}: {e}")
            return False

class ConsoleAlertChannel(AlertChannel):
    """Console/log-based alert channel for development"""
    
    def __init__(self, name: str = "console"):
        super().__init__(name)
    
    async def send_alert(self, alert: Alert) -> bool:
        """Log alert to console"""
        
        severity_prefix = {
            AlertSeverity.LOW: "ℹ️",
            AlertSeverity.MEDIUM: "⚠️", 
            AlertSeverity.HIGH: "🚨",
            AlertSeverity.CRITICAL: "🔴"
        }
        
        prefix = severity_prefix.get(alert.severity, "❓")
        
        console_message = (
            f"{prefix} [{alert.severity.value.upper()}] {alert.title}\n"
            f"   Type: {alert.alert_type.value.replace('_', ' ').title()}\n"
            f"   Time: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"   ID: {alert.alert_id}\n"
            f"   Message: {alert.message}"
        )
        
        if alert.data:
            console_message += f"\n   Data: {json.dumps(alert.data, indent=2)}"
        
        # Use appropriate log level based on severity
        if alert.severity == AlertSeverity.CRITICAL:
            logger.critical(console_message)
        elif alert.severity == AlertSeverity.HIGH:
            logger.error(console_message)
        elif alert.severity == AlertSeverity.MEDIUM:
            logger.warning(console_message)
        else:
            logger.info(console_message)
        
        return True

class AlertManager:
    """Central alert management system"""
    
    def __init__(self):
        self.channels: Dict[str, AlertChannel] = {}
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []
        self.max_history = 1000
        
        # Alert rate limiting
        self.alert_counts: Dict[str, List[datetime]] = {}
        self.rate_limit_window_minutes = 60
        self.rate_limit_max_alerts = 10
        
        # Background monitoring
        self._monitoring_active = False
        self._monitoring_thread = None
        
        # Setup default channels
        self._setup_default_channels()
    
    def _setup_default_channels(self):
        """Setup default alert channels based on environment"""
        
        # Always add console channel for development
        self.add_channel(ConsoleAlertChannel())
        
        # Add email channel if configured
        if os.getenv('SMTP_SERVER') and os.getenv('ALERT_FROM_EMAIL'):
            self.add_channel(EmailAlertChannel())
        
        # Add Slack channel if configured
        if os.getenv('SLACK_WEBHOOK_URL'):
            self.add_channel(SlackAlertChannel())
    
    def add_channel(self, channel: AlertChannel):
        """Add an alert notification channel"""
        self.channels[channel.name] = channel
        logger.info(f"Added alert channel: {channel.name}")
    
    async def send_alert(
        self,
        alert_type: AlertType,
        severity: AlertSeverity,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        force: bool = False
    ) -> Alert:
        """Send an alert through all configured channels"""
        
        # Create alert
        alert_id = f"{alert_type.value}_{int(time.time() * 1000)}"
        alert = Alert(
            alert_id=alert_id,
            alert_type=alert_type,
            severity=severity,
            title=title,
            message=message,
            timestamp=datetime.utcnow(),
            data=data or {}
        )
        
        # Check rate limiting unless forced
        if not force and self._is_rate_limited(alert_type):
            logger.warning(f"Alert rate limited: {alert_type.value}")
            return alert
        
        # Store alert
        self.active_alerts[alert_id] = alert
        self.alert_history.append(alert)
        
        # Maintain history size
        if len(self.alert_history) > self.max_history:
            self.alert_history = self.alert_history[-self.max_history:]
        
        # Send through all channels
        successful_channels = []
        failed_channels = []
        
        for channel_name, channel in self.channels.items():
            try:
                success = await channel.send_alert(alert)
                if success:
                    successful_channels.append(channel_name)
                else:
                    failed_channels.append(channel_name)
            except Exception as e:
                logger.error(f"Channel {channel_name} failed: {e}")
                failed_channels.append(channel_name)
        
        alert.notification_sent = len(successful_channels) > 0
        
        # Log alert result
        logger.info(
            f"Alert sent: {alert_id} - Success: {successful_channels}, Failed: {failed_channels}",
            extra={
                "event_type": "alert_sent",
                "alert_id": alert_id,
                "alert_type": alert_type.value,
                "severity": severity.value,
                "successful_channels": successful_channels,
                "failed_channels": failed_channels
            }
        )
        
        return alert
    
    def _is_rate_limited(self, alert_type: AlertType) -> bool:
        """Check if alert type is rate limited"""
        
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=self.rate_limit_window_minutes)
        
        # Clean old entries
        alert_key = alert_type.value
        if alert_key in self.alert_counts:
            self.alert_counts[alert_key] = [
                ts for ts in self.alert_counts[alert_key]
                if ts > window_start
            ]
        else:
            self.alert_counts[alert_key] = []
        
        # Check if limit exceeded
        if len(self.alert_counts[alert_key]) >= self.rate_limit_max_alerts:
            return True
        
        # Add current alert
        self.alert_counts[alert_key].append(now)
        return False
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Mark an alert as resolved"""
        
        if alert_id in self.active_alerts:
            alert = self.active_alerts[alert_id]
            alert.resolved = True
            alert.resolved_at = datetime.utcnow()
            
            del self.active_alerts[alert_id]
            
            logger.info(f"Alert resolved: {alert_id}")
            return True
        
        return False
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all active (unresolved) alerts"""
        return list(self.active_alerts.values())
    
    def get_alert_history(self, hours_back: int = 24) -> List[Alert]:
        """Get alert history for specified time window"""
        cutoff = datetime.utcnow() - timedelta(hours=hours_back)
        return [alert for alert in self.alert_history if alert.timestamp > cutoff]
    
    def start_monitoring(self, check_interval_seconds: int = 300):
        """Start background monitoring for automatic alerts"""
        
        if self._monitoring_active:
            logger.warning("Alert monitoring already active")
            return
        
        self._monitoring_active = True
        self._monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(check_interval_seconds,),
            daemon=True
        )
        self._monitoring_thread.start()
        logger.info(f"Started alert monitoring with {check_interval_seconds}s interval")
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self._monitoring_active = False
        if self._monitoring_thread:
            self._monitoring_thread.join(timeout=5)
        logger.info("Stopped alert monitoring")
    
    def _monitoring_loop(self, check_interval_seconds: int):
        """Background monitoring loop"""
        
        while self._monitoring_active:
            try:
                asyncio.run(self._check_system_health())
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
            
            time.sleep(check_interval_seconds)
    
    async def _check_system_health(self):
        """Check system health and generate alerts if needed"""
        
        try:
            # Import here to avoid circular dependencies
            from .analytics_queries import SurveyAnalytics
            from .database_monitoring import monitor
            from ..database import db
            
            # Check for high abandonment rates
            analytics = SurveyAnalytics(db)
            abandonment_alerts = analytics.check_abandonment_alerts()
            
            for alert_data in abandonment_alerts:
                await self.send_alert(
                    AlertType.HIGH_ABANDONMENT,
                    AlertSeverity.HIGH if alert_data.get("abandonment_rate", 0) > 75 else AlertSeverity.MEDIUM,
                    f"High Abandonment Rate: {alert_data.get('form_id')}",
                    f"Form {alert_data.get('form_id')} has {alert_data.get('abandonment_rate')}% abandonment rate",
                    alert_data
                )
            
            # Check for performance issues
            performance_alerts = analytics.check_performance_alerts()
            
            for alert_data in performance_alerts:
                await self.send_alert(
                    AlertType.SLOW_PERFORMANCE,
                    AlertSeverity.MEDIUM,
                    f"Slow Performance: {alert_data.get('form_id')}",
                    f"Form {alert_data.get('form_id')} average completion time: {alert_data.get('avg_completion_minutes')}min",
                    alert_data
                )
            
            # Check database performance
            db_summary = monitor.get_performance_summary()
            if db_summary.get('query_stats', {}).get('success_rate', 100) < 95:
                await self.send_alert(
                    AlertType.DATABASE_ISSUE,
                    AlertSeverity.HIGH,
                    "Database Error Rate High",
                    f"Database success rate: {db_summary.get('query_stats', {}).get('success_rate', 0)}%",
                    db_summary
                )
            
        except Exception as e:
            logger.error(f"Error checking system health: {e}")

# Global alert manager instance
alert_manager = AlertManager()

# Convenience functions for common alerts

async def alert_high_abandonment(form_id: str, rate: float, session_count: int):
    """Send high abandonment rate alert"""
    await alert_manager.send_alert(
        AlertType.HIGH_ABANDONMENT,
        AlertSeverity.HIGH if rate > 75 else AlertSeverity.MEDIUM,
        f"High Abandonment Rate: {form_id}",
        f"Form {form_id} has {rate}% abandonment rate ({session_count} sessions)",
        {"form_id": form_id, "abandonment_rate": rate, "session_count": session_count}
    )

async def alert_system_error(component: str, error: str):
    """Send system error alert"""
    await alert_manager.send_alert(
        AlertType.SYSTEM_ERROR,
        AlertSeverity.HIGH,
        f"System Error: {component}",
        f"Error in {component}: {error}",
        {"component": component, "error": error}
    )

async def alert_performance_issue(operation: str, duration_ms: float, threshold_ms: float):
    """Send performance issue alert"""
    await alert_manager.send_alert(
        AlertType.SLOW_PERFORMANCE,
        AlertSeverity.MEDIUM,
        f"Slow Performance: {operation}",
        f"{operation} took {duration_ms:.2f}ms (threshold: {threshold_ms}ms)",
        {"operation": operation, "duration_ms": duration_ms, "threshold_ms": threshold_ms}
    )

# Export main components
__all__ = [
    'AlertManager',
    'Alert',
    'AlertType',
    'AlertSeverity',
    'EmailAlertChannel',
    'SlackAlertChannel',
    'ConsoleAlertChannel',
    'alert_manager',
    'alert_high_abandonment',
    'alert_system_error',
    'alert_performance_issue'
]