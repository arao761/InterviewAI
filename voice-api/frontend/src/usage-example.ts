/**
 * Usage Example - How to integrate PrepWise Voice Recorder
 * 
 * This file shows how to use the audio recorder and API client in your application.
 * Copy and adapt this code to integrate with your project.
 */

import { AudioRecorder } from './audio-recorder';
import { RECORDING_PRESETS } from './audio-recorder-config';
import { VoiceApiClient } from './api-client';
import { AudioVisualizer, drawWaveform } from './audio-visualizer';
import { getCompressionRecommendation } from './audio-compressor';

// Example 1: Basic Recording
export async function basicRecordingExample() {
  // Create recorder with default settings
  const recorder = new AudioRecorder();
  
  try {
    // Request microphone permission
    await recorder.requestPermission();
    
    // Start recording
    await recorder.start();
    
    // Record for some time...
    // (in your app, this would be triggered by user action)
    
    // Stop recording
    const result = await recorder.stop();
    
    console.log('Recording complete:', {
      duration: result.duration,
      size: result.size,
      format: result.format,
      url: result.url // Use this for audio playback
    });
    
    // Clean up
    recorder.release();
    
    return result;
  } catch (error) {
    console.error('Recording failed:', error);
    recorder.release();
    throw error;
  }
}

// Example 2: Recording with Transcription and Validation
export async function recordingWithTranscriptionExample() {
  const recorder = new AudioRecorder(RECORDING_PRESETS.SPEECH_HIGH_QUALITY);
  const apiClient = new VoiceApiClient({ baseUrl: 'http://localhost:8000' });
  
  try {
    await recorder.requestPermission();
    await recorder.start();
    
    // ... user records ...
    
    const result = await recorder.stop();
    
    // Validate recording
    const validation = recorder.validateRecording(result);
    if (!validation.valid) {
      throw new Error(`Recording validation failed: ${validation.errors.join(', ')}`);
    }
    
    // Check compression needs
    const compressionInfo = getCompressionRecommendation(result.blob);
    if (compressionInfo.needsCompression) {
      console.warn(compressionInfo.recommendedAction);
    }
    
    // Use File object (converted from Blob)
    const transcription = await apiClient.transcribe(result.file, result.file.name);
    
    if (transcription.status === 'success') {
      console.log('Transcript:', transcription.transcript);
      return {
        audio: result,
        transcript: transcription.transcript
      };
    } else {
      throw new Error(transcription.error || 'Transcription failed');
    }
  } catch (error) {
    console.error('Error:', error);
    throw error;
  } finally {
    recorder.release();
  }
}

// Example 3: Event-Based Recording
export function eventBasedRecordingExample() {
  const recorder = new AudioRecorder();
  
  // Set up event listeners
  recorder.on('start', () => {
    console.log('Recording started');
  });
  
  recorder.on('stop', () => {
    console.log('Recording stopped');
  });
  
  recorder.on('error', (event) => {
    console.error('Recording error:', event.error);
  });
  
  recorder.on('statechange', (event) => {
    console.log('State changed:', event.state);
  });
  
  // Use recorder...
  return recorder;
}

// Example 4: Custom Configuration
export function customConfigurationExample() {
  const recorder = new AudioRecorder({
    format: 'webm',
    bitrate: '192k',
    sampleRate: 48000,
    channels: 1
  });
  
  return recorder;
}

// Example 5: Recording with Waveform Visualization
export async function recordingWithVisualizationExample(canvas: HTMLCanvasElement) {
  const recorder = new AudioRecorder();
  const visualizer = new AudioVisualizer();
  
  try {
    await recorder.requestPermission();
    const stream = recorder.getStream();
    
    if (!stream) {
      throw new Error('No audio stream available');
    }
    
    // Initialize visualizer
    await visualizer.initialize(stream);
    
    // Start visualization
    visualizer.start((waveformData) => {
      drawWaveform(canvas, waveformData.data, {
        color: '#667eea',
        lineWidth: 2
      });
    });
    
    // Start recording
    await recorder.start();
    
    // ... user records ...
    
    // Stop visualization
    visualizer.stop();
    
    // Stop recording
    const result = await recorder.stop();
    
    return result;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  } finally {
    visualizer.release();
    recorder.release();
  }
}

// Example 6: Recording with Volume Monitoring
export async function recordingWithVolumeMonitoringExample(
  onVolumeUpdate: (volume: number) => void
) {
  const recorder = new AudioRecorder();
  const visualizer = new AudioVisualizer();
  
  try {
    await recorder.requestPermission();
    const stream = recorder.getStream();
    
    if (!stream) {
      throw new Error('No audio stream available');
    }
    
    await visualizer.initialize(stream);
    
    // Monitor volume
    const volumeInterval = setInterval(() => {
      const volume = visualizer.getVolumeLevel();
      onVolumeUpdate(volume);
    }, 100);
    
    await recorder.start();
    
    // ... user records ...
    
    clearInterval(volumeInterval);
    visualizer.stop();
    const result = await recorder.stop();
    
    return result;
  } finally {
    visualizer.release();
    recorder.release();
  }
}

