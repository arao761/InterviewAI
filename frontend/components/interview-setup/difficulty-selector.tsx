import { Card } from '@/components/ui/card';
import { Zap, TrendingUp, Flame } from 'lucide-react';

const difficulties = [
  {
    id: 'beginner',
    name: 'Beginner',
    description: 'Start with the basics',
    icon: Zap,
    color: 'text-green-500',
    bgColor: 'bg-green-500/10',
  },
  {
    id: 'intermediate',
    name: 'Intermediate',
    description: 'Challenge yourself',
    icon: TrendingUp,
    color: 'text-yellow-500',
    bgColor: 'bg-yellow-500/10',
  },
  {
    id: 'advanced',
    name: 'Advanced',
    description: 'Master-level questions',
    icon: Flame,
    color: 'text-red-500',
    bgColor: 'bg-red-500/10',
  },
];

export default function DifficultySelector({
  value,
  onChange,
}: {
  value: string;
  onChange: (difficulty: string) => void;
}) {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">Select Difficulty</h2>
      <p className="text-muted-foreground mb-8">Choose your preferred difficulty level</p>

      <div className="grid md:grid-cols-3 gap-4">
        {difficulties.map((difficulty) => {
          const Icon = difficulty.icon;
          return (
            <Card
              key={difficulty.id}
              onClick={() => onChange(difficulty.id)}
              className={`p-6 cursor-pointer transition-all border-2 ${
                value === difficulty.id
                  ? 'border-primary bg-primary/5'
                  : 'border-border bg-card hover:border-primary/50'
              }`}
            >
              <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${difficulty.bgColor} mb-4`}>
                <Icon className={`w-6 h-6 ${difficulty.color}`} />
              </div>
              <h3 className="font-semibold mb-1">{difficulty.name}</h3>
              <p className="text-sm text-muted-foreground">{difficulty.description}</p>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
