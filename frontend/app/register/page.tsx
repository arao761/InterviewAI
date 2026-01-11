'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Loader2 } from 'lucide-react';

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuth();
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

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
      await register(email, name, password);
      // TEMPORARILY DISABLED - Redirect to login instead of email verification
      router.push('/login');
    } catch (err: any) {
      setError(err.message || 'Registration failed');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center px-4 py-12">
      <Card className="w-full max-w-md p-8 shadow-xl border-2 hover-lift animate-in">
        <div className="mb-8 text-center animate-in" style={{ animationDelay: '0.1s' }}>
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg">
            <svg className="w-8 h-8 text-primary-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold mb-2 gradient-text">Create Account</h1>
          <p className="text-muted-foreground">Sign up to get started</p>
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

        <form onSubmit={handleSubmit} className="space-y-6 stagger-children">
          <div className="animate-in" style={{ animationDelay: '0.3s' }}>
            <label htmlFor="name" className="block text-sm font-semibold mb-1">
              Name
            </label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              placeholder="Enter your name"
              autoComplete="name"
              className="w-full px-3 py-2.5 border rounded-lg bg-background transition-all focus:ring-2 focus:ring-primary/50 focus:border-primary"
            />
          </div>

          <div className="animate-in" style={{ animationDelay: '0.4s' }}>
            <label htmlFor="email" className="block text-sm font-semibold mb-1">
              Email
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

          <div className="animate-in" style={{ animationDelay: '0.5s' }}>
            <label htmlFor="password" className="block text-sm font-semibold mb-1">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              maxLength={72}
              placeholder="Enter your password"
              autoComplete="new-password"
              className="w-full px-3 py-2.5 border rounded-lg bg-background transition-all focus:ring-2 focus:ring-primary/50 focus:border-primary"
            />
          </div>

          <div className="animate-in" style={{ animationDelay: '0.6s' }}>
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
              placeholder="Confirm your password"
              autoComplete="new-password"
              className="w-full px-3 py-2.5 border rounded-lg bg-background transition-all focus:ring-2 focus:ring-primary/50 focus:border-primary"
            />
          </div>

          <Button
            type="submit"
            disabled={loading}
            className="w-full mt-8 bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 text-primary-foreground font-semibold py-6 shadow-lg hover:shadow-xl transition-all duration-300 animate-in"
            style={{ animationDelay: '0.7s' }}
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Creating account...
              </>
            ) : (
              'Sign Up'
            )}
          </Button>
        </form>

        <div className="mt-6 text-center text-sm text-muted-foreground animate-in" style={{ animationDelay: '0.8s' }}>
          Already have an account?{' '}
          <Link href="/login" className="text-primary hover:text-accent font-semibold transition-colors">
            Sign in
          </Link>
        </div>
      </Card>
    </div>
  );
}
