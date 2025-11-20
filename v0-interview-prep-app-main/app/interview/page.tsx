'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import dynamic from 'next/dynamic';
import InterviewHeader from '@/components/interview-session/interview-header';
import QuestionDisplay from '@/components/interview-session/question-display';
import RecordingControls from '@/components/interview-session/recording-controls';
import TranscriptPanel from '@/components/interview-session/transcript-panel';
import TimerDisplay from '@/components/interview-session/timer-display';
import { apiClient } from '@/lib/api/client';
import type { InterviewQuestion, ResponseEvaluation } from '@/lib/api/types';

// Dynamic import for CodeEditor to avoid SSR issues with Monaco
const CodeEditor = dynamic(
  () => import('@/components/interview-session/code-editor'),
  { ssr: false, loading: () => <div className="flex items-center justify-center h-full bg-[#1e1e1e] text-gray-400">Loading editor...</div> }
);

// Type declarations for Web Speech API
interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList;
  resultIndex: number;
}

interface SpeechRecognitionErrorEvent extends Event {
  error: string;
  message: string;
}

interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  start(): void;
  stop(): void;
  abort(): void;
  onresult: ((event: SpeechRecognitionEvent) => void) | null;
  onerror: ((event: SpeechRecognitionErrorEvent) => void) | null;
  onend: (() => void) | null;
  onstart: (() => void) | null;
}

declare global {
  interface Window {
    SpeechRecognition: new () => SpeechRecognition;
    webkitSpeechRecognition: new () => SpeechRecognition;
  }
}

interface InterviewSessionData {
  questions: InterviewQuestion[];
  formData: any;
  resumeData: any;
  startTime: string;
}

