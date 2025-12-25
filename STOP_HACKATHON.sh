#!/bin/bash

# PrepWise AI - Stop Script

echo "🛑 Stopping PrepWise AI servers..."
echo ""

# Kill backend
if [ -f "backend/backend.pid" ]; then
    kill $(cat backend/backend.pid) 2>/dev/null
    rm backend/backend.pid
    echo "✓ Backend stopped"
fi

# Kill frontend
if [ -f "frontend/frontend.pid" ]; then
    kill $(cat frontend/frontend.pid) 2>/dev/null
    rm frontend/frontend.pid
    echo "✓ Frontend stopped"
fi

# Also kill any processes on ports 8000 and 3000
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

# Stop Redis
echo "Stopping Redis cache server..."
brew services stop redis
echo "✓ Redis stopped"

echo ""
echo "All servers stopped!"
