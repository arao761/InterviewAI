# Vapi API Endpoint Troubleshooting

## Issue: 404 Not Found Error

You're getting a 404 error because Vapi may not have a direct transcription endpoint like OpenAI Whisper.

## Understanding Vapi

**Important:** Vapi is primarily a **voice AI platform** for building voice assistants, not a standalone transcription service. They may not offer a direct `/transcriptions` endpoint.

## Solutions

### Option 1: Check Vapi's Actual API Documentation

1. Go to [Vapi API Documentation](https://vapi.ai/docs)
2. Look for transcription or speech-to-text endpoints
3. Update the endpoint in your `.env` file:

```env
VAPI_TRANSCRIPTION_ENDPOINT=/actual/endpoint/path
```

### Option 2: Use Vapi's Voice Assistant API

If Vapi doesn't have direct transcription, you might need to:
1. Create a voice assistant in Vapi
2. Use the assistant to process audio
3. Extract transcription from the response

### Option 3: Fall Back to Whisper

If Vapi doesn't support direct transcription, you can switch back to Whisper:

```env
# In voice/.env
TRANSCRIPTION_PROVIDER=whisper
OPENAI_API_KEY=your_openai_key
```

## Current Endpoint Configuration

The service tries these endpoints (in order of common patterns):
- `/v1/transcriptions` (default - OpenAI-style)
- Can be overridden with `VAPI_TRANSCRIPTION_ENDPOINT` in `.env`

## How to Find the Correct Endpoint

1. **Check Vapi Dashboard:**
   - Log into [dashboard.vapi.ai](https://dashboard.vapi.ai)
   - Look for API documentation or examples

2. **Check Vapi Documentation:**
   - Visit [vapi.ai/docs](https://vapi.ai/docs)
   - Search for "transcription" or "speech to text"

3. **Contact Vapi Support:**
   - Ask if they have a transcription API
   - Get the correct endpoint URL

4. **Test Different Endpoints:**
   Add to `voice/.env`:
   ```env
   # Try different endpoint patterns:
   VAPI_TRANSCRIPTION_ENDPOINT=/api/v1/transcriptions
   # OR
   VAPI_TRANSCRIPTION_ENDPOINT=/transcribe
   # OR
   VAPI_TRANSCRIPTION_ENDPOINT=/api/transcribe
   ```

## Quick Fix: Switch to Whisper

If you need transcription working immediately:

1. **Update `.env`:**
   ```env
   TRANSCRIPTION_PROVIDER=whisper
   # Make sure OPENAI_API_KEY is set
   ```

2. **Restart backend:**
   ```bash
   # Stop current server (Ctrl+C)
   python3 main.py
   ```

## Next Steps

1. **Verify Vapi has transcription:**
   - Check their documentation
   - Contact support if needed

2. **If Vapi doesn't have transcription:**
   - Use Whisper (already configured)
   - Or find an alternative transcription service

3. **If Vapi does have transcription:**
   - Get the correct endpoint from docs
   - Update `VAPI_TRANSCRIPTION_ENDPOINT` in `.env`
   - Restart server

---

**Recommendation:** If you need transcription working now, switch to Whisper. If you specifically need Vapi, check their documentation for the correct transcription endpoint.

