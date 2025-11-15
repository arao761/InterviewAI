# Complete Testing Guide: Vapi Integration & User Response Recording

## 🎯 Testing Goals

1. ✅ Verify Vapi is properly integrated
2. ✅ Test audio recording functionality
3. ✅ Test transcription of user responses
4. ✅ Verify confidence scores are returned
5. ✅ Test end-to-end interview flow

## 📋 Pre-Testing Checklist

Before you start, make sure:

- [ ] Backend server is running
- [ ] Frontend dev server is running
- [ ] Vapi API key is configured in `.env`
- [ ] Deepgram API key is configured (if using Deepgram)
- [ ] Assistant ID is set (if using Vapi calls)
- [ ] Microphone permissions are granted in browser

## 🚀 Step 1: Start the Servers

### Terminal 1: Backend Server
```bash
cd voice
source venv/bin/activate
python3 main.py
```

**Expected output:**
```
🚀 Starting PrepWise Voice API...
📍 Server will be available at: http://localhost:8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Frontend Server
```bash
cd frontend
npm run dev
```

**Expected output:**
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
```

## 🧪 Step 2: Test Backend API (Vapi Integration)

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "transcription_provider": "vapi",
  "api_keys_configured": {
    "vapi": true
  },
  "ready_for_requests": true
}
```

✅ **Check:** `"transcription_provider": "vapi"` and `"vapi": true`

### Test 2: Config Endpoint
```bash
curl http://localhost:8000/config
```

**Expected Response:**
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

### Test 3: Test Transcription Service Initialization
```bash
cd voice
source venv/bin/activate
python3 -c "
from utils.vapi_transcription_service import VapiTranscriptionService
from config import Config

print('Testing Vapi service...')
service = VapiTranscriptionService()
print('✅ VapiTranscriptionService initialized')
print(f'   Base URL: {service.base_url}')
print(f'   API Key configured: {bool(service.api_key)}')
"
```

**Expected Output:**
```
Testing Vapi service...
✅ VapiTranscriptionService initialized
   Base URL: https://api.vapi.ai
   API Key configured: True
```

## 🎤 Step 3: Test Frontend Recording

### Open Test Page
1. Open browser: `http://localhost:5173/test-phase2.html`
2. You should see the recording interface

### Test Recording Functionality

1. **Click "Start Recording"**
   - ✅ Browser should ask for microphone permission
   - ✅ Grant permission
   - ✅ Recording indicator should appear
   - ✅ Duration counter should start
   - ✅ Waveform should visualize (if enabled)

2. **Speak for 5-10 seconds**
   - Say something like: "Hello, my name is John and I'm interested in this position."

3. **Click "Stop Recording"**
   - ✅ Recording should stop
   - ✅ Duration should freeze
   - ✅ Audio should be saved

4. **Click "Play Recording"**
   - ✅ Audio should play back
   - ✅ You should hear your recorded voice

## 📝 Step 4: Test Transcription (User Response Recording)

### Test with Deepgram (Recommended)

1. **Make sure Deepgram is configured:**
   ```env
   # In voice/.env
   DEEPGRAM_API_KEY=your_key
   USE_DEEPGRAM_VIA_VAPI=true
   ```

2. **Record Audio:**
   - Click "Start Recording"
   - Say: "I have 5 years of experience in software development. I'm skilled in Python, JavaScript, and React."
   - Click "Stop Recording"

3. **Transcribe:**
   - Check "Include Timestamps" ✅
   - Check "Include Confidence Scores" ✅
   - Click "Transcribe Recording"

4. **Verify Results:**
   - ✅ Transcript text appears
   - ✅ Should show: "I have 5 years of experience..."
   - ✅ Timestamps section shows word-level timestamps
   - ✅ Confidence scores section shows:
     - Average confidence (e.g., 0.85)
     - Word-level confidence scores
   - ✅ Metadata shows duration, format, etc.

### Test with Vapi Calls (If Assistant ID is Set)

1. **Make sure Assistant ID is configured:**
   ```env
   # In voice/.env
   VAPI_ASSISTANT_ID=your_assistant_id
   USE_DEEPGRAM_VIA_VAPI=false
   ```

2. **Record and Transcribe:**
   - Same steps as above
   - Note: This creates an actual call with your assistant

3. **Verify:**
   - ✅ Transcript appears
   - ✅ Shows user's speech
   - ✅ Timestamps and confidence included

## 🔍 Step 5: Detailed Verification

