/**
 * Vapi AI Interviewer Integration
 * High-level interface for real-time AI interviewer using Vapi
 */

import { VapiStreamingClient, VapiStreamingConfig, VapiStreamingCallbacks } from './vapi-streaming-client';
import { AudioRecorder } from './audio-recorder';

export interface InterviewerConfig {
  vapiApiKey: string;
  assistantId: string;
  baseUrl?: string;
}

export interface InterviewerCallbacks {
  onTranscript?: (text: string, isFinal: boolean) => void;
  onAssistantMessage?: (message: string) => void;
  onError?: (error: Error) => void;
  onCallStart?: (callId: string) => void;
  onCallEnd?: () => void;
}

export class VapiInterviewer {
  private config: InterviewerConfig;
  private callbacks: InterviewerCallbacks;
  private streamingClient: VapiStreamingClient | null = null;
  private audioRecorder: AudioRecorder | null = null;
  private audioStream: MediaStream | null = null;

  constructor(config: InterviewerConfig, callbacks: InterviewerCallbacks = {}) {
    this.config = config;
    this.callbacks = callbacks;
  }

  /**
   * Start the interview
   */
  async startInterview(): Promise<string> {
    try {
      // Request microphone access
      this.audioStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });

      // Create streaming client
      const streamingConfig: VapiStreamingConfig = {
        apiKey: this.config.vapiApiKey,
        assistantId: this.config.assistantId,
        baseUrl: this.config.baseUrl,
      };

      const streamingCallbacks: VapiStreamingCallbacks = {
        onTranscript: (text, isFinal) => {
          // Only show user transcripts (not assistant)
          if (isFinal) {
            this.callbacks.onTranscript?.(text, isFinal);
          }
        },
        onMessage: (message) => {
          // Handle assistant messages
          if (message.role === 'assistant' && message.content) {
            this.callbacks.onAssistantMessage?.(message.content);
          }
        },
        onError: (error) => {
          this.callbacks.onError?.(error);
        },
        onCallStart: (callId) => {
          this.callbacks.onCallStart?.(callId);
        },
        onCallEnd: () => {
          this.callbacks.onCallEnd?.();
        },
      };

      this.streamingClient = new VapiStreamingClient(streamingConfig, streamingCallbacks);

      // Start the call
      const callId = await this.streamingClient.startCall(this.audioStream);
      return callId;
    } catch (error) {
      this.callbacks.onError?.(error instanceof Error ? error : new Error(String(error)));
      throw error;
    }
  }

  /**
   * Stop the interview
   */
  async stopInterview(): Promise<void> {
    if (this.streamingClient) {
      await this.streamingClient.stopCall();
      this.streamingClient = null;
    }

    if (this.audioStream) {
      this.audioStream.getTracks().forEach(track => track.stop());
      this.audioStream = null;
    }
  }

  /**
   * Check if interview is active
   */
  get isActive(): boolean {
    return this.streamingClient?.connected || false;
  }

  /**
   * Get current call ID
   */
  get callId(): string | null {
    return this.streamingClient?.currentCallId || null;
  }
}

