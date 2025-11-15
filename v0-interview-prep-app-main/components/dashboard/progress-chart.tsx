'use client';

import { Card } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function ProgressChart() {
  const data = [
    { date: 'Oct 22', score: 70 },
    { date: 'Oct 29', score: 73 },
    { date: 'Nov 5', score: 78 },
    { date: 'Nov 12', score: 81 },
    { date: 'Nov 15', score: 82 },
  ];

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
