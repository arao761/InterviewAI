import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';

export default function ResultsHeader() {
  return (
    <div className="bg-card border-b border-border px-6 py-4">
      <Link href="/dashboard">
        <Button variant="ghost" size="sm" className="hover:bg-muted">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back
        </Button>
      </Link>
    </div>
  );
}
