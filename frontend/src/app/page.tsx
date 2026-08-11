import React from 'react';
import DashboardData from '@/components/DashboardData';

export default function Home() {
  return (
    <main className="min-h-screen bg-[#0b0c10] bg-gradient-modern flex flex-col items-center justify-center p-6 relative overflow-hidden">
      
      {/* Abstract Background Orbs */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-[var(--color-brand-primary)] rounded-full blur-[120px] opacity-20 pointer-events-none"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-[var(--color-brand-secondary)] rounded-full blur-[120px] opacity-20 pointer-events-none"></div>
      
      <div className="z-10 w-full max-w-5xl flex flex-col items-center animate-fade-in-up">
        
        {/* Header Section */}
        <div className="text-center mb-12">
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-4">
            Welcome to <span className="text-gradient">MOSAIC</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto leading-relaxed">
            Multi-Model Orchestration of Signals Across Integrated Channels. 
            A multimodal platform for deception-analysis research.
          </p>
        </div>

        {/* Dashboard Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full">
          
          {/* Card 1: Researcher */}
          <div className="glass p-8 rounded-2xl flex flex-col items-start transition-all hover:scale-[1.02] hover:border-[var(--color-brand-primary)] hover:shadow-[0_0_20px_rgba(0,210,255,0.15)] cursor-pointer">
            <div className="w-12 h-12 rounded-lg bg-[var(--color-brand-primary)]/20 text-[var(--color-brand-primary)] flex items-center justify-center mb-6">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6Z" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold mb-2">Researcher View</h2>
            <p className="text-sm text-gray-400 mb-6 flex-grow">
              Design experiments, manage datasets, and evaluate model performance across multiple modalities.
            </p>
            <button className="w-full py-3 px-4 rounded-lg bg-white/5 hover:bg-white/10 text-white font-medium border border-white/10 transition-colors">
              Access Workspace
            </button>
          </div>

          {/* Card 2: Operator */}
          <div className="glass p-8 rounded-2xl flex flex-col items-start transition-all hover:scale-[1.02] hover:border-[var(--color-brand-secondary)] hover:shadow-[0_0_20px_rgba(58,123,213,0.15)] cursor-pointer">
            <div className="w-12 h-12 rounded-lg bg-[var(--color-brand-secondary)]/20 text-[var(--color-brand-secondary)] flex items-center justify-center mb-6">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold mb-2">Operator Console</h2>
            <p className="text-sm text-gray-400 mb-6 flex-grow">
              Run active trials, monitor physiological sensors, and oversee data acquisition pipelines in real-time.
            </p>
            <button className="w-full py-3 px-4 rounded-lg bg-white/5 hover:bg-white/10 text-white font-medium border border-white/10 transition-colors">
              Start Session
            </button>
          </div>

          {/* Card 3: Live Monitor */}
          <div className="glass p-8 rounded-2xl flex flex-col items-start transition-all hover:scale-[1.02] hover:border-white/30 hover:shadow-[0_0_20px_rgba(255,255,255,0.1)] cursor-pointer">
            <div className="w-12 h-12 rounded-lg bg-white/10 text-white flex items-center justify-center mb-6">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 13.5 12 17.25 19.5 9.75M12 21a9.0 9.0 0 1 1 0-18 9 9 0 0 1 0 18Z" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold mb-2">Device Status</h2>
            <p className="text-sm text-gray-400 mb-6 flex-grow">
              Verify ESP32-C3 hardware integration, camera feed, and audio device synchronization.
            </p>
            <button className="w-full py-3 px-4 rounded-lg bg-white/5 hover:bg-white/10 text-white font-medium border border-white/10 transition-colors">
              Run Diagnostics
            </button>
          </div>
        </div>

        {/* Live Backend Data Integration */}
        <DashboardData />

      </div>
    </main>
  );
}
