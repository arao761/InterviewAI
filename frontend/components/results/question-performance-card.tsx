import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CheckCircle2, AlertCircle, TrendingUp, Lightbulb } from 'lucide-react';
import type { ResponseEvaluation, InterviewQuestion } from '@/lib/api/types';

interface QuestionPerformanceCardProps {
  question: InterviewQuestion | any;
  evaluation: ResponseEvaluation;
  index: number;
}

export default function QuestionPerformanceCard({
  question,
  evaluation,
  index
}: QuestionPerformanceCardProps) {
  const score = Math.round(evaluation.score);

  // Determine score level and styling
  const getScoreLevel = (score: number) => {
    if (score >= 90) return { label: 'Excellent', color: 'text-green-500', bgColor: 'bg-green-500/10', borderColor: 'border-green-500/20' };
    if (score >= 80) return { label: 'Very Good', color: 'text-blue-500', bgColor: 'bg-blue-500/10', borderColor: 'border-blue-500/20' };
    if (score >= 70) return { label: 'Good', color: 'text-cyan-500', bgColor: 'bg-cyan-500/10', borderColor: 'border-cyan-500/20' };
    if (score >= 60) return { label: 'Fair', color: 'text-yellow-500', bgColor: 'bg-yellow-500/10', borderColor: 'border-yellow-500/20' };
    return { label: 'Needs Work', color: 'text-red-500', bgColor: 'bg-red-500/10', borderColor: 'border-red-500/20' };
  };

  const scoreLevel = getScoreLevel(score);
  const questionText = question?.question || question?.text || `Question ${index + 1}`;

  return (
    <Card className={`bg-card border-border ${scoreLevel.borderColor} p-6 hover:shadow-lg transition-all duration-300`}>
      {/* Header Section */}
      <div className="flex justify-between items-start gap-4 mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <Badge variant="outline" className="px-3 py-1">
              Q{index + 1}
            </Badge>
            {question?.type && (
              <Badge variant="secondary" className="capitalize">
                {question.type}
              </Badge>
            )}
            {question?.difficulty && (
              <Badge
                variant="outline"
                className={
                  question.difficulty === 'hard' ? 'border-red-500 text-red-500' :
                  question.difficulty === 'medium' ? 'border-yellow-500 text-yellow-500' :
                  'border-green-500 text-green-500'
                }
              >
                {question.difficulty}
              </Badge>
            )}
          </div>
          <h3 className="font-semibold text-lg leading-tight text-foreground">
            {questionText}
          </h3>
        </div>

        {/* Score Display */}
        <div className="flex flex-col items-end gap-1 min-w-[100px]">
          <div className={`text-4xl font-bold ${scoreLevel.color}`}>
            {score}
          </div>
          <div className="text-xs text-muted-foreground">out of 100</div>
          <Badge className={`${scoreLevel.bgColor} ${scoreLevel.color} border-0 mt-1`}>
            {scoreLevel.label}
          </Badge>
        </div>
      </div>

      {/* Score Progress Bar */}
      <div className="mb-6">
        <div className="w-full h-3 bg-muted rounded-full overflow-hidden">
          <div
            className={`h-full ${scoreLevel.color.replace('text-', 'bg-')} transition-all duration-500 rounded-full`}
            style={{ width: `${score}%` }}
          />
        </div>
      </div>

      {/* Feedback Section */}
      {evaluation.feedback && (
        <div className={`${scoreLevel.bgColor} rounded-lg p-4 mb-4`}>
          <div className="flex items-start gap-2">
            <Lightbulb className={`w-5 h-5 mt-0.5 flex-shrink-0 ${scoreLevel.color}`} />
            <p className="text-sm text-foreground leading-relaxed">{evaluation.feedback}</p>
          </div>
        </div>
      )}

      {/* Strengths and Weaknesses Grid */}
      <div className="grid md:grid-cols-2 gap-6 mb-4">
        {/* Strengths */}
        {evaluation.strengths && evaluation.strengths.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-3">
              <CheckCircle2 className="w-5 h-5 text-green-500" />
              <h4 className="font-semibold text-sm text-green-500">
                Strengths ({evaluation.strengths.length})
              </h4>
            </div>
            <ul className="space-y-2">
              {evaluation.strengths.map((strength, i) => (
                <li key={i} className="flex items-start gap-2 text-sm">
                  <span className="text-green-500 mt-1 flex-shrink-0">✓</span>
                  <span className="text-foreground/90">{strength}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Weaknesses / Areas to Improve */}
        {evaluation.weaknesses && evaluation.weaknesses.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-3">
              <AlertCircle className="w-5 h-5 text-yellow-500" />
              <h4 className="font-semibold text-sm text-yellow-500">
                Areas to Improve ({evaluation.weaknesses.length})
              </h4>
            </div>
            <ul className="space-y-2">
              {evaluation.weaknesses.map((weakness, i) => (
                <li key={i} className="flex items-start gap-2 text-sm">
                  <span className="text-yellow-500 mt-1 flex-shrink-0">→</span>
                  <span className="text-foreground/90">{weakness}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Suggestions Section */}
      {evaluation.suggestions && evaluation.suggestions.length > 0 && (
        <div className="mt-4 pt-4 border-t border-border">
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp className="w-5 h-5 text-primary" />
            <h4 className="font-semibold text-sm text-foreground">
              Improvement Suggestions
            </h4>
          </div>
          <ul className="space-y-2">
            {evaluation.suggestions.map((suggestion, i) => (
              <li key={i} className="flex items-start gap-2 text-sm">
                <span className="text-primary mt-1 flex-shrink-0">•</span>
                <span className="text-foreground/90">{suggestion}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Key Takeaways (if available) */}
      {evaluation.key_takeaways && evaluation.key_takeaways.length > 0 && (
        <div className="mt-4 pt-4 border-t border-border">
          <h4 className="font-semibold text-sm text-foreground mb-3">
            Key Takeaways
          </h4>
          <ul className="space-y-2">
            {evaluation.key_takeaways.map((takeaway, i) => (
              <li key={i} className="flex items-start gap-2 text-sm">
                <span className="text-primary mt-1 flex-shrink-0">•</span>
                <span className="text-foreground/90">{takeaway}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </Card>
  );
}
