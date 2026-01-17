/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for Docker
  output: 'standalone',
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  async headers() {
    return [
      {
        // Apply security headers to all routes
        source: '/:path*',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: [
              "default-src 'self'",
              // Allow scripts from self and inline (needed for Next.js hydration)
              "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
              // Allow styles from self, inline, and Google Fonts
              "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
              // Allow images from self, data URIs, and HTTPS sources (including LinkedIn)
              "img-src 'self' data: https: blob:",
              // Allow fonts from self, data URIs, and Google Fonts
              "font-src 'self' data: https://fonts.gstatic.com",
              // Allow connections to self and external APIs (backend, Microsoft Foundry, Azure Speech Services, etc.)
              "connect-src 'self' http://localhost:8000 https://*",
              // Prevent framing (clickjacking protection)
              "frame-ancestors 'none'",
              // Allow media from self and HTTPS
              "media-src 'self' https: blob:",
              // Base URI restrictions
              "base-uri 'self'",
              // Form action restrictions
              "form-action 'self'",
            ].join('; '),
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=()',
          },
        ],
      },
    ]
  },
}

export default nextConfig