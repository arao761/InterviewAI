#!/bin/bash
# List all projects in the central API

TOKEN=$(curl -s -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"ankrao26@gmail.com","password":"Lakersfan23!"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo "Your projects:"
echo "=============="
curl -s http://localhost:8080/projects \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
