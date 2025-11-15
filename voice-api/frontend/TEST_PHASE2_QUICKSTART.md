# 🚀 Quick Start: Testing Phase 2

## Fastest Way to Test (2 minutes)

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

### Step 2: Start Development Server

```bash
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

### Step 3: Open Test Page

Open your browser and go to:
```
http://localhost:5173/test-phase2.html
```

### Step 4: Run Tests

The test page includes:

1. **Browser Compatibility Check** - Automatically runs on load
2. **Recording Controls** - Test start/stop/pause/resume
3. **Audio Playback** - Test recorded audio
4. **Error Handling** - Test various error scenarios
5. **Event System** - See all events in real-time
6. **API Integration** - Test backend connection (if running)

### What to Test

1. **Click "Start Recording"**
   - Browser will ask for microphone permission
   - Click "Allow"
   - Status should show "Recording"
   - Duration counter should start

2. **Speak into microphone**
   - Say something like "Hello, this is a test"
   - Watch the waveform visualization
   - Duration should increase

3. **Click "Stop"**
   - Status should show "Stopped"
   - Audio player should appear
   - File info should be displayed

4. **Play the recording**
   - Click play on the audio player
   - You should hear your voice!

5. **Test API Integration** (optional)
   - Start backend: `cd ../voice && python main.py`
   - Click "Test API Connection"
   - If you have a recording, try transcription

## ✅ Success Indicators

If you see:
- ✅ Microphone permission prompt appears
- ✅ Recording starts after permission granted
- ✅ Duration counter increments
- ✅ Waveform visualization works
- ✅ Stop button works
- ✅ Audio playback works
- ✅ File info is displayed
- ✅ No errors in console

**Then Phase 2 is working! 🎉**

## Alternative: Manual Testing

If you prefer to test programmatically, open browser console and run:

```javascript
// Import the module (if using ES modules)
import { AudioRecorder } from './src/index.ts';

// Create recorder
const recorder = new AudioRecorder();

// Request permission
await recorder.requestPermission();

// Start recording
await recorder.start();

// ... wait a few seconds ...

// Stop recording
const result = await recorder.stop();

// Play the recording
const audio = new Audio(result.url);
audio.play();

// Check results
console.log('Duration:', result.duration);
console.log('Size:', result.size);
console.log('Format:', result.format);
```

## Troubleshooting

### "Cannot GET /test-phase2.html"
- Make sure you're using `npm run dev` (not `npm run build`)
- Check that the file exists in the `frontend/` directory
- Try accessing: `http://localhost:5173/test-phase2.html`

### "Module not found" errors
- Make sure you ran `npm install`
- Check that `src/index.ts` exists
- Try restarting the dev server

### Microphone not working
- Check browser permissions
- Ensure microphone is connected
- Try a different browser
- Check system microphone settings

### API connection fails
- Make sure backend is running: `cd ../voice && python main.py`
- Check backend is on `http://localhost:8000`
- Check CORS settings in backend

## Full Testing Guide

For comprehensive testing, see: `PHASE2_TESTING_GUIDE.md`

---

**That's it! Start testing now! 🧪**

