import { Card } from '@/components/ui/card';
import { useState } from 'react';
import { Bell, Mail, MessageSquare, Trophy } from 'lucide-react';

export default function NotificationSettings() {
  const [notifications, setNotifications] = useState({
    emailNotifications: true,
    newInterviewReminders: true,
    performanceUpdates: true,
    achievementNotifications: true,
    weeklyDigest: false,
    marketingEmails: false,
  });

  const notificationOptions = [
    {
      id: 'emailNotifications',
      icon: Mail,
      title: 'Email Notifications',
      description: 'Receive notifications via email',
    },
    {
      id: 'newInterviewReminders',
      icon: Bell,
      title: 'Interview Reminders',
      description: 'Get reminded to practice interviews',
    },
    {
      id: 'performanceUpdates',
      icon: MessageSquare,
      title: 'Performance Updates',
      description: 'Receive weekly performance summaries',
    },
    {
      id: 'achievementNotifications',
      icon: Trophy,
      title: 'Achievement Badges',
      description: 'Get notified when you earn new badges',
    },
    {
      id: 'weeklyDigest',
      icon: Mail,
      title: 'Weekly Digest',
      description: 'Comprehensive summary of your week',
    },
    {
      id: 'marketingEmails',
      icon: Mail,
      title: 'Marketing Emails',
      description: 'Hear about new features and updates',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-6">Notification Preferences</h2>

        <div className="space-y-4">
          {notificationOptions.map((option) => {
            const Icon = option.icon;
            return (
              <Card
                key={option.id}
                className="bg-card border-border p-4 flex items-center justify-between hover:border-primary/50 transition-colors cursor-pointer"
                onClick={() =>
                  setNotifications({
                    ...notifications,
                    [option.id]: !notifications[option.id as keyof typeof notifications],
                  })
                }
              >
                <div className="flex items-start gap-4 flex-1">
                  <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center mt-1">
                    <Icon className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground">{option.title}</h3>
                    <p className="text-sm text-muted-foreground">{option.description}</p>
                  </div>
                </div>

                <input
                  type="checkbox"
                  checked={notifications[option.id as keyof typeof notifications]}
                  onChange={() => {}}
                  className="w-5 h-5 rounded border-border"
                />
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
}
