import type { NextConfig } from "next";
const nextConfig: NextConfig = {
  distDir: ".next-final",
  images: { remotePatterns: [{ protocol: "https", hostname: "images.unsplash.com" }] },
  async rewrites() { return [{ source: "/backend/:path*", destination: `${process.env.BACKEND_URL || "http://127.0.0.1:5000"}/:path*` }]; },
};
export default nextConfig;
