"use client"

import React, { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  Activity, 
  CheckCircle2, 
  Clock, 
  AlertTriangle, 
  Cpu, 
  Layers, 
  ArrowLeft, 
  Download, 
  RotateCcw, 
  Heart, 
  Mic, 
  Eye, 
  ShieldCheck, 
  ShieldAlert, 
  ArrowRight,
  Database,
  FileCode2,
  HelpCircle,
  Printer
} from 'lucide-react'

interface SessionResultData {
  session_id: string
  participant_id?: string
  status: string
  start_time: string | null
  end_time: string | null
  duration_seconds: number
  classification_type: string
  prediction: 'truthful' | 'deceptive' | null
  classification_label?: string
  fusion_probability: number | null
  confidence: number | null
  fusion_status: 'ready' | 'awaiting_active_modalities' | 'error' | 'unavailable'
  fusion_input_vector: (number | null)[]
  modalities_used: string[]
  modalities_missing: string[]
  physiology: {
    available: boolean
    sensor_source: string
    port: string
    connected: boolean
    sample_count: number
    heart_rate_bpm: number | null
    signal_quality: number | null
    signal_quality_status?: string
    temperature: string | null
    spo2: string | null
    hrv?: {
      sdnn: number | null
      rmssd: number | null
    } | null
    features_used?: {
      mean_ir?: number | null
      mean_red?: number | null
      ppg_peak_count?: number | null
      heart_rate_std?: number | null
    } | null
    probability: number | null
  }
  audio: {
    available: boolean
    capture_status: string
    feature_extraction_status: string
    probability: number | null
    quality: number | null
    features_used?: {
      mean_rms_energy?: number | null
      zcr_mean?: number | null
      mfcc_mean_0?: number | null
    } | null
  }
  vision: {
    available: boolean
    capture_status: string
    feature_extraction_status: string
    probability: number | null
    quality: number | null
    features_used?: {
      blink_rate?: number | null
      head_yaw_mean?: number | null
      eyebrow_delta_mean?: number | null
      face_detected?: number | null
    } | null
  }
  model_status: string
  traceability?: {
    physiology_pipeline: string
    audio_pipeline: string
    vision_pipeline: string
    fusion_model: string
    fusion_architecture: string
    flow_description?: string
  }
  disclaimer: string
}

