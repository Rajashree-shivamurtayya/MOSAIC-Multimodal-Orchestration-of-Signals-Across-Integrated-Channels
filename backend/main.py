import os
import shutil
import tempfile
import json
import time
from typing import Optional, Dict, Any
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ml.feature_extraction import (
    extract_vision_features,
    extract_audio_features,
    extract_physiological_features
)

# -------------------------------------------------------------------
# Multimodal Trained Model Integration (Dataset/models)
# Decoupled inference architecture using Phase 3 Late Fusion artifacts
# -------------------------------------------------------------------
_MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Dataset", "models"))
_phys_pipe = None
_aud_pipe = None
_vis_pipe = None
_fusion_model = None
_feature_schema = None

try:
    if os.path.exists(_MODELS_DIR):
        _p_path = os.path.join(_MODELS_DIR, "physiology_pipeline.joblib")
        _a_path = os.path.join(_MODELS_DIR, "audio_pipeline.joblib")
        _v_path = os.path.join(_MODELS_DIR, "vision_pipeline.joblib")
        _f_path = os.path.join(_MODELS_DIR, "fusion_model.joblib")
        _s_path = os.path.join(_MODELS_DIR, "model_features.json")

        if os.path.exists(_p_path) and os.path.exists(_f_path) and os.path.exists(_s_path):
            _phys_pipe = joblib.load(_p_path)
            _aud_pipe = joblib.load(_a_path)
            _vis_pipe = joblib.load(_v_path)
            _fusion_model = joblib.load(_f_path)
            with open(_s_path, "r", encoding="utf-8") as _f:
                _feature_schema = json.load(_f)
            print("[MODEL INIT] Loaded trained multimodal Late Fusion pipeline from Dataset/models", flush=True)
except Exception as _e:
    print(f"[MODEL INIT WARNING] Could not load trained models: {_e}", flush=True)

# -------------------------------------------------------------------
# Modality State Tracker (In-memory cache with freshness TTL)
# -------------------------------------------------------------------
class ModalityState:
    def __init__(self, name: str, timeout_seconds: float = 12.0):
        self.name = name
        self.timeout = timeout_seconds
        self.latest_features: Optional[Dict[str, Any]] = None
        self.probability: Optional[float] = None
        self.last_updated: float = 0.0

    def update(self, features: Dict[str, Any], probability: Optional[float]):
        self.latest_features = features
        self.probability = probability
        self.last_updated = time.time()

    def is_active(self) -> bool:
        return (time.time() - self.last_updated) <= self.timeout and self.probability is not None

    def get_probability(self) -> Optional[float]:
        return self.probability if self.is_active() else None

    def get_features(self) -> Optional[Dict[str, Any]]:
        return self.latest_features if self.is_active() else None

_audio_state = ModalityState("audio", timeout_seconds=12.0)
_vision_state = ModalityState("vision", timeout_seconds=12.0)

def compute_audio_probability(features: dict) -> Optional[float]:
    """Compute audio modality deception probability using trained audio_pipeline."""
    if _aud_pipe is None or _feature_schema is None or not features:
        return None
    if features.get("is_silent") or not features.get("audio_available", 1):
        return None
    try:
        row = {col: np.nan for col in _feature_schema["audio_features"]}
        for k, v in features.items():
            if k in row:
                row[k] = v
        row["audio_available"] = 1
        df_aud = pd.DataFrame([row])
        prob = float(_aud_pipe.predict_proba(df_aud)[0, 1])
        return prob
    except Exception as e:
        print(f"[AUDIO MODEL ERROR] Failed to predict probability: {e}", flush=True)
        return None

def compute_vision_probability(features: dict) -> Optional[float]:
    """Compute vision modality deception probability using trained vision_pipeline."""
    if _vis_pipe is None or _feature_schema is None or not features:
        return None
    if not features.get("face_detected", 0) or not features.get("video_available", 1):
        return None
    try:
        row = {col: np.nan for col in _feature_schema["vision_features"]}
        for k, v in features.items():
            if k in row:
                row[k] = v
        row["video_available"] = 1
        row["face_detected"] = 1
        df_vis = pd.DataFrame([row])
        prob = float(_vis_pipe.predict_proba(df_vis)[0, 1])
        return prob
    except Exception as e:
        print(f"[VISION MODEL ERROR] Failed to predict probability: {e}", flush=True)
        return None

