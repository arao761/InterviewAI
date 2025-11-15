'use client';

import { Card } from '@/components/ui/card';
import { Mic, BarChart3, Zap, TrendingUp } from 'lucide-react';
import { useScrollFadeIn } from '@/hooks/use-scroll-fade-in';

const features = [
  {
    icon: Mic,
    title: 'Live Recording & Transcription',
    description: 'Record your responses with real-time transcription and automatic analysis.',
  },
  {
    icon: Zap,
    title: 'Real-Time Feedback',
    description: 'Get instant feedback on your communication, pace, and technical accuracy.',
  },
  {
    icon: BarChart3,
    title: 'Detailed Analytics',
    description: 'Track your progress with comprehensive performance metrics and insights.',
  },
  {
    icon: TrendingUp,
    title: 'Interview History',
    description: 'Review past interviews and compare your improvement over time.',
  },
];

export default function FeaturesSection() {
  const fadeInRef = useScrollFadeIn();

  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div className="text-center mb-16">
        <h2 className="text-3xl sm:text-4xl font-bold mb-4">Powerful Features</h2>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Everything you need to prepare and succeed in your interviews.
        </p>
      </div>

      <div className="space-y-12">
        {features.map((feature, index) => {
          const Icon = feature.icon;
          const isEven = index % 2 === 0;
          
          return (
            <div 
              key={index} 
              className={`flex items-center gap-8 ${isEven ? 'flex-row' : 'flex-row-reverse'}`}
            >
              {/* Feature content */}
              <div className={`flex-1 ${isEven ? 'slide-in-left' : 'slide-in-right'}`} style={{ animationDelay: `${index * 0.1}s` }}>
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <Icon className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                    <p className="text-muted-foreground">{feature.description}</p>
                  </div>
                </div>
              </div>
              
              {/* Visual accent box */}
              <div className={`flex-1 scale-on-scroll`} style={{ animationDelay: `${index * 0.1 + 0.1}s` }}>
                <div className="h-64 rounded-lg bg-gradient-to-br from-primary/10 to-accent/10 border border-primary/20 flex items-center justify-center overflow-hidden relative group">
                  <div className="absolute inset-0 bg-gradient-shift opacity-0 group-hover:opacity-20 transition-opacity duration-500"></div>
                  <Icon className="w-20 h-20 text-primary/30 group-hover:text-primary/50 transition-colors" />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
