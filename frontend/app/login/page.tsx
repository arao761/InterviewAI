'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Loader2 } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [statusMessage, setStatusMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setStatusMessage('');
    setLoading(true);

    try {
      await login(email, password, (status) => {
        setStatusMessage(status);
      });
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Login failed');
      setStatusMessage('');
    } finally {
      setLoading(false);
      setStatusMessage('');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center px-4 py-12">
      <Card className="w-full max-w-md p-8 shadow-xl border-2 hover-lift animate-in">
        <div className="mb-8 text-center animate-in" style={{ animationDelay: '0.1s' }}>
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg">
            <svg className="w-8 h-8 text-primary-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold mb-2 gradient-text">Welcome Back</h1>
          <p className="text-muted-foreground">Sign in to your account</p>
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

        {statusMessage && !error && (
          <div className="bg-primary/10 border border-primary/30 text-primary px-4 py-3 rounded-lg mb-6 animate-in shadow-sm" style={{ animationDelay: '0.2s' }}>
            <div className="flex items-center gap-2">
              <Loader2 className="h-5 w-5 animate-spin flex-shrink-0" />
              <span>{statusMessage}</span>
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6 stagger-children">
          <div className="animate-in" style={{ animationDelay: '0.3s' }}>
            <Label htmlFor="email" className="text-sm font-semibold">Email</Label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="Enter your email"
              autoComplete="email"
              className="mt-2 transition-all focus:ring-2 focus:ring-primary/50 focus:border-primary"
            />
          </div>

          <div className="animate-in" style={{ animationDelay: '0.4s' }}>
            <div className="flex items-center justify-between mb-1">
            <Label htmlFor="password" className="text-sm font-semibold">Password</Label>
              <Link href="/forgot-password" className="text-sm text-primary hover:text-accent transition-colors font-medium">
                Forgot password?
              </Link>
            </div>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Enter your password"
              autoComplete="current-password"
              className="mt-2 transition-all focus:ring-2 focus:ring-primary/50 focus:border-primary"
            />
          </div>

          <Button
            type="submit"
            disabled={loading}
            className="w-full mt-8 bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 text-primary-foreground font-semibold py-6 shadow-lg hover:shadow-xl transition-all duration-300 animate-in"
            style={{ animationDelay: '0.5s' }}
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                {statusMessage || 'Signing in...'}
              </>
            ) : (
              'Sign In'
            )}
          </Button>
        </form>

        <div className="mt-6 text-center text-sm text-muted-foreground animate-in" style={{ animationDelay: '0.6s' }}>
          Don't have an account?{' '}
          <Link href="/register" className="text-primary hover:text-accent font-semibold transition-colors">
            Sign up
          </Link>
        </div>
      </Card>
    </div>
  );
}
