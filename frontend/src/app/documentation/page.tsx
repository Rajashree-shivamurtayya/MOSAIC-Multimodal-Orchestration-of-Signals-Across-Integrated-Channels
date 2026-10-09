"use client"

import React, { useState } from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  BookOpen, 
  Cpu, 
  Heart, 
  Mic, 
  Camera, 
  Layers, 
  ShieldCheck, 
  AlertTriangle, 
  CheckCircle2, 
  Activity, 
  Server, 
  FileText, 
  Database, 
  ArrowRight, 
  Terminal, 
  Info, 
  ChevronRight, 
  Zap, 
  Lock,
  Network
} from 'lucide-react'

export default function DocumentationPage() {
  const [activeSection, setActiveSection] = useState('overview')

  const scrollToSection = (id: string) => {
    setActiveSection(id)
    const element = document.getElementById(id)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }

  const sections = [
    { id: 'overview', title: '1. Project Overview' },
    { id: 'architecture', title: '2. System Architecture' },
    { id: 'hardware', title: '3. Hardware Setup (ESP32-C3 & MAX30102)' },
    { id: 'physio-pipeline', title: '4. Physiological Data Pipeline' },
    { id: 'audio-pipeline', title: '5. Audio Modality Pipeline' },
    { id: 'vision-pipeline', title: '6. Vision Modality Pipeline' },
    { id: 'late-fusion', title: '7. Late Fusion Engine' },
    { id: 'backend-api', title: '8. Backend API Reference' },
    { id: 'live-monitoring', title: '9. Live Monitoring & Telemetry' },
    { id: 'session-result', title: '10. Session Result Flow' },
    { id: 'offline-analytics', title: '11. Offline Analytics & Provenance' },
    { id: 'model-evaluation', title: '12. Verified Model Metrics' },
    { id: 'limitations', title: '13. System Limitations' },
    { id: 'disclaimer', title: '14. Scientific Disclaimer' },
  ]

  return (
    <div className="space-y-8 animate-fade-in-up pb-16 max-w-7xl mx-auto px-4 sm:px-6">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Badge variant="outline" className="text-cyan-400 border-cyan-500/30 text-xs">
              MOSAIC v1.0.0
            </Badge>
            <Badge variant="outline" className="text-slate-400 border-slate-700 text-xs">
              TECHNICAL SPECIFICATION
            </Badge>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white flex items-center gap-3">
            <BookOpen className="h-8 w-8 text-cyan-400" />
            System Documentation
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Architecture, hardware integration, multimodal pipelines, and empirical verification standards
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link href="/live">
            <Button variant="outline" size="sm" className="gap-1.5 text-xs border-slate-700 hover:bg-slate-800">
              <Activity className="h-3.5 w-3.5 text-emerald-400" /> Live System
            </Button>
          </Link>
          <Link href="/analytics">
            <Button variant="outline" size="sm" className="gap-1.5 text-xs border-slate-700 hover:bg-slate-800">
              <Layers className="h-3.5 w-3.5 text-cyan-400" /> Model Analytics
            </Button>
          </Link>
        </div>
      </div>

      {/* Mandatory Scientific Disclaimer Banner */}
      <div className="p-4 bg-amber-950/20 border border-amber-500/40 rounded-xl flex items-start gap-3.5 text-amber-200/90 text-xs leading-relaxed shadow-sm">
        <AlertTriangle className="h-5 w-5 text-amber-400 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold uppercase tracking-wider text-amber-300 block mb-0.5">
            Scientific Research Protocol Notice
          </span>
          <p>
            MOSAIC is a research prototype for experimental multimodal pattern classification. 
            It is not a medical diagnostic system or a definitive lie detector. 
            All classifications represent experimental statistical inferences based on physiological and behavioral cues under controlled research conditions.
          </p>
        </div>
      </div>

      {/* Layout Grid: Sticky Sidebar Nav + Content */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 items-start">
        {/* Sticky Table of Contents (Desktop) */}
        <div className="hidden lg:block lg:col-span-1 sticky top-6 space-y-2 bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-1.5">
            <FileText className="h-3.5 w-3.5 text-cyan-400" />
            Table of Contents
          </div>
          <nav className="space-y-1">
            {sections.map((sec) => (
              <button
                key={sec.id}
                onClick={() => scrollToSection(sec.id)}
                className={`w-full text-left px-2.5 py-1.5 rounded text-xs transition-colors block truncate ${
                  activeSection === sec.id
                    ? 'bg-cyan-500/20 text-cyan-300 font-semibold border-l-2 border-cyan-400 pl-2'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
                }`}
              >
                {sec.title}
              </button>
            ))}
          </nav>
        </div>

        {/* Main Content Area */}
        <div className="lg:col-span-3 space-y-10">

          {/* SECTION 1: PROJECT OVERVIEW */}
          <section id="overview" className="space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
              <span className="h-2 w-2 rounded-full bg-cyan-400"></span>
              <h2 className="text-xl font-bold text-white tracking-wide">1. Project Overview</h2>
            </div>
            <Card className="glass-panel border-slate-800">
              <CardContent className="pt-6 space-y-4 text-sm text-slate-300 leading-relaxed">
                <p>
                  <strong>MOSAIC</strong> (<em>Multimodal Orchestration of Signals Across Integrated Channels</em>) is an advanced 
                  experimental platform designed to evaluate synchronized physiological, acoustic, and computer vision signals 
                  for multimodal deception analysis.
                </p>
                <p>
                  Deception in human subjects triggers complex autonomic nervous system (ANS) reactions alongside subtle micro-behavioral 
                  and acoustic shifts. Traditional single-channel systems (such as standalone cardiovascular monitors or speech analyzers) 
                  suffer from high false-positive rates due to confounding emotional states (stress, surprise, apprehension). 
                  MOSAIC addresses this limitation by fusing three independent sensor modalities into a unified decision-level late fusion model:
                </p>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
                  <div className="p-3.5 bg-slate-900/80 rounded-lg border border-slate-800">
                    <div className="flex items-center gap-2 text-rose-400 font-semibold text-xs mb-1.5">
                      <Heart className="h-4 w-4" /> 1. Physiology
                    </div>
                    <p className="text-xs text-slate-400">
                      Optical photoplethysmography (PPG) from an ESP32-C3 &amp; MAX30102 sensor tracking systolic heart rate, pulse rate variability (HRV), and optical AC/DC pulsatile ratios.
                    </p>
                  </div>

                  <div className="p-3.5 bg-slate-900/80 rounded-lg border border-slate-800">
                    <div className="flex items-center gap-2 text-amber-400 font-semibold text-xs mb-1.5">
                      <Mic className="h-4 w-4" /> 2. Audio Acoustics
                    </div>
                    <p className="text-xs text-slate-400">
                      Real-time microphone capture extracting 13 MFCC spectral coefficients, zero-crossing rate (ZCR), and acoustic energy distribution.
                    </p>
                  </div>

                  <div className="p-3.5 bg-slate-900/80 rounded-lg border border-slate-800">
                    <div className="flex items-center gap-2 text-cyan-400 font-semibold text-xs mb-1.5">
                      <Camera className="h-4 w-4" /> 3. Computer Vision
                    </div>
                    <p className="text-xs text-slate-400">
                      Facial landmark tracking via webcam monitoring blink frequency, gaze deviation standard deviations, head pose velocity (yaw/pitch), and eyebrow tension.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </section>

          {/* SECTION 2: SYSTEM ARCHITECTURE */}
          <section id="architecture" className="space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
              <span className="h-2 w-2 rounded-full bg-cyan-400"></span>
              <h2 className="text-xl font-bold text-white tracking-wide">2. System Architecture</h2>
            </div>
            <Card className="glass-panel border-slate-800">
              <CardContent className="pt-6 space-y-4 text-sm text-slate-300">
                <p>
                  MOSAIC uses a decoupled, event-driven client-server architecture designed for high temporal fidelity and resilience against partial sensor disconnection.
                </p>

                {/* ASCII Architecture Diagram */}
                <div className="p-4 bg-black/60 rounded-xl border border-slate-800 font-mono text-[11px] leading-relaxed overflow-x-auto text-slate-300">
                  <pre>{`┌─────────────────────────────────────────────────────────────────────────────────┐
│                              MOSAIC ARCHITECTURE                                │
└─────────────────────────────────────────────────────────────────────────────────┘
 [HARDWARE LAYER]
   MAX30102 PPG Sensor ────(I2C @ 100Hz)────► ESP32-C3 Microcontroller
                                                    │ (USB Serial COM3 @ 115200)
                                                    ▼
 [DATA INGESTION & STORAGE]            backend/test_max30102.py (Background Listener)
                                                    │
                                                    ▼
                                           backend/mosaic_ppg.csv
                                                    │
 [BACKEND INFERENCE ENGINE (FastAPI)]               ▼
   Microphone Audio  ──► /api/predict ──► Feature Extraction (PPG / Audio / Vision)
   Webcam Vision     ──► (Port 8000)                │
                                                    ▼
                                           Trained Scikit-Learn Pipelines
                                           ├─ physiology_pipeline.joblib (42 feats)
                                           ├─ audio_pipeline.joblib      (83 feats)
                                           └─ vision_pipeline.joblib     (120 feats)
                                                    │
                                                    ▼
                                           Late Fusion Engine (Logistic Regression)
                                           └─ fusion_model.joblib [p_phys, p_aud, p_vis]
                                                    │
 [FRONTEND OPERATOR CONSOLE]                        ▼
   Next.js 16 Dashboard (Port 3000) ◄─── JSON Result Object & Telemetry Streams
   ├─ /live (Real-time Waveform, Heart Rate, Modality Cards, Session Controls)
   ├─ /session/[id]/result (Immutable Trial Audit & Feature Inspection)
   └─ /analytics (Verified Offline 5-Fold Cross-Validation Metrics)`}</pre>
                </div>

                <div className="space-y-2 pt-2">
                  <h4 className="font-semibold text-white text-xs uppercase tracking-wider">Key Architectural Invariants:</h4>
                  <ul className="list-disc list-inside text-xs text-slate-400 space-y-1.5 ml-2">
                    <li><strong className="text-slate-200">Strict Non-Blocking Asynchrony:</strong> Hardware serial polling runs independently of HTTP inference endpoints.</li>
                    <li><strong className="text-slate-200">Zero Synthetic Prior Substitution:</strong> If audio or vision is not actively streaming, the fusion engine returns <code>null</code> predictions rather than inventing default 0.5 priors.</li>
                    <li><strong className="text-slate-200">Deterministic Late Fusion:</strong> Late fusion is performed strictly at the decision level using output probabilities, ensuring unimodal explainability.</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </section>

          {/* SECTION 3: HARDWARE SETUP */}
          <section id="hardware" className="space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
              <span className="h-2 w-2 rounded-full bg-cyan-400"></span>
              <h2 className="text-xl font-bold text-white tracking-wide">3. Hardware Setup (ESP32-C3 &amp; MAX30102)</h2>
            </div>
            <Card className="glass-panel border-slate-800">
              <CardContent className="pt-6 space-y-4 text-sm text-slate-300">
                <p>
                  The physical sensing subsystem captures live cardiovascular pulse dynamics directly from human subjects.
                </p>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 bg-slate-900/60 rounded-lg border border-slate-800 space-y-2">
                    <div className="flex items-center gap-2 text-white font-semibold text-xs uppercase">
                      <Cpu className="h-4 w-4 text-cyan-400" /> ESP32-C3 Microcontroller
                    </div>
                    <ul className="text-xs text-slate-400 space-y-1 font-mono">
                      <li>&bull; Architecture: 32-bit RISC-V single-core @ 160MHz</li>
                      <li>&bull; USB CDC Serial: 115,200 baud</li>
                      <li>&bull; Operating Voltage: 3.3V DC</li>
                      <li>&bull; Host Connection: USB-C port (recognized as COM3 on Windows)</li>
                    </ul>
                  </div>

                  <div className="p-4 bg-slate-900/60 rounded-lg border border-slate-800 space-y-2">
                    <div className="flex items-center gap-2 text-white font-semibold text-xs uppercase">
                      <Heart className="h-4 w-4 text-rose-400" /> MAX30102 Pulse Oximeter Sensor
                    </div>
                    <ul className="text-xs text-slate-400 space-y-1 font-mono">
                      <li>&bull; Optical Channels: Red (660nm) &amp; Infrared (880nm)</li>
                      <li>&bull; Communication: I2C (Address 0x57)</li>
                      <li>&bull; Sampling Rate: 100 Hz</li>
                      <li>&bull; ADC Resolution: 18-bit internal converter</li>
                    </ul>
                  </div>
                </div>

                {/* Pinout Table */}
                <div className="space-y-1.5 pt-2">
                  <h4 className="font-semibold text-white text-xs uppercase tracking-wider">I2C Pinout Interconnect:</h4>
                  <div className="overflow-x-auto">
                    <table className="w-full text-xs text-left border border-slate-800 rounded-lg overflow-hidden">
                      <thead className="bg-slate-900 text-slate-400 font-mono">
                        <tr>
                          <th className="p-2.5 border-b border-slate-800">MAX30102 Sensor Pin</th>
                          <th className="p-2.5 border-b border-slate-800">ESP32-C3 Pin</th>
                          <th className="p-2.5 border-b border-slate-800">Description</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/60 font-mono text-slate-300">
                        <tr>
                          <td className="p-2.5 font-bold text-white">VIN / VCC</td>
                          <td className="p-2.5 text-cyan-400">3V3</td>
                          <td className="p-2.5 text-slate-400">Regulated 3.3V power supply</td>
                        </tr>
                        <tr>
                          <td className="p-2.5 font-bold text-white">GND</td>
                          <td className="p-2.5 text-cyan-400">GND</td>
                          <td className="p-2.5 text-slate-400">Common system ground</td>
                        </tr>
                        <tr>
                          <td className="p-2.5 font-bold text-white">SDA</td>
                          <td className="p-2.5 text-cyan-400">GPIO 8</td>
                          <td className="p-2.5 text-slate-400">I2C Serial Data (Hardware I2C)</td>
                        </tr>
                        <tr>
                          <td className="p-2.5 font-bold text-white">SCL</td>
                          <td className="p-2.5 text-cyan-400">GPIO 9</td>
                          <td className="p-2.5 text-slate-400">I2C Serial Clock (Hardware I2C)</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                <div className="p-3 bg-slate-900/80 rounded border border-slate-800 text-xs font-mono text-slate-400">
                  <span className="text-emerald-400 font-bold">Serial Stream Format: </span>
                  <code>timestamp_ms,ir_raw,red_raw\n</code> (e.g. <code>12450,148200,121400</code>).
                </div>
              </CardContent>
            </Card>
          </section>

          {/* SECTION 4: PHYSIOLOGICAL DATA PIPELINE */}
          <section id="physio-pipeline" className="space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
              <span className="h-2 w-2 rounded-full bg-cyan-400"></span>
              <h2 className="text-xl font-bold text-white tracking-wide">4. Physiological Data Pipeline</h2>
            </div>
            <Card className="glass-panel border-slate-800">
              <CardContent className="pt-6 space-y-4 text-sm text-slate-300">
                <p>
                  The physiological stream travels through a rigorous multi-stage digital signal processing pipeline before being evaluated by the trained machine learning pipeline:
                </p>

                {/* Pipeline Steps */}
                <div className="space-y-3 font-mono text-xs">
                  <div className="flex items-start gap-3 p-3 bg-slate-900/80 rounded border border-slate-800">
                    <span className="bg-rose-500/20 text-rose-300 px-2 py-0.5 rounded font-bold">Step 1</span>
                    <div>
                      <strong className="text-white block font-sans text-xs">Sensor Acquisition &amp; Buffering</strong>
                      <span>Continuous sampling of raw IR/Red counts at 100 Hz. Background script <code>test_max30102.py</code> logs to <code>mosaic_ppg.csv</code>.</span>
                    </div>
                  </div>

                  <div className="flex items-start gap-3 p-3 bg-slate-900/80 rounded border border-slate-800">
                    <span className="bg-cyan-500/20 text-cyan-300 px-2 py-0.5 rounded font-bold">Step 2</span>
                    <div>
                      <strong className="text-white block font-sans text-xs">Windowing &amp; Quality Filtering</strong>
                      <span>A sliding tail window (default 600 samples = 6.0 seconds) is extracted by <code>backend/ml/feature_extraction.py</code>. Verifies contact threshold (IR &gt; 10,000 counts) and sample stability (&ge; 50 samples).</span>
                    </div>
                  </div>

                  <div className="flex items-start gap-3 p-3 bg-slate-900/80 rounded border border-slate-800">
                    <span className="bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-bold">Step 3</span>
                    <div>
                      <strong className="text-white block font-sans text-xs">Systolic Peak Detection &amp; HRV Extraction</strong>
                      <span>Uses <code>scipy.signal.find_peaks</code> with distance constraint &ge; 40 samples (max 150 BPM) and prominence filtering. Computes Heart Rate (BPM), SDNN, and RMSSD.</span>
                    </div>
                  </div>

                  <div className="flex items-start gap-3 p-3 bg-slate-900/80 rounded border border-slate-800">
                    <span className="bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded font-bold">Step 4</span>
                    <div>
                      <strong className="text-white block font-sans text-xs">Pipeline Inference (physiology_pipeline.joblib)</strong>
                      <span>Constructs a 42-feature vector matching <code>model_features.json</code>. Transforms features via Median Imputer &amp; Standard Scaler, then predicts deception probability <code>p_phys</code>.</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </section>

          {/* SECTION 5: AUDIO PIPELINE */}
          <section id="audio-pipeline" className="space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
              <span className="h-2 w-2 rounded-full bg-cyan-400"></span>
              <h2 className="text-xl font-bold text-white tracking-wide">5. Audio Modality Pipeline</h2>
            </div>
            <Card className="glass-panel border-slate-800">
              <CardContent className="pt-6 space-y-4 text-sm text-slate-300">
                <p>
                  Acoustic prosody analysis operates on participant vocalizations captured via Web Audio API and analyzed in the backend:
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
                  <div className="p-3.5 bg-slate-900/60 rounded border border-slate-800 space-y-1.5">
                    <div className="text-amber-400 font-bold uppercase">Extracted Features (83 Total)</div>
                    <ul className="text-slate-400 space-y-1">
                      <li>&bull; 13 MFCC Coefficients (mean, std, delta, delta-delta)</li>
                      <li>&bull; Zero-Crossing Rate (ZCR mean &amp; variance)</li>
                      <li>&bull; Root-Mean-Square Energy (RMS energy mean &amp; std)</li>
                      <li>&bull; Spectral Centroid, Spread, &amp; Roll-off (85%)</li>
                      <li>&bull; Pitch (F0) fundamental frequency deviation</li>
                    </ul>
                  </div>

                  <div className="p-3.5 bg-slate-900/60 rounded border border-slate-800 space-y-1.5">
                    <div className="text-cyan-400 font-bold uppercase">Voice Activity Detection (VAD) Gate</div>
                    <ul className="text-slate-400 space-y-1">
                      <li>&bull; Energy threshold check (mean RMS energy &gt; 0.015)</li>
                      <li>&bull; Silent trials flagged via <code>is_silent = true</code></li>
                      <li>&bull; Inactive audio sets <code>audio_available = 0</code></li>
                      <li>&bull; Model: <code>audio_pipeline.joblib</code></li>
                      <li>&bull; Output: Audio deception probability <code>p_aud</code></li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
          </section>

          {/* SECTION 6: VISION PIPELINE */}
          <section id="vision-pipeline" className="space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
              <span className="h-2 w-2 rounded-full bg-cyan-400"></span>
              <h2 className="text-xl font-bold text-white tracking-wide">6. Vision Modality Pipeline</h2>
            </div>
            <Card className="glass-panel border-slate-800">
              <CardContent className="pt-6 space-y-4 text-sm text-slate-300">
                <p>
                  Visual behavioral analysis tracks involuntary facial micro-dynamics, blink frequencies, and gaze patterns using MediaPipe Face Landmarker:
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
                  <div className="p-3.5 bg-slate-900/60 rounded border border-slate-800 space-y-1.5">
                    <div className="text-cyan-400 font-bold uppercase">Extracted Features (121 Total)</div>
                    <ul className="text-slate-400 space-y-1">
                      <li>&bull; Blink dynamics: rate per minute, count, duration</li>
                      <li>&bull; Gaze deviation: mean and std in X and Y axes</li>
                      <li>&bull; Head Pose: yaw, pitch, roll, and angular delta velocity</li>
                      <li>&bull; Eyebrow movement: eyebrow-to-eye euclidean delta</li>
                      <li>&bull; Lip corner depression &amp; asymmetry metrics</li>
                    </ul>
                  </div>

                  <div className="p-3.5 bg-slate-900/60 rounded border border-slate-800 space-y-1.5">
                    <div className="text-rose-400 font-bold uppercase">Face Detection &amp; Quality Gate</div>
                    <ul className="text-slate-400 space-y-1">
                      <li>&bull; Requires active face landmark mesh (468 points)</li>
                      <li>&bull; If face lost: <code>face_detected = 0</code>, <code>video_available = 0</code></li>
                      <li>&bull; Gracefully invalidates vision channel when subject leaves frame</li>
                      <li>&bull; Model: <code>vision_pipeline.joblib</code></li>
                      <li>&bull; Output: Vision deception probability <code>p_vis</code></li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
          </section>

          {/* SECTION 7: LATE FUSION ENGINE */}
          <section id="late-fusion" className="space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
              <span className="h-2 w-2 rounded-full bg-cyan-400"></span>
              <h2 className="text-xl font-bold text-white tracking-wide">7. Late Fusion Engine</h2>
            </div>
            <Card className="glass-panel border-slate-800">
              <CardContent className="pt-6 space-y-4 text-sm text-slate-300">
                <p>
                  Decision-level late fusion combines the scalar probability outputs of all three unimodal classifiers into a trained meta-classifier:
                </p>

                <div className="p-4 bg-slate-900/80 rounded-xl border border-slate-800 space-y-3 font-mono text-xs">
                  <div className="text-cyan-300 font-bold uppercase tracking-wider">Late Fusion Execution Protocol:</div>
                  <div className="p-2.5 bg-black/50 rounded border border-slate-800 text-slate-300">
                    Input Vector = <code>[p_physiology, p_audio, p_vision]</code> (Shape: 1 &times; 3)
                  </div>
                  <p className="text-slate-400 leading-relaxed">
                    Evaluated by <code>fusion_model.joblib</code> (Scikit-Learn Logistic Regression).
                  </p>
                  <div className="border-t border-slate-800 pt-2 text-amber-300">
                    <strong>STRICT INVARIANT:</strong> Late fusion is performed <strong>IF AND ONLY IF</strong>:
                    <div className="mt-1 pl-4 text-slate-300">
                      <code>p_phys != null AND p_aud != null AND p_vis != null</code>
                    </div>
                  </div>
                  <p className="text-slate-400">
                    If ANY modality is absent or inactive:
                  </p>
                  <ul className="list-disc list-inside text-slate-400 pl-4 space-y-0.5">
                    <li><code>prediction = null</code></li>
                    <li><code>fusion_probability = null</code></li>
                    <li><code>confidence = null</code></li>
                    <li><code>fusion_status = "awaiting_active_modalities"</code></li>
                  </ul>
                  <p className="text-rose-400 font-bold">
                    Arbitrary 0.5 default priors are NEVER substituted for missing channels.
                  </p>
                </div>

                <div className="space-y-1.5 pt-1">
                  <h4 className="font-semibold text-white text-xs uppercase tracking-wider">Classification Rules:</h4>
                  <ul className="list-disc list-inside text-xs text-slate-400 space-y-1 font-mono">
                    <li><code>P(Deceptive) &gt;= 0.50</code> &rarr; Experimental Classification: <span className="text-rose-400 font-bold">DECEPTIVE</span></li>
                    <li><code>P(Deceptive) &lt; 0.50</code> &rarr; Experimental Classification: <span className="text-emerald-400 font-bold">TRUTHFUL</span></li>
                    <li><code>Confidence Score = |P(Deceptive) - 0.50| &times; 2.0</code> (Ranges from 0.0% to 100.0%)</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </section>

          {/* SECTION 8: BACKEND API REFERENCE */}
          <section id="backend-api" className="space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
              <span className="h-2 w-2 rounded-full bg-cyan-400"></span>
              <h2 className="text-xl font-bold text-white tracking-wide">8. Backend API Reference</h2>
            </div>
            <Card className="glass-panel border-slate-800">
              <CardContent className="pt-6 space-y-4 text-sm text-slate-300">
                <p>
                  The MOSAIC FastAPI backend (<code>http://127.0.0.1:8000</code>) exposes standardized REST endpoints for hardware inspection, live telemetry, and experimental session control:
                </p>

                <div className="overflow-x-auto">
                  <table className="w-full text-xs text-left border border-slate-800 rounded-lg overflow-hidden">
                    <thead className="bg-slate-900 text-slate-400 font-mono">
                      <tr>
                        <th className="p-2.5 border-b border-slate-800">Method</th>
                        <th className="p-2.5 border-b border-slate-800">Endpoint</th>
                        <th className="p-2.5 border-b border-slate-800">Purpose / Description</th>
                        <th className="p-2.5 border-b border-slate-800">Response Highlights</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/60 font-mono text-slate-300">
                      <tr>
                        <td className="p-2.5 font-bold text-emerald-400">GET</td>
                        <td className="p-2.5 text-white">/health</td>
                        <td className="p-2.5 text-slate-400 font-sans">Liveness and service health verification</td>
                        <td className="p-2.5 text-cyan-300">{`{"status": "healthy"}`}</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-bold text-emerald-400">GET</td>
                        <td className="p-2.5 text-white">/docs</td>
                        <td className="p-2.5 text-slate-400 font-sans">Interactive Swagger / OpenAPI UI</td>
                        <td className="p-2.5 text-cyan-300">HTML API Documentation</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-bold text-emerald-400">GET</td>
                        <td className="p-2.5 text-white">/api/physio/status</td>
                        <td className="p-2.5 text-slate-400 font-sans">Hardware connection &amp; CSV sample count</td>
                        <td className="p-2.5 text-cyan-300">port, samples, connected, streaming</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-bold text-emerald-400">GET</td>
                        <td className="p-2.5 text-white">/api/physiological/latest</td>
                        <td className="p-2.5 text-slate-400 font-sans">Extracted PPG features &amp; heart rate</td>
                        <td className="p-2.5 text-cyan-300">heart_rate, signal_quality, rmssd, sdnn</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-bold text-emerald-400">GET</td>
                        <td className="p-2.5 text-white">/api/physiological/waveform</td>
                        <td className="p-2.5 text-slate-400 font-sans">Raw optical IR/Red waveform window</td>
                        <td className="p-2.5 text-cyan-300">Array of [timestamp, ir, red]</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-bold text-emerald-400">GET</td>
                        <td className="p-2.5 text-white">/api/audio/status</td>
                        <td className="p-2.5 text-slate-400 font-sans">Acoustic state &amp; audio probability</td>
                        <td className="p-2.5 text-cyan-300">available, probability, quality</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-bold text-emerald-400">GET</td>
                        <td className="p-2.5 text-white">/api/vision/status</td>
                        <td className="p-2.5 text-slate-400 font-sans">Face mesh state &amp; vision probability</td>
                        <td className="p-2.5 text-cyan-300">available, probability, quality</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-bold text-cyan-400">POST</td>
                        <td className="p-2.5 text-white">/api/predict</td>
                        <td className="p-2.5 text-slate-400 font-sans">Execute real-time late fusion inference</td>
                        <td className="p-2.5 text-cyan-300">prediction, fusion_probability, confidence</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-bold text-cyan-400">POST</td>
                        <td className="p-2.5 text-white">/api/session/start</td>
                        <td className="p-2.5 text-slate-400 font-sans">Initialize a new experimental trial session</td>
                        <td className="p-2.5 text-cyan-300">{`{"session_id": "SES_...", "status": "success"}`}</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-bold text-emerald-400">GET</td>
                        <td className="p-2.5 text-white">/api/session/&#123;id&#125;/result</td>
                        <td className="p-2.5 text-slate-400 font-sans">Query immutable trial result record</td>
                        <td className="p-2.5 text-cyan-300">Complete multi-channel result object</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-bold text-emerald-400">GET</td>
                        <td className="p-2.5 text-white">/api/session/latest/result</td>
                        <td className="p-2.5 text-slate-400 font-sans">Query latest active or finalized trial</td>
                        <td className="p-2.5 text-cyan-300">Latest session record</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-bold text-cyan-400">POST</td>
                        <td className="p-2.5 text-white">/api/session/&#123;id&#125;/complete</td>
                        <td className="p-2.5 text-slate-400 font-sans">Lock trial results &amp; finalize duration</td>
                        <td className="p-2.5 text-cyan-300">Finalized result object</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-bold text-cyan-400">POST</td>
                        <td className="p-2.5 text-white">/api/session/reset</td>
                        <td className="p-2.5 text-slate-400 font-sans">Reset session state &amp; active buffers</td>
                        <td className="p-2.5 text-cyan-300">{`{"status": "success"}`}</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-bold text-emerald-400">GET</td>
                        <td className="p-2.5 text-white">/api/analytics</td>
                        <td className="p-2.5 text-slate-400 font-sans">Verified offline cross-validation metrics</td>
                        <td className="p-2.5 text-cyan-300">data_provenance, metrics, latency_benchmark</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          </section>

          {/* SECTION 9: LIVE MONITORING */}
          <section id="live-monitoring" className="space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
              <span className="h-2 w-2 rounded-full bg-cyan-400"></span>
              <h2 className="text-xl font-bold text-white tracking-wide">9. Live Monitoring &amp; Telemetry</h2>
            </div>
            <Card className="glass-panel border-slate-800">
              <CardContent className="pt-6 space-y-4 text-sm text-slate-300">
                <p>
                  The <Link href="/live" className="text-cyan-400 underline font-semibold">Live Monitoring page (/live)</Link> serves 
                  as the primary operator console during live participant testing:
                </p>
                <div className="space-y-2 text-xs font-mono">
                  <div className="p-3 bg-slate-900/60 rounded border border-slate-800">
                    <strong className="text-white block font-sans text-xs mb-1">Optical Waveform Display</strong>
                    <span className="text-slate-400">
                      Real-time interactive chart toggling between raw optical PPG windows (infrared channel) and calculated heart rate (BPM) trendlines with baseline reference.
                    </span>
                  </div>
                  <div className="p-3 bg-slate-900/60 rounded border border-slate-800">
                    <strong className="text-white block font-sans text-xs mb-1">Modality Status Indicators</strong>
                    <span className="text-slate-400">
                      Live badges for Physiology (MAX30102 COM port, sample count, SNR), Audio (RMS energy, silence detection), and Vision (face mesh lock, blink rate).
                    </span>
                  </div>
                  <div className="p-3 bg-slate-900/60 rounded border border-slate-800">
                    <strong className="text-white block font-sans text-xs mb-1">Source Labeling Distinction</strong>
                    <span className="text-slate-400">
                      Explicitly displays <span className="text-cyan-400 font-bold">LIVE SENSOR DATA</span> when MAX30102 hardware is streaming from COM3, or <span className="text-amber-400 font-bold">DEMO DATA</span> during software-only validation mode.
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </section>

          {/* SECTION 10: SESSION RESULT FLOW */}
          <section id="session-result" className="space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
              <span className="h-2 w-2 rounded-full bg-cyan-400"></span>
              <h2 className="text-xl font-bold text-white tracking-wide">10. Session Result Flow</h2>
            </div>
            <Card className="glass-panel border-slate-800">
              <CardContent className="pt-6 space-y-4 text-sm text-slate-300">
                <p>
                  When the operator concludes an experimental trial by clicking <strong>End Session</strong> on <code>/live</code>:
                </p>
                <ol className="list-decimal list-inside text-xs text-slate-400 space-y-2 font-mono">
                  <li>The frontend issues a <code>POST /api/session/&#123;id&#125;/complete</code> request.</li>
                  <li>The backend locks the session timestamps, calculates the trial duration, and computes the final late fusion decision.</li>
                  <li>The operator is automatically redirected to the dedicated audit page: <code>/session/&#123;sessionId&#125;/result</code>.</li>
                  <li>
                    The audit page displays the final experimental classification alongside the exact feature vectors:
                    hardware port, sample counts, heart rate BPM, audio MFCC energy, and vision gaze/blink statistics.
                  </li>
                  <li>All result data is permanent and queryable via <code>GET /api/session/&#123;sessionId&#125;/result</code>.</li>
                </ol>
              </CardContent>
            </Card>
          </section>

          {/* SECTION 11: OFFLINE ANALYTICS & PROVENANCE */}
          <section id="offline-analytics" className="space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
              <span className="h-2 w-2 rounded-full bg-cyan-400"></span>
              <h2 className="text-xl font-bold text-white tracking-wide">11. Offline Analytics &amp; Provenance</h2>
            </div>
            <Card className="glass-panel border-slate-800">
              <CardContent className="pt-6 space-y-4 text-sm text-slate-300">
                <p>
                  The <Link href="/analytics" className="text-cyan-400 underline font-semibold">Analytics page (/analytics)</Link> is 
                  dedicated strictly to <strong>OFFLINE MODEL EVALUATION</strong> of the trained pipeline artifacts on the research dataset:
                </p>
                <div className="p-3 bg-amber-950/20 border border-amber-500/30 rounded text-xs text-amber-200/90 leading-relaxed">
                  <strong>Source Labeling Standard:</strong> The footer displays <code>Source: OFFLINE MODEL EVALUATION</code> (amber). 
                  It does NOT claim to represent live participant data. Top banner displays <code>SIMULATED DATASET RESULTS</code>.
                </div>
                <p className="text-xs text-slate-400">
                  Evaluation was conducted using <strong>5-Fold StratifiedGroupKFold</strong> across 300 participants and 3,000 trials, 
                  guaranteeing zero cross-participant data leakage between training and testing folds.
                </p>
              </CardContent>
            </Card>
          </section>

          {/* SECTION 12: VERIFIED MODEL METRICS */}
          <section id="model-evaluation" className="space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
              <span className="h-2 w-2 rounded-full bg-cyan-400"></span>
              <h2 className="text-xl font-bold text-white tracking-wide">12. Verified Model Metrics (Data Provenance)</h2>
            </div>
            <Card className="glass-panel border-slate-800">
              <CardContent className="pt-6 space-y-5 text-sm text-slate-300">
                <p>
                  All metrics displayed on MOSAIC are traceable directly to documented cross-validation artifacts in <code>Dataset/results/model_comparison.csv</code> and empirical benchmark scripts. 
                  Unverified synthetic placeholders have been purged.
                </p>

                {/* Metrics Table */}
                <div className="overflow-x-auto">
                  <table className="w-full text-xs text-left border border-slate-800 rounded-lg overflow-hidden">
                    <thead className="bg-slate-900 text-slate-400 font-mono">
                      <tr>
                        <th className="p-2.5 border-b border-slate-800">Pipeline / Model</th>
                        <th className="p-2.5 border-b border-slate-800">Architecture</th>
                        <th className="p-2.5 border-b border-slate-800">Features</th>
                        <th className="p-2.5 border-b border-slate-800">Accuracy</th>
                        <th className="p-2.5 border-b border-slate-800">F1-Score</th>
                        <th className="p-2.5 border-b border-slate-800">ROC-AUC</th>
                        <th className="p-2.5 border-b border-slate-800">Verification State</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/60 font-mono text-slate-300">
                      <tr>
                        <td className="p-2.5 font-bold text-rose-400">Physiology Unimodal</td>
                        <td className="p-2.5 text-slate-400">Median Imputer + Scaler + LogisticRegression</td>
                        <td className="p-2.5 text-white">42</td>
                        <td className="p-2.5 text-emerald-400 font-bold">62.0%</td>
                        <td className="p-2.5 text-white">61.9%</td>
                        <td className="p-2.5 text-cyan-300">0.663</td>
                        <td className="p-2.5 text-emerald-400 font-bold">VERIFIED</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-bold text-amber-400">Audio Unimodal</td>
                        <td className="p-2.5 text-slate-400">Median Imputer + Scaler + LogisticRegression</td>
                        <td className="p-2.5 text-white">83</td>
                        <td className="p-2.5 text-emerald-400 font-bold">69.1%</td>
                        <td className="p-2.5 text-white">68.3%</td>
                        <td className="p-2.5 text-cyan-300">0.756</td>
                        <td className="p-2.5 text-emerald-400 font-bold">VERIFIED</td>
                      </tr>
                      <tr>
                        <td className="p-2.5 font-bold text-cyan-400">Vision Unimodal</td>
                        <td className="p-2.5 text-slate-400">Median Imputer + Scaler + LogisticRegression</td>
                        <td className="p-2.5 text-white">121</td>
                        <td className="p-2.5 text-emerald-400 font-bold">68.8%</td>
                        <td className="p-2.5 text-white">69.1%</td>
                        <td className="p-2.5 text-cyan-300">0.749</td>
                        <td className="p-2.5 text-emerald-400 font-bold">VERIFIED</td>
                      </tr>
                      <tr className="bg-cyan-950/20 font-bold">
                        <td className="p-2.5 text-cyan-300">Late Fusion (Decision Level)</td>
                        <td className="p-2.5 text-slate-300">LogisticRegression on [p_phys, p_aud, p_vis]</td>
                        <td className="p-2.5 text-white">3</td>
                        <td className="p-2.5 text-cyan-300 text-sm">73.4%</td>
                        <td className="p-2.5 text-cyan-300 text-sm">73.3%</td>
                        <td className="p-2.5 text-cyan-300 text-sm">0.801</td>
                        <td className="p-2.5 text-emerald-400">VERIFIED</td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                {/* Latency Benchmark Details */}
                <div className="p-4 bg-slate-900/60 rounded-xl border border-slate-800 space-y-2">
                  <div className="flex items-center gap-2 text-cyan-400 font-semibold text-xs uppercase tracking-wider">
                    <Zap className="h-4 w-4 text-amber-400" /> Empirical Latency Benchmark (90 Measured Runs on Host CPU)
                  </div>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono pt-1">
                    <div className="p-2.5 bg-black/40 rounded border border-slate-800">
                      <span className="text-slate-500 block text-[10px]">Pure Pipeline Mean</span>
                      <span className="text-white text-base font-bold">49.6 ms</span>
                    </div>
                    <div className="p-2.5 bg-black/40 rounded border border-slate-800">
                      <span className="text-slate-500 block text-[10px]">Pure Pipeline Median</span>
                      <span className="text-white text-base font-bold">47.9 ms</span>
                    </div>
                    <div className="p-2.5 bg-black/40 rounded border border-slate-800">
                      <span className="text-slate-500 block text-[10px]">End-to-End API Mean</span>
                      <span className="text-cyan-400 text-base font-bold">86.2 ms</span>
                    </div>
                    <div className="p-2.5 bg-black/40 rounded border border-slate-800">
                      <span className="text-slate-500 block text-[10px]">End-to-End API Median</span>
                      <span className="text-cyan-400 text-base font-bold">81.8 ms</span>
                    </div>
                  </div>
                  <p className="text-[11px] text-slate-500 italic mt-1 font-mono">
                    Measured using high-resolution time.perf_counter() across 100 iterations (10 warmup discarded).
                  </p>
                </div>

                {/* 3,000-Trial Confusion Matrix Summary */}
                <div className="p-4 bg-slate-900/60 rounded-xl border border-slate-800 space-y-2">
                  <div className="text-white font-semibold text-xs uppercase tracking-wider">
                    5-Fold Cross-Validation Confusion Matrix (Late Fusion, 3,000 Trials):
                  </div>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-mono">
                    <div className="p-2 bg-emerald-500/10 border border-emerald-500/30 rounded text-center">
                      <span className="block text-slate-400 text-[10px]">True Negative (TN)</span>
                      <span className="text-emerald-300 font-bold text-sm">1,108</span>
                    </div>
                    <div className="p-2 bg-rose-500/10 border border-rose-500/30 rounded text-center">
                      <span className="block text-slate-400 text-[10px]">False Positive (FP)</span>
                      <span className="text-rose-300 font-bold text-sm">392</span>
                    </div>
                    <div className="p-2 bg-rose-500/10 border border-rose-500/30 rounded text-center">
                      <span className="block text-slate-400 text-[10px]">False Negative (FN)</span>
                      <span className="text-rose-300 font-bold text-sm">405</span>
                    </div>
                    <div className="p-2 bg-emerald-500/10 border border-emerald-500/30 rounded text-center">
                      <span className="block text-slate-400 text-[10px]">True Positive (TP)</span>
                      <span className="text-emerald-300 font-bold text-sm">1,095</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </section>

          {/* SECTION 13: SYSTEM LIMITATIONS */}
          <section id="limitations" className="space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
              <span className="h-2 w-2 rounded-full bg-cyan-400"></span>
              <h2 className="text-xl font-bold text-white tracking-wide">13. System Limitations</h2>
            </div>
            <Card className="glass-panel border-slate-800">
              <CardContent className="pt-6 space-y-3 text-sm text-slate-300">
                <ul className="space-y-2.5 text-xs text-slate-400">
                  <li className="flex items-start gap-2">
                    <ChevronRight className="h-4 w-4 text-cyan-400 shrink-0 mt-0.5" />
                    <span><strong className="text-slate-200">Optical Motion Artifacts:</strong> The MAX30102 PPG sensor requires steady finger contact. Gross hand movements introduce optical decoupling that temporarily degrades peak detection accuracy.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <ChevronRight className="h-4 w-4 text-cyan-400 shrink-0 mt-0.5" />
                    <span><strong className="text-slate-200">Acoustic Environmental Noise:</strong> Vocal feature extraction operates best in quiet environments (&lt; 45 dB ambient noise). Loud external interference can skew MFCC spectral centroid estimates.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <ChevronRight className="h-4 w-4 text-cyan-400 shrink-0 mt-0.5" />
                    <span><strong className="text-slate-200">Visual Occlusion &amp; Head Rotation:</strong> MediaPipe facial mesh tracking degrades if the head is rotated beyond 45 degrees or if lighting is insufficient.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <ChevronRight className="h-4 w-4 text-cyan-400 shrink-0 mt-0.5" />
                    <span><strong className="text-slate-200">Controlled Research Distribution:</strong> The trained model distributions reflect controlled lab protocol experiments. Performance may vary under uncalibrated open-world conditions.</span>
                  </li>
                </ul>
              </CardContent>
            </Card>
          </section>

          {/* SECTION 14: SCIENTIFIC DISCLAIMER */}
          <section id="disclaimer" className="space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
              <span className="h-2 w-2 rounded-full bg-amber-400"></span>
              <h2 className="text-xl font-bold text-amber-300 tracking-wide">14. Scientific &amp; Legal Disclaimer</h2>
            </div>
            <Card className="glass-panel border-amber-500/30 bg-amber-950/10">
              <CardContent className="pt-6 space-y-3 text-xs text-amber-200/90 leading-relaxed">
                <p className="text-sm font-bold text-amber-300">
                  &ldquo;MOSAIC is a research prototype for experimental multimodal pattern classification. It is not a medical diagnostic system or a definitive lie detector.&rdquo;
                </p>
                <p>
                  Psychophysiological markers of deception (such as autonomic tachycardia, galvanic skin reactions, vocal pitch shift, and gaze aversion) are correlates of cognitive load, stress, and autonomic sympathetic arousal. They are not direct physiological markers of truth or falsehood.
                </p>
                <p>
                  MOSAIC classifications should never be used as sole or definitive evidence in judicial, forensic, medical, employment, or life-critical decisions. The system is developed exclusively for academic, engineering, and scientific research in signal processing and human-computer interaction.
                </p>
              </CardContent>
            </Card>
          </section>

        </div>
      </div>
    </div>
  )
}
