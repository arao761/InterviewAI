/**
 * Audio Recorder Module
 * Handles browser-based audio recording with MediaRecorder API
 */

import {
  AudioRecorderConfig,
  normalizeConfig,
  getMimeType,
} from './audio-recorder-config';

export type RecordingState = 'idle' | 'requesting' | 'recording' | 'paused' | 'stopped' | 'error';

export interface RecordingEvent {
  type: 'start' | 'stop' | 'pause' | 'resume' | 'dataavailable' | 'error' | 'statechange';
  data?: Blob;
  error?: Error;
  state?: RecordingState;
}

export interface RecordingResult {
  blob: Blob;
  file: File;
  url: string;
  duration: number;
  format: string;
  size: number;
}

/**
 * Audio Recorder Class
 * Manages audio recording from user's microphone
 */
export class AudioRecorder {
  private mediaRecorder: MediaRecorder | null = null;
  private audioStream: MediaStream | null = null;
  private config: AudioRecorderConfig;
  private state: RecordingState = 'idle';
  private chunks: Blob[] = [];
  private startTime: number = 0;
  private duration: number = 0;
  private eventListeners: Map<string, Set<(event: RecordingEvent) => void>> = new Map();

  constructor(config: Partial<AudioRecorderConfig> = {}) {
    this.config = normalizeConfig(config);
  }

  /**
   * Check if MediaRecorder API is supported
   */
  static isSupported(): boolean {
    return (
      typeof MediaRecorder !== 'undefined' &&
      typeof navigator !== 'undefined' &&
      typeof navigator.mediaDevices !== 'undefined' &&
      typeof navigator.mediaDevices.getUserMedia !== 'undefined'
    );
  }

