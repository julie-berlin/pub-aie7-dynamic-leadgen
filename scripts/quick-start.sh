#!/bin/bash

# Quick start script for Dynamic Survey API
# Sets up the development environment and runs the application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Dynamic Survey API - Quick Start${NC}"
echo -e "${BLUE}===================================${NC}"
echo ""

# Check dependencies
check_dependencies() {
    echo -e "${YELLOW}🔍 Checking dependencies...${NC}"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 is required but not installed${NC}"
        exit 1
    fi
    
    # Check uv
    if ! command -v uv &> /dev/null; then
        echo -e "${YELLOW}⚠️  uv not found, installing...${NC}"
        pip install uv
    fi
    
    # Check Docker (optional)
    if ! command -v docker &> /dev/null; then
        echo -e "${YELLOW}⚠️  Docker not found (optional for development)${NC}"
    fi
    
    echo -e "${GREEN}✅ Dependencies check completed${NC}"
}

# Environment setup
setup_environment() {
    echo -e "${YELLOW}⚙️  Setting up environment...${NC}"
    
    # Create .env from example if it doesn't exist
    if [ ! -f "backend/.env" ]; then
        echo "Creating .env file from example..."
        cp backend/.env.example backend/.env
        echo -e "${YELLOW}📝 Please edit backend/.env with your configuration${NC}"
    fi
    
    # Install Python dependencies
    echo "Installing Python dependencies with uv..."
    cd backend
    uv sync
    cd ..
    
    echo -e "${GREEN}✅ Environment setup completed${NC}"
}

# Database setup
setup_database() {
    echo -e "${YELLOW}🗄️  Setting up database...${NC}"
    
    echo "Please ensure your Supabase database is set up and configured in backend/.env"
    echo "Run the database migrations in your Supabase SQL Editor:"
    echo "  1. backend/database/migrations/001_initial_schema.sql"
    echo "  2. backend/database/migrations/002_populate_example_data.sql"
    
    # Test database connection
    echo "Testing database connection..."
    cd backend
    if PYTHONPATH=. python3 -c "from app.database import db; exit(0 if db.test_connection() else 1)"; then
        echo -e "${GREEN}✅ Database connection successful${NC}"
    else
        echo -e "${RED}❌ Database connection failed${NC}"
        echo "Please check your database configuration in backend/.env"
        exit 1
    fi
    cd ..
}

# Start application
start_application() {
    echo -e "${YELLOW}🎯 Starting application...${NC}"
    
    cd backend
    
    # Start with development settings
    echo "Starting FastAPI application..."
    echo "Access the application at: http://localhost:8000"
    echo "API Documentation: http://localhost:8000/docs"
    echo "Health Check: http://localhost:8000/health"
    echo ""
    echo -e "${BLUE}Press Ctrl+C to stop the application${NC}"
    echo ""
    
    # Run with hot reload for development
    PYTHONPATH=. uv run uvicorn app.main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --reload \
        --log-level info
}

# Docker option
start_with_docker() {
    echo -e "${YELLOW}🐳 Starting with Docker...${NC}"
    
    if [ ! -f "docker-compose.yml" ]; then
        echo -e "${RED}❌ docker-compose.yml not found${NC}"
        exit 1
    fi
    
    # Start services
    echo "Starting services with docker-compose..."
    docker-compose up --build
}

# Help function
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --docker, -d     Start with Docker Compose"
    echo "  --help, -h       Show this help message"
    echo ""
    echo "Quick Start Steps:"
    echo "  1. Checks dependencies (Python 3, uv)"
    echo "  2. Sets up Python environment"
    echo "  3. Creates .env file from example"
    echo "  4. Tests database connection"
    echo "  5. Starts the application"
    echo ""
    echo "Requirements:"
    echo "  - Python 3.12+"
    echo "  - Supabase account and database"
    echo "  - OpenAI API key"
    echo ""
}

# Main function
main() {
    case "${1:-}" in
        --docker|-d)
            check_dependencies
            start_with_docker
            ;;
        --help|-h)
            show_help
            ;;
        *)
            check_dependencies
            setup_environment
            setup_database
            start_application
            ;;
    esac
}

# Run main function
main "$@"