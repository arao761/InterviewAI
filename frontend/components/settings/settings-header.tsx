import { Button } from '@/components/ui/button';

export default function SettingsHeader() {
  return (
    <div className="bg-card border-b border-border px-6 py-4 flex justify-between items-center">
      <div className="text-xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
        InterviewAI
      </div>

      <div className="flex gap-3">
        <Button variant="ghost" size="sm" className="hover:bg-muted">
          Help
        </Button>
      </div>
    </div>
  );
}
