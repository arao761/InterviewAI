'use client';

import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Eye, Download, Trash2 } from 'lucide-react';

export default function InterviewHistory({
  interviews,
}: {
  interviews: Array<{
    id: number;
    type: string;
    company: string;
    date: string;
    score: number;
    duration: string;
    status: string;
  }>;
}) {
  const [sortBy, setSortBy] = useState('date');

  const getScoreBadgeColor = (score: number) => {
    if (score >= 85) return 'bg-green-500/20 text-green-500';
    if (score >= 75) return 'bg-blue-500/20 text-blue-500';
    return 'bg-yellow-500/20 text-yellow-500';
  };

  return (
    <Card className="bg-card border-border overflow-hidden">
      <div className="p-6 border-b border-border flex justify-between items-center">
        <h3 className="text-xl font-bold">Interview History</h3>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="px-3 py-1 bg-muted border border-border rounded text-sm focus:outline-none"
        >
          <option value="date">Sort by Date</option>
          <option value="score">Sort by Score</option>
          <option value="type">Sort by Type</option>
        </select>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-border">
              <th className="px-6 py-3 text-left text-xs font-semibold text-muted-foreground">Interview</th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-muted-foreground">Date</th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-muted-foreground">Duration</th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-muted-foreground">Score</th>
              <th className="px-6 py-3 text-right text-xs font-semibold text-muted-foreground">Actions</th>
            </tr>
          </thead>
          <tbody>
            {interviews.map((interview) => (
              <tr key={interview.id} className="border-b border-border hover:bg-muted/50 transition-colors">
                <td className="px-6 py-4">
                  <div>
                    <p className="font-semibold text-foreground">{interview.type}</p>
                    <p className="text-sm text-muted-foreground">{interview.company}</p>
                  </div>
                </td>
                <td className="px-6 py-4 text-sm text-muted-foreground">
                  {new Date(interview.date).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric',
                  })}
                </td>
                <td className="px-6 py-4 text-sm text-muted-foreground">{interview.duration}</td>
                <td className="px-6 py-4">
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-semibold ${getScoreBadgeColor(
                      interview.score
                    )}`}
                  >
                    {interview.score}%
                  </span>
                </td>
                <td className="px-6 py-4 flex justify-end gap-2">
                  <Button variant="ghost" size="sm" className="hover:bg-muted">
                    <Eye className="w-4 h-4" />
                  </Button>
                  <Button variant="ghost" size="sm" className="hover:bg-muted">
                    <Download className="w-4 h-4" />
                  </Button>
                  <Button variant="ghost" size="sm" className="hover:bg-destructive/10 hover:text-destructive">
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
