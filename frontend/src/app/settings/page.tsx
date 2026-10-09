"use client"

import React, { useState } from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ArrowLeft, Save, Bell, Shield, Server, Palette } from 'lucide-react'

export default function Settings() {
  const [saveStatus, setSaveStatus] = useState<string | null>(null)

  const handleSave = () => {
    setSaveStatus('Saving...')
    setTimeout(() => {
      setSaveStatus('Saved')
      setTimeout(() => setSaveStatus(null), 2000)
    }, 1000)
  }

  return (
    <div className="space-y-6 animate-fade-in-up pb-8">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Settings</h2>
          <p className="text-[var(--color-text-secondary)] mt-1">Configure MOSAIC system preferences</p>
        </div>
        <div className="flex items-center gap-3">
          <Link href="/">
            <Button variant="outline" className="border-[var(--color-border-strong)] bg-transparent hover:bg-[var(--color-bg-panel)]">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Dashboard
            </Button>
          </Link>
          <Button 
            className="bg-[var(--color-primary)] hover:bg-[var(--color-primary)]/90 text-white"
            onClick={handleSave}
            disabled={saveStatus !== null}
          >
            <Save className="h-4 w-4 mr-2" />
            {saveStatus || 'Save Changes'}
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="glass-panel">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Server className="h-5 w-5 text-[var(--color-primary)]" />
              API Configuration
            </CardTitle>
            <CardDescription>Backend connection settings</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-white">Backend Endpoint URL</label>
              <input 
                type="text" 
                defaultValue="http://localhost:8000"
                className="w-full bg-[var(--color-bg-panel)] border border-[var(--color-border-strong)] rounded-md px-3 py-2 text-white focus:outline-none focus:ring-1 focus:ring-[var(--color-primary)]"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-white">Websocket URL</label>
              <input 
                type="text" 
                defaultValue="ws://localhost:8000/ws"
                className="w-full bg-[var(--color-bg-panel)] border border-[var(--color-border-strong)] rounded-md px-3 py-2 text-white focus:outline-none focus:ring-1 focus:ring-[var(--color-primary)]"
              />
            </div>
          </CardContent>
        </Card>

        <Card className="glass-panel">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Palette className="h-5 w-5 text-[var(--color-primary)]" />
              Appearance
            </CardTitle>
            <CardDescription>Customize UI preferences</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between p-3 rounded-md border border-[var(--color-border-strong)] bg-[var(--color-bg-panel)]">
              <div>
                <div className="font-medium text-white">Dark Theme</div>
                <div className="text-sm text-[var(--color-text-secondary)]">Use dark mode by default</div>
              </div>
              <Badge className="bg-[var(--color-primary)] text-white">Active</Badge>
            </div>
            <div className="flex items-center justify-between p-3 rounded-md border border-[var(--color-border-strong)] bg-[var(--color-bg-panel)] opacity-50">
              <div>
                <div className="font-medium text-white">High Contrast</div>
                <div className="text-sm text-[var(--color-text-secondary)]">Increase contrast for visibility</div>
              </div>
              <Badge variant="outline" className="border-[var(--color-border-strong)] text-[var(--color-text-secondary)]">Disabled</Badge>
            </div>
          </CardContent>
        </Card>

        <Card className="glass-panel">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bell className="h-5 w-5 text-[var(--color-primary)]" />
              Notifications
            </CardTitle>
            <CardDescription>Alerts and sound settings</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-2">
              <input type="checkbox" id="sound" defaultChecked className="h-4 w-4 rounded border-[var(--color-border-strong)] bg-[var(--color-bg-panel)] text-[var(--color-primary)] focus:ring-[var(--color-primary)]" />
              <label htmlFor="sound" className="text-sm text-white">Enable sound alerts for anomalies</label>
            </div>
            <div className="flex items-center gap-2">
              <input type="checkbox" id="visual" defaultChecked className="h-4 w-4 rounded border-[var(--color-border-strong)] bg-[var(--color-bg-panel)] text-[var(--color-primary)] focus:ring-[var(--color-primary)]" />
              <label htmlFor="visual" className="text-sm text-white">Show visual notifications</label>
            </div>
          </CardContent>
        </Card>

        <Card className="glass-panel">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5 text-[var(--color-primary)]" />
              Privacy & Security
            </CardTitle>
            <CardDescription>Data retention and sharing</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-2">
              <input type="checkbox" id="save-local" defaultChecked className="h-4 w-4 rounded border-[var(--color-border-strong)] bg-[var(--color-bg-panel)] text-[var(--color-primary)] focus:ring-[var(--color-primary)]" />
              <label htmlFor="save-local" className="text-sm text-white">Save session data locally</label>
            </div>
            <div className="flex items-center gap-2">
              <input type="checkbox" id="anon" defaultChecked className="h-4 w-4 rounded border-[var(--color-border-strong)] bg-[var(--color-bg-panel)] text-[var(--color-primary)] focus:ring-[var(--color-primary)]" />
              <label htmlFor="anon" className="text-sm text-white">Anonymize physiological data</label>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
