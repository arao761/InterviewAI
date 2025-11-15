# Testing Guide: Vapi Integration (Phases 1-3)

## 🚀 Quick Start Testing

### Step 1: Start the Backend Server

Open a terminal and run:

```bash
cd voice
source venv/bin/activate
python3 main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!** The server needs to keep running.

---

### Step 2: Test Backend API (Phase 1)

Open a **new terminal** and test the endpoints:

#### Test Health Endpoint
```bash
curl http://localhost:8000/health
```

**Expected output:**
```json
{
  "status": "healthy",
  "service": "PrepWise Voice API",
  "transcription_provider": "vapi",
  "api_keys_configured": {
    "vapi": true
  },
  "ready_for_requests": true
}
```

✅ **Check:** `"transcription_provider": "vapi"` and `"vapi": true`

#### Test Config Endpoint
```bash
curl http://localhost:8000/config
```

**Expected output:**
```json
{
  "status": "success",
  "config": {
    "transcription_provider": "vapi",
    "api_keys_configured": {
      "vapi": true
    }
  }
}
```

✅ **Check:** Provider is "vapi"

#### Test Root Endpoint
```bash
curl http://localhost:8000/
```

✅ **Check:** Should return API information with endpoints listed

---

### Step 3: Test Frontend Recording (Phase 2)

1. **Start the frontend dev server** (in a new terminal):
   ```bash
   cd frontend
   npm run dev
   ```

2. **Open your browser** to:
   ```
   http://localhost:5173/test-phase2.html
   ```

3. **Test Recording:**
   - Click "Start Recording"
   - Allow microphone permissions
   - Speak for a few seconds
   - Click "Stop Recording"
   - ✅ **Check:** Audio waveform appears, duration shows

4. **Test Playback:**
   - Click "Play Recording"
   - ✅ **Check:** Audio plays back correctly

---

### Step 4: Test Transcription (Phase 3)

#### Option A: Using Frontend (Easiest)

1. **Record audio** (as in Step 3)

2. **Transcribe:**
   - Check "Include Timestamps" ✅
   - Check "Include Confidence Scores" ✅
   - Select language (or leave "Auto-detect")
   - Click "Transcribe Recording"

3. **Verify Results:**
   - ✅ Transcript text appears
   - ✅ Metadata shows (duration, format, etc.)
   - ✅ Timestamps section shows word-level and segment-level
   - ✅ Confidence scores section shows:
     - Average confidence
     - Word-level confidence scores
   - ✅ **Important:** Confidence scores should ALWAYS appear (100% of the time)

#### Option B: Using API Directly (Advanced)

```bash
# Create a test audio file first, then:
curl -X POST "http://localhost:8000/transcribe?include_timestamps=true&include_confidence=true" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/audio.wav"
```

---

## 🧪 Comprehensive Test Checklist

### Phase 1: Backend API ✅
- [ ] Health endpoint returns `"transcription_provider": "vapi"`
- [ ] Config endpoint shows Vapi configured
- [ ] Root endpoint lists `/transcribe` endpoint
- [ ] CORS headers are present

### Phase 2: Frontend Recording ✅
- [ ] Microphone permission request works
- [ ] Recording starts and stops correctly
- [ ] Audio waveform visualizes during recording
- [ ] Duration counter increments
- [ ] Playback works after recording

### Phase 3: Transcription ✅
- [ ] Transcription endpoint accepts audio files
- [ ] Transcript text is returned
- [ ] Timestamps are included (word-level and segment-level)
- [ ] **Confidence scores are ALWAYS present** (100% of transcriptions)
- [ ] Metadata includes duration, format, model
- [ ] Language parameter works (if specified)
- [ ] Error handling works for invalid files

---

## 🔍 What to Look For

### ✅ Success Indicators

1. **Health Check:**
   - Shows `"transcription_provider": "vapi"`
   - Shows `"vapi": true` in api_keys_configured

2. **Transcription Response:**
   ```json
   {
     "status": "success",
     "transcript": "your transcribed text here",
     "metadata": {
       "model": "vapi",
       "duration_seconds": 5.2
     },
     "timestamps": {
       "words": [...],
       "segments": [...]
     },
     "confidence": {
       "average": 0.85,
       "word_level": [...]
     }
   }
   ```

3. **Confidence Scores:**
   - ✅ Should ALWAYS be present when `include_confidence=true`
   - ✅ Either actual scores from Vapi OR estimated scores
   - ✅ Never null or empty

### ❌ Common Issues

**"Vapi API error: 404"**
- The API endpoint might need adjustment
- Check `voice/utils/vapi_transcription_service.py` line ~289
- May need to update the endpoint URL based on Vapi's actual API

**"Vapi API error: 401"**
- API key might be incorrect
- Verify key in `.env` file
- Make sure you're using PRIVATE key (not public)

**"Transcription failed"**
- Check backend terminal for error details
- Verify audio file format is supported
- Check network connectivity

**"Confidence scores missing"**
- Should never happen - confidence is always provided
- If it does, check backend logs for errors

---

## 🎯 Quick Test Script

Run this to test everything at once:

```bash
#!/bin/bash
echo "🧪 Testing Vapi Integration"
echo ""

echo "1. Testing health endpoint..."
curl -s http://localhost:8000/health | grep -q "vapi" && echo "   ✅ Vapi configured" || echo "   ❌ Vapi not configured"

echo "2. Testing config endpoint..."
curl -s http://localhost:8000/config | grep -q "vapi" && echo "   ✅ Provider set to vapi" || echo "   ❌ Provider not set"

echo "3. Testing transcription service initialization..."
cd voice
source venv/bin/activate
python3 -c "from utils.vapi_transcription_service import VapiTranscriptionService; s = VapiTranscriptionService(); print('   ✅ Service initialized')" 2>/dev/null && echo "   ✅ Service works" || echo "   ❌ Service failed"

echo ""
echo "✅ Basic tests complete!"
echo "For full testing, use the frontend: http://localhost:5173/test-phase2.html"
```

---

## 📊 Expected Test Results

### Backend Tests
```bash
cd voice
source venv/bin/activate
python3 tests/test_phases_1_3_comprehensive.py
```

**Expected:** All Phase 1-3 tests should pass ✅

### Frontend Test
- Open: `http://localhost:5173/test-phase2.html`
- Record → Transcribe → Verify all features work

---

## 🎉 Success Criteria

You'll know everything works when:

1. ✅ Backend starts without errors
2. ✅ Health endpoint shows Vapi as provider
3. ✅ Frontend can record audio
4. ✅ Transcription returns text
5. ✅ Timestamps are included
6. ✅ **Confidence scores are ALWAYS present** (100% of the time)
7. ✅ All metadata is correct

---

**Ready to test! Start with Step 1 above.** 🚀

