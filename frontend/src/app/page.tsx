"use client"

import React from 'react'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { useSystem } from '@/context/SystemContext'
import { Play, Pause, Camera, Mic, Heart, Activity, Info } from 'lucide-react'

interface StatusCardProps {
  title: string
  status: string
  icon: React.ComponentType<{ className?: string }>
  description: string
}

function StatusCard({ title, status, icon: Icon, description }: StatusCardProps) {
  return (
    <Card className="glass-panel">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-base flex items-center gap-2">
            <Icon className="h-4 w-4 text-[var(--color-primary)]" />
            {title}
          </CardTitle>
          <Badge 
            variant={
              status === 'CONNECTED' || status === 'READY' ? 'success' :
              status === 'PROCESSING' ? 'default' :
              status === 'SIMULATED' ? 'warning' :
              status === 'DEGRADED' ? 'warning' :
              status === 'UNAVAILABLE' ? 'outline' : 'error'
            }
          >
            {status}
          </Badge>
        </div>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
    </Card>
  )
}

export default function Home() {
  const { 
    pipelineStatus, 
    cameraStatus, 
    microphoneStatus, 
    physiologyStatus, 
    startTrial,
    stopTrial,
    sessionInfo,
    isSimulationMode,
    setSimulationMode,
    startCamera,
    startMicrophone
  } = useSystem()

  const handleStartTrial = () => {
    if (sessionInfo.sessionId) {
      stopTrial()
    } else {
      startTrial('P' + Math.floor(Math.random() * 1000).toString().padStart(3, '0'))
    }
  }

  return (
    <div className="space-y-6 animate-fade-in-up">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">System Overview</h2>
        <p className="text-[var(--color-text-secondary)] mt-1">
          Multimodal Orchestration of Signals Across Integrated Channels
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatusCard 
          title="Pipeline" 
          status={pipelineStatus} 
          icon={Activity} 
          description="Main orchestrator status"
        />
        <StatusCard 
          title="Camera" 
          status={cameraStatus} 
          icon={Camera} 
          description="Phase 7.2 Vision module"
        />
        <StatusCard 
          title="Microphone" 
          status={microphoneStatus} 
          icon={Mic} 
          description="Phase 8 Audio module"
        />
        <StatusCard 
          title="Physiology" 
          status={physiologyStatus} 
          icon={Heart} 
          description="Phase 9 MAX30102 + ESP32"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="col-span-2 glass-panel">
          <CardHeader>
            <CardTitle>Session Control</CardTitle>
            <CardDescription>Manage active trials and data collection</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-4 p-4 rounded-lg bg-[var(--color-bg-panel)] border border-[var(--color-border-subtle)]">
              <div className="flex-1">
                <p className="text-sm font-medium">Data Source Mode</p>
                <p className="text-xs text-[var(--color-text-muted)] mt-1">
                  {isSimulationMode 
                    ? "Running in Software Validation Mode using existing MOSAIC dataset."
                    : "Running with Live Sensor Data (Hardware Connected)."}
                </p>
              </div>
              <Button 
                variant={isSimulationMode ? "secondary" : "outline"} 
                onClick={async () => {
                  if (isSimulationMode) {
                    setSimulationMode(false)
                    await startCamera()
                    await startMicrophone()
                  } else {
                    setSimulationMode(true)
                  }
                }}
              >
                {isSimulationMode ? "Switch to Live Sensors" : "Switch to Simulation"}
              </Button>
            </div>

            <div className="flex items-center gap-4 justify-between mt-6 pt-4 border-t border-[var(--color-border-subtle)]">
              <div>
                {sessionInfo.sessionId ? (
                  <div>
                    <p className="text-sm font-medium text-[var(--color-success)]">Trial in progress</p>
                    <p className="text-xs text-[var(--color-text-muted)]">Session: {sessionInfo.sessionId} | Trial: {sessionInfo.trialId}</p>
                  </div>
                ) : (
                  <div>
                    <p className="text-sm font-medium text-[var(--color-text-muted)]">System idle</p>
                    <p className="text-xs text-[var(--color-text-muted)]">Ready for new session</p>
                  </div>
                )}
              </div>
              <Button 
                onClick={handleStartTrial}
                variant={sessionInfo.sessionId ? "danger" : "default"}
                size="lg"
                className="gap-2"
              >
                {sessionInfo.sessionId ? (
                  <><Pause className="h-4 w-4" /> Stop Trial</>
                ) : (
                  <><Play className="h-4 w-4" /> Start New Trial</>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="glass-panel">
          <CardHeader>
            <CardTitle>Inference Engine</CardTitle>
            <CardDescription>Trained Multimodal Artifacts (Dataset/models)</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center text-sm">
              <span className="text-[var(--color-text-secondary)]">Late Fusion (fusion_model.joblib)</span>
              <Badge variant="success">READY</Badge>
            </div>
            <div className="flex justify-between items-center text-sm">
              <span className="text-[var(--color-text-secondary)]">Vision (vision_pipeline.joblib)</span>
              <Badge variant="success">READY</Badge>
            </div>
            <div className="flex justify-between items-center text-sm">
              <span className="text-[var(--color-text-secondary)]">Audio (audio_pipeline.joblib)</span>
              <Badge variant="success">READY</Badge>
            </div>
            <div className="flex justify-between items-center text-sm">
              <span className="text-[var(--color-text-secondary)]">Physiology (physiology_pipeline.joblib)</span>
              <Badge variant="success">READY</Badge>
            </div>

            <div className="mt-4 pt-4 border-t border-[var(--color-border-subtle)]">
              <div className="flex items-start gap-2 p-3 rounded bg-[var(--color-bg-base)] text-xs text-[var(--color-text-muted)]">
                <Info className="h-4 w-4 flex-shrink-0 mt-0.5 text-[var(--color-accent)]" />
                <p>
                  This system analyzes multimodal behavioural and physiological signals. 
                  It does not establish whether a person is actually lying.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
