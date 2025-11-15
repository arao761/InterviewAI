# Phase 2 Testing Guide

Complete guide to test the Frontend Audio Recording Component.

## Prerequisites Check

Before testing, ensure you have:

- ✅ Node.js 18+ installed
- ✅ Modern browser (Chrome, Firefox, Safari, or Edge)
- ✅ Microphone connected/available
- ✅ Backend API running (optional, for full functionality)

## Quick Test (5 Minutes)

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

**Expected Output:**
- Dependencies installed successfully
- No errors in console

### Step 2: Start Development Server

```bash
npm run dev
```

**Expected Output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### Step 3: Open in Browser

1. Open http://localhost:3000
2. You should see the "PrepWise Voice Recorder" interface

### Step 4: Test Basic Recording

1. **Click "Start Recording"**
   - Browser should prompt for microphone permission
   - Status should change to "🔴 Recording..."
   - Duration counter should start incrementing

2. **Speak into microphone**
   - You should see the duration increasing
   - No errors in browser console

3. **Click "Stop"**
   - Status should change to "✅ Recording stopped"
   - Audio preview should appear
   - File size and format should be displayed

4. **Play the audio**
   - Click play on the audio player
   - You should hear your recording

## Comprehensive Testing Checklist

### ✅ Test 1: Browser Compatibility

- [ ] Test in Chrome/Edge
- [ ] Test in Firefox
- [ ] Test in Safari (if on Mac)
- [ ] Check console for errors

### ✅ Test 2: Microphone Permissions

**Test Permission Grant:**
- [ ] Click "Start Recording"
- [ ] Grant permission when prompted
- [ ] Recording should start successfully

**Test Permission Denial:**
- [ ] Click "Start Recording"
- [ ] Deny permission
- [ ] Should show clear error message
- [ ] Should explain how to enable permission

**Test Already Denied:**
- [ ] Deny permission in browser settings
- [ ] Try to record
- [ ] Should show helpful error message

### ✅ Test 3: Recording Controls

**Start Recording:**
- [ ] Button changes to disabled state
- [ ] Status shows "Recording..."
- [ ] Duration counter increments
- [ ] Pause button becomes enabled

**Pause Recording:**
- [ ] Click "Pause"
- [ ] Status shows "⏸ Paused"
- [ ] Duration stops incrementing
- [ ] Resume button becomes enabled

**Resume Recording:**
- [ ] Click "Resume"
- [ ] Status shows "Recording..."
- [ ] Duration continues from where it paused

**Stop Recording:**
- [ ] Click "Stop"
- [ ] Status shows "Recording stopped"
- [ ] Audio preview appears
- [ ] File info is displayed

### ✅ Test 4: Configuration Options

**Format Selection:**
- [ ] Change format to WebM → Record → Verify format
- [ ] Change format to WAV → Record → Verify format
- [ ] Change format to MP3 → Record → Verify format (if supported)

**Bitrate Selection:**
- [ ] Test different bitrates (64k, 128k, 192k, 256k)
- [ ] Verify file sizes differ appropriately
- [ ] Higher bitrate = larger file size

**Sample Rate Selection:**
- [ ] Test different sample rates
- [ ] Verify recording works with all options

**Note:** Configuration changes only work when recorder is idle

### ✅ Test 5: Error Handling

**No Microphone:**
- [ ] Disconnect microphone (if possible)
- [ ] Try to record
- [ ] Should show "No microphone found" error

**Microphone In Use:**
- [ ] Open another app using microphone
- [ ] Try to record
- [ ] Should show appropriate error message

