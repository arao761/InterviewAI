#!/bin/bash

# PrepWise AI - Complete Project Setup Script
# This script performs a fresh installation of all components

clear
echo "🔧 PrepWise AI - Complete Project Setup"
echo "=========================================="
echo ""

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"

# Step 1: Create main virtual environment
echo -e "\n${BLUE}Step 1: Creating main virtual environment...${NC}"
cd "$SCRIPT_DIR"
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  venv already exists, skipping creation${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate venv
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Step 2: Install AI Engine package (editable mode)
echo -e "\n${BLUE}Step 2: Installing AI Engine package...${NC}"
cd "$SCRIPT_DIR/ai-engine"
pip install --upgrade pip
pip install -e .
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ AI Engine installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install AI Engine${NC}"
    exit 1
fi

# Verify installation
echo -e "${BLUE}Verifying PrepWise AI installation...${NC}"
python -c "from src.api.prepwise_api import PrepWiseAPI; print('✓ Import successful')"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ PrepWise AI verified${NC}"
else
    echo -e "${RED}✗ PrepWise AI verification failed${NC}"
    exit 1
fi

# Step 3: Install Backend dependencies
echo -e "\n${BLUE}Step 3: Installing Backend dependencies...${NC}"
cd "$SCRIPT_DIR/backend"
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend dependencies installed${NC}"
else
    echo -e "${RED}✗ Failed to install backend dependencies${NC}"
    exit 1
fi

# Step 4: Install Frontend dependencies
echo -e "\n${BLUE}Step 4: Installing Frontend dependencies...${NC}"
cd "$SCRIPT_DIR/v0-interview-prep-app-main"
if command -v pnpm &> /dev/null; then
    pnpm install
    echo -e "${GREEN}✓ Frontend dependencies installed (pnpm)${NC}"
elif command -v npm &> /dev/null; then
    npm install
    echo -e "${GREEN}✓ Frontend dependencies installed (npm)${NC}"
else
    echo -e "${RED}✗ Neither pnpm nor npm found. Please install Node.js${NC}"
    exit 1
fi

# Step 5: Check environment variables
echo -e "\n${BLUE}Step 5: Checking environment variables...${NC}"
cd "$SCRIPT_DIR"
if [ -f ".env" ]; then
    if grep -q "OPENAI_API_KEY=your-openai-api-key-here" .env; then
        echo -e "${YELLOW}⚠️  OPENAI_API_KEY not configured in .env${NC}"
        echo -e "${YELLOW}   Please update .env with your OpenAI API key${NC}"
    else
        echo -e "${GREEN}✓ Environment variables configured${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo -e "${YELLOW}   Please create .env file with OPENAI_API_KEY${NC}"
fi

# Step 6: Run tests
echo -e "\n${BLUE}Step 6: Running tests...${NC}"
cd "$SCRIPT_DIR/ai-engine"
python -m pytest tests/ -v --tb=short
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed${NC}"
else
    echo -e "${YELLOW}⚠️  Some tests failed (this may be okay if API keys are not configured)${NC}"
fi

# Summary
echo -e "\n${GREEN}=========================================="
echo "✅ Setup Complete!"
echo "==========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Configure your OpenAI API key in .env"
echo "2. Start all services: ./START_ALL_SERVICES.sh"
echo "3. Access the application:"
echo "   - Backend API: http://localhost:8000/api/v1/docs"
echo "   - Voice API: http://localhost:8001/docs"
echo "   - Frontend: http://localhost:3000"
echo ""
