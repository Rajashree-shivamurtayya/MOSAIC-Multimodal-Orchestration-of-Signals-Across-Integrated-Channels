"use client"

import React, { createContext, useContext, useState, useEffect, useRef } from 'react'

export type ConnectionStatus = 'CONNECTED' | 'READY' | 'PROCESSING' | 'DEGRADED' | 'UNAVAILABLE' | 'ERROR' | 'PERMISSION DENIED' | 'SIMULATED'
export type DataSource = 'SIMULATED DATA' | 'LIVE SENSOR DATA' | 'MIXED / PARTIAL INPUT'

interface SystemState {
  pipelineStatus: ConnectionStatus
  cameraStatus: ConnectionStatus
  microphoneStatus: ConnectionStatus
  physiologyStatus: ConnectionStatus
  inferenceStatus: ConnectionStatus
  frontendStatus: ConnectionStatus
  
  dataSource: DataSource
  isSimulationMode: boolean
  
  sessionInfo: {
    sessionId: string | null
    trialId: string | null
    participantId: string | null
  }

  // Live Media State
  isCameraActive: boolean
  isMicActive: boolean
}

interface SystemContextType extends SystemState {
  setSimulationMode: (mode: boolean) => void
  setConnectionStatus: (component: keyof SystemState, status: ConnectionStatus) => void
  startTrial: (participantId: string, customSessionId?: string) => void
  stopTrial: () => void
  
  // Media Actions
  startCamera: () => Promise<void>
  stopCamera: () => void
  startMicrophone: () => Promise<void>
  stopMicrophone: () => void
  
  // Expose refs for MediaStreams
  videoStreamRef: React.MutableRefObject<MediaStream | null>
  audioStreamRef: React.MutableRefObject<MediaStream | null>
}

const defaultState: SystemState = {
  pipelineStatus: 'READY',
  cameraStatus: 'UNAVAILABLE',
  microphoneStatus: 'UNAVAILABLE',
  physiologyStatus: 'READY',
  inferenceStatus: 'READY',
  frontendStatus: 'CONNECTED',
  dataSource: 'LIVE SENSOR DATA',
  isSimulationMode: false,
  sessionInfo: {
    sessionId: null,
    trialId: null,
    participantId: null
  },
  isCameraActive: false,
  isMicActive: false
}

const SystemContext = createContext<SystemContextType | undefined>(undefined)

export function SystemProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<SystemState>(defaultState)
  
  const videoStreamRef = useRef<MediaStream | null>(null)
  const audioStreamRef = useRef<MediaStream | null>(null)

  const setSimulationMode = (mode: boolean) => {
    // If switching to simulation, stop live hardware
    if (mode) {
      if (videoStreamRef.current) stopCamera()
      if (audioStreamRef.current) stopMicrophone()
      setState(prev => ({ 
        ...prev, 
        isSimulationMode: true,
        dataSource: 'SIMULATED DATA',
        cameraStatus: 'SIMULATED',
        microphoneStatus: 'SIMULATED',
        physiologyStatus: 'SIMULATED'
      }))
    } else {
      setState(prev => ({ 
        ...prev, 
        isSimulationMode: false,
        dataSource: 'LIVE SENSOR DATA',
        cameraStatus: 'UNAVAILABLE',
        microphoneStatus: 'UNAVAILABLE',
        physiologyStatus: 'UNAVAILABLE'
      }))
    }
  }

  const setConnectionStatus = (component: keyof SystemState, status: ConnectionStatus) => {
    setState(prev => ({ ...prev, [component]: status }))
  }

  const startTrial = (participantId: string, customSessionId?: string) => {
    const sessionId = customSessionId || `SES-${Date.now().toString().slice(-6)}`
    const trialId = `TRL-${Math.floor(Math.random() * 1000)}`
    setState(prev => ({
      ...prev,
      sessionInfo: { sessionId, trialId, participantId },
      pipelineStatus: 'PROCESSING'
    }))
  }

  const stopTrial = () => {
    setState(prev => ({
      ...prev,
      sessionInfo: { sessionId: null, trialId: null, participantId: null },
      pipelineStatus: 'READY'
    }))
  }

  const startCamera = async () => {
    try {
      if (state.isSimulationMode) setSimulationMode(false)
      const stream = await navigator.mediaDevices.getUserMedia({ video: true })
      videoStreamRef.current = stream
      setState(prev => ({ 
        ...prev, 
        isCameraActive: true,
        cameraStatus: 'CONNECTED',
        dataSource: 'LIVE SENSOR DATA'
      }))
    } catch (err: unknown) {
      console.error("Failed to start camera", err)
      const isDenied = err instanceof Error && err.name === 'NotAllowedError'
      setState(prev => ({ ...prev, cameraStatus: isDenied ? 'PERMISSION DENIED' : 'ERROR' }))
    }
  }

  const stopCamera = () => {
    if (videoStreamRef.current) {
      videoStreamRef.current.getTracks().forEach(track => track.stop())
      videoStreamRef.current = null
    }
    setState(prev => ({ ...prev, isCameraActive: false, cameraStatus: 'UNAVAILABLE' }))
  }

  const startMicrophone = async () => {
    try {
      if (state.isSimulationMode) setSimulationMode(false)
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      audioStreamRef.current = stream
      setState(prev => ({ 
        ...prev, 
        isMicActive: true,
        microphoneStatus: 'CONNECTED',
        dataSource: 'LIVE SENSOR DATA'
      }))
    } catch (err: unknown) {
      console.error("Failed to start microphone", err)
      const isDenied = err instanceof Error && err.name === 'NotAllowedError'
      setState(prev => ({ ...prev, microphoneStatus: isDenied ? 'PERMISSION DENIED' : 'ERROR' }))
    }
  }

  const stopMicrophone = () => {
    if (audioStreamRef.current) {
      audioStreamRef.current.getTracks().forEach(track => track.stop())
      audioStreamRef.current = null
    }
    setState(prev => ({ ...prev, isMicActive: false, microphoneStatus: 'UNAVAILABLE' }))
  }

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopCamera()
      stopMicrophone()
    }
  }, [])

  return (
    <SystemContext.Provider value={{ 
      ...state, 
      setSimulationMode, 
      setConnectionStatus, 
      startTrial, 
      stopTrial,
      startCamera,
      stopCamera,
      startMicrophone,
      stopMicrophone,
      videoStreamRef,
      audioStreamRef
    }}>
      {children}
    </SystemContext.Provider>
  )
}

export function useSystem() {
  const context = useContext(SystemContext)
  if (context === undefined) {
    throw new Error('useSystem must be used within a SystemProvider')
  }
  return context
}
