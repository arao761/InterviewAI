import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Brain, Target, MessageSquare, Sparkles, TrendingUp, CheckCircle } from 'lucide-react';

interface MetricConfig {
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  color: string;
  bgColor: string;
  description: string;
}

const METRIC_CONFIGS: Record<string, MetricConfig> = {
  clarity: {
    label: 'Clarity',
    icon: MessageSquare,
    color: 'text-blue-500',
    bgColor: 'bg-blue-500',
    description: 'How clear and articulate your responses were'
  },
  confidence: {
    label: 'Confidence',
    icon: Sparkles,
    color: 'text-purple-500',
    bgColor: 'bg-purple-500',
    description: 'Your confidence and assertiveness level'
  },
  structure: {
    label: 'Structure',
    icon: Target,
    color: 'text-cyan-500',
    bgColor: 'bg-cyan-500',
    description: 'Organization and logical flow of answers'
  },
  technicalAccuracy: {
    label: 'Technical Accuracy',
    icon: Brain,
    color: 'text-indigo-500',
    bgColor: 'bg-indigo-500',
    description: 'Correctness and depth of technical knowledge'
  },
  engagement: {
    label: 'Engagement',
    icon: TrendingUp,
    color: 'text-pink-500',
    bgColor: 'bg-pink-500',
    description: 'Energy and enthusiasm in delivery'
  }
};

interface EnhancedPerformanceMetricsProps {
  metrics: Record<string, number>;
}

export default function EnhancedPerformanceMetrics({ metrics }: EnhancedPerformanceMetricsProps) {
  const getPerformanceLevel = (score: number) => {
    if (score >= 90) return { label: 'Excellent', color: 'text-green-500' };
    if (score >= 80) return { label: 'Very Good', color: 'text-blue-500' };
    if (score >= 70) return { label: 'Good', color: 'text-cyan-500' };
    if (score >= 60) return { label: 'Fair', color: 'text-yellow-500' };
    return { label: 'Needs Work', color: 'text-red-500' };
  };

  // Calculate average score
  const metricValues = Object.values(metrics).filter(v => typeof v === 'number' && !isNaN(v));
  const averageScore = metricValues.length > 0
    ? Math.round(metricValues.reduce((sum, val) => sum + val, 0) / metricValues.length)
    : 0;

  return (
    <Card className="bg-card border-border p-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-2xl font-bold">Performance Breakdown</h3>
          <p className="text-muted-foreground text-sm mt-1">
            Detailed analysis of your interview performance across key areas
          </p>
        </div>
        <div className="text-right">
          <div className="text-3xl font-bold text-primary">{averageScore}%</div>
          <div className="text-xs text-muted-foreground">Average</div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-6">
        {Object.entries(metrics).map(([key, value]) => {
          const config = METRIC_CONFIGS[key];
          if (!config || typeof value !== 'number' || isNaN(value)) return null;

          const Icon = config.icon;
          const level = getPerformanceLevel(value);

          return (
            <div key={key} className="space-y-3">
              {/* Metric Header */}
              <div className="flex items-center gap-2">
                <div className={`p-2 rounded-lg ${config.bgColor}/10`}>
                  <Icon className={`w-5 h-5 ${config.color}`} />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-semibold text-foreground">{config.label}</p>
                </div>
              </div>

              {/* Score Display */}
              <div className="flex items-baseline gap-2">
                <span className={`text-3xl font-bold ${config.color}`}>{value}</span>
                <span className="text-sm text-muted-foreground">/ 100</span>
              </div>

              {/* Level Badge */}
              <Badge variant="outline" className={`${level.color} border-current`}>
                {level.label}
              </Badge>

              {/* Progress Bar */}
              <div className="w-full h-2.5 bg-muted rounded-full overflow-hidden">
                <div
                  className={`h-full ${config.bgColor} transition-all duration-700 ease-out`}
                  style={{ width: `${value}%` }}
                />
              </div>

              {/* Description */}
              <p className="text-xs text-muted-foreground leading-relaxed">
                {config.description}
              </p>
            </div>
          );
        })}
      </div>

      {/* Overall Performance Insights */}
      <div className="mt-8 pt-6 border-t border-border">
        <h4 className="font-semibold text-sm text-foreground mb-3">Performance Insights</h4>
        <div className="grid md:grid-cols-2 gap-4">
          {/* Top Strength */}
          {metricValues.length > 0 && (() => {
            const topMetric = Object.entries(metrics).reduce((best, [key, val]) => {
              if (typeof val !== 'number' || isNaN(val)) return best;
              if (!best || val > best.value) return { key, value: val };
              return best;
            }, null as { key: string; value: number } | null);

            if (topMetric && METRIC_CONFIGS[topMetric.key]) {
              return (
                <div className="flex items-start gap-3 p-3 bg-green-500/10 rounded-lg border border-green-500/20">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-semibold text-green-500">Top Strength</p>
                    <p className="text-sm text-foreground">
                      {METRIC_CONFIGS[topMetric.key].label} ({topMetric.value}%)
                    </p>
                  </div>
                </div>
              );
            }
          })()}

          {/* Area to Focus */}
          {metricValues.length > 0 && (() => {
            const weakMetric = Object.entries(metrics).reduce((worst, [key, val]) => {
              if (typeof val !== 'number' || isNaN(val)) return worst;
              if (!worst || val < worst.value) return { key, value: val };
              return worst;
            }, null as { key: string; value: number } | null);

            if (weakMetric && METRIC_CONFIGS[weakMetric.key]) {
              return (
                <div className="flex items-start gap-3 p-3 bg-yellow-500/10 rounded-lg border border-yellow-500/20">
                  <Target className="w-5 h-5 text-yellow-500 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-semibold text-yellow-500">Focus Area</p>
                    <p className="text-sm text-foreground">
                      {METRIC_CONFIGS[weakMetric.key].label} ({weakMetric.value}%)
                    </p>
                  </div>
                </div>
              );
            }
          })()}
        </div>
      </div>
    </Card>
  );
}

