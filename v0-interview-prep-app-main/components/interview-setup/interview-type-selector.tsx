import { Card } from '@/components/ui/card';
import { Code, Users } from 'lucide-react';

const interviewTypes = [
  {
    id: 'technical',
    name: 'Technical Interview',
    description: 'Practice coding and technical problem-solving',
    icon: Code,
  },
  {
    id: 'behavioral',
    name: 'Behavioral Interview',
    description: 'Master situational and competency-based questions',
    icon: Users,
  },
];

export default function InterviewTypeSelector({
  value,
  onChange,
}: {
  value: string;
  onChange: (type: string) => void;
}) {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">Select Interview Type</h2>
      <p className="text-muted-foreground mb-8">Choose the type of interview you want to practice</p>

      <div className="grid md:grid-cols-2 gap-4">
        {interviewTypes.map((type) => {
          const Icon = type.icon;
          return (
            <Card
              key={type.id}
              onClick={() => onChange(type.id)}
              className={`p-6 cursor-pointer transition-all border-2 ${
                value === type.id
                  ? 'border-primary bg-primary/5'
                  : 'border-border bg-card hover:border-primary/50'
              }`}
            >
              <div className="flex items-start gap-4">
                <div
                  className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                    value === type.id ? 'bg-primary/20' : 'bg-muted'
                  }`}
                >
                  <Icon className={`w-5 h-5 ${value === type.id ? 'text-primary' : 'text-muted-foreground'}`} />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold mb-1">{type.name}</h3>
                  <p className="text-sm text-muted-foreground">{type.description}</p>
                </div>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
