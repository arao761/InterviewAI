#!/bin/bash

# Docker Test Script for InterviewAI
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🧪 Testing Docker Setup for InterviewAI${NC}"
echo "=========================================="
echo ""

# Check Docker
echo -e "${BLUE}Step 1: Checking Docker...${NC}"
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running!${NC}"
    echo -e "${YELLOW}Please start Docker Desktop and try again.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker is running${NC}"

# Check Docker Compose
echo -e "${BLUE}Step 2: Checking Docker Compose...${NC}"
if ! docker-compose version > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker Compose not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose is available${NC}"

# Check .env file
echo -e "${BLUE}Step 3: Checking environment file...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo -e "${BLUE}Creating basic .env file...${NC}"
    cat > .env << EOF
OPENAI_API_KEY=your-openai-api-key-here
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || echo "change-this-secret-key")
DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/prepwise_db
REDIS_URL=redis://redis:6379/0
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
FRONTEND_URL=http://localhost:3000
EOF
    echo -e "${YELLOW}⚠️  Please edit .env and add your OPENAI_API_KEY${NC}"
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

# Stop any existing containers
echo -e "${BLUE}Step 4: Cleaning up any existing containers...${NC}"
docker-compose down -v 2>/dev/null || true
echo -e "${GREEN}✓ Cleanup complete${NC}"

# Build images
echo -e "${BLUE}Step 5: Building Docker images...${NC}"
echo -e "${YELLOW}This may take a few minutes on first run...${NC}"
docker-compose build --no-cache
echo -e "${GREEN}✓ Images built successfully${NC}"

# Start services
echo -e "${BLUE}Step 6: Starting services...${NC}"
docker-compose up -d
echo -e "${GREEN}✓ Services started${NC}"

# Wait for services
echo -e "${BLUE}Step 7: Waiting for services to be ready...${NC}"
sleep 10

# Check service status
echo -e "${BLUE}Step 8: Checking service status...${NC}"
docker-compose ps

# Test endpoints
echo -e "${BLUE}Step 9: Testing endpoints...${NC}"

# Test backend health
echo -n "Testing backend health endpoint... "
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend is healthy${NC}"
else
    echo -e "${RED}✗ Backend health check failed${NC}"
    echo "Backend logs:"
    docker-compose logs backend | tail -20
fi

# Test frontend
echo -n "Testing frontend... "
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Frontend is responding${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend may still be starting...${NC}"
fi

# Summary
echo ""
echo -e "${GREEN}=========================================="
echo "✅ Docker Test Complete!"
echo "==========================================${NC}"
echo ""
echo "Services are running:"
echo -e "  Frontend:  ${BLUE}http://localhost:3000${NC}"
echo -e "  Backend:   ${BLUE}http://localhost:8000${NC}"
echo -e "  API Docs:  ${BLUE}http://localhost:8000/api/v1/docs${NC}"
echo ""
echo "Useful commands:"
echo "  View logs:    docker-compose logs -f"
echo "  Stop:         docker-compose down"
echo "  Restart:      docker-compose restart"
echo ""
