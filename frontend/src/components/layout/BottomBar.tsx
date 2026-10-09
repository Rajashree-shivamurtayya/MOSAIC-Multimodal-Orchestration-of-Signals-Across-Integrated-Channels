"use client"

import React from 'react'
import { usePathname } from 'next/navigation'
import { useSystem, ConnectionStatus } from '@/context/SystemContext'
import { cn } from '@/lib/utils'

const StatusDot = ({ status }: { status: ConnectionStatus }) => {
  return (
    <span
      className={cn("h-2 w-2 rounded-full", {
        "bg-[var(--color-success)]": status === 'CONNECTED' || status === 'READY',
        "bg-[var(--color-primary)] animate-pulse": status === 'PROCESSING',
        "bg-[var(--color-warning)]": status === 'DEGRADED',
        "bg-[var(--color-error)]": status === 'ERROR',
        "bg-[var(--color-text-muted)]": status === 'UNAVAILABLE',
      })}
    />
  )
}

export function BottomBar() {
  const { pipelineStatus, dataSource } = useSystem()
  const pathname = usePathname()
  const isAnalytics = pathname === '/analytics'
  const isDoc = pathname === '/documentation' || pathname === '/docs'

  return (
    <footer className="flex h-10 items-center justify-between border-t border-[var(--color-border-strong)] bg-[var(--color-bg-surface)] px-6 text-xs text-[var(--color-text-secondary)]">
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2">
          <span className="font-semibold tracking-wider">MOSAIC v1.0.0</span>
        </div>
        
        <div className="h-4 w-px bg-[var(--color-border-strong)]"></div>
        
        <div className="flex items-center gap-2">
          <span>Pipeline:</span>
          <div className="flex items-center gap-1.5 bg-[var(--color-bg-panel)] px-2 py-0.5 rounded-md border border-[var(--color-border-subtle)]">
            <StatusDot status={pipelineStatus} />
            <span className="uppercase font-medium tracking-wide">{pipelineStatus}</span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <span>Source:</span>
        <span className={cn(
          "uppercase font-medium tracking-wider",
          isAnalytics 
            ? "text-[var(--color-warning)] font-semibold" 
            : isDoc
            ? "text-cyan-400 font-semibold"
            : dataSource === 'SIMULATED DATA' ? "text-[var(--color-warning)]" : "text-[var(--color-success)]"
        )}>
          {isAnalytics ? "OFFLINE MODEL EVALUATION" : isDoc ? "SYSTEM SPECIFICATION" : dataSource}
        </span>
      </div>
    </footer>
  )
}
