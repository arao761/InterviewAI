#!/bin/bash

echo "🛑 Stopping All PrepWise AI Services..."
echo ""

# Stop backend
if [ -f "backend/backend.pid" ]; then
    kill $(cat backend/backend.pid) 2>/dev/null
    rm backend/backend.pid
    echo "✓ Backend API stopped"
fi

# Stop voice API
if [ -f "voice-api/voice/voice.pid" ]; then
    kill $(cat voice-api/voice/voice.pid) 2>/dev/null
    rm voice-api/voice/voice.pid
    echo "✓ Voice API stopped"
fi

# Stop frontend
if [ -f "v0-interview-prep-app-main/frontend.pid" ]; then
    kill $(cat v0-interview-prep-app-main/frontend.pid) 2>/dev/null
    rm v0-interview-prep-app-main/frontend.pid
    echo "✓ Frontend stopped"
fi

# Also kill any processes on the ports
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:8001 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

echo ""
echo "All services stopped!"
