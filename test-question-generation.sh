#!/bin/bash
# Test Question Generation Endpoint

echo "🧪 Testing Question Generation"
echo "=============================="
echo ""

# Test 1: Minimal request
echo "Test 1: Minimal request (both types)"
curl -X POST http://localhost:8000/api/v1/ai/generate-questions \
  -H "Content-Type: application/json" \
  -d '{
    "resume_data": {
      "name": "Test User",
      "skills": ["Python", "JavaScript"],
      "experience": []
    },
    "interview_type": "both",
    "num_questions": 3
  }' 2>/dev/null | python3 -m json.tool

echo ""
echo "================================================"
echo ""

# Test 2: With technical domain
echo "Test 2: Technical questions with domain"
curl -X POST http://localhost:8000/api/v1/ai/generate-questions \
  -H "Content-Type: application/json" \
  -d '{
    "resume_data": {
      "name": "Test User",
      "skills": ["Python", "React", "Node.js"],
      "experience": [
        {
          "title": "Software Engineer",
          "company": "Tech Corp"
        }
      ]
    },
    "interview_type": "technical",
    "domain": "web_development",
    "num_questions": 5
  }' 2>/dev/null | python3 -m json.tool

echo ""
echo "================================================"
echo ""

# Test 3: Behavioral only
echo "Test 3: Behavioral questions only"
curl -X POST http://localhost:8000/api/v1/ai/generate-questions \
  -H "Content-Type: application/json" \
  -d '{
    "resume_data": {
      "name": "Jane Doe",
      "experience": [
        {
          "title": "Senior Developer",
          "company": "StartupCo"
        }
      ]
    },
    "interview_type": "behavioral",
    "num_questions": 4
  }' 2>/dev/null | python3 -m json.tool

echo ""
echo "✅ Tests complete!"
