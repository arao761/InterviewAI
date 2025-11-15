/**
 * Audio Waveform Visualizer
 * Creates real-time waveform visualization during recording
 */

export interface WaveformData {
  data: Uint8Array;
  timestamp: number;
}

export class AudioVisualizer {
  private audioContext: AudioContext | null = null;
  private analyser: AnalyserNode | null = null;
  private dataArray: Uint8Array<ArrayBuffer> | null = null;
  private animationFrameId: number | null = null;
  private stream: MediaStream | null = null; // Stored for cleanup
  private source: MediaStreamAudioSourceNode | null = null;
  private onUpdateCallback: ((data: WaveformData) => void) | null = null;

  /**
   * Initialize visualizer with audio stream
   */
  async initialize(stream: MediaStream): Promise<void> {
    this.stream = stream; // Store for cleanup
    
    // Create audio context
    this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    
    // Create analyser node
    this.analyser = this.audioContext.createAnalyser();
    this.analyser.fftSize = 256; // Lower for smoother visualization
    this.analyser.smoothingTimeConstant = 0.8;
    
    // Create source from stream
    this.source = this.audioContext.createMediaStreamSource(stream);
    this.source.connect(this.analyser);
    
    // Create data array
    const bufferLength = this.analyser.frequencyBinCount;
    this.dataArray = new Uint8Array(new ArrayBuffer(bufferLength));
  }

  /**
   * Start visualization updates
   */
  start(callback: (data: WaveformData) => void): void {
    if (!this.analyser || !this.dataArray) {
      throw new Error('Visualizer not initialized. Call initialize() first.');
    }

    this.onUpdateCallback = callback;
    this.update();
  }

  /**
   * Stop visualization updates
   */
  stop(): void {
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
    this.onUpdateCallback = null;
  }

  /**
   * Update loop for visualization
   */
  private update = (): void => {
    if (!this.analyser || !this.dataArray || !this.onUpdateCallback) {
      return;
    }

    // Get frequency data
    this.analyser.getByteFrequencyData(this.dataArray);
    
    // Call callback with data (create new array to avoid reference issues)
    const dataCopy = new Uint8Array(this.dataArray.length);
    for (let i = 0; i < this.dataArray.length; i++) {
      dataCopy[i] = this.dataArray[i];
    }
    this.onUpdateCallback({
      data: dataCopy as Uint8Array,
      timestamp: Date.now()
    });

    // Continue animation loop
    this.animationFrameId = requestAnimationFrame(this.update);
  };

  /**
   * Get current waveform data (one-time read)
   */
  getWaveformData(): Uint8Array | null {
    if (!this.analyser || !this.dataArray) {
      return null;
    }

    this.analyser.getByteFrequencyData(this.dataArray);
    // Create a copy to avoid reference issues
    const dataCopy = new Uint8Array(this.dataArray.length);
    for (let i = 0; i < this.dataArray.length; i++) {
      dataCopy[i] = this.dataArray[i];
    }
    return dataCopy as Uint8Array;
  }

  /**
   * Get average volume level (0-100)
   */
  getVolumeLevel(): number {
    if (!this.analyser || !this.dataArray) {
      return 0;
    }

    this.analyser.getByteFrequencyData(this.dataArray);
    
    let sum = 0;
    for (let i = 0; i < this.dataArray.length; i++) {
      sum += this.dataArray[i];
    }
    
    return Math.round((sum / this.dataArray.length / 255) * 100);
  }

  /**
   * Clean up resources
   */
  release(): void {
    this.stop();
    
    if (this.source) {
      this.source.disconnect();
      this.source = null;
    }
    
    if (this.audioContext && this.audioContext.state !== 'closed') {
      this.audioContext.close();
    }
    
    // Clean up stream tracks
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }
    
    this.analyser = null;
    this.dataArray = null;
  }
}

/**
 * Draw waveform on canvas
 */
export function drawWaveform(
  canvas: HTMLCanvasElement,
  data: Uint8Array,
  options: {
    color?: string;
    lineWidth?: number;
    backgroundColor?: string;
  } = {}
): void {
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const { color = '#667eea', lineWidth = 2, backgroundColor = 'transparent' } = options;
  const width = canvas.width;
  const height = canvas.height;

  // Clear canvas
  ctx.fillStyle = backgroundColor;
  ctx.fillRect(0, 0, width, height);

  // Draw waveform
  ctx.strokeStyle = color;
  ctx.lineWidth = lineWidth;
  ctx.beginPath();

  const sliceWidth = width / data.length;
  let x = 0;

  for (let i = 0; i < data.length; i++) {
    const v = data[i] / 255.0;
    const y = (v * height) / 2;

    if (i === 0) {
      ctx.moveTo(x, height / 2 - y);
    } else {
      ctx.lineTo(x, height / 2 - y);
    }

    x += sliceWidth;
  }

  ctx.lineTo(width, height / 2);
  ctx.stroke();
}

/**
 * Draw volume meter
 */
export function drawVolumeMeter(
  canvas: HTMLCanvasElement,
  volume: number,
  options: {
    color?: string;
    backgroundColor?: string;
    maxVolume?: number;
  } = {}
): void {
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const { color = '#27ae60', backgroundColor = '#f0f0f0', maxVolume = 100 } = options;
  const width = canvas.width;
  const height = canvas.height;

  // Clear canvas
  ctx.fillStyle = backgroundColor;
  ctx.fillRect(0, 0, width, height);

  // Draw volume bar
  const volumeWidth = (volume / maxVolume) * width;
  ctx.fillStyle = color;
  ctx.fillRect(0, 0, volumeWidth, height);
}

