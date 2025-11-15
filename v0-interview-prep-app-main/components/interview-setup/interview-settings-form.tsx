import { Card } from '@/components/ui/card';

const focusAreaOptions = [
  'Communication',
  'Technical Skills',
  'Problem Solving',
  'Leadership',
  'Team Collaboration',
  'Time Management',
];

export default function InterviewSettingsForm({
  data,
  onChange,
}: {
  data: {
    duration: string;
    numberOfQuestions: string;
    focusAreas: string[];
  };
  onChange: (updates: Partial<typeof data>) => void;
}) {
  const toggleFocusArea = (area: string) => {
    const updated = data.focusAreas.includes(area)
      ? data.focusAreas.filter((a) => a !== area)
      : [...data.focusAreas, area];
    onChange({ focusAreas: updated });
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">Interview Settings</h2>
      <p className="text-muted-foreground mb-8">Customize your interview experience</p>

      <div className="space-y-8">
        {/* Duration */}
        <div>
          <label className="block text-sm font-semibold mb-4 text-foreground">Interview Duration</label>
          <div className="grid grid-cols-3 gap-4">
            {['15', '30', '60'].map((duration) => (
              <Card
                key={duration}
                onClick={() => onChange({ duration })}
                className={`p-4 text-center cursor-pointer transition-all border-2 ${
                  data.duration === duration
                    ? 'border-primary bg-primary/5'
                    : 'border-border bg-card hover:border-primary/50'
                }`}
              >
                <div className="text-2xl font-bold">{duration}</div>
                <div className="text-xs text-muted-foreground mt-1">minutes</div>
              </Card>
            ))}
          </div>
        </div>

        {/* Number of Questions */}
        <div>
          <label className="block text-sm font-semibold mb-4 text-foreground">Number of Questions</label>
          <div className="grid grid-cols-3 gap-4">
            {['3', '5', '10'].map((num) => (
              <Card
                key={num}
                onClick={() => onChange({ numberOfQuestions: num })}
                className={`p-4 text-center cursor-pointer transition-all border-2 ${
                  data.numberOfQuestions === num
                    ? 'border-primary bg-primary/5'
                    : 'border-border bg-card hover:border-primary/50'
                }`}
              >
                <div className="text-2xl font-bold">{num}</div>
                <div className="text-xs text-muted-foreground mt-1">questions</div>
              </Card>
            ))}
          </div>
        </div>

        {/* Focus Areas */}
        <div>
          <label className="block text-sm font-semibold mb-4 text-foreground">Focus Areas (Select at least 1)</label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {focusAreaOptions.map((area) => (
              <Card
                key={area}
                onClick={() => toggleFocusArea(area)}
                className={`p-3 text-center cursor-pointer transition-all border-2 ${
                  data.focusAreas.includes(area)
                    ? 'border-primary bg-primary/5'
                    : 'border-border bg-card hover:border-primary/50'
                }`}
              >
                <div className="text-sm font-medium">{area}</div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
