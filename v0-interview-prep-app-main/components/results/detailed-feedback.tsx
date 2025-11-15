import { Card } from '@/components/ui/card';
import { AlertCircle, CheckCircle, Lightbulb } from 'lucide-react';

export default function DetailedFeedback({
  questions,
}: {
  questions: Array<{
    id: number;
    question: string;
    score: number;
    feedback: string;
    strengths: string[];
    improvements: string[];
  }>;
}) {
  return (
    <div className="space-y-6">
      <Card className="bg-primary/5 border border-primary/20 p-6">
        <div className="flex gap-4">
          <Lightbulb className="w-5 h-5 text-primary flex-shrink-0 mt-1" />
          <div>
            <h4 className="font-semibold text-foreground mb-2">Key Takeaways</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>• Focus on the STAR method for behavioral questions</li>
              <li>• Include quantifiable metrics in your examples</li>
              <li>• Practice reducing filler words like "um" and "uh"</li>
              <li>• Maintain consistent pacing throughout your responses</li>
            </ul>
          </div>
        </div>
      </Card>

      {questions.map((q) => (
        <Card key={q.id} className="bg-card border-border p-6">
          <div className="mb-4">
            <h4 className="font-semibold text-lg mb-2">Question {q.id}</h4>
            <p className="text-muted-foreground">{q.question}</p>
          </div>

          <div className="space-y-4">
            <div className="bg-muted/50 rounded-lg p-4">
              <p className="text-sm">{q.feedback}</p>
            </div>

            <div className="grid md:grid-cols-3 gap-4">
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <h5 className="font-semibold text-sm">Strengths</h5>
                </div>
                <ul className="space-y-2">
                  {q.strengths.map((s, i) => (
                    <li key={i} className="text-sm text-muted-foreground">
                      • {s}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="md:col-span-2">
                <div className="flex items-center gap-2 mb-3">
                  <AlertCircle className="w-4 h-4 text-yellow-500" />
                  <h5 className="font-semibold text-sm">Areas for Improvement</h5>
                </div>
                <ul className="space-y-2">
                  {q.improvements.map((imp, i) => (
                    <li key={i} className="text-sm text-muted-foreground">
                      • {imp}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}
