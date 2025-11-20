import { ArrowLeft, Info } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function InterviewHeader({
  questionNumber,
  totalQuestions,
  onExit,
}: {
  questionNumber: number;
  totalQuestions: number;
  onExit: () => void;
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

      <Button variant="ghost" size="sm" className="hover:bg-muted">
        <Info className="w-4 h-4" />
      </Button>
    </div>
  );
}
