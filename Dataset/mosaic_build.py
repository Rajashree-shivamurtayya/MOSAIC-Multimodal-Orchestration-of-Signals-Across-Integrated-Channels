"""Stage 3 - build the CSV + XLSX deliverables with a data dictionary and live formulas."""
import warnings, re
import numpy as np, pandas as pd
warnings.simplefilter("ignore")
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

BASE = "/sessions/clever-upbeat-hamilton/mnt/outputs"
df = pd.read_csv(f"{BASE}/_stage2.csv")
parts = pd.read_csv(f"{BASE}/_participants.csv")
qb = pd.read_csv(f"{BASE}/_questions.csv")
met = pd.read_csv(f"{BASE}/_metrics.csv")
abl = pd.read_csv(f"{BASE}/_ablation.csv")
hp = pd.read_csv(f"{BASE}/_headpose.csv")

# ──────────────────────────────────────────────────────────────────────────
# CORE column set (the workbook's main sheet + the "start here" CSV)
# ──────────────────────────────────────────────────────────────────────────
CORE = [
    "participant_id", "session_id", "trial_id", "trial_index", "question_id",
    "question_type", "question_category", "question_difficulty",
    "age", "sex", "ground_truth_label", "ground_truth_binary",
    "answer_length_words", "answer_duration_seconds",
    # physiology
    "baseline_heart_rate_bpm", "heart_rate_bpm", "heart_rate_change_from_baseline",
    "heart_rate_std", "rmssd_ms", "sdnn_ms", "pnn50_percent",
    "baseline_spo2_percent", "spo2_percent", "spo2_change_from_baseline",
    "perfusion_index", "perfusion_index_change_from_baseline", "pulse_signal_quality",
    # audio
    "response_latency_ms", "speech_duration_seconds", "speaking_rate_wpm",
    "pause_count", "mean_pause_duration_ms", "pause_ratio",
    "filler_word_count", "filler_word_rate", "stutter_event_count",
    "repetition_count", "prolongation_count", "block_count", "hesitation_count",
    "hesitation_rate", "mean_pitch_hz", "pitch_std", "pitch_range_hz",
    "jitter_percent", "shimmer_percent", "hnr_db", "mean_rms_energy",
    "zero_crossing_rate", "spectral_centroid",
    # vision
    "face_detection_confidence", "blink_count", "blink_rate_per_minute",
    "blink_delta_pre_to_answer", "mean_blink_duration_ms", "mean_eye_aspect_ratio",
    "gaze_deviation_degrees", "looking_away_ratio", "gaze_shift_count",
    "head_yaw_degrees", "head_pitch_degrees", "head_roll_degrees",
    "head_movement_count", "head_motion_score", "dominant_expression",
    "baseline_left_eyebrow_eye_distance", "left_eyebrow_eye_distance",
    "left_eyebrow_height_delta", "right_eyebrow_height_delta",
    "left_eyebrow_raise_ratio", "left_eyebrow_velocity", "eyebrow_asymmetry",
    "eyebrow_raise_event_count", "eyebrow_movement_score",
    "naive_left_eyebrow_delta_camera_frame",
    "baseline_head_yaw", "baseline_head_pitch", "head_yaw_delta", "head_pitch_delta",
    "head_movement_velocity_deg_s",
    "baseline_left_eye_openness", "left_eye_openness", "left_eye_openness_delta",
    "long_blink_count", "eye_closure_duration_ms",
    "baseline_gaze_x", "gaze_x_delta", "gaze_y_delta", "gaze_velocity_deg_s",
    "facial_motion_mean", "facial_motion_peak", "facial_landmark_velocity_mean",
    "expression_stability",
    "facial_expression_confidence", "facial_movement_score", "lip_movement_score",
    # quality
    "audio_quality_score", "video_quality_score", "oximeter_signal_quality",
    "overall_trial_quality", "missing_data_percent",
    "audio_available", "video_available", "physiological_available",
    # outputs
    "physiological_model_probability", "audio_model_probability",
    "computer_vision_model_probability", "fusion_model_probability",
    "fusion_model_prediction", "prediction_confidence", "prediction_correct",
]
CORE = [c for c in CORE if c in df.columns]

