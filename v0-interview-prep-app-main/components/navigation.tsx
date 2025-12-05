'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ThemeToggle } from '@/components/theme-toggle';
import { Sparkles } from 'lucide-react';

export default function Navigation() {
  return (
    <nav className="border-b border-border/50 bg-background/80 backdrop-blur-xl sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-20">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-accent p-0.5 group-hover:scale-110 transition-transform">
            <div className="w-full h-full rounded-xl bg-background flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-primary" />
            </div>
          </div>
          <span className="text-xl font-bold bg-gradient-to-r from-primary via-accent to-secondary bg-clip-text text-transparent">
            InterviewAI
          </span>
        </Link>

        {/* Navigation items */}
        <div className="flex gap-2 items-center">
          <Link href="/about">
            <Button variant="ghost" size="sm" className="hover:bg-primary/10 hover:text-primary transition-colors">
              About
            </Button>
          </Link>
          <Link href="/pricing">
            <Button variant="ghost" size="sm" className="hover:bg-accent/10 hover:text-accent transition-colors">
              Pricing
            </Button>
          </Link>
          <div className="mx-2">
            <ThemeToggle />
          </div>
          <Link href="/interview-setup">
            <Button size="sm" className="bg-gradient-to-r from-primary to-accent text-primary-foreground hover:opacity-90 hover:shadow-lg hover:shadow-primary/30 transition-all hover:scale-105 rounded-lg">
              Get Started
            </Button>
          </Link>
        </div>
      </div>
    </nav>
  );
}
