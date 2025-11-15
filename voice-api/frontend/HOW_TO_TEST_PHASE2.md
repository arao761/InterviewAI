# How to Test Phase 2: Frontend Audio Recording Component

## 📚 Overview

Phase 2 implements the complete frontend audio recording component with:
- ✅ Browser-based audio recording
- ✅ Microphone permission handling
- ✅ Recording controls (start/stop/pause/resume)
- ✅ Audio data handling (Blob, File conversion)
- ✅ Waveform visualization
- ✅ Audio quality optimization
- ✅ Error handling
- ✅ Browser compatibility

## 🎯 Quick Test (5 minutes)

### Method 1: Interactive Test Page (Recommended)

1. **Start the dev server:**
   ```bash
   cd frontend
   npm install  # if not already done
   npm run dev
   ```

2. **Open test page:**
   - Navigate to: `http://localhost:5173/test-phase2.html`
   - The page includes a complete test suite with UI

3. **Follow the on-screen tests:**
   - Browser compatibility check (automatic)
   - Recording controls test
   - Audio playback test
   - Error handling test
   - API integration test

### Method 2: Programmatic Testing

Open browser console and run:

```javascript
// Import (if using ES modules in browser)
import { AudioRecorder } from './src/index.ts';

// Or use the global if available
const { AudioRecorder } = window.PrepWiseVoiceRecorder;

// Create recorder
const recorder = new AudioRecorder();

// Test basic flow
async function test() {
  try {
    // Request permission
    await recorder.requestPermission();
    console.log('✅ Permission granted');
    
    // Start recording
    await recorder.start();
    console.log('✅ Recording started');
    
    // Wait 5 seconds
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    // Stop recording
    const result = await recorder.stop();
    console.log('✅ Recording stopped');
    console.log('Duration:', result.duration, 's');
    console.log('Size:', (result.size / 1024).toFixed(2), 'KB');
    console.log('Format:', result.format);
    
    // Play the recording
    const audio = new Audio(result.url);
    audio.play();
    
    // Clean up
    recorder.release();
  } catch (error) {
    console.error('❌ Error:', error);
  }
}

test();
```

## 📋 Complete Testing Checklist

### Test 1: Browser Recording Setup ✅

- [ ] **MediaRecorder API Support**
  - Open console: `typeof MediaRecorder !== 'undefined'` → should be `true`
  
- [ ] **Microphone Permission**
  - Call `recorder.requestPermission()`
  - Grant permission → should return `MediaStream`
  - Deny permission → should throw clear error

- [ ] **Format Detection**
  - Test WebM: `new AudioRecorder({ format: 'webm' })`
  - Test WAV: `new AudioRecorder({ format: 'wav' })`
  - Test MP3: `new AudioRecorder({ format: 'mp3' })`
  - Should auto-fallback if format not supported

- [ ] **Configuration**
  - Test different bitrates: `'64k'`, `'128k'`, `'192k'`, `'256k'`
  - Test different sample rates: `22050`, `44100`, `48000`
  - Test mono/stereo: `channels: 1` or `2`

### Test 2: Recording Controls ✅

- [ ] **Start Recording**
  - `await recorder.start()`
  - State should be `'recording'`
  - `recorder.isRecording()` → `true`
  - Duration should increment

- [ ] **Stop Recording**
  - `await recorder.stop()`
  - Should return `RecordingResult` with:
    - `blob`: Blob object
    - `file`: File object
    - `url`: Object URL
    - `duration`: Number
    - `format`: String
    - `size`: Number

- [ ] **Pause/Resume**
  - `recorder.pause()` → state should be `'paused'`
  - `recorder.resume()` → state should be `'recording'`
  - Duration should continue from pause point

- [ ] **Duration Tracking**
  - Record for exactly 10 seconds
  - Check `recorder.getDuration()` → should be ~10.0s
  - Accuracy within 0.5 seconds

### Test 3: Audio Data Handling ✅

- [ ] **Blob Creation**
  - After stop, `result.blob` should be valid Blob
  - `result.blob.size > 0`
  - `result.blob.type` matches format

- [ ] **File Conversion**
  - `result.file` should be File object
  - `result.file.name` has correct extension
  - Can be used with `FormData` for upload

- [ ] **Audio Playback**
  - Create `<audio src="${result.url}"></audio>`
  - Should play without errors
  - Sound quality should be clear

