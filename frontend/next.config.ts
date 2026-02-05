import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Ensure proper output for Vercel
  output: undefined, // Let Vercel auto-detect (default behavior)

  // Disable trailing slashes for cleaner URLs
  trailingSlash: false,

  // Enable React strict mode
  reactStrictMode: true,
};

export default nextConfig;
