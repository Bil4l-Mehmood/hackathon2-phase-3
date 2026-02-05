/** @type {import('next').NextConfig} */
const nextConfig = {
  // Allow API calls to localhost backend
  async rewrites() {
    return [];
  },
};

export default nextConfig;
