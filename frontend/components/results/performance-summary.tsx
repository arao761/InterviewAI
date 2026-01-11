import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Trophy, Target, TrendingUp, Lightbulb, Star, Award } from 'lucide-react';
import type { InterviewEvaluationReport } from '@/lib/api/types';

interface PerformanceSummaryProps {
  evaluation: InterviewEvaluationReport;
}

export default function PerformanceSummary({ evaluation }: PerformanceSummaryProps) {
  const overallScore = Math.round(evaluation.overall_score || 0);
  const individualEvals = evaluation.individual_evaluations || [];

  // Calculate consistency
  const scores = individualEvals.map(e => e.score).filter(s => !isNaN(s));
  const avgScore = scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;
  const variance = scores.length > 0
    ? scores.reduce((sum, score) => sum + Math.pow(score - avgScore, 2), 0) / scores.length
    : 0;
  const stdDev = Math.sqrt(variance);
  const consistency = Math.max(0, 100 - stdDev);

  // Determine performance badges
  const badges = [];
  if (overallScore >= 90) badges.push({ icon: Trophy, label: 'Outstanding', color: 'text-yellow-500', bg: 'bg-yellow-500/10' });
  if (overallScore >= 85) badges.push({ icon: Award, label: 'Excellence', color: 'text-purple-500', bg: 'bg-purple-500/10' });
  if (consistency >= 80) badges.push({ icon: Target, label: 'Consistent', color: 'text-blue-500', bg: 'bg-blue-500/10' });

  const excellentCount = individualEvals.filter(e => e.score >= 90).length;
  if (excellentCount >= 3) badges.push({ icon: Star, label: 'High Performer', color: 'text-cyan-500', bg: 'bg-cyan-500/10' });

  // Get top performing question
  const topQuestion = individualEvals.reduce((best, current, index) => {
    if (!best || current.score > best.eval.score) {
      return { eval: current, index };
    }
    return best;
  }, null as { eval: any; index: number } | null);

  return (
    <div className="grid md:grid-cols-2 gap-6">
      {/* Key Highlights Card */}
      <Card className="bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20 p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-3 bg-primary/20 rounded-lg">
            <Trophy className="w-6 h-6 text-primary" />
          </div>
          <h3 className="text-xl font-bold">Key Highlights</h3>
        </div>

        <div className="space-y-4">
          {/* Achievement Badges */}
          {badges.length > 0 && (
            <div>
              <p className="text-sm text-muted-foreground mb-2">Achievements</p>
              <div className="flex flex-wrap gap-2">
                {badges.map((badge, i) => {
                  const Icon = badge.icon;
                  return (
                    <Badge
                      key={i}
                      variant="outline"
                      className={`${badge.bg} ${badge.color} border-current px-3 py-1.5`}
                    >
                      <Icon className="w-3 h-3 mr-1.5" />
                      {badge.label}
                    </Badge>
                  );
                })}
              </div>
            </div>
          )}

          {/* Top Performance */}
          {topQuestion && (
            <div className="pt-4 border-t border-border/50">
              <p className="text-sm text-muted-foreground mb-2">Best Performance</p>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Question {topQuestion.index + 1}</span>
                <Badge className="bg-green-500/10 text-green-500 border-0 text-lg px-3 py-1">
                  {Math.round(topQuestion.eval.score)}%
                </Badge>
              </div>
            </div>
          )}

          {/* Consistency Score */}
          <div className="pt-4 border-t border-border/50">
            <p className="text-sm text-muted-foreground mb-2">Consistency</p>
            <div className="flex items-center gap-3">
              <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                <div
                  className="h-full bg-primary transition-all duration-500"
                  style={{ width: `${consistency}%` }}
                />
              </div>
              <span className="text-sm font-semibold text-primary">{Math.round(consistency)}%</span>
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              {consistency >= 80
                ? 'Highly consistent performance across questions'
                : consistency >= 60
                ? 'Good consistency with some variation'
                : 'Consider practicing to improve consistency'}
            </p>
          </div>
        </div>
      </Card>

      {/* Strengths & Growth Areas */}
      <Card className="bg-card border-border p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-3 bg-green-500/10 rounded-lg">
            <TrendingUp className="w-6 h-6 text-green-500" />
          </div>
          <h3 className="text-xl font-bold">What You Did Well</h3>
        </div>

        <div className="space-y-4">
          {/* Top Strengths */}
          {evaluation.strengths && evaluation.strengths.length > 0 && (
            <div>
              <ul className="space-y-2">
                {evaluation.strengths.slice(0, 3).map((strength, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <span className="text-green-500 mt-1 flex-shrink-0">✓</span>
                    <span className="text-foreground/90">{strength}</span>
                  </li>
                ))}
              </ul>
              {evaluation.strengths.length > 3 && (
                <p className="text-xs text-muted-foreground mt-2 ml-5">
                  +{evaluation.strengths.length - 3} more strengths
                </p>
              )}
            </div>
          )}

          {/* Growth Areas */}
          {evaluation.areas_for_improvement && evaluation.areas_for_improvement.length > 0 && (
            <div className="pt-4 border-t border-border">
              <div className="flex items-center gap-2 mb-3">
                <Lightbulb className="w-4 h-4 text-yellow-500" />
                <h4 className="text-sm font-semibold text-foreground">Priority Focus Areas</h4>
              </div>
              <ul className="space-y-2">
                {evaluation.areas_for_improvement.slice(0, 2).map((area, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <span className="text-yellow-500 mt-1 flex-shrink-0">→</span>
                    <span className="text-foreground/90">{area}</span>
                  </li>
                ))}
              </ul>
              {evaluation.areas_for_improvement.length > 2 && (
                <p className="text-xs text-muted-foreground mt-2 ml-5">
                  +{evaluation.areas_for_improvement.length - 2} more areas to focus on
                </p>
              )}
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}