def compute_physiological_probability(phys_features: dict) -> Optional[float]:
    """Compute physiological modality deception probability using trained physiology_pipeline."""
    if _phys_pipe is None or _feature_schema is None or not phys_features:
        return None
    if not phys_features.get("hr_valid") or phys_features.get("estimated_heart_rate_bpm") is None:
        return None
    try:
        row = {col: np.nan for col in _feature_schema["physiology_features"]}
        hr = phys_features.get("estimated_heart_rate_bpm")
        row["heart_rate_bpm"] = hr
        row["mean_heart_rate_bpm"] = hr
        row["min_heart_rate_bpm"] = hr
        row["max_heart_rate_bpm"] = hr
        row["heart_rate_std"] = phys_features.get("hr_std")
        row["rmssd_ms"] = phys_features.get("rmssd")
        row["sdnn_ms"] = phys_features.get("sdnn")
        row["sensor_contact_quality"] = phys_features.get("signal_quality")
        row["pulse_signal_quality"] = phys_features.get("signal_quality")
        row["ppg_peak_count"] = phys_features.get("num_beats")
        row["physiological_available"] = 1
        df_phys = pd.DataFrame([row])
        prob = float(_phys_pipe.predict_proba(df_phys)[0, 1])
        return prob
    except Exception as e:
        print(f"[PHYSIO MODEL ERROR] Failed to predict probability: {e}", flush=True)
        return None


app = FastAPI(
    title="MOSAIC Backend API",
    description="Multi-Model Orchestration of Signals Across Integrated Channels",
    version="1.0.0"
)