  /**
   * Request microphone permission and initialize audio stream
   */
  async requestPermission(): Promise<MediaStream> {
    if (!AudioRecorder.isSupported()) {
      throw new Error(
        'MediaRecorder API is not supported in this browser. Please use a modern browser.'
      );
    }

    this.setState('requesting');

    try {
      // Request audio permissions with optimal constraints for noise reduction
      const constraints: MediaStreamConstraints = {
        audio: {
          sampleRate: this.config.sampleRate,
          channelCount: this.config.channels,
          echoCancellation: true,      // Browser-level noise reduction
          noiseSuppression: true,       // Browser-level noise reduction
          autoGainControl: true,        // Automatic volume adjustment
          // Chrome-specific quality settings (will be ignored in other browsers)
          ...(typeof (navigator.mediaDevices.getSupportedConstraints as any) === 'function' && {
            googEchoCancellation: true,   // Chrome-specific echo cancellation
            googNoiseSuppression: true,    // Chrome-specific noise suppression
            googAutoGainControl: true,     // Chrome-specific auto gain
            googHighpassFilter: true,     // Chrome-specific high-pass filter
            googTypingNoiseDetection: true, // Chrome-specific typing noise detection
          } as any),
        },
      };

      this.audioStream = await navigator.mediaDevices.getUserMedia(constraints);
      this.setState('idle');
      return this.audioStream;
    } catch (error) {
      this.setState('error');
      const err = error as Error;
      
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        throw new Error(
          'Microphone permission denied. Please allow microphone access and try again.'
        );
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        throw new Error('No microphone found. Please connect a microphone and try again.');
      } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
        throw new Error(
          'Microphone is already in use by another application. Please close other applications and try again.'
        );
      } else {
        throw new Error(`Failed to access microphone: ${err.message}`);
      }
    }
  }

  /**
   * Initialize MediaRecorder with optimal settings
   */
  private initializeMediaRecorder(): void {
    if (!this.audioStream) {
      throw new Error('Audio stream not initialized. Call requestPermission() first.');
    }

    // Get supported MIME type
    const mimeType = this.config.mimeType || getMimeType(this.config.format);
    
    if (!mimeType) {
      throw new Error(
        `Audio format ${this.config.format} is not supported in this browser.`
      );
    }

    // Create MediaRecorder with optimal settings
    const options: MediaRecorderOptions & { timeslice?: number } = {
      mimeType: mimeType,
      audioBitsPerSecond: this.parseBitrate(this.config.bitrate),
    };

    // Add timeslice if specified (for chunked recording)
    if (this.config.timeslice && this.config.timeslice > 0) {
      options.timeslice = this.config.timeslice;
    }

    try {
      this.mediaRecorder = new MediaRecorder(this.audioStream, options);
      this.setupEventHandlers();
    } catch (error) {
      const err = error as Error;
      throw new Error(`Failed to create MediaRecorder: ${err.message}`);
    }
  }

  /**
   * Setup event handlers for MediaRecorder
   */
  private setupEventHandlers(): void {
    if (!this.mediaRecorder) return;

    this.mediaRecorder.ondataavailable = (event: BlobEvent) => {
      if (event.data && event.data.size > 0) {
        this.chunks.push(event.data);
        this.emit('dataavailable', { data: event.data });
      }
    };

    this.mediaRecorder.onstart = () => {
      this.startTime = Date.now();
      this.emit('start');
    };

    this.mediaRecorder.onstop = () => {
      this.duration = (Date.now() - this.startTime) / 1000;
      this.emit('stop');
    };

    this.mediaRecorder.onerror = () => {
      const error = new Error('MediaRecorder error occurred');
      this.setState('error');
      this.emit('error', { error });
    };
  }

  /**
   * Start recording
   */
  async start(): Promise<void> {
    try {
      // Request permission if not already done
      if (!this.audioStream) {
        await this.requestPermission();
      }

      // Initialize MediaRecorder if not already done
      if (!this.mediaRecorder) {
        this.initializeMediaRecorder();
      }

      // Reset chunks for new recording
      this.chunks = [];
      this.duration = 0;

      // Start recording
      if (this.mediaRecorder && this.mediaRecorder.state === 'inactive') {
        if (this.config.timeslice && this.config.timeslice > 0) {
          this.mediaRecorder.start(this.config.timeslice);
        } else {
          this.mediaRecorder.start();
        }
        this.setState('recording');
      }
    } catch (error) {
      this.setState('error');
      throw error;
    }
  }

  /**
   * Pause recording
   */
  pause(): void {
    if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
      this.mediaRecorder.pause();
      this.duration += (Date.now() - this.startTime) / 1000;
      this.setState('paused');
      this.emit('pause');
    }
  }

  /**
   * Resume recording
   */
  resume(): void {
    if (this.mediaRecorder && this.mediaRecorder.state === 'paused') {
      this.mediaRecorder.resume();
      this.startTime = Date.now();
      this.setState('recording');
      this.emit('resume');
    }
  }

  /**
   * Stop recording and return result
   */
  async stop(): Promise<RecordingResult> {
    return new Promise((resolve, reject) => {
      if (!this.mediaRecorder) {
        reject(new Error('MediaRecorder not initialized'));
        return;
      }

      if (this.mediaRecorder.state === 'inactive') {
        reject(new Error('Recording is not active'));
        return;
      }

      // Handle stop event - we'll use a one-time listener
      const stopHandler = () => {
        try {
          const blob = new Blob(this.chunks, { type: this.config.mimeType || 'audio/webm' });
          
          // Convert Blob to File object
          const filename = `recording_${Date.now()}.${this.config.format}`;
          const file = new File([blob], filename, {
            type: this.config.mimeType || 'audio/webm',
            lastModified: Date.now()
          });
          
          const url = URL.createObjectURL(blob);
          
          const result: RecordingResult = {
            blob,
            file,
            url,
            duration: this.duration,
            format: this.config.format,
            size: blob.size,
          };

          this.setState('stopped');
          resolve(result);
        } catch (error) {
          reject(error);
        }
      };

      // Temporarily replace stop handler, then restore original
      const originalOnStop = this.mediaRecorder.onstop;
      this.mediaRecorder.onstop = () => {
        stopHandler();
        // Restore original handler if it exists
        if (originalOnStop && this.mediaRecorder) {
          this.mediaRecorder.onstop = originalOnStop;
        } else if (this.mediaRecorder) {
          // Re-setup handlers
          this.setupEventHandlers();
        }
      };

      // Stop recording
      this.mediaRecorder.stop();
    });
  }

  /**
   * Get current recording state
   */
  getState(): RecordingState {
    return this.state;
  }

  /**
   * Get current recording duration in seconds
   */
  getDuration(): number {
    if (this.state === 'recording') {
      return this.duration + (Date.now() - this.startTime) / 1000;
    }
    return this.duration;
  }

  /**
   * Check if currently recording
   */
  isRecording(): boolean {
    return this.state === 'recording';
  }

  /**
   * Release resources and stop all tracks
   */
  release(): void {
    // Stop MediaRecorder
    if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
      try {
        this.mediaRecorder.stop();
      } catch (error) {
        // Ignore errors when stopping
      }
    }

    // Stop all audio tracks
    if (this.audioStream) {
      this.audioStream.getTracks().forEach((track) => {
        track.stop();
      });
      this.audioStream = null;
    }

    this.mediaRecorder = null;
    this.chunks = [];
    this.setState('idle');
  }

  /**
   * Add event listener
   */
  on(event: RecordingEvent['type'], callback: (event: RecordingEvent) => void): void {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, new Set());
    }
    this.eventListeners.get(event)!.add(callback);
  }

  /**
   * Remove event listener
   */
  off(event: RecordingEvent['type'], callback: (event: RecordingEvent) => void): void {
    this.eventListeners.get(event)?.delete(callback);
  }

  /**
   * Emit event to listeners
   */
  private emit(type: RecordingEvent['type'], data: Partial<RecordingEvent> = {}): void {
    const event: RecordingEvent = { type, ...data };
    this.eventListeners.get(type)?.forEach((callback) => {
      try {
        callback(event);
      } catch (error) {
        console.error('Error in event listener:', error);
      }
    });
  }

  /**
   * Set state and emit state change event
   */
  private setState(newState: RecordingState): void {
    if (this.state !== newState) {
      this.state = newState;
      this.emit('statechange', { state: newState });
    }
  }

  /**
   * Parse bitrate string to number (e.g., '128k' -> 128000)
   */
  private parseBitrate(bitrate: string): number {
    const match = bitrate.match(/^(\d+)([km]?)$/i);
    if (!match) {
      return 128000; // Default
    }

    const value = parseInt(match[1], 10);
    const unit = match[2].toLowerCase();

    if (unit === 'k') {
      return value * 1000;
    } else if (unit === 'm') {
      return value * 1000000;
    }

    return value;
  }

  /**
   * Get current configuration
   */
  getConfig(): AudioRecorderConfig {
    return { ...this.config };
  }

  /**
   * Get audio stream (for visualization)
   */
  getStream(): MediaStream | null {
    return this.audioStream;
  }

  /**
   * Validate audio before sending
   */
  validateRecording(result: RecordingResult): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    // Check file size
    if (result.size === 0) {
      errors.push('Recording is empty');
    }

    // Check duration
    if (result.duration < 0.1) {
      errors.push('Recording is too short (less than 0.1 seconds)');
    }

    // Check format
    if (!result.format || !['webm', 'wav', 'mp3'].includes(result.format)) {
      errors.push(`Invalid format: ${result.format}`);
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Update configuration (only if not recording)
   */
  updateConfig(config: Partial<AudioRecorderConfig>): void {
    if (this.state === 'recording' || this.state === 'paused') {
      throw new Error('Cannot update configuration while recording');
    }

    this.config = normalizeConfig({ ...this.config, ...config });
    
    // Release old resources if stream exists
    if (this.audioStream) {
      this.release();
    }
  }
}

