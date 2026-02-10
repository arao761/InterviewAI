#!/bin/bash
# Login and create project

RESPONSE=$(curl -s -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"ankrao26@gmail.com","password":"Lakersfan23!"}')

TOKEN=$(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo "Token obtained, creating project..."

curl -X POST "http://localhost:8080/projects" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"project_id":"InterviewAI"}'
