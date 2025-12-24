'use client';

import { Sparkles, Zap, Shield } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="relative border-t border-border/50 bg-gradient-to-b from-background to-card/30 overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-24 right-0 w-96 h-96 bg-primary/5 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-24 left-0 w-96 h-96 bg-accent/5 rounded-full blur-3xl"></div>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Main content */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-8 mb-12">
          {/* Brand */}
          <div className="max-w-md">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-accent p-0.5">
                <div className="w-full h-full rounded-xl bg-background flex items-center justify-center">
                  <Sparkles className="w-5 h-5 text-primary" />
                </div>
              </div>
              <h3 className="font-bold text-xl bg-gradient-to-r from-primary via-accent to-secondary bg-clip-text text-transparent">
                InterviewAI
              </h3>
            </div>
            <p className="text-muted-foreground leading-relaxed">
              Transform your interview performance with AI-powered coaching and real-time feedback.
            </p>
          </div>

          {/* Features highlight */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                <Zap className="w-4 h-4 text-primary" />
              </div>
              <div>
                <p className="font-medium text-sm mb-1">AI-Powered</p>
                <p className="text-xs text-muted-foreground">Advanced technology</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-accent/10 flex items-center justify-center flex-shrink-0">
                <Shield className="w-4 h-4 text-accent" />
              </div>
              <div>
                <p className="font-medium text-sm mb-1">Secure</p>
                <p className="text-xs text-muted-foreground">Your data protected</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-secondary/10 flex items-center justify-center flex-shrink-0">
                <Sparkles className="w-4 h-4 text-secondary" />
              </div>
              <div>
                <p className="font-medium text-sm mb-1">Effective</p>
                <p className="text-xs text-muted-foreground">Proven results</p>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-8 border-t border-border/50">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <p className="text-sm text-muted-foreground">
              &copy; 2025 InterviewAI. All rights reserved.
            </p>
            <p className="text-xs text-muted-foreground">
              Built with precision and care
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
