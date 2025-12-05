'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ArrowRight, Sparkles, BrainCircuit, Target } from 'lucide-react';
import { useScrollFadeIn } from '@/hooks/use-scroll-fade-in';
import { useParallax } from '@/hooks/use-parallax';

export default function HeroSection() {
  const fadeInRef = useScrollFadeIn();
  const { ref: parallaxRef1, offset: offset1 } = useParallax(0.5);
  const { ref: parallaxRef2, offset: offset2 } = useParallax(-0.3);
  const { ref: parallaxRef3, offset: offset3 } = useParallax(0.2);

  return (
    <section className="relative min-h-[700px] flex items-center justify-center px-4 sm:px-6 lg:px-8 py-20 overflow-hidden">
      {/* Enhanced background effects */}
      <div className="absolute inset-0 overflow-hidden">
        <div
          ref={parallaxRef1}
          className="parallax-element absolute top-20 right-0 w-[600px] h-[600px] bg-primary/15 rounded-full blur-3xl opacity-40"
          style={{ transform: `translate(20%, ${offset1}px)` }}
        ></div>
        <div
          ref={parallaxRef2}
          className="parallax-element absolute bottom-0 left-0 w-[500px] h-[500px] bg-accent/15 rounded-full blur-3xl opacity-40"
          style={{ transform: `translate(-20%, ${offset2}px)` }}
        ></div>
        <div
          ref={parallaxRef3}
          className="parallax-element absolute top-1/2 left-1/2 w-[400px] h-[400px] bg-secondary/10 rounded-full blur-3xl opacity-30"
          style={{ transform: `translate(-50%, calc(-50% + ${offset3}px))` }}
        ></div>

        {/* Geometric shapes */}
        <div className="absolute top-1/4 left-10 w-20 h-20 border-2 border-primary/20 rounded-lg rotate-12 animate-pulse"></div>
        <div className="absolute bottom-1/4 right-20 w-16 h-16 border-2 border-accent/20 rounded-full animate-pulse" style={{ animationDelay: '1s' }}></div>
        <div className="absolute top-1/3 right-1/4 w-12 h-12 bg-primary/10 rotate-45" style={{ clipPath: 'polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)' }}></div>
      </div>

      <div ref={fadeInRef} className="relative z-10 max-w-6xl mx-auto fade-in-animation">
        {/* Badge with icon */}
        <div className="flex justify-center mb-8">
          <div className="inline-flex items-center gap-3 px-6 py-3 rounded-2xl bg-gradient-to-r from-primary/10 via-accent/10 to-secondary/10 border border-primary/20 backdrop-blur-sm scale-on-scroll">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
                <Sparkles className="w-4 h-4 text-primary" />
              </div>
              <span className="text-sm font-medium bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                Next-Gen AI Interview Coach
              </span>
            </div>
          </div>
        </div>

        {/* Hero title with unique layout */}
        <div className="text-center mb-8">
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
            <span className="block mb-2">Ace Every Interview</span>
            <span className="block bg-gradient-to-r from-primary via-accent to-secondary bg-clip-text text-transparent animate-gradient">
              With AI Precision
            </span>
          </h1>

          <p className="text-xl sm:text-2xl text-muted-foreground mb-12 max-w-3xl mx-auto leading-relaxed">
            Real-time coaching, intelligent feedback, and data-driven insights to transform your interview performance
          </p>
        </div>

        {/* CTA with visual elements */}
        <div className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-16">
          <Link href="/interview-setup">
            <Button
              size="lg"
              className="bg-gradient-to-r from-primary to-accent text-primary-foreground hover:opacity-90 transition-all hover:scale-105 hover:shadow-2xl hover:shadow-primary/50 px-8 py-6 text-lg rounded-xl group"
            >
              Start Practicing Now
              <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
            </Button>
          </Link>
        </div>

        {/* Stats with cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <div className="fade-in-animation relative group" style={{ animationDelay: '0.1s' }}>
            <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-primary/5 rounded-2xl blur-xl group-hover:blur-2xl transition-all"></div>
            <div className="relative bg-card/50 backdrop-blur-sm border border-border rounded-2xl p-8 hover:border-primary/50 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4">
                <BrainCircuit className="w-6 h-6 text-primary" />
              </div>
              <div className="text-4xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent mb-2">10K+</div>
              <p className="text-sm text-muted-foreground font-medium">Professionals Trained</p>
            </div>
          </div>

          <div className="fade-in-animation relative group" style={{ animationDelay: '0.2s' }}>
            <div className="absolute inset-0 bg-gradient-to-br from-accent/20 to-accent/5 rounded-2xl blur-xl group-hover:blur-2xl transition-all"></div>
            <div className="relative bg-card/50 backdrop-blur-sm border border-border rounded-2xl p-8 hover:border-accent/50 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center mb-4">
                <Target className="w-6 h-6 text-accent" />
              </div>
              <div className="text-4xl font-bold bg-gradient-to-r from-accent to-secondary bg-clip-text text-transparent mb-2">95%</div>
              <p className="text-sm text-muted-foreground font-medium">Interview Success Rate</p>
            </div>
          </div>

          <div className="fade-in-animation relative group" style={{ animationDelay: '0.3s' }}>
            <div className="absolute inset-0 bg-gradient-to-br from-secondary/20 to-secondary/5 rounded-2xl blur-xl group-hover:blur-2xl transition-all"></div>
            <div className="relative bg-card/50 backdrop-blur-sm border border-border rounded-2xl p-8 hover:border-secondary/50 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 rounded-xl bg-secondary/10 flex items-center justify-center mb-4">
                <Sparkles className="w-6 h-6 text-secondary" />
              </div>
              <div className="text-4xl font-bold bg-gradient-to-r from-secondary to-primary bg-clip-text text-transparent mb-2">50+</div>
              <p className="text-sm text-muted-foreground font-medium">Top Tech Companies</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
