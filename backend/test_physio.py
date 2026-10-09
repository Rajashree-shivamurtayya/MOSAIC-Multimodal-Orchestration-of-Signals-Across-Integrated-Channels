import os
import sys
from ml.feature_extraction import extract_physiological_features

# ============================================================
# MOSAIC - Physiological Signal Verification Script
# Validates Heart Rate, HRV (SDNN, RMSSD), Skin Temperature,
# Signal Quality, and Optical SpO2 from mosaic_ppg.csv
# ============================================================

CSV_FILE = "mosaic_ppg.csv"


def main():
    target_path = os.path.abspath(CSV_FILE)

    if not os.path.exists(target_path):
        print("=" * 50)
        print("MOSAIC PHYSIOLOGICAL ANALYSIS")
        print("=" * 50)
        print(f"ERROR: File '{CSV_FILE}' not found at {target_path}")
        print("Run 'python test_max30102.py' first to collect sensor data.")
        print("Status: FAILED")
        print("=" * 50)
        sys.exit(1)

    features = extract_physiological_features(target_path)

    if features is None:
        print("=" * 50)
        print("MOSAIC PHYSIOLOGICAL ANALYSIS")
        print("=" * 50)
        print(f"Source: MAX30102")
        print(f"File: {CSV_FILE}")
        print("\nERROR: Failed to extract physiological features from dataset.")
        print("Status: FAILED")
        print("=" * 50)
        sys.exit(1)

    # Format values honestly without fabricating
    samples_str = str(features.get("sample_count", "N/A"))
    sampling_rate_val = features.get("sampling_rate")
    sampling_rate_str = f"{sampling_rate_val:.2f} Hz" if sampling_rate_val is not None else "N/A"

    mean_hr_val = features.get("mean_hr")
    mean_hr_str = f"{mean_hr_val:.1f} BPM" if mean_hr_val is not None else "Unavailable / No Valid Peaks"

    sdnn_val = features.get("sdnn")
    sdnn_str = f"{sdnn_val:.1f} ms" if sdnn_val is not None else "Unavailable / Insufficient Beats"

    rmssd_val = features.get("rmssd")
    rmssd_str = f"{rmssd_val:.1f} ms" if rmssd_val is not None else "Unavailable / Insufficient Beats"

    mean_ir_val = features.get("mean_ir")
    mean_ir_str = f"{mean_ir_val:.1f}" if mean_ir_val is not None else "N/A"

    mean_red_val = features.get("mean_red")
    mean_red_str = f"{mean_red_val:.1f}" if mean_red_val is not None else "N/A"

    mean_temp_val = features.get("mean_temperature")
    mean_temp_str = f"{mean_temp_val:.2f} C" if mean_temp_val is not None else "N/A"

    spo2_val = features.get("spo2_percent")
    if features.get("spo2_available") and spo2_val is not None:
        spo2_str = f"{spo2_val:.1f} %"
    else:
        spo2_str = "Unavailable (Uncalibrated Optical Sensor)"

    sq_val = features.get("signal_quality_percent")
    sq_str = f"{sq_val:.1f} % ({features.get('signal_quality_status', 'N/A').upper()})" if sq_val is not None else "N/A"

    beats_count = features.get("num_beats", 0)

    print("=" * 50)
    print("MOSAIC PHYSIOLOGICAL ANALYSIS")
    print("=" * 50)
    print("Source: MAX30102")
    print(f"File: {CSV_FILE}")
    print()
    print(f"Samples: {samples_str}")
    print(f"Sampling Rate: {sampling_rate_str}")
    print(f"Detected Beats: {beats_count}")
    print()
    print(f"Mean HR: {mean_hr_str}")
    print(f"SDNN: {sdnn_str}")
    print(f"RMSSD: {rmssd_str}")
    print()
    print(f"Mean IR: {mean_ir_str}")
    print(f"Mean RED: {mean_red_str}")
    print(f"Mean Temperature: {mean_temp_str}")
    print()
    print(f"SpO2: {spo2_str}")
    print()
    print(f"Signal Quality: {sq_str}")
    print()
    print("Status: SUCCESS")
    print("=" * 50)


if __name__ == "__main__":
    main()
