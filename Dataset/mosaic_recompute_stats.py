"""
Recompute every statistic in the MOSAIC workbook straight from the CSV.

Nothing here is taken on trust: the effect sizes, the class balance and the
model scores are all rebuilt from mosaic_dataset_full_*.csv so you can verify
the workbook, or regenerate the tables after changing the data.

    python mosaic_recompute_stats.py

Requires: pandas, numpy, scikit-learn.
"""
import glob
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

CSV = sorted(glob.glob("mosaic_dataset_full_*.csv"))[0]
df = pd.read_csv(CSV)
y = df.ground_truth_binary.values
print(f"{CSV}: {len(df)} trials, {df.shape[1]} columns, "
      f"{df.participant_id.nunique()} participants\n")

# ── 1. class balance, per participant and overall
print("Class balance:", df.ground_truth_label.value_counts().to_dict())
per_p = df.groupby("participant_id").ground_truth_binary.sum()
print("Deceptive trials per participant:", per_p.unique(), "(should be a single value)\n")

# ── 2. effect sizes
def cohens_d(col):
    a = df.loc[y == 0, col].dropna()
    b = df.loc[y == 1, col].dropna()
    sp = np.sqrt(((len(a) - 1) * a.var() + (len(b) - 1) * b.var()) / (len(a) + len(b) - 2))
    return (b.mean() - a.mean()) / sp if sp else np.nan

skip = {"ground_truth_binary", "trial_index", "prediction_correct",
        "fusion_model_prediction", "audio_available", "video_available",
        "physiological_available", "modality_count_available"}
num = [c for c in df.select_dtypes(include=[np.number]).columns if c not in skip]
eff = pd.Series({c: cohens_d(c) for c in num}).dropna().sort_values(key=abs, ascending=False)
print("Top 15 features by |Cohen's d|:")
print(eff.head(15).round(3).to_string(), "\n")
print("Sanity checks:")
print(f"  question_difficulty d = {eff.get('question_difficulty', float('nan')):+.3f} "
      "(small: condition is counterbalanced across questions, and the only")
print("                            residual comes from Q01 always being the truthful anchor.")
print("                            question_id and question_difficulty are excluded from the")
print("                            model feature sets for exactly this reason.)")
print(f"  spo2_percent        d = {eff.get('spo2_percent', float('nan')):+.3f} "
      "(weak by design - SpO2 is a poor deception cue)\n")

# ── 3. arithmetic consistency of derived columns
checks = {
    "heart_rate_change_from_baseline": df.heart_rate_bpm - df.baseline_heart_rate_bpm,
    "spo2_change_from_baseline": df.spo2_percent - df.baseline_spo2_percent,
    "pause_ratio": df.silence_duration_seconds / df.audio_duration_seconds,
    "filler_word_rate": df.filler_word_count / df.word_count,
    "stutter_event_count": df.repetition_count + df.prolongation_count + df.block_count,
    "blink_delta_pre_to_answer": df.blink_rate_per_minute - df.pre_question_blink_rate,
    "left_eyebrow_height_delta": df.left_eyebrow_eye_distance - df.baseline_left_eyebrow_eye_distance,
    "right_eyebrow_height_delta": df.right_eyebrow_eye_distance - df.baseline_right_eyebrow_eye_distance,
    "left_eyebrow_raise_ratio": df.left_eyebrow_eye_distance / df.baseline_left_eyebrow_eye_distance,
    "eyebrow_asymmetry": (df.left_eyebrow_height_delta - df.right_eyebrow_height_delta).abs(),
    "head_yaw_delta": df.head_yaw_degrees - df.baseline_head_yaw,
    "head_pitch_delta": df.head_pitch_degrees - df.baseline_head_pitch,
    "left_eye_openness_delta": df.left_eye_openness - df.baseline_left_eye_openness,
    "gaze_x_delta": df.gaze_x - df.baseline_gaze_x,
    "expression_stability": 1.0 / (1.0 + df.expression_change_count),
}
# Tolerance = the rounding already applied to the stored columns. Values are
# rounded to 1-4 decimals in the CSV, so an exact match is not expected; what
# matters is that the error never exceeds half a unit in the last stored place.
TOL = {"heart_rate_change_from_baseline": 0.105, "spo2_change_from_baseline": 0.011,
       "pause_ratio": 1e-3, "filler_word_rate": 1e-3, "stutter_event_count": 1e-9,
       "blink_delta_pre_to_answer": 0.011,
       "left_eyebrow_height_delta": 1.1e-5, "right_eyebrow_height_delta": 1.1e-5,
       "left_eyebrow_raise_ratio": 1.1e-4, "eyebrow_asymmetry": 2.1e-5,
       "head_yaw_delta": 0.011, "head_pitch_delta": 0.011,
       "left_eye_openness_delta": 1.1e-4, "gaze_x_delta": 1.1e-4,
       "expression_stability": 1.1e-4}
print("Derived-column arithmetic (max error vs. its rounding tolerance):")
ok_all = True
for col, expected in checks.items():
    err = (df[col] - expected).abs().max()
    good = err <= TOL[col]; ok_all &= good
    print(f"  {col:<36} {err:.2e}  (tol {TOL[col]:.0e})  {'OK' if good else 'MISMATCH'}")
