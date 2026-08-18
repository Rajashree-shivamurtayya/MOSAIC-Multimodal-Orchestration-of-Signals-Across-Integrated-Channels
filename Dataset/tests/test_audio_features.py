import pytest
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from audio.audio_feature_extractor import AudioFeatureExtractor

@pytest.fixture
def extractor():
    return AudioFeatureExtractor()

def test_vad(extractor):
    silent = np.zeros(16000 * 2) 
    is_speech = extractor._vad(silent)
    assert not np.any(is_speech)
    
    loud = np.random.randn(16000 * 2) * 0.5
    is_speech = extractor._vad(loud)
    assert np.any(is_speech)

def test_extract_trial_features(extractor):
    baseline = [np.random.randn(16000 * 5) * 0.1]
    answer = [np.random.randn(16000 * 15) * 0.1]
    
    features, quality = extractor.extract_trial_features(baseline, answer)
    
    assert quality in ["GOOD", "FAIR", "POOR"]
    assert features["audio_available"] == 1
    assert "mean_pitch_hz" in features
    
    import json
    base_dir = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(base_dir, "models", "model_features.json")) as f:
        schema_keys = json.load(f)["audio_features"]
    
    for key in schema_keys:
        assert key in features

def test_missing_audio(extractor):
    features, quality = extractor.extract_trial_features([], [])
    assert quality == "POOR"
    assert features["audio_available"] == 0
