#!/bin/bash

# PrepWise AI - Complete Integration Startup Script
# Starts: Backend API + Voice API + Frontend

clear
echo "🚀 PrepWise AI - Starting ALL Services"
echo "=========================================="
echo ""

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 1. Start Backend API (Port 8000)
echo -e "${BLUE}1. Starting Backend API (Port 8000)...${NC}"
cd "$SCRIPT_DIR/backend"
source "$SCRIPT_DIR/venv/bin/activate"

# Verify prepwise-ai is installed
if ! python -c "from src.api.prepwise_api import PrepWiseAPI" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  PrepWise AI not installed. Installing...${NC}"
    pip install -e ../prepwise-ai
fi

# Set explicit port
export HOST=0.0.0.0
export PORT=8000
nohup python main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > backend.pid
echo -e "${GREEN}✓ Backend API started on http://localhost:8000 (PID: $BACKEND_PID)${NC}"
sleep 2

# 2. Start Voice API (Port 8001)
echo -e "${BLUE}2. Starting Voice API (Port 8001)...${NC}"
cd "$SCRIPT_DIR/voice-api/voice"
# Check if venv exists, if not use the main venv
if [ -d "venv" ]; then
    source venv/bin/activate
else
    source "$SCRIPT_DIR/venv/bin/activate"
fi
# Set explicit port
export HOST=0.0.0.0
export PORT=8001
nohup python main.py > voice.log 2>&1 &
VOICE_PID=$!
echo $VOICE_PID > voice.pid
echo -e "${GREEN}✓ Voice API started on http://localhost:8001 (PID: $VOICE_PID)${NC}"
sleep 2

# 3. Start Frontend (Port 3000)
echo -e "${BLUE}3. Starting Frontend (Port 3000)...${NC}"
cd "$SCRIPT_DIR/v0-interview-prep-app-main"
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    pnpm install
fi
# Set explicit port
export PORT=3000
nohup pnpm dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > frontend.pid
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}🎉 All Services Running!${NC}"
echo "=========================================="
echo ""
echo -e "📊 Services:"
echo -e "  ${BLUE}Backend API:${NC}  http://localhost:8000"
echo -e "  ${BLUE}Voice API:${NC}    http://localhost:8001"
echo -e "  ${BLUE}Frontend:${NC}     http://localhost:3000"
echo ""
echo -e "📚 Documentation:"
echo -e "  Backend Docs:  http://localhost:8000/api/v1/docs"
echo -e "  Voice Docs:    http://localhost:8001/docs"
echo ""
echo -e "📝 Logs:"
echo -e "  Backend:  backend/backend.log"
echo -e "  Voice:    voice-api/voice/voice.log"
echo -e "  Frontend: v0-interview-prep-app-main/frontend.log"
echo ""
echo -e "🛑 To stop all services:"
echo -e "  ./STOP_ALL_SERVICES.sh"
echo ""
echo -e "${GREEN}Ready for your hackathon! 🏆${NC}"
echo ""

# Wait a bit and check if services are running
sleep 3
echo "Checking service health..."
curl -s http://localhost:8000/health > /dev/null && echo -e "  ${GREEN}✓${NC} Backend API" || echo -e "  ${YELLOW}⚠${NC} Backend API (check logs)"
curl -s http://localhost:8001/health > /dev/null && echo -e "  ${GREEN}✓${NC} Voice API" || echo -e "  ${YELLOW}⚠${NC} Voice API (check logs)"
echo ""
