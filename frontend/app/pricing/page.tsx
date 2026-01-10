'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import Navigation from '@/components/navigation';
import Footer from '@/components/footer';
import { Check, Loader2 } from 'lucide-react';
import { useScrollFadeIn } from '@/hooks/use-scroll-fade-in';
import { useAuth } from '@/context/AuthContext';
import { apiClient } from '@/lib/api/client';

export default function PricingPage() {
  const fadeInRef = useScrollFadeIn();
  const router = useRouter();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const [processingPlan, setProcessingPlan] = useState<string | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const pricingSection = document.getElementById('pricing-plans');
    if (pricingSection) {
      pricingSection.scrollIntoView({ behavior: 'smooth' });
    }
  }, []);

  const handlePlanClick = async (planName: string, planKey: string) => {
    setError('');

    // Enterprise plan - contact sales
    if (planKey === 'enterprise') {
      window.location.href = 'mailto:contact@interviewai.com?subject=Enterprise Plan Inquiry&body=Hi, I would like to learn more about the Enterprise plan for my organization.';
      return;
    }
    
    // Check if user is authenticated
    if (!isAuthenticated) {
      router.push('/login?redirect=/pricing');
      return;
    }
    
    // Create checkout session
    setProcessingPlan(planKey);
    try {
      console.log('Creating checkout session for plan:', planKey);
      const response = await apiClient.createCheckoutSession(
        planKey as 'starter' | 'professional'
      );
      console.log('Checkout session created:', response);
      
      if (response.checkout_url) {
      // Redirect to Stripe Checkout
        window.location.href = response.checkout_url;
      } else {
        throw new Error('No checkout URL received from server');
      }
    } catch (err: any) {
      console.error('Checkout error:', err);
      const errorMessage = err.message || err.detail || 'Failed to start checkout process';
      setError(errorMessage);
      setProcessingPlan(null);
      
      // Show more detailed error if Stripe is not configured
      if (errorMessage.includes('Stripe is not configured') || errorMessage.includes('not configured')) {
        setError('Stripe payment is not configured. Please contact support or check your Stripe API keys.');
      }
    }
  };

  const plans = [
    {
      name: 'Starter',
      key: 'starter',
      price: '$9',
      period: '/month',
      description: 'Perfect for beginners',
      features: [
        '5 interviews per month',
        'Basic feedback',
        'Interview history',
        'Email support',
      ],
      cta: 'Get Started',
      highlight: false,
    },
    {
      name: 'Professional',
      key: 'professional',
      price: '$29',
      period: '/month',
      description: 'For serious candidates',
      features: [
        'Unlimited interviews',
        'AI-powered feedback',
        'Real-time transcript analysis',
        'Skill improvement tracking',
        'Priority support',
        'Custom interview types',
        '14-day free trial',
      ],
      cta: 'Start Free Trial',
      highlight: true,
    },
    {
      name: 'Enterprise',
      key: 'enterprise',
      price: 'Custom',
      period: 'pricing',
      description: 'For teams & organizations',
      features: [
        'Unlimited everything',
        'Team collaboration',
        'Analytics dashboard',
        'Custom AI models',
        'Dedicated support',
        'API access',
      ],
      cta: 'Contact Sales',
      highlight: false,
    },
  ];

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h1 className="text-4xl sm:text-5xl font-bold mb-4 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            Simple, Transparent Pricing
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Choose the perfect plan for your interview preparation journey
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-destructive/10 border border-destructive text-destructive rounded-lg">
            {error}
          </div>
        )}

        <div id="pricing-plans" ref={fadeInRef} className="grid md:grid-cols-3 gap-8 mb-16 fade-in-animation">
          {plans.map((plan, index) => (
            <Card
              key={index}
              className={`p-8 flex flex-col ${
                plan.highlight
                  ? 'border-2 border-primary ring-2 ring-primary/20 lg:scale-105'
                  : ''
              }`}
            >
              {plan.highlight && (
                <div className="mb-4 inline-block px-3 py-1 bg-primary text-primary-foreground rounded-full text-xs font-semibold w-fit">
                  Most Popular
                </div>
              )}
              <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
              <p className="text-muted-foreground mb-4">{plan.description}</p>
              <div className="mb-6">
                <span className="text-4xl font-bold">{plan.price}</span>
                <span className="text-muted-foreground ml-2">{plan.period}</span>
              </div>
              <Button
                size="lg"
                onClick={() => handlePlanClick(plan.name, plan.key)}
                disabled={processingPlan === plan.key || authLoading}
                className={`mb-8 w-full ${
                  plan.highlight
                    ? 'bg-primary text-primary-foreground hover:bg-primary/90'
                    : 'bg-accent text-accent-foreground hover:bg-accent/90'
                }`}
              >
                {processingPlan === plan.key ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Processing...
                  </>
                ) : (
                  plan.cta
                )}
              </Button>
              <div className="space-y-4 flex-1">
                {plan.features.map((feature, featureIndex) => (
                  <div key={featureIndex} className="flex gap-3 items-start">
                    <Check className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
                    <span className="text-sm">{feature}</span>
                  </div>
                ))}
              </div>
            </Card>
          ))}
        </div>

        <Card className="p-8 bg-card/50 border border-border">
          <h2 className="text-2xl font-bold mb-6 text-center">Frequently Asked Questions</h2>
          <div className="grid md:grid-cols-2 gap-8">
            {[
              {
                q: 'Can I switch plans anytime?',
                a: 'Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately.',
              },
              {
                q: 'Is there a free trial?',
                a: 'Professional plan users get a 14-day free trial with full access to all features.',
              },
              {
                q: 'What payment methods do you accept?',
                a: 'We accept all major credit cards, PayPal, and wire transfers for enterprise plans.',
              },
              {
                q: 'Do you offer refunds?',
                a: 'Yes, 30-day money-back guarantee if you are not satisfied with the service.',
              },
            ].map((faq, index) => (
              <div key={index}>
                <h3 className="font-semibold mb-2">{faq.q}</h3>
                <p className="text-sm text-muted-foreground">{faq.a}</p>
              </div>
            ))}
          </div>
        </Card>
      </main>
      <Footer />
    </div>
  );
}
