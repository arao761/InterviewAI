/**
 * Audio Recorder Configuration
 * Optimal settings for browser-based audio recording
 */

export interface AudioRecorderConfig {
  /** Audio format: 'webm', 'wav', or 'mp3' */
  format: 'webm' | 'wav' | 'mp3';
  
  /** Audio bitrate in kbps (e.g., '128k', '192k', '256k') */
  bitrate: string;
  
  /** Sample rate in Hz (e.g., 44100, 48000) */
  sampleRate: number;
  
  /** Number of audio channels (1 = mono, 2 = stereo) */
  channels: 1 | 2;
  
  /** MIME type for MediaRecorder */
  mimeType?: string;
  
  /** Time slice for data chunks in milliseconds (0 = no chunks) */
  timeslice?: number;
}

/**
 * Default configuration optimized for speech recording
 */
export const DEFAULT_CONFIG: AudioRecorderConfig = {
  format: 'webm',
  bitrate: '128k',
  sampleRate: 44100,
  channels: 1, // Mono is sufficient for speech
  timeslice: 0, // Record as single blob
};

/**
 * Predefined configurations for different use cases
 */
export const RECORDING_PRESETS = {
  /** High quality speech recording (recommended for interviews) */
  SPEECH_HIGH_QUALITY: {
    format: 'webm' as const,
    bitrate: '192k',
    sampleRate: 48000,
    channels: 1 as const,
  },
  
  /** Standard quality speech recording (balanced) */
  SPEECH_STANDARD: {
    format: 'webm' as const,
    bitrate: '128k',
    sampleRate: 44100,
    channels: 1 as const,
  },
  
  /** Low bandwidth speech recording */
  SPEECH_LOW_BANDWIDTH: {
    format: 'webm' as const,
    bitrate: '64k',
    sampleRate: 22050,
    channels: 1 as const,
  },
  
  /** High quality music/audio recording */
  MUSIC_HIGH_QUALITY: {
    format: 'webm' as const,
    bitrate: '256k',
    sampleRate: 48000,
    channels: 2 as const,
  },
  
  /** WAV format (uncompressed, larger files) */
  WAV_UNCOMPRESSED: {
    format: 'wav' as const,
    bitrate: '1411k', // CD quality
    sampleRate: 44100,
    channels: 1 as const,
  },
} as const;

/**
 * Get MIME type based on format and browser support
 * @param format Audio format
 * @returns MIME type string or null if not supported
 */
export function getMimeType(format: 'webm' | 'wav' | 'mp3'): string | null {
  const mimeTypes: Record<string, string[]> = {
    webm: [
      'audio/webm;codecs=opus',
      'audio/webm',
      'audio/webm;codecs=vorbis',
    ],
    wav: [
      'audio/wav',
      'audio/wave',
    ],
    mp3: [
      'audio/mpeg',
      'audio/mp3',
    ],
  };

  const types = mimeTypes[format] || [];
  
  // Check browser support
  for (const mimeType of types) {
    if (MediaRecorder.isTypeSupported(mimeType)) {
      return mimeType;
    }
  }
  
  return null;
}

/**
 * Get the best supported format for the current browser
 * @returns Best supported format
 */
export function getBestSupportedFormat(): 'webm' | 'wav' | 'mp3' {
  // Check formats in order of preference
  const formats: Array<'webm' | 'wav' | 'mp3'> = ['webm', 'wav', 'mp3'];
  
  for (const format of formats) {
    if (getMimeType(format)) {
      return format;
    }
  }
  
  // Fallback to webm (most browsers support it)
  return 'webm';
}

/**
 * Validate and normalize configuration
 * @param config User configuration
 * @returns Validated and normalized configuration
 */
export function normalizeConfig(
  config: Partial<AudioRecorderConfig> = {}
): AudioRecorderConfig {
  const normalized = { ...DEFAULT_CONFIG, ...config };
  
  // Ensure format is supported
  const supportedFormat = getBestSupportedFormat();
  if (!getMimeType(normalized.format)) {
    console.warn(
      `Format ${normalized.format} not supported, using ${supportedFormat}`
    );
    normalized.format = supportedFormat;
  }
  
  // Get MIME type
  normalized.mimeType = getMimeType(normalized.format) || undefined;
  
  // Validate sample rate (common values: 8000, 16000, 22050, 44100, 48000)
  const validSampleRates = [8000, 16000, 22050, 44100, 48000];
  if (!validSampleRates.includes(normalized.sampleRate)) {
    console.warn(
      `Sample rate ${normalized.sampleRate} may not be supported, using 44100`
    );
    normalized.sampleRate = 44100;
  }
  
  // Validate channels
  if (normalized.channels !== 1 && normalized.channels !== 2) {
    console.warn(`Invalid channels ${normalized.channels}, using 1`);
    normalized.channels = 1;
  }
  
  return normalized;
}

