# Phase 2 Testing Guide - Complete Checklist

This guide provides a comprehensive testing procedure for all Phase 2 features: Frontend Audio Recording Component.

## 📋 Table of Contents

1. [Quick Start Testing](#quick-start-testing)
2. [Detailed Feature Testing](#detailed-feature-testing)
3. [Browser Compatibility Testing](#browser-compatibility-testing)
4. [Error Handling Testing](#error-handling-testing)
5. [Integration Testing](#integration-testing)
6. [Performance Testing](#performance-testing)
7. [Automated Testing](#automated-testing)

---

## Quick Start Testing

### Option 1: Use the Test HTML File (Recommended)

1. **Start the development server:**
   ```bash
   cd frontend
   npm run dev
   ```

2. **Open the test file:**
   - Navigate to: `http://localhost:5173/test-phase2.html`
   - Or open `test-phase2.html` directly in your browser

3. **Run through the test suite:**
   - The page includes all test sections
   - Follow the on-screen instructions
   - Check the event log for detailed information

### Option 2: Manual Testing

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Build the project:**
   ```bash
   npm run build
   ```

3. **Import and use in your code:**
   ```typescript
   import { AudioRecorder } from './src/index';
   ```

---

## Detailed Feature Testing

### ✅ Test 1: Browser Recording Setup

#### 1.1 MediaRecorder API Support
- [ ] Open browser console
- [ ] Check: `typeof MediaRecorder !== 'undefined'` should be `true`
- [ ] Check: `typeof navigator.mediaDevices.getUserMedia !== 'undefined'` should be `true`

#### 1.2 Microphone Permission Request
- [ ] Create recorder instance: `const recorder = new AudioRecorder()`
- [ ] Call: `await recorder.requestPermission()`
- [ ] **Expected:** Browser shows permission prompt
- [ ] **Grant permission:**
  - [ ] Click "Allow" or "Allow access"
  - [ ] Should return `MediaStream` object
  - [ ] No errors in console
- [ ] **Deny permission:**
  - [ ] Click "Block" or "Deny"
  - [ ] Should throw error with message: "Microphone permission denied..."
  - [ ] Error should be clear and actionable

#### 1.3 MediaRecorder Initialization
- [ ] After permission granted, recorder should be ready
- [ ] Check: `recorder.getState()` should return `'idle'`
- [ ] Verify configuration is applied:
  ```typescript
  const config = recorder.getConfig();
  console.log(config); // Should show format, bitrate, sampleRate, etc.
  ```

#### 1.4 Format Detection
- [ ] Test WebM format: `new AudioRecorder({ format: 'webm' })`
- [ ] Test WAV format: `new AudioRecorder({ format: 'wav' })`
- [ ] Test MP3 format: `new AudioRecorder({ format: 'mp3' })`
- [ ] **Expected:** Browser should support at least WebM
- [ ] If format not supported, should fall back automatically
- [ ] Console should show warning if fallback occurs

#### 1.5 Configuration Options
- [ ] Test different bitrates: `'64k'`, `'128k'`, `'192k'`, `'256k'`
- [ ] Test different sample rates: `22050`, `44100`, `48000`
- [ ] Test mono vs stereo: `channels: 1` and `channels: 2`
- [ ] **Expected:** All configurations should work (with browser limitations)

---

### ✅ Test 2: Recording Controls

#### 2.1 Start Recording
- [ ] Call: `await recorder.start()`
- [ ] **Expected:**
  - [ ] State changes to `'recording'`
  - [ ] `recorder.isRecording()` returns `true`
  - [ ] Duration starts incrementing
  - [ ] Event `'start'` is emitted
  - [ ] No errors in console

#### 2.2 Stop Recording
- [ ] While recording, call: `await recorder.stop()`
- [ ] **Expected:**
  - [ ] Returns `RecordingResult` object with:
    - [ ] `blob`: Blob object
    - [ ] `file`: File object
    - [ ] `url`: Object URL for playback
    - [ ] `duration`: Number (seconds)
    - [ ] `format`: String
    - [ ] `size`: Number (bytes)
  - [ ] State changes to `'stopped'`
  - [ ] Event `'stop'` is emitted
  - [ ] Duration is accurate (within 0.5s)

#### 2.3 Pause Recording
- [ ] While recording, call: `recorder.pause()`
- [ ] **Expected:**
  - [ ] State changes to `'paused'`
  - [ ] Duration stops incrementing
  - [ ] Event `'pause'` is emitted
  - [ ] Can resume later

#### 2.4 Resume Recording
- [ ] While paused, call: `recorder.resume()`
- [ ] **Expected:**
  - [ ] State changes back to `'recording'`
  - [ ] Duration continues from where it paused
  - [ ] Event `'resume'` is emitted
  - [ ] Total duration is sum of all recording segments

#### 2.5 Duration Tracking
- [ ] Record for exactly 10 seconds (use timer)
- [ ] **Expected:**
  - [ ] `recorder.getDuration()` shows ~10.0s
  - [ ] After stop, `result.duration` is ~10.0s
  - [ ] Accuracy within 0.5 seconds

#### 2.6 Error Handling - No Microphone
- [ ] Disconnect microphone (if possible)
- [ ] Try: `await recorder.requestPermission()`
- [ ] **Expected:**
  - [ ] Error thrown: "No microphone found..."
  - [ ] State changes to `'error'`
  - [ ] Event `'error'` is emitted

#### 2.7 Error Handling - Permission Denied
- [ ] Deny microphone permission
- [ ] Try: `await recorder.requestPermission()`
- [ ] **Expected:**
  - [ ] Error thrown: "Microphone permission denied..."
  - [ ] Clear instructions on how to enable

#### 2.8 Error Handling - Microphone In Use
- [ ] Open another app using microphone (e.g., Zoom, Teams)
- [ ] Try: `await recorder.requestPermission()`
- [ ] **Expected:**
  - [ ] Error thrown: "Microphone is already in use..."
  - [ ] Helpful error message

---

### ✅ Test 3: Audio Data Handling

#### 3.1 Audio Chunks Collection
- [ ] Start recording
- [ ] **Expected:**
  - [ ] Chunks are collected during recording
  - [ ] Event `'dataavailable'` is emitted (if timeslice configured)
  - [ ] Chunks are stored internally

#### 3.2 Blob Creation
- [ ] Stop recording
- [ ] Check: `result.blob` is a `Blob` object
- [ ] **Expected:**
  - [ ] `result.blob.size > 0`
  - [ ] `result.blob.type` matches configured format
  - [ ] Blob is valid audio data

#### 3.3 File Object Conversion
- [ ] Check: `result.file` is a `File` object
- [ ] **Expected:**
  - [ ] `result.file.name` contains filename with extension
  - [ ] `result.file.size === result.blob.size`
  - [ ] `result.file.type === result.blob.type`
  - [ ] File can be used with FormData for upload

#### 3.4 Audio Playback
- [ ] Create audio element: `<audio src="${result.url}"></audio>`
- [ ] Play the audio
- [ ] **Expected:**
  - [ ] Audio plays without errors
  - [ ] Sound quality is clear
  - [ ] Duration matches recording duration
  - [ ] No distortion or artifacts

#### 3.5 Waveform Visualization
- [ ] Initialize visualizer: `const visualizer = new AudioVisualizer()`
- [ ] Get stream: `const stream = recorder.getStream()`
- [ ] Initialize: `await visualizer.initialize(stream)`
- [ ] Start visualization: `visualizer.start(callback)`
- [ ] **Expected:**
  - [ ] Callback receives waveform data
  - [ ] Data is `Uint8Array`
  - [ ] Data updates in real-time
  - [ ] Can draw on canvas using `drawWaveform()`

---

### ✅ Test 4: Audio Quality

#### 4.1 Noise Reduction
- [ ] Check browser constraints in code
- [ ] Verify: `echoCancellation: true`
- [ ] Verify: `noiseSuppression: true`
- [ ] Verify: `autoGainControl: true`
- [ ] **Expected:**
  - [ ] Browser applies noise reduction
  - [ ] Recorded audio has less background noise
  - [ ] Speech is clearer

#### 4.2 Optimal Recording Parameters
- [ ] Test with default config (128k, 44100Hz, mono)
- [ ] Test with high quality config (192k, 48000Hz, mono)
- [ ] **Expected:**
  - [ ] Both configurations work
  - [ ] Higher quality produces larger files
  - [ ] Audio quality is appropriate for speech

#### 4.3 Audio Validation
- [ ] Record short clip (< 0.1s)
- [ ] Call: `recorder.validateRecording(result)`
- [ ] **Expected:**
  - [ ] Returns `{ valid: false, errors: ['Recording is too short...'] }`
- [ ] Record normal clip (> 1s)
- [ ] Call: `recorder.validateRecording(result)`
- [ ] **Expected:**
  - [ ] Returns `{ valid: true, errors: [] }`

#### 4.4 Compression Recommendations
- [ ] Record large file (> 25MB if possible)
- [ ] Call: `getCompressionRecommendation(result.blob)`
- [ ] **Expected:**
  - [ ] Returns recommendation object
  - [ ] `needsCompression: true` if file is large
  - [ ] Helpful message about compression

---

### ✅ Test 5: Browser Compatibility

#### 5.1 Chrome/Edge Testing
- [ ] Test in Chrome 47+ or Edge
- [ ] **Expected:**
  - [ ] All features work
  - [ ] WebM format supported
  - [ ] Noise reduction works
  - [ ] Visualization works

#### 5.2 Firefox Testing
- [ ] Test in Firefox 25+
- [ ] **Expected:**
  - [ ] All features work
  - [ ] WebM format supported
  - [ ] May have different MIME type support

#### 5.3 Safari Testing
- [ ] Test in Safari 14.1+
- [ ] **Expected:**
  - [ ] All features work
  - [ ] May prefer different formats
  - [ ] May have different constraints support

#### 5.4 Format Fallback
- [ ] Test in different browsers
- [ ] Try unsupported format
- [ ] **Expected:**
  - [ ] Automatically falls back to supported format
  - [ ] Console shows warning
  - [ ] Recording still works

---

## Error Handling Testing

### Test Error Scenarios

1. **Permission Denied:**
   - [ ] Deny permission → Should show clear error
   - [ ] Error message explains how to enable

2. **No Microphone:**
   - [ ] Disconnect mic → Should detect and error
   - [ ] Error message is helpful

3. **Microphone In Use:**
   - [ ] Use mic in another app → Should detect conflict
   - [ ] Error message suggests closing other apps

4. **Invalid Configuration:**
   - [ ] Try invalid format → Should fall back
   - [ ] Try invalid sample rate → Should use default
   - [ ] Try to change config while recording → Should error

5. **Browser Not Supported:**
   - [ ] Test in old browser → Should detect and error
   - [ ] Error message suggests modern browser

---

## Integration Testing

### Test with Backend API

1. **Start Backend:**
   ```bash
   cd ../voice
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python main.py
   ```

2. **Test API Client:**
   ```typescript
   import { VoiceApiClient } from './src/index';
   
   const client = new VoiceApiClient({ baseUrl: 'http://localhost:8000' });
   
   // Test health check
   const health = await client.healthCheck();
   console.log('API Health:', health);
   
   // Test transcription
   const result = await recorder.stop();
   const transcript = await client.transcribe(result.file, result.file.name);
   console.log('Transcript:', transcript);
   ```

3. **Expected:**
   - [ ] Health check returns status
   - [ ] Transcription works (if API key configured)
   - [ ] Errors are handled gracefully

---

## Performance Testing

### Test Recording Duration Accuracy

1. Record for exactly 10 seconds (use external timer)
2. Check displayed duration
3. **Expected:** Within 0.5 seconds accuracy

### Test File Size

1. Record same duration with different bitrates:
   - 64k bitrate
   - 128k bitrate
   - 192k bitrate
2. **Expected:**
   - Higher bitrate = larger file
   - File sizes are reasonable
   - Quality difference is noticeable

### Test Memory Usage

1. Record multiple times (10+ recordings)
2. Check browser memory usage (DevTools → Performance)
3. **Expected:**
   - No memory leaks
   - Old recordings are cleaned up
   - Memory usage stays stable

---

## Automated Testing

### Type Checking

```bash
npm run type-check
```

**Expected:** No TypeScript errors

### Build Test

```bash
npm run build
```

**Expected:**
- Build completes successfully
- `dist/` directory created
- No build errors or warnings

### Manual Test Script

Run in browser console:

```javascript
// Test 1: Check if AudioRecorder is available
console.log('AudioRecorder available:', typeof AudioRecorder !== 'undefined');

// Test 2: Check browser support
if (typeof AudioRecorder !== 'undefined') {
  console.log('MediaRecorder supported:', AudioRecorder.isSupported());
}

// Test 3: Create recorder instance
const recorder = new AudioRecorder();
console.log('Recorder created:', recorder);

// Test 4: Check initial state
console.log('Initial state:', recorder.getState());

// Test 5: Request permission
recorder.requestPermission()
  .then(() => console.log('✅ Permission granted'))
  .catch(err => console.error('❌ Permission error:', err));
```

---

## Success Criteria

Phase 2 is **working correctly** if:

- ✅ Can request microphone permission
- ✅ Can start/stop recording
- ✅ Can pause/resume recording
- ✅ Duration tracking is accurate
- ✅ Audio playback works
- ✅ File info is accurate
- ✅ Configuration options work
- ✅ Error handling works for all scenarios
- ✅ No console errors during normal use
- ✅ Works in multiple browsers
- ✅ Can integrate with backend API
- ✅ Waveform visualization works
- ✅ Audio validation works
- ✅ Memory is properly managed

---

## Common Issues & Solutions

### Issue: "MediaRecorder is not supported"

**Solution:**
- Use modern browser (Chrome 47+, Firefox 25+, Safari 14.1+)
- Check browser console for specific error

### Issue: "Permission denied"

**Solution:**
1. Check browser settings → Privacy → Microphone
2. Ensure site has permission
3. Try refreshing page
4. Check if microphone is in use by another app

### Issue: "Format not supported"

**Solution:**
- This is normal - module automatically falls back
- Check console for which format is being used
- WebM is most widely supported

### Issue: "Cannot connect to API"

**Solution:**
1. Ensure backend is running: `cd ../voice && python main.py`
2. Check CORS settings in backend
3. Verify API URL matches backend URL
4. Check browser console for specific error

---

## Reporting Test Results

After testing, document:

1. **Browser & Version:** e.g., "Chrome 120.0.0.0"
2. **Operating System:** e.g., "macOS 14.0"
3. **Test Results:** Pass/Fail for each test
4. **Issues Found:** List any bugs or problems
5. **Performance:** File sizes, duration accuracy, etc.

---

## Next Steps

Once all tests pass:

1. ✅ Phase 2 is complete
2. ✅ Ready for Phase 3 (Transcription Service)
3. ✅ Can integrate into main application
4. ✅ Can customize UI/UX as needed

---

**Happy Testing! 🧪🎤**

