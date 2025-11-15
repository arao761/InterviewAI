'use client';

import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="border-t border-border bg-card/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          <div>
            <h3 className="font-bold text-lg mb-4 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              InterviewAI
            </h3>
            <p className="text-muted-foreground text-sm">
              Master your interviews with AI-powered coaching.
            </p>
          </div>
          {[
            { title: 'Product', links: [{ name: 'Features', href: '/#features' }, { name: 'Pricing', href: '/pricing#pricing-plans' }, { name: 'Security', href: '#' }] },
            { title: 'Company', links: [{ name: 'About', href: '/about#team' }, { name: 'Blog', href: '#' }, { name: 'Careers', href: '#' }] },
            { title: 'Legal', links: [{ name: 'Privacy', href: '#' }, { name: 'Terms', href: '#' }, { name: 'Contact', href: '#' }] },
          ].map((col, i) => (
            <div key={i}>
              <h4 className="font-semibold mb-4 text-foreground">{col.title}</h4>
              <ul className="space-y-2">
                {col.links.map((link, j) => (
                  <li key={j}>
                    <Link href={link.href} className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                      {link.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="border-t border-border pt-8 flex justify-between items-center text-sm text-muted-foreground">
          <p>&copy; 2025 InterviewAI. All rights reserved.</p>
          <div className="flex gap-4">
            <a href="#" className="hover:text-foreground transition-colors">Twitter</a>
            <a href="#" className="hover:text-foreground transition-colors">LinkedIn</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