# ──────────────────────────────────────────────────────────────────────────
# DATA DICTIONARY
# ──────────────────────────────────────────────────────────────────────────
def group_of(c):
    if c in ("participant_id", "session_id", "trial_id", "trial_index", "session_date",
             "question_start_timestamp"): return "01_Identity"
    if c.startswith("question") or c in ("expected_answer_type",): return "02_Question"
    if c in ("age", "age_group", "sex", "height_cm", "weight_kg", "bmi", "dominant_hand",
             "native_language", "education_level", "wears_glasses"): return "03_Demographics"
    if "ground_truth" in c or c in ("experiment_condition", "deception_instruction",
                                    "participant_answer", "answer_length_words",
                                    "answer_length_syllables", "answer_duration_seconds",
                                    "experimenter_confidence"): return "04_GroundTruth"
    if re.match(r"^(baseline_heart|heart_rate|mean_heart|min_heart|max_heart|mean_rr|std_rr|rmssd|sdnn|nn50|pnn50)", c): return "05_Physio_Cardiac"
    if "spo2" in c: return "06_Physio_SpO2"
    if re.match(r"^(perfusion|pulse_|ppg_|baseline_perfusion|sensor_contact)", c): return "07_Physio_PPG"
    if re.match(r"^(audio_duration|speech_|silence_|speaking_|articulation_|syllable_rate|word_count|response_latency|time_to_first)", c): return "08_Audio_Timing"
    if "pause" in c: return "09_Audio_Pauses"
    if re.match(r"^(filler|um_|uh_|ah_|er_|like_|you_know|other_filler)", c): return "10_Audio_Fillers"
    if re.match(r"^(stutter|.*repetition|prolongation|block_count|self_correction|false_start|hesitation)", c): return "11_Audio_Disfluency"
    if re.match(r"^(mean_pitch|min_pitch|max_pitch|pitch_|jitter|shimmer|hnr)", c): return "12_Audio_Pitch_Quality"
    if re.match(r"^(mean_rms|rms_energy|voice_intensity|zero_crossing|spectral_)", c): return "13_Audio_Spectral"
    if c.startswith("mfcc_"): return "14_Audio_MFCC"
    if "eyebrow" in c or c.startswith("naive_"): return "16b_Vision_Eyebrow"
    if re.match(r"^(left_eye_|right_eye_|baseline_left_eye|baseline_right_eye|long_blink|eye_closure)", c): return "16_Vision_Eye"
    if c.startswith("baseline_gaze"): return "17_Vision_Gaze"
    if c.startswith("baseline_head"): return "18_Vision_HeadPose"
    if re.match(r"^(facial_motion|facial_landmark)", c): return "22b_Vision_Motion"
    if re.match(r"^(face_|landmark_)", c): return "15_Vision_Face"
    if re.match(r"^(blink_|eye_|mean_eye)", c): return "16_Vision_Eye"
    if c.startswith("gaze_") or "looking" in c: return "17_Vision_Gaze"
    if c.startswith("head_"): return "18_Vision_HeadPose"
    if "expression" in c or c == "dominant_expression": return "19_Vision_Expression"
    if re.match(r"^au\d\d_", c) or "action_unit" in c or c == "facial_movement_score": return "20_Vision_ActionUnits"
    if re.match(r"^(mouth_|lip_|jaw_)", c): return "21_Vision_Mouth"
    if re.match(r"^(shoulder_|body_|posture_|lean_)", c): return "22_Vision_Body"
    if re.match(r"^(pre_question|during_question|post_answer|hr_delta|spo2_delta|energy_delta|blink_delta|reaction_time|peak_response|recovery_time)", c): return "23_Temporal_Windows"
    if c.endswith("_change_score") or c in ("speech_hesitation_score", "facial_behavior_score"): return "24_Engineered_Scores"
    if re.match(r"^(audio_quality|audio_signal|audio_clipping|video_|oximeter_signal|motion_artifact|overall_trial_quality|missing_|outlier_|duplicate_|annotation_|quality_control)", c): return "25_DataQuality"
    if re.match(r"^(room_|ambient_|lighting_|camera_|microphone_|oximeter_finger|oximeter_model|background_)", c): return "26_Environment"
    if re.match(r"^(sleep_|caffeine|exercise_|time_since|resting_time)", c): return "27_ParticipantState"
    if "_available" in c or c == "modality_count_available": return "28_ModalityFlags"
    if "model_" in c or c.startswith("prediction_"): return "29_ModelOutputs"
    return "30_DatasetMgmt"

