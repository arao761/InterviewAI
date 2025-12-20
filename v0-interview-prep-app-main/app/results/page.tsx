'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import ResultsHeader from '@/components/results/results-header';
import OverallScore from '@/components/results/overall-score';
import PerformanceMetrics from '@/components/results/performance-metrics';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { DownloadCloud, Share2, ArrowLeft } from 'lucide-react';
import { useScrollFadeIn } from '@/hooks/use-scroll-fade-in';
import { calculatePerformanceMetrics, calculateSimpleMetrics } from '@/lib/utils/metrics-calculator';
import type { InterviewEvaluationReport, ResponseEvaluation } from '@/lib/api/types';

export default function ResultsPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState('overview');
  const [evaluation, setEvaluation] = useState<InterviewEvaluationReport | null>(null);
  const [responses, setResponses] = useState<Array<any>>([]);
  const overallScoreRef = useScrollFadeIn();
  const metricsRef = useScrollFadeIn();
  const questionsRef = useScrollFadeIn();

  useEffect(() => {
    // Load results from sessionStorage
    const savedEvaluation = sessionStorage.getItem('interviewEvaluation');
    const savedResults = sessionStorage.getItem('interviewResults');

    if (savedEvaluation) {
      setEvaluation(JSON.parse(savedEvaluation));
    }

    if (savedResults) {
      const results = JSON.parse(savedResults);
      setResponses(results.responses || []);
    }

    // If no evaluation but have results, redirect to processing
    if (!savedEvaluation && savedResults) {
      console.log('No evaluation found, redirecting to processing...');
      router.push('/interview/processing');
      return;
    }

    // If no results at all, redirect to setup
    if (!savedEvaluation && !savedResults) {
      router.push('/interview-setup');
    }
  }, [router]);

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'detailed', label: 'Detailed Feedback' },
    { id: 'transcript', label: 'Transcript' },
  ];

  const calculateMetrics = () => {
    if (!evaluation) return {};

    try {
      // Use advanced keyword-based metrics calculation
      return calculatePerformanceMetrics(evaluation);
    } catch (error) {
      console.warn('Failed to calculate advanced metrics, using fallback:', error);
      // Fallback to simple calculation
      return calculateSimpleMetrics(evaluation);
    }
  };

  if (!evaluation && responses.length === 0) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground">Loading results...</p>
        </div>
      </div>
    );
  }

  const overallScore = Math.round(evaluation?.overall_score || 0);
  const metrics = calculateMetrics();

  return (
    <div className="min-h-screen bg-background text-foreground">
      <ResultsHeader />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Top Section */}
        <div className="flex justify-between items-start mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2">Interview Results</h1>
            <p className="text-muted-foreground">
              AI-Powered Interview • {new Date().toLocaleDateString()}
            </p>
          </div>

          <div className="flex gap-3">
            <Button variant="outline" className="border-border hover:bg-card">
              <Share2 className="w-4 h-4 mr-2" />
              Share
            </Button>
            <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
              <DownloadCloud className="w-4 h-4 mr-2" />
              Download Report
            </Button>
          </div>
        </div>

        {/* Overall Score Card */}
        <div ref={overallScoreRef} className="mb-8 fade-in-animation">
          <OverallScore score={overallScore} />
        </div>

        {/* Performance Metrics */}
        {Object.keys(metrics).length > 0 && (
          <div ref={metricsRef} className="mb-8 fade-in-animation">
            <PerformanceMetrics metrics={metrics} />
          </div>
        )}

        {/* Overall Feedback */}
        {evaluation && (
          <div className="mb-8">
            <Card className="bg-card border-border p-6">
              <h2 className="text-2xl font-bold mb-4">Overall Feedback</h2>
              <p className="text-muted-foreground mb-6">{evaluation.detailed_feedback}</p>

              <div className="grid md:grid-cols-2 gap-6">
                {/* Strengths */}
                {evaluation.strengths && evaluation.strengths.length > 0 && (
                  <div>
                    <h3 className="font-semibold text-lg mb-3 text-green-500">Your Strengths</h3>
                    <ul className="space-y-2">
                      {evaluation.strengths.map((strength, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <span className="text-green-500 mt-1">✓</span>
                          <span className="text-sm">{strength}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Areas for Improvement */}
                {evaluation.areas_for_improvement && evaluation.areas_for_improvement.length > 0 && (
                  <div>
                    <h3 className="font-semibold text-lg mb-3 text-yellow-500">Areas to Improve</h3>
                    <ul className="space-y-2">
                      {evaluation.areas_for_improvement.map((area, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <span className="text-yellow-500 mt-1">→</span>
                          <span className="text-sm">{area}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* Recommendations */}
              {evaluation.recommendations && evaluation.recommendations.length > 0 && (
                <div className="mt-6 pt-6 border-t border-border">
                  <h3 className="font-semibold text-lg mb-3">Recommendations</h3>
                  <ul className="space-y-2">
                    {evaluation.recommendations.map((rec, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-primary mt-1">•</span>
                        <span className="text-sm">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </Card>
          </div>
        )}

        {/* Tabs */}
        <div className="mb-8">
          <div className="flex border-b border-border mb-6 gap-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 font-medium text-sm transition-colors border-b-2 -mb-px ${
                  activeTab === tab.id
                    ? 'border-primary text-foreground'
                    : 'border-transparent text-muted-foreground hover:text-foreground'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Overview Tab - Individual Question Results */}
          {activeTab === 'overview' && (
            <div ref={questionsRef} className="space-y-6 fade-in-animation">
              {responses.map((response, index) => {
                const evaluation = response.evaluation;
                return (
                  <Card key={index} className="bg-card border-border p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex-1">
                        <h3 className="font-semibold text-lg mb-2">
                          Q{index + 1}: {response.question?.question || response.question?.text || 'Question'}
                        </h3>
                      </div>
                      {evaluation && (
                        <div className="text-right">
                          <div className="text-3xl font-bold text-primary">{Math.round(evaluation.score)}</div>
                          <div className="text-xs text-muted-foreground">out of 100</div>
                        </div>
                      )}
                    </div>

                    {evaluation?.feedback && (
                      <div className="bg-muted/50 rounded-lg p-4 mb-4">
                        <p className="text-sm text-foreground">{evaluation.feedback}</p>
                      </div>
                    )}

                    <div className="grid md:grid-cols-2 gap-4">
                      {evaluation?.strengths && evaluation.strengths.length > 0 && (
                        <div>
                          <h4 className="font-semibold text-sm mb-3 text-green-500">Strengths</h4>
                          <ul className="space-y-2">
                            {evaluation.strengths.map((strength, i) => (
                              <li key={i} className="flex items-start gap-2 text-sm">
                                <span className="text-green-500 mt-1">✓</span>
                                <span>{strength}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                      {evaluation?.weaknesses && evaluation.weaknesses.length > 0 && (
                        <div>
                          <h4 className="font-semibold text-sm mb-3 text-yellow-500">Areas to Improve</h4>
                          <ul className="space-y-2">
                            {evaluation.weaknesses.map((weakness, i) => (
                              <li key={i} className="flex items-start gap-2 text-sm">
                                <span className="text-yellow-500 mt-1">→</span>
                                <span>{weakness}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </Card>
                );
              })}
            </div>
          )}

          {/* Transcript Tab */}
          {activeTab === 'transcript' && (
            <div className="bg-card border border-border rounded-lg p-6">
              <div className="space-y-6">
                {responses.map((response, index) => (
                  <div key={index} className="border-b border-border pb-6 last:border-b-0">
                    <h3 className="font-semibold mb-3">
                      Q{index + 1}: {response.question?.question || response.question?.text}
                    </h3>
                    <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap">
                      {response.answer}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Bottom Actions */}
        <div className="flex justify-between items-center pt-8 border-t border-border">
          <Link href="/dashboard">
            <Button variant="outline" className="border-border hover:bg-card">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Dashboard
            </Button>
          </Link>

          <Link href="/interview-setup">
            <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
              Practice Another Interview
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
