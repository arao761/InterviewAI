'use client';

import { Quote, Star } from 'lucide-react';

export default function SocialProofSection() {
  const testimonials = [
    {
      name: 'Sarah Chen',
      role: 'Software Engineer at Google',
      content: 'InterviewAI helped me prepare for my Google interview. The real-time feedback was invaluable!',
      rating: 5,
    },
    {
      name: 'Marcus Johnson',
      role: 'Product Manager at Amazon',
      content: 'The AI coaching felt like having a personal interview coach. Landed my dream PM role!',
      rating: 5,
    },
    {
      name: 'Emily Rodriguez',
      role: 'Data Scientist at Meta',
      content: 'Practice sessions were incredibly realistic. Helped me build confidence for the real thing.',
      rating: 5,
    },
  ];

  const companies = [
    { name: 'Google', logo: '🔍' },
    { name: 'Meta', logo: '👥' },
    { name: 'Amazon', logo: '📦' },
    { name: 'Microsoft', logo: '💻' },
    { name: 'Apple', logo: '🍎' },
    { name: 'Netflix', logo: '🎬' },
  ];

  return (
    <section className="relative py-16 px-4 sm:px-6 lg:px-8 overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-card/30 to-background"></div>

      <div className="relative max-w-7xl mx-auto">
        {/* Companies Section */}
        <div className="mb-16">
          <p className="text-center text-sm text-muted-foreground mb-8 font-medium tracking-wider uppercase">
            Trusted by candidates joining top companies
          </p>
          <div className="flex flex-wrap justify-center items-center gap-8 md:gap-12">
            {companies.map((company, index) => (
              <div
                key={index}
                className="flex items-center gap-2 text-2xl opacity-60 hover:opacity-100 transition-opacity"
              >
                <span>{company.logo}</span>
                <span className="text-lg font-semibold text-foreground">{company.name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Testimonials */}
        <div className="grid md:grid-cols-3 gap-6">
          {testimonials.map((testimonial, index) => (
            <div
              key={index}
              className="relative group"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {/* Glow effect */}
              <div className="absolute -inset-0.5 bg-gradient-to-r from-primary to-accent rounded-2xl blur opacity-0 group-hover:opacity-20 transition duration-500"></div>

              {/* Card */}
              <div className="relative bg-card/50 backdrop-blur-sm border border-border rounded-2xl p-6 hover:border-primary/30 transition-all duration-300 h-full">
                {/* Quote icon */}
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                  <Quote className="w-5 h-5 text-primary" />
                </div>

                {/* Stars */}
                <div className="flex gap-1 mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-4 h-4 fill-primary text-primary" />
                  ))}
                </div>

                {/* Content */}
                <p className="text-sm text-foreground mb-4 leading-relaxed">
                  "{testimonial.content}"
                </p>

                {/* Author */}
                <div className="border-t border-border pt-4">
                  <p className="font-semibold text-sm">{testimonial.name}</p>
                  <p className="text-xs text-muted-foreground">{testimonial.role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
