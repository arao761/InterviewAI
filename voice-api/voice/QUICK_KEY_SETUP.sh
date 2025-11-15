#!/bin/bash
# Quick script to add Vapi API key to .env file

echo "🔑 Vapi API Key Setup"
echo "===================="
echo ""
echo "This script will help you add your Vapi PRIVATE API key to the .env file"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    touch .env
fi

# Check if VAPI_API_KEY already exists
if grep -q "VAPI_API_KEY=" .env; then
    echo "⚠️  VAPI_API_KEY already exists in .env"
    echo "Current value:"
    grep "VAPI_API_KEY=" .env | sed 's/VAPI_API_KEY=.*/VAPI_API_KEY=***HIDDEN***/'
    echo ""
    read -p "Do you want to update it? (y/n): " update
    if [ "$update" != "y" ]; then
        echo "Keeping existing key."
        exit 0
    fi
    # Remove old line
    sed -i.bak '/^VAPI_API_KEY=/d' .env
fi

# Check if TRANSCRIPTION_PROVIDER exists
if ! grep -q "TRANSCRIPTION_PROVIDER=" .env; then
    echo "TRANSCRIPTION_PROVIDER=vapi" >> .env
    echo "✅ Added TRANSCRIPTION_PROVIDER=vapi"
fi

# Get API key from user
echo "Please paste your Vapi PRIVATE API key:"
read -s vapi_key

if [ -z "$vapi_key" ]; then
    echo "❌ No key provided. Exiting."
    exit 1
fi

# Add to .env
echo "" >> .env
echo "# Vapi API Configuration (for transcription)" >> .env
echo "VAPI_API_KEY=$vapi_key" >> .env

echo ""
echo "✅ Vapi API key added to .env file!"
echo ""
echo "To verify, run:"
echo "  python3 -c \"from config import Config; print('Key loaded:', 'YES' if Config.VAPI_API_KEY else 'NO')\""
echo ""

