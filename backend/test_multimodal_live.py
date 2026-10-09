import requests
import json
import numpy as np
import soundfile as sf
import tempfile
import os
import time

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("=" * 60)
    print("MOSAIC MULTIMODAL INTEGRATION TEST SUITE")
    print("=" * 60)

    # 1. Health check
    print("\n--- 1. Testing GET /health ---")
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    assert r.status_code == 200, f"Health check failed: {r.status_code}"
    print("[PASS] Backend health check:", r.json())

    # 2. Hardware / Physio status
    print("\n--- 2. Testing GET /api/physio/status ---")
    r = requests.get(f"{BASE_URL}/api/physio/status", timeout=5)
    assert r.status_code == 200, f"Physio status failed: {r.status_code}"
    status_data = r.json()
    print("[PASS] Physio status response:")
    print(json.dumps(status_data, indent=2))
    assert "connected" in status_data
    assert "port" in status_data
    assert "sensor" in status_data

    # 3. Real physiological feature extraction
    print("\n--- 3. Testing GET /api/physiological/latest ---")
    r = requests.get(f"{BASE_URL}/api/physiological/latest", timeout=5)
    assert r.status_code == 200, f"Latest physio failed: {r.status_code}"
    phys_data = r.json()
    assert phys_data.get("status") == "success"
    feats = phys_data["features"]
    print(f"[PASS] Real MAX30102 Features Extracted:")
    print(f"       Heart Rate: {feats.get('estimated_heart_rate_bpm')} BPM")
    print(f"       Signal Quality: {feats.get('signal_quality_percent')}%")
    print(f"       HRV SDNN / RMSSD: {feats.get('sdnn')} ms / {feats.get('rmssd')} ms")
    print(f"       Sample Count: {feats.get('sample_count')}")
    print(f"       Temperature: {feats.get('mean_temperature')} (Must be None)")
    print(f"       SpO2: {feats.get('spo2_percent')} (Must be None)")
    assert feats.get("mean_temperature") is None, "Temperature must be None (not calibrated/streamed)!"
    assert feats.get("spo2_percent") is None, "SpO2 must be None (uncalibrated)!"

    # 4. Modality Status Check (Prior to audio/vision activation)
    print("\n--- 4. Testing Modality Status (Before Activation) ---")
    r_a = requests.get(f"{BASE_URL}/api/audio/status").json()
    r_v = requests.get(f"{BASE_URL}/api/vision/status").json()
    print(f"[PASS] Audio Status: {r_a}")
    print(f"[PASS] Vision Status: {r_v}")
    assert r_a.get("probability") is None or r_a.get("available") is False
    assert r_v.get("probability") is None or r_v.get("available") is False

    # 5. Missing modality prediction test
    print("\n--- 5. Testing POST /api/predict (Missing Modalities) ---")
    r_pred = requests.post(f"{BASE_URL}/api/predict").json()
    print(f"[PASS] Missing Modality Behavior:")
    print(f"       Fusion Status: {r_pred.get('fusion_status')}")
    print(f"       Prediction: {r_pred.get('prediction')} (Must be None)")
    print(f"       Fusion Prob: {r_pred.get('fusion_probability')} (Must be None)")
    print(f"       Modalities Used: {r_pred.get('modalities_used')}")
    print(f"       Modalities Missing: {r_pred.get('modalities_missing')}")
    assert r_pred.get("fusion_status") == "awaiting_active_modalities"
    assert r_pred.get("prediction") is None
    assert r_pred.get("fusion_probability") is None
    assert "audio" in r_pred.get("modalities_missing")
    assert "vision" in r_pred.get("modalities_missing")

    # 6. Audio feature extraction via API
    print("\n--- 6. Testing POST /api/extract/audio ---")
    t = np.linspace(0, 1.5, 24000)
    # Audio with modulation simulating speech formant
    y = 0.5 * np.sin(2 * np.pi * 220 * t) + 0.3 * np.sin(2 * np.pi * 440 * t)
    wav_path = tempfile.mktemp(suffix=".wav")
    sf.write(wav_path, y, 16000)
    with open(wav_path, "rb") as f:
        r_aud = requests.post(f"{BASE_URL}/api/extract/audio", files={"file": f}).json()
    if os.path.exists(wav_path):
        os.remove(wav_path)
    print(f"[PASS] Audio Extraction Result: available={r_aud.get('available')}, probability={r_aud.get('probability')}")
    assert r_aud.get("available") is True
    assert r_aud.get("probability") is not None

    # Check updated audio status
    r_a_active = requests.get(f"{BASE_URL}/api/audio/status").json()
    print(f"[PASS] Active Audio Status: {r_a_active}")
    assert r_a_active.get("available") is True

    # 7. Session creation
    print("\n--- 7. Testing POST /api/session/start ---")
    r_ses = requests.post(f"{BASE_URL}/api/session/start", params={"participant_id": "TEST_PARTICIPANT"}).json()
    session_id = r_ses["session_id"]
    print(f"[PASS] Session Started: {session_id}")

    # 8. Full late fusion with 3 genuine probabilities
    print("\n--- 8. Testing Late Fusion Pipeline with 3 Genuine Modalities ---")
    # Update vision modality on running server via API
    dummy_vis_feats = {
        "face_detected": 1,
        "video_available": 1,
        "blink_rate": 18.0,
        "blink_count": 2,
        "head_yaw_degrees": 2.5,
        "head_pitch_degrees": -1.0,
        "head_roll_degrees": 0.5,
        "eyebrow_delta_mean": 0.015,
        "gaze_x_mean": 0.52,
        "gaze_y_mean": 0.49,
        "mean_eye_aspect_ratio": 0.28,
        "mouth_aspect_ratio": 0.12,
        "face_area_pixels": 45000.0
    }
    r_vis_up = requests.post(f"{BASE_URL}/api/modality/vision/update", json=dummy_vis_feats).json()
    print(f"[INFO] Injected vision features via API: prob={r_vis_up.get('probability')}")
    assert r_vis_up.get("available") is True

    # Now run prediction with all 3 modalities active
    r_full = requests.post(f"{BASE_URL}/api/predict", params={"session_id": session_id}).json()
    print("\n[PASS] Full Multimodal Prediction Result:")
    print(json.dumps(r_full, indent=2))
    assert r_full.get("fusion_status") == "ready"
    assert r_full.get("prediction") in ["truthful", "deceptive"]
    assert r_full.get("fusion_probability") is not None
    assert r_full.get("confidence") is not None
    assert len(r_full.get("modalities_used")) == 3
    assert len(r_full.get("modalities_missing")) == 0
    assert r_full.get("classification_type") == "experimental_classification"

    # 9. Session result endpoint
    print(f"\n--- 9. Testing GET /api/session/{session_id}/result ---")
    r_res = requests.get(f"{BASE_URL}/api/session/{session_id}/result").json()
    print(json.dumps(r_res, indent=2))
    assert r_res.get("session_id") == session_id
    assert r_res.get("prediction") in ["truthful", "deceptive"]
    assert r_res.get("classification_type") == "experimental_classification"
    assert "disclaimer" in r_res

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
