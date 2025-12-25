import { Card } from '@/components/ui/card';
import { useState } from 'react';

export default function PreferencesSettings() {
  const [preferences, setPreferences] = useState({
    interviewDuration: '30',
    difficulty: 'intermediate',
    language: 'english',
    theme: 'dark',
  });

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold mb-6">Interview Preferences</h2>

        {/* Default Interview Duration */}
        <div className="mb-6">
          <label className="block text-sm font-semibold mb-4 text-foreground">Default Interview Duration</label>
          <div className="space-y-2">
            {['15', '30', '60'].map((duration) => (
              <label key={duration} className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted cursor-pointer">
                <input
                  type="radio"
                  name="duration"
                  value={duration}
                  checked={preferences.interviewDuration === duration}
                  onChange={(e) => setPreferences({ ...preferences, interviewDuration: e.target.value })}
                  className="w-4 h-4"
                />
                <span className="text-sm">{duration} minutes</span>
              </label>
            ))}
          </div>
        </div>

        {/* Default Difficulty */}
        <div className="mb-6">
          <label className="block text-sm font-semibold mb-4 text-foreground">Default Difficulty Level</label>
          <div className="space-y-2">
            {[
              { value: 'beginner', label: 'Beginner' },
              { value: 'intermediate', label: 'Intermediate' },
              { value: 'advanced', label: 'Advanced' },
            ].map((opt) => (
              <label key={opt.value} className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted cursor-pointer">
                <input
                  type="radio"
                  name="difficulty"
                  value={opt.value}
                  checked={preferences.difficulty === opt.value}
                  onChange={(e) => setPreferences({ ...preferences, difficulty: e.target.value })}
                  className="w-4 h-4"
                />
                <span className="text-sm">{opt.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Language */}
        <div className="mb-6">
          <label className="block text-sm font-semibold mb-3 text-foreground">Language</label>
          <select
            value={preferences.language}
            onChange={(e) => setPreferences({ ...preferences, language: e.target.value })}
            className="w-full px-4 py-2 bg-muted border border-border rounded-lg text-foreground focus:outline-none focus:border-primary transition-colors"
          >
            <option value="english">English</option>
            <option value="spanish">Spanish</option>
            <option value="french">French</option>
            <option value="german">German</option>
            <option value="mandarin">Mandarin</option>
          </select>
        </div>

        {/* Theme */}
        <div>
          <label className="block text-sm font-semibold mb-4 text-foreground">Theme</label>
          <div className="grid grid-cols-3 gap-4">
            {[
              { value: 'light', label: 'Light' },
              { value: 'dark', label: 'Dark' },
              { value: 'auto', label: 'Auto' },
            ].map((theme) => (
              <label
                key={theme.value}
                className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                  preferences.theme === theme.value
                    ? 'border-primary bg-primary/5'
                    : 'border-border hover:border-primary/50'
                }`}
              >
                <input
                  type="radio"
                  name="theme"
                  value={theme.value}
                  checked={preferences.theme === theme.value}
                  onChange={(e) => setPreferences({ ...preferences, theme: e.target.value })}
                  className="sr-only"
                />
                <span className="font-medium text-sm">{theme.label}</span>
              </label>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