- [ ] **Waveform Visualization**
  ```javascript
  const visualizer = new AudioVisualizer();
  await visualizer.initialize(recorder.getStream());
  visualizer.start((data) => {
    drawWaveform(canvas, data.data);
  });
  ```
  - Should show real-time waveform
  - Updates smoothly

### Test 4: Audio Quality ✅

- [ ] **Noise Reduction**
  - Check browser constraints include:
    - `echoCancellation: true`
    - `noiseSuppression: true`
    - `autoGainControl: true`
  - Recorded audio should have less background noise

- [ ] **Audio Validation**
  - Record short clip (< 0.1s)
  - `recorder.validateRecording(result)` → should fail
  - Record normal clip (> 1s)
  - `recorder.validateRecording(result)` → should pass

- [ ] **Compression Recommendations**
  - Record large file
  - `getCompressionRecommendation(result.blob)`
  - Should return helpful recommendation

### Test 5: Error Handling ✅

- [ ] **Permission Denied**
  - Deny microphone permission
  - Should show clear error message
  - Should explain how to enable

- [ ] **No Microphone**
  - Disconnect microphone (if possible)
  - Should detect and show error

- [ ] **Microphone In Use**
  - Open another app using mic
  - Should detect conflict
  - Should suggest closing other apps

- [ ] **Invalid Configuration**
  - Try invalid format → should fall back
  - Try to change config while recording → should error

### Test 6: Browser Compatibility ✅

- [ ] **Chrome/Edge**
  - Test in Chrome 47+ or Edge
  - All features should work

- [ ] **Firefox**
  - Test in Firefox 25+
  - All features should work

- [ ] **Safari**
  - Test in Safari 14.1+
  - All features should work (may have format differences)

### Test 7: API Integration ✅

- [ ] **Backend Connection**
  ```bash
  # Start backend
  cd ../voice
  python main.py
  ```
  
  ```javascript
  // Test API client
  const client = new VoiceApiClient({ baseUrl: 'http://localhost:8000' });
  const health = await client.healthCheck();
  console.log('API Health:', health);
  ```

- [ ] **Transcription**
  ```javascript
  const result = await recorder.stop();
  const transcript = await client.transcribe(result.file, result.file.name);
  console.log('Transcript:', transcript);
  ```

## 🎨 Using the Test HTML Page

The `test-phase2.html` file provides:

1. **Browser Compatibility Check** - Automatically runs on load
2. **Interactive Controls** - Buttons for all recording functions
3. **Real-time Status** - Shows current state and duration
4. **Configuration Options** - Dropdowns for format, bitrate, sample rate
5. **Waveform Visualization** - Real-time waveform display
6. **Audio Preview** - Play recorded audio
7. **Validation Results** - Shows if recording is valid
8. **Event Log** - Shows all events in real-time
9. **API Testing** - Test backend connection and transcription

## 📊 Success Criteria

Phase 2 is **working correctly** if:

- ✅ Can request microphone permission
- ✅ Can start/stop recording
- ✅ Can pause/resume recording
- ✅ Duration tracking is accurate
- ✅ Audio playback works
- ✅ File info is accurate
- ✅ Configuration options work
- ✅ Error handling works
- ✅ No console errors
- ✅ Works in multiple browsers
- ✅ Can integrate with backend
- ✅ Waveform visualization works

## 🔧 Troubleshooting

### "Cannot GET /test-phase2.html"
- Make sure you're using `npm run dev` (not `npm run build`)
- Check file exists in `frontend/` directory
- Try: `http://localhost:5173/test-phase2.html`

### "Module not found"
- Run `npm install`
- Check `src/index.ts` exists
- Restart dev server

### Microphone not working
- Check browser permissions
- Ensure microphone is connected
- Try different browser
- Check system settings

### API connection fails
- Ensure backend is running: `cd ../voice && python main.py`
- Check backend URL matches: `http://localhost:8000`
- Check CORS settings in backend

## 📖 Additional Resources

- **Quick Start:** `TEST_PHASE2_QUICKSTART.md`
- **Complete Guide:** `PHASE2_TESTING_GUIDE.md`
- **Usage Examples:** `src/usage-example.ts`
- **API Documentation:** See code comments in source files

## 🎯 Next Steps

Once all tests pass:

1. ✅ Phase 2 is complete
2. ✅ Ready for Phase 3 (Transcription Service)
3. ✅ Can integrate into main application
4. ✅ Can customize UI/UX as needed

---

**Happy Testing! 🧪🎤**

