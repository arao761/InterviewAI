import { Card } from '@/components/ui/card';

export default function JobDetailsForm({
  data,
  onChange,
}: {
  data: {
    jobTitle: string;
    company: string;
    industry: string;
    yearsOfExperience: string;
  };
  onChange: (updates: Partial<typeof data>) => void;
}) {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">Job Details</h2>
      <p className="text-muted-foreground mb-8">Tell us about the position you're interviewing for</p>

      <div className="space-y-6">
        {[
          { label: 'Job Title (optional)', value: 'jobTitle', placeholder: 'e.g., Senior Software Engineer' },
          { label: 'Company (optional)', value: 'company', placeholder: 'e.g., Google' },
          { label: 'Industry (optional)', value: 'industry', placeholder: 'e.g., Technology' },
          { label: 'Years of Experience (optional)', value: 'yearsOfExperience', placeholder: 'e.g., 5' },
        ].map((field) => (
          <div key={field.value}>
            <label className="block text-sm font-semibold mb-2 text-foreground">{field.label}</label>
            <input
              type="text"
              value={data[field.value as keyof typeof data]}
              onChange={(e) => onChange({ [field.value]: e.target.value } as any)}
              placeholder={field.placeholder}
              className="w-full px-4 py-2 bg-muted border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary transition-colors"
            />
          </div>
        ))}
      </div>
    </div>
  );
}
