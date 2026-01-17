/**
 * Microsoft Foundry AI Interviewer Integration
 * Uses Microsoft Foundry (Azure AI Services) for AI responses
 * Uses Azure Speech Services for speech-to-text and text-to-speech
 */

// @ts-ignore - Azure Speech SDK types may not be fully compatible
import * as SpeechSDK from 'microsoft-cognitiveservices-speech-sdk';

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
  foundryEndpoint: string;
  foundryApiKey: string;
  deploymentName?: string; // Azure OpenAI deployment name (optional, for Azure OpenAI endpoint format)
  speechKey?: string;
  speechRegion?: string;
  speechEndpoint?: string; // Optional custom speech endpoint
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

export class FoundryInterviewer {
  private config: InterviewerConfig;
  private callbacks: InterviewerCallbacks;
  private isCallActive: boolean = false;
  private lastAssistantMessage: string = '';
  private lastUserTranscript: string = '';

  // Azure Speech Services
  private recognizer: SpeechSDK.SpeechRecognizer | null = null;
  private synthesizer: SpeechSDK.SpeechSynthesizer | null = null;
  private audioConfig: SpeechSDK.AudioConfig | null = null;
  private speechConfig: SpeechSDK.SpeechConfig | null = null;
  private synthesizerConfig: SpeechSDK.SpeechConfig | null = null;

  // Conversation history for context
  private conversationHistory: Array<{ role: 'user' | 'assistant' | 'system'; content: string }> = [];

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
   * Call Microsoft Foundry API for AI response
   */
  private async callFoundryAPI(userMessage: string): Promise<string> {
    try {
      // Build messages array for chat completion
      const messages: Array<{ role: 'user' | 'assistant' | 'system'; content: string }> = [];

      // Add system prompt if not already in conversation history
      if (this.conversationHistory.length === 0) {
        const systemPrompt = this.buildSystemPrompt();
        if (systemPrompt) {
          messages.push({ role: 'system', content: systemPrompt });
          this.conversationHistory.push({ role: 'system', content: systemPrompt });
        }
      }

      // Add conversation history
      messages.push(...this.conversationHistory.filter(msg => msg.role !== 'system'));

      // Add current user message
      messages.push({ role: 'user', content: userMessage });
      this.conversationHistory.push({ role: 'user', content: userMessage });

      // Build the endpoint URL
      // Support both Azure OpenAI format and Foundry format
      let endpointUrl: string;
      if (this.config.deploymentName) {
        // Azure OpenAI format: https://{resource}.openai.azure.com/openai/deployments/{deployment}/chat/completions
        endpointUrl = `${this.config.foundryEndpoint}/openai/deployments/${this.config.deploymentName}/chat/completions?api-version=2024-02-15-preview`;
      } else {
        // Foundry format: https://{foundry-endpoint}/chat/completions
        endpointUrl = `${this.config.foundryEndpoint}/chat/completions?api-version=2024-02-15-preview`;
      }

      // Call Microsoft Foundry/Azure OpenAI endpoint
      const response = await fetch(endpointUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'api-key': this.config.foundryApiKey,
        },
        body: JSON.stringify({
          messages: messages,
          temperature: 0.7,
          max_tokens: 500,
          stream: false,
        }),
      });

      if (!response.ok) {
        let errorText = '';
        try {
          const errorData = await response.json();
          errorText = errorData.error?.message || errorData.message || JSON.stringify(errorData);
        } catch {
          errorText = await response.text();
        }
        const errorMessage = `Foundry API error (${response.status}): ${errorText}`;
        console.error('FoundryInterviewer API Error:', errorMessage);
        throw new Error(errorMessage);
      }

      const data = await response.json();
      const assistantMessage = data.choices?.[0]?.message?.content || '';

      if (assistantMessage) {
        this.conversationHistory.push({ role: 'assistant', content: assistantMessage });
      }

