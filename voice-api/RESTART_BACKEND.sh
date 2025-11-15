#!/bin/bash
# Quick script to restart the backend server

echo "🔄 Restarting backend server..."

cd "$(dirname "$0")/voice"

# Kill existing server
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "   Stopping existing server..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    sleep 1
fi

# Start server
echo "   Starting server..."
source venv/bin/activate
python3 main.py