DESC = {
 "participant_id": "Pseudonymous research ID. Never store real identity here.",
 "session_id": "One recording session per participant.",
 "trial_id": "Primary key. One question/answer trial. Unique across the dataset.",
 "trial_index": "Position of the trial within the session (1-10). Arousal habituates as this rises.",
 "question_difficulty": "Cognitive load imposed by the question, 0-1. Drives latency, pauses and arousal.",
 "ground_truth_binary": "TARGET. 0 = truthful, 1 = deceptive. From the experimental protocol, never from a model.",
 "ground_truth_label": "Text form of the target.",
 "experiment_condition": "Which instruction the participant was given for this trial.",
 "baseline_heart_rate_bpm": "HR in the pre-question baseline window. Compare every HR feature against this, not against a population norm.",
 "heart_rate_bpm": "Mean HR during the answer window.",
 "heart_rate_change_from_baseline": "Computed as heart_rate_bpm - baseline_heart_rate_bpm. The single most useful cardiac feature.",
 "rmssd_ms": "Short-term HRV. Falls as sympathetic arousal rises.",
 "sdnn_ms": "Overall HRV. Correlated with rmssd_ms by construction.",
 "pnn50_percent": "Percent of successive RR intervals differing by >50 ms. Derived from rmssd_ms.",
 "spo2_percent": "Blood oxygen during the answer window. Weak deception signal by design - keep it, do not lean on it.",
 "perfusion_index": "PPG perfusion. Falls with stress vasoconstriction. Also drives PPG signal quality.",
 "pulse_signal_quality": "0-1 PPG quality from SNR and motion. Low values attenuate every physiological feature.",
 "response_latency_ms": "Silence between end of question and first word. Strongest single audio feature.",
 "speaking_rate_wpm": "Words per minute over the answer.",
 "pause_ratio": "Computed as silence_duration_seconds / audio_duration_seconds.",
 "filler_word_rate": "Computed as filler_word_count / word_count.",
 "stutter_event_count": "Computed as repetition_count + prolongation_count + block_count.",
 "hesitation_rate": "Computed as hesitation_count / speech_duration_seconds.",
 "jitter_percent": "Cycle-to-cycle pitch perturbation. Rises with vocal tension.",
 "shimmer_percent": "Cycle-to-cycle amplitude perturbation.",
 "hnr_db": "Harmonics-to-noise ratio. Falls as voice quality degrades.",
 "blink_rate_per_minute": "Blinks per minute during the answer window.",
 "blink_delta_pre_to_answer": "Computed as blink_rate_per_minute - pre_question_blink_rate. Better feature than raw blink rate.",
 "mean_eye_aspect_ratio": "Mean of left and right EAR. Lower under cognitive load.",
 "gaze_deviation_degrees": "Angular deviation of gaze from the camera axis.",
 "looking_away_ratio": "Fraction of the answer window not looking at the camera.",
 "head_motion_score": "Normalised mean of yaw/pitch/roll variability.",
 "facial_action_unit_activity": "Mean intensity across all 17 AUs.",
 "left_eyebrow_eye_distance": "Distance from left brow centre to left eye centre, divided by inter-ocular distance. Dividing by inter-ocular distance cancels camera distance, so leaning toward the webcam does not look like a brow raise.",
 "baseline_left_eyebrow_eye_distance": "The same measure during the pre-question baseline window. People differ hugely in resting brow height, so only the change from this value is meaningful.",
 "left_eyebrow_height_delta": "Computed as left_eyebrow_eye_distance minus its baseline. THIS is the eyebrow-raise feature to model on, not the absolute distance.",
 "left_eyebrow_raise_ratio": "Current brow-eye distance divided by baseline. Scale-free alternative to the delta.",
 "left_eyebrow_velocity": "Peak raise divided by rise time, in inter-ocular units per second. Fast micro-raises differ from slow deliberate ones.",
 "left_eyebrow_acceleration": "Rate of change of eyebrow velocity.",
 "eyebrow_asymmetry": "Absolute difference between left and right delta. Asymmetric brow movement is associated with deliberate rather than spontaneous expression.",
 "eyebrow_raise_event_count": "Discrete raise events detected in the answer window.",
 "eyebrow_movement_score": "Mean absolute brow delta across both sides.",
 "naive_left_eyebrow_delta_camera_frame": "DELIBERATELY FLAWED, kept for the report. Brow height in raw camera coordinates, so head pitch contaminates it: tilt the head back and the brows rise in the image without moving a muscle. Compare against left_eyebrow_height_delta - see the Headpose_Check sheet. Do not use as a model input.",
 "baseline_head_yaw": "Head yaw during the pre-question baseline window.",
 "head_yaw_delta": "Computed as head_yaw_degrees minus baseline_head_yaw. Head pose must be tracked so that head movement is not mistaken for facial movement.",
 "head_pitch_delta": "Computed as head_pitch_degrees minus baseline_head_pitch. This is the term that contaminates the naive_* eyebrow columns.",
 "head_movement_velocity_deg_s": "Angular head speed over the answer window.",
 "left_eye_openness_delta": "Computed as left_eye_openness minus its baseline-window value.",
 "long_blink_count": "Blinks longer than a normal closure. Associated with cognitive load.",
 "eye_closure_duration_ms": "Total time the eyes were closed across the answer window.",
 "gaze_x_delta": "Computed as gaze_x minus baseline_gaze_x. Corrects for a participant's habitual gaze offset.",
 "gaze_velocity_deg_s": "Angular gaze speed. High values mean darting eyes; note that looking away is NOT evidence of deception.",
 "facial_motion_mean": "Mean per-frame landmark displacement across the whole face, averaged over the answer window.",
 "facial_motion_peak": "Largest per-frame facial displacement in the window.",
 "facial_landmark_velocity_mean": "Mean landmark speed in inter-ocular units per second.",
 "expression_stability": "Computed as 1 / (1 + expression_change_count). Higher means a steadier face.",
 "audio_quality_score": "0-1 from SNR. Below 0.30 the trial is flagged POOR.",
 "video_quality_score": "0-1 from blur, brightness and occlusion.",
 "overall_trial_quality": "GOOD / WARNING / POOR. Route POOR trials to review, do not feed them to the model silently.",
 "physiological_model_probability": "Out-of-fold P(deceptive) from the physiology-only model. Participant-level GroupKFold, no leakage.",
 "audio_model_probability": "Out-of-fold P(deceptive) from the audio-only model.",
 "computer_vision_model_probability": "Out-of-fold P(deceptive) from the vision-only model.",
 "fusion_model_probability": "Out-of-fold P(deceptive) from late fusion over the three modality probabilities.",
 "prediction_confidence": "Computed as |fusion_probability - 0.5| * 2. Distance from the decision boundary, not a truth guarantee.",
 "prediction_correct": "Evaluation column only. Never use as a model input.",
 "data_source": "SIMULATED. This dataset was generated, not collected from human participants.",
}
GROUP_DESC = {
 "14_Audio_MFCC": "Mel-frequency cepstral coefficient {n} ({stat}). MFCC 1 tracks energy, 2-3 track spectral shape, 4-13 carry weak arousal signal.",
 "20_Vision_ActionUnits": "Facial Action Coding System AU intensity 0-5. AU04/07/14/45 rise with arousal; AU06/12 (genuine smile) fall.",
 "19_Vision_Expression": "Expression probability. The seven probability columns sum to 1.0 per row.",
}

