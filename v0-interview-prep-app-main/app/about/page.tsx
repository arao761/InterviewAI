'use client';

import { useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import Navigation from '@/components/navigation';
import Footer from '@/components/footer';
import { Users, Target, Zap } from 'lucide-react';
import Image from 'next/image';

export default function AboutPage() {
  useEffect(() => {
    const teamSection = document.getElementById('team');
    if (teamSection) {
      teamSection.scrollIntoView({ behavior: 'smooth' });
    }
  }, []);

  const stats = [
    { label: 'Users Trained', value: '50,000+' },
    { label: 'Interviews Conducted', value: '500,000+' },
    { label: 'Success Rate', value: '94%' },
  ];

  const team = [
    {
      name: 'Ankit Rao',
      role: 'CEO & Co-founder + AI and NLP Integrator',
      bio: 'Previous Intern @Amazon, Meta, Google, accepted to Nvidia Ignite 2026\n      BACS and DS Minor @UVA',
      image: 'https://media.licdn.com/dms/image/v2/D4E03AQHcmUArD8p0YA/profile-displayphoto-shrink_400_400/B4EZce_HtgHkAs-/0/1748571553507?e=1764806400&v=beta&t=GD9XmnTud0Two5ZXMhU22PnL2JDRIrlC5C1XN2Vrwnw', // Replace with Bitmoji URL
    },
    {
      name: 'Pranav Vaddepalli',
      role: 'Co-founder + Backend Developer',
      bio: 'AI researcher with language models in the healtcare society\n      BSCS and DS Minor @UVA',
      image: 'https://avatars.dicebear.com/api/avataaars/pranav.svg?scale=80', // Replace with Bitmoji URL
    },
    {
      name: 'Vaibhav Mahajan',
      role: 'Co-founder + Voice API Setup',
      bio: 'AI researcher in computer vision\n      BSCS and DS Minor @UVA',
      image: 'https://media.licdn.com/dms/image/v2/D4E03AQHVcpywd9gjIA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1721784103161?e=1764806400&v=beta&t=hBsvqFOete2VbeJfynOiPSGCBouYHM7rb4-VUcm0M-4', // Replace with Bitmoji URL
    },
    {
      name: 'Kedaar Chennam',
      role: 'Co-founder + Frontend Developer',
      bio: 'Previous Intern @Microsoft\n      BACS, ECON, and DS Minor @UVA',
      image: 'https://media.licdn.com/dms/image/v2/D4E03AQHVcpywd9gjIA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1721784103161?e=1764806400&v=beta&t=hBsvqFOete2VbeJfynOiPSGCBouYHM7rb4-VUcm0M-4', // Replace with Bitmoji URL
    },
  ];

  const values = [
    {
      icon: Target,
      title: 'Mission-Driven',
      description: 'We believe everyone deserves access to world-class interview preparation.',
    },
    {
      icon: Zap,
      title: 'Innovation First',
      description: 'Cutting-edge AI technology that continuously learns and improves.',
    },
    {
      icon: Users,
      title: 'User-Centric',
      description: 'Every feature is designed with your success in mind.',
    },
  ];

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl sm:text-5xl font-bold mb-4 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            About InterviewAI
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Empowering job seekers with AI-powered interview coaching to land their dream jobs
          </p>
        </div>

        {/* Story Section */}
        <Card className="p-8 md:p-12 mb-16 bg-card/50">
          <h2 className="text-3xl font-bold mb-6">Our Story</h2>
          <div className="space-y-4 text-muted-foreground">
            <p>
              Getajob.io was founded in 2025 by Ankit Rao, Pranav Vaddepalli, Vaibhav Mahajan, and Kedaar Chennam. As CS students at the University of Virginia, we know that the CS field is getting increasingly more difficult, espescially when it comes to getting a job. This puts stress and forces people in the CS field to work extra hard to land even an entry level job.
            </p>
            <p>
              However, we decided help you. By combining AI expertise with real interview experience, we built a platform that gives candidates the personalized coaching they need to succeed. Every interview is unique, and our AI learns from each one to provide better, more actionable feedback.
            </p>
            
          </div>
        </Card>

        {/* Stats Section */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {stats.map((stat, index) => (
            <Card key={index} className="p-8 text-center bg-card/50">
              <div className="text-4xl font-bold text-primary mb-2">{stat.value}</div>
              <p className="text-muted-foreground">{stat.label}</p>
            </Card>
          ))}
        </div>

        {/* Values Section */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold mb-8 text-center">Our Values</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {values.map((value, index) => {
              const IconComponent = value.icon;
              return (
                <Card key={index} className="p-8 bg-card/50">
                  <IconComponent className="w-10 h-10 text-primary mb-4" />
                  <h3 className="text-xl font-bold mb-2">{value.title}</h3>
                  <p className="text-muted-foreground text-sm">{value.description}</p>
                </Card>
              );
            })}
          </div>
        </div>

        {/* Team Section */}
        <div id="team" className="mb-16">
          <h2 className="text-3xl font-bold mb-8 text-center">Meet Our Team</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {team.map((member, index) => (
              <Card key={index} className="p-6 bg-card/50 text-center">
                {member.image ? (
                  <Image
                    src={member.image || "/placeholder.svg"}
                    alt={member.name}
                    width={64}
                    height={64}
                    className="w-16 h-16 rounded-full mx-auto mb-4 object-cover"
                  />
                ) : (
                  <div className="w-16 h-16 rounded-full bg-gradient-to-r from-primary to-accent mx-auto mb-4" />
                )}
                <h3 className="font-bold text-lg mb-1">{member.name}</h3>
                <p className="text-primary text-sm font-semibold mb-3">{member.role}</p>
                <p className="text-muted-foreground text-sm">{member.bio}</p>
              </Card>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <Card className="p-8 md:p-12 text-center bg-gradient-to-r from-primary/10 to-accent/10 border border-primary/20">
          <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Interview Skills?</h2>
          <p className="text-muted-foreground mb-6 max-w-2xl mx-auto">
            Join thousands of successful candidates who have landed their dream jobs with InterviewAI.
          </p>
          <Button size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90">
            Start Your Free Trial
          </Button>
        </Card>
      </main>
      <Footer />
    </div>
  );
}
