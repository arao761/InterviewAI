/**
 * Evaluation Loading Component
 * Displays loading state with progress indicator during interview evaluation
 */

'use client';

import { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Loader2, AlertCircle, RefreshCw } from 'lucide-react';

interface EvaluationLoadingProps {
  progress: number;
  stage: string;
  error?: string;
  onRetry?: () => void;
}

const LOADING_TIPS = [
  'Your responses are being analyzed by our AI evaluation engine...',
  'We\'re assessing clarity, confidence, and technical accuracy...',
  'Evaluating your communication structure and engagement...',
  'Generating detailed feedback and improvement suggestions...',
  'Almost done! Compiling your comprehensive results...'
];

export default function EvaluationLoading({
  progress,
  stage,
  error,
  onRetry
}: EvaluationLoadingProps) {
  const [currentTip, setCurrentTip] = useState(0);

  // Rotate tips every 3 seconds
  useEffect(() => {
    if (error) return;

    const interval = setInterval(() => {
      setCurrentTip((prev) => (prev + 1) % LOADING_TIPS.length);
    }, 3000);

    return () => clearInterval(interval);
  }, [error]);

  if (error) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="max-w-md w-full p-8 border-destructive">
          <div className="flex flex-col items-center text-center space-y-4">
            <div className="rounded-full bg-destructive/10 p-3">
              <AlertCircle className="w-8 h-8 text-destructive" />
            </div>

            <div>
              <h2 className="text-xl font-bold mb-2">Evaluation Error</h2>
              <p className="text-muted-foreground text-sm">
                {error}
              </p>
            </div>

            {onRetry && (
              <Button
                onClick={onRetry}
                className="w-full"
                variant="outline"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Try Again
              </Button>
            )}

            <Button
              onClick={() => window.location.href = '/interview-setup'}
              variant="ghost"
              className="w-full"
            >
              Start New Interview
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="max-w-2xl w-full p-8">
        <div className="space-y-6">
          {/* Header */}
          <div className="text-center space-y-2">
            <div className="flex justify-center mb-4">
              <Loader2 className="w-12 h-12 animate-spin text-primary" />
            </div>
            <h2 className="text-2xl font-bold">Analyzing Your Interview</h2>
            <p className="text-muted-foreground">
              This will only take a few moments...
            </p>
          </div>

          {/* Progress Bar */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">{stage}</span>
              <span className="font-medium">{Math.round(progress)}%</span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>

          {/* Loading Tips */}
          <div className="bg-muted/50 rounded-lg p-4 min-h-[60px] flex items-center justify-center">
            <p className="text-sm text-center text-muted-foreground transition-opacity duration-300">
              {LOADING_TIPS[currentTip]}
            </p>
          </div>

          {/* Stage Indicators */}
          <div className="flex justify-between items-center pt-4">
            <StageIndicator
              label="Preparing"
              active={progress < 20}
              completed={progress >= 20}
            />
            <div className="flex-1 h-px bg-border mx-2" />
            <StageIndicator
              label="Analyzing"
              active={progress >= 20 && progress < 80}
              completed={progress >= 80}
            />
            <div className="flex-1 h-px bg-border mx-2" />
            <StageIndicator
              label="Finalizing"
              active={progress >= 80}
              completed={progress >= 100}
            />
          </div>
        </div>
      </Card>
    </div>
  );
}

interface StageIndicatorProps {
  label: string;
  active: boolean;
  completed: boolean;
}

function StageIndicator({ label, active, completed }: StageIndicatorProps) {
  return (
    <div className="flex flex-col items-center space-y-1">
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center border-2 transition-colors ${
          completed
            ? 'bg-primary border-primary text-primary-foreground'
            : active
            ? 'border-primary text-primary'
            : 'border-muted-foreground/30 text-muted-foreground/30'
        }`}
      >
        {completed ? (
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
        ) : (
          <div className={active ? 'w-2 h-2 rounded-full bg-primary' : ''} />
        )}
      </div>
      <span
        className={`text-xs ${
          completed || active ? 'text-foreground' : 'text-muted-foreground/50'
        }`}
      >
        {label}
      </span>
    </div>
  );
}
