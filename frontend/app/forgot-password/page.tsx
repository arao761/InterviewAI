'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Loader2, Mail, CheckCircle2 } from 'lucide-react';

export default function ForgotPasswordPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess(false);

    if (!email) {
      setError('Please enter your email address');
      return;
    }

    setLoading(true);

    try {
      const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
      const response = await fetch(`${baseURL}/auth/forgot-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(true);
      } else {
        setError(data.detail || 'Failed to send password reset email');
      }
    } catch (error: any) {
      setError(error.message || 'Failed to send password reset email. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center px-4 py-12">
      <Card className="w-full max-w-md p-8 shadow-xl border-2 hover-lift animate-in">
        <div className="mb-8 text-center animate-in" style={{ animationDelay: '0.1s' }}>
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg">
            <Mail className="w-8 h-8 text-primary-foreground" />
          </div>
          <h1 className="text-3xl font-bold mb-2 gradient-text">Forgot Password?</h1>
          <p className="text-muted-foreground">
            Enter your email address and we'll send you a link to reset your password.
          </p>
        </div>

        {error && (
          <div className="bg-destructive/10 border border-destructive/30 text-destructive px-4 py-3 rounded-lg mb-6 animate-in shadow-sm" style={{ animationDelay: '0.2s' }}>
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <span>{error}</span>
            </div>
          </div>
        )}

        {success ? (
          <div className="text-center space-y-6 animate-in" style={{ animationDelay: '0.2s' }}>
            <div className="flex justify-center animate-in" style={{ animationDelay: '0.3s' }}>
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg">
                <CheckCircle2 className="w-12 h-12 text-primary-foreground" />
              </div>
            </div>
            <div className="animate-in" style={{ animationDelay: '0.4s' }}>
              <h2 className="text-xl font-semibold mb-2 gradient-text">Email Sent!</h2>
              <p className="text-muted-foreground mb-4">
                If an account with that email exists, we've sent a password reset link to <strong className="text-foreground">{email}</strong>.
              </p>
              <p className="text-sm text-muted-foreground">
                Please check your email and click the link to reset your password. The link will expire in 1 hour.
              </p>
            </div>
            <div className="space-y-3 animate-in" style={{ animationDelay: '0.5s' }}>
              <Link href="/login">
                <Button variant="outline" className="w-full border-2 hover:bg-primary/10 hover:border-primary transition-all">Back to Login</Button>
              </Link>
              <Button
                onClick={() => {
                  setSuccess(false);
                  setEmail('');
                }}
                className="w-full bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 text-primary-foreground font-semibold py-6 shadow-lg hover:shadow-xl transition-all duration-300"
              >
                Send Another Email
              </Button>
            </div>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-6 stagger-children">
            <div className="animate-in" style={{ animationDelay: '0.3s' }}>
              <label htmlFor="email" className="block text-sm font-semibold mb-1">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="Enter your email"
                autoComplete="email"
                className="w-full px-3 py-2.5 border rounded-lg bg-background transition-all focus:ring-2 focus:ring-primary/50 focus:border-primary"
              />
            </div>

            <Button
              type="submit"
              disabled={loading}
              className="w-full mt-8 bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 text-primary-foreground font-semibold py-6 shadow-lg hover:shadow-xl transition-all duration-300 animate-in"
              style={{ animationDelay: '0.4s' }}
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Sending...
                </>
              ) : (
                <>
                  <Mail className="mr-2 h-4 w-4" />
                  Send Reset Link
                </>
              )}
            </Button>
          </form>
        )}

        <div className="mt-6 text-center text-sm text-muted-foreground animate-in" style={{ animationDelay: '0.5s' }}>
          Remember your password?{' '}
          <Link href="/login" className="text-primary hover:text-accent font-semibold transition-colors">
            Sign in
          </Link>
        </div>
      </Card>
    </div>
  );
}

