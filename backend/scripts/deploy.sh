#!/bin/bash

# Production deployment script for Dynamic Survey API
# Handles Docker build, environment setup, and deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="dynamic-survey"
ENVIRONMENT=${1:-production}
VERSION=${2:-latest}

echo -e "${BLUE}🚀 Dynamic Survey API Deployment${NC}"
echo -e "${BLUE}=================================${NC}"
echo "Environment: $ENVIRONMENT"
echo "Version: $VERSION"
echo ""

# Validation functions
validate_environment() {
    echo -e "${YELLOW}📋 Validating environment...${NC}"
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        echo -e "${RED}❌ .env file not found${NC}"
        echo "Please create .env file from .env.example"
        exit 1
    fi
    
    # Load environment variables
    set -a
    source .env
    set +a
    
    # Validate required variables
    REQUIRED_VARS=("SUPABASE_URL" "SUPABASE_SECRET_KEY" "OPENAI_API_KEY")
    
    if [ "$ENVIRONMENT" = "production" ]; then
        REQUIRED_VARS+=("ADMIN_API_KEY" "JWT_SECRET")
    fi
    
    for var in "${REQUIRED_VARS[@]}"; do
        if [ -z "${!var}" ]; then
            echo -e "${RED}❌ Required environment variable $var is not set${NC}"
            exit 1
        fi
    done
    
    echo -e "${GREEN}✅ Environment validation passed${NC}"
}

# Database validation
validate_database() {
    echo -e "${YELLOW}🔌 Validating database connectivity...${NC}"
    
    # Test database connection with timeout
    timeout 30 python3 -c "
import sys
sys.path.append('backend')
from app.database import db
if not db.test_connection():
    print('❌ Database connection failed')
    sys.exit(1)
else:
    print('✅ Database connection successful')
" || {
        echo -e "${RED}❌ Database validation failed${NC}"
        exit 1
    }
}

# Docker build and deployment
build_and_deploy() {
    echo -e "${YELLOW}🏗️  Building Docker images...${NC}"
    
    # Stop existing containers
    echo "Stopping existing containers..."
    docker-compose -f docker-compose.${ENVIRONMENT}.yml down || true
    
    # Build images
    echo "Building backend image..."
    docker-compose -f docker-compose.${ENVIRONMENT}.yml build backend
    
    # Tag with version
    docker tag ${PROJECT_NAME}-api:${ENVIRONMENT} ${PROJECT_NAME}-api:${VERSION}
    
    echo -e "${GREEN}✅ Docker images built successfully${NC}"
}

# Start services
start_services() {
    echo -e "${YELLOW}🎯 Starting services...${NC}"
    
    # Start with health checks
    docker-compose -f docker-compose.${ENVIRONMENT}.yml up -d
    
    # Wait for services to be healthy
    echo "Waiting for services to be healthy..."
    
    # Wait for backend
    echo "Checking backend health..."
    BACKEND_PORT=${BACKEND_PORT:-8000}
    
    for i in {1..30}; do
        if curl -f http://localhost:${BACKEND_PORT}/health/ready >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Backend is healthy${NC}"
            break
        fi
        
        if [ $i -eq 30 ]; then
            echo -e "${RED}❌ Backend failed to start${NC}"
            docker-compose -f docker-compose.${ENVIRONMENT}.yml logs backend
            exit 1
        fi
        
        echo "Waiting for backend... ($i/30)"
        sleep 5
    done
    
    echo -e "${GREEN}✅ All services started successfully${NC}"
}

# Post-deployment verification
verify_deployment() {
    echo -e "${YELLOW}🏥 Verifying deployment...${NC}"
    
    BACKEND_PORT=${BACKEND_PORT:-8000}
    
    # Test health endpoints
    echo "Testing health endpoints..."
    
    # Basic health
    if ! curl -f http://localhost:${BACKEND_PORT}/health >/dev/null 2>&1; then
        echo -e "${RED}❌ Basic health check failed${NC}"
        exit 1
    fi
    
    # Readiness
    if ! curl -f http://localhost:${BACKEND_PORT}/health/ready >/dev/null 2>&1; then
        echo -e "${RED}❌ Readiness check failed${NC}"
        exit 1
    fi
    
    # Status
    STATUS_RESPONSE=$(curl -s http://localhost:${BACKEND_PORT}/health/status)
    STATUS=$(echo $STATUS_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])")
    
    if [ "$STATUS" != "healthy" ]; then
        echo -e "${RED}❌ Service status is not healthy: $STATUS${NC}"
        echo "Status response: $STATUS_RESPONSE"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Deployment verification passed${NC}"
    echo ""
    echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
    echo ""
    echo "Service URLs:"
    echo "  Backend API: http://localhost:${BACKEND_PORT}"
    echo "  Health Check: http://localhost:${BACKEND_PORT}/health"
    echo "  API Docs: http://localhost:${BACKEND_PORT}/docs"
}

# Cleanup function
cleanup_on_error() {
    echo -e "${RED}💥 Deployment failed. Cleaning up...${NC}"
    docker-compose -f docker-compose.${ENVIRONMENT}.yml down || true
    exit 1
}

# Main deployment flow
main() {
    # Set up error handling
    trap cleanup_on_error ERR
    
    # Change to project root
    cd "$(dirname "$0")/.."
    
    echo -e "${BLUE}Starting deployment for environment: $ENVIRONMENT${NC}"
    
    # Run deployment steps
    validate_environment
    validate_database
    build_and_deploy
    start_services
    verify_deployment
    
    echo -e "${GREEN}🚀 Deployment completed successfully!${NC}"
}

# Help function
show_help() {
    echo "Usage: $0 [ENVIRONMENT] [VERSION]"
    echo ""
    echo "Arguments:"
    echo "  ENVIRONMENT    Target environment (development|staging|production)"
    echo "                 Default: production"
    echo "  VERSION        Image version tag"
    echo "                 Default: latest"
    echo ""
    echo "Examples:"
    echo "  $0                    # Deploy to production with latest"
    echo "  $0 staging v1.2.3     # Deploy to staging with v1.2.3"
    echo ""
    echo "Environment Requirements:"
    echo "  - .env file with required variables"
    echo "  - Docker and docker-compose installed"
    echo "  - Database connectivity"
    echo ""
}

# Parse command line arguments
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac