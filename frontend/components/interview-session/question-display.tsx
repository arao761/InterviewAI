import { Card } from '@/components/ui/card';
import { Lightbulb } from 'lucide-react';

export default function QuestionDisplay({
  question,
  questionNumber,
  totalQuestions,
}: {
  question: string;
  questionNumber: number;
  totalQuestions: number;
}) {
  return (
    <div className="max-w-2xl">
      <div className="mb-6">
        <span className="text-sm font-semibold text-primary">Question {questionNumber} of {totalQuestions}</span>
      </div>

      <Card className="bg-card border-border p-8 mb-6">
        <div className="flex gap-4">
          <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
            <Lightbulb className="w-5 h-5 text-primary" />
          </div>
          <h2 className="text-3xl font-bold text-balance">{question}</h2>
        </div>
      </Card>

      <div className="bg-primary/5 border border-primary/20 rounded-lg p-4">
        <p className="text-sm text-muted-foreground">
          Tip: Take a moment to think before responding. Speak clearly and structure your answer with a beginning, middle, and end.
        </p>
      </div>
    </div>
  );
}
