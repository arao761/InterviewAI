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
  timeRemainingMinutes?: number;
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
  private lastAssistantMessage: string = '';
  private lastUserTranscript: string = '';

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

    // Add time management instructions
    prompt += `## Time Management\n`;
    if (ctx.duration) {
      prompt += `- Total interview duration: ${ctx.duration} minutes\n`;
    }
    if (ctx.timeRemainingMinutes !== undefined) {
      prompt += `- Time remaining: ${ctx.timeRemainingMinutes} minutes\n`;
      if (ctx.timeRemainingMinutes <= 5) {
        prompt += `- ⚠️ CRITICAL: Less than 5 minutes remaining! Begin wrapping up the interview NOW.\n`;
        prompt += `- Skip any remaining questions and ask the candidate if they have any final questions\n`;
        prompt += `- Provide a brief closing statement and thank them for their time\n`;
      } else if (ctx.timeRemainingMinutes <= 10) {
        prompt += `- ⚠️ WARNING: Less than 10 minutes remaining. Start transitioning to final questions.\n`;
        prompt += `- Focus on the most important remaining questions\n`;
        prompt += `- Keep follow-ups brief\n`;
      }
    }
    prompt += `\n`;

    // Add company-specific context for Oracle Global Industries
    if (ctx.company?.toLowerCase().includes('oracle')) {
      prompt += `## Company Context: Oracle Global Industries\n`;
      prompt += `Oracle Global Industries focuses on delivering enterprise software solutions for:\n`;
      prompt += `- Manufacturing and process industries\n`;
      prompt += `- Utilities (electric, gas, water)\n`;
      prompt += `- Construction and engineering\n`;
      prompt += `- Industrial manufacturing and automation\n\n`;
      prompt += `Oracle values:\n`;
      prompt += `- Innovation and technical excellence\n`;
      prompt += `- Customer-first mindset\n`;
      prompt += `- Collaboration and teamwork\n`;
      prompt += `- Continuous learning and growth\n`;
      prompt += `- Ownership and accountability\n\n`;
      prompt += `For this PRE-SCREENING interview, focus on:\n`;
      prompt += `- Understanding the candidate's background and how it aligns with Global Industries\n`;
      prompt += `- Assessing cultural fit and soft skills (communication, teamwork, problem-solving)\n`;
      prompt += `- Exploring their interest in Oracle and the Global Industries division\n`;
      prompt += `- Understanding their motivation for the software engineering intern role\n`;
      prompt += `- Discussing their academic projects, internships, or relevant experiences\n\n`;
    }

    // Add instructions based on interview type
    prompt += `## Instructions\n`;
    prompt += `- Start by greeting the candidate\n`;
    prompt += `- Ask questions naturally, one at a time\n`;
    prompt += `- Listen actively and ask follow-up questions when appropriate\n`;
    prompt += `- Provide brief acknowledgments of their responses\n`;

    // Different behavior based on interview type
    if (ctx.interviewType === 'technical') {
      prompt += `- IMPORTANT: This is a TECHNICAL interview. Focus on technical questions, whether it be coding or just technical.\n`;
      prompt += `- Briefly ask about their background, resume, or past experiences\n`;
      prompt += `- Ask technical questions\n`;
      prompt += `- Ask follow-up questions about technical concepts\n`;
    } else if (ctx.interviewType === 'behavioral') {
      prompt += `- This is a BEHAVIORAL interview. You can reference their background and experiences\n`;
      prompt += `- Ask about specific projects, roles, and situations from their resume\n`;
      prompt += `- Use the STAR method (Situation, Task, Action, Result) to probe deeper\n`;
      if (ctx.company?.toLowerCase().includes('oracle')) {
        prompt += `- For Oracle Global Industries pre-screening, ask about:\n`;
        prompt += `  * Why they're interested in Oracle and specifically Global Industries\n`;
        prompt += `  * How their background relates to enterprise software or industrial solutions\n`;
        prompt += `  * Examples of teamwork, problem-solving, and handling challenges\n`;
        prompt += `  * What they know about Oracle's products or the industries served (manufacturing, utilities, construction)\n`;
        prompt += `  * Their career goals and how this internship fits into them\n`;
        prompt += `  * Relevant coursework or projects related to databases, cloud, or enterprise systems\n`;
      }
    } else {
      prompt += `- This is a MIXED interview with both technical and behavioral questions\n`;
      prompt += `- For technical questions, focus only on technical concepts\n`;
      prompt += `- For behavioral questions, you can reference their background\n`;
    }

    prompt += `- IMPORTANT: Continuously monitor time and pace the interview accordingly\n`;
    prompt += `- When time is running low, gracefully wrap up the interview\n`;
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
            // Deduplicate user transcripts
            if (isFinal && text.trim() && text !== this.lastUserTranscript) {
              this.lastUserTranscript = text;
              this.callbacks.onTranscript?.(text, isFinal);
            } else if (!isFinal) {
              // Pass through interim transcripts without deduplication
              this.callbacks.onTranscript?.(text, isFinal);
            }
          } else if (message.role === 'assistant' && isFinal) {
            // Deduplicate assistant messages from transcript
            if (text.trim() && text !== this.lastAssistantMessage) {
              this.lastAssistantMessage = text;
              this.callbacks.onAssistantMessage?.(text);
            }
          }
        } else if (message.type === 'conversation-update') {
          // Handle conversation updates - but avoid duplicates
          const conversation = message.conversation || [];
          const lastMessage = conversation[conversation.length - 1];
          if (lastMessage && lastMessage.role === 'assistant' && lastMessage.content) {
            const content = lastMessage.content.trim();
            // Only trigger if this is a new message
            if (content && content !== this.lastAssistantMessage) {
              this.lastAssistantMessage = content;
              this.callbacks.onAssistantMessage?.(content);
            }
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
          }${this.config.context?.company ? ` at ${this.config.context.company}` : ''}. Are you ready to get started?`,
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

  /**
   * Update time remaining during the interview
   * Sends context update to assistant about remaining time
   */
  updateTimeRemaining(timeRemainingSeconds: number): void {
    if (!this.vapi || !this.isCallActive) {
      return;
    }

    const minutes = Math.floor(timeRemainingSeconds / 60);

    // Only send updates at key thresholds to avoid spam
    // Send at: 10min, 5min, 3min, 2min, 1min remaining
    const thresholds = [10, 5, 3, 2, 1];
    if (thresholds.includes(minutes)) {
      let timeMessage = '';

      if (minutes <= 2) {
        timeMessage = `URGENT: Only ${minutes} minute${minutes !== 1 ? 's' : ''} remaining in the interview. You must begin wrapping up NOW. Ask the candidate if they have any final questions, then provide a brief closing statement.`;
      } else if (minutes <= 5) {
        timeMessage = `CRITICAL: ${minutes} minutes remaining. Start transitioning to final questions and prepare to wrap up the interview.`;
      } else if (minutes <= 10) {
        timeMessage = `WARNING: ${minutes} minutes remaining. Focus on the most important questions and keep responses concise.`;
      }

      if (timeMessage) {
        console.log(`⏰ Sending time update to VAPI: ${minutes} minutes remaining`);
        this.vapi.send({
          type: 'add-message',
          message: {
            role: 'system',
            content: timeMessage,
          },
        });
      }
    }
  }
}