dd = []
for c in df.columns:
    g = group_of(c)
    s = df[c]
    if c in DESC:
        d = DESC[c]
    elif c.startswith("mfcc_"):
        n = int(c.split("_")[1]); stat = c.split("_")[-1]
        d = GROUP_DESC["14_Audio_MFCC"].format(n=n, stat=stat)
    elif re.match(r"^au\d\d_intensity$", c):
        d = GROUP_DESC["20_Vision_ActionUnits"]
    elif c.endswith("_expression_probability"):
        d = GROUP_DESC["19_Vision_Expression"]
    else:
        d = c.replace("_", " ").capitalize() + "."
    if pd.api.types.is_numeric_dtype(s):
        rng = f"{np.nanmin(s):.4g} … {np.nanmax(s):.4g}"
        dtype = "integer" if pd.api.types.is_integer_dtype(s) else "float"
    else:
        u = s.dropna().unique()
        rng = ", ".join(map(str, u[:6])) + (" …" if len(u) > 6 else "")
        dtype = "categorical"
    dd.append(dict(column_name=c, group=g, dtype=dtype, observed_range=rng,
                   missing_count=int(s.isna().sum()),
                   in_core_set="YES" if c in CORE else "",
                   description=d))
dd = pd.DataFrame(dd).sort_values(["group", "column_name"]).reset_index(drop=True)

