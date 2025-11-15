# 🎤 Hands-On Interactive Testing Guide

This guide shows you how to actually **use** the application and test it interactively!

## 🚀 Quick Start (5 minutes)

### Step 1: Start the Backend Server

Open **Terminal 1** and run:

```bash
cd /Users/mahajans/Claude-Hackathon/voice-api/voice
source venv/bin/activate
python3 main.py
```

**You should see:**
```
🚀 Starting PrepWise Voice API...
📍 Server will be available at: http://localhost:8000
📚 API Documentation: http://localhost:8000/docs
❤️  Health Check: http://localhost:8000/health
```

**Keep this terminal open!** The server needs to keep running.

### Step 2: Start the Frontend

Open **Terminal 2** (new terminal window) and run:

```bash
cd /Users/mahajans/Claude-Hackathon/voice-api/frontend
npm run dev
```

**You should see:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

**Keep this terminal open too!**

### Step 3: Open the Test Page

Open your web browser and go to:

```
http://localhost:5173/test-phase2.html
```

You'll see a beautiful test interface with:
- Recording controls
- Waveform visualization
- Audio playback
- Transcription section

---

## 🎯 Interactive Testing Steps

### Test 1: Record Audio

1. **Click "Start Recording"** button
2. **Allow microphone access** when browser prompts
3. **Speak into your microphone** - say something like:
   - "Hello, this is a test of the voice recording system"
   - "I am testing the transcription feature"
   - "Can you hear me clearly?"
4. **Watch the waveform** - you should see it moving as you speak
5. **Watch the duration** - it should be counting up (e.g., "5.2s")
6. **Click "Stop"** when done

**What to check:**
- ✅ Microphone permission prompt appears
- ✅ Recording starts after permission granted
- ✅ Waveform shows activity when you speak
- ✅ Duration counter increases
- ✅ Stop button works

### Test 2: Play Back Your Recording

1. **After stopping**, you should see an audio player
2. **Click the play button** on the audio player
3. **Listen to your recording**

**What to check:**
- ✅ Audio player appears after stopping
- ✅ You can hear your voice clearly
- ✅ Audio quality is good
- ✅ File size and format are displayed

### Test 3: Transcribe Your Recording

1. **Scroll down to "Test 3.5: Speech-to-Text Transcription"**
2. **Make sure "Automatically transcribe after recording stops" is checked**
3. **If you already recorded**, click **"Transcribe Recording"** button
4. **Wait for transcription** - you'll see "🔄 Transcribing audio... Please wait."
5. **See your transcript appear!**

**What to check:**
- ✅ Transcription starts automatically (or manually)
- ✅ Loading message appears
- ✅ Transcript text appears in the display box
- ✅ Text matches what you said
- ✅ Status shows "✅ Transcription successful!"

### Test 4: Check Advanced Features

After transcription, look for:

1. **Timestamps** (if enabled):
   - Word-level timestamps
   - Segment-level timestamps

2. **Confidence Scores** (if available):
   - Average confidence
   - Per-word confidence

3. **Metadata**:
   - Duration
   - Format
   - File size

---

## 🎨 What You'll See

### The Test Page Has:

1. **Recording Controls Section**
   - Format selector (WebM, WAV, MP3)
   - Bitrate selector
   - Sample rate selector
   - Start/Pause/Resume/Stop buttons

2. **Real-time Status**
   - Current state (idle, recording, paused, stopped)
   - Duration counter
   - File size
   - Format

3. **Waveform Visualization**
   - Real-time waveform as you speak
   - Visual feedback of audio levels

4. **Audio Playback**
   - Audio player with controls
   - Validation results

5. **Transcription Section**
   - Auto-transcribe checkbox
   - Transcribe button
   - Transcript display box
   - Status messages

6. **Event Log**
   - All events logged in real-time
   - Success/error messages

---

## ✅ Success Indicators

### Phase 2 (Recording) Works If:
- ✅ You can start/stop recording
- ✅ Waveform shows activity
- ✅ Audio playback works
- ✅ File info is displayed

### Phase 3 (Transcription) Works If:
- ✅ Transcription completes successfully
- ✅ Transcript text appears
- ✅ Text matches what you said
- ✅ No errors in the log

---

## 🔧 Troubleshooting

### "Backend API not available"
**Problem:** Frontend can't connect to backend

**Solution:**
1. Check backend is running in Terminal 1
2. Visit `http://localhost:8000/health` in browser
3. Should show: `{"status": "healthy", ...}`

### "Transcription failed"
**Problem:** Transcription doesn't work

**Solutions:**
1. **Check API key:**
   - Make sure `OPENAI_API_KEY` is in `voice/.env` file
   - Format: `OPENAI_API_KEY=sk-your-key-here`

2. **Check backend logs:**
   - Look at Terminal 1 for error messages
   - Common: "Invalid API key" or "Rate limit"

3. **Check audio file:**
   - Make sure you actually recorded something
   - Recording should be at least 0.1 seconds

### "Microphone not working"
**Problem:** Can't record audio

**Solutions:**
1. Check browser permissions (Settings → Privacy → Microphone)
2. Make sure microphone is connected
3. Try a different browser
4. Check system microphone settings

### "Waveform not showing"
**Problem:** Waveform visualization is blank

**Solutions:**
1. Make sure you're speaking into the microphone
2. Check microphone is working (test in another app)
3. Try refreshing the page

---

## 🎯 Full Test Checklist

### Phase 2 Features:
- [ ] Can request microphone permission
- [ ] Can start recording
- [ ] Waveform visualization works
- [ ] Can pause/resume recording
- [ ] Can stop recording
- [ ] Audio playback works
- [ ] File info is displayed correctly
- [ ] Different formats work (WebM, WAV)

### Phase 3 Features:
- [ ] Transcription starts automatically
- [ ] Transcription completes successfully
- [ ] Transcript text appears
- [ ] Text is accurate
- [ ] Timestamps are included (if enabled)
- [ ] Confidence scores are included (if available)
- [ ] Metadata is displayed
- [ ] Error handling works (try with backend off)

---

## 🎬 Example Test Session

1. **Start both servers** (backend + frontend)

2. **Open test page:**
   ```
   http://localhost:5173/test-phase2.html
   ```

3. **Record a test:**
   - Click "Start Recording"
   - Say: "Hello, my name is [your name]. I am testing the voice transcription system. This is a test of Phase 2 and Phase 3 features."
   - Click "Stop"

4. **Verify recording:**
   - Play back the audio
   - Check it sounds clear

5. **Test transcription:**
   - Wait for auto-transcription (or click "Transcribe Recording")
   - Verify transcript matches what you said
   - Check for timestamps and confidence scores

6. **Test different features:**
   - Try different formats (WebM, WAV)
   - Try different bitrates
   - Test pause/resume
   - Test error scenarios

---

## 💡 Pro Tips

1. **Speak clearly** - Better audio = better transcription
2. **Test in quiet environment** - Reduces background noise
3. **Check browser console** - Press F12 to see detailed logs
4. **Try different browsers** - Chrome, Firefox, Safari
5. **Test error scenarios** - Stop backend, deny permissions, etc.

---

## 🎉 Success!

If you can:
- ✅ Record audio
- ✅ See waveform
- ✅ Play back recording
- ✅ Get transcription
- ✅ See timestamps and confidence

**Then Phases 2 and 3 are working perfectly!** 🎊

---

**Now go test it yourself! Open that browser and start recording!** 🎤

