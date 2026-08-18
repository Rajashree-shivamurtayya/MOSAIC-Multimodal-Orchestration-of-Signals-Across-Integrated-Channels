"""
Stage 2 - fill the model prediction columns with REAL out-of-fold predictions.

Every probability in the dataset comes from a model that never saw that
participant during training (GroupKFold on participant_id). No leakage, and
the numbers are honest rather than invented.
"""
import warnings, json
import numpy as np, pandas as pd
warnings.simplefilter("ignore")

from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix)

BASE = "/sessions/clever-upbeat-hamilton/mnt/outputs"
df = pd.read_csv(f"{BASE}/_stage1.csv")
y = df.ground_truth_binary.values
groups = df.participant_id.values

PHYS = ["heart_rate_change_from_baseline", "heart_rate_percent_change_from_baseline",
        "heart_rate_std", "heart_rate_range", "heart_rate_recovery_rate",
        "rmssd_ms", "sdnn_ms", "pnn50_percent", "mean_rr_interval_ms",
        "spo2_change_from_baseline", "spo2_std", "perfusion_index",
        "perfusion_index_change_from_baseline", "pulse_amplitude",
        "pulse_rise_time_ms", "pulse_width_ms", "hr_delta_pre_to_question",
        "hr_delta_question_to_answer", "recovery_time_seconds", "pulse_signal_quality"]

AUDIO = ["response_latency_ms", "speaking_rate_wpm", "articulation_rate_wpm",
         "pause_count", "mean_pause_duration_ms", "pause_ratio", "pause_duration_std",
         "filler_word_count", "filler_word_rate", "stutter_event_count",
         "stutter_frequency", "repetition_count", "prolongation_count", "block_count",
         "self_correction_count", "false_start_count", "hesitation_rate",
         "mean_pitch_hz", "pitch_std", "pitch_range_hz", "jitter_percent",
         "shimmer_percent", "hnr_db", "voice_intensity_db", "zero_crossing_rate",
         "spectral_centroid", "spectral_flatness", "speech_to_silence_ratio",
         "mean_rms_energy"] + [f"mfcc_{i:02d}_mean" for i in range(1, 14)]

VISION = ["blink_rate_per_minute", "blink_delta_pre_to_answer", "mean_blink_duration_ms",
          "blink_duration_std", "mean_eye_aspect_ratio", "eye_openness_variance",
          "gaze_deviation_degrees", "gaze_stability", "gaze_shift_frequency",
          "looking_away_ratio", "head_yaw_std", "head_pitch_std", "head_roll_std",
          "head_motion_score", "head_movement_count", "expression_entropy",
          "fear_expression_probability", "surprise_expression_probability",
          "happy_expression_probability", "neutral_expression_probability",
          "au04_intensity", "au07_intensity", "au14_intensity", "au45_intensity",
          "au06_intensity", "au12_intensity", "facial_action_unit_activity",
          "body_motion_score", "posture_change_count",
          # eyebrow geometry, face-relative (NOT the naive_* camera-frame versions)
          "left_eyebrow_height_delta", "right_eyebrow_height_delta", "eyebrow_asymmetry",
          "eyebrow_raise_event_count", "eyebrow_movement_score", "eyebrow_raise_duration_ms",
          "left_eyebrow_peak_raise", "right_eyebrow_peak_raise", "left_eyebrow_velocity",
          "left_eyebrow_movement_std", "right_eyebrow_movement_std",
          # head pose relative to the baseline window
          "head_yaw_delta", "head_pitch_delta", "head_roll_delta",
          "head_movement_velocity_deg_s",
          # eye openness relative to the baseline window
          "left_eye_openness_delta", "right_eye_openness_delta", "long_blink_count",
          "eye_closure_duration_ms",
          # gaze relative to the baseline window
          "gaze_x_delta", "gaze_y_delta", "gaze_horizontal_deviation",
          "gaze_vertical_deviation", "gaze_velocity_deg_s",
          # whole-face temporal motion
          "facial_motion_mean", "facial_motion_std", "facial_motion_peak",
          "facial_landmark_velocity_mean", "facial_landmark_acceleration_mean",
          "expression_stability"]

BLOCKS = {"physiological": PHYS, "audio": AUDIO, "computer_vision": VISION}


