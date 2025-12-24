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
      <p className="text-muted-foreground mb-8">Choose your interview duration. The AI will dynamically adjust questions to fit the time.</p>

      <div className="space-y-8">
        {/* Duration */}
        <div>
          <label className="block text-sm font-semibold mb-4 text-foreground">Interview Duration</label>
          <div className="grid grid-cols-3 gap-4">
            {['15', '30', '60'].map((duration) => (
              <Card
                key={duration}
                onClick={() => onChange({ duration })}
                className={`p-6 text-center cursor-pointer transition-all border-2 ${
                  data.duration === duration
                    ? 'border-primary bg-primary/5'
                    : 'border-border bg-card hover:border-primary/50'
                }`}
              >
                <div className="text-3xl font-bold">{duration}</div>
                <div className="text-sm text-muted-foreground mt-2">minutes</div>
                <div className="text-xs text-muted-foreground mt-1">
                  {duration === '15' ? '~3-4 questions' : duration === '30' ? '~5-6 questions' : '~10-12 questions'}
                </div>
              </Card>
            ))}
          </div>
          <p className="text-xs text-muted-foreground mt-4 text-center">
            The AI interviewer will wrap up the interview as time runs out
          </p>
        </div>

        {/* Focus Areas */}
        <div>
          <label className="block text-sm font-semibold mb-4 text-foreground">Focus Areas (Optional)</label>
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
