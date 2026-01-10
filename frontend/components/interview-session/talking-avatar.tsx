'use client';

import { useEffect, useState, useRef } from 'react';
import { Bot, Volume2 } from 'lucide-react';

interface TalkingAvatarProps {
  isSpeaking: boolean;
  name?: string;
  style?: 'circle' | 'square';
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

export default function TalkingAvatar({
  isSpeaking,
  name = 'AI Interviewer',
  style = 'circle',
  size = 'lg'
}: TalkingAvatarProps) {
  const [waveform, setWaveform] = useState<number[]>([]);
  const animationRef = useRef<number | undefined>(undefined);

  // Size configurations
  const sizeConfig = {
    sm: { container: 'w-24 h-24', icon: 'w-8 h-8', text: 'text-xs' },
    md: { container: 'w-32 h-32', icon: 'w-12 h-12', text: 'text-sm' },
    lg: { container: 'w-40 h-40', icon: 'w-16 h-16', text: 'text-base' },
    xl: { container: 'w-64 h-64', icon: 'w-24 h-24', text: 'text-lg' }
  };

  const config = sizeConfig[size];

  // Generate waveform animation when speaking
  useEffect(() => {
    if (isSpeaking) {
      const generateWaveform = () => {
        const bars = Array.from({ length: 5 }, () => Math.random() * 100 + 30);
        setWaveform(bars);
        animationRef.current = requestAnimationFrame(generateWaveform);
      };
      generateWaveform();
    } else {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
      setWaveform([]);
    }

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isSpeaking]);

  return (
    <div className="flex flex-col items-center gap-4">
      {/* Avatar Container */}
      <div className="relative">
        {/* Main Avatar Circle */}
        <div
          className={`
            ${config.container}
            ${style === 'circle' ? 'rounded-full' : 'rounded-2xl'}
            bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500
            flex items-center justify-center
            transition-all duration-300
            ${isSpeaking ? 'scale-105 shadow-2xl shadow-blue-500/50' : 'scale-100 shadow-xl'}
            relative overflow-hidden
          `}
        >
          {/* Animated Background Gradient */}
          <div
            className={`
              absolute inset-0 bg-gradient-to-tr from-blue-600 via-purple-600 to-pink-600
              ${isSpeaking ? 'animate-pulse opacity-100' : 'opacity-0'}
              transition-opacity duration-300
            `}
          />

          {/* Ripple Effect when speaking */}
          {isSpeaking && (
            <>
              <div className={`absolute inset-0 ${style === 'circle' ? 'rounded-full' : 'rounded-2xl'} border-4 border-blue-400/50 animate-ping`} />
              <div className={`absolute inset-0 ${style === 'circle' ? 'rounded-full' : 'rounded-2xl'} border-4 border-purple-400/30 animate-ping`} style={{ animationDelay: '0.5s' }} />
            </>
          )}

          {/* Avatar Icon/Face */}
          <div className="relative z-10 flex flex-col items-center justify-center">
            <Bot className={`${config.icon} text-white drop-shadow-lg`} />
          </div>

          {/* Mouth Animation Overlay */}
          {isSpeaking && (
            <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2 z-20">
              <div className="w-8 h-4 bg-white/90 rounded-full animate-pulse" />
            </div>
          )}
        </div>

        {/* Speaking Indicator Badge */}
        {isSpeaking && (
          <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-3 py-1 rounded-full text-xs font-medium shadow-lg flex items-center gap-1 animate-bounce">
            <Volume2 className="w-3 h-3" />
            Speaking
          </div>
        )}
      </div>

      {/* Name Label */}
      <div className="text-center">
        <p className={`${config.text} font-semibold text-foreground`}>{name}</p>
        <p className="text-xs text-muted-foreground">
          {isSpeaking ? 'Speaking...' : 'Listening'}
        </p>
      </div>

      {/* Audio Waveform Visualization */}
      {isSpeaking && (
        <div className="flex items-center gap-1 h-12">
          {waveform.map((height, index) => (
            <div
              key={index}
              className="w-1 bg-gradient-to-t from-blue-500 to-purple-500 rounded-full transition-all duration-100"
              style={{
                height: `${height}%`,
                opacity: 0.7 + (height / 300)
              }}
            />
          ))}
        </div>
      )}
    </div>
  );
}
