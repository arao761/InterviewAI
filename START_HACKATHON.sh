#!/bin/bash

# PrepWise AI - Hackathon Startup Script
# This script starts both backend and frontend servers

clear
echo "🚀 PrepWise AI - Starting Hackathon Setup"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if backend is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Backend already running on port 8000${NC}"
else
    echo -e "${BLUE}Starting Backend API...${NC}"
    cd "$SCRIPT_DIR/backend"

    # Activate virtual environment
    source "$SCRIPT_DIR/venv/bin/activate"

    # Start backend in background
    nohup python main.py > backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > backend.pid

    # Wait for backend to start
    echo "Waiting for backend to start..."
    for i in {1..10}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Backend started successfully!${NC}"
            echo -e "  API Docs: ${BLUE}http://localhost:8000/api/v1/docs${NC}"
            break
        fi
        sleep 1
        echo -n "."
    done
    echo ""
fi

# Check if frontend is already running
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Frontend already running on port 3000${NC}"
else
    echo -e "${BLUE}Starting Frontend...${NC}"
    cd "$SCRIPT_DIR/v0-interview-prep-app-main"

    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo "Installing frontend dependencies..."
        pnpm install
    fi

    # Start frontend in background
    nohup pnpm dev > frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > frontend.pid

    echo -e "${GREEN}✓ Frontend starting...${NC}"
    echo -e "  Frontend: ${BLUE}http://localhost:3000${NC}"
    echo ""
fi

echo ""
echo "=========================================="
echo -e "${GREEN}🎉 PrepWise AI is running!${NC}"
echo "=========================================="
echo ""
echo -e "Frontend:  ${BLUE}http://localhost:3000${NC}"
echo -e "Backend:   ${BLUE}http://localhost:8000${NC}"
echo -e "API Docs:  ${BLUE}http://localhost:8000/api/v1/docs${NC}"
echo ""
echo "Logs:"
echo "  Backend:  backend/backend.log"
echo "  Frontend: v0-interview-prep-app-main/frontend.log"
echo ""
echo "To stop servers:"
echo "  ./STOP_HACKATHON.sh"
echo ""
echo -e "${GREEN}Good luck with your hackathon! 🚀${NC}"
echo ""
