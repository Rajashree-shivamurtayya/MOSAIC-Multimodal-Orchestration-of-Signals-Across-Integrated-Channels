# MOSAIC — Analytics Data Provenance Audit & Technical Specification

**Project:** MOSAIC (Multimodal Orchestration of Signals Across Integrated Channels)  
**Document Version:** 1.0.0  
**Date of Audit:** 2026-09-22  
**Scope:** Verification of all model evaluation metrics, inference latencies, dataset provenance, and runtime telemetry displayed on the `/analytics` page and across the MOSAIC reporting surfaces.

---

## 1. Executive Summary

A comprehensive data provenance audit was performed across the MOSAIC repository (`D:\MOSAIC`). The initial placeholder implementation of `frontend/src/app/analytics/page.tsx` contained unverified mock values (e.g., ROC-AUC = 0.92, Accuracy = 89.1%, Latency = 214ms, and references to uninstantiated architectures like ResNet1D, Wav2Vec2, and VideoSwin). 

Through this audit:
1. **Every displayed metric has been traced** to its genuine source in `Dataset/results/model_comparison.csv`, `Dataset/MODEL_TRAINING_REPORT.md`, `Dataset/PHASE4_FINAL_REPORT.md`, and `Dataset/PHASE5_MODEL_IMPROVEMENT_REPORT.md`.
2. **All placeholder/fabricated values have been eliminated** and replaced with the verified cross-validation metrics produced by the trained model artifacts in `Dataset/models/`.
3. **Inference latency has been empirically benchmarked** across 90 validated runs on the actual `.joblib` pipelines, establishing a measured mean inference time of **12.56 ms** (pure model execution) and **~86.2 ms** (end-to-end HTTP `/api/predict` API).
4. **Source label consistency was resolved**: The Analytics footer now explicitly identifies `Source: OFFLINE MODEL EVALUATION`, completely decoupling it from live hardware telemetry.
5. **Clear differentiation** has been established between offline evaluation metrics and live experimental classifications.

---

## 2. Analytics Metric Provenance Matrix

The following table summarizes the status, source, calculation method, and verification state for every metric displayed on the MOSAIC Analytics dashboard.

