import { Mic, Volume2, User, Bot } from 'lucide-react';
import { useRef, useEffect } from 'react';

interface ConversationMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function TranscriptPanel({
  transcript,
  onTranscriptChange,
  isRecording,
  conversationMessages = [],
  aiSpeaking = false,
}: {
  transcript: string;
  onTranscriptChange: (text: string) => void;
  isRecording: boolean;
  conversationMessages?: ConversationMessage[];
  aiSpeaking?: boolean;
}) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [conversationMessages]);

  const hasConversation = conversationMessages.length > 0;

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b border-border flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Mic className={`w-4 h-4 ${isRecording ? 'text-red-500 animate-pulse' : 'text-muted-foreground'}`} />
          <h3 className="font-semibold text-sm">
            {hasConversation ? 'Conversation' : 'Transcript'}
          </h3>
        </div>
        {aiSpeaking && (
          <span className="flex items-center gap-1 text-xs text-blue-500">
            <Volume2 className="w-3 h-3 animate-pulse" />
            AI Speaking
          </span>
        )}
      </div>

      {hasConversation ? (
        // Show conversation messages
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {conversationMessages.map((msg, index) => (
            <div
              key={index}
              className={`flex gap-2 ${msg.role === 'assistant' ? 'flex-row' : 'flex-row-reverse'}`}
            >
              <div className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center transition-all duration-300 ${
                msg.role === 'assistant'
                  ? 'bg-gradient-to-br from-blue-500/30 via-purple-500/30 to-pink-500/30 shadow-sm'
                  : 'bg-green-500/20'
              }`}>
                {msg.role === 'assistant' ? (
                  <Bot className="w-3 h-3 text-blue-500" />
                ) : (
                  <User className="w-3 h-3 text-green-500" />
                )}
              </div>
              <div className={`flex-1 p-2 rounded-lg text-sm ${
                msg.role === 'assistant'
                  ? 'bg-blue-500/10 text-foreground'
                  : 'bg-green-500/10 text-foreground'
              }`}>
                <p>{msg.content}</p>
                <span className="text-xs text-muted-foreground mt-1 block">
                  {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      ) : (
        // Show transcript textarea when no conversation
        <textarea
          value={transcript}
          onChange={(e) => onTranscriptChange(e.target.value)}
          placeholder="Your response will appear here when recording..."
          className="flex-1 p-4 bg-background text-foreground placeholder-muted-foreground resize-none focus:outline-none text-sm leading-relaxed"
          readOnly={isRecording}
        />
      )}

      {transcript && !hasConversation && (
        <div className="border-t border-border p-4 bg-muted/50">
          <div className="flex justify-between items-center text-xs text-muted-foreground">
            <span>{transcript.length} characters</span>
            <span>{transcript.split(/\s+/).filter((w) => w).length} words</span>
          </div>
        </div>
      )}

      {hasConversation && (
        <div className="border-t border-border p-3 bg-muted/50">
          <div className="text-xs text-muted-foreground text-center">
            {conversationMessages.length} messages in conversation
          </div>
        </div>
      )}
    </div>
  );
}