**Format Not Supported:**
- [ ] Select unsupported format (if browser doesn't support it)
- [ ] Should automatically fall back to supported format
- [ ] Console should show warning

### ✅ Test 6: Audio Quality

**Record Short Clip:**
- [ ] Record 5-10 seconds
- [ ] Play back
- [ ] Audio should be clear
- [ ] No distortion or clipping

**Record Longer Clip:**
- [ ] Record 30+ seconds
- [ ] Verify duration is accurate
- [ ] Play back entire recording
- [ ] Audio should remain clear

### ✅ Test 7: Backend Integration (Optional)

**Prerequisites:**
- Backend API running on http://localhost:8000
- API keys configured

**Test Health Check:**
- [ ] Page loads
- [ ] Should show "API is ready!" message (if API is running)
- [ ] Or show connection error (if API is not running)

**Test Transcription (if endpoint implemented):**
- [ ] Record audio
- [ ] Stop recording
- [ ] Should attempt to transcribe
- [ ] Should show transcription result or appropriate message

## Automated Testing

### Run Type Checking

```bash
npm run type-check
```

**Expected:** No TypeScript errors

### Build for Production

```bash
npm run build
```

**Expected:**
- Build completes successfully
- `dist/` directory created
- No build errors

### Preview Production Build

```bash
npm run preview
```

**Expected:**
- Production build served
- All functionality works as in dev mode

## Browser Console Testing

Open browser DevTools (F12) and check:

### Console Messages

**On Load:**
- ✅ No errors
- ✅ API health check message (if backend running)

**During Recording:**
- ✅ No errors
- ✅ State change events logged (if event listeners added)

**On Stop:**
- ✅ Recording result logged
- ✅ File size and format displayed

### Network Tab

**Check API Calls:**
- ✅ Health check request to `/health`
- ✅ Transcription request to `/transcribe` (if implemented)
- ✅ All requests return appropriate status codes

## Manual Test Script

Run this in browser console to test programmatically:

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

## Common Issues & Solutions

### Issue: "npm install" fails

**Solution:**
```bash
# Clear cache and retry
rm -rf node_modules package-lock.json
npm install
```

### Issue: "Port 3000 already in use"

**Solution:**
```bash
# Use different port
npm run dev -- --port 3001
```

### Issue: Microphone not working

**Solutions:**
1. Check browser permissions in settings
2. Ensure microphone is not in use by another app
3. Try different browser
4. Check system microphone settings

### Issue: "Format not supported"

**Solution:**
- This is normal - module automatically falls back
- Check console for which format is being used
- WebM is most widely supported

### Issue: Cannot connect to API

**Solutions:**
1. Ensure backend is running: `cd ../voice && python main.py`
2. Check CORS settings in backend
3. Verify API URL in demo.ts matches backend URL
4. Check browser console for specific error

### Issue: TypeScript errors

**Solution:**
```bash
# Install TypeScript if missing
npm install -D typescript

# Run type check
npm run type-check
```

## Performance Testing

### Test Recording Duration Accuracy

1. Record for exactly 10 seconds (use timer)
2. Check displayed duration
3. Should be within 0.5 seconds accuracy

### Test File Size

1. Record same duration with different bitrates
2. Compare file sizes
3. Higher bitrate should produce larger files

### Test Memory Usage

1. Record multiple times
2. Check browser memory usage
3. Should not have memory leaks
4. Old recordings should be cleaned up

## Integration Testing

### Test with Backend API

1. **Start Backend:**
   ```bash
   cd ../voice
   source venv/bin/activate
   python main.py
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test Flow:**
   - Record audio
   - Stop recording
   - Verify transcription attempt
   - Check API logs for requests

## Success Criteria

Phase 2 is working correctly if:

- ✅ Can request microphone permission
- ✅ Can start/stop recording
- ✅ Audio playback works
- ✅ File info is accurate
- ✅ Configuration options work
- ✅ Error handling works
- ✅ No console errors
- ✅ Works in multiple browsers
- ✅ Can integrate with backend (if available)

## Next Steps After Testing

Once all tests pass:

1. ✅ Phase 2 is complete
2. ✅ Ready for Phase 3 (Transcription Service)
3. ✅ Can integrate into main application
4. ✅ Can customize UI/UX as needed

## Reporting Issues

If you find issues:

1. Check browser console for errors
2. Note browser and version
3. Note operating system
4. Describe steps to reproduce
5. Include error messages

Happy Testing! 🧪

