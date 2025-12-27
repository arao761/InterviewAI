'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Mail, CheckCircle2 } from 'lucide-react';
import { apiClient } from '@/lib/api/client';

export default function VerifyEmailPendingPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const email = searchParams.get('email');
  const [resending, setResending] = useState(false);
  const [resendStatus, setResendStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [resendMessage, setResendMessage] = useState('');

  const handleResend = async () => {
    setResending(true);
    setResendStatus('idle');
    setResendMessage('');

    try {
      const token = apiClient.getToken();
      if (!token) {
        throw new Error('Please log in first to resend verification email');
      }

      const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
      const response = await fetch(`${baseURL}/auth/resend-verification`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        setResendStatus('success');
        setResendMessage('Verification email sent successfully!');
      } else {
        setResendStatus('error');
        setResendMessage(data.detail || 'Failed to resend verification email');
      }
    } catch (error: any) {
      setResendStatus('error');
      setResendMessage(error.message || 'Failed to resend verification email');
    } finally {
      setResending(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4">
      <Card className="w-full max-w-md p-8">
        <div className="text-center">
          <Mail className="w-16 h-16 mx-auto mb-4 text-primary" />
          <h1 className="text-2xl font-bold mb-2">Check Your Email</h1>
          <p className="text-muted-foreground mb-6">
            We've sent a verification email to <strong>{email || 'your email address'}</strong>.
            Please click the link in the email to verify your account.
          </p>

          <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-4 mb-6">
            <p className="text-sm text-blue-500">
              <strong>Note:</strong> The verification link will expire in 24 hours.
            </p>
          </div>

          {resendStatus === 'success' && (
            <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-3 mb-4">
              <p className="text-sm text-green-500 flex items-center justify-center gap-2">
                <CheckCircle2 className="w-4 h-4" />
                {resendMessage}
              </p>
            </div>
          )}

          {resendStatus === 'error' && (
            <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-3 mb-4">
              <p className="text-sm text-red-500">{resendMessage}</p>
            </div>
          )}

          <div className="space-y-3">
            <Button
              onClick={handleResend}
              disabled={resending}
              variant="outline"
              className="w-full"
            >
              {resending ? 'Sending...' : 'Resend Verification Email'}
            </Button>

            <Link href="/login">
              <Button className="w-full">Go to Login</Button>
            </Link>
          </div>

          <p className="text-sm text-muted-foreground mt-6">
            Already verified?{' '}
            <Link href="/login" className="text-primary hover:underline">
              Sign in
            </Link>
          </p>
        </div>
      </Card>
    </div>
  );
}

