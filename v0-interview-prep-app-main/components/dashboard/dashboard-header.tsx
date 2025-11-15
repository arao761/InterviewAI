import { Button } from '@/components/ui/button';
import { Settings, LogOut } from 'lucide-react';

export default function DashboardHeader() {
  return (
    <div className="bg-card border-b border-border px-6 py-4 flex justify-between items-center">
      <div className="text-xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
        InterviewAI
      </div>

      <div className="flex gap-3">
        <Button variant="ghost" size="sm" className="hover:bg-muted">
          <Settings className="w-4 h-4" />
        </Button>
        <Button variant="ghost" size="sm" className="hover:bg-muted">
          <LogOut className="w-4 h-4" />
        </Button>
      </div>
    </div>
  );
}
