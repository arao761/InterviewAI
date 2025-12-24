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
  const [evaluation, setEvaluation] = useState<InterviewEvaluationReport | null>(null);
  const [sessionData, setSessionData] = useState<any>(null);
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
      setSessionData(results.sessionData);
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

  const handleShare = async () => {
    try {
      if (navigator.share) {
        await navigator.share({
          title: 'Interview Results',
          text: `I scored ${overallScore}% on my interview!`,
          url: window.location.href
        });
      } else {
        // Fallback: copy link
        await navigator.clipboard.writeText(window.location.href);
        alert('Link copied to clipboard!');
      }
    } catch (error) {
      console.error('Error sharing:', error);
    }
  };

  const handleDownload = () => {
    if (!evaluation) return;

    // Generate text report
    const report = `
INTERVIEW RESULTS REPORT
========================

Date: ${new Date().toLocaleDateString()}
Overall Score: ${Math.round(evaluation.overall_score)}%
${evaluation.technical_score ? `Technical Score: ${Math.round(evaluation.technical_score)}%` : ''}
${evaluation.behavioral_score ? `Behavioral Score: ${Math.round(evaluation.behavioral_score)}%` : ''}

OVERALL FEEDBACK
----------------
${evaluation.detailed_feedback}

STRENGTHS
---------
${evaluation.strengths?.map((s, i) => `${i + 1}. ${s}`).join('\n') || 'N/A'}

AREAS FOR IMPROVEMENT
---------------------
${evaluation.areas_for_improvement?.map((a, i) => `${i + 1}. ${a}`).join('\n') || 'N/A'}

RECOMMENDATIONS
---------------
${evaluation.recommendations?.map((r, i) => `${i + 1}. ${r}`).join('\n') || 'N/A'}

INDIVIDUAL QUESTION RESULTS
----------------------------
${evaluation.individual_evaluations?.map((evalItem, i) => `
Question ${i + 1}
Score: ${Math.round(evalItem.score)}%
Feedback: ${evalItem.feedback}
Strengths: ${evalItem.strengths?.join(', ') || 'N/A'}
Areas to Improve: ${evalItem.weaknesses?.join(', ') || 'N/A'}
`).join('\n') || 'N/A'}
    `.trim();

    // Download as text file
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `interview-results-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (!evaluation) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground">Loading results...</p>
        </div>
      </div>
    );
  }

  const overallScore = Math.round(evaluation.overall_score || 0);
  const metrics = calculateMetrics();
  const questions = sessionData?.questions || [];
  const individualEvals = evaluation.individual_evaluations || [];

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
            <Button variant="outline" className="border-border hover:bg-card" onClick={handleShare}>
              <Share2 className="w-4 h-4 mr-2" />
              Share
            </Button>
            <Button className="bg-primary text-primary-foreground hover:bg-primary/90" onClick={handleDownload}>
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

        {/* Individual Question Results */}
        {individualEvals.length > 0 && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold mb-6">Individual Question Results</h2>
            <div ref={questionsRef} className="space-y-6 fade-in-animation">
              {individualEvals.map((evalItem, index) => {
                const question = questions[index];
                return (
                  <Card key={index} className="bg-card border-border p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex-1">
                        <h3 className="font-semibold text-lg mb-2">
                          Q{index + 1}: {question?.question || question?.text || `Question ${index + 1}`}
                        </h3>
                      </div>
                      <div className="text-right">
                        <div className="text-3xl font-bold text-primary">{Math.round(evalItem.score)}</div>
                        <div className="text-xs text-muted-foreground">out of 100</div>
                      </div>
                    </div>

                    {evalItem.feedback && (
                      <div className="bg-muted/50 rounded-lg p-4 mb-4">
                        <p className="text-sm text-foreground">{evalItem.feedback}</p>
                      </div>
                    )}

                    <div className="grid md:grid-cols-2 gap-4">
                      {evalItem.strengths && evalItem.strengths.length > 0 && (
                        <div>
                          <h4 className="font-semibold text-sm mb-3 text-green-500">Strengths</h4>
                          <ul className="space-y-2">
                            {evalItem.strengths.map((strength, i) => (
                              <li key={i} className="flex items-start gap-2 text-sm">
                                <span className="text-green-500 mt-1">✓</span>
                                <span>{strength}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                      {evalItem.weaknesses && evalItem.weaknesses.length > 0 && (
                        <div>
                          <h4 className="font-semibold text-sm mb-3 text-yellow-500">Areas to Improve</h4>
                          <ul className="space-y-2">
                            {evalItem.weaknesses.map((weakness, i) => (
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
          </div>
        )}

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