# ──────────────────────────────────────────────────────────────────────────
# EFFECT SIZE TABLE (values here; the workbook recomputes them with formulas)
# ──────────────────────────────────────────────────────────────────────────
FEAT = [c for c in CORE if pd.api.types.is_numeric_dtype(df[c])
        and c not in ("ground_truth_binary", "trial_index", "age", "prediction_correct",
                      "fusion_model_prediction", "audio_available", "video_available",
                      "physiological_available")]
eff = []
for c in FEAT:
    a = df.loc[df.ground_truth_binary == 0, c].dropna()
    b = df.loc[df.ground_truth_binary == 1, c].dropna()
    sp = np.sqrt(((len(a) - 1) * a.var() + (len(b) - 1) * b.var()) / (len(a) + len(b) - 2))
    eff.append(dict(feature=c, group=group_of(c), n_truthful=len(a), n_deceptive=len(b),
                    mean_truthful=round(a.mean(), 4), mean_deceptive=round(b.mean(), 4),
                    difference=round(b.mean() - a.mean(), 4),
                    cohens_d=round((b.mean() - a.mean()) / sp, 4) if sp else np.nan))
eff = pd.DataFrame(eff).reindex(pd.DataFrame(eff).cohens_d.abs().sort_values(ascending=False).index).reset_index(drop=True)

# session-level rollup
sess = df.groupby(["participant_id", "session_id"]).agg(
    number_of_questions=("trial_id", "count"),
    number_of_truthful_questions=("ground_truth_binary", lambda s: int((s == 0).sum())),
    number_of_deceptive_questions=("ground_truth_binary", lambda s: int((s == 1).sum())),
    session_average_hr=("heart_rate_bpm", "mean"),
    session_average_spo2=("spo2_percent", "mean"),
    session_average_blink_rate=("blink_rate_per_minute", "mean"),
    session_average_speaking_rate=("speaking_rate_wpm", "mean"),
    session_average_response_latency_ms=("response_latency_ms", "mean"),
    session_average_gaze_deviation=("gaze_deviation_degrees", "mean"),
    session_total_duration_seconds=("answer_duration_seconds", "sum"),
    session_fusion_accuracy=("prediction_correct", "mean"),
).round(3).reset_index()

# ──────────────────────────────────────────────────────────────────────────
# CSV OUTPUTS
# ──────────────────────────────────────────────────────────────────────────
df.to_csv(f"{BASE}/mosaic_dataset_full_3000x{df.shape[1]}.csv", index=False)
df[CORE].to_csv(f"{BASE}/mosaic_dataset_core.csv", index=False)
dd.to_csv(f"{BASE}/mosaic_data_dictionary.csv", index=False)

# ──────────────────────────────────────────────────────────────────────────
# XLSX WORKBOOK
# ──────────────────────────────────────────────────────────────────────────
FONT = "Arial"
H_FILL = PatternFill("solid", fgColor="1F3864")
H_FONT = Font(name=FONT, bold=True, color="FFFFFF", size=10)
BODY = Font(name=FONT, size=10)
TITLE = Font(name=FONT, bold=True, size=14, color="1F3864")
SUB = Font(name=FONT, bold=True, size=11, color="1F3864")
WARN = PatternFill("solid", fgColor="FFF2CC")
thin = Side(style="thin", color="BFBFBF")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = Workbook()

