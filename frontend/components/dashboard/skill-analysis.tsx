'use client';

import { Card } from '@/components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function SkillAnalysis({
  interviews = [],
}: {
  interviews?: Array<{
    id: number;
    score: number;
  }>;
}) {
  // For now, show empty state since we don't have skill breakdown data
  // This can be enhanced later when we add skill-specific feedback to the backend
  const skills: Array<{ name: string; value: number }> = [];

  if (skills.length === 0) {
    return (
      <Card className="bg-card border-border p-6">
        <h3 className="text-xl font-bold mb-6">Skill Breakdown</h3>
        <div className="flex items-center justify-center h-[250px] text-muted-foreground">
          <p className="text-sm">Skill analysis coming soon</p>
        </div>
      </Card>
    );
  }

  return (
    <Card className="bg-card border-border p-6">
      <h3 className="text-xl font-bold mb-6">Skill Breakdown</h3>

      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={skills} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" horizontal={false} />
          <XAxis type="number" stroke="var(--color-muted-foreground)" domain={[0, 100]} />
          <YAxis dataKey="name" type="category" stroke="var(--color-muted-foreground)" width={70} />
          <Tooltip
            contentStyle={{
              backgroundColor: 'var(--color-card)',
              border: '1px solid var(--color-border)',
            }}
            labelStyle={{ color: 'var(--color-foreground)' }}
          />
          <Bar dataKey="value" fill="var(--color-primary)" radius={[0, 8, 8, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </Card>
  );
}