export default function SessionResultPage() {
  const params = useParams()
  const router = useRouter()
  const sessionId = params?.sessionId as string || 'latest'

  const [data, setData] = useState<SessionResultData | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  useEffect(() => {
    let isMounted = true

    const fetchResult = async () => {
      try {
        setLoading(true)
        setError(null)
        const res = await fetch(`${API_BASE}/api/session/${sessionId}/result`)
        if (!res.ok) {
          throw new Error(`Failed to load session result (HTTP ${res.status})`)
        }
        const json: SessionResultData = await res.json()
        if (isMounted) {
          setData(json)
          setLoading(false)
        }
      } catch (err: unknown) {
        if (isMounted) {
          const msg = err instanceof Error ? err.message : 'Unknown error loading session'
          setError(msg)
          setLoading(false)
        }
      }
    }

    fetchResult()

    return () => {
      isMounted = false
    }
  }, [sessionId, API_BASE])

  const handleExportPDF = () => {
    if (typeof window !== 'undefined') {
      const originalTitle = document.title
      if (data?.session_id) {
        document.title = `MOSAIC_Session_${data.session_id}_Report`
      }
      window.print()
      setTimeout(() => {
        document.title = originalTitle
      }, 1000)
    }
  }

  if (loading) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center space-y-4">
        <div className="h-10 w-10 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin" />
        <p className="text-sm font-mono text-cyan-400">Loading experimental session result...</p>
        <p className="text-xs text-slate-500 font-mono">Querying {API_BASE}/api/session/{sessionId}/result</p>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center space-y-4 max-w-md mx-auto text-center">
        <AlertTriangle className="h-12 w-12 text-red-400" />
        <h2 className="text-lg font-bold text-white">Session Result Unavailable</h2>
        <p className="text-xs text-slate-400">{error || 'Session data could not be retrieved from the backend API.'}</p>
        <div className="flex gap-3 pt-2">
          <Button variant="outline" size="sm" onClick={() => router.push('/live')} className="gap-2">
            <ArrowLeft className="h-4 w-4" /> Back to Live Monitoring
          </Button>
          <Button variant="default" size="sm" onClick={() => window.location.reload()} className="gap-2">
            <RotateCcw className="h-4 w-4" /> Retry
          </Button>
        </div>
      </div>
    )
  }

  const isFusionReady = data.fusion_status === 'ready' && data.prediction !== null
  const isTruthful = data.prediction === 'truthful'
  const isDeceptive = data.prediction === 'deceptive'

  // Format duration into readable minutes and seconds
  const formatDuration = (seconds: number) => {
    if (seconds < 60) return `${seconds.toFixed(1)}s`
    const mins = Math.floor(seconds / 60)
    const secs = (seconds % 60).toFixed(0)
    return `${mins}m ${secs}s (${seconds.toFixed(1)}s)`
  }

  return (
    <div className="space-y-8 animate-fade-in-up pb-12 max-w-7xl mx-auto px-4 sm:px-6">
      {/* Top Header & Navigation */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono text-slate-400 mb-1">
            <span className="hover:text-cyan-400 cursor-pointer" onClick={() => router.push('/')}>Dashboard</span>
            <span>/</span>
            <span className="hover:text-cyan-400 cursor-pointer" onClick={() => router.push('/live')}>Live Experiment</span>
            <span>/</span>
            <span className="text-cyan-400 font-semibold">Final Session Result</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2.5">
            <Activity className="h-6 w-6 text-cyan-400" />
            MOSAIC Final Experimental Classification
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Multi-Model Orchestration of Signals Across Integrated Channels &mdash; Late Fusion Result
          </p>
        </div>

        <div className="flex items-center gap-2.5 flex-wrap print:hidden">
          <Button 
            variant="outline" 
            size="sm" 
            onClick={() => router.push('/live')}
            className="gap-2 border-slate-700 hover:border-slate-500 text-xs"
          >
            <ArrowLeft className="h-3.5 w-3.5" /> Back to Live
          </Button>
          <Button 
            variant="outline" 
            size="sm" 
            onClick={handleExportPDF}
            className="gap-2 border-slate-700 hover:border-cyan-500 text-xs text-cyan-300"
          >
            <Printer className="h-3.5 w-3.5" /> Export PDF
          </Button>
          <Button 
            size="sm" 
            onClick={() => router.push('/live')}
            className="gap-2 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-medium"
          >
            <RotateCcw className="h-3.5 w-3.5" /> New Session
          </Button>
        </div>
      </div>

      {/* SECTION F: FINAL LATE-FUSION RESULT (FEATURED HERO CARD) */}
      <Card className={`glass-panel border-2 overflow-hidden shadow-2xl ${
        isFusionReady 
          ? isTruthful 
            ? 'border-emerald-500/50 bg-gradient-to-b from-emerald-950/20 via-slate-900/60 to-slate-950 shadow-[0_0_30px_rgba(16,185,129,0.15)]' 
            : 'border-rose-500/50 bg-gradient-to-b from-rose-950/20 via-slate-900/60 to-slate-950 shadow-[0_0_30px_rgba(244,63,94,0.15)]'
          : 'border-amber-500/40 bg-gradient-to-b from-amber-950/20 via-slate-900/60 to-slate-950 shadow-[0_0_20px_rgba(245,158,11,0.1)]'
      }`}>
        <CardHeader className="border-b border-slate-800/80 pb-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div className="flex items-center gap-2.5">
              {isFusionReady ? (
                isTruthful ? (
                  <ShieldCheck className="h-6 w-6 text-emerald-400" />
                ) : (
                  <ShieldAlert className="h-6 w-6 text-rose-400" />
                )
              ) : (
                <Clock className="h-6 w-6 text-amber-400 animate-pulse" />
              )}
              <div>
                <CardTitle className="text-base tracking-wide uppercase font-bold text-white">
                  {isFusionReady ? 'Experimental Multimodal Classification Result' : 'Multimodal Late Fusion: Incomplete Modality Set'}
                </CardTitle>
                <CardDescription className="text-xs text-slate-400">
                  Model: <code className="text-cyan-300 font-mono">Dataset/models/fusion_model.joblib</code> &bull; Architecture: Decision-Level Late Fusion
                </CardDescription>
              </div>
            </div>

            <Badge variant={isFusionReady ? (isTruthful ? 'success' : 'error') : 'warning'} className="text-xs px-3 py-1 font-mono tracking-wider uppercase self-start sm:self-auto">
              {isFusionReady ? (data.prediction?.toUpperCase()) : 'AWAITING ACTIVE MODALITIES'}
            </Badge>
          </div>
        </CardHeader>

        <CardContent className="pt-6 space-y-6">
          {isFusionReady ? (
            <div className="space-y-6">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 p-6 rounded-xl bg-black/40 border border-slate-800/80">
                <div className="space-y-1.5">
                  <p className="text-[11px] uppercase font-bold tracking-widest text-slate-400">
                    Experimental Classification
                  </p>
                  <p className={`text-4xl sm:text-5xl font-black tracking-tight uppercase ${
                    isTruthful ? 'text-emerald-400 drop-shadow-[0_0_15px_rgba(52,211,153,0.3)]' : 'text-rose-400 drop-shadow-[0_0_15px_rgba(251,113,133,0.3)]'
                  }`}>
                    {data.prediction?.toUpperCase()}
                  </p>
                  <p className="text-xs text-slate-400 pt-1">
                    Pattern classified as <strong className="text-white capitalize">{data.prediction}</strong> by the trained multimodal Late Fusion model.
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-4 sm:gap-6 min-w-[280px]">
                  <div className="p-3.5 bg-slate-900/80 rounded-lg border border-slate-800 text-center">
                    <p className="text-[10px] uppercase font-semibold text-slate-400 tracking-wider">Fusion Probability</p>
                    <p className="text-2xl font-mono font-bold text-white mt-0.5">
                      {data.fusion_probability !== null ? data.fusion_probability.toFixed(4) : '--'}
                    </p>
                    <p className="text-[10px] text-slate-500 mt-0.5">Threshold: 0.500</p>
                  </div>

                  <div className="p-3.5 bg-slate-900/80 rounded-lg border border-slate-800 text-center">
                    <p className="text-[10px] uppercase font-semibold text-slate-400 tracking-wider">Confidence Metric</p>
                    <p className="text-2xl font-mono font-bold text-cyan-400 mt-0.5">
                      {data.confidence !== null ? `${(data.confidence * 100).toFixed(1)}%` : '--'}
                    </p>
                    <p className="text-[10px] text-slate-500 mt-0.5">|P - 0.5| &times; 2</p>
                  </div>
                </div>
              </div>

              {/* Modality Synchronization Checklist */}
              <div className="flex flex-wrap items-center justify-between gap-3 p-3.5 rounded-lg bg-emerald-950/20 border border-emerald-500/30 text-xs">
                <span className="font-semibold text-emerald-300 flex items-center gap-1.5 text-xs">
                  <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                  All 3 Modalities Synchronized in Late Fusion:
                </span>
                <div className="flex flex-wrap gap-2 text-xs font-mono">
                  <span className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 px-2.5 py-1 rounded flex items-center gap-1">
                    &bull; Physiology: <strong className="text-white ml-1">{data.physiology.probability?.toFixed(4)}</strong>
                  </span>
                  <span className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 px-2.5 py-1 rounded flex items-center gap-1">
                    &bull; Audio: <strong className="text-white ml-1">{data.audio.probability?.toFixed(4)}</strong>
                  </span>
                  <span className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 px-2.5 py-1 rounded flex items-center gap-1">
                    &bull; Vision: <strong className="text-white ml-1">{data.vision.probability?.toFixed(4)}</strong>
                  </span>
                </div>
              </div>
            </div>
          ) : (
            /* Missing Modality Scientific Integrity Notice */
            <div className="p-6 rounded-xl bg-amber-950/15 border border-amber-500/30 space-y-4">
              <div className="flex items-start gap-3">
                <AlertTriangle className="h-5 w-5 text-amber-400 shrink-0 mt-0.5" />
                <div className="space-y-1">
                  <h3 className="text-sm font-bold text-amber-300 uppercase tracking-wide">
                    Late Fusion Awaiting Active Modalities &mdash; No Synthetic Fallbacks
                  </h3>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    Genuine multimodal pattern classification requires concurrent valid probabilities from all three unimodal models.
                    Under MOSAIC scientific integrity rules, missing streams are <strong>never replaced with arbitrary 0.5 default priors</strong> or fabricated scores.
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1 text-xs">
                <div className="p-3 bg-black/40 rounded-lg border border-slate-800 space-y-1">
                  <p className="text-[10px] uppercase font-bold text-emerald-400">Available Modalities</p>
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {data.modalities_used.length > 0 ? (
                      data.modalities_used.map(m => (
                        <span key={m} className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 font-mono text-[11px] capitalize">
                          &bull; {m}
                        </span>
                      ))
                    ) : (
                      <span className="text-slate-500 italic">None</span>
                    )}
                  </div>
                </div>

                <div className="p-3 bg-black/40 rounded-lg border border-slate-800 space-y-1">
                  <p className="text-[10px] uppercase font-bold text-rose-400">Missing Modalities (Required for Late Fusion)</p>
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {data.modalities_missing.length > 0 ? (
                      data.modalities_missing.map(m => (
                        <span key={m} className="px-2 py-0.5 rounded bg-rose-500/10 text-rose-300 border border-rose-500/30 font-mono text-[11px] capitalize">
                          &bull; {m}
                        </span>
                      ))
                    ) : (
                      <span className="text-slate-500 italic">None</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Research Prototype Disclaimer */}
          <div className="pt-3 border-t border-slate-800/80 text-center">
            <p className="text-[10px] uppercase tracking-wider font-bold text-slate-400">
              Scientific Research Protocol Disclaimer
            </p>
            <p className="text-[11px] text-slate-400 mt-1 max-w-2xl mx-auto leading-relaxed">
              {data.disclaimer}
            </p>
          </div>
        </CardContent>
      </Card>

      {/* SECTION E: MODEL INPUTS (EXACT VALUES SENT TO LATE FUSION) */}
      <Card className="glass-panel border-slate-800">
        <CardHeader className="pb-3 border-b border-slate-800/80">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
              <Layers className="h-4 w-4" /> Section E: Model Inputs &amp; Late Fusion Vector
            </CardTitle>
            <Badge variant="outline" className="font-mono text-[10px] border-cyan-500/40 text-cyan-300">
              DIMENSION: 1 &times; 3
            </Badge>
          </div>
          <CardDescription className="text-xs text-slate-400">
            The exact 3-element unimodal deception probability vector evaluated by <code className="text-white font-mono">Dataset/models/fusion_model.joblib</code>.
          </CardDescription>
        </CardHeader>
        <CardContent className="pt-4 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {/* Physiology Probability */}
            <div className="p-3.5 rounded-lg bg-slate-900/60 border border-slate-800 space-y-1">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400 font-medium flex items-center gap-1.5">
                  <Heart className="h-3.5 w-3.5 text-rose-400" /> Physiology (p_phys)
                </span>
                <Badge variant={data.physiology.available ? "success" : "outline"} className="text-[9px]">
                  {data.physiology.available ? "ACTIVE" : "UNAVAILABLE"}
                </Badge>
              </div>
              <p className="text-xl font-mono font-bold text-white pt-1">
                {data.physiology.probability !== null && data.physiology.probability !== undefined 
                  ? data.physiology.probability.toFixed(4) 
                  : <span className="text-slate-500 text-sm">Unavailable</span>}
              </p>
              <p className="text-[10px] text-slate-500">Source: MAX30102 via COM3</p>
            </div>

            {/* Audio Probability */}
            <div className="p-3.5 rounded-lg bg-slate-900/60 border border-slate-800 space-y-1">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400 font-medium flex items-center gap-1.5">
                  <Mic className="h-3.5 w-3.5 text-amber-400" /> Audio (p_aud)
                </span>
                <Badge variant={data.audio.available ? "success" : "outline"} className="text-[9px]">
                  {data.audio.available ? "ACTIVE" : "UNAVAILABLE"}
                </Badge>
              </div>
              <p className="text-xl font-mono font-bold text-white pt-1">
                {data.audio.probability !== null && data.audio.probability !== undefined 
                  ? data.audio.probability.toFixed(4) 
                  : <span className="text-slate-500 text-sm">Unavailable</span>}
              </p>
              <p className="text-[10px] text-slate-500">Source: System Microphone</p>
            </div>

            {/* Vision Probability */}
            <div className="p-3.5 rounded-lg bg-slate-900/60 border border-slate-800 space-y-1">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400 font-medium flex items-center gap-1.5">
                  <Eye className="h-3.5 w-3.5 text-cyan-400" /> Vision (p_vis)
                </span>
                <Badge variant={data.vision.available ? "success" : "outline"} className="text-[9px]">
                  {data.vision.available ? "ACTIVE" : "UNAVAILABLE"}
                </Badge>
              </div>
              <p className="text-xl font-mono font-bold text-white pt-1">
                {data.vision.probability !== null && data.vision.probability !== undefined 
                  ? data.vision.probability.toFixed(4) 
                  : <span className="text-slate-500 text-sm">Unavailable</span>}
              </p>
              <p className="text-[10px] text-slate-500">Source: Host Webcam</p>
            </div>
          </div>

          {/* Raw Fusion Input Array Display */}
          <div className="p-3 bg-black/60 rounded-lg border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs font-mono">
            <span className="text-slate-400 font-semibold">Late Fusion Input Vector:</span>
            <div className="bg-slate-950 px-3 py-1.5 rounded border border-cyan-500/20 text-cyan-300 font-bold tracking-wider text-xs">
              [ {data.fusion_input_vector.map((val, idx) => (
                <span key={idx}>
                  {val !== null ? val.toFixed(4) : <span className="text-rose-400 font-normal">null</span>}
                  {idx < data.fusion_input_vector.length - 1 ? ', ' : ''}
                </span>
              ))} ]
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 2-COLUMN GRID: SECTION A (SUMMARY) & SECTION B (SENSOR TELEMETRY) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* SECTION A: SESSION SUMMARY */}
        <Card className="glass-panel border-slate-800">
          <CardHeader className="pb-3 border-b border-slate-800/80">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
                <Clock className="h-4 w-4 text-cyan-400" /> Section A: Session Summary
              </CardTitle>
              <Badge variant={data.status === 'completed' ? 'success' : 'outline'} className="text-[10px]">
                {data.status.toUpperCase()}
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="pt-4">
            <dl className="grid grid-cols-2 gap-4 text-xs">
              <div className="p-3 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <dt className="text-slate-500 font-medium">Session ID</dt>
                <dd className="text-white font-mono font-bold mt-1 text-sm">{data.session_id}</dd>
              </div>

              <div className="p-3 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <dt className="text-slate-500 font-medium">Participant ID</dt>
                <dd className="text-white font-mono font-bold mt-1 text-sm">{data.participant_id || 'P001'}</dd>
              </div>

              <div className="p-3 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <dt className="text-slate-500 font-medium">Start Time</dt>
                <dd className="text-white font-mono mt-1">{data.start_time || '--'}</dd>
              </div>

              <div className="p-3 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <dt className="text-slate-500 font-medium">End Time</dt>
                <dd className="text-white font-mono mt-1">{data.end_time || '--'}</dd>
              </div>

              <div className="col-span-2 p-3 bg-slate-900/50 rounded-lg border border-slate-800/80 flex items-center justify-between">
                <div>
                  <dt className="text-slate-500 font-medium">Total Duration</dt>
                  <dd className="text-cyan-400 font-mono font-bold mt-0.5 text-base">
                    {formatDuration(data.duration_seconds)}
                  </dd>
                </div>
                <Badge variant="outline" className="font-mono text-[10px] text-slate-400">
                  {data.duration_seconds.toFixed(1)}s elapsed
                </Badge>
              </div>
            </dl>
          </CardContent>
        </Card>

        {/* SECTION B: SENSOR DATA (MAX30102) */}
        <Card className="glass-panel border-slate-800">
          <CardHeader className="pb-3 border-b border-slate-800/80">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-bold uppercase tracking-wider text-rose-400 flex items-center gap-2">
                <Heart className="h-4 w-4" /> Section B: Real Physiological Sensor Data
              </CardTitle>
              <Badge variant={data.physiology.connected ? "success" : "error"} className="text-[10px]">
                {data.physiology.connected ? `CONNECTED (${data.physiology.port})` : "DISCONNECTED"}
              </Badge>
            </div>
            <CardDescription className="text-xs text-slate-400">
              Hardware: MAX30102 Optical PPG Sensor &bull; USB Serial COM Stream
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-4 space-y-3">
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Sensor Source</p>
                <p className="text-white font-mono font-bold mt-0.5">{data.physiology.sensor_source}</p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Serial COM Port</p>
                <p className="text-cyan-300 font-mono font-bold mt-0.5">{data.physiology.port}</p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Sample Count</p>
                <p className="text-white font-mono font-bold mt-0.5">{data.physiology.sample_count.toLocaleString()}</p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Heart Rate</p>
                <p className="text-emerald-400 font-mono font-bold mt-0.5 text-base">
                  {data.physiology.heart_rate_bpm ? `${data.physiology.heart_rate_bpm.toFixed(1)} BPM` : 'null'}
                </p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Signal Quality</p>
                <p className="text-white font-mono font-bold mt-0.5">
                  {data.physiology.signal_quality ? `${data.physiology.signal_quality.toFixed(1)}%` : 'null'}
                </p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">HRV (SDNN / RMSSD)</p>
                <p className="text-white font-mono font-bold mt-0.5 text-[11px]">
                  {data.physiology.hrv?.sdnn ? `${data.physiology.hrv.sdnn.toFixed(0)}ms / ${data.physiology.hrv.rmssd?.toFixed(0)}ms` : 'Unavailable'}
                </p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Temperature</p>
                <p className="text-slate-400 font-mono text-[10px] mt-0.5">{data.physiology.temperature}</p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">SpO2</p>
                <p className="text-slate-400 font-mono text-[10px] mt-0.5">{data.physiology.spo2}</p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Physiology Model</p>
                <p className="text-cyan-300 font-mono text-[10px] mt-0.5">physiology_pipeline</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* 2-COLUMN GRID: SECTION C (AUDIO) & SECTION D (VISION) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* SECTION C: AUDIO */}
        <Card className="glass-panel border-slate-800">
          <CardHeader className="pb-3 border-b border-slate-800/80">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-bold uppercase tracking-wider text-amber-400 flex items-center gap-2">
                <Mic className="h-4 w-4" /> Section C: Audio Modality Telemetry
              </CardTitle>
              <Badge variant={data.audio.available ? "success" : "outline"} className="text-[10px]">
                {data.audio.available ? "CAPTURED" : "UNAVAILABLE"}
              </Badge>
            </div>
            <CardDescription className="text-xs text-slate-400">
              Pipeline: <code className="text-white font-mono">Dataset/models/audio_pipeline.joblib</code> (83 acoustic features)
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-4 space-y-3">
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Capture Status</p>
                <p className="text-white font-mono font-bold mt-0.5 capitalize">{data.audio.capture_status}</p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Feature Extraction</p>
                <p className="text-white font-mono font-bold mt-0.5 capitalize">{data.audio.feature_extraction_status}</p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Audio Quality</p>
                <p className="text-white font-mono font-bold mt-0.5">
                  {data.audio.quality !== null ? `${(data.audio.quality * 100).toFixed(0)}%` : 'Unavailable'}
                </p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">RMS Energy</p>
                <p className="text-white font-mono mt-0.5">
                  {data.audio.features_used?.mean_rms_energy !== undefined && data.audio.features_used?.mean_rms_energy !== null 
                    ? data.audio.features_used.mean_rms_energy.toFixed(5) 
                    : 'Unavailable'}
                </p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Zero Crossing Rate</p>
                <p className="text-white font-mono mt-0.5">
                  {data.audio.features_used?.zcr_mean !== undefined && data.audio.features_used?.zcr_mean !== null 
                    ? data.audio.features_used.zcr_mean.toFixed(4) 
                    : 'Unavailable'}
                </p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Audio Probability</p>
                <p className="text-amber-400 font-mono font-bold mt-0.5 text-sm">
                  {data.audio.probability !== null ? data.audio.probability.toFixed(4) : 'Unavailable'}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* SECTION D: VISION */}
        <Card className="glass-panel border-slate-800">
          <CardHeader className="pb-3 border-b border-slate-800/80">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
                <Eye className="h-4 w-4" /> Section D: Vision Modality Telemetry
              </CardTitle>
              <Badge variant={data.vision.available ? "success" : "outline"} className="text-[10px]">
                {data.vision.available ? "CAPTURED" : "UNAVAILABLE"}
              </Badge>
            </div>
            <CardDescription className="text-xs text-slate-400">
              Pipeline: <code className="text-white font-mono">Dataset/models/vision_pipeline.joblib</code> (121 facial features)
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-4 space-y-3">
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Capture Status</p>
                <p className="text-white font-mono font-bold mt-0.5 capitalize">{data.vision.capture_status}</p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Feature Extraction</p>
                <p className="text-white font-mono font-bold mt-0.5 capitalize">{data.vision.feature_extraction_status}</p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Face Detected</p>
                <p className="text-white font-mono font-bold mt-0.5">
                  {data.vision.features_used?.face_detected === 1 ? 'Yes (1.0)' : 'No (0.0)'}
                </p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Blink Rate</p>
                <p className="text-white font-mono mt-0.5">
                  {data.vision.features_used?.blink_rate !== undefined && data.vision.features_used?.blink_rate !== null 
                    ? `${data.vision.features_used.blink_rate.toFixed(1)} bpm` 
                    : 'Unavailable'}
                </p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Head Yaw Mean</p>
                <p className="text-white font-mono mt-0.5">
                  {data.vision.features_used?.head_yaw_mean !== undefined && data.vision.features_used?.head_yaw_mean !== null 
                    ? `${data.vision.features_used.head_yaw_mean.toFixed(2)}°` 
                    : 'Unavailable'}
                </p>
              </div>

              <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80">
                <p className="text-[10px] text-slate-500 font-medium uppercase">Vision Probability</p>
                <p className="text-cyan-400 font-mono font-bold mt-0.5 text-sm">
                  {data.vision.probability !== null ? data.vision.probability.toFixed(4) : 'Unavailable'}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* SECTION G: TRACEABILITY ARCHITECTURE */}
      <Card className="glass-panel border-slate-800">
        <CardHeader className="pb-3 border-b border-slate-800/80">
          <CardTitle className="text-sm font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
            <Cpu className="h-4 w-4" /> Section G: Traceability &mdash; How This Result Was Produced
          </CardTitle>
          <CardDescription className="text-xs text-slate-400">
            End-to-end signal flow from physical hardware sensors and client capture streams to the trained Late Fusion model.
          </CardDescription>
        </CardHeader>
        <CardContent className="pt-4 space-y-4">
          {/* Visual Signal Flow Diagram */}
          <div className="p-4 bg-black/60 rounded-xl border border-slate-800 space-y-4 font-mono text-xs">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-center">
              {/* Channel 1 */}
              <div className="p-3 rounded-lg bg-slate-900/80 border border-rose-500/20 space-y-1">
                <div className="text-[10px] uppercase font-bold text-rose-400">1. Physical Sensor</div>
                <div className="font-bold text-white text-xs">MAX30102 via USB (COM3)</div>
                <ArrowRight className="h-3 w-3 text-slate-600 mx-auto my-1" />
                <div className="text-[11px] text-slate-400">42 Optical PPG Features</div>
                <ArrowRight className="h-3 w-3 text-slate-600 mx-auto my-1" />
                <div className="text-emerald-400 font-semibold">physiology_pipeline.joblib</div>
                <div className="pt-1 text-[11px] text-white">p_phys = {data.physiology.probability?.toFixed(4) || 'null'}</div>
              </div>

              {/* Channel 2 */}
              <div className="p-3 rounded-lg bg-slate-900/80 border border-amber-500/20 space-y-1">
                <div className="text-[10px] uppercase font-bold text-amber-400">2. Audio Stream</div>
                <div className="font-bold text-white text-xs">Microphone Capture</div>
                <ArrowRight className="h-3 w-3 text-slate-600 mx-auto my-1" />
                <div className="text-[11px] text-slate-400">83 MFCC &amp; Spectral Features</div>
                <ArrowRight className="h-3 w-3 text-slate-600 mx-auto my-1" />
                <div className="text-amber-400 font-semibold">audio_pipeline.joblib</div>
                <div className="pt-1 text-[11px] text-white">p_aud = {data.audio.probability?.toFixed(4) || 'null'}</div>
              </div>

              {/* Channel 3 */}
              <div className="p-3 rounded-lg bg-slate-900/80 border border-cyan-500/20 space-y-1">
                <div className="text-[10px] uppercase font-bold text-cyan-400">3. Video Stream</div>
                <div className="font-bold text-white text-xs">Webcam Face Detection</div>
                <ArrowRight className="h-3 w-3 text-slate-600 mx-auto my-1" />
                <div className="text-[11px] text-slate-400">121 Facial &amp; Landmark Features</div>
                <ArrowRight className="h-3 w-3 text-slate-600 mx-auto my-1" />
                <div className="text-cyan-400 font-semibold">vision_pipeline.joblib</div>
                <div className="pt-1 text-[11px] text-white">p_vis = {data.vision.probability?.toFixed(4) || 'null'}</div>
              </div>
            </div>

            {/* Convergence to Late Fusion */}
            <div className="p-3.5 bg-slate-950 rounded-lg border border-cyan-500/30 text-center space-y-1.5">
              <div className="text-[10px] uppercase tracking-wider text-slate-400 font-semibold">
                Decision Vector Convergence
              </div>
              <div className="text-cyan-300 font-bold text-sm">
                X_fusion = [ p_phys, p_aud, p_vis ] &rarr; fusion_model.joblib &rarr; P(deceptive)
              </div>
              <p className="text-[11px] text-slate-400 max-w-xl mx-auto pt-1 font-sans">
                Trained decision forest evaluates the joint probability vector to produce the final binary classification 
                (<span className="text-white font-semibold">TRUTHFUL</span> / <span className="text-white font-semibold">DECEPTIVE</span>) 
                and calibrated confidence margin.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
