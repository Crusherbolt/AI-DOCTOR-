'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useRouter } from 'next/router';

export default function AboutPage() {
  const router = useRouter();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [prediction, setPrediction] = useState<string | null>(null);
  const [confidence, setConfidence] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleNavigate = (e: React.MouseEvent<HTMLAnchorElement>, path: string) => {
    e.preventDefault();
    router.push(path);
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Reset states
    setSelectedFile(file);
    setPrediction(null);
    setConfidence(null);
    setError(null);
    setIsLoading(true);

    try {
        // Create FormData
        const formData = new FormData();
        formData.append('file', file);

        console.log('Sending request to server...');
        
        // Updated endpoint URL to match backend
        const response = await fetch('http://localhost:8501/predict', {
            method: 'POST',
            body: formData,
        });

        console.log('Response status:', response.status);
        
        const data = await response.json();
        console.log('Response data:', data);

        if (!response.ok) {
            throw new Error(data.detail?.message || 'Failed to process image');
        }

        if (data.status === 'success') {
            setPrediction(data.predicted_label);
            setConfidence(data.confidence);
        } else {
            throw new Error(data.message || 'Prediction failed');
        }
    } catch (error) {
        console.error('Error details:', error);
        setError(error instanceof Error ? error.message : 'Failed to process image. Please try again.');
    } finally {
        setIsLoading(false);
    }
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
              onClick={(e) => handleNavigate(e, "/playground")}
            >
              DOCTOR'S ROOM
            </a>
            <a 
              href="/"
              className="hover:text-cyan-400 transition-colors"
              onClick={(e) => handleNavigate(e, "/")}
            >
              Home
            </a>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold mb-6">Sinus Detection System</h2>
          <p className="text-gray-300 text-lg max-w-2xl mx-auto">
            Our advanced AI system can analyze your sinus condition through image processing.
            Upload a clear image of your face for analysis.
          </p>
        </motion.div>

        <div className="max-w-2xl mx-auto">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-gray-800/50 rounded-xl p-8 backdrop-blur-sm"
          >
            <div className="mb-8">
              <div className="w-32 h-32 mx-auto mb-4 rounded-full bg-gray-700/50 flex items-center justify-center">
                {selectedFile ? (
                  <img
                    src={URL.createObjectURL(selectedFile)}
                    alt="Preview"
                    className="w-full h-full object-cover rounded-full"
                  />
                ) : (
                  <svg 
                    className="w-16 h-16 text-cyan-400"
                    fill="none"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                  </svg>
                )}
              </div>
              
              <label className="block text-center">
                <span className="bg-cyan-500 hover:bg-cyan-600 px-6 py-3 rounded-lg cursor-pointer inline-block transition-colors">
                  {selectedFile ? 'Change Image' : 'Upload Image'}
                  <input
                    type="file"
                    className="hidden"
                    accept="image/*"
                    onChange={handleFileUpload}
                  />
                </span>
              </label>
            </div>

            {error && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-red-400 text-center mb-4"
              >
                {error}
              </motion.div>
            )}

            {isLoading && (
              <div className="text-center text-cyan-400">
                <div className="animate-spin w-8 h-8 border-4 border-current border-t-transparent rounded-full mx-auto mb-2"></div>
                Processing...
              </div>
            )}

            {selectedFile && !isLoading && (
              <div className="mt-6">
                <img
                  src={URL.createObjectURL(selectedFile)}
                  alt="Uploaded"
                  className="max-w-full h-auto max-h-64 mx-auto rounded-lg"
                />
              </div>
            )}

            {prediction && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="mt-6 text-center"
              >
                <div className={`text-xl font-bold mb-2 ${
                  prediction === 'unhealthy' ? 'text-red-400' : 'text-green-400'
                }`}>
                  {prediction === 'unhealthy' ? 'Potential Sinus Detected' : 'No Sinus Detected'}
                </div>
                {confidence && (
                  <div className="text-gray-300">
                    Confidence: {(confidence * 100).toFixed(2)}%
                  </div>
                )}
              </motion.div>
            )}
          </motion.div>
        </div>
      </main>
    </div>
  );
}