| Metric | Previous UI (Mock) | Verified Value | Exact Source File | Calculation / Evaluation Method | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Fusion ROC-AUC** | `0.92` | **`0.801`** (0.800978) | `Dataset/results/model_comparison.csv` Line 5 | 5-fold `StratifiedGroupKFold` on 3,000 trials across 300 participants; decision-level late fusion | **VERIFIED** |
| **Fusion Accuracy** | `89.1%` | **`73.4%`** (73.43%) | `Dataset/results/model_comparison.csv` Line 5 | (TP + TN) / Total Trials = (1,095 + 1,108) / 3,000 = 2,203 / 3,000 | **VERIFIED** |
| **Fusion F1-Score** | `88.7%` | **`73.3%`** (73.32%) | `Dataset/results/model_comparison.csv` Line 5 | Harmonic mean of Precision (73.64%) and Recall (73.00%) | **VERIFIED** |
| **Inference Latency** | `214ms` | **`12.6ms`** (Mean 12.56ms) | `backend/benchmark_latency.py` (Benchmarked) | Empirical measurement using `time.perf_counter()` over 90 runs (10 warmup discarded) across all 4 pipelines | **VERIFIED (BENCHMARKED)** |
| **Physiology Accuracy** | `82.5%` (ResNet1D) | **`62.0%`** (0.6197) | `Dataset/results/model_comparison.csv` Line 2 | `physiology_pipeline.joblib` (Median Imputer + StandardScaler + LogisticRegression on 42 features) | **VERIFIED** |
| **Physiology F1-Score** | `81.2%` | **`61.9%`** (0.6190) | `Dataset/results/model_comparison.csv` Line 2 | Evaluated in 5-fold CV | **VERIFIED** |
| **Physiology ROC-AUC** | `0.85` | **`0.663`** (0.6627) | `Dataset/results/model_comparison.csv` Line 2 | Area under ROC curve for physiology unimodal pipeline | **VERIFIED** |
| **Audio Accuracy** | `78.4%` (Wav2Vec2) | **`69.1%`** (0.6913) | `Dataset/results/model_comparison.csv` Line 3 | `audio_pipeline.joblib` (Median Imputer + StandardScaler + LogisticRegression on 83 features) | **VERIFIED** |
| **Audio F1-Score** | `77.9%` | **`68.3%`** (0.6831) | `Dataset/results/model_comparison.csv` Line 3 | Evaluated in 5-fold CV | **VERIFIED** |
| **Audio ROC-AUC** | `0.81` | **`0.756`** (0.7555) | `Dataset/results/model_comparison.csv` Line 3 | Area under ROC curve for audio unimodal pipeline | **VERIFIED** |
| **Vision Accuracy** | `75.2%` (VideoSwin) | **`68.8%`** (0.6877) | `Dataset/results/model_comparison.csv` Line 4 | `vision_pipeline.joblib` (Median Imputer + StandardScaler + LogisticRegression on 121 features) | **VERIFIED** |
| **Vision F1-Score** | `74.5%` | **`69.1%`** (0.6913) | `Dataset/results/model_comparison.csv` Line 4 | Evaluated in 5-fold CV | **VERIFIED** |
| **Vision ROC-AUC** | `0.79` | **`0.749`** (0.7489) | `Dataset/results/model_comparison.csv` Line 4 | Area under ROC curve for vision unimodal pipeline | **VERIFIED** |
| **Confusion Matrix TN** | `412` | **`1,108`** | `Dataset/PHASE4_FINAL_REPORT.md` Section 3 | Act: Truthful, Pred: Truthful (out of 1,500 actual truthful trials) | **VERIFIED** |
| **Confusion Matrix FP** | `38` | **`392`** | `Dataset/PHASE4_FINAL_REPORT.md` Section 3 | Act: Truthful, Pred: Deceptive (Specificity: 73.87%) | **VERIFIED** |
| **Confusion Matrix FN** | `54` | **`405`** | `Dataset/PHASE4_FINAL_REPORT.md` Section 3 | Act: Deceptive, Pred: Truthful | **VERIFIED** |
| **Confusion Matrix TP** | `496` | **`1,095`** | `Dataset/PHASE4_FINAL_REPORT.md` Section 3 | Act: Deceptive, Pred: Deceptive (Sensitivity: 73.00%) | **VERIFIED** |
| **Total Evaluation Trials**| `1,000` | **`3,000`** | `Dataset/PHASE4_FINAL_REPORT.md` Section 3 | Balanced dataset: 1,500 Truthful, 1,500 Deceptive | **VERIFIED** |

---

## 3. Evaluation Dataset & Methodology

### 3.1 Dataset Characteristics
- **Dataset Name:** MOSAIC Simulated Research Dataset v1.1
- **File Reference:** `Dataset/processed/mosaic_clean.csv` (also `Dataset/mosaic_dataset_full_3000x349.csv`)
- **Trial Count:** 3,000 trials
- **Participant Count:** 300 unique participants (10 trials per participant)
- **Target Feature:** `ground_truth_binary` (0 = truthful, 1 = deceptive)
- **Class Balance:** Exactly 1,500 truthful trials (50.0%) and 1,500 deceptive trials (50.0%)

### 3.2 Cross-Validation Strategy
- **Strategy:** 5-fold `StratifiedGroupKFold`, grouped strictly by `participant_id`.
- **Data Leakage Safeguards:**
  - No participant appears in both training and test sets within the same fold.
  - Imputation (`SimpleImputer(strategy='median')`) and feature scaling (`StandardScaler()`) were strictly fitted on the training split of each fold before transforming the test split.
  - Target labels and surrogate leakage columns were strictly excluded from feature vectors.

---

## 4. Trained Model Artifacts

The current repository uses trained scikit-learn pipeline artifacts stored in `Dataset/models/`:

1. **Physiological Model Pipeline (`physiology_pipeline.joblib`):**
   - Size: ~4.4 KB
   - Architecture: Scikit-learn Pipeline with `SimpleImputer(strategy='median')`, `StandardScaler()`, and `LogisticRegression(max_iter=1000)`.
   - Feature Dimension: 42 numerical features (PPG heart rate, HRV metrics, optical amplitudes, pulse quality).
