import pandas as pd
import numpy as np
import json
import os
import joblib
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

DATA_PATH = "processed/mosaic_clean.csv"
CONFIG_PATH = "processed/ml_feature_config.json"
RESULTS_DIR = "results"
MODELS_DIR = "models"
SEED = 20260811

def main():
    os.makedirs(MODELS_DIR, exist_ok=True)
    df = pd.read_csv(DATA_PATH)
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
        
    target_col = config["target"]
    phys_cols = config["physiology_features"]
    audio_cols = config["audio_features"]
    vis_cols = config["vision_features"]
    
    phys_flags = [c for c in config["availability_flags"] if "physiolog" in c or "pulse" in c]
    audio_flags = [c for c in config["availability_flags"] if "audio" in c]
    vis_flags = [c for c in config["availability_flags"] if "video" in c]
    
    phys_all = list(dict.fromkeys(phys_cols + phys_flags))
    audio_all = list(dict.fromkeys(audio_cols + audio_flags))
    vis_all = list(dict.fromkeys(vis_cols + vis_flags))
    
    X_phys = df[phys_all].select_dtypes(include=[np.number])
    X_aud = df[audio_all].select_dtypes(include=[np.number])
    X_vis = df[vis_all].select_dtypes(include=[np.number])
    
    y = df[target_col].values
    
    print("Training full final models...")
    model_phys = Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler()), ('clf', LogisticRegression(random_state=SEED, max_iter=1000))])
    model_aud = Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler()), ('clf', LogisticRegression(random_state=SEED, max_iter=1000))])
    model_vis = Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler()), ('clf', LogisticRegression(random_state=SEED, max_iter=1000))])
    
    model_phys.fit(X_phys, y)
    model_aud.fit(X_aud, y)
    model_vis.fit(X_vis, y)
    
    joblib.dump(model_phys, os.path.join(MODELS_DIR, "physiology_pipeline.joblib"))
    joblib.dump(model_aud, os.path.join(MODELS_DIR, "audio_pipeline.joblib"))
    joblib.dump(model_vis, os.path.join(MODELS_DIR, "vision_pipeline.joblib"))
    
    print("Saving feature lists...")
    feature_dict = {
        "physiology_features": X_phys.columns.tolist(),
        "audio_features": X_aud.columns.tolist(),
        "vision_features": X_vis.columns.tolist()
    }
    with open(os.path.join(MODELS_DIR, "model_features.json"), "w") as f:
        json.dump(feature_dict, f, indent=4)
        
    print("Training full fusion model...")
    fusion_oof = pd.read_csv(os.path.join(RESULTS_DIR, "fusion_oof_predictions.csv"))
    X_fusion = np.column_stack([
        fusion_oof["physiology_probability"],
        fusion_oof["audio_probability"],
        fusion_oof["vision_probability"]
    ])
    model_fusion = LogisticRegression(random_state=SEED)
    model_fusion.fit(X_fusion, y)
    
    joblib.dump(model_fusion, os.path.join(MODELS_DIR, "fusion_model.joblib"))
    
    print("Final models saved to models/")

if __name__ == "__main__":
    main()
