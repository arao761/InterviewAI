import { Button } from '@/components/ui/button';
import { Mic, Square, SkipForward, Check, Wifi, Loader2, Volume2 } from 'lucide-react';

export default function RecordingControls({
  isRecording,
  onToggleRecording,
  onNextQuestion,
  onSkip,
  isLastQuestion,
  disabled = false,
  isConnecting = false,
  isConnected = false,
  aiSpeaking = false,
}: {
  isRecording: boolean;
  onToggleRecording: () => void;
  onNextQuestion: () => void;
  onSkip: () => void;
  isLastQuestion: boolean;
  disabled?: boolean;
  isConnecting?: boolean;
  isConnected?: boolean;
  aiSpeaking?: boolean;
}) {
  return (
    <div className="space-y-6">
      {/* Connection Status */}
      {isConnected && (
        <div className="flex justify-center items-center gap-2 text-sm">
          <Wifi className="w-4 h-4 text-green-500" />
          <span className="text-green-500 font-medium">Connected to AI Interviewer</span>
          {aiSpeaking && (
            <span className="flex items-center gap-1 text-blue-500">
              <Volume2 className="w-4 h-4 animate-pulse" />
              AI Speaking
            </span>
          )}
        </div>
      )}

      {/* Recording Button */}
      <div className="flex justify-center">
        <Button
          onClick={onToggleRecording}
          size="lg"
          disabled={disabled || isConnecting}
          className={`rounded-full w-32 h-32 flex items-center justify-center text-lg font-semibold transition-all ${
            isConnecting
              ? 'bg-blue-600 text-white hover:bg-blue-700'
              : isRecording || isConnected
              ? 'bg-red-600 text-white hover:bg-red-700 animate-pulse'
              : 'bg-primary text-primary-foreground hover:bg-primary/90'
          }`}
        >
          {isConnecting ? (
            <>
              <Loader2 className="w-6 h-6 mr-2 animate-spin" />
              Connecting
            </>
          ) : isRecording || isConnected ? (
            <>
              <Square className="w-6 h-6 mr-2" />
              End Call
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
          {isConnecting ? (
            <span className="text-blue-500 font-semibold flex items-center justify-center gap-2">
              <Loader2 className="w-3 h-3 animate-spin" />
              Connecting to AI interviewer...
            </span>
          ) : isRecording || isConnected ? (
            <span className="text-red-500 font-semibold flex items-center justify-center gap-2">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
              Voice call in progress...
            </span>
          ) : (
            'Click to start voice interview with AI'
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
