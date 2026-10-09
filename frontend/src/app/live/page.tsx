"use client"

import React, { useState, useEffect, useRef, useCallback, useSyncExternalStore } from 'react'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { useSystem } from '@/context/SystemContext'
import { cn } from '@/lib/utils'
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer 
} from 'recharts'
import { Eye, Mic, Heart, Camera, Video, MicOff, VideoOff, Activity, CheckCircle2, Clock, AlertTriangle, Play, Square, RotateCcw } from 'lucide-react'

interface VisionFeatures {
  face_detected?: number
  video_available?: number
  blink_rate: number
  blink_count: number
  gaze_x_mean: number
  gaze_x_std: number
  gaze_y_mean: number
  gaze_y_std: number
  head_yaw_mean: number
  head_yaw_std: number
  head_yaw_delta: number
  head_pitch_mean: number
  head_pitch_std: number
  head_pitch_delta: number
  eyebrow_delta_mean: number
  eyebrow_delta_max: number
  eyebrow_delta_std: number
  frame_count: number
}

interface AudioFeatures {
  mfcc_mean: number[]
  zcr_mean: number
  mean_rms_energy?: number
  is_silent?: boolean
  audio_available?: number
}

interface PhysioFeatures {
  mean_hr: number | null
  heart_rate: number | null
  estimated_heart_rate_bpm?: number | null
  hr_std: number | null
  rmssd: number | null
  sdnn: number | null
  mean_ir: number | null
  mean_red: number | null
  mean_temperature: number | null
  temperature_available?: boolean
  mean_spo2: number | null
  spo2: number | null
  spo2_available: boolean
  sample_count: number
  stable_sample_count: number
  sampling_rate: number
  sampling_rate_hz?: number
  duration_seconds: number
  num_beats: number
  signal_quality: number
  signal_quality_percent: number
  signal_quality_status: string
  hr_valid: boolean
  source: string
}

interface ModalityScores {
  audio: number | null
  vision: number | null
  physiological: number | null
}

interface PredictionResult {
  session_id?: string
  trial_id?: number
  prediction: string | null
  classification_label?: string
  confidence: number | null
  fusion_probability: number | null
  fusion_status?: string
  classification_type?: string
  model_status: string
  disclaimer?: string
  modalities_used?: string[]
  modalities_missing?: string[]
  quality_summary?: {
    physiological?: number | null
    audio?: number | null
    vision?: number | null
  }
  modality_scores?: ModalityScores
  availability?: {
    audio: boolean
    vision: boolean
    physiological: boolean
  }
  features_used?: {
    heart_rate_bpm: number | null
    signal_quality_percent: number | null
    sample_count: number
  }
}

interface WaveformPoint {
  time: number
  timestamp_ms: number
  ir: number
  red: number
}

interface PhysioStatus {
  connected: boolean
  port: string
  sensor: string
  samples: number
  last_timestamp_ms: number | null
  csv_present: boolean
  file_size_bytes: number
  streaming?: boolean
  status: string
  message?: string
}

interface SimulatedMetrics {
  gazeX: string
  blinkRate: string
  headYaw: string
  eyebrowDelta: string
  zcr: string
  mfcc: string
  waveformHeights: number[]
}

const INITIAL_SIMULATED_METRICS: SimulatedMetrics = {
  gazeX: '1.42',
  blinkRate: '16',
  headYaw: '3.4',
  eyebrowDelta: '0.021',
  zcr: '0.082',
  mfcc: '-22.4',
  waveformHeights: [
    25, 40, 65, 30, 80, 45, 60, 20, 75, 90, 
    55, 35, 70, 85, 40, 30, 65, 50, 75, 60, 
    45, 80, 35, 70, 55, 40, 65, 30, 50, 20
  ],
}

const emptySubscribe = () => () => {}

