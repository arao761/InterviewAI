'use client';

import { Card } from '@/components/ui/card';
import Navigation from '@/components/navigation';
import Footer from '@/components/footer';
import { Users, Target, Zap } from 'lucide-react';
import Image from 'next/image';

export default function AboutPage() {
  const stats = [
    { label: 'Users Trained', value: '10K+' },
    { label: 'Interviews Conducted', value: '50K+' },
    { label: 'Success Rate', value: '95%' },
  ];

  const team = [
    {
      name: 'Ankit Rao',
      role: 'CEO & Co-founder',
      title: 'AI and NLP Integrator',
      bio: 'Previous Intern @Amazon, Meta, Google, accepted to Nvidia Ignite 2026',
      education: 'BACS and DS Minor @UVA',
      image: 'https://media.licdn.com/dms/image/v2/D4E03AQHcmUArD8p0YA/profile-displayphoto-shrink_400_400/B4EZce_HtgHkAs-/0/1748571553507?e=1764806400&v=beta&t=GD9XmnTud0Two5ZXMhU22PnL2JDRIrlC5C1XN2Vrwnw',
      gradient: 'from-primary to-accent',
    },
    {
      name: 'Pranav Vaddepalli',
      role: 'Co-founder',
      title: 'Backend Developer',
      bio: 'AI researcher with language models in the healthcare society',
      education: 'BSCS and DS Minor @UVA',
      image: 'https://avatars.dicebear.com/api/avataaars/pranav.svg?scale=80',
      gradient: 'from-accent to-secondary',
    },
    {
      name: 'Vaibhav Mahajan',
      role: 'Co-founder',
      title: 'Voice API Setup',
      bio: 'AI researcher in computer vision',
      education: 'BSCS and DS Minor @UVA',
      image: 'https://media.licdn.com/dms/image/v2/D4E03AQHVcpywd9gjIA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1721784103161?e=1764806400&v=beta&t=hBsvqFOete2VbeJfynOiPSGCBouYHM7rb4-VUcm0M-4',
      gradient: 'from-secondary to-primary',
    },
    {
      name: 'Kedaar Chennam',
      role: 'Co-founder',
      title: 'Frontend Developer',
      bio: 'Previous Intern @Microsoft',
      education: 'BACS, ECON, and DS Minor @UVA',
      image: 'https://media.licdn.com/dms/image/v2/D4E03AQHVcpywd9gjIA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1721784103161?e=1764806400&v=beta&t=hBsvqFOete2VbeJfynOiPSGCBouYHM7rb4-VUcm0M-4',
      gradient: 'from-primary via-accent to-secondary',
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
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        {/* Hero Section */}
        <div className="text-center mb-20">
          <div className="inline-block mb-4">
            <span className="text-sm font-semibold tracking-wider uppercase bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              About Us
            </span>
          </div>
          <h1 className="text-5xl sm:text-6xl font-bold mb-6 bg-gradient-to-r from-primary via-accent to-secondary bg-clip-text text-transparent">
            Meet the Team Behind InterviewAI
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Four passionate CS students from UVA on a mission to revolutionize interview preparation with AI
          </p>
        </div>

        {/* Team Section - Now at the top */}
        <div className="mb-24">
          <div className="grid md:grid-cols-2 gap-8">
            {team.map((member, index) => (
              <div key={index} className="group relative">
                {/* Glow effect */}
                <div className={`absolute -inset-0.5 bg-gradient-to-r ${member.gradient} rounded-3xl blur opacity-0 group-hover:opacity-30 transition duration-500`}></div>

                {/* Card */}
                <Card className="relative bg-card/50 backdrop-blur-sm border border-border rounded-3xl p-8 hover:border-primary/30 transition-all duration-300 overflow-hidden h-full">
                  {/* Background decoration */}
                  <div className={`absolute top-0 right-0 w-48 h-48 bg-gradient-to-br ${member.gradient} opacity-5 rounded-full blur-3xl group-hover:opacity-10 transition-opacity`}></div>

                  {/* Content */}
                  <div className="relative z-10 flex flex-col sm:flex-row gap-6 items-start">
                    {/* Profile Image */}
                    <div className="flex-shrink-0">
                      <div className={`p-1 rounded-2xl bg-gradient-to-br ${member.gradient}`}>
                        {member.image ? (
                          <Image
                            src={member.image || "/placeholder.svg"}
                            alt={member.name}
                            width={120}
                            height={120}
                            className="w-28 h-28 rounded-2xl object-cover bg-background"
                          />
                        ) : (
                          <div className={`w-28 h-28 rounded-2xl bg-gradient-to-br ${member.gradient}`} />
                        )}
                      </div>
                    </div>

                    {/* Info */}
                    <div className="flex-1 min-w-0">
                      <h3 className="text-2xl font-bold mb-1 group-hover:bg-gradient-to-r group-hover:from-primary group-hover:to-accent group-hover:bg-clip-text group-hover:text-transparent transition-all">
                        {member.name}
                      </h3>
                      <p className="text-primary font-semibold mb-1">{member.role}</p>
                      <p className="text-sm text-muted-foreground font-medium mb-3">{member.title}</p>

                      <div className="space-y-2 mb-4">
                        <p className="text-sm text-foreground leading-relaxed">{member.bio}</p>
                        <p className="text-sm text-muted-foreground">{member.education}</p>
                      </div>
                    </div>
                  </div>
                </Card>
              </div>
            ))}
          </div>
        </div>

        {/* Story Section */}
        <div className="relative mb-24">
          <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-accent/5 rounded-3xl blur-3xl"></div>
          <Card className="relative p-8 md:p-12 bg-card/50 backdrop-blur-sm border border-border/50 rounded-3xl">
            <h2 className="text-4xl font-bold mb-6 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">Our Story</h2>
            <div className="space-y-4 text-muted-foreground text-lg leading-relaxed">
              <p>
                InterviewAI was founded in 2025 by Ankit Rao, Pranav Vaddepalli, Vaibhav Mahajan, and Kedaar Chennam. As CS students at the University of Virginia, we know that the CS field is getting increasingly more difficult, especially when it comes to getting a job. This puts stress and forces people in the CS field to work extra hard to land even an entry level job.
              </p>
              <p>
                However, we decided to help you. By combining AI expertise with real interview experience, we built a platform that gives candidates the personalized coaching they need to succeed. Every interview is unique, and our AI learns from each one to provide better, more actionable feedback.
              </p>
            </div>
          </Card>
        </div>

        {/* Stats Section */}
        <div className="grid md:grid-cols-3 gap-8 mb-24">
          {stats.map((stat, index) => (
            <div key={index} className="relative group">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-primary to-accent rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-500"></div>
              <Card className="relative p-8 text-center bg-card/50 backdrop-blur-sm border border-border rounded-2xl hover:border-primary/30 transition-all">
                <div className="text-5xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent mb-2">{stat.value}</div>
                <p className="text-muted-foreground font-medium">{stat.label}</p>
              </Card>
            </div>
          ))}
        </div>

        {/* Values Section */}
        <div>
          <h2 className="text-4xl font-bold mb-12 text-center bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">Our Values</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {values.map((value, index) => {
              const IconComponent = value.icon;
              return (
                <div key={index} className="relative group">
                  <div className="absolute -inset-0.5 bg-gradient-to-r from-primary to-accent rounded-2xl blur opacity-0 group-hover:opacity-20 transition duration-500"></div>
                  <Card className="relative p-8 bg-card/50 backdrop-blur-sm border border-border rounded-2xl hover:border-primary/30 transition-all h-full">
                    <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-primary to-accent p-0.5 mb-6 group-hover:scale-110 transition-transform">
                      <div className="w-full h-full rounded-xl bg-background flex items-center justify-center">
                        <IconComponent className="w-7 h-7 text-primary" />
                      </div>
                    </div>
                    <h3 className="text-xl font-bold mb-3">{value.title}</h3>
                    <p className="text-muted-foreground leading-relaxed">{value.description}</p>
                  </Card>
                </div>
              );
            })}
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