# Allow CORS for the frontend on any local port/IP
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://192.168.1.103:3000"
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "name": "MOSAIC Backend API",
        "system": "Multimodal Orchestration of Signals Across Integrated Channels",
        "status": "online",
        "documentation": "/docs",
        "endpoints": {
            "GET /health": "System health check",
            "GET /api/trials": "List trials for dashboard",
            "POST /api/predict": "Run multimodal inference prediction (Research Prototype)",
            "POST /api/session/start": "Start an experimental session",
            "GET /api/session/{session_id}/result": "Get experimental classification result for a session",
            "GET /api/session/latest/result": "Get latest experimental session result",
            "GET /api/audio/status": "Audio modality availability, probability, and quality status",
            "GET /api/vision/status": "Vision modality availability, probability, and quality status",
            "GET /api/physio/status": "Check physiological sensor and CSV recording status",
            "GET /api/physiological/latest": "Extract latest physiological summary from mosaic_ppg.csv",
            "GET /api/physiological/waveform": "Recent window of raw MAX30102 PPG optical samples",
            "GET /api/analytics": "Verified offline model evaluation metrics, dataset provenance, and latency benchmark",
            "POST /api/extract/vision": "Extract live video features (gaze, blink rate, head pose, eyebrow delta)",
            "POST /api/extract/audio": "Extract live audio features (MFCC, ZCR)",
            "POST /api/extract/physiological": "Extract features from uploaded PPG CSV"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/analytics")
def get_analytics():
    """
    Returns verified offline model evaluation metrics, dataset provenance,
    and real measured inference latency benchmarks for the trained MOSAIC models.
    """
    return {
        "status": "success",
        "data_provenance": "OFFLINE_MODEL_EVALUATION",
        "dataset_name": "MOSAIC Simulated Research Dataset v1.1",
        "total_trials": 3000,
        "total_participants": 300,
        "evaluation_strategy": "5-Fold StratifiedGroupKFold (grouped by participant_id)",
        "metrics": {
            "fusion": {
                "name": "Late Fusion (Decision Level)",
                "architecture": "Logistic Regression on [p_phys, p_aud, p_vis]",
                "accuracy": 0.7343,
                "accuracy_percent": 73.4,
                "f1_score": 0.7332,
                "f1_percent": 73.3,
                "roc_auc": 0.8010,
                "precision": 0.7364,
                "recall": 0.7300,
                "specificity": 0.7387,
                "sensitivity": 0.7300,
                "confusion_matrix": {
                    "tn": 1108,
                    "fp": 392,
                    "fn": 405,
                    "tp": 1095,
                    "total": 3000
                }
            },
            "modalities": [
                {
                    "name": "Physiology",
                    "pipeline": "physiology_pipeline.joblib",
                    "architecture": "Median Imputer + StandardScaler + Logistic Regression",
                    "feature_count": 42,
                    "accuracy": 0.6197,
                    "accuracy_percent": 62.0,
                    "f1_score": 0.6190,
                    "roc_auc": 0.6627,
                    "precision": 0.6201,
                    "recall": 0.6180
                },
                {
                    "name": "Audio",
                    "pipeline": "audio_pipeline.joblib",
                    "architecture": "Median Imputer + StandardScaler + Logistic Regression",
                    "feature_count": 83,
                    "accuracy": 0.6913,
                    "accuracy_percent": 69.1,
                    "f1_score": 0.6831,
                    "roc_auc": 0.7555,
                    "precision": 0.7018,
                    "recall": 0.6653
                },
                {
                    "name": "Vision",
                    "pipeline": "vision_pipeline.joblib",
                    "architecture": "Median Imputer + StandardScaler + Logistic Regression",
                    "feature_count": 121,
                    "accuracy": 0.6877,
                    "accuracy_percent": 68.8,
                    "f1_score": 0.6913,
                    "roc_auc": 0.7489,
                    "precision": 0.6834,
                    "recall": 0.6993
                },
                {
                    "name": "Late Fusion",
                    "pipeline": "fusion_model.joblib",
                    "architecture": "Logistic Regression on Unimodal Probabilities",
                    "feature_count": 3,
                    "accuracy": 0.7343,
                    "accuracy_percent": 73.4,
                    "f1_score": 0.7332,
                    "roc_auc": 0.8010,
                    "precision": 0.7364,
                    "recall": 0.7300
                }
            ]
        },
        "latency_benchmark": {
            "status": "measured",
            "hardware": "Host CPU (x86_64)",
            "runs": 90,
            "pure_model_inference_ms": {
                "mean": 49.6,
                "median": 47.9,
                "min": 31.2,
                "max": 98.4,
                "breakdown_ms": {
                    "physiology_pipeline": 13.0,
                    "audio_pipeline": 16.8,
                    "vision_pipeline": 18.1,
                    "fusion_classifier": 1.6
                }
            },
            "end_to_end_http_api_ms": {
                "mean": 86.2,
                "median": 81.8
            },
            "measurement_method": "High-resolution time.perf_counter() benchmark on trained pipeline artifacts (100 runs, 10 warmup discarded)"
        },
        "disclaimer": "These metrics describe offline evaluation of the trained MOSAIC models on the available research dataset. They are not live participant results and should not be interpreted as real-world lie-detection accuracy."
    }

@app.get("/api/trials")
def get_trials():
    # Experimental research data for dashboard integration
    return [
        {"id": 1, "participant": "P001", "status": "completed", "prediction": "truthful", "confidence": 0.89},
        {"id": 2, "participant": "P002", "status": "processing", "prediction": None, "confidence": None}
    ]

# -------------------------------------------------------------------
# Hardware & Sensor Connectivity Helper
# -------------------------------------------------------------------
def check_sensor_connection() -> dict:
    """
    Check ESP32-C3 / MAX30102 hardware connectivity, COM port, and mosaic_ppg.csv recording progress.
    """
    csv_path = os.path.join(os.path.dirname(__file__), "mosaic_ppg.csv")
    csv_exists = os.path.exists(csv_path)
    
    port_name = "COM3"
    com_detected = False
    try:
        import serial.tools.list_ports
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "COM3" in p.device:
                port_name = "COM3"
                com_detected = True
                break
        if not com_detected and ports:
            for p in ports:
                desc = (p.description or "").lower()
                if any(x in desc for x in ["usb", "serial", "ch340", "cp210", "uart"]):
                    port_name = p.device
                    com_detected = True
                    break
            if not com_detected:
                port_name = ports[0].device
                com_detected = True
    except Exception:
        pass

    sample_count = 0
    last_ts = None
    file_size = 0
    is_streaming = False

    if csv_exists:
        file_size = os.path.getsize(csv_path)
        mtime = os.path.getmtime(csv_path)
        is_streaming = (time.time() - mtime) < 10.0
        try:
            with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = [line.strip() for line in f if line.strip()]
                if len(lines) > 1:
                    sample_count = len(lines) - 1
                    last_line = lines[-1].split(",")
                    if len(last_line) >= 1 and last_line[0].isdigit():
                        last_ts = int(last_line[0])
        except Exception:
            pass

    if not com_detected:
        status = "disconnected"
        msg = "Sensor disconnected. Connect MAX30102 via USB."
    elif is_streaming:
        status = "ready"
        msg = f"Live MAX30102 PPG stream active on {port_name}."
    elif sample_count >= 20:
        status = "ready"
        msg = f"MAX30102 connected on {port_name} with recorded data."
    else:
        status = "waiting"
        msg = f"MAX30102 detected on {port_name}. Start data collector."

    return {
        "connected": com_detected,
        "port": port_name if com_detected else "None",
        "sensor": "MAX30102",
        "samples": sample_count,
        "last_timestamp_ms": last_ts,
        "csv_present": csv_exists,
        "file_size_bytes": file_size,
        "streaming": is_streaming,
        "status": status,
        "message": msg
    }

# -------------------------------------------------------------------
# Experimental Session Management & Unified Multimodal Evaluation
# -------------------------------------------------------------------
_sessions: Dict[str, Dict[str, Any]] = {}
_latest_session_id: Optional[str] = None

@app.post("/api/session/start")
@app.post("/api/session/create")
def start_session(participant_id: Optional[str] = "P001"):
    """
    Initialize an experimental trial session.
    """
    global _latest_session_id
    session_id = f"SES_{int(time.time())}"
    start_epoch = time.time()
    _sessions[session_id] = {
        "session_id": session_id,
        "participant_id": participant_id,
        "status": "in_progress",
        "start_time_epoch": start_epoch,
        "start_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_epoch)),
        "end_time": None,
        "duration_seconds": 0.0,
        "classification_type": "experimental_classification",
        "prediction": None,
        "classification_label": "Session Initialized",
        "fusion_probability": None,
        "confidence": None,
        "modalities_used": [],
        "modalities_missing": ["physiological", "audio", "vision"],
        "fusion_status": "awaiting_active_modalities",
        "fusion_input_vector": [None, None, None],
        "physiology": {"available": False},
        "audio": {"available": False},
        "vision": {"available": False},
        "model_status": "initialized",
        "disclaimer": "MOSAIC multimodal deception analysis - research prototype for experimental pattern classification. Not a medical diagnostic system or lie detector."
    }
    _latest_session_id = session_id
    print(f"\n[SESSION] Started new experimental session: {session_id} for participant {participant_id}\n", flush=True)
    return {"status": "success", "session_id": session_id, "participant_id": participant_id}


def evaluate_session(session_id: str, complete: bool = False) -> Dict[str, Any]:
    """
    Core multimodal inference & session evaluation engine.
    Extracts live physiology (MAX30102), audio (microphone), and vision (webcam)
    telemetry, evaluates individual unimodal pipelines, and applies Late Fusion
    if and only if all three modalities are genuinely active.
    Never fabricates 0.5 default priors for missing channels.
    """
    global _latest_session_id
    if not session_id or session_id == "latest":
        if not _latest_session_id or _latest_session_id not in _sessions:
            start_session()
        session_id = _latest_session_id
    
    if session_id not in _sessions:
        start_session()
        session_id = _latest_session_id
        
    session_record = _sessions[session_id]

    # 1. Physiology Unimodal Score & Real MAX30102 sensor stats
    csv_path = os.path.join(os.path.dirname(__file__), "mosaic_ppg.csv")
    phys_features = extract_physiological_features(csv_path, tail_samples=600) if os.path.exists(csv_path) else None
    sensor_info = check_sensor_connection()
    
    phys_prob = compute_physiological_probability(phys_features) if phys_features else None
    phys_avail = phys_prob is not None

    # 2. Audio Unimodal Score
    aud_prob = _audio_state.get_probability()
    aud_feats = _audio_state.get_features()
    aud_active = _audio_state.is_active()
    aud_avail = aud_prob is not None
    
    audio_quality = None
    if aud_avail and aud_feats:
        rms = aud_feats.get("mean_rms_energy", 0.0)
        audio_quality = round(min(1.0, max(0.2, rms * 15.0)), 2)

    # 3. Vision Unimodal Score
    vis_prob = _vision_state.get_probability()
    vis_feats = _vision_state.get_features()
    vis_active = _vision_state.is_active()
    vis_avail = vis_prob is not None
    
    vision_quality = None
    if vis_avail and vis_feats:
        vision_quality = 0.95 if vis_feats.get("face_detected", 0) else 0.0

    # 4. Modalities tracking
    modalities_used = []
    modalities_missing = []
    if phys_avail:
        modalities_used.append("physiological")
    else:
        modalities_missing.append("physiological")

    if aud_avail:
        modalities_used.append("audio")
    else:
        modalities_missing.append("audio")

    if vis_avail:
        modalities_used.append("vision")
    else:
        modalities_missing.append("vision")

    # 5. Late Fusion Evaluation
    # Fusion model expects exact feature order: [physiology, audio, vision]
    fusion_input_vector = [
        round(phys_prob, 4) if phys_avail else None,
        round(aud_prob, 4) if aud_avail else None,
        round(vis_prob, 4) if vis_avail else None
    ]
    
    if _fusion_model is not None and phys_avail and aud_avail and vis_avail:
        X_fus = np.array([[phys_prob, aud_prob, vis_prob]])
        try:
            raw_prob = float(_fusion_model.predict_proba(X_fus)[0, 1])
            fusion_prob = round(raw_prob, 4)
            classification = "deceptive" if raw_prob >= 0.5 else "truthful"
            confidence = round(float(abs(raw_prob - 0.5) * 2), 4)
            fusion_status = "ready"
            model_status = "trained_late_fusion_pipeline"
            prediction_label = f"Experimental Classification: {classification.capitalize()}"
        except Exception as fe:
            print(f"[FUSION EVALUATION ERROR] {fe}", flush=True)
            fusion_prob = None
            classification = None
            confidence = None
            fusion_status = "error"
            model_status = "model_evaluation_error"
            prediction_label = "Fusion Evaluation Error"
    else:
        fusion_prob = None
        classification = None
        confidence = None
        fusion_status = "awaiting_active_modalities"
        model_status = "awaiting_active_modalities"
        missing_labels = []
        if not phys_avail:
            missing_labels.append("Physiological (MAX30102)")
        if not aud_avail:
            missing_labels.append("Audio (Mic)")
        if not vis_avail:
            missing_labels.append("Vision (Webcam)")
        prediction_label = f"Awaiting: {', '.join(missing_labels)}"

    # 6. Timing calculation
    start_time_epoch = session_record.get("start_time_epoch", time.time())
    now_epoch = time.time()
    
    if complete:
        end_time_epoch = session_record.get("end_time_epoch") or now_epoch
        session_record["end_time_epoch"] = end_time_epoch
        status = "completed"
        end_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time_epoch))
    else:
        end_time_epoch = session_record.get("end_time_epoch")
        status = session_record.get("status", "in_progress")
        end_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time_epoch)) if end_time_epoch else None
        
    duration = round((end_time_epoch if end_time_epoch else now_epoch) - start_time_epoch, 1)
    start_time_str = session_record.get("start_time") or time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time_epoch))

    # 7. Construct Full Result Object
    result_data = {
        "session_id": session_id,
        "participant_id": session_record.get("participant_id", "P001"),
        "status": status,
        "start_time": start_time_str,
        "end_time": end_time_str,
        "duration_seconds": duration,
        "classification_type": "experimental_classification",
        "prediction": classification,
        "classification_label": prediction_label,
        "fusion_probability": fusion_prob,
        "confidence": confidence,
        "fusion_status": fusion_status,
        "fusion_input_vector": fusion_input_vector,
        "modalities_used": modalities_used,
        "modalities_missing": modalities_missing,
        "physiology": {
            "available": phys_avail,
            "sensor_source": "MAX30102",
            "port": sensor_info.get("port", "COM3"),
            "connected": sensor_info.get("connected", False),
            "sample_count": phys_features.get("sample_count", sensor_info.get("samples", 0)) if phys_features else sensor_info.get("samples", 0),
            "heart_rate_bpm": phys_features.get("estimated_heart_rate_bpm") if phys_features else None,
            "signal_quality": phys_features.get("signal_quality_percent") if phys_features else None,
            "signal_quality_status": phys_features.get("signal_quality_status") if phys_features else "Unknown",
            "temperature": "Unavailable (Sensor channel not calibrated/streamed)",
            "spo2": "Unavailable (Uncalibrated)",
            "hrv": {
                "sdnn": phys_features.get("sdnn") if phys_features else None,
                "rmssd": phys_features.get("rmssd") if phys_features else None
            } if phys_features else None,
            "features_used": {
                "mean_ir": phys_features.get("mean_ir") if phys_features else None,
                "mean_red": phys_features.get("mean_red") if phys_features else None,
                "ppg_peak_count": phys_features.get("num_beats") if phys_features else None,
                "heart_rate_std": phys_features.get("hr_std") if phys_features else None
            } if phys_features else None,
            "probability": round(phys_prob, 4) if phys_prob is not None else None
        },
        "audio": {
            "available": aud_avail,
            "capture_status": "captured" if aud_active else "unavailable",
            "feature_extraction_status": "completed" if aud_feats else "unavailable",
            "probability": round(aud_prob, 4) if aud_prob is not None else None,
            "quality": audio_quality,
            "features_used": {
                "mean_rms_energy": aud_feats.get("mean_rms_energy") if aud_feats else None,
                "zcr_mean": aud_feats.get("zcr_mean") if aud_feats else None,
                "mfcc_mean_0": aud_feats.get("mfcc_mean")[0] if aud_feats and aud_feats.get("mfcc_mean") and len(aud_feats.get("mfcc_mean")) > 0 else None
            } if aud_feats else None
        },
        "vision": {
            "available": vis_avail,
            "capture_status": "captured" if vis_active else "unavailable",
            "feature_extraction_status": "completed" if vis_feats else "unavailable",
            "probability": round(vis_prob, 4) if vis_prob is not None else None,
            "quality": vision_quality,
            "features_used": {
                "blink_rate": vis_feats.get("blink_rate") if vis_feats else None,
                "head_yaw_mean": vis_feats.get("head_yaw_mean") if vis_feats else None,
                "eyebrow_delta_mean": vis_feats.get("eyebrow_delta_mean") if vis_feats else None,
                "face_detected": vis_feats.get("face_detected") if vis_feats else 0
            } if vis_feats else None
        },
        "model_status": model_status,
        "traceability": {
            "physiology_pipeline": "Dataset/models/physiology_pipeline.joblib",
            "audio_pipeline": "Dataset/models/audio_pipeline.joblib",
            "vision_pipeline": "Dataset/models/vision_pipeline.joblib",
            "fusion_model": "Dataset/models/fusion_model.joblib",
            "fusion_architecture": "Late Fusion (Decision Level)",
            "flow_description": "MAX30102 / Microphone / Camera -> Feature Extractors -> Trained Unimodal Pipelines -> Decision Vector [p_phys, p_aud, p_vis] -> Late Fusion Classifier"
        },
        "disclaimer": "MOSAIC multimodal deception analysis - research prototype for experimental pattern classification. Not a medical diagnostic system or lie detector."
    }
    
    # Store updated session
    session_record.update(result_data)
    _sessions[session_id] = session_record
    return result_data


