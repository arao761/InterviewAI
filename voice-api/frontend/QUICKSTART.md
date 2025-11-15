# Phase 2 Quick Start Guide

Get the frontend audio recording component up and running in 5 minutes!

## Prerequisites

- Node.js 18+ installed
- Backend API running (optional, for full functionality)

## Step 1: Install Dependencies

```bash
cd frontend
npm install
```

## Step 2: Start Development Server

```bash
npm run dev
```

The server will start at **http://localhost:3000**

## Step 3: Test the Recorder

1. Open http://localhost:3000 in your browser
2. Click "Start Recording"
3. Grant microphone permission when prompted
4. Speak into your microphone
5. Click "Stop" when done
6. Preview your recording and see the file details

## Step 4: Test with Backend (Optional)

1. Start the backend API:
   ```bash
   cd ../voice
   source venv/bin/activate
   python main.py
   ```

2. The frontend will automatically try to connect to http://localhost:8000
3. After recording, it will attempt to transcribe (if endpoint is implemented)

## Configuration

You can adjust recording settings in the demo:
- **Format**: WebM, WAV, or MP3
- **Bitrate**: 64k to 256k
- **Sample Rate**: 8000 to 48000 Hz

## Troubleshooting

### "Microphone permission denied"
- Check browser settings
- Ensure microphone is not in use by another app
- Try a different browser

### "Cannot connect to API"
- Make sure backend is running on port 8000
- Check CORS settings in backend
- Verify API_BASE_URL in demo.ts

### "Format not supported"
- The module will automatically fall back to a supported format
- Check browser console for warnings

## Next Steps

- Read the full [README.md](./README.md) for detailed documentation
- Check [PHASE2_SUMMARY.md](./PHASE2_SUMMARY.md) for feature overview
- Integrate the AudioRecorder class into your application

## Example Integration

```typescript
import { AudioRecorder } from './src/audio-recorder';

const recorder = new AudioRecorder();
await recorder.requestPermission();
await recorder.start();
// ... record ...
const result = await recorder.stop();
console.log('Recording:', result);
```

That's it! You're ready to record audio in the browser! 🎤

