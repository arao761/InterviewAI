'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import dynamic from 'next/dynamic';
import { Button } from '@/components/ui/button';
import { Loader2, Volume2, Wifi, WifiOff, Phone, PhoneOff } from 'lucide-react';
import TranscriptPanel from '@/components/interview-session/transcript-panel';
import TimerDisplay from '@/components/interview-session/timer-display';
import DSAProblemDisplay from '@/components/interview-session/dsa-problem-display';
import { VapiInterviewer } from '@/lib/vapi/vapi-interviewer';

// Dynamic import for CodeEditor to avoid SSR issues with Monaco
const CodeEditor = dynamic(
  () => import('@/components/interview-session/code-editor'),
  { ssr: false, loading: () => <div className="flex items-center justify-center h-full bg-[#1e1e1e] text-gray-400">Loading editor...</div> }
);

// Message type for conversation history
interface ConversationMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface InterviewSessionData {
  questions: any[];
  formData: any;
  resumeData: any;
  startTime: string;
}

export default function InterviewSession() {
  const router = useRouter();
  const [timeRemaining, setTimeRemaining] = useState(1800);
  const [sessionData, setSessionData] = useState<InterviewSessionData | null>(null);
  const [code, setCode] = useState('');
  const [codeLanguage, setCodeLanguage] = useState('javascript');
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  // VAPI state
  const [isCallActive, setIsCallActive] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [conversationMessages, setConversationMessages] = useState<ConversationMessage[]>([]);
  const [aiSpeaking, setAiSpeaking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [transcript, setTranscript] = useState('');

  const vapiInterviewerRef = useRef<VapiInterviewer | null>(null);
  const finalTranscriptRef = useRef<string>('');

  // Check if this is a technical interview
  const isTechnicalInterview = sessionData?.formData?.interviewType === 'technical';
  
  // Get current question
  const currentQuestion = sessionData?.questions?.[currentQuestionIndex];
  
  // Check if it's a coding question - multiple ways to detect
  const isCodingQuestion = 
    currentQuestion?.type === 'coding' || 
    currentQuestion?.question_type === 'coding' ||
    currentQuestion?.dsa_data !== undefined ||
    (isTechnicalInterview && currentQuestion?.category?.toLowerCase().includes('coding')) ||
    (isTechnicalInterview && currentQuestion?.category?.toLowerCase().includes('algorithm')) ||
    (isTechnicalInterview && currentQuestion?.category?.toLowerCase().includes('data structure'));
  
  // Get DSA problem data - ONLY for technical interviews
  // The dsa_data should contain the full DSA problem object with title, problem_statement, etc.
  let dsaProblem = null;
  
  // Only extract DSA problem data in technical interviews
  if (isTechnicalInterview && currentQuestion) {
    // Priority 1: Check dsa_data field (this is where backend stores the full DSA problem)
    if (currentQuestion.dsa_data && 
        typeof currentQuestion.dsa_data === 'object' &&
        currentQuestion.dsa_data.title &&
        currentQuestion.dsa_data.problem_statement) {
      dsaProblem = currentQuestion.dsa_data;
    }
    // Priority 2: Check other possible nested locations
    else if (currentQuestion.problem && 
             typeof currentQuestion.problem === 'object' &&
             currentQuestion.problem.title &&
             currentQuestion.problem.problem_statement) {
      dsaProblem = currentQuestion.problem;
    }
    else if (currentQuestion.dsa_problem && 
             typeof currentQuestion.dsa_problem === 'object' &&
             currentQuestion.dsa_problem.title &&
             currentQuestion.dsa_problem.problem_statement) {
      dsaProblem = currentQuestion.dsa_problem;
    }
    // Priority 3: Check if the question itself is a DSA problem
    // (but exclude if it's just a text question with "question debug shortcut")
    else if (currentQuestion.title && 
             currentQuestion.problem_statement && 
             currentQuestion.title !== 'question debug shortcut' &&
             currentQuestion.title !== currentQuestion.text &&
             currentQuestion.title !== currentQuestion.question &&
             !currentQuestion.title.toLowerCase().includes('debug')) {
      dsaProblem = currentQuestion;
    }
  }
  
  // Validate dsaProblem has required fields before using it
  // Make sure it's not just a text question with "question debug shortcut"
  // Only validate for technical interviews
  const isValidDSAProblem = isTechnicalInterview &&
                            dsaProblem && 
                            typeof dsaProblem === 'object' &&
                            dsaProblem.title && 
                            dsaProblem.title !== 'question debug shortcut' &&
                            dsaProblem.title !== 'question' &&
                            !dsaProblem.title.toLowerCase().includes('debug') &&
                            dsaProblem.problem_statement &&
                            dsaProblem.difficulty &&
                            dsaProblem.topic;
  
  // Debug logging
  useEffect(() => {
    if (currentQuestion && isTechnicalInterview) {
      console.log('🔍 Current question:', currentQuestion);
      console.log('🔍 Question keys:', Object.keys(currentQuestion || {}));
      console.log('🔍 Is coding question:', isCodingQuestion);
      console.log('🔍 DSA problem:', dsaProblem);
      console.log('🔍 Is technical interview:', isTechnicalInterview);
      console.log('🔍 All questions:', sessionData?.questions);
    }
  }, [currentQuestion, isCodingQuestion, dsaProblem, isTechnicalInterview, sessionData]);

  const handleCodeChange = (newCode: string, language: string) => {
    setCode(newCode);
    setCodeLanguage(language);
  };
  
  // Get initial code from DSA problem function signature for a specific language
  const getInitialCode = (lang: string = codeLanguage) => {
    if (dsaProblem?.function_signatures) {
      // Try to get signature for the requested language
      let sig = dsaProblem.function_signatures[lang];
      
      // Fallback to other languages if requested one not available
      if (!sig) {
        sig = dsaProblem.function_signatures.javascript ||
              dsaProblem.function_signatures.python ||
              dsaProblem.function_signatures.java ||
              dsaProblem.function_signatures.cpp;
      }
      
      if (sig) {
        // Create function body template based on language
        if (lang === 'python') {
          return `${sig}\n    pass\n`;
        } else if (lang === 'javascript' || lang === 'typescript') {
          return `${sig}\n    \n}\n`;
        } else if (lang === 'java') {
          return `${sig}\n        \n    }\n}\n`;
        } else if (lang === 'cpp' || lang === 'c') {
          return `${sig}\n    \n}\n`;
        } else if (lang === 'go') {
          return `${sig}\n    \n}\n`;
        } else if (lang === 'rust') {
          return `${sig}\n    \n}\n`;
        }
        // Default: just return the signature
        return sig;
      }
    }
    return '';
  };

  // Initialize VAPI interviewer
  const initializeVapi = useCallback(() => {
    const apiKey = process.env.NEXT_PUBLIC_VAPI_API_KEY;
    const assistantId = process.env.NEXT_PUBLIC_VAPI_ASSISTANT_ID;

    if (!apiKey || !assistantId) {
      setError('VAPI configuration missing. Please check your environment variables.');
      return null;
    }

    // Build interview context from session data
    const context = sessionData ? {
      resumeData: sessionData.resumeData,
      questions: sessionData.questions,
      interviewType: sessionData.formData?.interviewType,
      difficulty: sessionData.formData?.difficulty,
      jobTitle: sessionData.formData?.jobTitle,
      company: sessionData.formData?.company,
      duration: sessionData.formData?.duration,
      timeRemainingMinutes: Math.floor(timeRemaining / 60),
    } : undefined;

    const interviewer = new VapiInterviewer(
      {
        vapiApiKey: apiKey,
        assistantId: assistantId,
        context: context,
      },
      {
        onTranscript: (text, isFinal) => {
          if (text.trim()) {
            if (isFinal) {
              // Add to transcript
              const newTranscript = finalTranscriptRef.current + text + ' ';
              finalTranscriptRef.current = newTranscript;
              setTranscript(newTranscript);

              // Add user message to conversation (with deduplication)
              setConversationMessages(prev => {
                const lastMsg = prev[prev.length - 1];
                // Skip if same content as last message
                if (lastMsg && lastMsg.role === 'user' && lastMsg.content === text.trim()) {
                  return prev;
                }
                return [...prev, {
                  role: 'user',
                  content: text.trim(),
                  timestamp: new Date(),
                }];
              });
            }
          }
        },
        onAssistantMessage: (message) => {
          if (message.trim()) {
            // Add assistant message to conversation (with deduplication)
            setConversationMessages(prev => {
              const lastMsg = prev[prev.length - 1];
              // Skip if same content as last message
              if (lastMsg && lastMsg.role === 'assistant' && lastMsg.content === message.trim()) {
                return prev;
              }
              return [...prev, {
                role: 'assistant',
                content: message.trim(),
                timestamp: new Date(),
              }];
            });
          }
        },
        onError: (err) => {
          console.error('VAPI error:', err);
          setError(`Voice AI error: ${err.message}`);
          setIsCallActive(false);
          setIsConnecting(false);
        },
        onCallStart: () => {
          console.log('VAPI call started');
          setIsCallActive(true);
          setIsConnecting(false);
          setError(null);
        },
        onCallEnd: () => {
          console.log('VAPI call ended');
          setIsCallActive(false);
          setIsConnecting(false);
        },
        onSpeechStart: () => {
          setAiSpeaking(true);
        },
        onSpeechEnd: () => {
          setAiSpeaking(false);
        },
      }
    );

    return interviewer;
  }, [sessionData]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (vapiInterviewerRef.current) {
        vapiInterviewerRef.current.stopInterview();
      }
    };
  }, []);

  const handleStartCall = async () => {
    setError(null);
    setIsConnecting(true);

    try {
      const interviewer = initializeVapi();
      if (!interviewer) {
        setIsConnecting(false);
        return;
      }

      vapiInterviewerRef.current = interviewer;
      await interviewer.startInterview();
      // State updates handled by callbacks
    } catch (e) {
      console.error('Error starting VAPI interview:', e);
      setError('Failed to start voice interview. Please check your microphone permissions and try again.');
      setIsConnecting(false);
    }
  };

  const handleEndCall = async () => {
    if (vapiInterviewerRef.current) {
      await vapiInterviewerRef.current.stopInterview();
      vapiInterviewerRef.current = null;
    }
    setIsCallActive(false);
  };

  useEffect(() => {
    // Load interview session from sessionStorage
    const savedSession = sessionStorage.getItem('interviewSession');
    if (savedSession) {
      const session: InterviewSessionData = JSON.parse(savedSession);
      setSessionData(session);

      // Set timer based on duration
      const duration = parseInt(session.formData?.duration || '30');
      setTimeRemaining(duration * 60);
    } else {
      // No session found, redirect to setup
      router.push('/interview-setup');
    }
  }, [router]);

  useEffect(() => {
    if (timeRemaining <= 0) {
      handleEndCall();
      handleCompleteInterview();
      return;
    }

    const timer = setInterval(() => {
      setTimeRemaining((prev) => {
        const newTime = Math.max(0, prev - 1);

        // Update VAPI with time remaining at key thresholds
        if (vapiInterviewerRef.current) {
          vapiInterviewerRef.current.updateTimeRemaining(newTime);
        }

        return newTime;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [timeRemaining]);

  const handleCompleteInterview = async () => {
    // Stop call if active
    await handleEndCall();

    // Store results in sessionStorage
    const results = {
      responses: conversationMessages,
      sessionData,
      transcript: finalTranscriptRef.current,
      code: code,
      codeLanguage: codeLanguage,
      completedAt: new Date().toISOString(),
    };
    sessionStorage.setItem('interviewResults', JSON.stringify(results));

    // Navigate to processing page for evaluation
    router.push('/interview/processing');
  };

  const handleExit = () => {
    const confirmExit = window.confirm(
      'Are you sure you want to exit? Your progress will be lost.'
    );
    if (confirmExit) {
      handleEndCall();
      sessionStorage.removeItem('interviewSession');
      router.push('/interview-setup');
    }
  };

  if (!sessionData) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4 text-primary" />
          <p className="text-muted-foreground">Loading interview...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}
      <div className="bg-card border-b border-border px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" className="hover:bg-muted" onClick={handleExit}>
            Exit
          </Button>
          <div className="h-6 w-px bg-border"></div>
          <div className="text-sm text-muted-foreground">
            {sessionData.formData?.interviewType === 'technical' ? 'Technical' :
             sessionData.formData?.interviewType === 'behavioral' ? 'Behavioral' : 'Mixed'} Interview
          </div>
        </div>

        <div className="flex items-center gap-4">
          {/* Interview Control Button - Shrunk and moved to header when DSA problem is shown */}
          {isTechnicalInterview && dsaProblem && (
            <div className="flex items-center gap-2">
              {!isCallActive && !isConnecting ? (
                <Button
                  onClick={handleStartCall}
                  size="sm"
                  className="rounded-full w-12 h-12 flex items-center justify-center bg-green-600 hover:bg-green-700 text-white"
                  title="Start Interview"
                >
                  <Phone className="w-5 h-5" />
                </Button>
              ) : isConnecting ? (
                <Button
                  disabled
                  size="sm"
                  className="rounded-full w-12 h-12 flex items-center justify-center bg-blue-600 text-white"
                  title="Connecting..."
                >
                  <Loader2 className="w-5 h-5 animate-spin" />
                </Button>
              ) : (
                <Button
                  onClick={handleEndCall}
                  size="sm"
                  className="rounded-full w-12 h-12 flex items-center justify-center bg-red-600 hover:bg-red-700 text-white animate-pulse"
                  title="End Call"
                >
                  <PhoneOff className="w-5 h-5" />
                </Button>
              )}
            </div>
          )}

          {/* Connection Status */}
          <div className="flex items-center gap-2 text-sm">
            {isConnecting ? (
              <>
                <Loader2 className="w-4 h-4 text-blue-500 animate-spin" />
                <span className="text-blue-500">Connecting...</span>
              </>
            ) : isCallActive ? (
              <>
                <Wifi className="w-4 h-4 text-green-500" />
                <span className="text-green-500">Voice Active</span>
              </>
            ) : (
              <>
                <WifiOff className="w-4 h-4 text-muted-foreground" />
                <span className="text-muted-foreground">Voice Off</span>
              </>
            )}
          </div>

          <TimerDisplay timeRemaining={timeRemaining} />
        </div>
      </div>

      <div className="flex h-[calc(100vh-73px)]">
        {/* Main Section - DSA Problem & Code Editor */}
        <div className="flex-1 flex flex-col">
          {/* DSA Problem Display - shown for coding questions */}
          {isTechnicalInterview && isValidDSAProblem ? (
            <div className="flex-1 overflow-y-auto bg-background">
              <div className="max-w-4xl mx-auto p-6">
                <DSAProblemDisplay
                  problem={dsaProblem}
                  questionNumber={currentQuestionIndex + 1}
                  totalQuestions={sessionData?.questions?.length || 1}
                />
              </div>
            </div>
          ) : (
            /* Call Controls - Center of screen when no DSA problem */
            <div className="flex-1 flex items-center justify-center">
            <div className="text-center space-y-8">
              {/* AI Speaking Indicator */}
              {aiSpeaking && (
                <div className="flex items-center justify-center gap-2 text-blue-500">
                  <Volume2 className="w-5 h-5 animate-pulse" />
                  <span className="font-medium">AI is speaking...</span>
                </div>
              )}

              {/* Main Call Button */}
              <div className="flex justify-center">
                {!isCallActive && !isConnecting ? (
                  <Button
                    onClick={handleStartCall}
                    size="lg"
                    className="rounded-full w-40 h-40 flex flex-col items-center justify-center text-lg font-semibold bg-green-600 hover:bg-green-700 text-white"
                  >
                    <Phone className="w-10 h-10 mb-2" />
                    Start Interview
                  </Button>
                ) : isConnecting ? (
                  <Button
                    disabled
                    size="lg"
                    className="rounded-full w-40 h-40 flex flex-col items-center justify-center text-lg font-semibold bg-blue-600 text-white"
                  >
                    <Loader2 className="w-10 h-10 mb-2 animate-spin" />
                    Connecting...
                  </Button>
                ) : (
                  <Button
                    onClick={handleEndCall}
                    size="lg"
                    className="rounded-full w-40 h-40 flex flex-col items-center justify-center text-lg font-semibold bg-red-600 hover:bg-red-700 text-white animate-pulse"
                  >
                    <PhoneOff className="w-10 h-10 mb-2" />
                    End Call
                  </Button>
                )}
              </div>

              {/* Instructions */}
              <div className="text-sm text-muted-foreground max-w-md mx-auto">
                {!isCallActive && !isConnecting ? (
                  <p>Click the button above to start your voice interview with the AI interviewer. Make sure your microphone is enabled.</p>
                ) : isConnecting ? (
                  <p>Connecting to AI interviewer... Please allow microphone access if prompted.</p>
                ) : (
                  <p>Your interview is in progress. Speak naturally and the AI will guide you through the interview questions.</p>
                )}
              </div>

              {/* Error Display */}
              {error && (
                <div className="text-red-500 text-sm bg-red-500/10 p-4 rounded-lg max-w-md mx-auto">
                  {error}
                </div>
              )}

              {/* Complete Interview Button */}
              {isCallActive && (
                <Button
                  onClick={handleCompleteInterview}
                  variant="outline"
                  className="mt-4"
                >
                  Complete Interview
                </Button>
              )}
            </div>
          </div>
          )}
          
          {/* Show message if technical interview but no DSA problem found (for debugging) */}
          {isTechnicalInterview && !isValidDSAProblem && currentQuestion && (
            <div className="flex-1 p-6 overflow-y-auto border-t border-border">
              <div className="bg-muted/50 border border-border rounded-lg p-4">
                <p className="text-sm text-muted-foreground">
                  Technical interview question loaded. If this should be a coding question, check the browser console for debugging info.
                </p>
                <details className="mt-2">
                  <summary className="text-xs text-muted-foreground cursor-pointer">Question data (debug)</summary>
                  <pre className="text-xs mt-2 bg-background p-2 rounded overflow-auto">
                    {JSON.stringify(currentQuestion, null, 2)}
                  </pre>
                </details>
              </div>
            </div>
          )}
          
          {/* Show message if technical interview but no DSA problem found (for debugging) */}
          {isTechnicalInterview && !dsaProblem && currentQuestion && (
            <div className="flex-1 p-6 overflow-y-auto border-t border-border">
              <div className="bg-muted/50 border border-border rounded-lg p-4">
                <p className="text-sm text-muted-foreground">
                  Technical interview question loaded. If this should be a coding question, check the browser console for debugging info.
                </p>
                <details className="mt-2">
                  <summary className="text-xs text-muted-foreground cursor-pointer">Question data (debug)</summary>
                  <pre className="text-xs mt-2 bg-background p-2 rounded overflow-auto">
                    {JSON.stringify(currentQuestion, null, 2)}
                  </pre>
                </details>
              </div>
            </div>
          )}

          {/* Code Editor - shown for technical/coding interviews */}
          {(isTechnicalInterview || isCodingQuestion) && (
            <div className="flex-1 p-4 pt-0 min-h-[400px] border-t border-border">
              <div className="h-full">
                <div className="text-sm font-medium mb-2 text-muted-foreground">Code Editor</div>
                <div className="h-[calc(100%-24px)]">
                  <CodeEditor 
                    onCodeChange={handleCodeChange}
                    initialCode={isCodingQuestion && isValidDSAProblem ? getInitialCode(codeLanguage) : ''}
                  />
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Conversation Panel */}
        <div className="w-96 bg-card border-l border-border overflow-hidden flex flex-col">
          <TranscriptPanel
            transcript={transcript}
            onTranscriptChange={setTranscript}
            isRecording={isCallActive}
            conversationMessages={conversationMessages}
            aiSpeaking={aiSpeaking}
          />
        </div>
      </div>
    </div>
  );
}
