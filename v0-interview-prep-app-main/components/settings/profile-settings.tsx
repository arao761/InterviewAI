import { Card } from '@/components/ui/card';
import { Upload } from 'lucide-react';
import { useState } from 'react';

export default function ProfileSettings() {
  const [profile, setProfile] = useState({
    firstName: 'John',
    lastName: 'Doe',
    email: 'john.doe@example.com',
    phone: '+1 (555) 123-4567',
    bio: 'Software engineer passionate about growth',
    location: 'San Francisco, CA',
  });

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold mb-6">Profile Information</h2>

        {/* Profile Picture */}
        <div className="mb-8">
          <label className="block text-sm font-semibold mb-4 text-foreground">Profile Picture</label>
          <div className="flex items-center gap-6">
            <div className="w-20 h-20 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center text-2xl font-bold text-primary-foreground">
              JD
            </div>
            <div>
              <button className="flex items-center gap-2 px-4 py-2 rounded-lg border border-border hover:bg-muted transition-colors text-sm font-medium">
                <Upload className="w-4 h-4" />
                Upload Photo
              </button>
              <p className="text-xs text-muted-foreground mt-2">JPG, PNG or GIF. Max 5MB</p>
            </div>
          </div>
        </div>

        {/* Form Fields */}
        <div className="grid md:grid-cols-2 gap-6">
          {[
            { label: 'First Name', value: 'firstName' },
            { label: 'Last Name', value: 'lastName' },
            { label: 'Email', value: 'email', type: 'email' },
            { label: 'Phone', value: 'phone' },
            { label: 'Location', value: 'location', colSpan: true },
          ].map((field) => (
            <div key={field.value} className={field.colSpan ? 'md:col-span-2' : ''}>
              <label className="block text-sm font-semibold mb-2 text-foreground">{field.label}</label>
              <input
                type={field.type || 'text'}
                value={profile[field.value as keyof typeof profile]}
                onChange={(e) => setProfile({ ...profile, [field.value]: e.target.value })}
                className="w-full px-4 py-2 bg-muted border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary transition-colors"
              />
            </div>
          ))}

          {/* Bio */}
          <div className="md:col-span-2">
            <label className="block text-sm font-semibold mb-2 text-foreground">Bio</label>
            <textarea
              value={profile.bio}
              onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
              rows={4}
              className="w-full px-4 py-2 bg-muted border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary transition-colors resize-none"
            />
          </div>
        </div>
      </div>

      {/* Danger Zone */}
      <div className="pt-8 border-t border-border">
        <h3 className="font-semibold text-lg mb-4 text-destructive">Danger Zone</h3>
        <Card className="bg-destructive/5 border border-destructive/20 p-6">
          <div className="flex justify-between items-center">
            <div>
              <h4 className="font-semibold text-foreground">Delete Account</h4>
              <p className="text-sm text-muted-foreground mt-1">Permanently delete your account and all data</p>
            </div>
            <button className="px-4 py-2 rounded-lg border border-destructive text-destructive hover:bg-destructive/10 transition-colors text-sm font-medium">
              Delete Account
            </button>
          </div>
        </Card>
      </div>
    </div>
  );
}
