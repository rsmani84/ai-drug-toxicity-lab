import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // RDKit.js contains optional Node.js filesystem references in its bundle.
  // The student-facing app runs RDKit in the browser, where Node's fs module
  // is unavailable and must not be bundled.
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve = config.resolve ?? {};
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
      };
    }
    return config;
  },
};

export default nextConfig;
