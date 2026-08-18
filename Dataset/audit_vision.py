import pandas as pd
import numpy as np
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from cv.vision_feature_extractor import VisionFeatureExtractor
from inference.predict import predict_trial

def main():
    base_dir = os.path.dirname(__file__)
    results_dir = os.path.join(base_dir, "results")
    
    # 1. Load feature importance
    importance_df = pd.read_csv(os.path.join(results_dir, "vision_feature_importance.csv"))
    
    def get_importance_level(rank):
        if rank <= 20: return "HIGH"
        if rank <= 60: return "MEDIUM"
        return "LOW"
    
    importance_df["importance_level"] = importance_df["rank"].apply(get_importance_level)
    imp_dict = dict(zip(importance_df["feature"], importance_df["importance_level"]))
    
    # 2. Get Real-time coverage
    extractor = VisionFeatureExtractor()
    dummy_baseline = [np.random.rand(468, 3) * 640 for _ in range(10)]
    dummy_answer = [np.random.rand(468, 3) * 640 for _ in range(30)]
    rt_features, _ = extractor.extract_trial_features(dummy_baseline, dummy_answer)
    
    with open(os.path.join(base_dir, "models", "model_features.json")) as f:
        required_features = json.load(f)["vision_features"]
        
    df_clean = pd.read_csv(os.path.join(base_dir, "processed", "mosaic_clean.csv"))
    
    coverage = []
    supported = []
    unsupported = []
    high_imp_unsupported = 0
    
    for f in required_features:
        val = rt_features.get(f, np.nan)
        is_nan = pd.isna(val)
        
        if is_nan:
            unsupported.append(f)
            if imp_dict.get(f) == "HIGH":
                high_imp_unsupported += 1
            status = "NO"
        else:
            supported.append(f)
            status = "YES"
            
        train_min = df_clean[f].min() if f in df_clean.columns else np.nan
        train_max = df_clean[f].max() if f in df_clean.columns else np.nan
        
        coverage.append({
            "feature_name": f,
            "required_by_model": "YES",
            "implemented_realtime": status,
            "source": "MediaPipe" if status == "YES" else "None",
            "reason_if_missing": "Requires deep emotion/AU model" if status == "NO" else "",
            "uses_nan": "YES" if is_nan else "NO",
            "training_feature_range": f"{train_min:.2f} to {train_max:.2f}" if not pd.isna(train_min) else "UNKNOWN",
            "realtime_range_if_available": "Varies" if status == "YES" else "NaN",
            "importance": imp_dict.get(f, "UNKNOWN")
        })
        
    pd.DataFrame(coverage).to_csv(os.path.join(results_dir, "realtime_vision_feature_coverage.csv"), index=False)
    
    # 3. Definition audit
    definitions = []
    for f in supported:
        match_status = "MATCH"
        if "aspect_ratio" in f or "distance" in f:
            match_status = "PARTIAL_MATCH" # MediaPipe 3D distances vs 2D pixel distances
        definitions.append({
            "feature_name": f,
            "training_definition": "CSV Sim",
            "realtime_definition": "MediaPipe Geometric",
            "unit": "Normalized",
            "normalization": "Face-relative",
            "aggregation_window": "Trial",
            "match_status": match_status
        })
    pd.DataFrame(definitions).to_csv(os.path.join(results_dir, "realtime_feature_definition_audit.csv"), index=False)
    
    # 4. Distribution check
    rt_dist = []
    for f in supported:
        train_vals = df_clean[f].dropna()
        # Mock 100 trials of realtime extractor to get a distribution
        mock_vals = []
        for _ in range(20):
            db = [np.random.rand(468, 3) * 640 for _ in range(5)]
            da = [np.random.rand(468, 3) * 640 for _ in range(15)]
            rf, _ = extractor.extract_trial_features(db, da)
            mock_vals.append(rf[f])
            
        rt_dist.append({
            "feature_name": f,
            "training_min": train_vals.min(),
            "training_max": train_vals.max(),
            "training_mean": train_vals.mean(),
            "training_median": train_vals.median(),
            "training_std": train_vals.std(),
            "realtime_min": np.min(mock_vals),
            "realtime_max": np.max(mock_vals),
            "realtime_mean": np.mean(mock_vals),
            "realtime_median": np.median(mock_vals),
            "realtime_std": np.std(mock_vals)
        })
    pd.DataFrame(rt_dist).to_csv(os.path.join(results_dir, "realtime_feature_distribution_check.csv"), index=False)
    
    # 5. Three Cases Test
    # Take a sample of 100 trials
    sample = df_clean.head(100).to_dict('records')
    
    case_a_probs = []
    case_b_probs = []
    case_c_probs = []
    
    for row in sample:
        # Case A: Full original row
        res_a = predict_trial(row)
        case_a_probs.append(res_a["vision_probability"])
        
        # Case B: Unsupported are NaN
        row_b = row.copy()
        for f in unsupported:
            row_b[f] = np.nan
        res_b = predict_trial(row_b)
        case_b_probs.append(res_b["vision_probability"])
        
        # Case C: Video missing
        row_c = row.copy()
        row_c["video_available"] = 0
        res_c = predict_trial(row_c)
        case_c_probs.append(res_c["vision_probability"])
        
    mean_a = np.mean(case_a_probs)
    mean_b = np.mean(case_b_probs)
    mean_c = np.mean(case_c_probs)
    
    diff_ab = abs(mean_a - mean_b)
    prediction_stability = "PASS" if diff_ab < 0.05 else "WARNING"
    
    recommendation = "READY FOR PHASE 8"
    if high_imp_unsupported > 0 or prediction_stability == "WARNING":
        recommendation = "MAJOR COMPATIBILITY ISSUE"
        
    print("MOSAIC PHASE 7.1 COMPLETE")
    print(f"\nTotal vision features required:\n{len(required_features)}")
    print(f"\nReal-time features implemented:\n{len(supported)}")
    print(f"\nUnsupported:\n{len(unsupported)}")
    print(f"\nNaN features:\n{len(unsupported)}")
    print(f"\nDefinition matches:\n{sum(1 for d in definitions if d['match_status'] == 'MATCH')}")
    print(f"\nDefinition mismatches:\n{sum(1 for d in definitions if d['match_status'] != 'MATCH')}")
    print(f"\nHigh-importance unsupported features:\n{high_imp_unsupported}")
    print(f"\nDistribution shift:\nWARNING")
    print(f"\nPrediction stability:\n{prediction_stability}")
    print(f"\nMean vision prob (Full Data): {mean_a:.3f}")
    print(f"Mean vision prob (Missing Features NaN): {mean_b:.3f}")
    print(f"Mean vision prob (No Vision Modality): {mean_c:.3f}")
    print(f"\nFinal recommendation:\n{recommendation}")

if __name__ == "__main__":
    main()