      return assistantMessage;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      console.error('Error calling Foundry API:', errorMessage, error);
      throw new Error(`Failed to get AI response: ${errorMessage}`);
    }
  }

  /**
   * Handle recognized speech and get AI response
   */
  private async handleRecognizedSpeech(text: string): Promise<void> {
    if (!text.trim()) return;

    // Callback for transcript
    if (text.trim() !== this.lastUserTranscript) {
      this.lastUserTranscript = text.trim();
      this.callbacks.onTranscript?.(text.trim(), true);
    }

    // Get AI response from Foundry
    try {
      this.callbacks.onSpeechStart?.();
      const aiResponse = await this.callFoundryAPI(text.trim());

      if (aiResponse && aiResponse.trim() !== this.lastAssistantMessage) {
        this.lastAssistantMessage = aiResponse.trim();
        this.callbacks.onAssistantMessage?.(aiResponse.trim());

        // Synthesize and speak the response
        await this.speakText(aiResponse.trim());
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      console.error('Error handling recognized speech:', errorMessage, error);
      const errorObj = error instanceof Error ? error : new Error(`Speech processing error: ${errorMessage}`);
      this.callbacks.onError?.(errorObj);
    } finally {
      this.callbacks.onSpeechEnd?.();
    }
  }

  /**
   * Speak text using Azure Speech Services
   */
  private async speakText(text: string): Promise<void> {
    if (!this.synthesizer || !text.trim()) return;

    return new Promise((resolve, reject) => {
      this.callbacks.onSpeechStart?.();

      this.synthesizer!.speakTextAsync(
        text,
        (result: any) => {
          if (result.reason === SpeechSDK.ResultReason.SynthesizingAudioCompleted) {
            this.callbacks.onSpeechEnd?.();
            resolve();
          } else if (result.reason === SpeechSDK.ResultReason.Canceled) {
            const cancellation = SpeechSDK.CancellationDetails.fromResult(result);
            console.error('Speech synthesis canceled:', cancellation.reason, cancellation.errorDetails);
            this.callbacks.onSpeechEnd?.();
            reject(new Error(`Speech synthesis canceled: ${cancellation.errorDetails}`));
          } else {
            this.callbacks.onSpeechEnd?.();
            reject(new Error('Speech synthesis failed'));
          }
        },
        (error: any) => {
          console.error('Speech synthesis error:', error);
          this.callbacks.onSpeechEnd?.();
          reject(error);
        }
      );
    });
  }

  /**
   * Start the interview
   */
  async startInterview(): Promise<void> {
    try {
      // Check if Azure Speech Services is configured
      // Support both endpoint-based and region-based configuration
      const hasSpeechServices = (this.config.speechKey && this.config.speechRegion) || 
                                (this.config.speechKey && this.config.speechEndpoint);

      if (!hasSpeechServices) {
        const errorMsg = 'Azure Speech Services not configured. Please add either:\n' +
          '- NEXT_PUBLIC_AZURE_SPEECH_KEY and NEXT_PUBLIC_AZURE_SPEECH_REGION, OR\n' +
          '- NEXT_PUBLIC_AZURE_SPEECH_KEY and NEXT_PUBLIC_AZURE_SPEECH_ENDPOINT\n' +
          'to your .env file. You can get these from Azure Portal: https://portal.azure.com';
        console.error('FoundryInterviewer:', errorMsg);
        throw new Error(errorMsg);
      }

      // Initialize Azure Speech Services
      // Support both endpoint-based and region-based configuration
      if (this.config.speechEndpoint && this.config.speechKey) {
        // Use custom endpoint if provided (for STT, use the speech endpoint)
        // Speech SDK requires URL object, not string
        const endpointUrl = new URL(this.config.speechEndpoint);
        this.speechConfig = SpeechSDK.SpeechConfig.fromEndpoint(
          endpointUrl,
          this.config.speechKey
        );
        // For TTS, we can use the same endpoint or region
        if (this.config.speechRegion) {
          this.synthesizerConfig = SpeechSDK.SpeechConfig.fromSubscription(
            this.config.speechKey,
            this.config.speechRegion
          );
        } else {
          // Use the same endpoint for TTS
          this.synthesizerConfig = SpeechSDK.SpeechConfig.fromEndpoint(
            endpointUrl,
            this.config.speechKey
          );
        }
      } else if (this.config.speechKey && this.config.speechRegion) {
        // Use region-based configuration (standard approach)
        this.speechConfig = SpeechSDK.SpeechConfig.fromSubscription(
          this.config.speechKey,
          this.config.speechRegion
        );
        this.synthesizerConfig = SpeechSDK.SpeechConfig.fromSubscription(
          this.config.speechKey,
          this.config.speechRegion
        );
      } else {
        throw new Error('Speech Services configuration incomplete');
      }
      
      this.speechConfig.speechRecognitionLanguage = 'en-US';
      this.synthesizerConfig.speechSynthesisVoiceName = 'en-US-JennyNeural';

      // Set up audio input (microphone)
      this.audioConfig = SpeechSDK.AudioConfig.fromDefaultMicrophoneInput();

      // Create recognizer
      this.recognizer = new SpeechSDK.SpeechRecognizer(this.speechConfig, this.audioConfig);

      // Create synthesizer
      this.synthesizer = new SpeechSDK.SpeechSynthesizer(this.synthesizerConfig);

      // Set up recognition event handlers
      this.recognizer.recognizing = (_s: any, e: any) => {
        if (e.result.text) {
          this.callbacks.onTranscript?.(e.result.text, false);
        }
      };

      this.recognizer.recognized = async (_s: any, e: any) => {
        if (e.result.reason === SpeechSDK.ResultReason.RecognizedSpeech) {
          await this.handleRecognizedSpeech(e.result.text);
        } else if (e.result.reason === SpeechSDK.ResultReason.NoMatch) {
          console.log('No speech could be recognized');
        }
      };

      this.recognizer.canceled = (_s: any, e: any) => {
        const errorDetails = e.errorDetails || e.reason || 'Unknown error';
        console.error('Speech recognition canceled:', errorDetails, e);
        if (e.reason === SpeechSDK.CancellationReason.Error) {
          const errorMsg = typeof errorDetails === 'string' ? errorDetails : JSON.stringify(errorDetails);
          this.callbacks.onError?.(new Error(`Speech recognition error: ${errorMsg}`));
        }
      };

      this.recognizer.sessionStopped = (_s: any, _e: any) => {
        console.log('Speech recognition session stopped');
      };

      // Initialize conversation history with system prompt
      const systemPrompt = this.buildSystemPrompt();
      if (systemPrompt) {
        this.conversationHistory = [{ role: 'system', content: systemPrompt }];
      }

      // Start continuous recognition
      this.recognizer.startContinuousRecognitionAsync(
        () => {
          console.log('Microsoft Foundry interview started');
          this.isCallActive = true;
          this.callbacks.onCallStart?.();

          // Send initial greeting
          const greeting = `Hello! I've reviewed your background and I'm ready to conduct your interview. ${
            this.config.context?.jobTitle ? `We'll be discussing the ${this.config.context.jobTitle} position` : ''
          }${this.config.context?.company ? ` at ${this.config.context.company}` : ''}. Are you ready to get started?`;

          this.speakText(greeting).then(() => {
            this.callbacks.onAssistantMessage?.(greeting);
          });
        },
        (error: any) => {
          const errorMessage = error instanceof Error ? error.message : String(error);
          console.error('Error starting recognition:', errorMessage, error);
          const errorObj = error instanceof Error ? error : new Error(`Speech recognition failed: ${errorMessage}`);
          this.callbacks.onError?.(errorObj);
          throw errorObj;
        }
      );
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      console.error('Error starting Microsoft Foundry interview:', errorMessage, error);
      
      // Provide more specific error messages
      let userFriendlyError = errorMessage;
      if (errorMessage.includes('Speech Services not configured')) {
        userFriendlyError = errorMessage; // Already user-friendly
      } else if (errorMessage.includes('microphone') || errorMessage.includes('Audio')) {
        userFriendlyError = 'Microphone access denied or unavailable. Please grant microphone permissions and try again.';
      } else if (errorMessage.includes('Speech recognition') || errorMessage.includes('Speech SDK')) {
        userFriendlyError = `Speech recognition error: ${errorMessage}`;
      } else if (errorMessage.includes('Invalid URL') || errorMessage.includes('URL')) {
        userFriendlyError = `Invalid endpoint configuration: ${errorMessage}. Check your NEXT_PUBLIC_AZURE_SPEECH_ENDPOINT.`;
      } else {
        userFriendlyError = `Failed to start voice interview: ${errorMessage}`;
      }
      
      const errorObj = error instanceof Error ? error : new Error(userFriendlyError);
      if (!(error instanceof Error)) {
        errorObj.message = userFriendlyError;
      } else if (errorObj.message !== userFriendlyError) {
        errorObj.message = userFriendlyError;
      }
      this.callbacks.onError?.(errorObj);
      throw errorObj;
    }
  }

  /**
   * Stop the interview
   */
  async stopInterview(): Promise<void> {
    try {
      if (this.recognizer) {
        await new Promise<void>((resolve) => {
          this.recognizer!.stopContinuousRecognitionAsync(
            () => {
              this.recognizer!.close();
              this.recognizer = null;
              resolve();
            },
            () => resolve()
          );
        });
      }

      if (this.synthesizer) {
        this.synthesizer.close();
        this.synthesizer = null;
      }

      if (this.audioConfig) {
        this.audioConfig.close();
        this.audioConfig = null;
      }

      if (this.speechConfig) {
        this.speechConfig.close();
        this.speechConfig = null;
      }

      if (this.synthesizerConfig) {
        this.synthesizerConfig.close();
        this.synthesizerConfig = null;
      }

      this.isCallActive = false;
      this.callbacks.onCallEnd?.();
    } catch (error) {
      console.error('Error stopping interview:', error);
    }
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
    // For Microsoft Foundry, we can add system messages to conversation history
    if (message && message.type === 'add-message' && message.message) {
      const msg = message.message;
      if (msg.role === 'system' && msg.content) {
        this.conversationHistory.push({ role: 'system', content: msg.content });
      }
    }
  }

  /**
   * Update time remaining during the interview
   * Sends context update to assistant about remaining time
   */
  updateTimeRemaining(timeRemainingSeconds: number): void {
    if (!this.isCallActive) {
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
        console.log(`⏰ Sending time update to Foundry: ${minutes} minutes remaining`);
        this.send({
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