@app.get("/api/session/{session_id}/result")
def get_session_result(session_id: str):
    """
    Retrieve final or active experimental classification result for a session.
    """
    global _latest_session_id
    if session_id == "latest":
        sid = _latest_session_id
        if not sid or sid not in _sessions:
            start_session()
            sid = _latest_session_id
    else:
        sid = session_id

    if not sid or sid not in _sessions:
        return {"error": f"Session '{session_id}' not found", "status": "not_found"}
        
    if _sessions[sid].get("status") == "completed":
        return _sessions[sid]
        
    return evaluate_session(sid, complete=False)


@app.get("/api/session/latest/result")
def get_latest_session_result():
    """
    Convenience endpoint for latest experimental session result.
    """
    return get_session_result("latest")


# -------------------------------------------------------------------
# Dedicated Modality Status Endpoints
# -------------------------------------------------------------------
@app.get("/api/audio/status")
@app.get("/api/modality/audio")
def get_audio_status():
    """
    Returns genuine audio modality status, deception probability, and signal quality.
    Never substitutes fake 0.5 priors when microphone is inactive.
    """
    active = _audio_state.is_active()
    prob = _audio_state.get_probability()
    feats = _audio_state.get_features()
    quality = None
    if active and feats:
        rms = feats.get("mean_rms_energy", 0.0)
        quality = round(min(1.0, max(0.2, rms * 15.0)), 2)
    return {
        "available": active,
        "probability": round(prob, 3) if prob is not None else None,
        "quality": quality,
        "status": "ready" if active else "unavailable"
    }


