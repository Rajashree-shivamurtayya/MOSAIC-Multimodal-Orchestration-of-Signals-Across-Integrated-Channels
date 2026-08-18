import joblib
import json
import os
import numpy as np
import pandas as pd
from typing import Dict, Any

# Load models and features once upon import
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

phys_pipe = joblib.load(os.path.join(MODELS_DIR, "physiology_pipeline.joblib"))
aud_pipe = joblib.load(os.path.join(MODELS_DIR, "audio_pipeline.joblib"))
vis_pipe = joblib.load(os.path.join(MODELS_DIR, "vision_pipeline.joblib"))
fusion_model = joblib.load(os.path.join(MODELS_DIR, "fusion_model.joblib"))

with open(os.path.join(MODELS_DIR, "model_features.json")) as f:
    features = json.load(f)
    phys_features = features["physiology_features"]
    aud_features = features["audio_features"]
    vis_features = features["vision_features"]

def predict_trial(trial_features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict the deceptive-class probability for a single trial.
    Input must be a dictionary with feature names as keys.
    """
    def prepare_df(cols):
        data = {col: [trial_features.get(col, np.nan)] for col in cols}
        return pd.DataFrame(data)

    X_phys = prepare_df(phys_features)
    X_aud = prepare_df(aud_features)
    X_vis = prepare_df(vis_features)
    
    phys_avail = bool(trial_features.get("physiological_available", 1))
    aud_avail = bool(trial_features.get("audio_available", 1))
    vis_avail = bool(trial_features.get("video_available", 1))
    
    if phys_avail:
        phys_prob = float(phys_pipe.predict_proba(X_phys)[0, 1])
    else:
        phys_prob = 0.5
        
    if aud_avail:
        aud_prob = float(aud_pipe.predict_proba(X_aud)[0, 1])
    else:
        aud_prob = 0.5
        
    if vis_avail:
        vis_prob = float(vis_pipe.predict_proba(X_vis)[0, 1])
    else:
        vis_prob = 0.5
        
    X_fus = np.array([[phys_prob, aud_prob, vis_prob]])
    fusion_prob = float(fusion_model.predict_proba(X_fus)[0, 1])
    
    classification = "DECEPTIVE CLASS" if fusion_prob >= 0.5 else "TRUTH CLASS"
    sig_qual = trial_features.get("overall_trial_quality", "UNKNOWN")
    
    return {
        "physiology_probability": phys_prob,
        "audio_probability": aud_prob,
        "vision_probability": vis_prob,
        "fusion_probability": fusion_prob,
        "classification": classification,
        "physiology_available": phys_avail,
        "audio_available": aud_avail,
        "vision_available": vis_avail,
        "signal_quality": sig_qual,
        "model_version": "v1.1-LR-LateFusion"
    }