export default function LiveMonitoring() {
  const { 
    isSimulationMode, 
    cameraStatus, 
    microphoneStatus, 
    isCameraActive, 
    isMicActive, 
    startCamera, 
    stopCamera, 
    startMicrophone, 
    stopMicrophone, 
    videoStreamRef, 
    audioStreamRef, 
    setSimulationMode,
    startTrial,
    stopTrial
  } = useSystem()

  const router = useRouter()

  const isMounted = useSyncExternalStore(emptySubscribe, () => true, () => false)

  // Real heart rate trend data for chart (never pre-populated with random numbers in LIVE mode)
  const [data, setData] = useState<{ time: number; hr: number; baseline: number }[]>([])
  
  // Real-time extracted features
  const [visionFeatures, setVisionFeatures] = useState<VisionFeatures | null>(null)
  const [audioFeatures, setAudioFeatures] = useState<AudioFeatures | null>(null)
  const [physioFeatures, setPhysioFeatures] = useState<PhysioFeatures | null>(null)
  const [physioStatus, setPhysioStatus] = useState<PhysioStatus | null>(null)
  const [prediction, setPrediction] = useState<PredictionResult | null>(null)
  const [predictionLoading, setPredictionLoading] = useState<boolean>(true)
  const [predictionError, setPredictionError] = useState<string | null>(null)
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null)
  const [simMetrics, setSimMetrics] = useState<SimulatedMetrics>(INITIAL_SIMULATED_METRICS)
  const [waveformSamples, setWaveformSamples] = useState<WaveformPoint[]>([])
  const [activeGraphMode, setActiveGraphMode] = useState<'trend' | 'waveform'>('trend')
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null)
  const [sessionActionLoading, setSessionActionLoading] = useState(false)
  const [isSessionActive, setIsSessionActive] = useState(false)
  const [sessionStartTime, setSessionStartTime] = useState<number | null>(null)
  const [sessionElapsed, setSessionElapsed] = useState<number>(0)

  // In-flight & error suppression refs
  const isExtractingVisionRef = useRef(false)
  const isExtractingAudioRef = useRef(false)
  const hasLoggedOfflineRef = useRef(false)
  const videoRef = useRef<HTMLVideoElement | null>(null)

  // Stable callback ref to attach stream without resetting srcObject on re-renders
  const handleVideoRef = useCallback((node: HTMLVideoElement | null) => {
    videoRef.current = node
    if (node && videoStreamRef.current) {
      if (node.srcObject !== videoStreamRef.current) {
        node.srcObject = videoStreamRef.current
        node.play().catch(() => {})
      }
    }
  }, [videoStreamRef])

  // Sync stream to video element when camera becomes active or stream updates
  useEffect(() => {
    if (videoRef.current && videoStreamRef.current) {
      if (videoRef.current.srcObject !== videoStreamRef.current) {
        videoRef.current.srcObject = videoStreamRef.current
        videoRef.current.play().catch(() => {})
      }
    }
  }, [isCameraActive, videoStreamRef])

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  // Helper for safe MediaRecorder options
  const getRecorderOptions = (type: 'video' | 'audio') => {
    if (typeof window === 'undefined' || typeof MediaRecorder === 'undefined') return undefined
    const candidates = type === 'video'
      ? ['video/webm;codecs=vp8', 'video/webm', 'video/mp4']
      : ['audio/webm', 'audio/ogg', 'audio/mp4', 'audio/wav']
    for (const mime of candidates) {
      if (MediaRecorder.isTypeSupported(mime)) return { mimeType: mime }
    }
    return undefined
  }

  // Polling for real physiological sensor data (MAX30102) and multimodal prediction from FastAPI
  useEffect(() => {
    let isSubscribed = true

    const fetchBackendData = async () => {
      try {
        const sidParam = currentSessionId ? `&session_id=${currentSessionId}` : ''
        const [resHealth, resPhysio, resWaveform, resStatus, resPredict] = await Promise.allSettled([
          fetch(`${API_BASE}/health`),
          fetch(`${API_BASE}/api/physiological/latest`),
          fetch(`${API_BASE}/api/physiological/waveform?window_samples=100`),
          fetch(`${API_BASE}/api/physio/status`),
          fetch(`${API_BASE}/api/predict?trial_id=1${sidParam}`, { method: 'POST' })
        ])

        if (!isSubscribed) return

        // Backend health status check
        if (resHealth.status === 'fulfilled' && resHealth.value.ok) {
          setBackendOnline(true)
        } else {
          setBackendOnline(false)
        }

        // 1. Process Physiological Telemetry (Real MAX30102 data)
        if (resPhysio.status === 'fulfilled' && resPhysio.value.ok) {
          const json = await resPhysio.value.json()
          if (json.features) {
            setPhysioFeatures(json.features)

            // Feed live HR to dynamic chart only when real HR exists
            const hrVal = json.features.estimated_heart_rate_bpm ?? json.features.mean_hr ?? json.features.heart_rate
            if (hrVal && json.features.hr_valid) {
              setData(prev => {
                const newData = prev.length >= 30 ? prev.slice(1) : [...prev]
                const lastTime = newData[newData.length - 1]?.time || 0
                newData.push({
                  time: lastTime + 1,
                  hr: hrVal,
                  baseline: 75
                })
                return newData
              })
            }
          }
        }

        // 2. Process Raw PPG Waveform (Real MAX30102 optical samples)
        if (resWaveform.status === 'fulfilled' && resWaveform.value.ok) {
          const json = await resWaveform.value.json()
          if (json.samples && json.samples.length > 0) {
            setWaveformSamples(json.samples)
          }
        }

        // 3. Process Physio Status (Real serial port / hardware connection)
        if (resStatus.status === 'fulfilled' && resStatus.value.ok) {
          const json = await resStatus.value.json()
          setPhysioStatus(json)
        }

        // 4. Process Multimodal Prediction (Trained late fusion pipeline)
        if (resPredict.status === 'fulfilled' && resPredict.value.ok) {
          const json: PredictionResult = await resPredict.value.json()
          setPrediction(json)
          if (json.session_id && !currentSessionId) {
            setCurrentSessionId(json.session_id)
          }
          setPredictionLoading(false)
          setPredictionError(null)
        } else if (resPredict.status === 'rejected' || (resPredict.status === 'fulfilled' && !resPredict.value.ok)) {
          setPredictionLoading(false)
          setPredictionError('Inference temporarily unavailable')
        }
      } catch {
        setBackendOnline(false)
      }
    }

    fetchBackendData()
    const pollInterval = setInterval(fetchBackendData, 2000)
    return () => {
      isSubscribed = false
      clearInterval(pollInterval)
    }
  }, [API_BASE, isSimulationMode, currentSessionId])

  // Simulation updates: strictly isolated to Simulation Mode
  useEffect(() => {
    if (!isSimulationMode) return

    const interval = setInterval(() => {
      setData(prev => {
        const newData = prev.length >= 30 ? prev.slice(1) : [...prev]
        const lastTime = newData[newData.length - 1]?.time || 0
        newData.push({
          time: lastTime + 1,
          hr: 75 + Math.random() * 15 + Math.sin((lastTime + 1) / 2) * 5,
          baseline: 75
        })
        return newData
      })

      setSimMetrics({
        gazeX: (Math.random() * 2 + 1).toFixed(2),
        blinkRate: Math.floor(Math.random() * 5 + 12).toString(),
        headYaw: (Math.random() * 5 + 2).toFixed(1),
        eyebrowDelta: (Math.random() * 0.05).toFixed(3),
        zcr: (Math.random() * 0.1 + 0.05).toFixed(3),
        mfcc: (Math.random() * 15 - 30).toFixed(1),
        waveformHeights: Array.from({ length: 30 }, () => Math.floor(Math.random() * 85 + 15)),
      })
    }, 1000)

    return () => clearInterval(interval)
  }, [isSimulationMode])

  // Feature Extraction Polling: Upload live chunks to backend
  useEffect(() => {
    if (isSimulationMode) return

    const captureAndUpload = () => {
      // Capture Vision Chunk
      if (
        isCameraActive && 
        videoStreamRef.current && 
        videoStreamRef.current.active && 
        videoStreamRef.current.getVideoTracks().some(t => t.readyState === 'live') &&
        !isExtractingVisionRef.current
      ) {
        try {
          const options = getRecorderOptions('video')
          const vr = new MediaRecorder(videoStreamRef.current, options)
          const chunks: Blob[] = []
          vr.ondataavailable = e => { if (e.data && e.data.size > 0) chunks.push(e.data) }
          vr.onstop = async () => {
            if (chunks.length === 0) {
              isExtractingVisionRef.current = false
              return
            }
            const blob = new Blob(chunks, { type: options?.mimeType || 'video/webm' })
            const formData = new FormData()
            formData.append('file', blob, 'chunk.webm')
            try {
              const res = await fetch(`${API_BASE}/api/extract/vision`, { method: 'POST', body: formData })
              if (res.ok) {
                setBackendOnline(true)
                hasLoggedOfflineRef.current = false
                const result = await res.json()
                if (result.features) setVisionFeatures(result.features)
              }
            } catch {
              if (!hasLoggedOfflineRef.current) {
                console.warn(`[MOSAIC] Backend API at ${API_BASE} is unreachable.`)
                hasLoggedOfflineRef.current = true
              }
            } finally {
              isExtractingVisionRef.current = false
            }
          }
          isExtractingVisionRef.current = true
          vr.start()
          setTimeout(() => { 
            if (vr.state === 'recording') {
              vr.stop() 
            } else {
              isExtractingVisionRef.current = false
            }
          }, 1000)
        } catch {
          isExtractingVisionRef.current = false
        }
      }

      // Capture Audio Chunk
      if (
        isMicActive && 
        audioStreamRef.current && 
        audioStreamRef.current.active && 
        audioStreamRef.current.getAudioTracks().some(t => t.readyState === 'live') &&
        !isExtractingAudioRef.current
      ) {
        try {
          const options = getRecorderOptions('audio')
          const ar = new MediaRecorder(audioStreamRef.current, options)
          const chunks: Blob[] = []
          ar.ondataavailable = e => { if (e.data && e.data.size > 0) chunks.push(e.data) }
          ar.onstop = async () => {
            if (chunks.length === 0) {
              isExtractingAudioRef.current = false
              return
            }
            const blob = new Blob(chunks, { type: options?.mimeType || 'audio/webm' })
            const formData = new FormData()
            formData.append('file', blob, 'chunk.webm')
            try {
              const res = await fetch(`${API_BASE}/api/extract/audio`, { method: 'POST', body: formData })
              if (res.ok) {
                setBackendOnline(true)
                hasLoggedOfflineRef.current = false
                const result = await res.json()
                if (result.features) setAudioFeatures(result.features)
              }
            } catch {
              if (!hasLoggedOfflineRef.current) {
                console.warn(`[MOSAIC] Backend API at ${API_BASE} is unreachable.`)
                hasLoggedOfflineRef.current = true
              }
            } finally {
              isExtractingAudioRef.current = false
            }
          }
          isExtractingAudioRef.current = true
          ar.start()
          setTimeout(() => { 
            if (ar.state === 'recording') {
              ar.stop() 
            } else {
              isExtractingAudioRef.current = false
            }
          }, 1000)
        } catch {
          isExtractingAudioRef.current = false
        }
      }
    }

    const interval = setInterval(captureAndUpload, 2500)
    return () => {
      clearInterval(interval)
      isExtractingVisionRef.current = false
      isExtractingAudioRef.current = false
    }
  }, [isCameraActive, isMicActive, isSimulationMode, videoStreamRef, audioStreamRef, API_BASE])

  // Live Session Active Elapsed Timer
  useEffect(() => {
    let interval: NodeJS.Timeout | null = null
    if (isSessionActive && sessionStartTime) {
      interval = setInterval(() => {
        setSessionElapsed(Math.floor((Date.now() - sessionStartTime) / 1000))
      }, 1000)
    }
    return () => {
      if (interval) clearInterval(interval)
    }
  }, [isSessionActive, sessionStartTime])

  const formatTimer = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  // Session Control Handlers
  const handleStartSession = async () => {
    try {
      setSessionActionLoading(true)

      // Auto-start camera & mic if off in live sensor mode
      if (!isSimulationMode) {
        if (!isCameraActive) {
          try { await startCamera() } catch (e) { console.warn("Camera auto-start:", e) }
        }
        if (!isMicActive) {
          try { await startMicrophone() } catch (e) { console.warn("Mic auto-start:", e) }
        }
      }

      const res = await fetch(`${API_BASE}/api/session/start`, { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
      if (res.ok) {
        const json = await res.json()
        const sid = json.session_id
        setCurrentSessionId(sid)
        setIsSessionActive(true)
        setSessionStartTime(Date.now())
        setSessionElapsed(0)
        startTrial('P001', sid)
      }
    } catch (err) {
      console.error("Failed to start session:", err)
    } finally {
      setSessionActionLoading(false)
    }
  }

  const handleEndSession = async () => {
    try {
      setSessionActionLoading(true)
      const sid = currentSessionId || prediction?.session_id || 'latest'
      const res = await fetch(`${API_BASE}/api/session/${sid}/complete`, { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
      
      setIsSessionActive(false)
      stopTrial()

      if (res.ok) {
        const json = await res.json()
        const targetSid = json.session_id || sid
        router.push(`/session/${targetSid}/result`)
      } else {
        router.push(`/session/${sid}/result`)
      }
    } catch (err) {
      console.error("Failed to end session:", err)
      const sid = currentSessionId || 'latest'
      router.push(`/session/${sid}/result`)
    } finally {
      setSessionActionLoading(false)
    }
  }

  const handleResetSession = async () => {
    try {
      setSessionActionLoading(true)
      const res = await fetch(`${API_BASE}/api/session/reset`, { method: 'POST' })
      if (res.ok) {
        const json = await res.json()
        setCurrentSessionId(json.session_id)
        setIsSessionActive(false)
        setSessionStartTime(null)
        setSessionElapsed(0)
        stopTrial()
        setData([])
      }
    } catch (err) {
      console.error("Failed to reset session:", err)
    } finally {
      setSessionActionLoading(false)
    }
  }

  // Modality States
  const physActive = Boolean(physioFeatures && physioFeatures.hr_valid && physioFeatures.estimated_heart_rate_bpm)
  const audioActive = Boolean(isMicActive && audioFeatures && !audioFeatures.is_silent)
  const visionActive = Boolean(isCameraActive && visionFeatures && visionFeatures.face_detected === 1)
  const allModalitiesReady = Boolean(prediction?.fusion_status === 'ready' && prediction?.prediction)

  return (
    <div className="space-y-6 animate-fade-in-up pb-8">
      {/* Top Header & Hardware Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight">Live Multimodal Integration</h2>
            <Badge variant="outline" className="border-cyan-500/40 text-cyan-400 font-mono text-xs">
              Phase 11.1
            </Badge>
          </div>
          <p className="text-[var(--color-text-secondary)] mt-1 text-sm">
            Hardware PPG (MAX30102) &bull; Acoustic Processing &bull; Computer Vision &bull; Late Fusion Engine
          </p>
        </div>
        
        <div className="flex flex-wrap items-center gap-3">
          {/* Hardware Camera & Mic Toggles */}
          {!isSimulationMode && (
            <div className="flex gap-2">
              {isCameraActive ? (
                <Button variant="danger" size="sm" onClick={stopCamera} className="gap-2">
                  <VideoOff className="h-4 w-4"/> Stop Camera
                </Button>
              ) : (
                <Button variant="outline" size="sm" onClick={startCamera} className="gap-2 border-slate-700 hover:border-slate-500">
                  <Video className="h-4 w-4 text-emerald-400"/> Start Camera
                </Button>
              )}
              
              {isMicActive ? (
                <Button variant="danger" size="sm" onClick={stopMicrophone} className="gap-2">
                  <MicOff className="h-4 w-4"/> Stop Mic
                </Button>
              ) : (
                <Button variant="outline" size="sm" onClick={startMicrophone} className="gap-2 border-slate-700 hover:border-slate-500">
                  <Mic className="h-4 w-4 text-amber-400"/> Start Mic
                </Button>
              )}
            </div>
          )}

          {/* Mode Badge & Backend Connectivity Indicator */}
          <div className="flex gap-2 items-center">
            {isSimulationMode ? (
              <>
                <Button 
                  variant="outline" 
                  size="sm" 
                  onClick={async () => {
                    setSimulationMode(false)
                    setData([])
                    await startCamera()
                    await startMicrophone()
                  }}
                  className="text-xs"
                >
                  Switch to Live Sensors
                </Button>
                <Badge variant="warning" className="px-3 py-1 font-semibold tracking-wider">
                  DEMO / SYNTHETIC DATA
                </Badge>
              </>
            ) : (
              <>
                <Button 
                  variant="outline" 
                  size="sm" 
                  onClick={() => setSimulationMode(true)}
                  className="text-xs text-slate-400 hover:text-white"
                >
                  Switch to Simulation
                </Button>
                <Badge variant="success" className="px-3 py-1 font-semibold tracking-wider">
                  LIVE SENSOR MODE
                </Badge>
                {backendOnline === false && (
                  <Badge variant="error" className="px-3 py-1 font-mono text-xs animate-pulse">
                    BACKEND OFFLINE
                  </Badge>
                )}
                {backendOnline === true && (
                  <Badge variant="outline" className="px-3 py-1 border-emerald-500/40 text-emerald-400 text-xs font-mono">
                    API ONLINE :8000
                  </Badge>
                )}
              </>
            )}
          </div>
        </div>
      </div>

      {/* Backend Offline Warning Banner */}
      {backendOnline === false && !isSimulationMode && (
        <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-xs text-red-300 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="font-semibold uppercase tracking-wider text-red-400 flex items-center gap-1">
              <AlertTriangle className="h-4 w-4" /> Server Offline:
            </span>
            <span>FastAPI backend not running at <code className="bg-black/40 px-1.5 py-0.5 rounded text-red-200">{API_BASE}</code>. Run <code className="bg-black/40 px-1.5 py-0.5 rounded text-emerald-300">python main.py</code> in the backend directory.</span>
          </div>
        </div>
      )}

      {/* Session Control Toolbar */}
      <div className="p-3.5 bg-slate-900/60 border border-slate-800 rounded-xl flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-3">
          <span className="text-slate-400 font-medium uppercase tracking-wider text-[11px]">Experiment Session:</span>
          <code className="bg-black/60 px-2.5 py-1 rounded text-cyan-300 font-mono text-xs border border-cyan-500/20">
            {currentSessionId || prediction?.session_id || "SES_READY"}
          </code>
          {isSessionActive && (
            <Badge variant="success" className="gap-1.5 px-2.5 py-0.5 text-[10px] font-mono animate-pulse">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
              RECORDING {formatTimer(sessionElapsed)}
            </Badge>
          )}
          <Badge variant={allModalitiesReady ? "success" : "outline"} className="text-[10px]">
            {allModalitiesReady ? "ALL 3 MODALITIES ACTIVE" : "AWAITING ACTIVE MODALITIES"}
          </Badge>
        </div>

        <div className="flex items-center gap-2">
          {/* Start Session Button */}
          <Button 
            size="sm" 
            variant={isSessionActive ? "outline" : "default"} 
            onClick={handleStartSession} 
            disabled={sessionActionLoading || isSessionActive}
            className={cn(
              "gap-1.5 h-8 text-xs transition-all",
              isSessionActive 
                ? "border-emerald-500/40 text-emerald-400 opacity-90 cursor-default" 
                : "bg-emerald-600 hover:bg-emerald-500 text-white font-medium shadow-sm hover:shadow"
            )}
          >
            {isSessionActive ? (
              <>
                <span className="h-2 w-2 rounded-full bg-emerald-400 animate-ping"></span>
                Session Active
              </>
            ) : (
              <>
                <Play className="h-3.5 w-3.5 text-white fill-current" /> Start Session
              </>
            )}
          </Button>

          {/* End Session Button */}
          <Button 
            size="sm" 
            variant="danger" 
            onClick={handleEndSession} 
            disabled={sessionActionLoading}
            className={cn(
              "gap-1.5 h-8 text-xs font-medium transition-all text-white",
              isSessionActive 
                ? "bg-red-600 hover:bg-red-500 ring-2 ring-red-500/40 shadow-lg animate-pulse" 
                : "bg-red-700/80 hover:bg-red-600"
            )}
          >
            <Square className="h-3.5 w-3.5 fill-current" /> End Session
          </Button>

          {/* View Result Page Button */}
          <Button 
            size="sm" 
            variant="outline" 
            onClick={() => router.push(`/session/${currentSessionId || prediction?.session_id || 'latest'}/result`)}
            className="gap-1.5 h-8 text-xs border-cyan-500/40 text-cyan-300 hover:border-cyan-400 hover:text-white"
          >
            View Result Page
          </Button>

          {/* Reset Button */}
          <Button 
            size="sm" 
            variant="ghost" 
            onClick={handleResetSession} 
            disabled={sessionActionLoading}
            className="gap-1.5 h-8 text-xs text-slate-400 hover:text-white"
          >
            <RotateCcw className="h-3.5 w-3.5" /> Reset
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Left Column (2 Cols): Vision & Physiology Hardware View */}
        <div className="xl:col-span-2 space-y-6">
          {/* Vision Pipeline & Camera Feed */}
          <Card className="glass-panel overflow-hidden border-slate-800">
            <CardHeader className="border-b border-[var(--color-border-subtle)] pb-3">
              <div className="flex justify-between items-center">
                <CardTitle className="flex items-center gap-2 text-base">
                  <Eye className="h-5 w-5 text-cyan-400" />
                  Vision Pipeline (Face Landmarker)
                </CardTitle>
                <div className="flex gap-2 items-center">
                  {cameraStatus === 'PERMISSION DENIED' ? (
                    <Badge variant="error">PERMISSION DENIED</Badge>
                  ) : isCameraActive ? (
                    <Badge variant="success">LIVE CAMERA ACTIVE</Badge>
                  ) : isSimulationMode ? (
                    <Badge variant="warning">SIMULATION</Badge>
                  ) : (
                    <Badge variant="outline" className="text-slate-400 border-slate-700">CAMERA OFF</Badge>
                  )}
                  {visionFeatures?.face_detected === 1 && (
                    <Badge variant="outline" className="border-emerald-500/40 text-emerald-400">FACE DETECTED</Badge>
                  )}
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-0 relative">
              <div className="aspect-video bg-[#050505] relative flex items-center justify-center overflow-hidden">
                {isCameraActive ? (
                  <video 
                    ref={handleVideoRef}
                    autoPlay 
                    playsInline 
                    muted 
                    className="w-full h-full object-cover transform -scale-x-100"
                  />
                ) : (
                  <>
                    <div className="absolute inset-0 opacity-20 pointer-events-none" 
                         style={{ backgroundImage: 'radial-gradient(circle, #333 1px, transparent 1px)', backgroundSize: '20px 20px' }}></div>
                    <div className="text-center z-10 p-6">
                      <Camera className="h-12 w-12 text-[var(--color-text-muted)] mx-auto mb-2 opacity-50" />
                      <p className="text-[var(--color-text-muted)] font-mono text-sm tracking-wider">
                        {isSimulationMode ? "SIMULATED_VIDEO_FEED_ACTIVE" : "CAMERA INACTIVE — CLICK 'START CAMERA' TO STREAM"}
                      </p>
                    </div>
                  </>
                )}
              </div>
              
              {/* Vision Real Features */}
              <div className="grid grid-cols-4 divide-x divide-[var(--color-border-subtle)] border-t border-[var(--color-border-subtle)] bg-[var(--color-bg-surface)]">
                <div className="p-3 text-center">
                  <p className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Gaze X</p>
                  <p className="text-lg font-mono font-semibold text-white">
                    {visionFeatures && isCameraActive && visionFeatures.face_detected ? visionFeatures.gaze_x_mean.toFixed(2) : (isMounted && isSimulationMode ? simMetrics.gazeX : 'Unavailable')}
                  </p>
                </div>
                <div className="p-3 text-center">
                  <p className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Blink Rate</p>
                  <p className="text-lg font-mono font-semibold text-white">
                    {visionFeatures && isCameraActive && visionFeatures.face_detected ? `${visionFeatures.blink_rate.toFixed(1)} /min` : (isMounted && isSimulationMode ? `${simMetrics.blinkRate} /min` : 'Unavailable')}
                  </p>
                </div>
                <div className="p-3 text-center">
                  <p className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Head Yaw</p>
                  <p className="text-lg font-mono font-semibold text-white">
                    {visionFeatures && isCameraActive && visionFeatures.face_detected ? `${visionFeatures.head_yaw_mean.toFixed(1)}°` : (isMounted && isSimulationMode ? `${simMetrics.headYaw}°` : 'Unavailable')}
                  </p>
                </div>
                <div className="p-3 text-center">
                  <p className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Eyebrow Δ</p>
                  <p className="text-lg font-mono font-semibold text-white">
                    {visionFeatures && isCameraActive && visionFeatures.face_detected ? visionFeatures.eyebrow_delta_mean.toFixed(3) : (isMounted && isSimulationMode ? simMetrics.eyebrowDelta : 'Unavailable')}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Physiology Pipeline (MAX30102 Hardware Integration) */}
          <Card className="glass-panel border-slate-800">
            <CardHeader className="pb-3 border-b border-[var(--color-border-subtle)]">
              <div className="flex flex-wrap justify-between items-center gap-2">
                <CardTitle className="flex items-center gap-2 text-base">
                  <Heart className={`h-5 w-5 text-red-500 ${physActive ? 'animate-pulse' : ''}`} />
                  Physiology Pipeline (MAX30102 Sensor)
                </CardTitle>
                <div className="flex gap-2 items-center">
                  <div className="flex bg-black/40 rounded p-0.5 border border-slate-700/60">
                    <button 
                      type="button"
                      className={`text-[11px] px-2.5 py-0.5 rounded font-medium transition-colors ${activeGraphMode === 'trend' ? 'bg-[var(--color-primary)] text-white' : 'text-slate-400 hover:text-white'}`}
                      onClick={() => setActiveGraphMode('trend')}
                    >
                      HR Trend
                    </button>
                    <button 
                      type="button"
                      className={`text-[11px] px-2.5 py-0.5 rounded font-medium transition-colors ${activeGraphMode === 'waveform' ? 'bg-[var(--color-primary)] text-white' : 'text-slate-400 hover:text-white'}`}
                      onClick={() => setActiveGraphMode('waveform')}
                    >
                      PPG Waveform
                    </button>
                  </div>
                  
                  {/* Real Hardware Sensor Status */}
                  {physioStatus?.connected ? (
                    <Badge variant="success">
                      MAX30102 &bull; {physioStatus.port || "COM3"}
                    </Badge>
                  ) : (
                    <Badge variant="error">SENSOR DISCONNECTED</Badge>
                  )}

                  {physioStatus?.samples ? (
                    <Badge variant="outline" className="text-xs text-[var(--color-text-muted)] border-slate-700">
                      {physioStatus.samples.toLocaleString()} SAMPLES
                    </Badge>
                  ) : null}
                </div>
              </div>
            </CardHeader>
            <CardContent className="pt-5 space-y-4">
              {/* Graph Indicator Banner */}
              <div className="flex justify-between items-center text-xs text-slate-400 px-1">
                <span>
                  {activeGraphMode === 'trend' ? "Heart Rate (BPM) from optical systolic peak detection" : "Raw Optical PPG Window (Infrared channel)"}
                </span>
                <span className="font-mono text-[10px] font-semibold tracking-wider text-cyan-400 uppercase">
                  {isSimulationMode ? "DEMO DATA" : "LIVE SENSOR DATA"}
                </span>
              </div>

              <div className="h-44 w-full">
                {activeGraphMode === 'trend' ? (
                  data.length > 0 ? (
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={data} margin={{ top: 5, right: 5, left: -20, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-subtle)" vertical={false} />
                        <XAxis dataKey="time" hide />
                        <YAxis domain={['dataMin - 5', 'dataMax + 5']} stroke="var(--color-text-muted)" fontSize={12} tickFormatter={(val) => Math.round(val).toString()} />
                        <Tooltip 
                          contentStyle={{ backgroundColor: 'var(--color-bg-panel)', border: '1px solid var(--color-border-strong)' }}
                          itemStyle={{ color: 'var(--color-text-primary)' }}
                        />
                        <Line type="monotone" dataKey="baseline" stroke="var(--color-text-muted)" strokeDasharray="5 5" strokeWidth={1} dot={false} name="Rest Baseline" />
                        <Line type="monotone" dataKey="hr" stroke="var(--color-error)" strokeWidth={2} dot={false} isAnimationActive={false} name="Live Heart Rate (BPM)" />
                      </LineChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="h-full flex items-center justify-center border border-dashed border-slate-800 rounded-lg text-slate-500 text-xs font-mono">
                      Awaiting MAX30102 PPG heart rate stream... Place finger on sensor.
                    </div>
                  )
                ) : (
                  waveformSamples.length > 0 ? (
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={waveformSamples} margin={{ top: 5, right: 5, left: -10, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-subtle)" vertical={false} />
                        <XAxis dataKey="time" hide />
                        <YAxis domain={['dataMin - 100', 'dataMax + 100']} stroke="var(--color-text-muted)" fontSize={12} tickFormatter={(val) => Math.round(val).toString()} />
                        <Tooltip 
                          contentStyle={{ backgroundColor: 'var(--color-bg-panel)', border: '1px solid var(--color-border-strong)' }}
                          itemStyle={{ color: 'var(--color-text-primary)' }}
                        />
                        <Line type="monotone" dataKey="ir" stroke="#0ea5e9" strokeWidth={1.8} dot={false} isAnimationActive={false} name="IR Optical PPG" />
                      </LineChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="h-full flex items-center justify-center border border-dashed border-slate-800 rounded-lg text-slate-500 text-xs font-mono">
                      No PPG optical samples recorded in mosaic_ppg.csv yet.
                    </div>
                  )
                )}
              </div>

              {/* Real-time Physiological Telemetry Grid */}
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3 border-t border-[var(--color-border-subtle)] pt-4 text-center">
                <div className="p-2.5 rounded bg-[var(--color-bg-subtle)] border border-[var(--color-border-subtle)]">
                  <p className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Heart Rate</p>
                  <p className="text-lg font-mono font-bold text-white">
                    {physioFeatures?.estimated_heart_rate_bpm && physioFeatures.hr_valid
                      ? `${physioFeatures.estimated_heart_rate_bpm.toFixed(1)} BPM`
                      : 'Unavailable'}
                  </p>
                  <p className="text-[10px] text-slate-400 mt-0.5">
                    {physioFeatures?.hr_valid ? "Systolic peaks verified" : "Awaiting finger contact"}
                  </p>
                </div>

                <div className="p-2.5 rounded bg-[var(--color-bg-subtle)] border border-[var(--color-border-subtle)]">
                  <p className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-wider mb-1">HRV (SDNN / RMSSD)</p>
                  <p className="text-sm font-mono text-white font-semibold pt-1">
                    {physioFeatures?.sdnn && physioFeatures?.rmssd
                      ? `${physioFeatures.sdnn.toFixed(1)} ms / ${physioFeatures.rmssd.toFixed(1)} ms`
                      : 'Unavailable'}
                  </p>
                  <p className="text-[10px] text-slate-400 mt-0.5">RR variability</p>
                </div>

                <div className="p-2.5 rounded bg-[var(--color-bg-subtle)] border border-[var(--color-border-subtle)]">
                  <p className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Skin Temperature</p>
                  <p className="text-sm font-mono text-slate-400 pt-1">
                    Unavailable
                  </p>
                  <p className="text-[9px] text-slate-500 mt-0.5">No die sensor streamed</p>
                </div>

                <div className="p-2.5 rounded bg-[var(--color-bg-subtle)] border border-[var(--color-border-subtle)]">
                  <p className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Optical SpO2</p>
                  <p className="text-sm font-mono text-slate-400 pt-1">
                    Unavailable
                  </p>
                  <p className="text-[9px] text-slate-500 mt-0.5">Uncalibrated optical sensor</p>
                </div>

                <div className="p-2.5 rounded bg-[var(--color-bg-subtle)] border border-[var(--color-border-subtle)]">
                  <p className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Signal Quality</p>
                  <p className="text-sm font-mono text-white font-semibold pt-1">
                    {physioFeatures?.signal_quality_percent 
                      ? `${physioFeatures.signal_quality_percent.toFixed(0)}% (${(physioFeatures.signal_quality_status || 'GOOD').toUpperCase()})`
                      : 'Unavailable'}
                  </p>
                  <p className="text-[10px] text-slate-400 mt-0.5">Contact stability</p>
                </div>

                <div className="p-2.5 rounded bg-[var(--color-bg-subtle)] border border-[var(--color-border-subtle)]">
                  <p className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-wider mb-1">PPG Samples (Rate)</p>
                  <p className="text-sm font-mono text-white font-semibold pt-1">
                    {physioFeatures?.sample_count 
                      ? `${physioFeatures.sample_count} (${physioFeatures.sampling_rate || physioFeatures.sampling_rate_hz || 12.5} Hz)`
                      : 'Unavailable'}
                  </p>
                  <p className="text-[10px] text-slate-400 mt-0.5">COM port buffer</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Column: Audio, Modality Status Cards, Late Fusion & Result */}
        <div className="space-y-6">
          {/* Audio Pipeline Card */}
          <Card className="glass-panel border-slate-800">
            <CardHeader className="pb-3 border-b border-[var(--color-border-subtle)]">
              <div className="flex justify-between items-center">
                <CardTitle className="flex items-center gap-2 text-base">
                  <Mic className="h-5 w-5 text-amber-400" />
                  Audio Pipeline (Microphone)
                </CardTitle>
                <div className="flex gap-2">
                  {microphoneStatus === 'PERMISSION DENIED' ? (
                    <Badge variant="error">PERMISSION DENIED</Badge>
                  ) : isMicActive ? (
                    <Badge variant="success">LIVE MIC ACTIVE</Badge>
                  ) : isSimulationMode ? (
                    <Badge variant="warning">SIMULATION</Badge>
                  ) : (
                    <Badge variant="outline" className="text-slate-400 border-slate-700">MIC OFF</Badge>
                  )}
                </div>
              </div>
            </CardHeader>
            <CardContent className="pt-4 space-y-4">
              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-[var(--color-text-secondary)]">Zero Crossing Rate (ZCR)</span>
                  <span className="font-mono text-white">
                    {audioFeatures && isMicActive ? audioFeatures.zcr_mean.toFixed(3) : (isMounted && isSimulationMode ? simMetrics.zcr : 'Unavailable')}
                  </span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-[var(--color-text-secondary)]">MFCC Coefficient 1 (Mean)</span>
                  <span className="font-mono text-white">
                    {audioFeatures && audioFeatures.mfcc_mean?.length > 0 && isMicActive ? audioFeatures.mfcc_mean[0].toFixed(2) : (isMounted && isSimulationMode ? simMetrics.mfcc : 'Unavailable')}
                  </span>
                </div>
              </div>

              {/* Audio Waveform Bar Animation */}
              <div className="h-12 flex items-end justify-between gap-1 opacity-80 pt-2 border-t border-[var(--color-border-subtle)]">
                {Array.from({ length: 24 }).map((_, i) => {
                  let barHeight = 4
                  if (isSimulationMode) {
                    barHeight = simMetrics.waveformHeights[i] ?? 15
                  } else if (isMicActive && audioFeatures?.mfcc_mean && audioFeatures.mfcc_mean.length > 0 && !audioFeatures.is_silent) {
                    const coeff = Math.abs(audioFeatures.mfcc_mean[i % audioFeatures.mfcc_mean.length] || 10)
                    barHeight = Math.min(95, Math.max(8, (coeff % 70) + 12))
                  }
                  return (
                    <div 
                      key={i} 
                      className="w-full bg-amber-400/80 rounded-t-sm transition-all duration-200"
                      style={{ height: `${barHeight}%` }}
                    />
                  )
                })}
              </div>
            </CardContent>
          </Card>

          {/* REQUIREMENT 13: Three Modality Status Cards */}
          <div className="space-y-3">
            <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-1">
              Modality Input Status
            </p>
            <div className="grid grid-cols-3 gap-2 text-center">
              {/* 1. Physiological */}
              <div className="p-3 rounded-xl bg-slate-900/70 border border-slate-800 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-center gap-1 mb-1">
                    <Heart className="h-3.5 w-3.5 text-red-400" />
                    <span className="text-[10px] uppercase font-bold text-slate-300">Physiology</span>
                  </div>
                  <Badge variant={physActive ? "success" : "outline"} className="text-[9px] px-1.5 py-0.2">
                    {physActive ? "CONNECTED" : "WAITING"}
                  </Badge>
                </div>
                <div className="mt-2 pt-2 border-t border-slate-800">
                  <p className="text-[9px] text-slate-500 uppercase">Score</p>
                  <p className="text-xs font-mono font-bold text-white">
                    {prediction?.modality_scores?.physiological !== null && prediction?.modality_scores?.physiological !== undefined
                      ? prediction.modality_scores.physiological.toFixed(3)
                      : "Unavailable"}
                  </p>
                </div>
              </div>

              {/* 2. Audio */}
              <div className="p-3 rounded-xl bg-slate-900/70 border border-slate-800 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-center gap-1 mb-1">
                    <Mic className="h-3.5 w-3.5 text-amber-400" />
                    <span className="text-[10px] uppercase font-bold text-slate-300">Audio</span>
                  </div>
                  <Badge variant={audioActive ? "success" : "outline"} className="text-[9px] px-1.5 py-0.2">
                    {audioActive ? "CONNECTED" : "WAITING"}
                  </Badge>
                </div>
                <div className="mt-2 pt-2 border-t border-slate-800">
                  <p className="text-[9px] text-slate-500 uppercase">Score</p>
                  <p className="text-xs font-mono font-bold text-white">
                    {prediction?.modality_scores?.audio !== null && prediction?.modality_scores?.audio !== undefined
                      ? prediction.modality_scores.audio.toFixed(3)
                      : "Unavailable"}
                  </p>
                </div>
              </div>

              {/* 3. Vision */}
              <div className="p-3 rounded-xl bg-slate-900/70 border border-slate-800 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-center gap-1 mb-1">
                    <Eye className="h-3.5 w-3.5 text-cyan-400" />
                    <span className="text-[10px] uppercase font-bold text-slate-300">Vision</span>
                  </div>
                  <Badge variant={visionActive ? "success" : "outline"} className="text-[9px] px-1.5 py-0.2">
                    {visionActive ? "CONNECTED" : "WAITING"}
                  </Badge>
                </div>
                <div className="mt-2 pt-2 border-t border-slate-800">
                  <p className="text-[9px] text-slate-500 uppercase">Score</p>
                  <p className="text-xs font-mono font-bold text-white">
                    {prediction?.modality_scores?.vision !== null && prediction?.modality_scores?.vision !== undefined
                      ? prediction.modality_scores.vision.toFixed(3)
                      : "Unavailable"}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* REQUIREMENT 14: LATE FUSION & FINAL EXPERIMENTAL RESULT */}
          <Card className="glass-panel border-cyan-500/40 shadow-[0_0_20px_rgba(14,165,233,0.12)]">
            <CardHeader className="pb-3 border-b border-[var(--color-border-subtle)] bg-cyan-500/5">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-sm uppercase tracking-widest text-cyan-400 font-bold flex items-center gap-2">
                    <Activity className="h-4 w-4" /> MOSAIC EXPERIMENTAL RESULT
                  </CardTitle>
                  <p className="text-[10px] uppercase tracking-wider font-semibold text-slate-400 mt-0.5">
                    Model: trained_late_fusion_pipeline
                  </p>
                </div>
                <Badge variant={allModalitiesReady ? (prediction?.prediction === 'truthful' ? 'success' : 'error') : 'outline'}>
                  {allModalitiesReady ? (prediction?.prediction?.toUpperCase() || "READY") : "AWAITING ACTIVE MODALITIES"}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="pt-5 space-y-4">
              {allModalitiesReady ? (
                /* Genuine Multimodal Classification */
                <div className="text-center space-y-3">
                  <div>
                    <p className="text-[10px] uppercase tracking-wider text-slate-400 font-semibold mb-1">
                      Experimental Classification
                    </p>
                    <p className={`text-2xl font-black tracking-wider uppercase ${prediction?.prediction === 'truthful' ? 'text-emerald-400' : 'text-red-400'}`}>
                      {prediction?.prediction === 'truthful' ? 'TRUTHFUL' : 'DECEPTIVE'}
                    </p>
                  </div>

                  <div className="grid grid-cols-2 gap-3 p-3 bg-black/40 rounded-lg border border-slate-800 text-center">
                    <div>
                      <p className="text-[10px] text-slate-400 uppercase tracking-wider">Fusion Probability</p>
                      <p className="text-lg font-mono font-bold text-white">
                        {prediction?.fusion_probability !== null && prediction?.fusion_probability !== undefined
                          ? prediction.fusion_probability.toFixed(3)
                          : '--'}
                      </p>
                    </div>
                    <div>
                      <p className="text-[10px] text-slate-400 uppercase tracking-wider">Confidence</p>
                      <p className="text-lg font-mono font-bold text-cyan-400">
                        {prediction?.confidence !== null && prediction?.confidence !== undefined
                          ? prediction.confidence.toFixed(3)
                          : '--'}
                      </p>
                    </div>
                  </div>

                  {/* Modalities Used Checklist */}
                  <div className="pt-2 text-left space-y-1">
                    <p className="text-[10px] uppercase tracking-wider text-slate-400 font-semibold mb-1.5">
                      Modalities Used in Late Fusion:
                    </p>
                    <div className="flex flex-wrap gap-2 text-xs">
                      <span className="flex items-center gap-1 text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20 font-mono text-[11px]">
                        <CheckCircle2 className="h-3 w-3" /> Physiological (MAX30102)
                      </span>
                      <span className="flex items-center gap-1 text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20 font-mono text-[11px]">
                        <CheckCircle2 className="h-3 w-3" /> Audio (Microphone)
                      </span>
                      <span className="flex items-center gap-1 text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20 font-mono text-[11px]">
                        <CheckCircle2 className="h-3 w-3" /> Vision (Webcam)
                      </span>
                    </div>
                  </div>
                </div>
              ) : (
                /* Awaiting Active Modalities: No Fake 0.5 priors */
                <div className="text-center py-3 space-y-3">
                  <div className="inline-flex items-center gap-2 p-2 px-3 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs">
                    <Clock className="h-3.5 w-3.5 animate-spin" />
                    <span>Awaiting Active Modalities</span>
                  </div>

                  <p className="text-xs text-slate-300 max-w-xs mx-auto">
                    Late fusion requires real outputs from all 3 channels. Currently waiting for:
                  </p>

                  <div className="flex flex-wrap justify-center gap-1.5 text-xs font-mono">
                    {!physActive && (
                      <span className="bg-red-500/15 border border-red-500/30 text-red-300 px-2 py-0.5 rounded">
                        &bull; Physiological (MAX30102)
                      </span>
                    )}
                    {!audioActive && (
                      <span className="bg-amber-500/15 border border-amber-500/30 text-amber-300 px-2 py-0.5 rounded">
                        &bull; Audio (Mic active sound)
                      </span>
                    )}
                    {!visionActive && (
                      <span className="bg-cyan-500/15 border border-cyan-500/30 text-cyan-300 px-2 py-0.5 rounded">
                        &bull; Vision (Webcam face)
                      </span>
                    )}
                  </div>

                  <p className="text-[11px] text-slate-500">
                    Scientific honesty policy: Missing modalities are never fabricated or substituted with 0.5.
                  </p>
                </div>
              )}

              {/* End Session & View Dedicated Report */}
              <div className="pt-1">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={handleEndSession}
                  className="w-full text-xs gap-1.5 border-cyan-500/40 text-cyan-300 hover:border-cyan-400 hover:bg-cyan-500/10"
                >
                  End Session &amp; View Detailed Report &rarr;
                </Button>
              </div>

              {/* Research Prototype Disclaimer */}
              <div className="pt-3 border-t border-[var(--color-border-subtle)] text-center">
                <p className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">
                  SCIENTIFIC RESEARCH PROTOCOL DISCLAIMER
                </p>
                <p className="text-[10px] text-slate-400 mt-1 leading-relaxed">
                  MOSAIC multimodal deception analysis &mdash; research prototype for experimental pattern classification. Not a medical diagnostic system or lie detector.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
