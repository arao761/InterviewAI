/**
 * PrepWise Voice Recorder - Core Module Exports
 * 
 * This module exports the core functionality for integration into your project.
 * The demo UI has been removed - use these modules directly in your application.
 */

// Export Audio Recorder
export { AudioRecorder } from './audio-recorder';
export type { RecordingState, RecordingEvent, RecordingResult } from './audio-recorder';

// Export Configuration
export { 
  DEFAULT_CONFIG,
  RECORDING_PRESETS,
  getMimeType,
  getBestSupportedFormat,
  normalizeConfig
} from './audio-recorder-config';
export type { AudioRecorderConfig } from './audio-recorder-config';

// Export API Client
export { VoiceApiClient } from './api-client';
export type { ApiConfig, TranscriptionResponse, SynthesisResponse } from './api-client';

// Export Audio Visualizer
export { AudioVisualizer, drawWaveform, drawVolumeMeter } from './audio-visualizer';
export type { WaveformData } from './audio-visualizer';

// Export Audio Compressor
export { 
  compressAudioBlob, 
  needsCompression, 
  getCompressionRecommendation 
} from './audio-compressor';
export type { CompressionOptions } from './audio-compressor';

