'use client';

import { useState, useEffect } from 'react';
import InterviewHeader from '@/components/interview-session/interview-header';
import QuestionDisplay from '@/components/interview-session/question-display';
import RecordingControls from '@/components/interview-session/recording-controls';
import TranscriptPanel from '@/components/interview-session/transcript-panel';
import TimerDisplay from '@/components/interview-session/timer-display';

export default function InterviewSession() {
  const [isRecording, setIsRecording] = useState(false);
  const [timeRemaining, setTimeRemaining] = useState(1800); // 30 minutes
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [transcript, setTranscript] = useState('');
  const [responses, setResponses] = useState<string[]>([]);

  // Mock questions data
  const questions = [
    'Tell me about a challenging project you worked on and how you handled it.',
    'How do you approach problem-solving?',
    'Describe a time when you had to work with a difficult team member.',
    'What are your strengths and weaknesses?',
    'Where do you see yourself in 5 years?',
  ];

  useEffect(() => {
    if (timeRemaining <= 0) {
      setIsRecording(false);
      return;
    }

    const timer = setInterval(() => {
      setTimeRemaining((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeRemaining]);

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setResponses([...responses, transcript]);
      setTranscript('');
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setIsRecording(false);
    } else {
      // Interview complete
      console.log('Interview complete!');
    }
  };

  const handleSkipQuestion = () => {
    setResponses([...responses, transcript]);
    setTranscript('');
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

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
              question={questions[currentQuestionIndex]}
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
            />
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
