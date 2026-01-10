import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import type { InterviewEvaluationReport } from '@/lib/api/types';

interface ScoreBreakdownProps {
  evaluation: InterviewEvaluationReport;
}

export default function ScoreBreakdown({ evaluation }: ScoreBreakdownProps) {
  const overallScore = Math.round(evaluation.overall_score || 0);
  const technicalScore = evaluation.technical_score ? Math.round(evaluation.technical_score) : null;
  const behavioralScore = evaluation.behavioral_score ? Math.round(evaluation.behavioral_score) : null;
  const questionScores = evaluation.question_scores || [];
  const individualEvals = evaluation.individual_evaluations || [];

  // Calculate score distribution
  const scoreDistribution = {
    excellent: individualEvals.filter(e => e.score >= 90).length,
    good: individualEvals.filter(e => e.score >= 70 && e.score < 90).length,
    fair: individualEvals.filter(e => e.score >= 50 && e.score < 70).length,
    needsWork: individualEvals.filter(e => e.score < 50).length,
  };

  // Calculate average, min, max scores
  const scores = individualEvals.map(e => e.score).filter(s => !isNaN(s));
  const avgScore = scores.length > 0 ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : 0;
  const minScore = scores.length > 0 ? Math.round(Math.min(...scores)) : 0;
  const maxScore = scores.length > 0 ? Math.round(Math.max(...scores)) : 0;

  // Determine trend icon
  const getTrendIcon = (score: number, average: number) => {
    if (score > average + 5) return <TrendingUp className="w-4 h-4 text-green-500" />;
    if (score < average - 5) return <TrendingDown className="w-4 h-4 text-red-500" />;
    return <Minus className="w-4 h-4 text-muted-foreground" />;
  };

  return (
    <Card className="bg-card border-border p-6">
      <h3 className="text-xl font-bold mb-6">Score Breakdown</h3>

      {/* Overall Score Summary */}
      <div className="grid md:grid-cols-3 gap-4 mb-6">
        {/* Overall Score */}
        <div className="bg-gradient-to-br from-primary/10 to-primary/5 rounded-lg p-4 border border-primary/20">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm text-muted-foreground">Overall Score</p>
            {getTrendIcon(overallScore, avgScore)}
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-bold text-primary">{overallScore}</span>
            <span className="text-sm text-muted-foreground">/ 100</span>
          </div>
        </div>

        {/* Technical Score (if available) */}
        {technicalScore !== null && (
          <div className="bg-gradient-to-br from-indigo-500/10 to-indigo-500/5 rounded-lg p-4 border border-indigo-500/20">
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm text-muted-foreground">Technical</p>
              {getTrendIcon(technicalScore, avgScore)}
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-4xl font-bold text-indigo-500">{technicalScore}</span>
              <span className="text-sm text-muted-foreground">/ 100</span>
            </div>
          </div>
        )}

        {/* Behavioral Score (if available) */}
        {behavioralScore !== null && (
          <div className="bg-gradient-to-br from-purple-500/10 to-purple-500/5 rounded-lg p-4 border border-purple-500/20">
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm text-muted-foreground">Behavioral</p>
              {getTrendIcon(behavioralScore, avgScore)}
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-4xl font-bold text-purple-500">{behavioralScore}</span>
              <span className="text-sm text-muted-foreground">/ 100</span>
            </div>
          </div>
        )}
      </div>

      {/* Statistics Row */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="text-center p-3 bg-muted/50 rounded-lg">
          <p className="text-2xl font-bold text-green-500">{maxScore}</p>
          <p className="text-xs text-muted-foreground mt-1">Highest Score</p>
        </div>
        <div className="text-center p-3 bg-muted/50 rounded-lg">
          <p className="text-2xl font-bold text-primary">{avgScore}</p>
          <p className="text-xs text-muted-foreground mt-1">Average Score</p>
        </div>
        <div className="text-center p-3 bg-muted/50 rounded-lg">
          <p className="text-2xl font-bold text-yellow-500">{minScore}</p>
          <p className="text-xs text-muted-foreground mt-1">Lowest Score</p>
        </div>
      </div>

      {/* Score Distribution */}
      {individualEvals.length > 0 && (
        <>
          <div className="mb-4">
            <p className="text-sm font-semibold text-foreground mb-3">Score Distribution</p>
            <div className="space-y-2">
              {/* Excellent (90-100) */}
              <div className="flex items-center gap-3">
                <div className="w-24 text-sm text-muted-foreground">Excellent</div>
                <div className="flex-1 h-8 bg-muted rounded-lg overflow-hidden">
                  <div
                    className="h-full bg-green-500 transition-all duration-500 flex items-center justify-end px-3"
                    style={{ width: `${(scoreDistribution.excellent / individualEvals.length) * 100}%` }}
                  >
                    {scoreDistribution.excellent > 0 && (
                      <span className="text-xs font-semibold text-white">{scoreDistribution.excellent}</span>
                    )}
                  </div>
                </div>
                <Badge variant="outline" className="text-green-500 border-green-500 min-w-[50px] justify-center">
                  {scoreDistribution.excellent}
                </Badge>
              </div>

              {/* Good (70-89) */}
              <div className="flex items-center gap-3">
                <div className="w-24 text-sm text-muted-foreground">Good</div>
                <div className="flex-1 h-8 bg-muted rounded-lg overflow-hidden">
                  <div
                    className="h-full bg-blue-500 transition-all duration-500 flex items-center justify-end px-3"
                    style={{ width: `${(scoreDistribution.good / individualEvals.length) * 100}%` }}
                  >
                    {scoreDistribution.good > 0 && (
                      <span className="text-xs font-semibold text-white">{scoreDistribution.good}</span>
                    )}
                  </div>
                </div>
                <Badge variant="outline" className="text-blue-500 border-blue-500 min-w-[50px] justify-center">
                  {scoreDistribution.good}
                </Badge>
              </div>

              {/* Fair (50-69) */}
              <div className="flex items-center gap-3">
                <div className="w-24 text-sm text-muted-foreground">Fair</div>
                <div className="flex-1 h-8 bg-muted rounded-lg overflow-hidden">
                  <div
                    className="h-full bg-yellow-500 transition-all duration-500 flex items-center justify-end px-3"
                    style={{ width: `${(scoreDistribution.fair / individualEvals.length) * 100}%` }}
                  >
                    {scoreDistribution.fair > 0 && (
                      <span className="text-xs font-semibold text-white">{scoreDistribution.fair}</span>
                    )}
                  </div>
                </div>
                <Badge variant="outline" className="text-yellow-500 border-yellow-500 min-w-[50px] justify-center">
                  {scoreDistribution.fair}
                </Badge>
              </div>

              {/* Needs Work (0-49) */}
              <div className="flex items-center gap-3">
                <div className="w-24 text-sm text-muted-foreground">Needs Work</div>
                <div className="flex-1 h-8 bg-muted rounded-lg overflow-hidden">
                  <div
                    className="h-full bg-red-500 transition-all duration-500 flex items-center justify-end px-3"
                    style={{ width: `${(scoreDistribution.needsWork / individualEvals.length) * 100}%` }}
                  >
                    {scoreDistribution.needsWork > 0 && (
                      <span className="text-xs font-semibold text-white">{scoreDistribution.needsWork}</span>
                    )}
                  </div>
                </div>
                <Badge variant="outline" className="text-red-500 border-red-500 min-w-[50px] justify-center">
                  {scoreDistribution.needsWork}
                </Badge>
              </div>
            </div>
          </div>

          {/* Total Questions */}
          <div className="pt-4 border-t border-border">
            <div className="flex justify-between items-center">
              <p className="text-sm text-muted-foreground">Total Questions Answered</p>
              <Badge variant="outline" className="text-lg px-4 py-1">
                {individualEvals.length}
              </Badge>
            </div>
          </div>
        </>
      )}
    </Card>
  );
}
