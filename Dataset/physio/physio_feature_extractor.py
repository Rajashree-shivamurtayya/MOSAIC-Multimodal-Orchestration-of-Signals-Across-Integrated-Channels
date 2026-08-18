import numpy as np
import json
import os

class PhysioFeatureExtractor:
    def __init__(self):
        pass

    def extract_trial_features(self, baseline_packets, answer_packets):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(base_dir, "models", "model_features.json")) as f:
            schema_keys = json.load(f)["physiology_features"]

        features = {k: np.nan for k in schema_keys}
        
        if len(answer_packets) == 0:
            features["physiological_available"] = 0
            return features, "POOR"
            
        b_hr = [p.get("hr", np.nan) for p in baseline_packets if p.get("contact", False)]
        b_spo2 = [p.get("spo2", np.nan) for p in baseline_packets if p.get("contact", False)]
        
        a_hr = [p.get("hr", np.nan) for p in answer_packets if p.get("contact", False)]
        a_spo2 = [p.get("spo2", np.nan) for p in answer_packets if p.get("contact", False)]
        
        b_hr = [x for x in b_hr if not np.isnan(x)]
        b_spo2 = [x for x in b_spo2 if not np.isnan(x)]
        a_hr = [x for x in a_hr if not np.isnan(x)]
        a_spo2 = [x for x in a_spo2 if not np.isnan(x)]
        
        if len(a_hr) == 0:
            features["physiological_available"] = 0
            return features, "POOR"
            
        features["physiological_available"] = 1
            
        base_hr_val = np.mean(b_hr) if b_hr else 0
        base_spo2_val = np.mean(b_spo2) if b_spo2 else 0
        features["baseline_heart_rate_bpm"] = base_hr_val
        features["baseline_spo2_percent"] = base_spo2_val
        
        features["heart_rate_bpm"] = np.mean(a_hr)
        features["mean_heart_rate_bpm"] = np.mean(a_hr)
        features["max_heart_rate_bpm"] = np.max(a_hr)
        features["min_heart_rate_bpm"] = np.min(a_hr)
        features["heart_rate_std"] = np.std(a_hr)
        features["heart_rate_range"] = np.max(a_hr) - np.min(a_hr)
        features["heart_rate_change_from_baseline"] = np.mean(a_hr) - base_hr_val
        features["heart_rate_percent_change_from_baseline"] = ((np.mean(a_hr) - base_hr_val) / base_hr_val * 100) if base_hr_val > 0 else 0
        
        features["mean_rr_interval_ms"] = 60000 / np.mean(a_hr) if np.mean(a_hr) > 0 else 0
        
        features["spo2_percent"] = np.mean(a_spo2)
        features["during_question_spo2"] = np.mean(a_spo2) 
        features["pre_question_spo2"] = base_spo2_val
        features["spo2_max"] = np.max(a_spo2)
        features["spo2_min"] = np.min(a_spo2)
        features["spo2_std"] = np.std(a_spo2)
        features["spo2_range"] = np.max(a_spo2) - np.min(a_spo2)
        features["spo2_change_from_baseline"] = np.mean(a_spo2) - base_spo2_val
        features["spo2_delta_pre_to_question"] = np.mean(a_spo2) - base_spo2_val
        
        features["sensor_contact_quality"] = 1.0
        
        quality = "GOOD" if len(a_hr) > 50 else "FAIR"
        
        return features, quality
