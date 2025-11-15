import { Card } from '@/components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function SkillAnalysis() {
  const skills = [
    { name: 'Clarity', value: 85 },
    { name: 'Confidence', value: 72 },
    { name: 'Structure', value: 80 },
    { name: 'Engagement', value: 88 },
  ];

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
