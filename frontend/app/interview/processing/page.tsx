/**
 * Interview Evaluation Processing Page
 * Handles the transition from interview completion to results display
 * Orchestrates evaluation API call and data transformation
 */

'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import EvaluationLoading from '@/components/interview/evaluation-loading';
import { extractQuestionAnswerPairs, validateQuestionAnswerPairs } from '@/lib/utils/conversation-transformer';
import { apiClient } from '@/lib/api/client';
import type { InterviewEvaluationReport } from '@/lib/api/types';

interface ConversationMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function ProcessingPage() {
  const router = useRouter();
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState('Preparing...');
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  const hasStartedEvaluation = useRef(false);

  const MAX_RETRIES = 2;
  const EVALUATION_TIMEOUT = 30000; // 30 seconds

  useEffect(() => {
    // Prevent double execution in React Strict Mode
    if (hasStartedEvaluation.current) return;
    hasStartedEvaluation.current = true;

    // Add beforeunload warning
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      e.preventDefault();
      e.returnValue = 'Your interview is being evaluated. Are you sure you want to leave?';
    };
    window.addEventListener('beforeunload', handleBeforeUnload);

    // Start evaluation
    evaluateInterview();

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, []);

  const evaluateInterview = async () => {
    try {
      setError(null);
      setProgress(0);
      setStage('Preparing your interview data...');

      // Step 1: Read interview data from sessionStorage (0-20%)
      const savedResults = sessionStorage.getItem('interviewResults');
      const savedSession = sessionStorage.getItem('interviewSession');

      if (!savedResults || !savedSession) {
        throw new Error('Interview data not found. Please complete an interview first.');
      }

      const results = JSON.parse(savedResults);
      const sessionData = JSON.parse(savedSession);

      setProgress(10);

      // Extract data
      const conversationMessages: ConversationMessage[] = results.responses || [];
      const questions = sessionData.questions || [];
      const interviewType = sessionData.formData?.interviewType || 'mixed';

      console.log('Processing interview:', {
        messageCount: conversationMessages.length,
        questionCount: questions.length,
        interviewType
      });

      setProgress(20);

      // Step 2: Transform conversation to Q&A pairs (20-40%)
      setStage('Matching questions with your responses...');

      const qaPairs = extractQuestionAnswerPairs(conversationMessages, questions);

      // Validate pairs
      const validation = validateQuestionAnswerPairs(qaPairs);
      if (!validation.valid) {
        console.error('Validation errors:', validation.errors);
        throw new Error('Failed to process interview responses. Some questions may not have been answered.');
      }

      console.log('Q&A pairs extracted:', qaPairs.length);
      setProgress(40);

      // Step 3: Call evaluation API (40-80%)
      setStage('Analyzing your responses...');

      // Create timeout promise
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Evaluation timeout - please try again')), EVALUATION_TIMEOUT);
      });

      // Call API with timeout
      console.log('Calling evaluateInterview API with:', {
        qaPairsCount: qaPairs.length,
        interviewType
      });

      const evaluationPromise = apiClient.evaluateInterview({
        questions_and_responses: qaPairs.map(pair => ({
          question: pair.question,
          response: pair.response
        })),
        interview_type: interviewType as any
      });

      setProgress(60);

      const response = await Promise.race([evaluationPromise, timeoutPromise]) as any;

      console.log('Evaluation API response:', response);

      setProgress(80);

      // Check response structure
      if (!response) {
        throw new Error('No response received from evaluation API');
      }

      // Handle error response
      if (response.success === false) {
        console.error('Evaluation API returned error:', response);
        throw new Error(response.error || response.detail || 'Evaluation failed - invalid response from server');
      }

      // Check if response has report
      if (!response.report) {
        console.error('Response missing report field:', response);
        throw new Error('Evaluation failed - response missing report data');
      }

      const evaluation: InterviewEvaluationReport = response.report;

      // Validate evaluation data
      if (!evaluation.overall_score && evaluation.overall_score !== 0) {
        console.error('Invalid evaluation data:', evaluation);
        throw new Error('Evaluation failed - invalid evaluation data received');
      }

      console.log('Evaluation completed:', {
        overallScore: evaluation.overall_score,
        questionCount: evaluation.total_questions
      });

      // Step 4: Store evaluation in sessionStorage (80-100%)
      setStage('Finalizing your results...');
      setProgress(90);

      sessionStorage.setItem('interviewEvaluation', JSON.stringify(evaluation));
      // Clear the processing attempt flag since we succeeded
      sessionStorage.removeItem('processingAttempted');

      setProgress(100);
      setStage('Complete!');

      // Navigate to results
      setTimeout(() => {
        router.push('/results');
      }, 500);

    } catch (err) {
      console.error('Evaluation error:', err);
      console.error('Error details:', {
        message: err instanceof Error ? err.message : String(err),
        stack: err instanceof Error ? err.stack : undefined,
        retryCount,
        hasStartedEvaluation: hasStartedEvaluation.current
      });

      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred';

      // Retry logic - only retry on network errors or timeouts
      const isRetryableError = errorMessage.includes('timeout') || 
                               errorMessage.includes('Network') || 
                               errorMessage.includes('Failed to fetch') ||
                               errorMessage.includes('connection');

      if (isRetryableError && retryCount < MAX_RETRIES) {
        console.log(`Retrying... (${retryCount + 1}/${MAX_RETRIES})`);
        setRetryCount(prev => prev + 1);

        // Exponential backoff
        setTimeout(() => {
          hasStartedEvaluation.current = false;
          evaluateInterview();
        }, 1000 * Math.pow(2, retryCount));
      } else {
        // Don't retry on validation or data errors
        console.error('Final error after retries:', errorMessage);
        setError(errorMessage);
        hasStartedEvaluation.current = false; // Allow manual retry
      }
    }
  };

  const handleRetry = () => {
    setRetryCount(0);
    hasStartedEvaluation.current = false;
    evaluateInterview();
  };

  return (
    <EvaluationLoading
      progress={progress}
      stage={stage}
      error={error}
      onRetry={handleRetry}
    />
  );
}
