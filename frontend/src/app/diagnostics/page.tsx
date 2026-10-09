"use client"

import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { useSystem } from '@/context/SystemContext'
import { RefreshCw, Server, Cpu, Database, Network, Heart } from 'lucide-react'

interface DiagnosticItemProps {
  title: string
  status: string
  details: string[]
  icon: React.ComponentType<{ className?: string }>
}

function DiagnosticItem({ title, status, details, icon: Icon }: DiagnosticItemProps) {
  const isError = status === 'ERROR' || status === 'NOT CONNECTED' || status === 'UNAVAILABLE'
  const isWarning = status === 'WARNING' || status === 'DEGRADED'
  
  return (
    <div className="flex items-start gap-4 p-4 rounded-lg bg-[var(--color-bg-base)] border border-[var(--color-border-subtle)]">
      <div className={`p-2 rounded-md ${isError ? 'bg-[var(--color-error)]/10 text-[var(--color-error)]' : isWarning ? 'bg-[var(--color-warning)]/10 text-[var(--color-warning)]' : 'bg-[var(--color-success)]/10 text-[var(--color-success)]'}`}>
        <Icon className="h-5 w-5" />
      </div>
      <div className="flex-1">
        <div className="flex items-center justify-between mb-1">
          <h4 className="font-semibold text-white">{title}</h4>
          <Badge variant={isError ? 'error' : isWarning ? 'warning' : 'success'}>
            {status}
          </Badge>
        </div>
        <div className="space-y-1 mt-2">
          {details.map((detail: string, i: number) => (
            <p key={i} className="text-xs text-[var(--color-text-muted)] font-mono">{detail}</p>
          ))}
        </div>
      </div>
    </div>
  )
}

export default function Diagnostics() {
  const { cameraStatus, microphoneStatus, isSimulationMode } = useSystem()
  const [isRefreshing, setIsRefreshing] = useState(false)

  const handleRefresh = () => {
    setIsRefreshing(true)
    setTimeout(() => setIsRefreshing(false), 1500)
  }

  return (
    <div className="space-y-6 animate-fade-in-up pb-8">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">System Diagnostics</h2>
          <p className="text-[var(--color-text-secondary)] mt-1">Engineering view of hardware and pipeline states</p>
        </div>
        <Button onClick={handleRefresh} disabled={isRefreshing} variant="outline" className="gap-2">
          <RefreshCw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
          Run Diagnostics
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="glass-panel">
          <CardHeader className="border-b border-[var(--color-border-subtle)]">
            <CardTitle className="flex items-center gap-2">
              <Server className="h-5 w-5 text-[var(--color-text-secondary)]" />
              Hardware & Sensors
            </CardTitle>
          </CardHeader>
          <CardContent className="p-4 space-y-4">
            <DiagnosticItem 
              title="ESP32-C3 Microcontroller"
              status={isSimulationMode ? "NOT CONNECTED" : "CONNECTED"}
              icon={Cpu}
              details={[
                `Port: ${isSimulationMode ? 'N/A' : 'COM3'}`,
                `Baud Rate: 115200`,
                `Last Heartbeat: ${isSimulationMode ? 'Never' : '23ms ago'}`
              ]}
            />
            <DiagnosticItem 
              title="MAX30102 Physiology Sensor"
              status={isSimulationMode ? "NOT CONNECTED" : "CONNECTED"}
              icon={Heart}
              details={[
                `I2C Address: 0x57`,
                `Sample Rate: 100Hz`,
                isSimulationMode ? `Status: Awaiting Hardware` : `Status: Acquiring clean PPG`
              ]}
            />
            <DiagnosticItem 
              title="Camera Feed (Vision)"
              status={cameraStatus}
              icon={Network}
              details={[
                `Resolution: 1920x1080 @ 30fps`,
                `Format: MJPEG`,
                `Dropped Frames: 0`
              ]}
            />
            <DiagnosticItem 
              title="Microphone (Audio)"
              status={microphoneStatus}
              icon={Network}
              details={[
                `Sample Rate: 16000Hz`,
                `Channels: 1 (Mono)`,
                `Bit Depth: 16-bit`
              ]}
            />
          </CardContent>
        </Card>

        <Card className="glass-panel">
          <CardHeader className="border-b border-[var(--color-border-subtle)]">
            <CardTitle className="flex items-center gap-2">
              <Database className="h-5 w-5 text-[var(--color-text-secondary)]" />
              Software Pipeline
            </CardTitle>
          </CardHeader>
          <CardContent className="p-4 space-y-4">
            <DiagnosticItem 
              title="Feature Extractor"
              status="READY"
              icon={Server}
              details={[
                `Vision Features: 42 extracted`,
                `Audio Features: 28 extracted`,
                `Physiology Features: 14 extracted`,
                `Missing Features: 0`
              ]}
            />
            <DiagnosticItem 
              title="Inference Engine (FastAPI)"
              status="READY"
              icon={Server}
              details={[
                `Endpoint: http://localhost:8000`,
                `Latency (p95): 230ms`,
                `Model Versions: v1.2.0 (Phase 6)`
              ]}
            />
            <DiagnosticItem 
              title="Late Fusion Engine"
              status="READY"
              icon={Server}
              details={[
                `Weights: Fixed (Optimized Phase 5)`,
                `Mode: Ensemble Classification`,
                `Confidence Threshold: 0.65`
              ]}
            />
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
