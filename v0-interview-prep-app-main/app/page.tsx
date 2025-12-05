'use client';

import Navigation from '@/components/navigation';
import HeroSection from '@/components/hero-section';
import SocialProofSection from '@/components/social-proof-section';
import FeaturesSection from '@/components/features-section';
import Footer from '@/components/footer';

export default function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation />
      <main>
        <HeroSection />
        <SocialProofSection />
      </main>
      <Footer />
    </div>
  );
}
