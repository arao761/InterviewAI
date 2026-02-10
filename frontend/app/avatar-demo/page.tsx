'use client';

import { useState } from 'react';
import AnimatedFaceAvatar from '@/components/interview-session/animated-face-avatar';
import TalkingAvatar from '@/components/interview-session/talking-avatar';
import ProfessionalAvatar from '@/components/interview-session/professional-avatar';
import { Button } from '@/components/ui/button';

/**
 * Avatar Demo Page
 *
 * This page demonstrates all three avatar components available for the interview interface.
 * Access this page at: /avatar-demo
 *
 * This is a development/preview page to help choose and test different avatar styles.
 */
export default function AvatarDemoPage() {
  const [isSpeaking, setIsSpeaking] = useState(false);

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-12 text-center">
          <h1 className="text-4xl font-bold mb-4">Interview Avatar Components</h1>
          <p className="text-muted-foreground mb-6">
            Preview and test the different avatar styles available for the AI interviewer
          </p>

          {/* Control Panel */}
          <div className="flex justify-center gap-4">
            <Button
              onClick={() => setIsSpeaking(!isSpeaking)}
              size="lg"
              className={isSpeaking ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'}
            >
              {isSpeaking ? 'Stop Speaking' : 'Start Speaking'}
            </Button>
          </div>
        </div>

        {/* Avatar Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          {/* Animated Face Avatar */}
          <div className="bg-card border border-border rounded-lg p-8">
            <div className="mb-6 pb-4 border-b border-border">
              <h2 className="text-xl font-semibold mb-2">Animated Face Avatar</h2>
              <p className="text-sm text-muted-foreground">
                Friendly, cartoon-style with realistic facial animations
              </p>
              <div className="mt-2 text-xs text-muted-foreground">
                <strong>Best for:</strong> Behavioral interviews
              </div>
            </div>
            <div className="flex justify-center py-8">
              <AnimatedFaceAvatar
                isSpeaking={isSpeaking}
                name="AI Interviewer"
              />
            </div>
          </div>

          {/* Talking Avatar */}
          <div className="bg-card border border-border rounded-lg p-8">
            <div className="mb-6 pb-4 border-b border-border">
              <h2 className="text-xl font-semibold mb-2">Talking Avatar</h2>
              <p className="text-sm text-muted-foreground">
                Modern gradient design with waveform visualization
              </p>
              <div className="mt-2 text-xs text-muted-foreground">
                <strong>Best for:</strong> Modern tech interviews
              </div>
            </div>
            <div className="flex justify-center py-8">
              <TalkingAvatar
                isSpeaking={isSpeaking}
                name="AI Interviewer"
                style="circle"
                size="lg"
              />
            </div>
          </div>

          {/* Professional Avatar */}
          <div className="bg-card border border-border rounded-lg p-8">
            <div className="mb-6 pb-4 border-b border-border">
              <h2 className="text-xl font-semibold mb-2">Professional Avatar</h2>
              <p className="text-sm text-muted-foreground">
                Clean, business-like design with audio visualization
              </p>
              <div className="mt-2 text-xs text-muted-foreground">
                <strong>Best for:</strong> Professional/corporate settings
              </div>
            </div>
            <div className="flex justify-center py-8">
              <ProfessionalAvatar
                isSpeaking={isSpeaking}
                name="Sarah Chen"
                role="Senior Recruiter"
                avatarColor="blue"
              />
            </div>
          </div>
        </div>

        {/* Variant Examples */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-6">Size Variants</h2>
          <div className="bg-card border border-border rounded-lg p-8">
            <div className="flex flex-wrap justify-center items-end gap-8">
              <div className="text-center">
                <TalkingAvatar isSpeaking={isSpeaking} size="sm" />
                <p className="text-xs text-muted-foreground mt-2">Small</p>
              </div>
              <div className="text-center">
                <TalkingAvatar isSpeaking={isSpeaking} size="md" />
                <p className="text-xs text-muted-foreground mt-2">Medium</p>
              </div>
              <div className="text-center">
                <TalkingAvatar isSpeaking={isSpeaking} size="lg" />
                <p className="text-xs text-muted-foreground mt-2">Large</p>
              </div>
              <div className="text-center">
                <TalkingAvatar isSpeaking={isSpeaking} size="xl" />
                <p className="text-xs text-muted-foreground mt-2">Extra Large</p>
              </div>
            </div>
          </div>
        </div>

        {/* Color Variants */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-6">Color Variants (Professional Avatar)</h2>
          <div className="bg-card border border-border rounded-lg p-8">
            <div className="flex flex-wrap justify-center items-start gap-12">
              <div className="text-center">
                <ProfessionalAvatar
                  isSpeaking={isSpeaking}
                  name="Alex Blue"
                  role="Tech Lead"
                  avatarColor="blue"
                />
                <p className="text-xs text-muted-foreground mt-2">Blue Theme</p>
              </div>
              <div className="text-center">
                <ProfessionalAvatar
                  isSpeaking={isSpeaking}
                  name="Jordan Purple"
                  role="Product Manager"
                  avatarColor="purple"
                />
                <p className="text-xs text-muted-foreground mt-2">Purple Theme</p>
              </div>
              <div className="text-center">
                <ProfessionalAvatar
                  isSpeaking={isSpeaking}
                  name="Morgan Green"
                  role="Engineering Manager"
                  avatarColor="green"
                />
                <p className="text-xs text-muted-foreground mt-2">Green Theme</p>
              </div>
            </div>
          </div>
        </div>

        {/* Implementation Guide */}
        <div className="bg-card border border-border rounded-lg p-8">
          <h2 className="text-2xl font-bold mb-4">Implementation</h2>
          <p className="text-muted-foreground mb-4">
            These avatars are already integrated into the interview page. The AnimatedFaceAvatar
            is currently used by default.
          </p>

          <div className="bg-muted/50 rounded-lg p-4 mb-4">
            <h3 className="font-semibold mb-2">Current Usage:</h3>
            <pre className="text-xs overflow-x-auto">
{`// In /app/interview/page.tsx
<AnimatedFaceAvatar
  isSpeaking={aiSpeaking}
  name="AI Interviewer"
/>`}
            </pre>
          </div>

          <div className="bg-muted/50 rounded-lg p-4">
            <h3 className="font-semibold mb-2">To Switch Avatars:</h3>
            <ol className="text-sm space-y-2 list-decimal list-inside">
              <li>Import the desired avatar component</li>
              <li>Replace the component in the interview page JSX</li>
              <li>Adjust props as needed (size, color, etc.)</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
}
