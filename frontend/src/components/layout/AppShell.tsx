"use client"

import React from 'react'
import { Sidebar } from './Sidebar'
import { TopBar } from './TopBar'
import { BottomBar } from './BottomBar'
import { SystemProvider } from '@/context/SystemContext'

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <SystemProvider>
      <div className="flex h-screen overflow-hidden bg-[var(--color-bg-base)] text-[var(--color-text-primary)]">
        {/* Left Sidebar */}
        <Sidebar />
        
        {/* Main Content Area */}
        <div className="flex flex-1 flex-col overflow-hidden">
          {/* Top Navigation */}
          <TopBar />
          
          {/* Page Content */}
          <main className="flex-1 overflow-y-auto p-6 scroll-smooth">
            <div className="mx-auto max-w-7xl h-full">
              {children}
            </div>
          </main>
          
          {/* Bottom Status Bar */}
          <BottomBar />
        </div>
      </div>
    </SystemProvider>
  )
}
