'use client';

import { useEffect, useState, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import Navigation from '@/components/navigation';
import Footer from '@/components/footer';
import { CheckCircle, Loader2 } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { apiClient } from '@/lib/api/client';

function PaymentSuccessContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const [subscription, setSubscription] = useState<any>(null);
  const [sessionDetails, setSessionDetails] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
      return;
    }

    const sessionId = searchParams.get('session_id');

    const fetchData = async () => {
      try {
        // Fetch subscription from our backend
        const sub = await apiClient.getSubscription();
        setSubscription(sub);

        // If we have a session_id, verify it with backend
        if (sessionId) {
          try {
            const session = await apiClient.getCheckoutSession(sessionId);
            setSessionDetails(session);
          } catch (err) {
            console.warn('Could not fetch session details:', err);
            // Not critical, continue without session details
          }
        }
      } catch (error: any) {
        console.error('Error fetching subscription:', error);
        setError(error.message || 'Failed to load subscription details');
      } finally {
        setLoading(false);
      }
    };

    if (isAuthenticated) {
      fetchData();
    }
  }, [isAuthenticated, authLoading, router, searchParams]);

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation />
      <main className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <Card className="p-8 text-center">
          {loading ? (
            <div className="py-12">
              <Loader2 className="w-12 h-12 animate-spin mx-auto mb-4 text-primary" />
              <p className="text-muted-foreground">Loading subscription details...</p>
            </div>
          ) : (
            <>
              <div className="mb-6">
                <div className="w-16 h-16 rounded-full bg-green-500/20 flex items-center justify-center mx-auto mb-4">
                  <CheckCircle className="w-10 h-10 text-green-500" />
                </div>
                <h1 className="text-3xl font-bold mb-2">Payment Successful!</h1>
                <p className="text-muted-foreground">
                  Thank you for your subscription. Your account has been upgraded.
                </p>
              </div>

              {error && (
                <div className="mb-6 p-4 bg-destructive/10 border border-destructive text-destructive rounded-lg">
                  {error}
                </div>
              )}

              {sessionDetails && sessionDetails.status === 'open' && (
                <div className="mb-6 p-4 bg-yellow-500/10 border border-yellow-500 text-yellow-700 dark:text-yellow-400 rounded-lg">
                  <p>Your checkout session is still open. Please complete the payment.</p>
                </div>
              )}

              {subscription && (
                <div className="mb-8 p-6 bg-muted/50 rounded-lg text-left">
                  <h2 className="font-semibold mb-4">Subscription Details</h2>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Plan:</span>
                      <span className="font-medium capitalize">{subscription.plan || 'N/A'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Status:</span>
                      <span className="font-medium capitalize">{subscription.status || 'N/A'}</span>
                    </div>
                    {sessionDetails?.customer_details?.email && (
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Email:</span>
                        <span className="font-medium">{sessionDetails.customer_details.email}</span>
                      </div>
                    )}
                    {subscription.current_period_end && (
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Next billing date:</span>
                        <span className="font-medium">
                          {new Date(subscription.current_period_end).toLocaleDateString()}
                        </span>
                      </div>
                    )}
                    {subscription.trial_end && (
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Trial ends:</span>
                        <span className="font-medium">
                          {new Date(subscription.trial_end).toLocaleDateString()}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/dashboard">
                  <Button size="lg" className="w-full sm:w-auto">
                    Go to Dashboard
                  </Button>
                </Link>
                <Link href="/interview-setup">
                  <Button size="lg" variant="outline" className="w-full sm:w-auto">
                    Start Interview
                  </Button>
                </Link>
              </div>
            </>
          )}
        </Card>
      </main>
      <Footer />
    </div>
  );
}

export default function PaymentSuccessPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-background text-foreground">
        <Navigation />
        <main className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <Card className="p-8 text-center">
            <div className="py-12">
              <Loader2 className="w-12 h-12 animate-spin mx-auto mb-4 text-primary" />
              <p className="text-muted-foreground">Loading...</p>
            </div>
          </Card>
        </main>
        <Footer />
      </div>
    }>
      <PaymentSuccessContent />
    </Suspense>
  );
}

