#!/bin/bash
# Script to add Vapi Assistant ID to .env file

echo "🔑 Adding Vapi Assistant ID"
echo "============================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    touch .env
fi

# Check if VAPI_ASSISTANT_ID already exists
if grep -q "VAPI_ASSISTANT_ID=" .env; then
    echo "⚠️  VAPI_ASSISTANT_ID already exists in .env"
    echo "Current value:"
    grep "VAPI_ASSISTANT_ID=" .env | sed 's/VAPI_ASSISTANT_ID=.*/VAPI_ASSISTANT_ID=***HIDDEN***/'
    echo ""
    read -p "Do you want to update it? (y/n): " update
    if [ "$update" != "y" ]; then
        echo "Keeping existing ID."
        exit 0
    fi
    # Remove old line
    sed -i.bak '/^VAPI_ASSISTANT_ID=/d' .env
fi

# Get Assistant ID from user
echo "Please paste your Vapi Assistant ID:"
read assistant_id

if [ -z "$assistant_id" ]; then
    echo "❌ No ID provided. Exiting."
    exit 1
fi

# Add to .env
echo "" >> .env
echo "# Vapi Assistant ID (for AI interviewer)" >> .env
echo "VAPI_ASSISTANT_ID=$assistant_id" >> .env

# Make sure USE_DEEPGRAM_VIA_VAPI is false or not set
if grep -q "USE_DEEPGRAM_VIA_VAPI=true" .env; then
    echo ""
    echo "⚠️  USE_DEEPGRAM_VIA_VAPI is set to true"
    echo "   This will use Deepgram instead of Vapi calls"
    read -p "Set it to false to use Vapi directly? (y/n): " change
    if [ "$change" = "y" ]; then
        sed -i.bak 's/USE_DEEPGRAM_VIA_VAPI=true/USE_DEEPGRAM_VIA_VAPI=false/' .env
        echo "✅ Set USE_DEEPGRAM_VIA_VAPI=false"
    fi
fi

echo ""
echo "✅ Vapi Assistant ID added to .env file!"
echo ""
echo "📝 Next steps:"
echo "   1. Restart your backend server"
echo "   2. Test transcription - it will now use Vapi calls"
echo ""
echo "To verify, run:"
echo "  python3 -c \"import os; from dotenv import load_dotenv; load_dotenv(); print('✅ Set' if os.getenv('VAPI_ASSISTANT_ID') else '❌ Missing')\""
echo ""

