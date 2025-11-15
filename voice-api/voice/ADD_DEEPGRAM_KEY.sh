#!/bin/bash
# Script to add Deepgram API key to .env file

echo "🔑 Adding Deepgram API Key"
echo "============================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    touch .env
fi

# Check if DEEPGRAM_API_KEY already exists
if grep -q "DEEPGRAM_API_KEY=" .env; then
    echo "⚠️  DEEPGRAM_API_KEY already exists in .env"
    echo "Current value:"
    grep "DEEPGRAM_API_KEY=" .env | sed 's/DEEPGRAM_API_KEY=.*/DEEPGRAM_API_KEY=***HIDDEN***/'
    echo ""
    read -p "Do you want to update it? (y/n): " update
    if [ "$update" != "y" ]; then
        echo "Keeping existing key."
        exit 0
    fi
    # Remove old line
    sed -i.bak '/^DEEPGRAM_API_KEY=/d' .env
fi

# Check if USE_DEEPGRAM_VIA_VAPI exists
if ! grep -q "USE_DEEPGRAM_VIA_VAPI=" .env; then
    echo "USE_DEEPGRAM_VIA_VAPI=true" >> .env
    echo "✅ Added USE_DEEPGRAM_VIA_VAPI=true"
fi

# Get API key from user
echo ""
echo "📝 Get your Deepgram API key:"
echo "   1. Go to https://deepgram.com"
echo "   2. Sign up (free tier available)"
echo "   3. Go to API Keys in dashboard"
echo "   4. Create a new API key"
echo ""
echo "Please paste your Deepgram API key:"
read -s deepgram_key

if [ -z "$deepgram_key" ]; then
    echo "❌ No key provided. Exiting."
    exit 1
fi

# Add to .env
echo "" >> .env
echo "# Deepgram API (for transcription via Vapi)" >> .env
echo "DEEPGRAM_API_KEY=$deepgram_key" >> .env

echo ""
echo "✅ Deepgram API key added to .env file!"
echo ""
echo "📝 Next steps:"
echo "   1. Restart your backend server"
echo "   2. Test transcription in the frontend"
echo ""
echo "To verify, run:"
echo "  python3 -c \"import os; from dotenv import load_dotenv; load_dotenv(); print('✅ Set' if os.getenv('DEEPGRAM_API_KEY') else '❌ Missing')\""
echo ""

