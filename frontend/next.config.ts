import type { NextConfig } from "next";
import dotenv from "dotenv";

dotenv.config({ path: "../.env" });

const nextConfig: NextConfig = {
  reactStrictMode: true,
  env: {
    BACKEND_URL: process.env.BACKEND_URL,
    SECRET_KEY: process.env.SECRET_KEY,
  },
};

export default nextConfig;
