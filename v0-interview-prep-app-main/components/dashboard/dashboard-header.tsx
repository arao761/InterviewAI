'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Settings, LogOut } from 'lucide-react';

export default function DashboardHeader() {
  const handleLogout = () => {
    // Clear all session data
    sessionStorage.clear();
    localStorage.clear();
    // Redirect to home
    window.location.href = '/';
  };

  return (
    <div className="bg-card border-b border-border px-6 py-4 flex justify-between items-center">
      <div className="text-xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
        InterviewAI
      </div>

      <div className="flex gap-3">
        <Link href="/settings">
          <Button variant="ghost" size="sm" className="hover:bg-muted">
            <Settings className="w-4 h-4" />
          </Button>
        </Link>
        <Button variant="ghost" size="sm" className="hover:bg-muted" onClick={handleLogout}>
          <LogOut className="w-4 h-4" />
        </Button>
      </div>
    </div>
  );
}