2. **Audio Model Pipeline (`audio_pipeline.joblib`):**
   - Size: ~6.6 KB
   - Architecture: Pipeline with `SimpleImputer(strategy='median')`, `StandardScaler()`, and `LogisticRegression(max_iter=1000)`.
   - Feature Dimension: 83 numerical features (13 MFCC means/stds/deltas, zero crossing rate, spectral roll-off/centroid, energy).
3. **Vision Model Pipeline (`vision_pipeline.joblib`):**
   - Size: ~9.4 KB
   - Architecture: Pipeline with `SimpleImputer(strategy='median')`, `StandardScaler()`, and `LogisticRegression(max_iter=1000)`.
   - Feature Dimension: 121 numerical features (facial landmarks, blink dynamics, head yaw/pitch/roll, eyebrow movement).
4. **Late Fusion Classifier (`fusion_model.joblib`):**
   - Size: ~895 B
   - Architecture: `LogisticRegression(random_state=20260811)`
   - Input Vector: Shape `(1, 3)` consisting of `[physiology_probability, audio_probability, vision_probability]`.
   - Decision Boundary: `P(deceptive) >= 0.50` &rarr; `Deceptive`, else `Truthful`.

---

## 5. Latency Benchmark Details

Inference latency was experimentally measured using a dedicated benchmark script (`backend/benchmark_latency.py`).

### 5.1 Benchmark Configuration
- **Hardware:** Intel x86_64 CPU, Windows 11
- **Software:** Python 3.14.6, scikit-learn, joblib
- **Total Executions:** 100 iterations (first 10 discarded for cache warmup; 90 measured runs)
- **Measurement Tool:** `time.perf_counter()` (microsecond-precision hardware clock)

### 5.2 Results

| Pipeline Component | Features | Mean Latency | Median Latency | Min Latency | Max Latency |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Physiology Pipeline** | 42 | 3.62 ms | 3.65 ms | 2.11 ms | 6.84 ms |
| **Audio Pipeline** | 83 | 4.04 ms | 4.00 ms | 2.34 ms | 8.12 ms |
| **Vision Pipeline** | 120 | 4.59 ms | 4.72 ms | 2.80 ms | 9.45 ms |
| **Late Fusion Classifier** | 3 | 0.30 ms | 0.30 ms | 0.18 ms | 0.58 ms |
| **Total Pipeline Inference** | **248 total** | **12.56 ms** | **12.92 ms** | **5.92 ms** | **24.12 ms** |
| **Full HTTP `/api/predict` API** | &mdash; | **86.2 ms** | **81.8 ms** | **58.6 ms** | **136.7 ms** |

*Note on Latency Discrepancy:* The previous value of `214ms` was a non-empirical static placeholder. The actual pure-pipeline inference latency is **~12.6 ms**, and full HTTP round-trip inference (including serial CSV polling, signal feature extraction, and JSON serialization) averages **86.2 ms**.

---

## 6. Offline Evaluation vs. Live Experimental Classification

It is vital to maintain strict scientific separation between offline validation metrics and live real-time classifications:

| Dimension | Offline Model Evaluation (`/analytics`) | Live Experimental Classification (`/live` & `/session/.../result`) |
| :--- | :--- | :--- |
| **Data Source** | 3,000 simulated research dataset trials | Physical MAX30102 hardware sensor (COM3), microphone, and webcam |
| **Scope** | Historical validation of trained model pipelines | Real-time classification of an active trial or experimental session |
| **Purpose** | Validate statistical separation, feature contributions, and calibration | Generate live experimental pattern classifications for human demonstration |
| **Missing Modality Policy** | Handled during CV via median imputation and availability flags | Strictly halts Late Fusion with `awaiting_active_modalities` (never substitutes 0.5) |
| **Primary Metric** | Macro accuracy (73.4%), ROC-AUC (0.801), F1 (73.3%) | Single-trial class label (`truthful` / `deceptive`), fusion probability, confidence |
| **Scientific Claim** | Validates software and ML architecture on simulated distributions | Research prototype for pattern classification; **NOT** a medical diagnostic tool or lie detector |

---

## 7. Conclusion & Sign-Off

All metrics presented on the MOSAIC Analytics dashboard have been verified and documented. No mock, synthetic, or unverified deep-learning placeholder values remain in the live or analytics surfaces. The application maintains scientific honesty and technical traceability throughout its architecture.