export default function InterviewSession() {
  const router = useRouter();
  const [isRecording, setIsRecording] = useState(false);
  const [timeRemaining, setTimeRemaining] = useState(1800); // 30 minutes
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [transcript, setTranscript] = useState('');
  const [responses, setResponses] = useState<Array<{ question: InterviewQuestion; answer: string; evaluation?: ResponseEvaluation }>>([]);
  const [questions, setQuestions] = useState<InterviewQuestion[]>([]);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [sessionData, setSessionData] = useState<InterviewSessionData | null>(null);
  const [speechError, setSpeechError] = useState<string | null>(null);
  const [code, setCode] = useState('');
  const [codeLanguage, setCodeLanguage] = useState('javascript');

  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const finalTranscriptRef = useRef<string>('');

  // Determine if current question should show code editor
  const isCodeQuestion = () => {
    if (!sessionData?.formData?.interviewType) return false;
    if (sessionData.formData.interviewType !== 'technical') return false;

    const question = questions[currentQuestionIndex];
    if (!question) return false;

    // Check if it's a coding question based on type or content
    const questionText = (question.question || question.text || '').toLowerCase();
    const isCodingType = question.type?.toLowerCase().includes('coding') ||
                         question.type?.toLowerCase().includes('algorithm') ||
                         question.type?.toLowerCase().includes('implementation');
    const hasCodingKeywords = questionText.includes('implement') ||
                              questionText.includes('write a function') ||
                              questionText.includes('write a program') ||
                              questionText.includes('code') ||
                              questionText.includes('algorithm');

    return isCodingType || hasCodingKeywords;
  };

  const handleCodeChange = (newCode: string, language: string) => {
    setCode(newCode);
    setCodeLanguage(language);
  };

  // Initialize speech recognition
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognitionAPI = window.SpeechRecognition || window.webkitSpeechRecognition;

      if (SpeechRecognitionAPI) {
        const recognition = new SpeechRecognitionAPI();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onresult = (event: SpeechRecognitionEvent) => {
          let interimTranscript = '';
          let finalTranscript = finalTranscriptRef.current;

          for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcriptPart = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
              finalTranscript += transcriptPart + ' ';
              finalTranscriptRef.current = finalTranscript;
            } else {
              interimTranscript += transcriptPart;
            }
          }

          setTranscript(finalTranscript + interimTranscript);
        };

        recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
          console.error('Speech recognition error:', event.error);
          if (event.error === 'not-allowed') {
            setSpeechError('Microphone access denied. Please allow microphone access in your browser settings.');
          } else if (event.error === 'no-speech') {
            // This is common, don't show error
          } else {
            setSpeechError(`Speech recognition error: ${event.error}`);
          }
        };

        recognition.onend = () => {
          // Restart if still recording (handles browser auto-stop)
          if (isRecording && recognitionRef.current) {
            try {
              recognitionRef.current.start();
            } catch (e) {
              // Already started
            }
          }
        };

        recognitionRef.current = recognition;
      } else {
        setSpeechError('Speech recognition is not supported in this browser. Please use Chrome.');
      }
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
    };
  }, [isRecording]);

  const handleToggleRecording = () => {
    if (!recognitionRef.current) {
      setSpeechError('Speech recognition is not available.');
      return;
    }

    if (isRecording) {
      // Stop recording
      recognitionRef.current.stop();
      setIsRecording(false);
    } else {
      // Start recording
      setSpeechError(null);
      finalTranscriptRef.current = transcript; // Keep existing transcript
      try {
        recognitionRef.current.start();
        setIsRecording(true);
      } catch (e) {
        console.error('Error starting speech recognition:', e);
        setSpeechError('Failed to start speech recognition. Please try again.');
      }
    }
  };

  useEffect(() => {
    // Load interview session from sessionStorage
    const savedSession = sessionStorage.getItem('interviewSession');
    if (savedSession) {
      const session: InterviewSessionData = JSON.parse(savedSession);
      setSessionData(session);
      setQuestions(session.questions || []);

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
      setIsRecording(false);
      handleCompleteInterview();
      return;
    }

    const timer = setInterval(() => {
      setTimeRemaining((prev) => Math.max(0, prev - 1));
    }, 1000);

    return () => clearInterval(timer);
  }, [timeRemaining]);

  const handleNextQuestion = async () => {
    const hasCode = isCodeQuestion() && code.trim();
    if (!transcript.trim() && !hasCode) {
      alert('Please provide an answer before proceeding.');
      return;
    }

    setIsEvaluating(true);
    setIsRecording(false);

    // Combine transcript and code for the full answer
    let fullAnswer = transcript;
    if (hasCode) {
      fullAnswer = transcript
        ? `${transcript}\n\n--- Code (${codeLanguage}) ---\n${code}`
        : `--- Code (${codeLanguage}) ---\n${code}`;
    }

    try {
      // Evaluate the response
      const currentQuestion = questions[currentQuestionIndex];
      const response = await apiClient.evaluateResponse({
        question: currentQuestion,
        transcript: fullAnswer,
        question_type: currentQuestion.type,
      });

      const newResponse = {
        question: currentQuestion,
        answer: fullAnswer,
        evaluation: response.success && 'evaluation' in response ? response.evaluation : undefined,
      };

      setResponses([...responses, newResponse]);
      setTranscript('');
      setCode('');
      finalTranscriptRef.current = '';

      // Move to next question or complete
      if (currentQuestionIndex < questions.length - 1) {
        setCurrentQuestionIndex(currentQuestionIndex + 1);
      } else {
        // Interview complete
        handleCompleteInterview();
      }
    } catch (error) {
      console.error('Error evaluating response:', error);
      // Store response without evaluation
      setResponses([
        ...responses,
        {
          question: questions[currentQuestionIndex],
          answer: fullAnswer,
        },
      ]);
      setTranscript('');
      setCode('');
      finalTranscriptRef.current = '';

      if (currentQuestionIndex < questions.length - 1) {
        setCurrentQuestionIndex(currentQuestionIndex + 1);
      } else {
        handleCompleteInterview();
      }
    } finally {
      setIsEvaluating(false);
    }
  };

  const handleSkipQuestion = () => {
    // Stop recording if active
    if (isRecording && recognitionRef.current) {
      recognitionRef.current.stop();
      setIsRecording(false);
    }

    setResponses([
      ...responses,
      {
        question: questions[currentQuestionIndex],
        answer: transcript || '(skipped)',
      },
    ]);
    setTranscript('');
    setCode('');
    finalTranscriptRef.current = '';

    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      handleCompleteInterview();
    }
  };

  const handleCompleteInterview = async () => {
    // Store results in sessionStorage
    const results = {
      responses,
      sessionData,
      completedAt: new Date().toISOString(),
    };
    sessionStorage.setItem('interviewResults', JSON.stringify(results));

    // Optionally: Get full interview evaluation
    if (responses.length > 0) {
      try {
        const questionsAndResponses = responses.map(r => ({
          question: r.question,
          response: r.answer,
        }));

        const evaluation = await apiClient.evaluateInterview({
          questions_and_responses: questionsAndResponses,
          interview_type: sessionData?.formData?.interviewType || 'mixed',
        });

        if (evaluation.success && 'report' in evaluation) {
          sessionStorage.setItem('interviewEvaluation', JSON.stringify(evaluation.report));
        }
      } catch (error) {
        console.error('Error getting full evaluation:', error);
      }
    }

    // Navigate to results page
    router.push('/results');
  };

  const handleExit = () => {
    const confirmExit = window.confirm(
      'Are you sure you want to exit? Your progress will be lost.'
    );
    if (confirmExit) {
      // Clear session data
      sessionStorage.removeItem('interviewSession');
      router.push('/interview-setup');
    }
  };

  if (questions.length === 0) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground">Loading interview...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <InterviewHeader questionNumber={currentQuestionIndex + 1} totalQuestions={questions.length} onExit={handleExit} />

      <div className="flex flex-col lg:flex-row h-[calc(100vh-80px)]">
        {/* Main Interview Section */}
        <div className="flex-1 flex flex-col border-b lg:border-b-0 lg:border-r border-border">
          {/* Timer */}
          <div className="bg-card border-b border-border p-4 flex justify-end">
            <TimerDisplay timeRemaining={timeRemaining} />
          </div>

          {/* Question Display */}
          <div className={`${isCodeQuestion() ? 'p-4' : 'flex-1 flex items-center justify-center p-8'}`}>
            <QuestionDisplay
              question={questions[currentQuestionIndex].question || questions[currentQuestionIndex].text || ''}
              questionNumber={currentQuestionIndex + 1}
              totalQuestions={questions.length}
            />
          </div>

          {/* Code Editor - shown for coding questions */}
          {isCodeQuestion() && (
            <div className="flex-1 p-4 pt-0 min-h-[300px]">
              <CodeEditor onCodeChange={handleCodeChange} />
            </div>
          )}

          {/* Recording Controls */}
          <div className="bg-card border-t border-border p-8">
            <RecordingControls
              isRecording={isRecording}
              onToggleRecording={handleToggleRecording}
              onNextQuestion={handleNextQuestion}
              onSkip={handleSkipQuestion}
              isLastQuestion={currentQuestionIndex === questions.length - 1}
              disabled={isEvaluating}
            />
            {isEvaluating && (
              <p className="text-center text-sm text-muted-foreground mt-4">
                Evaluating your response...
              </p>
            )}
            {speechError && (
              <p className="text-center text-sm text-red-500 mt-4">
                {speechError}
              </p>
            )}
          </div>
        </div>

        {/* Transcript Panel */}
        <div className="w-full lg:w-80 bg-card border-t lg:border-t-0 border-border overflow-hidden flex flex-col">
          <TranscriptPanel
            transcript={transcript}
            onTranscriptChange={setTranscript}
            isRecording={isRecording}
          />
        </div>
      </div>
    </div>
  );
}
