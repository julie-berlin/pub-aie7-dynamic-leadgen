#!/bin/bash

# Production startup script for Dynamic Survey API
# Handles environment validation, database connectivity, and graceful startup

set -e  # Exit on any error

echo "🚀 Starting Dynamic Survey API in production mode..."

# Environment validation
echo "📋 Validating environment configuration..."
python3 -m app.utils.env_validator production
if [ $? -ne 0 ]; then
    echo "❌ Environment validation failed"
    exit 1
fi

# Database connectivity check
echo "🔌 Testing database connectivity..."
python3 -c "
from app.database import db
if not db.test_connection():
    print('❌ Database connection failed')
    exit(1)
else:
    print('✅ Database connection successful')
"

# Wait for external dependencies if needed
if [ ! -z "$WAIT_FOR_SERVICES" ]; then
    echo "⏳ Waiting for external services..."
    for service in $WAIT_FOR_SERVICES; do
        echo "  Waiting for $service..."
        timeout 60 bash -c "until curl -f $service/health 2>/dev/null; do sleep 2; done" || {
            echo "❌ Service $service is not available"
            exit 1
        }
    done
fi

# Pre-startup tasks
echo "⚙️  Running pre-startup tasks..."

# Create log directory
mkdir -p /app/logs

# Set up log rotation if logrotate is available
if command -v logrotate &> /dev/null; then
    echo "📝 Setting up log rotation..."
    cat > /tmp/logrotate.conf << EOF
/app/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 appuser appuser
}
EOF
    logrotate -f /tmp/logrotate.conf || true
fi

# Warm up the application
echo "🔥 Warming up application..."
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from app.main import app
    print('✅ Application loaded successfully')
except Exception as e:
    print(f'❌ Application failed to load: {e}')
    sys.exit(1)
"

# Final system check
echo "🏥 Running final system health check..."
python3 -c "
import os
import psutil

# Check memory usage
memory = psutil.virtual_memory()
if memory.percent > 90:
    print(f'⚠️  High memory usage: {memory.percent}%')

# Check disk space
disk = psutil.disk_usage('/')
if disk.percent > 90:
    print(f'⚠️  Low disk space: {disk.percent}% used')

# Check CPU
cpu_percent = psutil.cpu_percent(interval=1)
if cpu_percent > 80:
    print(f'⚠️  High CPU usage: {cpu_percent}%')

print('✅ System health check completed')
"

# Start the application
echo "🎯 Starting FastAPI application with production settings..."
echo "   Environment: $ENVIRONMENT"
echo "   Workers: $(python3 -c "from app.utils.config_loader import get_api_config; print(get_api_config().workers)")"
echo "   Port: 8000"
echo "   Log Level: $LOG_LEVEL"

# Start with gunicorn for production
if command -v gunicorn &> /dev/null; then
    echo "🦄 Starting with Gunicorn..."
    exec gunicorn app.main:app \
        --bind 0.0.0.0:8000 \
        --workers $(python3 -c "from app.utils.config_loader import get_api_config; print(get_api_config().workers)") \
        --worker-class uvicorn.workers.UvicornWorker \
        --max-requests 1000 \
        --max-requests-jitter 100 \
        --timeout 90 \
        --keep-alive 5 \
        --log-level info \
        --access-logfile /app/logs/access.log \
        --error-logfile /app/logs/error.log \
        --capture-output \
        --enable-stdio-inheritance
else
    echo "🦄 Starting with Uvicorn..."
    exec uvicorn app.main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --workers $(python3 -c "from app.utils.config_loader import get_api_config; print(get_api_config().workers)") \
        --log-level info \
        --access-log \
        --no-use-colors
fi