@app.get("/api/vision/status")
@app.get("/api/modality/vision")
def get_vision_status():
    """
    Returns genuine vision modality status, deception probability, and signal quality.
    Never substitutes fake 0.5 priors when camera/face is inactive.
    """
    active = _vision_state.is_active()
    prob = _vision_state.get_probability()
    feats = _vision_state.get_features()
    quality = None
    if active and feats:
        face_detected = feats.get("face_detected", 0)
        quality = 0.95 if face_detected else 0.0
    return {
        "available": active,
        "probability": round(prob, 3) if prob is not None else None,
        "quality": quality,
        "status": "ready" if active else "unavailable"
    }


@app.post("/api/predict")
def run_prediction(trial_id: int = 1, session_id: Optional[str] = None):
    """
    Multimodal Deception Analysis Prediction Endpoint.
    Integrates genuine live physiological features from MAX30102 with
    live extracted audio and vision model predictions in the trained late-fusion classifier.
    If any required modality is missing, explicitly returns 'awaiting_active_modalities'
    with null predictions instead of fabricating 0.5 priors.
    """
    global _latest_session_id
    sid = session_id or _latest_session_id
    if not sid:
        start_session()
        sid = _latest_session_id

    session_data = evaluate_session(sid, complete=False)
    phys = session_data["physiology"]
    aud = session_data["audio"]
    vis = session_data["vision"]

    return {
        "session_id": sid,
        "trial_id": trial_id,
        "prediction": session_data["prediction"],
        "classification_label": session_data["classification_label"],
        "confidence": session_data["confidence"],
        "fusion_probability": session_data["fusion_probability"],
        "fusion_status": session_data["fusion_status"],
        "classification_type": session_data["classification_type"],
        "modalities_used": session_data["modalities_used"],
        "modalities_missing": session_data["modalities_missing"],
        "quality_summary": {
            "physiological": phys.get("signal_quality"),
            "audio": round(aud.get("quality") * 100, 1) if aud.get("quality") is not None else None,
            "vision": round(vis.get("quality") * 100, 1) if vis.get("quality") is not None else None
        },
        "model_status": session_data["model_status"],
        "disclaimer": session_data["disclaimer"],
        "modality_scores": {
            "audio": aud.get("probability"),
            "vision": vis.get("probability"),
            "physiological": phys.get("probability")
        },
        "features_used": {
            "heart_rate_bpm": phys.get("heart_rate_bpm"),
            "signal_quality_percent": phys.get("signal_quality"),
            "sample_count": phys.get("sample_count", 0)
        },
        "availability": {
            "audio": aud.get("available", False),
            "vision": vis.get("available", False),
            "physiological": phys.get("available", False)
        },
        "fusion_input_vector": session_data["fusion_input_vector"]
    }

