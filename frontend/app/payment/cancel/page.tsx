'use client';

import Link from 'next/link';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import Navigation from '@/components/navigation';
import Footer from '@/components/footer';
import { XCircle } from 'lucide-react';

export default function PaymentCancelPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation />
      <main className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <Card className="p-8 text-center">
          <div className="mb-6">
            <div className="w-16 h-16 rounded-full bg-destructive/20 flex items-center justify-center mx-auto mb-4">
              <XCircle className="w-10 h-10 text-destructive" />
            </div>
            <h1 className="text-3xl font-bold mb-2">Payment Canceled</h1>
            <p className="text-muted-foreground">
              Your payment was canceled. No charges were made to your account.
            </p>
          </div>

          <div className="mb-8 p-6 bg-muted/50 rounded-lg">
            <p className="text-sm text-muted-foreground mb-4">
              If you encountered any issues during checkout, please try again or contact support.
            </p>
            <p className="text-sm text-muted-foreground">
              You can return to the pricing page to select a plan that works best for you.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/pricing">
              <Button size="lg" className="w-full sm:w-auto">
                Return to Pricing
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button size="lg" variant="outline" className="w-full sm:w-auto">
                Go to Dashboard
              </Button>
            </Link>
          </div>
        </Card>
      </main>
      <Footer />
    </div>
  );
}

