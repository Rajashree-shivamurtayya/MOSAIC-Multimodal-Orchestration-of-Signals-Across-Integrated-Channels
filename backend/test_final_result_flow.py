"""
MOSAIC Multimodal Live Integration - Final Session Result Flow Test
Verifies the end-to-end integration:
Hardware / CSV -> Audio / Vision -> Unimodal Pipelines -> Late Fusion -> Session Result Endpoint
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_final_result_flow():
    print("\n" + "="*60)
    print("  MOSAIC FINAL SESSION RESULT FLOW VERIFICATION")
    print("="*60)

    # 1. Health check
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    assert r.status_code == 200, f"Health check failed: {r.status_code}"
    print("\n[TEST 1] Backend Health Check: PASSED")

    # 2. Check Physio Sensor Status
    r = requests.get(f"{BASE_URL}/api/physio/status", timeout=5)
    assert r.status_code == 200
    phys_status = r.json()
    print(f"[TEST 2] Physio Status: Port={phys_status.get('port')}, Samples={phys_status.get('samples')}, Connected={phys_status.get('connected')}")
    assert phys_status.get("sensor") == "MAX30102"

    # 3. Start New Session
    r = requests.post(f"{BASE_URL}/api/session/start", params={"participant_id": "P_DEMO_01"}, timeout=5)
    assert r.status_code == 200
    start_json = r.json()
    session_id = start_json.get("session_id")
    print(f"\n[TEST 3] Session Started: ID={session_id}")
    assert session_id is not None

    # 4. Check In-Progress Session Result (Missing Audio & Vision)
    r = requests.get(f"{BASE_URL}/api/session/{session_id}/result", timeout=5)
    assert r.status_code == 200
    res_initial = r.json()
    print("\n[TEST 4] Session State Before Audio/Vision:")
    print(f"  - Status: {res_initial.get('status')}")
    print(f"  - Fusion Status: {res_initial.get('fusion_status')}")
    print(f"  - Prediction: {res_initial.get('prediction')} (Must be None when modalities are missing)")
    print(f"  - Modalities Used: {res_initial.get('modalities_used')}")
    print(f"  - Modalities Missing: {res_initial.get('modalities_missing')}")
    print(f"  - Physiology Available: {res_initial.get('physiology', {}).get('available')}")
    print(f"  - Heart Rate: {res_initial.get('physiology', {}).get('heart_rate_bpm')} BPM")
    print(f"  - Temperature: {res_initial.get('physiology', {}).get('temperature')}")
    print(f"  - SpO2: {res_initial.get('physiology', {}).get('spo2')}")

    assert res_initial.get("fusion_status") == "awaiting_active_modalities"
    assert res_initial.get("prediction") is None
    assert "audio" in res_initial.get("modalities_missing", [])
    assert "vision" in res_initial.get("modalities_missing", [])
    assert res_initial.get("physiology", {}).get("temperature") == "Unavailable (Sensor channel not calibrated/streamed)"
    assert res_initial.get("physiology", {}).get("spo2") == "Unavailable (Uncalibrated)"

    # 5. Provide Audio Modality Telemetry
    aud_payload = {
        "audio_available": 1,
        "is_silent": False,
        "zcr_mean": 0.048,
        "mean_rms_energy": 0.028,
        "mfcc_mean": [-22.5, 4.8, 1.2, -0.5]
    }
    r = requests.post(f"{BASE_URL}/api/modality/audio/update", json=aud_payload, timeout=5)
    assert r.status_code == 200
    aud_res = r.json()
    print(f"\n[TEST 5] Audio Modality Updated: Probability={aud_res.get('probability')}")
    assert aud_res.get("available") is True
    assert aud_res.get("probability") is not None

    # 6. Provide Vision Modality Telemetry
    vis_payload = {
        "video_available": 1,
        "face_detected": 1,
        "blink_rate": 15.0,
        "blink_count": 6,
        "head_yaw_mean": 1.8,
        "eyebrow_delta_mean": 0.015
    }
    r = requests.post(f"{BASE_URL}/api/modality/vision/update", json=vis_payload, timeout=5)
    assert r.status_code == 200
    vis_res = r.json()
    print(f"[TEST 6] Vision Modality Updated: Probability={vis_res.get('probability')}")
    assert vis_res.get("available") is True
    assert vis_res.get("probability") is not None

    # 7. Run Predict Endpoint (all 3 modalities active)
    r = requests.post(f"{BASE_URL}/api/predict", params={"session_id": session_id}, timeout=5)
    assert r.status_code == 200
    pred_res = r.json()
    print("\n[TEST 7] Predict Endpoint Response:")
    print(f"  - Prediction: {pred_res.get('prediction')}")
    print(f"  - Fusion Probability: {pred_res.get('fusion_probability')}")
    print(f"  - Confidence: {pred_res.get('confidence')}")
    print(f"  - Fusion Status: {pred_res.get('fusion_status')}")
    print(f"  - Fusion Input Vector: {pred_res.get('fusion_input_vector')}")
    assert pred_res.get("fusion_status") == "ready"
    assert pred_res.get("prediction") in ["truthful", "deceptive"]
    assert pred_res.get("fusion_probability") is not None

    # 8. Complete Session Endpoint
    r = requests.post(f"{BASE_URL}/api/session/{session_id}/complete", timeout=5)
    assert r.status_code == 200
    final_res = r.json()
    print("\n[TEST 8] Final Session Result (Completed):")
    print(f"  - Session ID: {final_res.get('session_id')}")
    print(f"  - Status: {final_res.get('status')}")
    print(f"  - Start Time: {final_res.get('start_time')}")
    print(f"  - End Time: {final_res.get('end_time')}")
    print(f"  - Duration: {final_res.get('duration_seconds')}s")
    print(f"  - Final Prediction: {final_res.get('prediction')}")
    print(f"  - Fusion Probability: {final_res.get('fusion_probability')}")
    print(f"  - Confidence: {final_res.get('confidence')}")
    print(f"  - Fusion Input Vector: {final_res.get('fusion_input_vector')}")
    print(f"  - Modalities Used: {final_res.get('modalities_used')}")
    print(f"  - Modalities Missing: {final_res.get('modalities_missing')}")
    print(f"  - Sensor Source: {final_res.get('physiology', {}).get('sensor_source')}")
    print(f"  - Sensor COM Port: {final_res.get('physiology', {}).get('port')}")
    print(f"  - Heart Rate: {final_res.get('physiology', {}).get('heart_rate_bpm')} BPM")
    print(f"  - Signal Quality: {final_res.get('physiology', {}).get('signal_quality')}%")
    print(f"  - Audio Model Probability: {final_res.get('audio', {}).get('probability')}")
    print(f"  - Vision Model Probability: {final_res.get('vision', {}).get('probability')}")
    print(f"  - Disclaimer: {final_res.get('disclaimer')}")

    # Verify All Contractual Fields
    assert final_res.get("session_id") == session_id
    assert final_res.get("status") == "completed"
    assert final_res.get("start_time") is not None
    assert final_res.get("end_time") is not None
    assert final_res.get("classification_type") == "experimental_classification"
    assert final_res.get("prediction") in ["truthful", "deceptive"]
    assert final_res.get("fusion_probability") is not None
    assert final_res.get("confidence") is not None
    assert final_res.get("fusion_status") == "ready"
    assert len(final_res.get("fusion_input_vector", [])) == 3
    assert final_res.get("modalities_used") == ["physiological", "audio", "vision"]
    assert final_res.get("modalities_missing") == []
    assert final_res.get("physiology", {}).get("sensor_source") == "MAX30102"
    assert final_res.get("audio", {}).get("capture_status") == "captured"
    assert final_res.get("vision", {}).get("capture_status") == "captured"

    # 9. Verify GET /api/session/latest/result matches completed result
    r = requests.get(f"{BASE_URL}/api/session/latest/result", timeout=5)
    assert r.status_code == 200
    latest_res = r.json()
    assert latest_res.get("session_id") == session_id
    assert latest_res.get("status") == "completed"
    assert latest_res.get("prediction") == final_res.get("prediction")
    print("\n[TEST 9] Latest Session Endpoint Verification: PASSED (Identical to Completed Record)")

    print("\n" + "="*60)
    print("  ALL 9 END-TO-END FINAL RESULT TESTS PASSED!")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_final_result_flow()
