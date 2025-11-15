'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import InterviewHeader from '@/components/interview-session/interview-header';
import QuestionDisplay from '@/components/interview-session/question-display';
import RecordingControls from '@/components/interview-session/recording-controls';
import TranscriptPanel from '@/components/interview-session/transcript-panel';
import TimerDisplay from '@/components/interview-session/timer-display';
import { apiClient } from '@/lib/api/client';
import type { InterviewQuestion, ResponseEvaluation } from '@/lib/api/types';

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
    if (!transcript.trim()) {
      alert('Please provide an answer before proceeding.');
      return;
    }

    setIsEvaluating(true);
    setIsRecording(false);

    try {
      // Evaluate the response
      const currentQuestion = questions[currentQuestionIndex];
      const response = await apiClient.evaluateResponse({
        question: currentQuestion,
        transcript: transcript,
        question_type: currentQuestion.type,
      });

      const newResponse = {
        question: currentQuestion,
        answer: transcript,
        evaluation: response.success && 'evaluation' in response ? response.evaluation : undefined,
      };

      setResponses([...responses, newResponse]);
      setTranscript('');

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
          answer: transcript,
        },
      ]);
      setTranscript('');

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
    setResponses([
      ...responses,
      {
        question: questions[currentQuestionIndex],
        answer: transcript || '(skipped)',
      },
    ]);
    setTranscript('');

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
      <InterviewHeader questionNumber={currentQuestionIndex + 1} totalQuestions={questions.length} />

      <div className="flex flex-col lg:flex-row h-[calc(100vh-80px)]">
        {/* Main Interview Section */}
        <div className="flex-1 flex flex-col border-b lg:border-b-0 lg:border-r border-border">
          {/* Timer */}
          <div className="bg-card border-b border-border p-4 flex justify-end">
            <TimerDisplay timeRemaining={timeRemaining} />
          </div>

          {/* Question Display */}
          <div className="flex-1 flex items-center justify-center p-8">
            <QuestionDisplay
              question={questions[currentQuestionIndex].question || questions[currentQuestionIndex].text || ''}
              questionNumber={currentQuestionIndex + 1}
              totalQuestions={questions.length}
            />
          </div>

          {/* Recording Controls */}
          <div className="bg-card border-t border-border p-8">
            <RecordingControls
              isRecording={isRecording}
              onToggleRecording={() => setIsRecording(!isRecording)}
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
