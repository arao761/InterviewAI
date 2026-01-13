'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import DashboardHeader from '@/components/dashboard/dashboard-header';
import QuickStats from '@/components/dashboard/quick-stats';
import ProgressChart from '@/components/dashboard/progress-chart';
import InterviewHistory from '@/components/dashboard/interview-history';
import SkillAnalysis from '@/components/dashboard/skill-analysis';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';
import apiClient from '@/lib/api/client';
import { useAuth } from '@/context/AuthContext';

export default function Dashboard() {
  const router = useRouter();
  const { isAuthenticated, loading: authLoading } = useAuth();
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
  const [authError, setAuthError] = useState(false);

  useEffect(() => {
    // Wait for auth to finish loading
    if (authLoading) {
      return;
    }

    // If not authenticated, don't try to fetch data
    if (!isAuthenticated) {
      setAuthError(true);
      setLoading(false);
      setError('Please log in to view your dashboard');
      return;
    }

    async function fetchDashboardData() {
      try {
        setLoading(true);
        setError(null);
        setAuthError(false);

        // Fetch dashboard statistics and interview history separately to handle partial failures
        let statsData = null;
        let historyData = null;
        const errors: string[] = [];

        try {
          statsData = await apiClient.getDashboardStats();
        } catch (err: any) {
          console.error('Error fetching stats:', err);
          const errorMessage = err?.message || 'Failed to load statistics';
          
          // Check if it's an authentication error
          if (errorMessage.includes('Invalid or expired token') || 
              errorMessage.includes('Not authenticated') ||
              errorMessage.includes('401')) {
            setAuthError(true);
            apiClient.logout();
            errors.push('Please log in to view your dashboard');
          } else {
            errors.push('Failed to load statistics');
          }
          
          // Use default empty stats
          statsData = {
            total_interviews: 0,
            average_score: 0,
            best_score: null,
            hours_spent: 0,
          };
        }

        try {
          historyData = await apiClient.getInterviewHistory();
        } catch (err: any) {
          console.error('Error fetching history:', err);
          const errorMessage = err?.message || 'Failed to load interview history';
          
          // Check if it's an authentication error
          if (errorMessage.includes('Invalid or expired token') || 
              errorMessage.includes('Not authenticated') ||
              errorMessage.includes('401')) {
            if (!authError) {
              setAuthError(true);
              apiClient.logout();
            }
            if (!errors.some(e => e.includes('log in'))) {
              errors.push('Please log in to view your dashboard');
            }
          } else {
            errors.push('Failed to load interview history');
          }
          
          // Use default empty history
          historyData = { interviews: [] };
        }

        // Update stats
        if (statsData) {
          setStats({
            totalInterviews: statsData.total_interviews,
            averageScore: Math.round(statsData.average_score),
            bestScore: statsData.best_score ? Math.round(statsData.best_score) : null,
            hoursSpent: statsData.hours_spent,
          });
        }

        // Transform interview history to match component format
        if (historyData) {
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
        }

        // Set error only if both failed
        if (errors.length === 2) {
          setError(errors.join('. '));
        } else if (errors.length === 1) {
          setError(errors[0] + '. Some data may be unavailable.');
        }
      } catch (err) {
        console.error('Unexpected error:', err);
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
  }, [isAuthenticated, authLoading]);

  // Show loading while checking authentication
  if (authLoading || (loading && isAuthenticated)) {
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

  // If not authenticated, show login prompt
  if (!isAuthenticated || authError) {
    return (
      <div className="min-h-screen bg-background text-foreground">
        <DashboardHeader />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Header with Action */}
          <div className="flex justify-between items-center mb-12">
            <div>
              <h1 className="text-4xl font-bold mb-2 gradient-text">Dashboard</h1>
              <p className="text-muted-foreground">Track your interview preparation progress</p>
            </div>

            <Link href="/interview-setup">
            <Button className="bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 text-primary-foreground font-semibold shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
                <Plus className="w-4 h-4 mr-2" />
                New Interview
              </Button>
            </Link>
          </div>

          {/* Authentication Required Message */}
          <div className="mb-8 p-6 bg-primary/10 border border-primary/20 rounded-lg">
            <p className="text-primary font-semibold mb-2 text-lg">Authentication Required</p>
            <p className="text-sm text-muted-foreground mb-4">
              Please log in to view your dashboard statistics and interview history.
            </p>
            <div className="flex gap-3">
              <Link href="/login">
                <Button className="bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 text-primary-foreground font-semibold shadow-lg hover:shadow-xl transition-all duration-300">
                  Log In
                </Button>
              </Link>
              <Link href="/register">
                <Button variant="outline" className="border-2 border-primary/30 hover:border-primary/50 hover:bg-primary/10 transition-all">
                  Sign Up
                </Button>
              </Link>
            </div>
          </div>

          {/* Quick Stats - Show zeros */}
          <div className="mb-12">
            <QuickStats stats={stats} />
          </div>

          {/* Interview History - Show empty state */}
          <div>
            <InterviewHistory interviews={[]} />
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
          {/* Header with Action */}
          <div className="flex justify-between items-center mb-12">
            <div>
              <h1 className="text-4xl font-bold mb-2 gradient-text">Dashboard</h1>
              <p className="text-muted-foreground">Track your interview preparation progress</p>
            </div>

            <Link href="/interview-setup">
            <Button className="bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 text-primary-foreground font-semibold shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
                <Plus className="w-4 h-4 mr-2" />
                New Interview
              </Button>
            </Link>
          </div>

          {/* Error Message */}
          <div className="mb-8 p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
            <p className="text-destructive font-semibold mb-2">
              {authError ? 'Authentication Required' : 'Unable to load dashboard data'}
            </p>
            <p className="text-sm text-muted-foreground">{error}</p>
            {authError ? (
              <div className="mt-4 flex gap-3">
                <Link href="/login">
                  <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
                    Log In
                  </Button>
                </Link>
                <Link href="/register">
                  <Button variant="outline" className="border-border hover:bg-card">
                    Sign Up
                  </Button>
                </Link>
              </div>
            ) : (
              <p className="text-sm text-muted-foreground mt-2">You can still start a new interview using the button above.</p>
            )}
          </div>

          {/* Quick Stats - Show zeros even on error */}
          <div className="mb-12">
            <QuickStats stats={stats} />
          </div>

          {/* Interview History - Show empty state */}
          <div>
            <InterviewHistory interviews={[]} />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 text-foreground">
      <DashboardHeader />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header with Action */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-6 mb-12 animate-in" style={{ animationDelay: '0.1s' }}>
          <div>
            <h1 className="text-4xl font-bold mb-2 gradient-text">Dashboard</h1>
            <p className="text-muted-foreground">Track your interview preparation progress</p>
          </div>

          <Link href="/interview-setup">
            <Button className="bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 text-primary-foreground font-semibold shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
              <Plus className="w-4 h-4 mr-2" />
              New Interview
            </Button>
          </Link>
        </div>

        {/* Quick Stats */}
        <div className="mb-12 animate-in" style={{ animationDelay: '0.2s' }}>
          <QuickStats stats={stats} />
        </div>

        {/* Charts Section */}
        <div className="grid lg:grid-cols-3 gap-8 mb-12 stagger-children">
          <div className="lg:col-span-2 animate-in" style={{ animationDelay: '0.3s' }}>
            <ProgressChart interviews={interviews} />
          </div>
          <div className="animate-in" style={{ animationDelay: '0.4s' }}>
            <SkillAnalysis interviews={interviews} />
          </div>
        </div>

        {/* Interview History */}
        <div className="animate-in" style={{ animationDelay: '0.5s' }}>
          <InterviewHistory interviews={interviews} />
        </div>
      </div>
    </div>
  );
}
