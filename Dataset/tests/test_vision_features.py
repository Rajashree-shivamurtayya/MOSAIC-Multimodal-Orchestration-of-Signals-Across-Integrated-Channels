import pytest
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from cv.vision_feature_extractor import VisionFeatureExtractor

@pytest.fixture
def extractor():
    return VisionFeatureExtractor()

@pytest.fixture
def dummy_landmarks():
    return np.random.rand(468, 3) * 640

def test_compute_ear(extractor, dummy_landmarks):
    ear = extractor.compute_ear(dummy_landmarks, 159, 145, 33, 133)
    assert isinstance(ear, float)
    assert ear >= 0

def test_compute_head_pose(extractor, dummy_landmarks):
    yaw, pitch, roll = extractor.compute_head_pose(dummy_landmarks, 640, 480)
    assert isinstance(yaw, float)
    assert isinstance(pitch, float)
    assert isinstance(roll, float)

def test_extract_trial_features(extractor, dummy_landmarks):
    baseline = [dummy_landmarks] * 30
    answer = [dummy_landmarks] * 90
    
    features, quality = extractor.extract_trial_features(baseline, answer, 640, 480)
    
    assert quality in ["GOOD", "FAIR", "POOR"]
    assert features["video_available"] == 1
    assert "baseline_left_eyebrow_eye_distance" in features
    assert "left_eyebrow_height_delta" in features
    
    # Check schema matching
    base_dir = os.path.dirname(os.path.dirname(__file__))
    import json
    with open(os.path.join(base_dir, "models", "model_features.json")) as f:
        schema_keys = json.load(f)["vision_features"]
    
    for key in schema_keys:
        assert key in features

def test_missing_face(extractor):
    baseline = [None] * 30
    answer = [None] * 90
    
    features, quality = extractor.extract_trial_features(baseline, answer, 640, 480)
    assert quality == "POOR"
    assert features["video_available"] == 0
