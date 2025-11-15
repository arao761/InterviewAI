'use client';

import { useState } from 'react';
import DashboardHeader from '@/components/dashboard/dashboard-header';
import QuickStats from '@/components/dashboard/quick-stats';
import ProgressChart from '@/components/dashboard/progress-chart';
import InterviewHistory from '@/components/dashboard/interview-history';
import SkillAnalysis from '@/components/dashboard/skill-analysis';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';

export default function Dashboard() {
  const [filter, setFilter] = useState('all');

  // Mock data
  const interviews = [
    {
      id: 1,
      type: 'Behavioral',
      company: 'Google',
      date: '2025-11-10',
      score: 82,
      duration: '28m',
      status: 'completed',
    },
    {
      id: 2,
      type: 'Technical',
      company: 'Meta',
      date: '2025-11-08',
      score: 75,
      duration: '32m',
      status: 'completed',
    },
    {
      id: 3,
      type: 'Case Study',
      company: 'McKinsey',
      date: '2025-11-05',
      score: 88,
      duration: '35m',
      status: 'completed',
    },
    {
      id: 4,
      type: 'Behavioral',
      company: 'Amazon',
      date: '2025-11-02',
      score: 79,
      duration: '25m',
      status: 'completed',
    },
  ];

  const stats = {
    totalInterviews: 12,
    averageScore: 81,
    bestScore: 92,
    hoursSpent: 8.5,
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <DashboardHeader />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header with Action */}
        <div className="flex justify-between items-center mb-12">
          <div>
            <h1 className="text-4xl font-bold mb-2">Dashboard</h1>
            <p className="text-muted-foreground">Track your interview preparation progress</p>
          </div>

          <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
            <Plus className="w-4 h-4 mr-2" />
            New Interview
          </Button>
        </div>

        {/* Quick Stats */}
        <div className="mb-12">
          <QuickStats stats={stats} />
        </div>

        {/* Charts Section */}
        <div className="grid lg:grid-cols-3 gap-8 mb-12">
          <div className="lg:col-span-2">
            <ProgressChart />
          </div>
          <div>
            <SkillAnalysis />
          </div>
        </div>

        {/* Interview History */}
        <div>
          <InterviewHistory interviews={interviews} />
        </div>
      </div>
    </div>
  );
}
