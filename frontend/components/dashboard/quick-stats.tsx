'use client';

import { Card } from '@/components/ui/card';
import { TrendingUp, Target, Zap, Clock } from 'lucide-react';
import { useScrollFadeIn } from '@/hooks/use-scroll-fade-in';

export default function QuickStats({
  stats,
}: {
  stats: {
    totalInterviews: number;
    averageScore: number;
    bestScore: number | null;
    hoursSpent: number;
  };
}) {
  const fadeInRef = useScrollFadeIn();

  const statItems = [
    {
      label: 'Total Interviews',
      value: stats.totalInterviews,
      icon: Zap,
      color: 'text-blue-500',
      bgColor: 'bg-blue-500/10',
    },
    {
      label: 'Average Score',
      value: `${stats.averageScore}%`,
      icon: TrendingUp,
      color: 'text-green-500',
      bgColor: 'bg-green-500/10',
    },
    {
      label: 'Best Score',
      value: stats.bestScore !== null ? `${stats.bestScore}%` : 'N/A',
      icon: Target,
      color: 'text-purple-500',
      bgColor: 'bg-purple-500/10',
    },
    {
      label: 'Hours Practiced',
      value: stats.hoursSpent,
      icon: Clock,
      color: 'text-orange-500',
      bgColor: 'bg-orange-500/10',
    },
  ];

  return (
    <div ref={fadeInRef} className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 fade-in-animation">
      {statItems.map((stat) => {
        const Icon = stat.icon;
        return (
          <Card key={stat.label} className="bg-card border-border p-6">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <p className="text-sm text-muted-foreground mb-2">{stat.label}</p>
                <p className="text-3xl font-bold">{stat.value}</p>
              </div>
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${stat.bgColor}`}>
                <Icon className={`w-5 h-5 ${stat.color}`} />
              </div>
            </div>
          </Card>
        );
      })}
    </div>
  );
}
