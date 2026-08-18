import pytest
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from physio.physio_feature_extractor import PhysioFeatureExtractor

@pytest.fixture
def extractor():
    return PhysioFeatureExtractor()

def test_extract_trial_features(extractor):
    baseline = [{"timestamp": 0, "hr": 70, "spo2": 98, "contact": True} for _ in range(250)]
    answer = [{"timestamp": 0, "hr": 75, "spo2": 98, "contact": True} for _ in range(750)]
    
    features, quality = extractor.extract_trial_features(baseline, answer)
    
    assert quality in ["GOOD", "FAIR", "POOR"]
    assert features["physiological_available"] == 1
    assert features["baseline_heart_rate_bpm"] == 70
    assert features["mean_heart_rate_bpm"] == 75
    assert features["heart_rate_change_from_baseline"] == 5

def test_missing_data(extractor):
    features, quality = extractor.extract_trial_features([], [])
    assert quality == "POOR"
    assert features["physiological_available"] == 0

def test_no_contact(extractor):
    baseline = [{"timestamp": 0, "hr": 70, "spo2": 98, "contact": False} for _ in range(250)]
    answer = [{"timestamp": 0, "hr": 75, "spo2": 98, "contact": False} for _ in range(750)]
    
    features, quality = extractor.extract_trial_features(baseline, answer)
    assert quality == "POOR"
    assert features["physiological_available"] == 0
