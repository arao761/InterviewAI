#!/bin/bash

echo "Testing production backend on Render..."
echo ""

# Test forgot password
echo "1. Requesting password reset..."
RESPONSE=$(curl -s -X POST https://interviewai-qsjr.onrender.com/api/v1/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email":"ankrao26@gmail.com"}')

echo "Response: $RESPONSE"
echo ""

# The token is emailed, so we can't get it from the API response
# But we can check the local database for testing

echo "2. To test reset password on production:"
echo "   - Check your email for the reset link"
echo "   - Click the link (it should point to your Vercel frontend)"
echo "   - The frontend will send the token to: https://interviewai-qsjr.onrender.com/api/v1/auth/reset-password"
echo ""
echo "3. If it still fails with 400:"
echo "   - Check Render logs to see the exact error"
echo "   - Make sure Render deployed the latest code (commit 5a89b23)"
echo "   - Check that FRONTEND_URL env var on Render is set correctly (no trailing slash)"