### Check What Was Recorded

In the frontend, after transcription, verify:

1. **Transcript Text:**
   ```
   ✅ Matches what you said
   ✅ Proper punctuation
   ✅ Correct capitalization
   ```

2. **Timestamps:**
   ```
   ✅ Word-level timestamps present
   ✅ Each word has start/end time
   ✅ Segment-level timestamps present
   ✅ Times are reasonable (match audio duration)
   ```

3. **Confidence Scores:**
   ```
   ✅ Average confidence shown (0.0 to 1.0)
   ✅ Word-level confidence for each word
   ✅ Scores are reasonable (typically 0.7-0.98)
   ✅ NEVER null or empty (100% of the time)
   ```

4. **Metadata:**
   ```
   ✅ Duration matches recording time
   ✅ Format shown (webm, wav, etc.)
   ✅ Sample rate shown
   ✅ Model shown (vapi or deepgram)
   ```

## 🎯 Step 6: Test Interview Scenario

### Simulate an Interview Response

1. **Record Interview Answer:**
   - Click "Start Recording"
   - Say: "I'm excited about this opportunity because I've always been passionate about software development. In my previous role, I led a team of 5 developers and successfully delivered 3 major projects on time. I'm particularly interested in this position because it aligns with my career goals of working on innovative technology solutions."
   - Click "Stop Recording"

2. **Transcribe:**
   - Click "Transcribe Recording"
   - Wait for results

3. **Verify Complete Response:**
   - ✅ Full answer is transcribed
   - ✅ All sentences captured
   - ✅ Proper sentence structure
   - ✅ Key phrases present:
     - "excited about this opportunity"
     - "led a team of 5 developers"
     - "3 major projects"
     - "innovative technology solutions"

## 🐛 Step 7: Troubleshooting

### Issue: "Vapi API error: 404"

**Solution:**
- Make sure `USE_DEEPGRAM_VIA_VAPI=true` is set
- Or set `VAPI_ASSISTANT_ID` if using Vapi calls
- Check `DEEPGRAM_API_KEY` is configured

### Issue: "Transcription failed"

**Check:**
1. Backend logs for error details
2. Network tab in browser (F12) for API errors
3. Verify API keys are correct

### Issue: "No audio recorded"

**Check:**
1. Microphone permissions granted
2. Microphone is working (test in other apps)
3. Browser console for errors

### Issue: "Confidence scores missing"

**Should never happen!** If it does:
1. Check backend logs
2. Verify `include_confidence=true` in request
3. Check response format

## 📊 Step 8: Test Results Checklist

After testing, verify:

### Backend Tests ✅
- [ ] Health endpoint shows Vapi provider
- [ ] Config endpoint shows Vapi configured
- [ ] Transcription service initializes
- [ ] API endpoints respond correctly

### Recording Tests ✅
- [ ] Microphone permission works
- [ ] Recording starts/stops correctly
- [ ] Audio playback works
- [ ] Duration tracking works
- [ ] Waveform visualization works (if enabled)

### Transcription Tests ✅
- [ ] Transcription returns text
- [ ] Text matches what was said
- [ ] Timestamps are included
- [ ] Confidence scores are ALWAYS present
- [ ] Metadata is accurate

### Integration Tests ✅
- [ ] Frontend can communicate with backend
- [ ] Audio file is sent correctly
- [ ] Response is parsed correctly
- [ ] UI displays all information
- [ ] Error handling works

## 🎉 Success Criteria

You'll know everything works when:

1. ✅ Backend shows Vapi as provider
2. ✅ Recording captures audio clearly
3. ✅ Transcription accurately captures speech
4. ✅ Timestamps show when each word was spoken
5. ✅ Confidence scores appear for every transcription (100%)
6. ✅ Full interview responses are captured accurately

## 📝 Test Report Template

After testing, document:

```
Test Date: [Date]
Tester: [Your Name]

Backend Status: ✅ / ❌
- Health endpoint: ✅
- Config endpoint: ✅
- Service initialization: ✅

Recording Status: ✅ / ❌
- Microphone permission: ✅
- Recording start/stop: ✅
- Audio playback: ✅

Transcription Status: ✅ / ❌
- Text accuracy: ✅
- Timestamps: ✅
- Confidence scores: ✅
- Metadata: ✅

Issues Found:
- [List any issues]

Next Steps:
- [What to improve]
```

---

**Ready to test! Follow the steps above to verify your Vapi integration!** 🚀

