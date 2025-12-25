'use client';

import { Card } from '@/components/ui/card';
import { Mic, BarChart3, Zap, TrendingUp, ChevronRight } from 'lucide-react';

const features = [
  {
    icon: Mic,
    title: 'Live Recording & Transcription',
    description: 'Record your responses with real-time transcription and automatic analysis.',
    gradient: 'from-primary/20 via-primary/10 to-transparent',
    iconGradient: 'from-primary to-accent',
  },
  {
    icon: Zap,
    title: 'Real-Time Feedback',
    description: 'Get instant feedback on your communication, pace, and technical accuracy.',
    gradient: 'from-accent/20 via-accent/10 to-transparent',
    iconGradient: 'from-accent to-secondary',
  },
  {
    icon: BarChart3,
    title: 'Detailed Analytics',
    description: 'Track your progress with comprehensive performance metrics and insights.',
    gradient: 'from-secondary/20 via-secondary/10 to-transparent',
    iconGradient: 'from-secondary to-primary',
  },
  {
    icon: TrendingUp,
    title: 'Interview History',
    description: 'Review past interviews and compare your improvement over time.',
    gradient: 'from-primary/15 via-accent/10 to-transparent',
    iconGradient: 'from-primary via-accent to-secondary',
  },
];

export default function FeaturesSection() {
  return (
    <section className="relative py-16 pb-24 bg-gradient-to-b from-background via-muted/5 to-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Section header */}
      <div className="text-center mb-12">
        <div className="inline-block mb-4">
          <span className="text-sm font-semibold tracking-wider uppercase bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            Powerful Features
          </span>
        </div>
        <h2 className="text-4xl sm:text-5xl font-bold mb-6">
          Everything You Need to{' '}
          <span className="bg-gradient-to-r from-primary via-accent to-secondary bg-clip-text text-transparent">
            Excel
          </span>
        </h2>
        <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
          Advanced AI technology meets intuitive design to deliver the ultimate interview preparation experience
        </p>
      </div>

      {/* Features grid with bento box style */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {features.map((feature, index) => {
          const Icon = feature.icon;

          return (
            <div
              key={index}
              className={`fade-in-animation group relative ${
                index === 0 ? 'lg:col-span-2' : ''
              }`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {/* Glow effect */}
              <div className={`absolute -inset-0.5 bg-gradient-to-r ${feature.iconGradient} rounded-3xl blur opacity-0 group-hover:opacity-20 transition duration-500`}></div>

              {/* Card */}
              <div className={`relative bg-card backdrop-blur-sm border-2 border-border/80 rounded-3xl p-8 hover:border-primary/50 transition-all duration-300 overflow-hidden shadow-lg hover:shadow-2xl hover:shadow-primary/20 ${
                index === 0 ? 'lg:flex lg:items-center lg:gap-12' : ''
              }`}>
                {/* Background decoration */}
                <div className={`absolute top-0 right-0 w-64 h-64 bg-gradient-to-br ${feature.gradient} rounded-full blur-3xl opacity-50 group-hover:opacity-70 transition-opacity`}></div>

                {/* Content */}
                <div className={`relative z-10 ${index === 0 ? 'lg:flex-1' : ''}`}>
                  {/* Icon with gradient background */}
                  <div className="mb-6">
                    <div className={`inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br ${feature.iconGradient} p-0.5 group-hover:scale-110 transition-transform duration-300`}>
                      <div className="w-full h-full rounded-2xl bg-background flex items-center justify-center">
                        <Icon className="w-7 h-7 text-primary group-hover:text-accent transition-colors" />
                      </div>
                    </div>
                  </div>

                  {/* Text content */}
                  <h3 className="text-2xl font-bold mb-3 text-foreground group-hover:bg-gradient-to-r group-hover:from-primary group-hover:to-accent group-hover:bg-clip-text group-hover:text-transparent transition-all">
                    {feature.title}
                  </h3>
                  <p className="text-foreground/80 text-lg leading-relaxed mb-4">
                    {feature.description}
                  </p>

                  {/* Hover indicator */}
                  <div className="inline-flex items-center gap-2 text-sm font-medium text-primary opacity-0 group-hover:opacity-100 transition-opacity">
                    <span>Learn more</span>
                    <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>

                {/* Visual element for first feature */}
                {index === 0 && (
                  <div className="relative mt-8 lg:mt-0 lg:flex-1">
                    <div className="aspect-video rounded-2xl bg-gradient-to-br from-primary/10 via-accent/10 to-secondary/10 border border-primary/20 flex items-center justify-center overflow-hidden">
                      <div className="relative">
                        <Icon className="w-32 h-32 text-primary/20" />
                        <div className="absolute inset-0 bg-gradient-to-t from-transparent to-primary/10 animate-pulse"></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Decorative elements */}
      <div className="absolute top-10 right-10 w-20 h-20 border border-primary/10 rounded-full animate-pulse"></div>
      <div className="absolute bottom-20 left-10 w-16 h-16 bg-accent/5 rotate-45" style={{ clipPath: 'polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)' }}></div>
      </div>
    </section>
  );
}
