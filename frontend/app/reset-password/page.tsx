'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Loader2, CheckCircle2, XCircle, Lock } from 'lucide-react';

function ResetPasswordForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  // Get token from URL - token_urlsafe tokens are already URL-safe, no decoding needed
  // They contain only: A-Z, a-z, 0-9, -, _ which are all safe in URLs
  // Just use the token as-is from the URL parameter
  const token = searchParams.get('token');

  useEffect(() => {
    if (!token) {
      setError('No reset token provided. Please use the link from your email.');
    }
  }, [token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!token) {
      setError('No reset token provided');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    if (password.length > 72) {
      setError('Password cannot be longer than 72 characters');
      return;
    }

    setLoading(true);

    try {
      const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
      const response = await fetch(`${baseURL}/auth/reset-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token, new_password: password }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(true);
        // Redirect to login after 3 seconds
        setTimeout(() => {
          router.push('/login');
        }, 3000);
      } else {
        setError(data.detail || 'Password reset failed');
      }
    } catch (error: any) {
      setError(error.message || 'Failed to reset password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center px-4 py-12">
        <Card className="w-full max-w-md p-8 shadow-xl border-2 hover-lift animate-in">
          <div className="text-center">
            <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg animate-in" style={{ animationDelay: '0.1s' }}>
              <CheckCircle2 className="w-12 h-12 text-primary-foreground" />
            </div>
            <h1 className="text-2xl font-bold mb-2 gradient-text animate-in" style={{ animationDelay: '0.2s' }}>Password Reset Successful!</h1>
            <p className="text-muted-foreground mb-6 animate-in" style={{ animationDelay: '0.3s' }}>
              Your password has been reset successfully. You can now log in with your new password.
            </p>
            <p className="text-sm text-muted-foreground mb-6 animate-in" style={{ animationDelay: '0.4s' }}>Redirecting to login page...</p>
            <Link href="/login" className="animate-in" style={{ animationDelay: '0.5s' }}>
              <Button className="w-full bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 text-primary-foreground font-semibold py-6 shadow-lg hover:shadow-xl transition-all duration-300">
                Go to Login
              </Button>
            </Link>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center px-4 py-12">
      <Card className="w-full max-w-md p-8 shadow-xl border-2 hover-lift animate-in">
        <div className="mb-8 text-center animate-in" style={{ animationDelay: '0.1s' }}>
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg">
            <Lock className="w-8 h-8 text-primary-foreground" />
          </div>
          <h1 className="text-3xl font-bold mb-2 gradient-text">Reset Password</h1>
          <p className="text-muted-foreground">
            Enter your new password below.
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

        {!token && (
          <div className="bg-accent/10 border border-accent/30 text-accent px-4 py-3 rounded-lg mb-6 animate-in shadow-sm" style={{ animationDelay: '0.2s' }}>
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              <span>No reset token found. Please use the link from your email.</span>
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6 stagger-children">
          <div className="animate-in" style={{ animationDelay: '0.3s' }}>
            <label htmlFor="password" className="block text-sm font-semibold mb-1">
              New Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              maxLength={72}
              placeholder="Enter your new password"
              autoComplete="new-password"
              className="w-full px-3 py-2.5 border rounded-lg bg-background transition-all focus:ring-2 focus:ring-primary/50 focus:border-primary"
            />
            <p className="text-xs text-muted-foreground mt-1.5">
              Must be at least 8 characters long
            </p>
          </div>

          <div className="animate-in" style={{ animationDelay: '0.4s' }}>
            <label htmlFor="confirmPassword" className="block text-sm font-semibold mb-1">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              maxLength={72}
              placeholder="Confirm your new password"
              autoComplete="new-password"
              className="w-full px-3 py-2.5 border rounded-lg bg-background transition-all focus:ring-2 focus:ring-primary/50 focus:border-primary"
            />
          </div>

          <Button
            type="submit"
            disabled={loading || !token}
            className="w-full mt-8 bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 text-primary-foreground font-semibold py-6 shadow-lg hover:shadow-xl transition-all duration-300 animate-in disabled:opacity-50"
            style={{ animationDelay: '0.5s' }}
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Resetting...
              </>
            ) : (
              'Reset Password'
            )}
          </Button>
        </form>

        <div className="mt-6 text-center text-sm text-muted-foreground animate-in" style={{ animationDelay: '0.6s' }}>
          Remember your password?{' '}
          <Link href="/login" className="text-primary hover:text-accent font-semibold transition-colors">
            Sign in
          </Link>
        </div>
      </Card>
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center">
        <div className="w-16 h-16 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg">
          <Loader2 className="h-8 w-8 animate-spin text-primary-foreground" />
        </div>
      </div>
    }>
      <ResetPasswordForm />
    </Suspense>
  );
}

