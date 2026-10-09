"use client"

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  Activity, 
  LayoutDashboard, 
  History, 
  LineChart, 
  Wrench, 
  BookOpen, 
  Settings 
} from 'lucide-react'
import { cn } from '@/lib/utils'

const navigation = [
  { name: 'System Overview', href: '/', icon: LayoutDashboard },
  { name: 'Live Monitoring', href: '/live', icon: Activity },
  { name: 'Trial History', href: '/history', icon: History },
  { name: 'Analytics', href: '/analytics', icon: LineChart },
  { name: 'System Diagnostics', href: '/diagnostics', icon: Wrench },
  { name: 'Documentation', href: '/documentation', icon: BookOpen },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <div className="flex h-full w-64 flex-col bg-[var(--color-bg-surface)] border-r border-[var(--color-border-strong)]">
      <div className="flex h-16 items-center px-6 border-b border-[var(--color-border-strong)]">
        <h1 className="text-xl font-bold tracking-widest text-white flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-[var(--color-primary)]"></span>
          MOSAIC
        </h1>
      </div>
      <div className="flex-1 overflow-y-auto py-4">
        <nav className="space-y-1 px-3">
          {navigation.map((item) => {
            const isActive = pathname === item.href || (item.href === '/documentation' && (pathname === '/documentation' || pathname === '/docs'))
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  isActive
                    ? 'bg-[var(--color-primary)]/10 text-[var(--color-primary)]'
                    : 'text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-panel)] hover:text-white',
                  'group flex items-center rounded-md px-3 py-2.5 text-sm font-medium transition-colors'
                )}
              >
                <item.icon
                  className={cn(
                    isActive ? 'text-[var(--color-primary)]' : 'text-[var(--color-text-muted)] group-hover:text-white',
                    'mr-3 h-5 w-5 flex-shrink-0 transition-colors'
                  )}
                  aria-hidden="true"
                />
                {item.name}
              </Link>
            )
          })}
        </nav>
      </div>
    </div>
  )
}
