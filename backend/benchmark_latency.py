"""
MOSAIC Model Inference Latency Benchmark
Directly measures the pure inference latency of all trained scikit-learn pipeline artifacts:
- physiology_pipeline.joblib
- audio_pipeline.joblib
- vision_pipeline.joblib
- fusion_model.joblib

Also benchmarks the end-to-end HTTP predict endpoint latency.
"""

import time
import os
import json
import joblib
import numpy as np
import pandas as pd
import requests

MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Dataset", "models"))

def benchmark_model_inference(num_runs: int = 100, warmup: int = 10):
    print("=" * 65)
    print("  MOSAIC MODEL INFERENCE LATENCY BENCHMARK")
    print("=" * 65)
    print(f"Artifacts directory: {MODELS_DIR}")
    
    # Load pipelines
    p_pipe = joblib.load(os.path.join(MODELS_DIR, "physiology_pipeline.joblib"))
    a_pipe = joblib.load(os.path.join(MODELS_DIR, "audio_pipeline.joblib"))
    v_pipe = joblib.load(os.path.join(MODELS_DIR, "vision_pipeline.joblib"))
    f_model = joblib.load(os.path.join(MODELS_DIR, "fusion_model.joblib"))
    
    with open(os.path.join(MODELS_DIR, "model_features.json"), "r") as f:
        feature_schema = json.load(f)
        
    df_phys = pd.DataFrame([{col: 0.0 for col in feature_schema["physiology_features"]}])
    df_aud = pd.DataFrame([{col: 0.0 for col in feature_schema["audio_features"]}])
    df_vis = pd.DataFrame([{col: 0.0 for col in feature_schema["vision_features"]}])
    
    # Warmup runs
    for _ in range(warmup):
        pp = p_pipe.predict_proba(df_phys)[0, 1]
        ap = a_pipe.predict_proba(df_aud)[0, 1]
        vp = v_pipe.predict_proba(df_vis)[0, 1]
        fp = f_model.predict_proba(np.array([[pp, ap, vp]]))[0, 1]
        
    latencies = []
    phys_latencies = []
    aud_latencies = []
    vis_latencies = []
    fusion_latencies = []
    
    for _ in range(num_runs - warmup):
        t0 = time.perf_counter()
        
        tp0 = time.perf_counter()
        pp = p_pipe.predict_proba(df_phys)[0, 1]
        tp1 = time.perf_counter()
        phys_latencies.append((tp1 - tp0) * 1000)
        
        ta0 = time.perf_counter()
        ap = a_pipe.predict_proba(df_aud)[0, 1]
        ta1 = time.perf_counter()
        aud_latencies.append((ta1 - ta0) * 1000)
        
        tv0 = time.perf_counter()
        vp = v_pipe.predict_proba(df_vis)[0, 1]
        tv1 = time.perf_counter()
        vis_latencies.append((tv1 - tv0) * 1000)
        
        tf0 = time.perf_counter()
        fp = f_model.predict_proba(np.array([[pp, ap, vp]]))[0, 1]
        tf1 = time.perf_counter()
        fusion_latencies.append((tf1 - tf0) * 1000)
        
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1000)
        
    arr = np.array(latencies)
    print(f"\n[BENCHMARK RESULTS - {len(arr)} Validated Runs]")
    print(f"Total Multimodal Pipeline Inference (Mean):   {np.mean(arr):.2f} ms")
    print(f"Total Multimodal Pipeline Inference (Median): {np.median(arr):.2f} ms")
    print(f"Total Multimodal Pipeline Inference (Min):    {np.min(arr):.2f} ms")
    print(f"Total Multimodal Pipeline Inference (Max):    {np.max(arr):.2f} ms")
    print(f"Total Multimodal Pipeline Inference (StdDev): {np.std(arr):.2f} ms")
    
    print("\n--- Per-Component Breakdown ---")
    print(f"1. Physiology Pipeline ({len(feature_schema['physiology_features'])} feats): Mean {np.mean(phys_latencies):.2f} ms, Median {np.median(phys_latencies):.2f} ms")
    print(f"2. Audio Pipeline ({len(feature_schema['audio_features'])} feats):      Mean {np.mean(aud_latencies):.2f} ms, Median {np.median(aud_latencies):.2f} ms")
    print(f"3. Vision Pipeline ({len(feature_schema['vision_features'])} feats):     Mean {np.mean(vis_latencies):.2f} ms, Median {np.median(vis_latencies):.2f} ms")
    print(f"4. Late Fusion Classifier (3 feats):  Mean {np.mean(fusion_latencies):.3f} ms, Median {np.median(fusion_latencies):.3f} ms")
    print("=" * 65)

if __name__ == "__main__":
    benchmark_model_inference()
