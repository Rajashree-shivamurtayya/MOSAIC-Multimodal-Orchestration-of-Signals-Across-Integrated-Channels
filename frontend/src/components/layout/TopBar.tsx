"use client"

import React, { useEffect, useState } from 'react'
import { Bell, Wifi, WifiOff } from 'lucide-react'
import { useSystem } from '@/context/SystemContext'
import { Badge } from '@/components/ui/badge'

export function TopBar() {
  const { sessionInfo, frontendStatus, dataSource } = useSystem()
  const [time, setTime] = useState<string>('')

  useEffect(() => {
    const updateTime = () => {
      const now = new Date()
      setTime(now.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' }))
    }
    updateTime()
    const timer = setInterval(updateTime, 1000)
    return () => clearInterval(timer)
  }, [])

  return (
    <header className="flex h-16 items-center justify-between border-b border-[var(--color-border-strong)] bg-[var(--color-bg-surface)] px-6">
      <div className="flex items-center">
        {sessionInfo.sessionId ? (
          <div className="flex items-center gap-4">
            <div className="flex flex-col">
              <span className="text-xs text-[var(--color-text-muted)] uppercase font-semibold">Active Session</span>
              <span className="text-sm font-medium text-white">{sessionInfo.sessionId}</span>
            </div>
            <div className="h-8 w-px bg-[var(--color-border-strong)]"></div>
            <div className="flex flex-col">
              <span className="text-xs text-[var(--color-text-muted)] uppercase font-semibold">Trial</span>
              <span className="text-sm font-medium text-white">{sessionInfo.trialId}</span>
            </div>
            {sessionInfo.participantId && (
              <>
                <div className="h-8 w-px bg-[var(--color-border-strong)]"></div>
                <div className="flex flex-col">
                  <span className="text-xs text-[var(--color-text-muted)] uppercase font-semibold">Participant</span>
                  <span className="text-sm font-medium text-white">{sessionInfo.participantId}</span>
                </div>
              </>
            )}
          </div>
        ) : (
          <div className="text-sm text-[var(--color-text-muted)] font-medium uppercase tracking-wider">
            System Idle
          </div>
        )}
      </div>

      <div className="flex items-center gap-6">
        {/* Data Source Indicator */}
        {dataSource === 'SIMULATED DATA' ? (
           <Badge variant="warning" className="uppercase tracking-wider">
            {dataSource} - Software Validation Mode
           </Badge>
        ) : (
          <Badge variant="success" className="uppercase tracking-wider">
            {dataSource}
          </Badge>
        )}

        <div className="h-5 w-px bg-[var(--color-border-strong)]"></div>

        <div className="flex items-center gap-2">
          {frontendStatus === 'CONNECTED' ? (
            <Wifi className="h-4 w-4 text-[var(--color-success)]" />
          ) : (
            <WifiOff className="h-4 w-4 text-[var(--color-error)]" />
          )}
          <span className="text-sm font-medium text-[var(--color-text-secondary)]">
            {frontendStatus}
          </span>
        </div>

        <button className="relative text-[var(--color-text-secondary)] hover:text-white transition-colors">
          <Bell className="h-5 w-5" />
          <span className="absolute top-0 right-0 block h-2 w-2 rounded-full bg-[var(--color-primary)] ring-2 ring-[var(--color-bg-surface)]" />
        </button>

        <div className="text-sm font-mono text-[var(--color-text-secondary)] bg-[var(--color-bg-panel)] px-3 py-1 rounded-md border border-[var(--color-border-subtle)]">
          {time}
        </div>
      </div>
    </header>
  )
}
