'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import DashboardHeader from '@/components/dashboard/dashboard-header';
import QuickStats from '@/components/dashboard/quick-stats';
import ProgressChart from '@/components/dashboard/progress-chart';
import InterviewHistory from '@/components/dashboard/interview-history';
import SkillAnalysis from '@/components/dashboard/skill-analysis';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';
import apiClient from '@/lib/api/client';

export default function Dashboard() {
  const [filter, setFilter] = useState('all');
  const [stats, setStats] = useState({
    totalInterviews: 0,
    averageScore: 0,
    bestScore: null as number | null,
    hoursSpent: 0,
  });
  const [interviews, setInterviews] = useState<Array<{
    id: number;
    type: string;
    company: string;
    date: string;
    score: number;
    duration: string;
    status: string;
  }>>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchDashboardData() {
      try {
        setLoading(true);
        setError(null);

        // Fetch dashboard statistics and interview history in parallel
        const [statsData, historyData] = await Promise.all([
          apiClient.getDashboardStats(),
          apiClient.getInterviewHistory(),
        ]);

        // Update stats
        setStats({
          totalInterviews: statsData.total_interviews,
          averageScore: Math.round(statsData.average_score),
          bestScore: statsData.best_score ? Math.round(statsData.best_score) : null,
          hoursSpent: statsData.hours_spent,
        });

        // Transform interview history to match component format
        const transformedInterviews = historyData.interviews.map((interview) => ({
          id: interview.id,
          type: interview.interview_type 
            ? interview.interview_type.charAt(0).toUpperCase() + interview.interview_type.slice(1)
            : 'Interview',
          company: interview.technical_domain || 'General',
          date: interview.date,
          score: interview.score ? Math.round(interview.score) : 0,
          duration: interview.duration_minutes 
            ? `${Math.round(interview.duration_minutes)}m`
            : 'N/A',
          status: interview.status,
        }));

        setInterviews(transformedInterviews);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError(err instanceof Error ? err.message : 'Failed to load dashboard data');
        // Set empty data on error
        setStats({
          totalInterviews: 0,
          averageScore: 0,
          bestScore: null,
          hoursSpent: 0,
        });
        setInterviews([]);
      } finally {
        setLoading(false);
      }
    }

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-background text-foreground">
        <DashboardHeader />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="flex items-center justify-center h-64">
            <p className="text-muted-foreground">Loading dashboard...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background text-foreground">
        <DashboardHeader />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="flex items-center justify-center h-64">
            <p className="text-destructive">Error: {error}</p>
          </div>
        </div>
      </div>
    );
  }

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

          <Link href="/interview-setup">
            <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
              <Plus className="w-4 h-4 mr-2" />
              New Interview
            </Button>
          </Link>
        </div>

        {/* Quick Stats */}
        <div className="mb-12">
          <QuickStats stats={stats} />
        </div>

        {/* Charts Section */}
        <div className="grid lg:grid-cols-3 gap-8 mb-12">
          <div className="lg:col-span-2">
            <ProgressChart interviews={interviews} />
          </div>
          <div>
            <SkillAnalysis interviews={interviews} />
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
