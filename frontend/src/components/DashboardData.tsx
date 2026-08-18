"use client";

import React, { useState, useEffect } from 'react';

interface Trial {
  id: string | number;
  participant: string;
  status: string;
  prediction?: string;
  confidence?: number;
}

export default function DashboardData() {
  const [trials, setTrials] = useState<Trial[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch data from FastAPI backend
    fetch('http://localhost:8000/api/trials')
      .then(res => res.json())
      .then(data => {
        setTrials(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch from backend", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="w-full mt-12 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
      <h3 className="text-2xl font-bold mb-6 border-b border-white/10 pb-2">Recent Trials (Live from Backend)</h3>
      
      {loading ? (
        <div className="flex justify-center p-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[var(--color-brand-primary)]"></div>
        </div>
      ) : trials.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {trials.map(trial => (
            <div key={trial.id} className="glass p-5 rounded-xl border border-white/5 flex justify-between items-center">
              <div>
                <p className="font-semibold text-lg text-white">{trial.participant}</p>
                <p className={`text-sm ${trial.status === 'completed' ? 'text-green-400' : 'text-yellow-400'}`}>
                  Status: {trial.status}
                </p>
              </div>
              
              {trial.prediction && trial.confidence !== undefined && (
                <div className="text-right">
                  <p className="font-bold text-[var(--color-brand-primary)] uppercase text-sm tracking-wider">
                    {trial.prediction}
                  </p>
                  <p className="text-xs text-gray-400">
                    Conf: {(trial.confidence * 100).toFixed(1)}%
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="glass p-6 rounded-xl text-center text-gray-400">
          Backend connection failed or no trials available. Ensure FastAPI is running on port 8000.
        </div>
      )}
    </div>
  );
}
