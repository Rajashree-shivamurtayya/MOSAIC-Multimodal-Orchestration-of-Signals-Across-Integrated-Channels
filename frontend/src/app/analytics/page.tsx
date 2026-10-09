"use client"

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer,
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Cell
} from 'recharts'
import { FileText, Target, Zap, Activity, ShieldCheck, Database, Layers, Info } from 'lucide-react'

// Verified offline evaluation results from Dataset/results/model_comparison.csv & MODEL_TRAINING_REPORT.md
// Evaluation protocol: 5-Fold StratifiedGroupKFold on 300 participants / 3,000 trials
const performanceData = [
  { name: 'Physiology (LR)', accuracy: 62.0, f1: 61.9, auc: 0.663, model: 'physiology_pipeline.joblib' },
  { name: 'Audio (LR)', accuracy: 69.1, f1: 68.3, auc: 0.756, model: 'audio_pipeline.joblib' },
  { name: 'Vision (LR)', accuracy: 68.8, f1: 69.1, auc: 0.749, model: 'vision_pipeline.joblib' },
  { name: 'Late Fusion (LR)', accuracy: 73.4, f1: 73.3, auc: 0.801, model: 'fusion_model.joblib' },
]

const radarData = [
  { subject: 'Physiology', A: 62.0, fullMark: 100 },
  { subject: 'Audio', A: 69.1, fullMark: 100 },
  { subject: 'Vision', A: 68.8, fullMark: 100 },
  { subject: 'Fusion', A: 73.4, fullMark: 100 },
]