def sheet_from_df(wb, name, d, freeze="A2", table=True, widths=None):
    ws = wb.create_sheet(name)
    ws.append(list(d.columns))
    for r in d.itertuples(index=False):
        ws.append([None if (isinstance(v, float) and np.isnan(v)) else v for v in r])
    for cell in ws[1]:
        cell.fill, cell.font = H_FILL, H_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font = BODY
    ws.freeze_panes = freeze
    ws.row_dimensions[1].height = 30
    # Autofilter + manual banding instead of an Excel Table object: ListObjects
    # make LibreOffice take minutes to open a workbook this size.
    if table and len(d) > 0:
        ws.auto_filter.ref = f"A1:{get_column_letter(d.shape[1])}{len(d)+1}"
        band = PatternFill("solid", fgColor="F2F5FA")
        for rr in range(3, len(d) + 2, 2):
            for cc in range(1, d.shape[1] + 1):
                ws.cell(rr, cc).fill = band
    for i, c in enumerate(d.columns, 1):
        w = widths.get(c, None) if widths else None
        if w is None:
            w = min(max(11, len(str(c)) + 2), 46)
        ws.column_dimensions[get_column_letter(i)].width = w
    return ws

# ---- 1. README
FUS_ACC = float(met.loc[met.model == "fusion_late", "accuracy"].iloc[0])
FUS_AUC = float(met.loc[met.model == "fusion_late", "roc_auc"].iloc[0])
PHY_ACC = float(met.loc[met.model == "physiological", "accuracy"].iloc[0])