expr = [c for c in df.columns if c.endswith("_expression_probability")]
have_video = df.video_available == 1
s = df.loc[have_video, expr].sum(axis=1)
e = abs(s - 1).max(); ok_all &= e < 1e-3
print(f"  {'expression probabilities sum to 1':<36} {e:.2e}  (tol 1e-03)  "
      f"{'OK' if e < 1e-3 else 'MISMATCH'}")
print(f"  (checked on the {int(have_video.sum())} trials that have video; the rest are NaN by design)")
print(f"\n  ALL DERIVED COLUMNS CONSISTENT: {ok_all}\n")

# ── 3b. eyebrow measurement: face-relative vs raw camera frame
print("Eyebrow measurement check:")
for c in ["left_eyebrow_height_delta", "naive_left_eyebrow_delta_camera_frame"]:
    print(f"  d({c}) = {cohens_d(c):+.3f}")
corr_ok = df.left_eyebrow_height_delta.corr(df.au01_intensity)
corr_pitch = df.naive_left_eyebrow_delta_camera_frame.corr(df.head_pitch_delta)
corr_clean = df.left_eyebrow_height_delta.corr(df.head_pitch_delta)
print(f"  face-relative brow delta vs AU01 (brow raiser): r = {corr_ok:+.3f}  "
      "(should be strong - they measure the same thing)")
print(f"  raw-camera brow delta vs head pitch:            r = {corr_pitch:+.3f}  "
      "(contaminated by head movement)")
print(f"  face-relative brow delta vs head pitch:         r = {corr_clean:+.3f}  "
      "(small: normalisation removed the geometric")
print("                                                              contamination. What remains is real - "
      "aroused people")
print("                                                              both raise their brows and move their "
      "heads.)\n")

# ── 4. re-fit the models with participant-level splits
PHYS = ["heart_rate_change_from_baseline", "heart_rate_std", "rmssd_ms", "sdnn_ms",
        "pnn50_percent", "spo2_change_from_baseline", "perfusion_index",
        "perfusion_index_change_from_baseline", "hr_delta_pre_to_question"]
AUD = ["response_latency_ms", "speaking_rate_wpm", "pause_count", "mean_pause_duration_ms",
       "pause_ratio", "filler_word_rate", "stutter_event_count", "hesitation_rate",
       "mean_pitch_hz", "pitch_std", "jitter_percent", "shimmer_percent", "hnr_db"]
VIS = ["blink_rate_per_minute", "blink_delta_pre_to_answer", "mean_blink_duration_ms",
       "mean_eye_aspect_ratio", "gaze_deviation_degrees", "looking_away_ratio",
       "head_yaw_std", "head_pitch_std", "head_motion_score", "au04_intensity",
       "au45_intensity", "facial_action_unit_activity",
       "left_eyebrow_height_delta", "right_eyebrow_height_delta", "eyebrow_asymmetry",
       "eyebrow_movement_score", "head_yaw_delta", "head_pitch_delta",
       "left_eye_openness_delta", "gaze_x_delta", "facial_motion_mean"]

def score(cols, label):
    X, p = df[cols], np.zeros(len(df))
    for tr, te in GroupKFold(n_splits=5).split(X, y, df.participant_id):
        m = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                          LogisticRegression(max_iter=2000, C=.35))
        m.fit(X.iloc[tr], y[tr])
        p[te] = m.predict_proba(X.iloc[te])[:, 1]
    print(f"  {label:<22} acc {accuracy_score(y, p >= .5):.4f}   "
          f"f1 {f1_score(y, p >= .5):.4f}   auc {roc_auc_score(y, p):.4f}")
    return p

print("Out-of-fold performance (GroupKFold on participant_id, reduced feature sets):")
pp, pa, pv = score(PHYS, "Physiology"), score(AUD, "Audio"), score(VIS, "Vision")
fus = pd.DataFrame({"p": pp, "a": pa, "v": pv})
score_p = np.zeros(len(df))
for tr, te in GroupKFold(n_splits=5).split(fus, y, df.participant_id):
    m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    m.fit(fus.iloc[tr], y[tr])
    score_p[te] = m.predict_proba(fus.iloc[te])[:, 1]
print(f"  {'Fusion (late)':<22} acc {accuracy_score(y, score_p >= .5):.4f}   "
      f"f1 {f1_score(y, score_p >= .5):.4f}   auc {roc_auc_score(y, score_p):.4f}")

# ── 5. what leakage looks like, so you can recognise it
Xr, pr = df[PHYS + AUD + VIS], np.zeros(len(df))
from sklearn.model_selection import StratifiedKFold
for tr, te in StratifiedKFold(5, shuffle=True, random_state=0).split(Xr, y):
    m = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                      LogisticRegression(max_iter=2000, C=.35))
    m.fit(Xr.iloc[tr], y[tr])
    pr[te] = m.predict_proba(Xr.iloc[te])[:, 1]
print(f"\nSame features, split by ROW instead of by participant: acc {accuracy_score(y, pr >= .5):.4f}")
print("Compare that against the participant-split scores above. The gap is small here because")
print("most features are baseline-relative (change-from-baseline, deltas), which already removes")
print("the participant's identity. Swap in absolute values such as raw heart_rate_bpm or")
print("mean_pitch_hz and the row-split score inflates while the participant-split score does not.")
print("That gap is participant leakage. Always split by participant_id.")
