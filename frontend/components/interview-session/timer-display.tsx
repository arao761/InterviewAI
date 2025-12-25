import { Clock } from 'lucide-react';

export default function TimerDisplay({ timeRemaining }: { timeRemaining: number }) {
  const minutes = Math.floor(timeRemaining / 60);
  const seconds = timeRemaining % 60;

  const isLowTime = timeRemaining < 300; // Less than 5 minutes
  const isCritical = timeRemaining < 60; // Less than 1 minute

  return (
    <div
      className={`flex items-center gap-2 px-4 py-2 rounded-lg font-mono text-lg font-semibold ${
        isCritical
          ? 'bg-red-500/20 text-red-500 animate-pulse'
          : isLowTime
            ? 'bg-yellow-500/20 text-yellow-500'
            : 'bg-muted text-foreground'
      }`}
    >
      <Clock className="w-5 h-5" />
      <span>
        {minutes.toString().padStart(2, '0')}:{seconds.toString().padStart(2, '0')}
      </span>
    </div>
  );
}
