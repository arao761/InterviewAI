#!/bin/bash
# Script to start the backend server, handling port conflicts

echo "🚀 Starting PrepWise Voice API..."

# Check if port 8000 is in use
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "⚠️  Port 8000 is already in use"
    echo "   Stopping existing processes..."
    
    # Kill processes on port 8000
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    sleep 2
    
    # Verify port is free
    if lsof -ti:8000 > /dev/null 2>&1; then
        echo "❌ Could not free port 8000"
        echo "   Please manually stop the process using: lsof -ti:8000 | xargs kill -9"
        exit 1
    else
        echo "✅ Port 8000 is now free"
    fi
fi

# Activate virtual environment and start server
cd "$(dirname "$0")"
source venv/bin/activate
python3 main.py

