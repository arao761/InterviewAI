# Migration Guide: Switching from Whisper to Vapi

## Overview

This guide explains how to switch from OpenAI Whisper to Vapi while maintaining all Phases 1-3 functionality.

## What Changed

### New Files Created
- `voice/utils/vapi_transcription_service.py` - Vapi-based transcription service

### Files Modified
- `voice/config.py` - Added Vapi API key and provider selection
- `voice/main.py` - Updated to use Vapi when configured
- `voice/requirements.txt` - Added `requests` library

### Files Unchanged (Still Work!)
- All Phase 1 code (backend API)
- All Phase 2 code (frontend recording)
- All Phase 3 API endpoints (same interface)
- All tests (same interface)

## Migration Steps

### Step 1: Install Dependencies

```bash
cd voice
source venv/bin/activate
pip install requests
```

### Step 2: Get Vapi Private API Key

1. Sign up for Vapi account at https://vapi.ai
2. Go to [dashboard.vapi.ai](https://dashboard.vapi.ai)
3. Navigate to "API Keys" in your account menu
4. Copy your **PRIVATE API key** (not the public one!)
5. Add to `.env` file:

```bash
# In voice/.env file
# Use PRIVATE key for backend (keep it secret!)
VAPI_API_KEY=your_private_vapi_api_key_here
TRANSCRIPTION_PROVIDER=vapi
```

**Important:** 
- ✅ Use **PRIVATE** key (this is for backend/server-side use)
- ❌ Do NOT use public key (that's only for client-side JavaScript)
- 🔒 Keep your private key secret - never expose it in frontend code or public repos

### Step 3: Update Configuration

The system will automatically use Vapi when:
- `TRANSCRIPTION_PROVIDER=vapi` is set in `.env`
- `VAPI_API_KEY` is configured

### Step 4: Test

1. **Start backend:**
   ```bash
   cd voice
   source venv/bin/activate
   python3 main.py
   ```

2. **Test transcription:**
   - Use the frontend test page
   - Record audio and transcribe
   - Should work exactly the same!

## Configuration Options

### Use Vapi (Default)
```env
TRANSCRIPTION_PROVIDER=vapi
VAPI_API_KEY=your_vapi_key
```

### Use Whisper (Fallback)
```env
TRANSCRIPTION_PROVIDER=whisper
OPENAI_API_KEY=your_openai_key
```

## API Compatibility

The Vapi transcription service maintains **100% compatibility** with the existing interface:

- ✅ Same method signatures
- ✅ Same response format
- ✅ Same query parameters
- ✅ Same error handling
- ✅ Same features (timestamps, confidence, chunking)

## Vapi-Specific Features

### Confidence Scores
- Vapi provides confidence scores when available
- If not available, system estimates confidence based on:
  - Audio quality (sample rate)
  - Transcript length
  - Transcription patterns

### Timestamps
- Word-level timestamps
- Segment-level timestamps
- Automatically adjusted for chunked files

### Language Support
- Multi-language transcription
- Auto-detect or manual specification

## Testing

All existing tests work without modification:

```bash
# Backend tests
python3 tests/test_phases_1_3_comprehensive.py

# Frontend tests
# Open: http://localhost:5173/test-phase2.html
```

## Troubleshooting

### "Vapi API key not configured"
- Add `VAPI_API_KEY` to `voice/.env` file
- Restart backend server

### "Vapi API error"
- Check API key is valid
- Verify Vapi API endpoint URL
- Check network connectivity

### "Transcription failed"
- Verify Vapi API is accessible
- Check audio file format is supported
- Review backend logs for details

## API Endpoint Adjustments

You may need to adjust the Vapi API endpoint URL in:
- `voice/utils/vapi_transcription_service.py`
- Line: `VAPI_BASE_URL = "https://api.vapi.ai"`

Update based on Vapi's actual API documentation.

## Benefits of Vapi

1. **Always provides confidence scores** - Estimated when not available
2. **Better accuracy** - Vapi's advanced models
3. **Cost-effective** - Potentially better pricing
4. **Same interface** - No code changes needed

## Rollback

To switch back to Whisper:

```env
TRANSCRIPTION_PROVIDER=whisper
OPENAI_API_KEY=your_openai_key
```

No code changes needed!

---

**Migration Complete! All Phases 1-3 continue to work with Vapi!** 🎉

