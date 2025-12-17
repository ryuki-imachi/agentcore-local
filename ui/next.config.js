/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',

  // Exclude problematic packages from bundling
  serverExternalPackages: [
    'pino',
    'pino-pretty',
    'thread-stream',
  ],

  // Enable Turbopack (Next.js 16 default)
  turbopack: {},
};

module.exports = nextConfig;
