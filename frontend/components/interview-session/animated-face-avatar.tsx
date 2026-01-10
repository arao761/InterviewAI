'use client';

import { useEffect, useState, useRef } from 'react';

interface AnimatedFaceAvatarProps {
  isSpeaking: boolean;
  name?: string;
}

export default function AnimatedFaceAvatar({
  isSpeaking,
  name = 'AI Interviewer'
}: AnimatedFaceAvatarProps) {
  const [mouthAnimation, setMouthAnimation] = useState(0);
  const [eyeState, setEyeState] = useState<'open' | 'blink'>('open');
  const animationRef = useRef<number | undefined>(undefined);
  const blinkIntervalRef = useRef<NodeJS.Timeout | undefined>(undefined);

  // Mouth animation when speaking
  useEffect(() => {
    if (isSpeaking) {
      let frame = 0;
      const animate = () => {
        // Create mouth movement pattern (0-1 range)
        frame += 0.15;
        const value = Math.abs(Math.sin(frame)) * 0.8 + 0.2;
        setMouthAnimation(value);
        animationRef.current = requestAnimationFrame(animate);
      };
      animate();
    } else {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
      setMouthAnimation(0);
    }

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isSpeaking]);

  // Random eye blinking
  useEffect(() => {
    const blink = () => {
      setEyeState('blink');
      setTimeout(() => setEyeState('open'), 150);
    };

    // Blink every 3-5 seconds randomly
    const scheduleNextBlink = () => {
      const delay = 3000 + Math.random() * 2000;
      blinkIntervalRef.current = setTimeout(() => {
        blink();
        scheduleNextBlink();
      }, delay);
    };

    scheduleNextBlink();

    return () => {
      if (blinkIntervalRef.current) {
        clearTimeout(blinkIntervalRef.current);
      }
    };
  }, []);

  return (
    <div className="flex flex-col items-center gap-6">
      {/* Avatar Container */}
      <div className="relative">
        {/* Main Avatar */}
        <div
          className={`
            w-48 h-48 rounded-full
            bg-gradient-to-br from-blue-100 via-purple-50 to-pink-100
            dark:from-blue-900/30 dark:via-purple-900/30 dark:to-pink-900/30
            flex items-center justify-center
            transition-all duration-300
            ${isSpeaking ? 'scale-105 shadow-2xl shadow-blue-500/30' : 'scale-100 shadow-xl'}
            border-4 border-white dark:border-gray-800
            relative overflow-visible
          `}
        >
          {/* Glow effect when speaking */}
          {isSpeaking && (
            <div className="absolute inset-0 rounded-full bg-blue-400/20 animate-pulse" />
          )}

          {/* Face Container */}
          <div className="relative w-full h-full flex flex-col items-center justify-center">
            {/* Eyes */}
            <div className="flex gap-8 mb-4">
              {/* Left Eye */}
              <div className="relative w-6 h-6">
                <div
                  className={`
                    absolute inset-0 rounded-full bg-gray-800 dark:bg-gray-200
                    transition-all duration-150
                    ${eyeState === 'blink' ? 'scale-y-[0.1]' : 'scale-y-100'}
                  `}
                />
                {/* Pupil */}
                {eyeState === 'open' && (
                  <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-3 h-3 rounded-full bg-blue-500 dark:bg-blue-400">
                    {/* Highlight */}
                    <div className="absolute top-1 left-1 w-1.5 h-1.5 rounded-full bg-white/80" />
                  </div>
                )}
              </div>

              {/* Right Eye */}
              <div className="relative w-6 h-6">
                <div
                  className={`
                    absolute inset-0 rounded-full bg-gray-800 dark:bg-gray-200
                    transition-all duration-150
                    ${eyeState === 'blink' ? 'scale-y-[0.1]' : 'scale-y-100'}
                  `}
                />
                {/* Pupil */}
                {eyeState === 'open' && (
                  <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-3 h-3 rounded-full bg-blue-500 dark:bg-blue-400">
                    {/* Highlight */}
                    <div className="absolute top-1 left-1 w-1.5 h-1.5 rounded-full bg-white/80" />
                  </div>
                )}
              </div>
            </div>

            {/* Mouth */}
            <div className="relative mt-4">
              {isSpeaking ? (
                /* Speaking mouth - animated */
                <svg
                  width="48"
                  height="32"
                  viewBox="0 0 48 32"
                  className="text-gray-800 dark:text-gray-200"
                >
                  <ellipse
                    cx="24"
                    cy="16"
                    rx="20"
                    ry={8 + mouthAnimation * 12}
                    fill="currentColor"
                    className="transition-all duration-100"
                  />
                  {/* Tongue when mouth is open */}
                  {mouthAnimation > 0.5 && (
                    <ellipse
                      cx="24"
                      cy="20"
                      rx="12"
                      ry="6"
                      fill="#ff6b9d"
                      opacity="0.8"
                    />
                  )}
                </svg>
              ) : (
                /* Neutral smile when not speaking */
                <svg
                  width="48"
                  height="24"
                  viewBox="0 0 48 24"
                  className="text-gray-800 dark:text-gray-200"
                >
                  <path
                    d="M 8 8 Q 24 16 40 8"
                    stroke="currentColor"
                    strokeWidth="3"
                    fill="none"
                    strokeLinecap="round"
                  />
                </svg>
              )}
            </div>
          </div>

          {/* Ripple Effect when speaking */}
          {isSpeaking && (
            <>
              <div className="absolute inset-0 rounded-full border-4 border-blue-400/50 animate-ping" />
              <div className="absolute inset-0 rounded-full border-4 border-purple-400/30 animate-ping" style={{ animationDelay: '0.5s' }} />
            </>
          )}
        </div>

        {/* Sound waves visualization */}
        {isSpeaking && (
          <div className="absolute -left-16 top-1/2 transform -translate-y-1/2 flex flex-col gap-1">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="h-1 bg-blue-500 rounded-full animate-pulse"
                style={{
                  width: `${20 + i * 8}px`,
                  animationDelay: `${i * 0.2}s`
                }}
              />
            ))}
          </div>
        )}

        {isSpeaking && (
          <div className="absolute -right-16 top-1/2 transform -translate-y-1/2 flex flex-col gap-1 items-end">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="h-1 bg-blue-500 rounded-full animate-pulse"
                style={{
                  width: `${20 + i * 8}px`,
                  animationDelay: `${i * 0.2}s`
                }}
              />
            ))}
          </div>
        )}
      </div>

      {/* Name and Status */}
      <div className="text-center space-y-1">
        <p className="text-lg font-semibold text-foreground">{name}</p>
        <div className={`
          text-sm font-medium px-4 py-1.5 rounded-full inline-block
          ${isSpeaking
            ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
            : 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'
          }
          transition-colors duration-300
        `}>
          {isSpeaking ? 'Speaking...' : 'Listening'}
        </div>
      </div>
    </div>
  );
}
