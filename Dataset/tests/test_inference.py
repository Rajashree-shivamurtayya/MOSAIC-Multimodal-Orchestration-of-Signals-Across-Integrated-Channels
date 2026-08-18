import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from simulation.sensor_adapter import CSVSensorAdapter
from inference.predict import predict_trial

@pytest.fixture
def base_trial():
    adapter = CSVSensorAdapter()
    return next(adapter.get_trials_for_participant(adapter.df["participant_id"].iloc[0]))

def test_normal_complete_trial(base_trial):
    res = predict_trial(base_trial)
    assert 0 <= res["fusion_probability"] <= 1
    assert res["physiology_available"] is True
    assert res["audio_available"] is True
    assert res["vision_available"] is True
    assert res["classification"] in ["DECEPTIVE CLASS", "TRUTH CLASS"]

def test_missing_physiology(base_trial):
    base_trial["physiological_available"] = 0
    res = predict_trial(base_trial)
    assert res["physiology_available"] is False
    assert res["physiology_probability"] == 0.5
    assert 0 <= res["fusion_probability"] <= 1

def test_missing_audio(base_trial):
    base_trial["audio_available"] = 0
    res = predict_trial(base_trial)
    assert res["audio_available"] is False
    assert res["audio_probability"] == 0.5
    assert 0 <= res["fusion_probability"] <= 1

def test_missing_vision(base_trial):
    base_trial["video_available"] = 0
    res = predict_trial(base_trial)
    assert res["vision_available"] is False
    assert res["vision_probability"] == 0.5
    assert 0 <= res["fusion_probability"] <= 1

def test_poor_signal_quality(base_trial):
    base_trial["overall_trial_quality"] = "POOR"
    res = predict_trial(base_trial)
    assert res["signal_quality"] == "POOR"
    
def test_invalid_missing_feature(base_trial):
    # Remove an important feature, the pipeline imputer should handle it
    from inference.predict import phys_features
    if phys_features and phys_features[0] in base_trial:
        del base_trial[phys_features[0]]
    res = predict_trial(base_trial)
    assert 0 <= res["physiology_probability"] <= 1
    
def test_no_ground_truth_leakage(base_trial):
    # ground_truth_binary should not affect probability
    if "ground_truth_binary" in base_trial:
        base_trial["ground_truth_binary"] = 0
        res1 = predict_trial(base_trial)
        base_trial["ground_truth_binary"] = 1
        res2 = predict_trial(base_trial)
        assert res1["fusion_probability"] == res2["fusion_probability"]
