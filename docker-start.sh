#!/bin/bash

# InterviewAI Docker Startup Script
# Quick start script for Docker setup

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐳 InterviewAI Docker Setup${NC}"
echo "================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker Desktop.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker is running${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo -e "${BLUE}Creating .env from template...${NC}"
    
    # Create basic .env file
    cat > .env << EOF
# InterviewAI Environment Variables
OPENAI_API_KEY=your-openai-api-key-here
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || echo "your-secret-key-change-in-production")
DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/prepwise_db
REDIS_URL=redis://redis:6379/0
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
FRONTEND_URL=http://localhost:3000
EOF
    
    echo -e "${GREEN}✓ Created .env file${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env and add your OPENAI_API_KEY${NC}"
    echo ""
    read -p "Press Enter to continue after adding your API key..."
fi

# Build and start containers
echo -e "${BLUE}Building Docker images...${NC}"
docker-compose build

echo -e "${BLUE}Starting services...${NC}"
docker-compose up -d

# Wait for services to be healthy
echo -e "${BLUE}Waiting for services to start...${NC}"
sleep 5

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo -e "${GREEN}=========================================="
    echo "✅ InterviewAI is running!"
    echo "==========================================${NC}"
    echo ""
    echo -e "Frontend:  ${BLUE}http://localhost:3000${NC}"
    echo -e "Backend:   ${BLUE}http://localhost:8000${NC}"
    echo -e "API Docs:  ${BLUE}http://localhost:8000/api/v1/docs${NC}"
    echo ""
    echo "View logs:"
    echo "  docker-compose logs -f"
    echo ""
    echo "Stop services:"
    echo "  docker-compose down"
    echo ""
else
    echo -e "${RED}❌ Some services failed to start${NC}"
    echo "Check logs with: docker-compose logs"
    exit 1
fi