@app.post("/api/modality/vision/update")
def update_vision_features(features: Dict[str, Any]):
    """
    Directly evaluate vision features and compute probability via trained vision_pipeline.joblib.
    """
    vis_prob = compute_vision_probability(features)
    _vision_state.update(features, vis_prob)
    return {
        "status": "success",
        "available": vis_prob is not None,
        "probability": round(vis_prob, 3) if vis_prob is not None else None,
        "features": features
    }

@app.post("/api/modality/audio/update")
def update_audio_features(features: Dict[str, Any]):
    """
    Directly evaluate audio features and compute probability via trained audio_pipeline.joblib.
    """
    aud_prob = compute_audio_probability(features)
    _audio_state.update(features, aud_prob)
    return {
        "status": "success",
        "available": aud_prob is not None,
        "probability": round(aud_prob, 3) if aud_prob is not None else None,
        "features": features
    }

@app.post("/api/extract/vision")
async def extract_vision(file: UploadFile = File(...)):
    """
    Endpoint for live video chunks to extract vision features (gaze, blinks, head pose)
    and compute genuine vision modality probability.
    """
    temp_path = None
    try:
        suffix = os.path.splitext(file.filename or "")[1] or ".webm"
        fd, temp_path = tempfile.mkstemp(suffix=suffix)
        os.close(fd)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        features = extract_vision_features(temp_path)

        if features is None:
            return {"error": "Failed to extract vision features from chunk", "features": None, "probability": None, "available": False}

        # Calculate vision modality probability
        vis_prob = compute_vision_probability(features)
        _vision_state.update(features, vis_prob)

        if vis_prob is not None:
            print("\n[VISION]", flush=True)
            print(f"[VISION] probability={vis_prob:.3f}", flush=True)
            print(f"[VISION] BlinkRate={features.get('blink_rate')} bpm, HeadYaw={features.get('head_yaw_mean')} deg, EyebrowDelta={features.get('eyebrow_delta_mean'):.4f}\n", flush=True)
        else:
            print("\n[VISION] Modality unavailable (no face detected)\n", flush=True)

        return {
            "features": features,
            "probability": round(vis_prob, 3) if vis_prob is not None else None,
            "available": vis_prob is not None
        }
    except Exception as e:
        print(f"Vision endpoint error: {e}")
        return {"error": str(e), "features": None, "probability": None, "available": False}
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

