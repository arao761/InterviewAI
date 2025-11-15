/**
 * API Client for PrepWise Voice API
 * Handles communication with the backend API
 */

export interface ApiConfig {
  baseUrl: string;
  timeout?: number;
}

export interface TranscriptionResponse {
  status: string;
  transcript?: string;
  error?: string;
  metadata?: {
    duration_seconds?: number;
    format?: string;
    sample_rate?: number;
    channels?: number;
    model?: string;
    chunked?: boolean;
    num_chunks?: number;
  };
  timestamps?: {
    words?: Array<{
      word: string;
      start: number;
      end: number;
    }>;
    segments?: Array<{
      text: string;
      start: number;
      end: number;
    }>;
  };
  confidence?: {
    average?: number;
    word_level?: Array<{
      word: string;
      start: number;
      end: number;
      confidence?: number;
    }>;
  };
  request_metadata?: {
    filename?: string;
    file_size_bytes?: number;
    file_size_mb?: number;
    format?: string;
  };
}

export interface SynthesisResponse {
  status: string;
  audioUrl?: string;
  error?: string;
}

export class VoiceApiClient {
  private baseUrl: string;
  private timeout: number;

  constructor(config: ApiConfig) {
    this.baseUrl = config.baseUrl.replace(/\/$/, ''); // Remove trailing slash
    this.timeout = config.timeout || 30000; // 30 seconds default
  }

  /**
   * Check API health
   */
  async healthCheck(): Promise<{ status: string; ready: boolean }> {
    try {
      const response = await this.fetchWithTimeout(`${this.baseUrl}/health`);
      const data = await response.json();
      return {
        status: data.status || 'unknown',
        ready: data.ready_for_requests || false,
      };
    } catch (error) {
      throw new Error(`Health check failed: ${error}`);
    }
  }

  /**
   * Get API configuration
   */
  async getConfig(): Promise<any> {
    try {
      const response = await this.fetchWithTimeout(`${this.baseUrl}/config`);
      return await response.json();
    } catch (error) {
      throw new Error(`Failed to get config: ${error}`);
    }
  }

  /**
   * Transcribe audio file with advanced options
   */
  async transcribe(
    audioBlob: Blob,
    filename?: string,
    options?: {
      language?: string;
      responseFormat?: 'text' | 'json' | 'verbose_json' | 'srt' | 'vtt';
      includeTimestamps?: boolean;
      includeConfidence?: boolean;
      chunkLargeFiles?: boolean;
    }
  ): Promise<TranscriptionResponse> {
    try {
      const formData = new FormData();
      formData.append('file', audioBlob, filename || 'recording.webm');

      // Build query parameters
      const params = new URLSearchParams();
      if (options?.language) params.append('language', options.language);
      if (options?.responseFormat) params.append('response_format', options.responseFormat);
      if (options?.includeTimestamps !== undefined) {
        params.append('include_timestamps', options.includeTimestamps.toString());
      }
      if (options?.includeConfidence !== undefined) {
        params.append('include_confidence', options.includeConfidence.toString());
      }
      if (options?.chunkLargeFiles !== undefined) {
        params.append('chunk_large_files', options.chunkLargeFiles.toString());
      }

      const url = `${this.baseUrl}/transcribe${params.toString() ? '?' + params.toString() : ''}`;

      const response = await this.fetchWithTimeout(url, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ error: 'Unknown error' }));
        throw new Error(error.error || error.detail || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      return {
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }

  /**
   * Synthesize text to speech
   */
  async synthesize(text: string, voice?: string): Promise<SynthesisResponse> {
    try {
      const response = await this.fetchWithTimeout(`${this.baseUrl}/synthesize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, voice }),
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ error: 'Unknown error' }));
        throw new Error(error.error || error.detail || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      return {
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }

  /**
   * Fetch with timeout
   */
  private async fetchWithTimeout(
    url: string,
    options: RequestInit = {}
  ): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });
      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      clearTimeout(timeoutId);
      if (error instanceof Error && error.name === 'AbortError') {
        throw new Error('Request timeout');
      }
      throw error;
    }
  }
}

