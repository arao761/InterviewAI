'use client';

import { useMemo } from 'react';
import { Card } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function ProgressChart({
  interviews = [],
}: {
  interviews?: Array<{
    id: number;
    date: string;
    score: number;
  }>;
}) {
  const data = useMemo(() => {
    if (interviews.length === 0) {
      return [];
    }

    // Sort interviews by date and format for chart
    const sortedInterviews = [...interviews]
      .filter((i) => i.score > 0)
      .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
      .map((interview) => {
        const date = new Date(interview.date);
        return {
          date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
          score: interview.score,
        };
      });

    return sortedInterviews;
  }, [interviews]);

  if (data.length === 0) {
    return (
      <Card className="bg-card border-border p-6">
        <h3 className="text-xl font-bold mb-6">Performance Trend</h3>
        <div className="flex items-center justify-center h-[300px] text-muted-foreground">
          <p>No interview data available yet. Complete your first interview to see your progress!</p>
        </div>
      </Card>
    );
  }

  return (
    <Card className="bg-card border-border p-6">
      <h3 className="text-xl font-bold mb-6">Performance Trend</h3>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
          <XAxis dataKey="date" stroke="var(--color-muted-foreground)" />
          <YAxis stroke="var(--color-muted-foreground)" domain={[0, 100]} />
          <Tooltip
            contentStyle={{
              backgroundColor: 'var(--color-card)',
              border: '1px solid var(--color-border)',
              borderRadius: '0.5rem',
            }}
            labelStyle={{ color: 'var(--color-foreground)' }}
          />
          <Line
            type="monotone"
            dataKey="score"
            stroke="var(--color-primary)"
            dot={{ fill: 'var(--color-primary)', r: 5 }}
            activeDot={{ r: 7 }}
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </Card>
  );
}