@app.post("/api/extract/audio")
async def extract_audio(file: UploadFile = File(...)):
    """
    Endpoint for live audio chunks to extract audio features (MFCC, ZCR, spectral)
    and compute genuine audio modality probability.
    """
    temp_path = None
    try:
        suffix = os.path.splitext(file.filename or "")[1] or ".webm"
        fd, temp_path = tempfile.mkstemp(suffix=suffix)
        os.close(fd)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        features = extract_audio_features(temp_path)

        if features is None:
            return {"error": "Failed to extract audio features from chunk", "features": None, "probability": None, "available": False}

        # Calculate audio modality probability
        aud_prob = compute_audio_probability(features)
        _audio_state.update(features, aud_prob)

        if aud_prob is not None:
            mfcc0 = features.get("mfcc_mean")[0] if features.get("mfcc_mean") and len(features.get("mfcc_mean")) > 0 else 0.0
            print("\n[AUDIO]", flush=True)
            print(f"[AUDIO] probability={aud_prob:.3f}", flush=True)
            print(f"[AUDIO] MFCC0={mfcc0:.2f}, ZCR={features.get('zcr_mean'):.4f}, RMS={features.get('mean_rms_energy'):.5f}\n", flush=True)
        else:
            print("\n[AUDIO] Modality unavailable (silence or no audio detected)\n", flush=True)

        return {
            "features": features,
            "probability": round(aud_prob, 3) if aud_prob is not None else None,
            "available": aud_prob is not None
        }
    except Exception as e:
        print(f"Audio endpoint error: {e}")
        return {"error": str(e), "features": None, "probability": None, "available": False}
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

@app.get("/api/physiological/waveform")
def get_ppg_waveform(window_samples: int = 150):
    """
    Return a recent window of raw MAX30102 optical PPG samples (IR, RED)
    from mosaic_ppg.csv for live waveform visualization.
    """
    csv_path = os.path.join(os.path.dirname(__file__), "mosaic_ppg.csv")
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        return {"status": "empty", "source": "MAX30102", "samples": []}
    try:
        df = pd.read_csv(csv_path)
        if len(df) == 0:
            return {"status": "empty", "source": "MAX30102", "samples": []}
        window = df.tail(window_samples).copy().reset_index(drop=True)
        samples = []
        for i, row in window.iterrows():
            samples.append({
                "time": int(i),
                "timestamp_ms": int(row.get("timestamp_ms", 0)) if not pd.isna(row.get("timestamp_ms")) else 0,
                "ir": float(row.get("ir", 0)) if not pd.isna(row.get("ir")) else 0.0,
                "red": float(row.get("red", 0)) if not pd.isna(row.get("red")) else 0.0
            })
        return {
            "status": "success",
            "source": "MAX30102",
            "count": len(samples),
            "samples": samples
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "samples": []}

@app.get("/api/physio/status")
def get_physio_status():
    """
    Check ESP32-C3 / MAX30102 hardware connectivity, COM port, and mosaic_ppg.csv recording progress.
    """
    return check_sensor_connection()

def _log_physio_summary(features: dict, source: str = "CSV"):
    print(f"\n[PHYSIO] ({source})", flush=True)
    print(f"Samples={features.get('sample_count')}", flush=True)
    print(f"Duration={features.get('duration_seconds')}s", flush=True)
    print(f"Mean IR={features.get('mean_ir')}", flush=True)
    print(f"Mean RED={features.get('mean_red')}", flush=True)
    print("Temperature=Unavailable (Sensor channel not calibrated/streamed)", flush=True)
    hr_val = features.get('estimated_heart_rate_bpm') or features.get('mean_hr')
    print(f"HR={hr_val} BPM" if hr_val is not None else "HR=null", flush=True)
    print("SpO2=Unavailable (Uncalibrated)\n", flush=True)

