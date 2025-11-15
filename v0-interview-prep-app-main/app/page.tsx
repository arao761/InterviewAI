'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import Navigation from '@/components/navigation';
import HeroSection from '@/components/hero-section';
import FeaturesSection from '@/components/features-section';
import ResumeUploadSection from '@/components/resume-upload-section';
import Footer from '@/components/footer';

export default function Home() {
  const [showUpload, setShowUpload] = useState(false);

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation />
      <main>
        {!showUpload ? (
          <>
            <HeroSection onGetStarted={() => setShowUpload(true)} />
            <FeaturesSection />
          </>
        ) : (
          <ResumeUploadSection onBack={() => setShowUpload(false)} />
        )}
      </main>
      <Footer />
    </div>
  );
}
