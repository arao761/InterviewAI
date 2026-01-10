'use client';

import { useEffect, useState, useRef } from 'react';
import { User, Sparkles } from 'lucide-react';

interface ProfessionalAvatarProps {
  isSpeaking: boolean;
  name?: string;
  role?: string;
  avatarColor?: string;
}

export default function ProfessionalAvatar({
  isSpeaking,
  name = 'AI Interviewer',
  role = 'Technical Recruiter',
  avatarColor = 'blue'
}: ProfessionalAvatarProps) {
  const [audioLevels, setAudioLevels] = useState<number[]>(new Array(20).fill(0));
  const animationRef = useRef<number | undefined>(undefined);

  // Color configurations
  const colorSchemes = {
    blue: {
      gradient: 'from-blue-600 to-blue-400',
      ring: 'ring-blue-500/50',
      glow: 'shadow-blue-500/30',
      badge: 'bg-blue-500',
    },
    purple: {
      gradient: 'from-purple-600 to-purple-400',
      ring: 'ring-purple-500/50',
      glow: 'shadow-purple-500/30',
      badge: 'bg-purple-500',
    },
    green: {
      gradient: 'from-green-600 to-green-400',
      ring: 'ring-green-500/50',
      glow: 'shadow-green-500/30',
      badge: 'bg-green-500',
    }
  };

  const colors = colorSchemes[avatarColor as keyof typeof colorSchemes] || colorSchemes.blue;

  // Simulate audio levels when speaking
  useEffect(() => {
    if (isSpeaking) {
      const animate = () => {
        const newLevels = audioLevels.map(() => Math.random());
        setAudioLevels(newLevels);
        animationRef.current = requestAnimationFrame(animate);
      };
      animate();
    } else {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
      setAudioLevels(new Array(20).fill(0));
    }

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isSpeaking]);

  return (
    <div className="flex flex-col items-center gap-6">
      {/* Avatar Container with Professional Design */}
      <div className="relative">
        {/* Outer Ring - Active State */}
        <div className={`
          absolute inset-0 rounded-full
          ${isSpeaking ? `ring-4 ${colors.ring} ${colors.glow} shadow-2xl` : 'ring-2 ring-border shadow-lg'}
          transition-all duration-300
        `} />

        {/* Main Avatar Circle */}
        <div className={`
          relative w-32 h-32 rounded-full
          bg-gradient-to-br ${colors.gradient}
          flex items-center justify-center
          ${isSpeaking ? 'scale-105' : 'scale-100'}
          transition-all duration-300
          overflow-hidden
        `}>
          {/* Background Pattern */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(255,255,255,0.8),transparent_50%)]" />
          </div>

          {/* Avatar Icon */}
          <div className="relative z-10">
            <User className="w-16 h-16 text-white" strokeWidth={1.5} />
          </div>

          {/* Animated Overlay when speaking */}
          {isSpeaking && (
            <div className="absolute inset-0 bg-white/10 animate-pulse" />
          )}

          {/* AI Badge */}
          <div className="absolute -bottom-1 -right-1 w-10 h-10 bg-white dark:bg-gray-800 rounded-full flex items-center justify-center shadow-lg">
            <Sparkles className={`w-5 h-5 ${colors.badge} bg-clip-text text-transparent`} fill="currentColor" />
          </div>
        </div>

        {/* Speaking Indicator Ring */}
        {isSpeaking && (
          <>
            <div className="absolute inset-0 rounded-full border-2 border-white/30 animate-ping" />
            <div
              className="absolute inset-0 rounded-full border-2 border-white/20 animate-ping"
              style={{ animationDelay: '0.5s', animationDuration: '2s' }}
            />
          </>
        )}
      </div>

      {/* Name and Role */}
      <div className="text-center space-y-1">
        <h3 className="text-xl font-semibold text-foreground">{name}</h3>
        <p className="text-sm text-muted-foreground">{role}</p>
      </div>

      {/* Status Badge */}
      <div className={`
        px-6 py-2 rounded-full font-medium text-sm
        transition-all duration-300
        ${isSpeaking
          ? `${colors.badge} text-white shadow-lg`
          : 'bg-muted text-muted-foreground'
        }
      `}>
        {isSpeaking ? 'Speaking' : 'Listening'}
      </div>

      {/* Audio Visualization Bar */}
      {isSpeaking && (
        <div className="flex items-end gap-1 h-16 w-64 justify-center">
          {audioLevels.map((level, index) => (
            <div
              key={index}
              className={`w-2 bg-gradient-to-t ${colors.gradient} rounded-full transition-all duration-100`}
              style={{
                height: `${10 + level * 70}%`,
                opacity: 0.5 + level * 0.5
              }}
            />
          ))}
        </div>
      )}

      {/* Subtitle when listening */}
      {!isSpeaking && (
        <p className="text-xs text-muted-foreground max-w-xs text-center">
          Ready to hear your response
        </p>
      )}
    </div>
  );
}
