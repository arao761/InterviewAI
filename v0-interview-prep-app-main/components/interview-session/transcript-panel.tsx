import { Card } from '@/components/ui/card';
import { Mic } from 'lucide-react';

export default function TranscriptPanel({
  transcript,
  onTranscriptChange,
  isRecording,
}: {
  transcript: string;
  onTranscriptChange: (text: string) => void;
  isRecording: boolean;
}) {
  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b border-border flex items-center gap-2">
        <Mic className={`w-4 h-4 ${isRecording ? 'text-red-500 animate-pulse' : 'text-muted-foreground'}`} />
        <h3 className="font-semibold text-sm">Live Transcript</h3>
      </div>

      <textarea
        value={transcript}
        onChange={(e) => onTranscriptChange(e.target.value)}
        placeholder="Your response will appear here when recording..."
        className="flex-1 p-4 bg-background text-foreground placeholder-muted-foreground resize-none focus:outline-none text-sm leading-relaxed"
        readOnly={isRecording}
      />

      {transcript && (
        <div className="border-t border-border p-4 bg-muted/50">
          <div className="flex justify-between items-center text-xs text-muted-foreground">
            <span>{transcript.length} characters</span>
            <span>{transcript.split(/\s+/).filter((w) => w).length} words</span>
          </div>
        </div>
      )}
    </div>
  );
}
