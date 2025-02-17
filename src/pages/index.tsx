'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { useRouter } from 'next/router';  // Note: using next/router instead of next/navigation


export default function LandingPage() {
  const router = useRouter();

  const handleNavigate = (e: React.MouseEvent<HTMLAnchorElement>, path: string) => {
    e.preventDefault();
    router.push(path);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white">
      <nav className="p-6">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Aerion</h1>
          <div className="space-x-6">
            <a 
              href="/playground" 
              className="hover:text-cyan-400 transition-colors"
              onClick={(e) => handleNavigate(e, '/playground')}
            >
              DOCTOR'S ROOM
            </a>
            <a 
              href="/about" 
              className="hover:text-cyan-400 transition-colors"
              onClick={(e) => handleNavigate(e, '/about')}
            >
              SINUS VERIFICATION
            </a>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-20">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-5xl font-bold mb-6">Welcome to Your Virtual AI Doctor</h2>
            <p className="text-gray-300 text-lg mb-8">
            Our cutting-edge platform uses advanced audio and video diagnostics to evaluate sinus and facial concerns. With fast, accurate prescriptions, we provide an affordable alternative to traditional care for patients in need.
            </p>
            <a 
              href="/playground"
              className="bg-cyan-500 hover:bg-cyan-600 text-white px-8 py-3 rounded-lg 
                       inline-block transition-colors font-bold"
              onClick={(e) => handleNavigate(e, '/playground')}
            >
              ENTER DOCTOR'S ROOM
            </a>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="relative h-[400px] rounded-lg overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 
                          animate-pulse rounded-lg border border-gray-700"></div>
          </motion.div>
        </div>
      </main>
    </div>
  );
}