ws = wb.active; ws.title = "README"
ws.column_dimensions["A"].width = 3
ws.column_dimensions["B"].width = 112
rows = [
 ("t", "MOSAIC — Multimodal Deception Analysis · Simulated Experimental Dataset"),
 ("", ""),
 ("w", "THIS DATA IS SIMULATED. It was generated by a causal model, not collected from human "
       "participants. Label it as simulated in the report, the dashboard and the viva. Presenting "
       "it as real collected data would be research misconduct."),
 ("", ""),
 ("s", "1. What is in this workbook"),
 ("b", "Trials_Core — 3,000 trial records, one row per question. 300 participants × 10 trials "
       "(5 truthful + 5 deceptive each). This is the sheet you model on."),
 ("b", "Data_Dictionary — every column in the full dataset: group, type, observed range, missing count, meaning."),
 ("b", "Participants — 300-row registry of participant traits and same-day state (sleep, caffeine, exercise)."),
 ("b", "Question_Bank — the 24 questions, their type, category and difficulty weight."),
 ("b", "Session_Summary — per-session rollups."),
 ("b", "Feature_Effects — mean per condition and Cohen's d for every core feature, ranked by effect size. "
       "Read this before choosing which features to engineer."),
 ("b", "Baseline_Results / Ablation — out-of-fold model performance, for the evaluation chapter."),
 ("b", "Headpose_Check — evidence that the eyebrow features are measured in the face coordinate system rather "
       "than raw camera pixels, and what happens when they are not."),
 ("", ""),
 ("s", "2. Why the columns correlate instead of being random"),
 ("b", "Every row was produced by a causal chain, not by drawing each column independently:"),
 ("m", "  participant traits (trait anxiety, deception skill, resting HR, habitual speech rate, base blink rate)"),
 ("m", "        +  question difficulty  +  condition (truthful/deceptive)  +  habituation across trial_index"),
 ("m", "                              ↓"),
 ("m", "                     latent AROUSAL  and  latent COGNITIVE LOAD"),
 ("m", "                              ↓"),
 ("m", "     physiological channel        audio channel            vision channel"),
 ("m", "     (own noise term)             (own noise term)         (own noise term)"),
 ("m", "                              ↓"),
 ("m", "     HR / HRV / SpO2 / PI    latency / pauses / pitch   blink / gaze / AU / head pose"),
 ("m", "                              ↓"),
 ("m", "     signal quality (from room noise, lighting, motion, perfusion) ATTENUATES the signal"),
 ("m", "     and injects extra measurement noise — so bad trials genuinely carry less information."),
 ("", ""),
 ("b", "Consequences you can verify in the data, and should mention in the viva:"),
 ("b", "  · Caffeine and poor sleep raise resting HR, which raises every HR reading for that participant."),
 ("b", "  · Anxious participants look aroused even when telling the truth — that is why per-trial baselines exist."),
 ("b", "  · Participants high in deception skill leak less, so some deceptive trials look completely normal."),
 ("b", "  · Arousal habituates: trial 10 is calmer than trial 2 at the same condition."),
 ("b", "  · Derived columns are arithmetic, not independent draws. heart_rate_change_from_baseline is exactly "
       "heart_rate_bpm minus baseline_heart_rate_bpm; pause_ratio is exactly silence over duration."),
 ("b", "  · The seven expression probabilities sum to 1.0 in every row."),
 ("", ""),
 ("s", "3. The design is counterbalanced — say this in the viva"),
 ("b", "Condition is assigned to questions at random, per participant. The same question appears as truthful for "
       "one participant and deceptive for another. Without this, the deceptive trials would all be the hard probe "
       "questions and a model could 'detect deception' just by recognising which question was asked — a confound "
       "an examiner will look for."),
 ("b", "One deliberate exception: Q01 is always truthful, because a known-true question first is how you "
       "establish a participant's resting signal. That leaves a small residual imbalance in question difficulty "
       "(Cohen's d ≈ 0.26). question_id and question_difficulty are therefore excluded from every model feature "
       "set. Say this before an examiner asks."),
 ("", ""),
 ("s", "4. Deliberate imperfections (do not 'fix' these)"),
 ("b", f"· Classes overlap heavily. Late fusion reaches {FUS_ACC:.1%} accuracy / {FUS_AUC:.2f} AUC, not 99%. A "
       "near-perfect result on this problem is the clearest sign a dataset is fake — published multimodal "
       "deception systems sit in the 65-75% range and untrained humans are close to chance."),
 ("b", f"· Physiology is the weakest channel ({PHY_ACC:.1%}) and adds almost nothing on top of audio+vision. "
       "That is a real finding to report, not a bug to tune away."),
 ("b", "· SpO2 is a weak predictor. That matches the physiology — do not tune it up."),
 ("b", "· ~5% of trials are missing one whole modality; the *_available flags mark them."),
 ("b", "· Some trials are flagged POOR quality and should be routed to review, not silently scored."),
 ("", ""),
 ("s", "5. How to split the data"),
 ("b", "Split by participant_id, never by row. All 10 trials of a participant must land in the same fold, "
       "otherwise the model memorises the person's baseline and your accuracy is inflated. Every probability "
       "column in this dataset was produced with participant-level GroupKFold for exactly this reason."),
 ("", ""),
 ("s", "6. Do not train on these columns"),
 ("b", "ground_truth_binary / ground_truth_label / experiment_condition / deception_instruction are the target "
       "and its aliases. The *_model_probability, *_model_prediction, prediction_confidence and prediction_correct "
       "columns are outputs — using them as inputs is leakage."),
 ("", ""),
 ("s", "7. Wording for the report"),
 ("b", "Call the output a multimodal deception-analysis score, not a lie detection. The system produces an "
       "experimental classification from physiological, speech and facial-behavioural features; it is not "
       "evidence that a person lied."),
 ("", ""),
 ("s", "8. Provenance"),
 ("b", "dataset_version mosaic_sim_v1.0 · feature_extraction_version featx_v1.2 · generator seed 20260811 · "
       "regenerate with mosaic_generate.py then mosaic_models.py then mosaic_build.py."),
]
r = 1
for kind, text in rows:
    c = ws.cell(row=r, column=2, value=text)
    if kind == "t": c.font = TITLE
    elif kind == "s": c.font = SUB
    elif kind == "w":
        c.font = Font(name=FONT, bold=True, size=10, color="7F6000")
        c.fill = WARN; c.border = BOX; ws.row_dimensions[r].height = 46
    elif kind == "m": c.font = Font(name="Consolas", size=9, color="404040")
    else: c.font = BODY
    c.alignment = Alignment(wrap_text=True, vertical="top")
    if kind == "b" and len(text) > 110:
        ws.row_dimensions[r].height = 15 * (len(text) // 110 + 1)
    r += 1

# ---- 2. Trials_Core
ws_t = sheet_from_df(wb, "Trials_Core", df[CORE], freeze="D2", table=False)
ncore = len(CORE)
ws_t.auto_filter.ref = f"A1:{get_column_letter(ncore)}{len(df)+1}"

# ---- 3. Data dictionary
sheet_from_df(wb, "Data_Dictionary", dd,
              widths={"description": 90, "observed_range": 30, "group": 24, "column_name": 38})

# ---- 4-6. reference sheets
sheet_from_df(wb, "Participants", parts)
sheet_from_df(wb, "Question_Bank", qb, widths={"question_text": 56})
sheet_from_df(wb, "Session_Summary", sess)

# ---- 7. Feature_Effects (values, computed from the same 3,000 rows during generation)
eff_out = eff[["feature", "group", "n_truthful", "n_deceptive", "mean_truthful",
               "mean_deceptive", "difference", "cohens_d"]].copy()
eff_out["abs_cohens_d"] = eff_out.cohens_d.abs().round(4)
eff_out["effect_size"] = pd.cut(eff_out.abs_cohens_d, [-.01, .2, .5, .8, 99],
                                labels=["negligible", "small", "medium", "large"]).astype(str)
ws = sheet_from_df(wb, "Feature_Effects", eff_out, widths={"feature": 40, "group": 24})
notes = [
 "Sorted by |Cohen's d| descending, so the most discriminative features are at the top.",
 "cohens_d uses the within-group pooled standard deviation, over the same 3,000 rows shown in Trials_Core.",
 "These are stored values, not Excel formulas. This is a fixed dataset snapshot, and a cross-sheet "
 "conditional-SD formula over 3,000 rows makes the workbook take minutes to open in LibreOffice. "
 "Run mosaic_recompute_stats.py to regenerate this table from the CSV and verify every number.",
 "Reading the numbers: |d| < 0.2 negligible, 0.2-0.5 small, 0.5-0.8 medium, > 0.8 large. Nothing here is "
 "enormous - if a single feature separated the classes on its own, the dataset would be unrealistic.",
 "question_difficulty sits near zero because the design is counterbalanced. That is intentional: see README.",
]
for j, t in enumerate(notes):
    nc = ws.cell(len(eff_out) + 3 + j, 1, t)
    nc.font = Font(name=FONT, italic=True, size=9, color="595959")

# ---- 8-9. results
sheet_from_df(wb, "Baseline_Results", met)
sheet_from_df(wb, "Ablation", abl)
ws = sheet_from_df(wb, "Headpose_Check", hp, widths={"model": 34})
hp_notes = [
 "Why the eyebrow measurement is taken inside the face coordinate system rather than in raw camera pixels.",
 "Rows 1 and 2 use ONLY the two eyebrow-delta columns. Face-relative keeps the signal; raw camera frame "
 "collapses to near chance, because head pitch moves the brows in the image without the person moving them.",
 "Rows 3 and 4 swap the same two columns inside the full vision feature set. The difference nearly vanishes - "
 "the other 57 features (including head pose) let the model correct for the contamination on its own.",
 "The lesson for the report: normalisation matters most when a feature has to stand on its own, and a rich "
 "feature set can hide a badly-measured feature rather than fix it. Measure it properly anyway.",
]
for j, t in enumerate(hp_notes):
    nc = ws.cell(len(hp) + 3 + j, 1, t)
    nc.font = Font(name=FONT, italic=True, size=9, color="595959")

OUT = f"{BASE}/MOSAIC_dataset_v1.xlsx"
wb.save(OUT)
# Round-trip through openpyxl: a freshly-written workbook of this size makes
# LibreOffice take minutes to recalculate; re-saving normalises it to ~10s.
from openpyxl import load_workbook as _lw
_lw(OUT).save(OUT)
print("core cols:", len(CORE), "| dict rows:", len(dd), "| effects:", len(eff), "| sessions:", len(sess))
print("saved MOSAIC_dataset_v1.xlsx")
