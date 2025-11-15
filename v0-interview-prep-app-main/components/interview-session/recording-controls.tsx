import { Button } from '@/components/ui/button';
import { Mic, Square, SkipForward, Check } from 'lucide-react';

export default function RecordingControls({
  isRecording,
  onToggleRecording,
  onNextQuestion,
  onSkip,
  isLastQuestion,
  disabled = false,
}: {
  isRecording: boolean;
  onToggleRecording: () => void;
  onNextQuestion: () => void;
  onSkip: () => void;
  isLastQuestion: boolean;
  disabled?: boolean;
}) {
  return (
    <div className="space-y-6">
      {/* Recording Button */}
      <div className="flex justify-center">
        <Button
          onClick={onToggleRecording}
          size="lg"
          disabled={disabled}
          className={`rounded-full w-32 h-32 flex items-center justify-center text-lg font-semibold transition-all ${
            isRecording
              ? 'bg-red-600 text-white hover:bg-red-700 animate-pulse'
              : 'bg-primary text-primary-foreground hover:bg-primary/90'
          }`}
        >
          {isRecording ? (
            <>
              <Square className="w-6 h-6 mr-2" />
              Stop
            </>
          ) : (
            <>
              <Mic className="w-6 h-6 mr-2" />
              Start
            </>
          )}
        </Button>
      </div>

      {/* Status Text */}
      <div className="text-center">
        <p className="text-sm text-muted-foreground">
          {isRecording ? (
            <span className="text-red-500 font-semibold flex items-center justify-center gap-2">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
              Recording in progress...
            </span>
          ) : (
            'Click to start recording your response'
          )}
        </p>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-4">
        <Button
          variant="outline"
          className="flex-1 border-border hover:bg-card"
          onClick={onSkip}
          disabled={disabled}
        >
          <SkipForward className="w-4 h-4 mr-2" />
          Skip
        </Button>
        <Button
          onClick={onNextQuestion}
          disabled={disabled}
          className="flex-1 bg-primary text-primary-foreground hover:bg-primary/90"
        >
          <Check className="w-4 h-4 mr-2" />
          {isLastQuestion ? 'Finish' : 'Next'}
        </Button>
      </div>
    </div>
  );
}
