#!/bin/bash
# Quick test script for Vapi integration

echo "🧪 Testing Vapi Integration"
echo "============================"
echo ""

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "❌ Backend server is not running!"
    echo "   Start it with: cd voice && python3 main.py"
    exit 1
fi

echo "1️⃣  Testing Health Endpoint..."
HEALTH=$(curl -s http://localhost:8000/health)
if echo "$HEALTH" | grep -q '"transcription_provider": "vapi"'; then
    echo "   ✅ Provider: vapi"
else
    echo "   ❌ Provider not set to vapi"
fi

if echo "$HEALTH" | grep -q '"vapi": true'; then
    echo "   ✅ Vapi key configured"
else
    echo "   ❌ Vapi key not configured"
fi

echo ""
echo "2️⃣  Testing Config Endpoint..."
CONFIG=$(curl -s http://localhost:8000/config)
if echo "$CONFIG" | grep -q '"transcription_provider": "vapi"'; then
    echo "   ✅ Config shows vapi provider"
else
    echo "   ❌ Config provider mismatch"
fi

echo ""
echo "3️⃣  Testing Transcription Service..."
cd voice 2>/dev/null || { echo "   ❌ Cannot find voice directory"; exit 1; }
source venv/bin/activate 2>/dev/null
python3 -c "
from utils.vapi_transcription_service import VapiTranscriptionService
try:
    service = VapiTranscriptionService()
    print('   ✅ VapiTranscriptionService initialized')
    print('   ✅ Base URL:', service.base_url)
except Exception as e:
    print('   ❌ Service initialization failed:', str(e))
" 2>/dev/null

echo ""
echo "4️⃣  Testing Backend Tests..."
python3 tests/test_phases_1_3_comprehensive.py 2>&1 | tail -20

echo ""
echo "============================"
echo "✅ Basic tests complete!"
echo ""
echo "📝 Next Steps:"
echo "   1. Test frontend: http://localhost:5173/test-phase2.html"
echo "   2. Record audio and transcribe"
echo "   3. Verify confidence scores appear (100% of the time)"
echo ""