def oof(X, y, groups, model):
    """Out-of-fold probabilities via participant-level GroupKFold."""
    p = np.zeros(len(y))
    for tr, te in GroupKFold(n_splits=5).split(X, y, groups):
        m = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), model)
        m.fit(X.iloc[tr], y[tr])
        p[te] = m.predict_proba(X.iloc[te])[:, 1]
    return p


def report(name, y, p):
    yh = (p >= .5).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, yh).ravel()
    return dict(model=name, accuracy=round(accuracy_score(y, yh), 4),
                precision=round(precision_score(y, yh), 4),
                recall=round(recall_score(y, yh), 4),
                f1=round(f1_score(y, yh), 4),
                roc_auc=round(roc_auc_score(y, p), 4),
                TP=int(tp), TN=int(tn), FP=int(fp), FN=int(fn))


metrics, probs = [], {}
for name, cols in BLOCKS.items():
    p = oof(df[cols], y, groups, LogisticRegression(max_iter=2000, C=0.35))
    probs[name] = p
    metrics.append(report(name, y, p))

# late fusion over the three modality probabilities + availability flags
fus = pd.DataFrame({k: probs[k] for k in BLOCKS})
fus["modality_count_available"] = df.modality_count_available
p_fus = oof(fus, y, groups, LogisticRegression(max_iter=2000))
metrics.append(report("fusion_late", y, p_fus))

# early fusion (all raw features) as a comparison point for the ablation chapter
p_early = oof(df[PHYS + AUDIO + VISION], y, groups,
              GradientBoostingClassifier(n_estimators=180, max_depth=3, learning_rate=.06))
metrics.append(report("fusion_early_gbdt", y, p_early))

# ── ablation table
ablation = []
for label, cols in [("Physiology", PHYS), ("Audio", AUDIO), ("Vision", VISION),
                    ("Physiology+Audio", PHYS + AUDIO), ("Physiology+Vision", PHYS + VISION),
                    ("Audio+Vision", AUDIO + VISION), ("All modalities", PHYS + AUDIO + VISION)]:
    pa = oof(df[cols], y, groups, LogisticRegression(max_iter=2000, C=0.35))
    r = report(label, y, pa); r["n_features"] = len(cols)
    ablation.append(r)

# ── does head-pose normalisation actually matter? measure it, do not assume it.
BROW_OK = ["left_eyebrow_height_delta", "right_eyebrow_height_delta"]
BROW_NAIVE = ["naive_left_eyebrow_delta_camera_frame", "naive_right_eyebrow_delta_camera_frame"]
REST = [c for c in VISION if c not in BROW_OK]
norm = []
for label, cols in [("brow only - face-relative", BROW_OK),
                    ("brow only - raw camera frame", BROW_NAIVE),
                    ("full vision - face-relative brow", VISION),
                    ("full vision - raw camera brow", REST + BROW_NAIVE)]:
    pn = oof(df[cols], y, groups, LogisticRegression(max_iter=2000, C=0.35))
    r = report(label, y, pn); r["n_features"] = len(cols)
    norm.append(r)
pd.DataFrame(norm).to_csv(f"{BASE}/_headpose.csv", index=False)

# ── write predictions back
df["physiological_model_probability"] = probs["physiological"].round(4)
df["audio_model_probability"] = probs["audio"].round(4)
df["computer_vision_model_probability"] = probs["computer_vision"].round(4)
df["fusion_model_probability"] = p_fus.round(4)
for m in ["physiological", "audio", "computer_vision"]:
    df[f"{m}_model_prediction"] = (probs[m] >= .5).astype(int)
df["fusion_model_prediction"] = (p_fus >= .5).astype(int)
df["prediction_confidence"] = (np.abs(p_fus - .5) * 2).round(4)
df["prediction_correct"] = (df.fusion_model_prediction == df.ground_truth_binary).astype(int)
df["model_version"] = "fusion_lr_v1"

df.to_csv(f"{BASE}/_stage2.csv", index=False)
pd.DataFrame(metrics).to_csv(f"{BASE}/_metrics.csv", index=False)
pd.DataFrame(ablation).to_csv(f"{BASE}/_ablation.csv", index=False)

print(pd.DataFrame(metrics).to_string(index=False))
print()
print()
print("Head-pose normalisation check:")
print(pd.DataFrame(norm)[["model", "n_features", "accuracy", "roc_auc"]].to_string(index=False))
print()
print(pd.DataFrame(ablation)[["model", "n_features", "accuracy", "precision", "recall", "f1", "roc_auc"]].to_string(index=False))
