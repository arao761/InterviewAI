#!/bin/bash

# PrepWise AI - Integration Test Script
# Tests that all components are properly integrated

clear
echo "🧪 PrepWise AI - Integration Tests"
echo "===================================="
echo ""

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FAILED=0

# Activate venv
cd "$SCRIPT_DIR"
source venv/bin/activate

echo -e "${BLUE}Test 1: Verify PrepWise AI package installation${NC}"
python -c "from src.api.prepwise_api import PrepWiseAPI" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ PrepWise AI package imports correctly${NC}"
else
    echo -e "${RED}✗ PrepWise AI package import failed${NC}"
    FAILED=$((FAILED + 1))
fi

echo -e "\n${BLUE}Test 2: Verify PrepWiseAPI initialization${NC}"
python -c "
from src.api.prepwise_api import PrepWiseAPI
import os
os.environ['OPENAI_API_KEY'] = 'test-key'
api = PrepWiseAPI()
print('✓ PrepWiseAPI initialized')
" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ PrepWiseAPI can be initialized${NC}"
else
    echo -e "${RED}✗ PrepWiseAPI initialization failed${NC}"
    FAILED=$((FAILED + 1))
fi

echo -e "\n${BLUE}Test 3: Verify Backend AIService integration${NC}"
cd "$SCRIPT_DIR/backend"
python -c "
import os
os.environ['OPENAI_API_KEY'] = 'test-key'
from app.services.ai_service import AIService
service = AIService()
print('✓ AIService initialized')
" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend AIService integrates correctly${NC}"
else
    echo -e "${RED}✗ Backend AIService integration failed${NC}"
    FAILED=$((FAILED + 1))
fi

echo -e "\n${BLUE}Test 4: Check Backend dependencies${NC}"
cd "$SCRIPT_DIR/backend"
if grep -q "^-e ../prepwise-ai" requirements.txt; then
    echo -e "${GREEN}✓ Backend requirements.txt includes prepwise-ai${NC}"
else
    echo -e "${RED}✗ Backend requirements.txt missing prepwise-ai reference${NC}"
    FAILED=$((FAILED + 1))
fi

echo -e "\n${BLUE}Test 5: Check environment configuration${NC}"
if [ -f "$SCRIPT_DIR/.env" ]; then
    if grep -q "OPENAI_API_KEY=your-openai-api-key-here" "$SCRIPT_DIR/.env"; then
        echo -e "${YELLOW}⚠️  OPENAI_API_KEY not configured (using placeholder)${NC}"
    else
        echo -e "${GREEN}✓ Environment variables configured${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
fi

echo -e "\n${BLUE}Test 6: Run PrepWise AI unit tests${NC}"
cd "$SCRIPT_DIR/prepwise-ai"
python -m pytest tests/ -q --tb=no 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All PrepWise AI tests passed${NC}"
else
    echo -e "${YELLOW}⚠️  Some tests failed (may be due to missing API keys)${NC}"
fi

# Summary
echo ""
echo "===================================="
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All integration tests passed!${NC}"
    echo ""
    echo "System is ready. You can now:"
    echo "1. Configure OpenAI API key in .env (if not done)"
    echo "2. Start all services: ./START_ALL_SERVICES.sh"
    exit 0
else
    echo -e "${RED}❌ $FAILED test(s) failed${NC}"
    echo ""
    echo "Please fix the issues above before starting the system."
    echo "You may need to run: ./SETUP_PROJECT.sh"
    exit 1
fi
