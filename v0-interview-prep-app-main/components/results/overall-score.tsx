import { Card } from '@/components/ui/card';

export default function OverallScore({ score }: { score: number }) {
  let scoreLevel = '';
  let scoreColor = '';

  if (score >= 90) {
    scoreLevel = 'Excellent';
    scoreColor = 'text-green-500';
  } else if (score >= 80) {
    scoreLevel = 'Good';
    scoreColor = 'text-blue-500';
  } else if (score >= 70) {
    scoreLevel = 'Fair';
    scoreColor = 'text-yellow-500';
  } else {
    scoreLevel = 'Needs Improvement';
    scoreColor = 'text-red-500';
  }

  return (
    <Card className="bg-gradient-to-br from-card to-card border-border p-8">
      <div className="flex flex-col md:flex-row items-center justify-between gap-8">
        <div>
          <p className="text-muted-foreground text-sm mb-2">Overall Performance</p>
          <h2 className="text-5xl font-bold mb-2">{score}/100</h2>
          <p className={`text-lg font-semibold ${scoreColor}`}>{scoreLevel}</p>
        </div>

        <div className="relative w-48 h-48">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 200 200">
            {/* Background circle */}
            <circle cx="100" cy="100" r="90" fill="none" stroke="currentColor" strokeWidth="8" className="text-muted opacity-20" />

            {/* Progress circle */}
            <circle
              cx="100"
              cy="100"
              r="90"
              fill="none"
              stroke="currentColor"
              strokeWidth="8"
              strokeDasharray={`${(score / 100) * 565.48} 565.48`}
              className={scoreColor}
              strokeLinecap="round"
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <div className="text-4xl font-bold">{score}</div>
              <div className="text-xs text-muted-foreground mt-1">% Score</div>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}
