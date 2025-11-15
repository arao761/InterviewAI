# Vapi AI Interviewer Setup Guide

## Overview

For an AI interviewer application, Vapi works differently than simple transcription. Vapi is designed for **real-time voice conversations** with AI assistants, not just transcription.

## Two Approaches

### Approach 1: Use Deepgram Directly (Recommended for Transcription)

Vapi uses Deepgram for transcription. For just transcribing user speech, you can use Deepgram directly:

1. **Get Deepgram API Key:**
   - Sign up at [deepgram.com](https://deepgram.com)
   - Get your API key from the dashboard

2. **Configure in `.env`:**
   ```env
   DEEPGRAM_API_KEY=your_deepgram_key
   USE_DEEPGRAM_VIA_VAPI=true
   ```

3. **Benefits:**
   - Direct transcription (faster)
   - Lower cost for transcription-only
   - Same transcription quality Vapi uses

### Approach 2: Use Vapi Calls (For Full AI Interviewer)

For a complete AI interviewer with conversation flow:

1. **Create an Assistant in Vapi:**
   - Go to [dashboard.vapi.ai](https://dashboard.vapi.ai)
   - Create a new assistant
   - Configure it for interviews
   - Copy the Assistant ID

2. **Configure in `.env`:**
   ```env
   VAPI_ASSISTANT_ID=your_assistant_id
   ```

3. **How it works:**
   - Creates a call with your assistant
   - Assistant processes the audio
   - Returns transcript from the conversation
   - Can extend to full interview flow later

## Current Implementation

The service now supports both approaches:

- **Deepgram (transcription-only):** Fast, direct transcription
- **Vapi Calls (AI interviewer):** Full conversation with assistant

## Setup Steps

### For Transcription-Only (Quick Start)

```env
# In voice/.env
DEEPGRAM_API_KEY=your_deepgram_key
USE_DEEPGRAM_VIA_VAPI=true
VAPI_API_KEY=your_vapi_key  # Still needed for some features
TRANSCRIPTION_PROVIDER=vapi
```

### For AI Interviewer (Full Setup)

```env
# In voice/.env
VAPI_API_KEY=your_vapi_key
VAPI_ASSISTANT_ID=your_assistant_id
TRANSCRIPTION_PROVIDER=vapi
```

## Next Steps for AI Interviewer

1. **Create Assistant in Vapi Dashboard:**
   - Configure interview prompts
   - Set up conversation flow
   - Enable transcription

2. **Extend the Service:**
   - Add real-time audio streaming
   - Handle call events (webhooks)
   - Process interview responses
   - Store interview data

3. **Frontend Integration:**
   - Connect to Vapi Web SDK
   - Real-time audio streaming
   - Display interview questions
   - Show conversation flow

## API Endpoints for AI Interviewer

### Create Call
```python
POST https://api.vapi.ai/call
{
  "assistantId": "your_assistant_id",
  "customer": {
    "number": "+1234567890"  # Optional for web calls
  }
}
```

### Get Call Transcript
```python
GET https://api.vapi.ai/call/{call_id}/transcript
```

### Webhooks (Recommended)
Set up webhooks in Vapi dashboard to receive:
- Call events
- Transcripts in real-time
- User speech events

## Testing

1. **Test Transcription (Deepgram):**
   ```bash
   # Set USE_DEEPGRAM_VIA_VAPI=true
   # Record audio and transcribe
   ```

2. **Test AI Interviewer (Vapi Calls):**
   ```bash
   # Set VAPI_ASSISTANT_ID
   # Create a call
   # Get transcript
   ```

## Resources

- [Vapi Documentation](https://docs.vapi.ai)
- [Vapi AI Interviewer Guide](https://vapi.ai/library/build-and-deploy-a-full-stack-real-time-ai-voice-agent-interview-platform)
- [Deepgram API](https://developers.deepgram.com)

---

**For now, use Deepgram for transcription. Then extend to full AI interviewer with Vapi calls!**