export default function Analytics() {
  const [latencyData, setLatencyData] = useState<{
    pureMean: number
    pureMedian: number
    apiMean: number
    runs: number
  }>({
    pureMean: 49.6,
    pureMedian: 47.9,
    apiMean: 86.2,
    runs: 90
  })

  // Optionally sync real-time benchmark telemetry from backend API if available
  useEffect(() => {
    const fetchAnalyticsApi = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/api/analytics')
        if (res.ok) {
          const json = await res.json()
          if (json.latency_benchmark?.pure_model_inference_ms) {
            setLatencyData({
              pureMean: json.latency_benchmark.pure_model_inference_ms.mean,
              pureMedian: json.latency_benchmark.pure_model_inference_ms.median,
              apiMean: json.latency_benchmark.end_to_end_http_api_ms?.mean || 86.2,
              runs: json.latency_benchmark.runs
            })
          }
        }
      } catch {
        // Fallback to verified local benchmark numbers
      }
    }
    fetchAnalyticsApi()
  }, [])

  return (
    <div className="space-y-6 animate-fade-in-up pb-8 max-w-7xl mx-auto px-4 sm:px-6">
      {/* Top Header & Context Badges */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2.5">
            <Activity className="h-6 w-6 text-cyan-400" />
            System Analytics
          </h1>
          <p className="text-xs text-slate-400 mt-0.5 font-medium">
            Offline Model Evaluation &bull; Phase 3&ndash;5 Cross-Validation Analysis
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="warning" className="px-3 py-1 font-mono text-xs tracking-wider">
            SIMULATED DATASET RESULTS
          </Badge>
          <Badge variant="outline" className="px-3 py-1 font-mono text-xs border-cyan-500/40 text-cyan-300">
            5-FOLD GROUPED CV
          </Badge>
        </div>
      </div>

      {/* STEP 4: Explanatory Context Banner */}
      <div className="p-4 bg-amber-950/20 border border-amber-500/30 rounded-xl flex items-start gap-3 text-xs text-amber-200/90 leading-relaxed">
        <Info className="h-5 w-5 text-amber-400 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold uppercase tracking-wider text-amber-300 block mb-0.5">
            Offline Evaluation Scope &mdash; Research Dataset Notice
          </span>
          <p>
            These metrics describe offline cross-validation of the trained MOSAIC models on the available research dataset (300 participants, 3,000 trials). 
            They are not live participant measurements and should not be interpreted as real-world lie-detection accuracy.
          </p>
        </div>
      </div>

      {/* Verified Metrics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="glass-panel border-slate-800">
          <CardHeader className="pb-2">
            <CardTitle className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Fusion ROC-AUC
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold font-mono text-white">0.801</div>
            <p className="text-xs text-emerald-400 mt-1 flex items-center">
              <Activity className="h-3 w-3 mr-1" /> 5-Fold Grouped CV (0.80)
            </p>
          </CardContent>
        </Card>

        <Card className="glass-panel border-slate-800">
          <CardHeader className="pb-2">
            <CardTitle className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Fusion Accuracy
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold font-mono text-white">73.4%</div>
            <p className="text-xs text-emerald-400 mt-1 flex items-center">
              <Target className="h-3 w-3 mr-1" /> Documented Baseline
            </p>
          </CardContent>
        </Card>

        <Card className="glass-panel border-slate-800">
          <CardHeader className="pb-2">
            <CardTitle className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Fusion F1-Score
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold font-mono text-white">73.3%</div>
            <p className="text-xs text-cyan-400 mt-1 flex items-center">
              <FileText className="h-3 w-3 mr-1" /> Balanced Precision/Recall
            </p>
          </CardContent>
        </Card>

        <Card className="glass-panel border-slate-800">
          <CardHeader className="pb-2">
            <CardTitle className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Measured Inference Latency
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold font-mono text-cyan-400">{latencyData.pureMean.toFixed(1)}ms</div>
            <p className="text-xs text-slate-400 mt-1 flex items-center">
              <Zap className="h-3 w-3 mr-1 text-amber-400" /> Median {latencyData.pureMedian.toFixed(1)}ms ({latencyData.runs} runs)
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Comparison & Radar Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="glass-panel border-slate-800">
          <CardHeader>
            <CardTitle className="text-sm font-bold uppercase tracking-wider text-white">
              Modality Comparison (Accuracy %)
            </CardTitle>
            <CardDescription className="text-xs text-slate-400">
              Cross-validated performance of unimodal pipelines vs. decision-level late fusion
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[280px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={performanceData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-subtle)" vertical={false} />
                  <XAxis dataKey="name" stroke="var(--color-text-muted)" fontSize={11} />
                  <YAxis domain={[50, 85]} stroke="var(--color-text-muted)" fontSize={11} unit="%" />
                  <RechartsTooltip 
                    contentStyle={{ backgroundColor: 'var(--color-bg-panel)', border: '1px solid var(--color-border-strong)', borderRadius: '8px' }}
                    itemStyle={{ color: 'var(--color-text-primary)' }}
                    cursor={{ fill: 'var(--color-border-subtle)' }}
                    formatter={(val: any) => [`${val}%`, 'Accuracy']}
                  />
                  <Bar dataKey="accuracy" radius={[4, 4, 0, 0]}>
                    {performanceData.map((entry, index) => (
                      <Cell 
                        key={`cell-${index}`} 
                        fill={index === 3 ? 'var(--color-primary)' : 'var(--color-text-muted)'} 
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-2 text-center">
              <p className="text-[11px] text-slate-500 font-mono">
                Late Fusion (+4.3% over best single modality: Audio 69.1%)
              </p>
            </div>
          </CardContent>
        </Card>

        <Card className="glass-panel border-slate-800">
          <CardHeader>
            <CardTitle className="text-sm font-bold uppercase tracking-wider text-white">
              Performance Radar
            </CardTitle>
            <CardDescription className="text-xs text-slate-400">
              Multidimensional view of modality contributions (Accuracy %)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[280px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                  <PolarGrid stroke="var(--color-border-subtle)" />
                  <PolarAngleAxis dataKey="subject" stroke="var(--color-text-secondary)" fontSize={11} />
                  <PolarRadiusAxis angle={30} domain={[50, 80]} stroke="var(--color-text-muted)" fontSize={10} />
                  <Radar name="Accuracy" dataKey="A" stroke="var(--color-primary)" fill="var(--color-primary)" fillOpacity={0.4} />
                  <RechartsTooltip 
                    contentStyle={{ backgroundColor: 'var(--color-bg-panel)', border: '1px solid var(--color-border-strong)' }}
                    formatter={(val: any) => [`${val}%`, 'Accuracy']}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Confusion Matrix & Provenance Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Verified Confusion Matrix */}
        <Card className="glass-panel border-slate-800">
          <CardHeader className="pb-3 border-b border-slate-800/80">
            <CardTitle className="text-sm font-bold uppercase tracking-wider text-white">
              Confusion Matrix (Late Fusion)
            </CardTitle>
            <CardDescription className="text-xs text-slate-400">
              Verified 5-Fold Cross-Validation on Research Dataset (3,000 Trials)
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-5">
            <div className="flex flex-col items-center justify-center">
              <div className="grid grid-cols-3 gap-1 mb-2 max-w-sm w-full text-center text-xs font-semibold text-slate-400">
                <div></div>
                <div className="text-emerald-400 font-mono">Pred: Truthful</div>
                <div className="text-rose-400 font-mono">Pred: Deceptive</div>
              </div>
              <div className="grid grid-cols-3 gap-1 max-w-sm w-full text-center">
                <div className="flex items-center justify-end pr-3 text-xs font-semibold text-slate-400 font-mono">
                  Act: Truthful
                </div>
                <div className="bg-emerald-500/20 p-4 rounded-lg border border-emerald-500/40 text-emerald-300 font-mono text-xl font-bold">
                  1,108
                  <span className="block text-[9px] font-sans text-slate-400 font-normal mt-0.5">True Negative</span>
                </div>
                <div className="bg-rose-500/20 p-4 rounded-lg border border-rose-500/40 text-rose-300 font-mono text-xl font-bold">
                  392
                  <span className="block text-[9px] font-sans text-slate-400 font-normal mt-0.5">False Positive</span>
                </div>
                
                <div className="flex items-center justify-end pr-3 text-xs font-semibold text-slate-400 font-mono">
                  Act: Deceptive
                </div>
                <div className="bg-rose-500/20 p-4 rounded-lg border border-rose-500/40 text-rose-300 font-mono text-xl font-bold">
                  405
                  <span className="block text-[9px] font-sans text-slate-400 font-normal mt-0.5">False Negative</span>
                </div>
                <div className="bg-emerald-500/30 p-4 rounded-lg border border-emerald-500/50 text-emerald-200 font-mono text-xl font-bold">
                  1,095
                  <span className="block text-[9px] font-sans text-slate-400 font-normal mt-0.5">True Positive</span>
                </div>
              </div>

              <div className="flex justify-between max-w-sm w-full text-[10px] text-slate-500 font-mono mt-3 px-1">
                <span>Total Trials: 3,000</span>
                <span>Balanced Accuracy: 73.4%</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* STEP 6: Measured Latency Benchmark Documentation */}
        <Card className="glass-panel border-slate-800">
          <CardHeader className="pb-3 border-b border-slate-800/80">
            <CardTitle className="text-sm font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
              <Zap className="h-4 w-4 text-amber-400" /> Measured Latency Benchmark Details
            </CardTitle>
            <CardDescription className="text-xs text-slate-400">
              Empirical execution timings on trained scikit-learn pipeline artifacts
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-4 space-y-3 text-xs">
            <dl className="grid grid-cols-2 gap-2.5">
              <div className="p-2.5 bg-slate-900/60 rounded border border-slate-800">
                <dt className="text-slate-500 text-[10px] uppercase font-bold">Execution Hardware</dt>
                <dd className="text-white font-mono mt-0.5 font-semibold">Host CPU (x86_64)</dd>
              </div>

              <div className="p-2.5 bg-slate-900/60 rounded border border-slate-800">
                <dt className="text-slate-500 text-[10px] uppercase font-bold">Benchmark Runs</dt>
                <dd className="text-white font-mono mt-0.5 font-semibold">{latencyData.runs} runs (10 warmup)</dd>
              </div>

              <div className="p-2.5 bg-slate-900/60 rounded border border-slate-800">
                <dt className="text-slate-500 text-[10px] uppercase font-bold">Pure Model Inference</dt>
                <dd className="text-cyan-300 font-mono mt-0.5 font-semibold">Mean: {latencyData.pureMean.toFixed(1)}ms | Median: {latencyData.pureMedian.toFixed(1)}ms</dd>
              </div>

              <div className="p-2.5 bg-slate-900/60 rounded border border-slate-800">
                <dt className="text-slate-500 text-[10px] uppercase font-bold">End-to-End HTTP API</dt>
                <dd className="text-white font-mono mt-0.5 font-semibold">~{latencyData.apiMean.toFixed(1)}ms (/api/predict)</dd>
              </div>
            </dl>

            <div className="p-3 bg-black/40 rounded border border-slate-800 space-y-1 font-mono text-[11px] text-slate-300">
              <div className="text-[10px] uppercase font-bold text-slate-500">Pipeline Execution Breakdown</div>
              <div className="flex justify-between"><span>&bull; Physiology (42 feats):</span> <span className="text-white">~13.0 ms</span></div>
              <div className="flex justify-between"><span>&bull; Audio (83 feats):</span> <span className="text-white">~16.8 ms</span></div>
              <div className="flex justify-between"><span>&bull; Vision (120 feats):</span> <span className="text-white">~18.1 ms</span></div>
              <div className="flex justify-between border-t border-slate-800 pt-1 text-cyan-300 font-bold">
                <span>&bull; Late Fusion Classifier (3 feats):</span> <span>~1.6 ms</span>
              </div>
            </div>

            <p className="text-[10px] text-slate-500 italic">
              Method: High-resolution time.perf_counter() bench on Dataset/models/*.joblib.
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Provenance & Scientific Disclaimer Card */}
      <Card className="glass-panel border-slate-800 text-center">
        <CardContent className="pt-5 pb-4 space-y-2">
          <p className="text-[10px] text-slate-400 uppercase tracking-widest font-bold">
            SCIENTIFIC RESEARCH PROTOCOL DISCLAIMER
          </p>
          <p className="text-xs text-slate-400 max-w-2xl mx-auto leading-relaxed">
            MOSAIC multimodal deception analysis &mdash; research prototype for experimental pattern classification. 
            Offline analytics describe model performance on simulated training distributions and do not constitute a medical diagnostic system or lie detector.
          </p>
          <div className="pt-2 flex justify-center items-center gap-4 text-[10px] font-mono text-slate-500">
            <span>Source: OFFLINE MODEL EVALUATION</span>
            <span>&bull;</span>
            <span>Protocol: 5-Fold StratifiedGroupKFold</span>
            <span>&bull;</span>
            <span>Dataset: 3,000 Trials</span>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
