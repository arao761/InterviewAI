'use client';

import { useState } from 'react';
import ResultsHeader from '@/components/results/results-header';
import OverallScore from '@/components/results/overall-score';
import PerformanceMetrics from '@/components/results/performance-metrics';
import DetailedFeedback from '@/components/results/detailed-feedback';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { DownloadCloud, Share2, ArrowLeft } from 'lucide-react';
import { useScrollFadeIn } from '@/hooks/use-scroll-fade-in';

export default function ResultsPage() {
  const [activeTab, setActiveTab] = useState('overview');
  const overallScoreRef = useScrollFadeIn();
  const metricsRef = useScrollFadeIn();
  const questionsRef = useScrollFadeIn();

  // Mock results data
  const results = {
    overallScore: 78,
    interviewType: 'Behavioral Interview',
    duration: '28m 42s',
    questionsAnswered: 5,
    completedAt: new Date().toLocaleDateString(),
    metrics: {
      clarity: 85,
      confidence: 72,
      structure: 80,
      technicalAccuracy: 75,
      engagement: 88,
    },
    questions: [
      {
        id: 1,
        question: 'Tell me about a challenging project you worked on',
        score: 82,
        duration: '4m 20s',
        feedback:
          'Great job structuring your answer with the STAR method. You could have added more specific metrics.',
        strengths: ['Clear structure', 'Good examples', 'Professional tone'],
        improvements: ['Add more quantifiable results', 'Reduce filler words'],
      },
      {
        id: 2,
        question: 'How do you approach problem-solving?',
        score: 75,
        duration: '3m 15s',
        feedback:
          'Solid approach, but consider walking through a concrete example to illustrate your methodology.',
        strengths: ['Logical thinking', 'Comprehensive'],
        improvements: ['Use specific example', 'More concise'],
      },
    ],
  };

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'detailed', label: 'Detailed Feedback' },
    { id: 'transcript', label: 'Transcript' },
  ];

  return (
    <div className="min-h-screen bg-background text-foreground">
      <ResultsHeader />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Top Section */}
        <div className="flex justify-between items-start mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2">Interview Results</h1>
            <p className="text-muted-foreground">{results.interviewType} • {results.completedAt}</p>
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
          <OverallScore score={results.overallScore} />
        </div>

        {/* Performance Metrics */}
        <div ref={metricsRef} className="mb-8 fade-in-animation">
          <PerformanceMetrics metrics={results.metrics} />
        </div>

        {/* Tabs */}
        <div className="mb-8">
          {/* Tab Navigation */}
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

          {/* Tab Content */}
          {activeTab === 'overview' && (
            <div ref={questionsRef} className="space-y-6 fade-in-animation">
              {results.questions.map((q) => (
                <Card key={q.id} className="bg-card border-border p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg mb-2">{q.question}</h3>
                      <p className="text-sm text-muted-foreground">Duration: {q.duration}</p>
                    </div>
                    <div className="text-right">
                      <div className="text-3xl font-bold text-primary">{q.score}</div>
                      <div className="text-xs text-muted-foreground">out of 100</div>
                    </div>
                  </div>

                  <div className="bg-muted/50 rounded-lg p-4 mb-4">
                    <p className="text-sm text-foreground">{q.feedback}</p>
                  </div>

                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <h4 className="font-semibold text-sm mb-3 text-green-500">Strengths</h4>
                      <ul className="space-y-2">
                        {q.strengths.map((strength, i) => (
                          <li key={i} className="flex items-start gap-2 text-sm">
                            <span className="text-green-500 mt-1">✓</span>
                            <span>{strength}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h4 className="font-semibold text-sm mb-3 text-yellow-500">Areas to Improve</h4>
                      <ul className="space-y-2">
                        {q.improvements.map((improvement, i) => (
                          <li key={i} className="flex items-start gap-2 text-sm">
                            <span className="text-yellow-500 mt-1">→</span>
                            <span>{improvement}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          )}

          {activeTab === 'detailed' && (
            <DetailedFeedback questions={results.questions} />
          )}

          {activeTab === 'transcript' && (
            <div className="bg-card border border-border rounded-lg p-6">
              <div className="space-y-6">
                {results.questions.map((q) => (
                  <div key={q.id} className="border-b border-border pb-6 last:border-b-0">
                    <h3 className="font-semibold mb-3">Q{q.id}: {q.question}</h3>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut
                      labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
                      nisi ut aliquip ex ea commodo consequat.
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Bottom Actions */}
        <div className="flex justify-between items-center pt-8 border-t border-border">
          <Button variant="outline" className="border-border hover:bg-card">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Dashboard
          </Button>

          <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
            Practice Another Interview
          </Button>
        </div>
      </div>
    </div>
  );
}
