/**
 * Vapi AI Interviewer Integration
 * High-level interface for real-time AI interviewer using official Vapi SDK
 */

import Vapi from '@vapi-ai/web';

export interface InterviewContext {
  resumeData?: any;
  questions?: any[];
  interviewType?: string;
  difficulty?: string;
  jobTitle?: string;
  company?: string;
  duration?: string;
}

export interface InterviewerConfig {
  vapiApiKey: string;
  assistantId: string;
  context?: InterviewContext;
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
   * Build the system prompt with interview context
   */
  private buildSystemPrompt(): string {
    const ctx = this.config.context;
    if (!ctx) {
      return '';
    }

    let prompt = `You are an AI interviewer conducting a ${ctx.interviewType || 'mixed'} interview.\n\n`;

    // Add interview details
    if (ctx.jobTitle || ctx.company) {
      prompt += `## Interview Details\n`;
      if (ctx.jobTitle) prompt += `- Position: ${ctx.jobTitle}\n`;
      if (ctx.company) prompt += `- Company: ${ctx.company}\n`;
      if (ctx.difficulty) prompt += `- Difficulty: ${ctx.difficulty}\n`;
      if (ctx.duration) prompt += `- Duration: ${ctx.duration} minutes\n`;
      prompt += `\n`;
    }

    // Add resume/candidate information
    if (ctx.resumeData) {
      prompt += `## Candidate Background\n`;
      if (ctx.resumeData.name) prompt += `- Name: ${ctx.resumeData.name}\n`;
      if (ctx.resumeData.email) prompt += `- Email: ${ctx.resumeData.email}\n`;
      if (ctx.resumeData.skills && ctx.resumeData.skills.length > 0) {
        prompt += `- Skills: ${ctx.resumeData.skills.join(', ')}\n`;
      }
      if (ctx.resumeData.experience && ctx.resumeData.experience.length > 0) {
        prompt += `\n### Work Experience\n`;
        ctx.resumeData.experience.forEach((exp: any) => {
          prompt += `- ${exp.title || exp.position} at ${exp.company} (${exp.duration || exp.dates})\n`;
          if (exp.description) prompt += `  ${exp.description}\n`;
        });
      }
      if (ctx.resumeData.education && ctx.resumeData.education.length > 0) {
        prompt += `\n### Education\n`;
        ctx.resumeData.education.forEach((edu: any) => {
          prompt += `- ${edu.degree} from ${edu.school || edu.institution} (${edu.year || edu.dates})\n`;
        });
      }
      prompt += `\n`;
    }

    // Add questions to ask
    if (ctx.questions && ctx.questions.length > 0) {
      prompt += `## Interview Questions\n`;
      prompt += `Ask these questions during the interview, adapting based on the conversation flow:\n\n`;
      ctx.questions.forEach((q: any, i: number) => {
        const questionText = q.question || q.text || q;
        prompt += `${i + 1}. ${questionText}\n`;
        if (q.type) prompt += `   (Type: ${q.type})\n`;
      });
      prompt += `\n`;
    }

    // Add instructions
    prompt += `## Instructions\n`;
    prompt += `- Start by greeting the candidate and introducing yourself\n`;
    prompt += `- Ask questions naturally, one at a time\n`;
    prompt += `- Listen actively and ask follow-up questions when appropriate\n`;
    prompt += `- Provide brief acknowledgments of their responses\n`;
    prompt += `- Reference their background when relevant to personalize the interview\n`;
    prompt += `- Keep track of time and pace the interview accordingly\n`;
    prompt += `- At the end, thank them and let them know next steps\n`;

    return prompt;
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

      // Build assistant overrides with context
      const systemPrompt = this.buildSystemPrompt();

      if (systemPrompt) {
        // Start with assistant overrides including the personalized system prompt
        // Use variableValues to pass context that can be used in assistant's prompt template
        // Or use firstMessage override for initial context
        await this.vapi.start(this.config.assistantId, {
          firstMessage: `Hello! I've reviewed your background and I'm ready to conduct your interview. ${
            this.config.context?.jobTitle ? `We'll be discussing the ${this.config.context.jobTitle} position` : ''
          }${this.config.context?.company ? ` at ${this.config.context.company}` : ''}. Let's get started!`,
          variableValues: {
            interviewContext: systemPrompt,
            candidateName: this.config.context?.resumeData?.name || 'Candidate',
            jobTitle: this.config.context?.jobTitle || 'the position',
            company: this.config.context?.company || 'our company',
            interviewType: this.config.context?.interviewType || 'mixed',
          },
        });
      } else {
        // Start without overrides
        await this.vapi.start(this.config.assistantId);
      }

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
