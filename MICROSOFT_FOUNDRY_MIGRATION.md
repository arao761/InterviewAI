# Microsoft Foundry Migration

This document describes the migration from Vapi to Microsoft Foundry for voice API integration.

## Overview

InterviewAI now uses **Microsoft Foundry** (Azure AI Services) combined with **Azure Speech Services** for real-time voice interviews instead of Vapi.

## Architecture

- **Microsoft Foundry**: Provides the conversational AI endpoint for interview questions and responses
- **Azure Speech Services**: Handles real-time speech-to-text (STT) and text-to-speech (TTS)

## Setup Instructions

### 1. Azure Portal Setup

#### Microsoft Foundry
1. Navigate to [Azure Portal](https://portal.azure.com)
2. Go to your Microsoft Foundry project (e.g., "InterviewAI")
3. Copy the **Project Endpoint** URL (e.g., `https://theinterviewai.services.ai.azure.com/api/projects/InterviewAI`)
4. Copy the **API Key** from the "Endpoints and keys" section

#### Azure Speech Services
1. In Azure Portal, create or navigate to a **Speech** resource
2. Go to "Keys and Endpoint"
3. Copy the **Key 1** (or Key 2)
4. Copy the **Region** (e.g., `eastus`, `westus2`)

### 2. Environment Variables

Add the following to your `frontend/.env.local`:

```bash
# Microsoft Foundry Configuration
NEXT_PUBLIC_FOUNDRY_ENDPOINT=https://theinterviewai.services.ai.azure.com/api/projects/InterviewAI
NEXT_PUBLIC_FOUNDRY_API_KEY=your-foundry-api-key-here

# Azure Speech Services Configuration
NEXT_PUBLIC_AZURE_SPEECH_REGION=your-region-here
NEXT_PUBLIC_AZURE_SPEECH_KEY=your-speech-key-here
```

**Note**: The endpoint format may need adjustment based on your specific Microsoft Foundry setup. If the chat completions endpoint doesn't work, you may need to modify the endpoint format in `frontend/lib/microsoft-foundry/foundry-interviewer.ts`.

### 3. Install Dependencies

The migration replaces `@vapi-ai/web` with `microsoft-cognitiveservices-speech-sdk`:

```bash
cd frontend
pnpm install
```

The package.json has already been updated to include `microsoft-cognitiveservices-speech-sdk`.

## Key Changes

### Code Structure

- **Old**: `frontend/lib/vapi/vapi-interviewer.ts`
- **New**: `frontend/lib/microsoft-foundry/foundry-interviewer.ts`

### API Differences

#### Vapi (Old)
- Single SDK handled both voice and AI
- Used WebSocket for real-time communication
- Required `assistantId` configuration

#### Microsoft Foundry (New)
- Separate services: Foundry for AI, Speech Services for voice
- REST API for AI responses
- Real-time speech recognition via Azure Speech SDK
- More granular control over speech settings

### Features

✅ **Maintained Features:**
- Real-time speech-to-text transcription
- Text-to-speech for AI responses
- Interview context and personalization
- Time management and reminders
- Conversation history tracking

✅ **New Capabilities:**
- Direct control over speech recognition settings
- Customizable voice selection
- Better error handling and recovery
- More flexible conversation management

## Files Modified

1. **Created**: `frontend/lib/microsoft-foundry/foundry-interviewer.ts` - New interviewer class
2. **Modified**: `frontend/app/interview/page.tsx` - Updated to use FoundryInterviewer
3. **Modified**: `frontend/package.json` - Replaced `@vapi-ai/web` with `microsoft-cognitiveservices-speech-sdk`
4. **Modified**: `SECURITY.md` - Updated environment variable documentation
5. **Modified**: `frontend/lib/utils/conversation-transformer.ts` - Updated comments
6. **Modified**: `frontend/next.config.mjs` - Updated CSP comments

## Testing

1. Start the frontend: `cd frontend && pnpm dev`
2. Navigate to the interview page
3. Start a voice interview
4. Verify:
   - Microphone permissions are requested
   - Speech recognition works (you see your words transcribed)
   - AI responses are generated and spoken
   - Conversation flows naturally

## Troubleshooting

### "Microsoft Foundry configuration missing"
- Check that all environment variables are set in `.env.local`
- Restart the Next.js dev server after adding variables

### "Speech recognition error"
- Verify Azure Speech Services key and region are correct
- Check microphone permissions in browser
- Ensure Speech resource is active in Azure Portal

### "Foundry API error"
- Verify the endpoint URL is correct (should end with `/api/projects/YourProjectName`)
- Check API key is valid and not expired
- Ensure the Foundry project is active
- **Note**: The endpoint format in the code assumes `/chat/completions` path. If your Foundry endpoint uses a different format, you may need to adjust the API call in `foundry-interviewer.ts`

### Audio playback issues
- Check browser audio permissions
- Verify AudioContext is supported (modern browsers)
- Check browser console for Web Audio API errors

## Security Notes

- API keys are exposed to the client (prefixed with `NEXT_PUBLIC_`)
- Implement domain restrictions in Azure Portal
- Use IP whitelisting for production
- Rotate keys regularly
- Monitor usage in Azure Portal

## Support

For issues with:
- **Microsoft Foundry**: Check [Azure AI Services documentation](https://learn.microsoft.com/azure/ai-services/)
- **Azure Speech Services**: Check [Speech Services documentation](https://learn.microsoft.com/azure/ai-services/speech-service/)
