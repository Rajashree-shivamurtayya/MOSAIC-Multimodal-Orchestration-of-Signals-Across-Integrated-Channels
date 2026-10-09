import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive headless backend safe for servers
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks

# ============================================================
# MOSAIC - PPG Waveform Plotter & Physiological Visualizer
# Demonstrates raw optical waveforms and filtered systolic peaks
# Saves figure to ppg_signal.png
# ============================================================

CSV_FILE = "mosaic_ppg.csv"
OUTPUT_PLOT = "ppg_signal.png"


def main():
    target_path = os.path.abspath(CSV_FILE)
    if not os.path.exists(target_path):
        print(f"ERROR: File '{CSV_FILE}' not found.")
        sys.exit(1)

    df = pd.read_csv(target_path)
    if len(df) < 20:
        print("ERROR: Not enough samples to plot.")
        sys.exit(1)

    # Focus on a stable segment with finger contact
    stable_df = df[df["ir"] > 10000].copy()
    if len(stable_df) < 50:
        stable_df = df.copy()

    # Take a 20-second window (or full segment if short) for clear visualization of pulse waves
    timestamps = stable_df["timestamp_ms"].to_numpy(dtype=float)
    t_zero = timestamps[0]
    time_s = (timestamps - t_zero) / 1000.0

    diffs = np.diff(timestamps)
    valid_diffs = diffs[diffs > 0]
    fs = 1000.0 / np.median(valid_diffs) if len(valid_diffs) > 0 else 12.5

    # Window of up to ~250 samples (~20 seconds) for crisp pulse waveform details
    plot_len = min(250, len(stable_df))
    # Pick a steady portion in the middle or end
    start_idx = max(0, len(stable_df) - plot_len - 50)
    end_idx = start_idx + plot_len

    sub_t = time_s[start_idx:end_idx] - time_s[start_idx]
    sub_ir = stable_df["ir"].iloc[start_idx:end_idx].to_numpy(dtype=float)
    sub_red = stable_df["red"].iloc[start_idx:end_idx].to_numpy(dtype=float)

    # Filter for systolic pulse waves
    nyq = fs / 2.0
    b, a = butter(2, [0.7 / nyq, min(3.0 / nyq, 0.95)], btype="band")
    filtered_ir = filtfilt(b, a, sub_ir - np.mean(sub_ir))

    min_dist = max(int(fs * 0.33), 1)
    peaks, _ = find_peaks(filtered_ir, distance=min_dist, prominence=np.std(filtered_ir) * 0.25)

    # Plot
    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

    # Subplot 1: Raw Optical Sensor Readings
    axes[0].plot(sub_t, sub_ir, label="Raw IR (880nm)", color="#e11d48", linewidth=1.5)
    axes[0].plot(sub_t, sub_red, label="Raw RED (660nm)", color="#ea580c", linewidth=1.5, alpha=0.85)
    axes[0].set_ylabel("Raw Sensor Counts", fontsize=11, fontweight="bold")
    axes[0].set_title("MOSAIC MAX30102 - Raw Optical PPG Acquisition", fontsize=13, fontweight="bold", pad=10)
    axes[0].legend(loc="upper right", frameon=True)
    axes[0].grid(True, linestyle="--", alpha=0.5)

    # Subplot 2: Filtered AC Waveform with Detected Heartbeat Peaks
    axes[1].plot(sub_t, filtered_ir, label="Filtered PPG Waveform (0.7 - 3.0 Hz)", color="#0284c7", linewidth=2.0)
    if len(peaks) > 0:
        axes[1].plot(
            sub_t[peaks],
            filtered_ir[peaks],
            "o",
            color="#16a34a",
            markersize=7,
            label=f"Detected Systolic Peaks ({len(peaks)} beats)"
        )

    axes[1].set_xlabel("Time (seconds)", fontsize=11, fontweight="bold")
    axes[1].set_ylabel("Normalized AC Amplitude", fontsize=11, fontweight="bold")
    axes[1].set_title("Bandpass Filtered Pulse Waveform & Beat Intervals", fontsize=12, fontweight="bold", pad=10)
    axes[1].legend(loc="upper right", frameon=True)
    axes[1].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    output_abs = os.path.abspath(OUTPUT_PLOT)
    plt.savefig(output_abs, dpi=180)
    plt.close()

    print(f"PPG Waveform plot successfully saved to: {output_abs}")


if __name__ == "__main__":
    main()
