import { ArrowLeft, Info, Wifi, WifiOff, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function InterviewHeader({
  questionNumber,
  totalQuestions,
  onExit,
  isConnected = false,
  isConnecting = false,
}: {
  questionNumber: number;
  totalQuestions: number;
  onExit: () => void;
  isConnected?: boolean;
  isConnecting?: boolean;
}) {
  return (
    <div className="bg-card border-b border-border px-6 py-4 flex justify-between items-center">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" className="hover:bg-muted" onClick={onExit}>
          <ArrowLeft className="w-4 h-4 mr-2" />
          Exit
        </Button>
        <div className="h-6 w-px bg-border"></div>
        <div className="text-sm text-muted-foreground">
          Question <span className="font-semibold text-foreground">{questionNumber}</span> of{' '}
          <span className="font-semibold text-foreground">{totalQuestions}</span>
        </div>
      </div>

      <div className="flex items-center gap-3">
        {/* Connection Status */}
        <div className="flex items-center gap-2 text-sm">
          {isConnecting ? (
            <>
              <Loader2 className="w-4 h-4 text-blue-500 animate-spin" />
              <span className="text-blue-500">Connecting...</span>
            </>
          ) : isConnected ? (
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

        <Button variant="ghost" size="sm" className="hover:bg-muted">
          <Info className="w-4 h-4" />
        </Button>
      </div>
    </div>
  );
}
