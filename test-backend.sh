#!/bin/bash

echo "🧪 Testing PrepWise AI Backend Integration"
echo "==========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

BASE_URL="http://localhost:8000"

# Test 1: Root endpoint
echo "Test 1: Root endpoint"
response=$(curl -s "${BASE_URL}/")
if echo "$response" | grep -q "PrepWise"; then
    echo -e "${GREEN}✓ Root endpoint working${NC}"
else
    echo -e "${RED}✗ Root endpoint failed${NC}"
    echo "$response"
fi
echo ""

# Test 2: Health check
echo "Test 2: Health check"
response=$(curl -s "${BASE_URL}/health")
if echo "$response" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed${NC}"
    echo "$response"
fi
echo ""

# Test 3: AI Service health
echo "Test 3: AI Service health"
response=$(curl -s "${BASE_URL}/api/v1/ai/health")
if echo "$response" | grep -q "healthy"; then
    echo -e "${GREEN}✓ AI Service is healthy${NC}"
    echo "$response" | jq '.' 2>/dev/null || echo "$response"
else
    echo -e "${RED}✗ AI Service health check failed${NC}"
    echo "$response"
fi
echo ""

# Test 4: Generate questions
echo "Test 4: Generate interview questions"
response=$(curl -s -X POST "${BASE_URL}/api/v1/ai/generate-questions" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_data": {
      "name": "Test User",
      "skills": ["Python", "JavaScript"],
      "experience": [],
      "education": []
    },
    "interview_type": "technical",
    "num_questions": 2
  }')

if echo "$response" | grep -q "success"; then
    echo -e "${GREEN}✓ Question generation working${NC}"
    echo "$response" | jq '.count, .questions[0].question' 2>/dev/null || echo "$response"
else
    echo -e "${RED}✗ Question generation failed${NC}"
    echo "$response"
fi
echo ""

echo "==========================================="
echo "🎉 Backend testing complete!"
echo ""
echo "If all tests passed, your backend is ready!"
echo "Start frontend with: cd v0-interview-prep-app-main && pnpm dev"