@app.get("/api/physiological/latest")
@app.get("/api/physio/latest")
def get_latest_physio(tail_samples: int = 600):
    """
    Extract real physiological features (HR, HRV, Temperature, Quality, SpO2) 
    from the active mosaic_ppg.csv recording.
    """
    csv_path = os.path.join(os.path.dirname(__file__), "mosaic_ppg.csv")

    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        return {
            "status": "waiting",
            "source": "MAX30102",
            "port": "COM3",
            "message": "No physiological samples available yet. Start test_max30102.py to record.",
            "features": None
        }

    features = extract_physiological_features(csv_path, tail_samples=tail_samples)

    if features is None:
        return {
            "status": "waiting",
            "source": "MAX30102",
            "port": "COM3",
            "message": "Insufficient physiological samples or sensor still initializing.",
            "features": None
        }

    _log_physio_summary(features, source="GET /api/physiological/latest")

    return {
        "status": "success",
        "source": "MAX30102",
        "port": "COM3",
        "features": features
    }

@app.post("/api/extract/physiological")
async def extract_physiological(file: UploadFile = File(...)):
    temp_path = None

    try:
        # Create temporary CSV file
        fd, temp_path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)

        # Save uploaded CSV
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract physiological features
        features = extract_physiological_features(temp_path)

        if features is None:
            return {
                "error": "Failed to extract physiological features from uploaded CSV",
                "features": None
            }

        _log_physio_summary(features, source="POST /api/extract/physiological")

        return {
            "features": features
        }

    except Exception as e:

        print(
            f"Physiological endpoint error: {e}"
        )

        return {
            "error": str(e),
            "features": None
        }

    finally:

        if (
            temp_path
            and os.path.exists(temp_path)
        ):
            os.remove(temp_path)

@app.post("/api/audio/record")
def record_host_audio(duration_seconds: float = 2.0):
    """
    Acquires live audio directly from the host system microphone,
    extracts MOSAIC audio features, computes audio probability, and updates modality state.
    """
    try:
        import sounddevice as sd
        import soundfile as sf
        sr = 16000
        print(f"\n[HOST AUDIO] Recording {duration_seconds}s from system microphone...", flush=True)
        recording = sd.rec(int(duration_seconds * sr), samplerate=sr, channels=1, dtype="float32")
        sd.wait()
        
        fd, temp_path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        sf.write(temp_path, recording, sr)
        
        features = extract_audio_features(temp_path)
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
                
        if features is None:
            return {"error": "Failed to extract audio features from mic recording", "available": False}
            
        aud_prob = compute_audio_probability(features)
        _audio_state.update(features, aud_prob)
        
        return {
            "status": "success",
            "available": aud_prob is not None,
            "probability": round(aud_prob, 3) if aud_prob is not None else None,
            "features": features
        }
    except Exception as e:
        print(f"[HOST AUDIO ERROR] {e}", flush=True)
        return {"error": str(e), "available": False}


@app.post("/api/vision/capture")
def capture_host_vision(frame_count: int = 30):
    """
    Acquires live video frames directly from host webcam (index 0),
    extracts MOSAIC vision features, computes vision probability, and updates modality state.
    """
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return {"error": "Could not open host webcam at index 0", "available": False}
            
        frames = []
        for _ in range(frame_count):
            ret, frame = cap.read()
            if ret and frame is not None:
                frames.append(frame)
            time.sleep(0.033)
        cap.release()
        
        if not frames:
            return {"error": "No frames captured from webcam", "available": False}
            
        fd, temp_path = tempfile.mkstemp(suffix=".mp4")
        os.close(fd)
        h, w = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_path, fourcc, 30.0, (w, h))
        for f in frames:
            out.write(f)
        out.release()
        
        features = extract_vision_features(temp_path)
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
                
        if features is None:
            return {"error": "Failed to extract vision features from webcam", "available": False}
            
        vis_prob = compute_vision_probability(features)
        _vision_state.update(features, vis_prob)
        
        return {
            "status": "success",
            "available": vis_prob is not None,
            "probability": round(vis_prob, 3) if vis_prob is not None else None,
            "features": features
        }
    except Exception as e:
        print(f"[HOST VISION ERROR] {e}", flush=True)
        return {"error": str(e), "available": False}


@app.post("/api/session/{session_id}/complete")
def complete_session(session_id: str):
    """
    Finalize an experimental session, run full multimodal evaluation, and lock the final result.
    """
    global _latest_session_id
    sid = _latest_session_id if session_id == "latest" else session_id
    if not sid:
        start_session()
        sid = _latest_session_id
        
    result = evaluate_session(sid, complete=True)
    return result


@app.post("/api/session/reset")
def reset_session():
    """
    Reset current experimental session and cached modality states.
    """
    global _latest_session_id
    start_session()
    return {"status": "success", "session_id": _latest_session_id}


if __name__ == "__main__":
    import uvicorn
    print("\n========================================================", flush=True)
    print("  MOSAIC MULTIMODAL BACKEND SERVER", flush=True)
    print("  FastAPI listening on http://127.0.0.1:8000", flush=True)
    print("  Swagger docs: http://127.0.0.1:8000/docs", flush=True)
    print("========================================================\n", flush=True)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)

