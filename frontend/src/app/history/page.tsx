"use client"

import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Search, Filter, ChevronDown, ChevronRight, Eye } from 'lucide-react'
import { cn } from '@/lib/utils'
import Link from 'next/link'

// Mock data
const mockTrials = Array.from({ length: 15 }).map((_, i) => ({
  id: `TRL-2026${(100 + i).toString()}`,
  session: `SES-${(800 + Math.floor(i/3)).toString()}`,
  participant: `P${(20 + Math.floor(i/2)).toString().padStart(3, '0')}`,
  timestamp: new Date(Date.now() - i * 86400000 - Math.random() * 3600000).toISOString(),
  fusionScore: Math.random() * 0.5 + 0.3,
  classification: Math.random() > 0.5 ? 'Deceptive' : 'Truthful',
  quality: Math.random() > 0.8 ? 'FAIR' : 'GOOD',
  modalities: ['Vision', 'Audio', 'Physiology'].filter(() => Math.random() > 0.1)
}))

export default function TrialHistory() {
  const [searchTerm, setSearchTerm] = useState('')
  const [expandedRow, setExpandedRow] = useState<string | null>(null)

  const filteredTrials = mockTrials.filter(trial => 
    trial.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
    trial.participant.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const toggleRow = (id: string) => {
    setExpandedRow(prev => prev === id ? null : id)
  }

  return (
    <div className="space-y-6 animate-fade-in-up">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Trial History</h2>
        <p className="text-[var(--color-text-secondary)] mt-1">Review past experimental classifications and raw data</p>
      </div>

      <Card className="glass-panel">
        <CardHeader className="pb-4 border-b border-[var(--color-border-subtle)]">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <CardTitle>Session Records</CardTitle>
            <div className="flex items-center gap-2 w-full sm:w-auto">
              <div className="relative flex-1 sm:w-64">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-[var(--color-text-muted)]" />
                <input
                  type="text"
                  placeholder="Search trials..."
                  className="w-full bg-[var(--color-bg-base)] border border-[var(--color-border-strong)] rounded-md pl-9 pr-3 py-2 text-sm focus:outline-none focus:border-[var(--color-primary)] transition-colors"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
              <button className="p-2 border border-[var(--color-border-strong)] rounded-md bg-[var(--color-bg-base)] hover:bg-[var(--color-bg-panel)] transition-colors">
                <Filter className="h-4 w-4 text-[var(--color-text-secondary)]" />
              </button>
            </div>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-[var(--color-text-secondary)] uppercase bg-[var(--color-bg-base)]/50 border-b border-[var(--color-border-strong)]">
                <tr>
                  <th className="px-6 py-4 font-semibold">Trial ID</th>
                  <th className="px-6 py-4 font-semibold">Participant</th>
                  <th className="px-6 py-4 font-semibold">Date & Time</th>
                  <th className="px-6 py-4 font-semibold">Classification</th>
                  <th className="px-6 py-4 font-semibold">Fusion Prob</th>
                  <th className="px-6 py-4 font-semibold">Quality</th>
                  <th className="px-6 py-4 font-semibold text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--color-border-subtle)]">
                {filteredTrials.map((trial) => (
                  <React.Fragment key={trial.id}>
                    <tr 
                      className={cn(
                        "hover:bg-[var(--color-bg-panel)]/50 transition-colors cursor-pointer",
                        expandedRow === trial.id && "bg-[var(--color-bg-panel)]"
                      )}
                      onClick={() => toggleRow(trial.id)}
                    >
                      <td className="px-6 py-4 font-mono font-medium text-white flex items-center gap-2">
                        {expandedRow === trial.id ? <ChevronDown className="h-4 w-4 text-[var(--color-text-muted)]" /> : <ChevronRight className="h-4 w-4 text-[var(--color-text-muted)]" />}
                        {trial.id}
                      </td>
                      <td className="px-6 py-4">{trial.participant}</td>
                      <td className="px-6 py-4 font-mono text-[var(--color-text-secondary)]">
                        {new Date(trial.timestamp).toLocaleString()}
                      </td>
                      <td className="px-6 py-4">
                        <Badge variant={trial.classification === 'Deceptive' ? 'warning' : 'success'}>
                          {trial.classification}
                        </Badge>
                      </td>
                      <td className="px-6 py-4 font-mono">
                        {(trial.fusionScore * 100).toFixed(1)}%
                      </td>
                      <td className="px-6 py-4">
                        <Badge variant={trial.quality === 'GOOD' ? 'success' : 'default'}>
                          {trial.quality}
                        </Badge>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <Link 
                          href={`/history/${trial.id}`}
                          className="inline-flex items-center justify-center p-2 rounded-md hover:bg-[var(--color-bg-base)] text-[var(--color-text-secondary)] hover:text-white transition-colors"
                          onClick={(e) => e.stopPropagation()}
                        >
                          <Eye className="h-4 w-4" />
                        </Link>
                      </td>
                    </tr>
                    
                    {/* Expandable Row Content */}
                    {expandedRow === trial.id && (
                      <tr className="bg-[var(--color-bg-base)]/30 border-b border-[var(--color-border-strong)]">
                        <td colSpan={7} className="px-10 py-6">
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div>
                              <h4 className="text-xs font-semibold uppercase text-[var(--color-text-muted)] mb-3">Available Modalities</h4>
                              <div className="flex gap-2">
                                {['Vision', 'Audio', 'Physiology'].map(mod => (
                                  <Badge 
                                    key={mod} 
                                    variant={trial.modalities.includes(mod) ? 'default' : 'outline'}
                                    className={!trial.modalities.includes(mod) ? 'opacity-50' : ''}
                                  >
                                    {mod}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                            <div>
                              <h4 className="text-xs font-semibold uppercase text-[var(--color-text-muted)] mb-3">Session Details</h4>
                              <div className="space-y-1 text-sm">
                                <p><span className="text-[var(--color-text-secondary)] w-24 inline-block">Session ID:</span> <span className="font-mono text-white">{trial.session}</span></p>
                                <p><span className="text-[var(--color-text-secondary)] w-24 inline-block">Duration:</span> <span className="font-mono text-white">4m 12s</span></p>
                              </div>
                            </div>
                            <div className="flex items-end justify-end">
                              <Link 
                                href={`/history/${trial.id}`}
                                className="text-sm font-medium text-[var(--color-primary)] hover:text-[var(--color-primary-dark)] transition-colors flex items-center gap-1"
                              >
                                View full detail report <ChevronRight className="h-4 w-4" />
                              </Link>
                            </div>
                          </div>
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
