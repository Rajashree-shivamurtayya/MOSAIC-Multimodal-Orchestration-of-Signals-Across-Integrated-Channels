"use client"

import React, { use } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { ArrowLeft, Eye, Mic, Heart, Activity, FileJson, AlertTriangle } from 'lucide-react'
import Link from 'next/link'

export default function TrialDetail({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params)
  
  return (
    <div className="space-y-6 animate-fade-in-up pb-8">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link href="/history" className="p-2 border border-[var(--color-border-strong)] rounded-md hover:bg-[var(--color-bg-panel)] transition-colors">
            <ArrowLeft className="h-5 w-5 text-[var(--color-text-secondary)]" />
          </Link>
          <div>
            <h2 className="text-2xl font-bold tracking-tight flex items-center gap-3">
              Trial Details: <span className="font-mono text-[var(--color-primary)]">{resolvedParams.id}</span>
            </h2>
            <p className="text-[var(--color-text-secondary)] mt-1">Recorded on {new Date().toLocaleString()}</p>
          </div>
        </div>
        <div className="flex gap-2">
          <Badge variant="warning">SIMULATED DATA</Badge>
          <Badge variant="success">COMPLETED</Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2 glass-panel">
          <CardHeader className="border-b border-[var(--color-border-subtle)]">
            <CardTitle>Multimodal Feature Summary</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div className="divide-y divide-[var(--color-border-subtle)]">
              {/* Vision Summary */}
              <div className="p-6 flex flex-col md:flex-row gap-6 hover:bg-[var(--color-bg-base)]/50 transition-colors">
                <div className="md:w-1/4">
                  <div className="flex items-center gap-2 mb-2">
                    <Eye className="h-4 w-4 text-[var(--color-primary)]" />
                    <h3 className="font-semibold text-white">Vision</h3>
                  </div>
                  <Badge variant="success" className="mb-1">Q: GOOD</Badge>
                </div>
                <div className="md:w-3/4 grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Gaze Dev</p>
                    <p className="font-mono text-white">2.41°</p>
                  </div>
                  <div>
                    <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Blinks</p>
                    <p className="font-mono text-white">16/min</p>
                  </div>
                  <div>
                    <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Head Mov</p>
                    <p className="font-mono text-white">4.2 mm/s</p>
                  </div>
                  <div>
                    <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Face Valid</p>
                    <p className="font-mono text-white">98.5%</p>
                  </div>
                </div>
              </div>

              {/* Audio Summary */}
              <div className="p-6 flex flex-col md:flex-row gap-6 hover:bg-[var(--color-bg-base)]/50 transition-colors">
                <div className="md:w-1/4">
                  <div className="flex items-center gap-2 mb-2">
                    <Mic className="h-4 w-4 text-[var(--color-accent)]" />
                    <h3 className="font-semibold text-white">Audio</h3>
                  </div>
                  <Badge variant="default" className="mb-1">Q: FAIR</Badge>
                </div>
                <div className="md:w-3/4 grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Resp Latency</p>
                    <p className="font-mono text-white">0.82s</p>
                  </div>
                  <div>
                    <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Silence Ratio</p>
                    <p className="font-mono text-white">14.2%</p>
                  </div>
                  <div>
                    <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Pitch Var</p>
                    <p className="font-mono text-white">22.4 Hz</p>
                  </div>
                </div>
              </div>

              {/* Physiology Summary */}
              <div className="p-6 flex flex-col md:flex-row gap-6 hover:bg-[var(--color-bg-base)]/50 transition-colors">
                <div className="md:w-1/4">
                  <div className="flex items-center gap-2 mb-2">
                    <Heart className="h-4 w-4 text-[var(--color-error)]" />
                    <h3 className="font-semibold text-white">Physiology</h3>
                  </div>
                  <Badge variant="success" className="mb-1">Q: EXCELLENT</Badge>
                </div>
                <div className="md:w-3/4 grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Avg HR</p>
                    <p className="font-mono text-white">78 bpm</p>
                  </div>
                  <div>
                    <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Base HR</p>
                    <p className="font-mono text-white">72 bpm</p>
                  </div>
                  <div>
                    <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Max HR Δ</p>
                    <p className="font-mono text-[var(--color-error)]">+14 bpm</p>
                  </div>
                  <div>
                    <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-1">SpO2</p>
                    <p className="font-mono text-white">98%</p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Card className="glass-panel">
            <CardHeader className="pb-2 border-b border-[var(--color-border-subtle)] bg-[var(--color-primary)]/5">
              <CardTitle className="text-center uppercase tracking-widest text-[var(--color-primary)] text-sm">
                Experimental Classification
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
              <div className="text-center mb-6">
                <div className="flex items-center justify-center gap-4">
                  <span className="text-4xl font-bold font-mono text-white">76.4%</span>
                  <div className="flex flex-col items-start">
                    <span className="text-sm font-semibold text-[var(--color-warning)] uppercase tracking-wide">Deceptive</span>
                    <span className="text-xs text-[var(--color-text-muted)]">Late Fusion</span>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--color-text-secondary)]">Physiology Model</span>
                  <span className="font-mono text-white">81.2%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--color-text-secondary)]">Audio Model</span>
                  <span className="font-mono text-white">72.5%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--color-text-secondary)]">Vision Model</span>
                  <span className="font-mono text-white">65.1%</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-panel">
            <CardHeader className="pb-4 border-b border-[var(--color-border-subtle)]">
              <CardTitle className="text-sm uppercase tracking-wider text-[var(--color-text-secondary)]">Technical Details</CardTitle>
            </CardHeader>
            <CardContent className="pt-4">
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <Activity className="h-4 w-4 text-[var(--color-text-muted)] mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-white">Processing Time</p>
                    <p className="text-xs text-[var(--color-text-muted)] font-mono">Vision: 142ms | Audio: 215ms | Phys: 45ms | Fusion: 12ms</p>
                  </div>
                </div>
                
                <div className="flex items-start gap-3">
                  <AlertTriangle className="h-4 w-4 text-[var(--color-warning)] mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-white">Warnings (1)</p>
                    <p className="text-xs text-[var(--color-text-muted)]">Audio clipping detected at 01:14 (handled by Phase 8 preprocessing)</p>
                  </div>
                </div>

                <Button variant="outline" className="w-full mt-2 gap-2 text-xs">
                  <FileJson className="h-4 w-4" /> Export Raw JSON Features
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
