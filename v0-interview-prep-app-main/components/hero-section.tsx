'use client';

import { Button } from '@/components/ui/button';
import { ArrowRight, Sparkles } from 'lucide-react';
import { useScrollFadeIn } from '@/hooks/use-scroll-fade-in';
import { useParallax } from '@/hooks/use-parallax';

export default function HeroSection({ onGetStarted }: { onGetStarted: () => void }) {
  const fadeInRef = useScrollFadeIn();
  const { ref: parallaxRef1, offset: offset1 } = useParallax(0.5);
  const { ref: parallaxRef2, offset: offset2 } = useParallax(-0.3);

  return (
    <section className="relative min-h-[600px] flex items-center justify-center px-4 sm:px-6 lg:px-8 py-20 overflow-hidden">
      <div className="absolute inset-0 overflow-hidden">
        <div 
          ref={parallaxRef1}
          className="parallax-element absolute top-0 right-0 w-96 h-96 bg-primary/20 rounded-full blur-3xl opacity-30"
          style={{ transform: `translateY(${offset1}px)` }}
        ></div>
        <div 
          ref={parallaxRef2}
          className="parallax-element absolute bottom-0 left-0 w-96 h-96 bg-accent/20 rounded-full blur-3xl opacity-30"
          style={{ transform: `translateY(${offset2}px)` }}
        ></div>
      </div>

      <div ref={fadeInRef} className="relative z-10 max-w-4xl mx-auto text-center fade-in-animation">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-card border border-border mb-8 scale-on-scroll">
          <Sparkles className="w-4 h-4 text-primary" />
          <span className="text-sm text-muted-foreground">AI-Powered Interview Preparation</span>
        </div>

        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6 text-balance">
          Master Your <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">Interviews</span> with AI
        </h1>

        <p className="text-lg sm:text-xl text-muted-foreground mb-12 max-w-2xl mx-auto text-balance">
          Get real-time feedback, track your progress, and land your dream job with personalized interview coaching powered by AI.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button onClick={onGetStarted} size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90 transition-all hover:scale-105">
            Get Started <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </div>

        <div className="grid grid-cols-3 gap-4 mt-16 pt-16 border-t border-border">
          <div className="fade-in-animation" style={{ animationDelay: '0.1s' }}>
            <div className="text-3xl font-bold text-primary">10K+</div>
            <p className="text-sm text-muted-foreground">Users Prepared</p>
          </div>
          <div className="fade-in-animation" style={{ animationDelay: '0.2s' }}>
            <div className="text-3xl font-bold text-primary">95%</div>
            <p className="text-sm text-muted-foreground">Success Rate</p>
          </div>
          <div className="fade-in-animation" style={{ animationDelay: '0.3s' }}>
            <div className="text-3xl font-bold text-primary">50+</div>
            <p className="text-sm text-muted-foreground">Companies</p>
          </div>
        </div>
      </div>
    </section>
  );
}
