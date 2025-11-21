/**
 * Vapi AI Interviewer Integration
 * High-level interface for real-time AI interviewer using official Vapi SDK
 */

import Vapi from '@vapi-ai/web';

export interface InterviewerConfig {
  vapiApiKey: string;
  assistantId: string;
}

export interface InterviewerCallbacks {
  onTranscript?: (text: string, isFinal: boolean) => void;
  onAssistantMessage?: (message: string) => void;
  onError?: (error: Error) => void;
  onCallStart?: () => void;
  onCallEnd?: () => void;
  onSpeechStart?: () => void;
  onSpeechEnd?: () => void;
}

export class VapiInterviewer {
  private config: InterviewerConfig;
  private callbacks: InterviewerCallbacks;
  private vapi: Vapi | null = null;
  private isCallActive: boolean = false;

  constructor(config: InterviewerConfig, callbacks: InterviewerCallbacks = {}) {
    this.config = config;
    this.callbacks = callbacks;
  }

  /**
   * Start the interview
   */
  async startInterview(): Promise<void> {
    try {
      // Create Vapi instance with API key
      this.vapi = new Vapi(this.config.vapiApiKey);

      // Set up event listeners
      this.vapi.on('call-start', () => {
        console.log('VAPI call started');
        this.isCallActive = true;
        this.callbacks.onCallStart?.();
      });

      this.vapi.on('call-end', () => {
        console.log('VAPI call ended');
        this.isCallActive = false;
        this.callbacks.onCallEnd?.();
      });

      this.vapi.on('speech-start', () => {
        this.callbacks.onSpeechStart?.();
      });

      this.vapi.on('speech-end', () => {
        this.callbacks.onSpeechEnd?.();
      });

      this.vapi.on('message', (message: any) => {
        // Handle different message types
        if (message.type === 'transcript') {
          const text = message.transcript || '';
          const isFinal = message.transcriptType === 'final';

          if (message.role === 'user') {
            this.callbacks.onTranscript?.(text, isFinal);
          } else if (message.role === 'assistant' && isFinal) {
            this.callbacks.onAssistantMessage?.(text);
          }
        } else if (message.type === 'conversation-update') {
          // Handle conversation updates
          const conversation = message.conversation || [];
          const lastMessage = conversation[conversation.length - 1];
          if (lastMessage && lastMessage.role === 'assistant') {
            this.callbacks.onAssistantMessage?.(lastMessage.content);
          }
        }
      });

      this.vapi.on('error', (error: any) => {
        console.error('VAPI error:', error);
        this.callbacks.onError?.(error instanceof Error ? error : new Error(String(error.message || error)));
      });

      // Start the call with the assistant
      await this.vapi.start(this.config.assistantId);

    } catch (error) {
      console.error('Error starting VAPI interview:', error);
      this.callbacks.onError?.(error instanceof Error ? error : new Error(String(error)));
      throw error;
    }
  }

  /**
   * Stop the interview
   */
  async stopInterview(): Promise<void> {
    if (this.vapi) {
      this.vapi.stop();
      this.vapi = null;
    }
    this.isCallActive = false;
  }

  /**
   * Check if interview is active
   */
  get isActive(): boolean {
    return this.isCallActive;
  }

  /**
   * Send a message to the assistant (for context)
   */
  send(message: any): void {
    if (this.vapi) {
      this.vapi.send(message);
    }
  }
}
