import { Card } from '@/components/ui/card';
import { useState } from 'react';
import { Shield, Lock, Eye } from 'lucide-react';

export default function PrivacySettings() {
  const [privacy, setPrivacy] = useState({
    profileVisibility: 'private',
    dataCollection: false,
    twoFactorEnabled: false,
    sessionTimeout: '30',
  });

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold mb-6">Privacy & Security</h2>

        {/* Two-Factor Authentication */}
        <div className="mb-8 p-6 rounded-lg border border-border bg-card hover:border-primary/50 transition-colors">
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <Lock className="w-5 h-5 text-primary" />
              </div>
              <div>
                <h3 className="font-semibold text-lg text-foreground">Two-Factor Authentication</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  Add an extra layer of security to your account
                </p>
              </div>
            </div>
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={privacy.twoFactorEnabled}
                onChange={(e) => setPrivacy({ ...privacy, twoFactorEnabled: e.target.checked })}
                className="w-5 h-5"
              />
              <span className="text-sm font-medium">
                {privacy.twoFactorEnabled ? 'Enabled' : 'Disabled'}
              </span>
            </label>
          </div>
        </div>

        {/* Profile Visibility */}
        <div className="mb-8">
          <label className="block text-sm font-semibold mb-4 text-foreground flex items-center gap-2">
            <Eye className="w-4 h-4" />
            Profile Visibility
          </label>
          <div className="space-y-3">
            {[
              { value: 'private', label: 'Private - Only you can see your profile' },
              { value: 'friends', label: 'Friends Only - Share with connections' },
              { value: 'public', label: 'Public - Anyone can see your profile' },
            ].map((option) => (
              <label key={option.value} className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted cursor-pointer">
                <input
                  type="radio"
                  name="visibility"
                  value={option.value}
                  checked={privacy.profileVisibility === option.value}
                  onChange={(e) => setPrivacy({ ...privacy, profileVisibility: e.target.value })}
                  className="w-4 h-4"
                />
                <span className="text-sm">{option.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Data Collection */}
        <div className="mb-8 p-6 rounded-lg border border-border bg-card">
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <Shield className="w-5 h-5 text-primary" />
              </div>
              <div>
                <h3 className="font-semibold text-foreground">Analytics & Improvement</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  Allow us to collect anonymous usage data to improve the platform
                </p>
              </div>
            </div>
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={privacy.dataCollection}
                onChange={(e) => setPrivacy({ ...privacy, dataCollection: e.target.checked })}
                className="w-5 h-5"
              />
            </label>
          </div>
        </div>

        {/* Session Timeout */}
        <div>
          <label className="block text-sm font-semibold mb-3 text-foreground">Session Timeout</label>
          <select
            value={privacy.sessionTimeout}
            onChange={(e) => setPrivacy({ ...privacy, sessionTimeout: e.target.value })}
            className="w-full px-4 py-2 bg-muted border border-border rounded-lg text-foreground focus:outline-none focus:border-primary transition-colors"
          >
            <option value="15">15 minutes</option>
            <option value="30">30 minutes</option>
            <option value="60">1 hour</option>
            <option value="never">Never</option>
          </select>
          <p className="text-xs text-muted-foreground mt-2">
            Automatically log out after this period of inactivity
          </p>
        </div>
      </div>
    </div>
  );
}
