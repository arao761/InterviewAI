# PrepWise Voice Recorder - Integration Module

Core audio recording and transcription functionality for PrepWise interview preparation platform.

## Overview

This module provides browser-based audio recording and transcription capabilities. The demo UI has been removed - use the core modules directly in your application.

## Installation

```bash
npm install
```

## Core Modules

### AudioRecorder
Browser-based audio recording using MediaRecorder API with:
- Microphone permission handling
- Start/stop/pause/resume controls
- Duration tracking
- Error handling
- Audio validation
- Blob to File conversion
- Browser-level noise reduction

### AudioVisualizer
Real-time waveform visualization during recording:
- Waveform drawing on canvas
- Volume level monitoring
- Real-time audio analysis

### AudioCompressor
Audio compression utilities:
- Compression recommendations
- Size validation
- Client-side compression helpers

### VoiceApiClient
Client for communicating with the PrepWise Voice API backend.

### Configuration
Audio recording presets and configuration utilities.

## Quick Start

```typescript
import { AudioRecorder, AudioVisualizer, VoiceApiClient } from './src';

// Create recorder
const recorder = new AudioRecorder();

// Request permission and start recording
await recorder.requestPermission();
await recorder.start();

// Stop and get result (includes both Blob and File)
const result = await recorder.stop();

// Validate recording
const validation = recorder.validateRecording(result);
if (!validation.valid) {
  console.error('Validation errors:', validation.errors);
}

// Transcribe using API (can use result.file or result.blob)
const apiClient = new VoiceApiClient({ baseUrl: 'http://localhost:8000' });
const transcription = await apiClient.transcribe(result.file, result.file.name);
```

### With Waveform Visualization

```typescript
import { AudioRecorder, AudioVisualizer, drawWaveform } from './src';

const recorder = new AudioRecorder();
const visualizer = new AudioVisualizer();
const canvas = document.getElementById('waveform') as HTMLCanvasElement;

await recorder.requestPermission();
const stream = recorder.getStream();
if (stream) {
  await visualizer.initialize(stream);
  visualizer.start((data) => {
    drawWaveform(canvas, data.data);
  });
}

await recorder.start();
// ... record ...
await recorder.stop();
visualizer.stop();
```

## API Reference

### AudioRecorder

```typescript
const recorder = new AudioRecorder(config?: Partial<AudioRecorderConfig>);

// Methods
await recorder.requestPermission(): Promise<MediaStream>
await recorder.start(): Promise<void>
recorder.pause(): void
recorder.resume(): void
await recorder.stop(): Promise<RecordingResult>
recorder.release(): void
recorder.getState(): RecordingState
recorder.getDuration(): number
recorder.isRecording(): boolean

// Events
recorder.on('start', (event) => {})
recorder.on('stop', (event) => {})
recorder.on('pause', (event) => {})
recorder.on('resume', (event) => {})
recorder.on('error', (event) => {})
recorder.on('statechange', (event) => {})
```

### VoiceApiClient

```typescript
const client = new VoiceApiClient({ baseUrl: 'http://localhost:8000' });

// Methods
await client.healthCheck(): Promise<{ status: string; ready: boolean }>
await client.getConfig(): Promise<any>
await client.transcribe(audioBlob: Blob, filename?: string): Promise<TranscriptionResponse>
await client.synthesize(text: string, voice?: string): Promise<SynthesisResponse>
```

## Recording Presets

```typescript
import { RECORDING_PRESETS } from './src/audio-recorder-config';

RECORDING_PRESETS.SPEECH_HIGH_QUALITY    // Best for interviews
RECORDING_PRESETS.SPEECH_STANDARD         // Balanced quality
RECORDING_PRESETS.SPEECH_LOW_BANDWIDTH    // Minimal bandwidth
RECORDING_PRESETS.MUSIC_HIGH_QUALITY      // Stereo, high quality
RECORDING_PRESETS.WAV_UNCOMPRESSED        // Lossless quality
```

## Usage Examples

See `src/usage-example.ts` for complete integration examples.

## Integration

1. Import the modules you need:
   ```typescript
   import { AudioRecorder, VoiceApiClient } from './src';
   ```

2. Use in your components:
   ```typescript
   const recorder = new AudioRecorder();
   await recorder.requestPermission();
   await recorder.start();
   // ... user records ...
   const result = await recorder.stop();
   ```

3. Connect to backend:
   ```typescript
   const apiClient = new VoiceApiClient({ baseUrl: 'YOUR_API_URL' });
   const transcript = await apiClient.transcribe(result.blob);
   ```

## Browser Support

- Chrome/Edge 47+
- Firefox 25+
- Safari 14.1+
- Opera 27+

## Requirements

- Backend API running (for transcription)
- OpenAI API key configured in backend
- Modern browser with MediaRecorder support

## File Structure

```
src/
├── audio-recorder.ts          # Main AudioRecorder class
├── audio-recorder-config.ts   # Configuration and presets
├── audio-visualizer.ts        # Waveform visualization
├── audio-compressor.ts        # Audio compression utilities
├── api-client.ts              # Backend API client
├── index.ts                   # Module exports
└── usage-example.ts           # Integration examples
```

## Phase 2 Features Completed

### ✅ Browser Recording Setup
- JavaScript/TypeScript module for audio recording
- Microphone permission requests
- MediaRecorder initialization with optimal settings
- Audio format configuration (webm, wav, mp3)
- Bitrate and sample rate configuration

### ✅ Recording Controls
- Start recording function
- Stop recording function
- Pause/resume functionality
- Recording duration tracking
- Error handling (no mic, permissions denied)

### ✅ Audio Data Handling
- Collect audio chunks during recording
- Create Blob from recorded chunks
- Convert Blob to File object
- Audio playback support (via URL)
- Waveform visualization during recording

### ✅ Audio Quality
- Browser-level noise reduction (echo cancellation, noise suppression)
- Optimal recording parameters
- Audio file validation before sending
- Compression recommendations
- Browser compatibility handling

## Next Steps

1. Import the modules into your main application
2. Create your own UI components using the AudioRecorder
3. Integrate with your existing interview prep flow
4. Customize configuration as needed
