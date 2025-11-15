/**
 * Vapi Real-Time Streaming Client
 * Handles real-time audio streaming to Vapi for AI interviewer
 */

export interface VapiStreamingConfig {
  apiKey: string;
  assistantId: string;
  baseUrl?: string;
}

export interface VapiStreamingCallbacks {
  onTranscript?: (text: string, isFinal: boolean) => void;
  onMessage?: (message: any) => void;
  onError?: (error: Error) => void;
  onCallStart?: (callId: string) => void;
  onCallEnd?: () => void;
}

export class VapiStreamingClient {
  private apiKey: string;
  private assistantId: string;
  private baseUrl: string;
  private ws: WebSocket | null = null;
  private mediaRecorder: MediaRecorder | null = null;
  private audioStream: MediaStream | null = null;
  private callbacks: VapiStreamingCallbacks;
  private callId: string | null = null;
  private isConnected: boolean = false;

  constructor(config: VapiStreamingConfig, callbacks: VapiStreamingCallbacks = {}) {
    this.apiKey = config.apiKey;
    this.assistantId = config.assistantId;
    this.baseUrl = config.baseUrl || 'https://api.vapi.ai';
    this.callbacks = callbacks;
  }

  /**
   * Start a real-time call with Vapi
   */
  async startCall(audioStream: MediaStream): Promise<string> {
    try {
      // First, create a call via REST API
      const callResponse = await fetch(`${this.baseUrl}/call`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          assistantId: this.assistantId,
          type: 'web', // Web call (no phone number needed)
        }),
      });

      if (!callResponse.ok) {
        const error = await callResponse.json().catch(() => ({ message: 'Failed to create call' }));
        throw new Error(error.message || `HTTP ${callResponse.status}`);
      }

      const callData = await callResponse.json();
      this.callId = callData.id;

      if (!this.callId) {
        throw new Error('No call ID returned from Vapi');
      }

      // Get WebSocket URL from call data
      const wsUrl = callData.serverUrl || `wss://${this.baseUrl.replace('https://', '')}/call/${this.callId}/stream`;

      // Connect WebSocket for real-time streaming
      await this.connectWebSocket(wsUrl, audioStream);

      this.callbacks.onCallStart?.(this.callId);
      return this.callId;
    } catch (error) {
      this.callbacks.onError?.(error instanceof Error ? error : new Error(String(error)));
      throw error;
    }
  }

  /**
   * Connect WebSocket and stream audio
   */
  private async connectWebSocket(wsUrl: string, audioStream: MediaStream): Promise<void> {
    return new Promise((resolve, reject) => {
      this.audioStream = audioStream;

      // Create WebSocket connection
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log('Vapi WebSocket connected');
        this.isConnected = true;

        // Start streaming audio
        this.startAudioStreaming(audioStream);
        resolve();
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.handleMessage(data);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.callbacks.onError?.(new Error('WebSocket connection error'));
        reject(error);
      };

      this.ws.onclose = () => {
        console.log('WebSocket closed');
        this.isConnected = false;
        this.callbacks.onCallEnd?.();
      };
    });
  }

  /**
   * Start streaming audio chunks
   */
  private startAudioStreaming(audioStream: MediaStream): void {
    // Create MediaRecorder to capture audio chunks
    const options = {
      mimeType: 'audio/webm;codecs=opus',
      audioBitsPerSecond: 16000, // Lower bitrate for streaming
    };

    try {
      this.mediaRecorder = new MediaRecorder(audioStream, options);
    } catch (error) {
      // Fallback to default
      this.mediaRecorder = new MediaRecorder(audioStream);
    }

    this.mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0 && this.ws && this.ws.readyState === WebSocket.OPEN) {
        // Send audio chunk to Vapi
        // Vapi expects base64 encoded audio or binary
        const reader = new FileReader();
        reader.onloadend = () => {
          const base64Audio = (reader.result as string).split(',')[1];
          this.ws?.send(JSON.stringify({
            type: 'audio',
            audio: base64Audio,
          }));
        };
        reader.readAsDataURL(event.data);
      }
    };

    // Start recording with small chunks for real-time streaming
    this.mediaRecorder.start(100); // Send chunk every 100ms
  }

  /**
   * Handle messages from Vapi
   */
  private handleMessage(data: any): void {
    this.callbacks.onMessage?.(data);

    // Handle transcript messages
    if (data.type === 'transcript' || data.transcript) {
      const transcript = data.transcript || data.text || '';
      const isFinal = data.isFinal !== false;
      this.callbacks.onTranscript?.(transcript, isFinal);
    }

    // Handle user speech transcript
    if (data.type === 'user-speech' || data.role === 'user') {
      const transcript = data.text || data.content || '';
      this.callbacks.onTranscript?.(transcript, true);
    }
  }

  /**
   * Stop the call and cleanup
   */
  async stopCall(): Promise<void> {
    // Stop audio streaming
    if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
      this.mediaRecorder.stop();
    }

    // Stop audio stream
    if (this.audioStream) {
      this.audioStream.getTracks().forEach(track => track.stop());
      this.audioStream = null;
    }

    // Close WebSocket
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }

    // End call via API
    if (this.callId) {
      try {
        await fetch(`${this.baseUrl}/call/${this.callId}`, {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ ended: true }),
        });
      } catch (error) {
        console.error('Error ending call:', error);
      }
    }

    this.isConnected = false;
    this.callId = null;
  }

  /**
   * Check if currently connected
   */
  get connected(): boolean {
    return this.isConnected;
  }

  /**
   * Get current call ID
   */
  get currentCallId(): string | null {
    return this.callId;
  }
}

