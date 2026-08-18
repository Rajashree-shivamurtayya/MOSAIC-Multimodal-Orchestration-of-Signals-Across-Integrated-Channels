"""
MOSAIC - Multimodal Deception Analysis
Synthetic experimental dataset generator.

IMPORTANT: This produces SIMULATED data for software/ML pipeline validation.
It is NOT collected from human participants and must be labelled as simulated
in any report, dashboard or viva.

Generative structure (causal, not independent random columns):

  participant traits ─┐
  question difficulty ├──> latent AROUSAL ──┬──> physiological latent ──> HR / HRV / SpO2 / PI
  condition (T/D)     │                     ├──> audio latent        ──> pauses / pitch / jitter
  habituation         ┘                     └──> vision latent       ──> blink / gaze / AU
                        cognitive load ─────────> response latency / fillers / stutter
  environment ──> signal quality ──> attenuates every modality's signal + adds noise

Every "derived" column (deltas, ratios, counts) is COMPUTED from its parents,
never drawn independently.
"""

import warnings
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

warnings.simplefilter("ignore")

RNG = np.random.default_rng(20260811)
N_PARTICIPANTS = 300
TRIALS_PER_PARTICIPANT = 10          # 5 truthful + 5 deceptive
DATASET_VERSION = "mosaic_sim_v1.0"
FEATURE_VERSION = "featx_v1.2"

z = lambda n: RNG.normal(0, 1, n)
clip = np.clip


# ──────────────────────────────────────────────────────────────────────────
# 1. QUESTION BANK
# ──────────────────────────────────────────────────────────────────────────
# difficulty 0..1 = cognitive load the question imposes
QUESTION_BANK = [
    # (qid, text, type, category, difficulty, expected_answer_type, condition_role)
    ("Q01", "Please state your first name.",                              "short_answer", "control",       0.05, "text",   "truth_only"),
    ("Q02", "What day of the week is it today?",                          "short_answer", "control",       0.05, "text",   "truth_only"),
    ("Q03", "Are you currently seated?",                                  "yes_no",       "control",       0.05, "binary", "truth_only"),
    ("Q04", "Is the room light on?",                                      "yes_no",       "control",       0.05, "binary", "truth_only"),
    ("Q05", "What city were you born in?",                                "short_answer", "personal",      0.20, "text",   "either"),
    ("Q06", "How many siblings do you have?",                             "short_answer", "personal",      0.20, "text",   "either"),
    ("Q07", "Do you own a two-wheeler?",                                  "yes_no",       "personal",      0.25, "binary", "either"),
    ("Q08", "What is your favourite subject this semester?",              "short_answer", "personal",      0.25, "text",   "either"),
    ("Q09", "What colour was the folder on the table in room 2?",         "yes_no",       "memory_based",  0.55, "binary", "either"),
    ("Q10", "Did you see anyone else in the corridor?",                   "yes_no",       "memory_based",  0.50, "binary", "either"),
    ("Q11", "Describe what you did in the previous room.",                "open_ended",   "memory_based",  0.70, "text",   "either"),
    ("Q12", "How long were you alone in that room?",                      "short_answer", "memory_based",  0.60, "text",   "either"),
    ("Q13", "What is the capital of Karnataka?",                          "short_answer", "knowledge",     0.15, "text",   "either"),
    ("Q14", "How many days are there in February this year?",             "short_answer", "knowledge",     0.20, "text",   "either"),
    ("Q15", "Did you take the blue file from the desk?",                  "yes_no",       "probe",         0.80, "binary", "deceptive_bias"),
    ("Q16", "Did you open the drawer?",                                   "yes_no",       "probe",         0.75, "binary", "deceptive_bias"),
    ("Q17", "Do you know where the missing item is now?",                 "yes_no",       "probe",         0.85, "binary", "deceptive_bias"),
    ("Q18", "Explain exactly how you spent the last ten minutes.",        "open_ended",   "probe",         0.90, "text",   "deceptive_bias"),
    ("Q19", "Have you told me the complete truth so far?",                "yes_no",       "probe",         0.80, "binary", "deceptive_bias"),
    ("Q20", "Is there anything about this task you have not mentioned?",  "open_ended",   "probe",         0.85, "text",   "deceptive_bias"),
    ("Q21", "Would anyone else confirm your account of events?",          "yes_no",       "probe",         0.70, "binary", "either"),
    ("Q22", "Did you touch anything on the shelf?",                       "yes_no",       "probe",         0.70, "binary", "deceptive_bias"),
    ("Q23", "What was written on the envelope?",                          "short_answer", "memory_based",  0.65, "text",   "either"),
    ("Q24", "Are you comfortable continuing the session?",                "yes_no",       "control",       0.10, "binary", "truth_only"),
]
QB = pd.DataFrame(QUESTION_BANK, columns=[
    "question_id", "question_text", "question_type", "question_category",
    "question_difficulty", "expected_answer_type", "typical_use"])
QB["condition_assignment"] = "counterbalanced (random per participant)"
QB.loc[QB.question_id == "Q01", "condition_assignment"] = "always truthful (baseline anchor)"
QMAP = QB.set_index("question_id").to_dict("index")

# expected words by answer type (drives duration, mouth movement, MFCC stability...)
BASE_WORDS = {"yes_no": 2.2, "short_answer": 5.0, "open_ended": 26.0}


# ──────────────────────────────────────────────────────────────────────────
# 2. PARTICIPANT-LEVEL TRAITS
# ──────────────────────────────────────────────────────────────────────────
n = N_PARTICIPANTS
pid = [f"P{i:03d}" for i in range(1, n + 1)]

age = clip(RNG.normal(23.5, 5.2, n), 18, 55).round(0)
sex = RNG.choice(["M", "F"], n, p=[0.53, 0.47])
is_f = (sex == "F").astype(float)
height = np.where(is_f == 1, RNG.normal(160, 6.2, n), RNG.normal(172, 6.8, n)).round(1)
bmi = clip(RNG.normal(22.6, 3.4, n), 16, 36)
weight = (bmi * (height / 100) ** 2).round(1)

trait_anxiety = z(n)                       # STAI-like latent, standardised
deception_skill = z(n)                     # good liars leak less
fitness = clip(RNG.normal(0, 1, n) - 0.25 * (bmi - 22.6) / 3.4, -3, 3)
base_disfluency = clip(RNG.gamma(2.2, 0.45, n), 0.15, 4.0)   # trait stutter/filler tendency
skin_perfusion = clip(RNG.normal(0, 1, n), -3, 3)            # affects PPG quality & PI

# resting physiology from traits
base_hr_p = clip(64 + 0.10 * (age - 23.5) + 3.6 * is_f + 4.2 * trait_anxiety
                 - 3.0 * fitness + RNG.normal(0, 4.2, n), 48, 96)
base_rmssd_p = clip(52 - 0.55 * (age - 20) + 7 * fitness - 5 * trait_anxiety
                    + RNG.normal(0, 8, n), 10, 105)
base_spo2_p = clip(RNG.normal(97.6, 0.75, n), 94.5, 100)
base_pi_p = clip(np.exp(RNG.normal(1.05, 0.45, n)) + 0.6 * skin_perfusion, 0.3, 14)

# speech traits
base_speech_rate_p = clip(RNG.normal(158, 17, n), 105, 215)
base_pitch_p = np.where(is_f == 1, RNG.normal(208, 17, n), RNG.normal(118, 13, n))
base_latency_p = clip(RNG.normal(620, 170, n), 220, 1500)
base_intensity_p = clip(RNG.normal(63.5, 3.2, n), 54, 74)

# vision traits
base_blink_p = clip(RNG.normal(16.5, 4.6, n), 6, 34)
base_ear_p = clip(RNG.normal(0.288, 0.022, n), 0.21, 0.36)
base_lookaway_p = clip(RNG.beta(2.2, 9.0, n), 0.01, 0.60)
wears_glasses = RNG.choice([0, 1], n, p=[0.62, 0.38])

# facial anatomy: brow-to-eye distance is measured in units of inter-ocular
# distance, so it is scale-free (independent of camera distance). People differ
# enormously here - naturally high brows vs low brows - which is exactly why the
# model must use the change from a personal baseline, not the absolute value.
base_brow_eye_p = clip(RNG.normal(0.42, 0.055, n), 0.24, 0.62)
brow_expressive_p = clip(RNG.normal(1.0, 0.30, n), 0.30, 2.4)   # how much they move brows
brow_asym_p = RNG.normal(0, 0.013, n)                            # natural L-R difference
base_gaze_x_p = RNG.normal(0, 0.055, n)                          # habitual gaze offset
base_gaze_y_p = RNG.normal(0, 0.045, n)

# state-of-day variables
sleep_hours = clip(RNG.normal(6.8, 1.3, n), 3.0, 10.5).round(1)
caffeine = RNG.choice([0, 1], n, p=[0.55, 0.45])
caffeine_mg = np.where(caffeine == 1, clip(RNG.normal(95, 45, n), 20, 260).round(0), 0)
exercise_before = RNG.choice([0, 1], n, p=[0.82, 0.18])
mins_since_exercise = np.where(exercise_before == 1,
                               clip(RNG.normal(75, 45, n), 10, 300).round(0), np.nan)
mins_since_meal = clip(RNG.normal(150, 90, n), 15, 480).round(0)
rest_before_min = clip(RNG.normal(6, 2.2, n), 2, 15).round(1)

# state modifies resting HR (real, measurable cross-correlation in the data)
state_hr_shift = (0.030 * caffeine_mg
                  + np.where(exercise_before == 1, 9.0 * np.exp(-np.nan_to_num(mins_since_exercise, nan=999) / 70), 0)
                  - 0.55 * (sleep_hours - 6.8))
session_base_hr = clip(base_hr_p + state_hr_shift, 48, 118)

education = RNG.choice(["UG_year_2", "UG_year_3", "UG_year_4", "PG"], n, p=[.28, .40, .24, .08])
native_lang = RNG.choice(["Kannada", "Hindi", "Telugu", "Tamil", "Malayalam", "English"],
                         n, p=[.42, .18, .14, .11, .08, .07])
dominant_hand = RNG.choice(["right", "left"], n, p=[.90, .10])

participants = pd.DataFrame(dict(
    participant_id=pid, age=age.astype(int), sex=sex, height_cm=height, weight_kg=weight,
    bmi=bmi.round(1), dominant_hand=dominant_hand, native_language=native_lang,
    education_level=education, wears_glasses=wears_glasses,
    trait_anxiety_z=trait_anxiety.round(3), deception_skill_z=deception_skill.round(3),
    resting_hr_bpm=base_hr_p.round(1), resting_rmssd_ms=base_rmssd_p.round(1),
    resting_spo2_percent=base_spo2_p.round(1), resting_perfusion_index=base_pi_p.round(2),
    habitual_speech_rate_wpm=base_speech_rate_p.round(1),
    habitual_pitch_hz=base_pitch_p.round(1), habitual_blink_rate=base_blink_p.round(1),
    sleep_duration_hours=sleep_hours, caffeine_consumed=caffeine,
    caffeine_amount_mg=caffeine_mg, exercise_before_test=exercise_before,
    time_since_exercise_minutes=mins_since_exercise,
    time_since_last_meal_minutes=mins_since_meal,
    resting_time_before_test_minutes=rest_before_min,
))


# ──────────────────────────────────────────────────────────────────────────
# 3. TRIAL SCHEDULE  (each participant: 5 truthful + 5 deceptive, control first)
# ──────────────────────────────────────────────────────────────────────────
rows = []
start_day = datetime(2026, 1, 12, 9, 30)

for i in range(n):
    p = pid[i]
    sess = f"S{i + 1:03d}"
    # environment is a session property
    room_temp = round(float(RNG.normal(25.5, 1.8)), 1)
    humidity = round(float(clip(RNG.normal(58, 9), 30, 85)), 1)
    ambient_noise = round(float(clip(RNG.normal(41, 6.5), 28, 66)), 1)
    lighting = round(float(clip(RNG.normal(320, 90), 90, 620)), 0)
    cam_dist = round(float(clip(RNG.normal(62, 9), 40, 95)), 1)
    cam_angle = round(float(RNG.normal(0, 6.5)), 1)
    mic_dist = round(float(clip(RNG.normal(35, 8), 18, 60)), 1)
    finger = RNG.choice(["left_index", "right_index", "left_middle"], p=[.5, .35, .15])
    background = RNG.choice(["plain_wall", "lab_bench", "curtain"], p=[.6, .28, .12])

    # COUNTERBALANCED DESIGN: condition is assigned to questions at random, so
    # question difficulty is NOT confounded with the label. Without this, a model
    # could "detect deception" purely by recognising which question was asked.
    # Q01 is always the truthful baseline anchor (standard practice: a known-true
    # question first, to establish the participant's resting signal).
    pool = [q for q in QB.question_id if q != "Q01"]
    picked = list(RNG.choice(pool, 9, replace=False))
    RNG.shuffle(picked)
    t_dec = picked[:5]                       # 5 deceptive
    t_truth = ["Q01"] + picked[5:]           # 1 anchor + 4 truthful

    order = ["Q01"] + list(RNG.permutation(picked))
    labels = [0] + [1 if q in t_dec else 0 for q in order[1:]]

    sess_date = start_day + timedelta(days=int(i // 6), minutes=int(37 * (i % 6)))
    t_cursor = sess_date + timedelta(seconds=float(rest_before_min[i] * 60))

    for k, (qid, lab) in enumerate(zip(order, labels), start=1):
        q = QMAP[qid]
        rows.append(dict(
            participant_id=p, session_id=sess, trial_id=f"{sess}T{k:02d}",
            trial_index=k, question_id=qid, ground_truth_binary=lab,
            session_date=sess_date.strftime("%Y-%m-%d"),
            question_start_timestamp=t_cursor.strftime("%Y-%m-%d %H:%M:%S"),
            room_temperature_celsius=room_temp, room_humidity_percent=humidity,
            ambient_noise_db=ambient_noise, lighting_level_lux=lighting,
            camera_distance_cm=cam_dist, camera_angle_degrees=cam_angle,
            microphone_distance_cm=mic_dist, oximeter_finger=finger,
            background_type=background, _pi=i,
        ))
        t_cursor += timedelta(seconds=float(RNG.normal(34, 8)))

df = pd.DataFrame(rows)
N = len(df)
pi_idx = df["_pi"].to_numpy()

# broadcast participant traits to trial rows
def pv(a): return np.asarray(a)[pi_idx]

cond = df["ground_truth_binary"].to_numpy().astype(float)
diff = df["question_id"].map(lambda q: QMAP[q]["question_difficulty"]).to_numpy()
qtype = df["question_id"].map(lambda q: QMAP[q]["question_type"]).to_numpy()
qcat = df["question_id"].map(lambda q: QMAP[q]["question_category"]).to_numpy()
tidx = df["trial_index"].to_numpy().astype(float)

diff_z = (diff - diff.mean()) / diff.std()


# ──────────────────────────────────────────────────────────────────────────
# 4. LATENT AROUSAL + COGNITIVE LOAD  (the heart of the correlation structure)
# ──────────────────────────────────────────────────────────────────────────
habituation = -0.075 * (tidx - 5.5)              # settles down across the session
arousal = (1.15 * cond
           + 0.50 * pv(trait_anxiety)
           - 0.42 * cond * pv(deception_skill)   # skilled liars leak less
           + 0.30 * diff_z
           + habituation
           + RNG.normal(0, 1.0, N))

cog_load = (0.90 * cond
            + 0.42 * diff_z
            - 0.25 * cond * pv(deception_skill)
            + 0.30 * arousal
            + RNG.normal(0, 1.0, N))

# each modality observes the latent through its own noisy channel
phys_lat = arousal + RNG.normal(0, 1.25, N)
aud_lat = arousal + RNG.normal(0, 1.10, N)
vis_lat = arousal + RNG.normal(0, 1.40, N)


# ──────────────────────────────────────────────────────────────────────────
# 5. SIGNAL QUALITY  (environment -> quality -> attenuates the signal)
# ──────────────────────────────────────────────────────────────────────────
motion = clip(RNG.gamma(1.8, 0.55, N) + 0.18 * clip(arousal, 0, None), 0, 6)

# physiological
pi_trial = clip(pv(base_pi_p) * np.exp(-0.11 * phys_lat) + RNG.normal(0, 0.35, N), 0.15, 15)
ppg_snr = clip(24 + 3.4 * np.log(pi_trial) - 2.6 * motion + RNG.normal(0, 2.4, N), 2, 34)
oxi_quality = clip(ppg_snr / 30, 0.06, 1.0)
contact_quality = clip(0.94 - 0.09 * motion + 0.03 * np.log(pi_trial) + RNG.normal(0, .05, N), .25, 1)

# audio
snr_db = clip(34 - 0.62 * (df.ambient_noise_db.to_numpy() - 40)
              - 0.16 * (df.microphone_distance_cm.to_numpy() - 35)
              + RNG.normal(0, 2.6, N), 3, 42)
audio_quality = clip(snr_db / 38, 0.05, 1.0)
clipping_ratio = clip(RNG.beta(1.3, 60, N) + 0.004 * clip(snr_db - 32, 0, None), 0, 0.12)

# video
lux = df.lighting_level_lux.to_numpy()
blur = clip(0.10 + 0.035 * motion + 0.00035 * (400 - lux) + RNG.normal(0, .03, N), 0.01, 0.85)
brightness = clip(0.30 + 0.0016 * lux + RNG.normal(0, .05, N), 0.12, 1.0)
occlusion = clip(RNG.beta(1.4, 22, N) + 0.02 * pv(wears_glasses), 0, 0.55)
video_quality = clip(0.55 * (1 - blur) + 0.30 * np.minimum(brightness / 0.8, 1)
                     + 0.15 * (1 - occlusion) + RNG.normal(0, .03, N), 0.05, 1.0)
face_conf = clip(0.985 - 0.35 * occlusion - 0.20 * blur + RNG.normal(0, .02, N), 0.35, 0.999)

# poor quality => the true signal is attenuated and extra measurement noise appears
def observe(latent, quality, base_noise):
    """Attenuate the latent by measurement quality and inject quality-dependent noise."""
    return latent * (0.45 + 0.55 * quality) + RNG.normal(0, base_noise, N) / (0.35 + 0.65 * quality)

phys_obs = observe(phys_lat, oxi_quality, 0.30)
aud_obs = observe(aud_lat, audio_quality, 0.28)
vis_obs = observe(vis_lat, video_quality, 0.32)
cog_obs = observe(cog_load, audio_quality, 0.25)


# ──────────────────────────────────────────────────────────────────────────
# 6. PHYSIOLOGICAL FEATURES
# ──────────────────────────────────────────────────────────────────────────
drift = 0.9 * np.sin(tidx / 3.0) + RNG.normal(0, 1.6, N)
pre_hr = clip(pv(session_base_hr) + drift, 45, 130)                       # baseline window
hr_rise = 1.1 + 3.05 * phys_obs + RNG.normal(0, 1.9, N)
during_q_hr = clip(pre_hr + 0.55 * hr_rise + RNG.normal(0, 1.1, N), 45, 165)
answer_hr = clip(pre_hr + hr_rise, 45, 175)                               # answer window
post_hr = clip(pre_hr + 0.34 * hr_rise + RNG.normal(0, 1.3, N), 45, 165)

hr_mean = (0.25 * pre_hr + 0.30 * during_q_hr + 0.30 * answer_hr + 0.15 * post_hr)
hr_std = clip(2.1 + 0.55 * np.abs(hr_rise) + RNG.normal(0, .6, N), 0.5, 16)
hr_min = clip(np.minimum(pre_hr, post_hr) - clip(RNG.normal(2.0, 1.0, N), 0, None), 40, 170)
hr_max = np.maximum(answer_hr, during_q_hr) + clip(RNG.normal(2.2, 1.1, N), 0, None)

rmssd = clip(pv(base_rmssd_p) * np.exp(-0.135 * phys_obs) + RNG.normal(0, 3.2, N), 5, 140)
sdnn = clip(rmssd * 1.32 + RNG.normal(0, 5.0, N), 6, 190)
pnn50 = clip(0.62 * rmssd - 7.5 + RNG.normal(0, 3.4, N), 0, 62)
mean_rr = 60000.0 / hr_mean
nn50 = np.round(pnn50 / 100 * clip(hr_mean * 0.35, 5, 60)).astype(int)

spo2 = clip(pv(base_spo2_p) - 0.16 * phys_obs + RNG.normal(0, 0.42, N), 92, 100)
spo2_pre = clip(pv(base_spo2_p) + RNG.normal(0, 0.35, N), 92, 100)
spo2_during = clip(spo2_pre - 0.10 * phys_obs + RNG.normal(0, 0.25, N), 92, 100)
spo2_min = np.minimum.reduce([spo2, spo2_pre, spo2_during]) - clip(RNG.normal(0.35, 0.2, N), 0, None)
spo2_max = np.maximum.reduce([spo2, spo2_pre, spo2_during]) + clip(RNG.normal(0.30, 0.2, N), 0, None)
spo2_std = clip((spo2_max - spo2_min) / 3.4 + RNG.normal(0, .08, N), 0.05, 3.0)

pulse_amp = clip(0.42 * pi_trial + RNG.normal(0, 0.09, N), 0.03, 6)
ppg_peaks = np.round(hr_mean / 60 * 8.0).astype(int)                       # over 8 s window
pulse_rise = clip(148 - 4.5 * phys_obs + RNG.normal(0, 12, N), 90, 230)
pulse_fall = clip(pulse_rise * 1.75 + RNG.normal(0, 18, N), 140, 430)
pulse_width = pulse_rise + pulse_fall


# ──────────────────────────────────────────────────────────────────────────
# 7. AUDIO / SPEECH FEATURES
# ──────────────────────────────────────────────────────────────────────────
exp_words = np.array([BASE_WORDS[t] for t in qtype])
word_count = np.maximum(1, np.round(exp_words * np.exp(0.16 * cog_obs) * np.exp(RNG.normal(0, .22, N)))).astype(int)
syllables = np.maximum(word_count, np.round(word_count * RNG.normal(1.75, 0.18, N))).astype(int)

speak_rate = clip(pv(base_speech_rate_p) - 5.4 * aud_obs - 3.0 * cog_obs + RNG.normal(0, 7.5, N), 70, 235)
speech_dur = clip(word_count / (speak_rate / 60.0), 0.25, 90)

pause_lam = clip(0.55 + 0.085 * word_count + 0.52 * cog_obs + 0.28 * pv(base_disfluency), 0.1, 22)
pause_count = RNG.poisson(pause_lam)
mean_pause = clip(305 + 62 * cog_obs + 34 * aud_obs + RNG.normal(0, 55, N), 90, 1600)
max_pause = mean_pause * clip(RNG.normal(2.0, 0.45, N), 1.05, 5.0)
pause_std = clip((max_pause - mean_pause) / 2.6, 10, 900)
silence_dur = pause_count * mean_pause / 1000.0
audio_dur = speech_dur + silence_dur + clip(RNG.normal(0.45, 0.15, N), 0.05, None)

resp_latency = clip(pv(base_latency_p) + 238 * cog_obs + 84 * aud_obs + RNG.normal(0, 155, N), 140, 4200)

filler_lam = clip(pv(base_disfluency) * (0.30 + 0.055 * word_count) * (1 + 0.34 * clip(cog_obs, -0.9, None)), 0.02, 16)
filler_count = RNG.poisson(filler_lam)
_fs = RNG.dirichlet([2.4, 2.0, 1.1, 0.8, 1.3, 0.7], N)
um_c, uh_c, ah_c, er_c, like_c, yk_c = [np.round(filler_count * _fs[:, j]).astype(int) for j in range(6)]
other_filler = np.maximum(0, filler_count - (um_c + uh_c + ah_c + er_c + like_c + yk_c))
mean_filler_dur = clip(RNG.normal(295, 60, N) + 18 * cog_obs, 90, 900)

stut_lam = clip(pv(base_disfluency) * 0.45 * (1 + 0.40 * clip(cog_obs, -0.9, None)) * (word_count / 6) ** 0.55, 0.01, 12)
word_rep = RNG.poisson(stut_lam * 0.45)
syl_rep = RNG.poisson(stut_lam * 0.30)
snd_rep = RNG.poisson(stut_lam * 0.15)
prolongation = RNG.poisson(stut_lam * 0.22)
block_count = RNG.poisson(stut_lam * 0.18)
repetition_count = word_rep + syl_rep + snd_rep
stutter_events = repetition_count + prolongation + block_count
self_correction = RNG.poisson(clip(0.16 + 0.30 * clip(cog_obs, -0.8, None), 0.01, 5))
false_start = RNG.poisson(clip(0.11 + 0.26 * clip(cog_obs, -0.8, None), 0.01, 5))
hesitation_count = filler_count + prolongation + block_count + false_start

mean_pitch = clip(pv(base_pitch_p) * (1 + 0.032 * aud_obs) + RNG.normal(0, 5.5, N), 70, 330)
pitch_std = clip(20.5 + 3.6 * aud_obs + 0.05 * mean_pitch + RNG.normal(0, 3.4, N), 4, 75)
pitch_min = clip(mean_pitch - 1.85 * pitch_std, 55, 320)
pitch_max = mean_pitch + 2.05 * pitch_std
jitter = clip(0.52 + 0.115 * aud_obs + 0.10 * pv(base_disfluency) + RNG.normal(0, .10, N), 0.10, 2.4)
shimmer = clip(3.25 + 0.52 * aud_obs + RNG.normal(0, .55, N), 1.0, 11)
hnr = clip(18.6 - 0.95 * aud_obs - 2.4 * jitter + 0.10 * snr_db + RNG.normal(0, 1.3, N), 3, 30)

intensity_db = clip(pv(base_intensity_p) + 0.85 * aud_obs - 0.06 * (df.microphone_distance_cm.to_numpy() - 35)
                    + RNG.normal(0, 1.5, N), 48, 82)
rms_energy = clip(10 ** ((intensity_db - 94) / 20) * 1.9, 1e-4, 0.9)
rms_std = clip(rms_energy * clip(RNG.normal(0.42, 0.09, N), 0.1, 1.2), 1e-5, 0.6)
zcr = clip(0.081 + 0.0062 * aud_obs + 0.00018 * (mean_pitch - 160) + RNG.normal(0, .011, N), 0.015, 0.30)
spec_centroid = clip(1580 + 118 * aud_obs + 2.1 * (mean_pitch - 160) + RNG.normal(0, 165, N), 600, 4200)
spec_bandwidth = clip(spec_centroid * clip(RNG.normal(0.92, 0.09, N), 0.5, 1.5), 350, 4200)
spec_rolloff = clip(spec_centroid * clip(RNG.normal(2.35, 0.22, N), 1.4, 3.6), 900, 8000)
spec_flatness = clip(0.031 + 0.0045 * aud_obs + RNG.normal(0, .008, N), 0.002, 0.22)

# MFCCs: mfcc1 tracks energy, mfcc2/3 track spectral shape, rest carry weak arousal + noise
mfcc = {}
for c in range(1, 14):
    if c == 1:
        m = -382 + 118 * np.log10(rms_energy + 1e-6) / 2 + RNG.normal(0, 9, N)
    elif c == 2:
        m = 92 - 0.011 * spec_centroid + 2.6 * aud_obs + RNG.normal(0, 7, N)
    elif c == 3:
        m = -14 + 0.0042 * spec_centroid - 1.9 * aud_obs + RNG.normal(0, 6, N)
    else:
        m = RNG.normal(0, 9, N) + (0.55 if c % 2 == 0 else -0.42) * aud_obs
    s = clip(np.abs(m) * 0.11 + 3.2 + 0.35 * np.abs(aud_obs) + RNG.normal(0, 0.9, N), 0.6, 45)
    mfcc[f"mfcc_{c:02d}_mean"] = m.round(3)
    mfcc[f"mfcc_{c:02d}_std"] = s.round(3)


# ──────────────────────────────────────────────────────────────────────────
# 8. COMPUTER-VISION FEATURES
# ──────────────────────────────────────────────────────────────────────────
face_area = clip(RNG.normal(1, .10, N) * (62 / df.camera_distance_cm.to_numpy()) ** 2 * 41000, 6000, 130000)
face_w = np.sqrt(face_area / 1.32)
face_h = face_area / face_w

blink_rate_pre = clip(pv(base_blink_p) + RNG.normal(0, 2.2, N), 3, 45)
blink_rate = clip(pv(base_blink_p) + 3.35 * vis_obs + RNG.normal(0, 2.6, N), 3, 52)
blink_rate_post = clip(pv(base_blink_p) + 1.15 * vis_obs + RNG.normal(0, 2.3, N), 3, 48)
blink_count = np.round(blink_rate * audio_dur / 60.0).astype(int)
mean_blink_dur = clip(268 - 7.8 * vis_obs + RNG.normal(0, 22, N), 120, 420)
blink_dur_std = clip(mean_blink_dur * 0.20 + RNG.normal(0, 8, N), 8, 160)

ear_common = pv(base_ear_p) - 0.0038 * vis_obs
ear_l = clip(ear_common + RNG.normal(0, .010, N), 0.14, 0.42)
ear_r = clip(ear_common + RNG.normal(0, .010, N), 0.14, 0.42)
ear_mean = (ear_l + ear_r) / 2

lookaway = clip(pv(base_lookaway_p) + 0.048 * vis_obs + RNG.normal(0, .035, N), 0.0, 0.92)
gaze_dev = clip(3.9 + 1.55 * vis_obs + 14 * (lookaway - pv(base_lookaway_p)) + RNG.normal(0, 1.2, N), 0.2, 26)
gaze_x = clip(RNG.normal(0, 1, N) * gaze_dev / 9 + 0.02 * vis_obs, -1, 1)
gaze_y = clip(RNG.normal(0, 1, N) * gaze_dev / 11 - 0.03 * vis_obs, -1, 1)
gaze_shifts = RNG.poisson(clip(1.5 + 0.62 * clip(vis_obs, -1.5, None) + 0.12 * audio_dur, 0.2, 30))
gaze_stability = clip(1 - gaze_dev / 26 + RNG.normal(0, .04, N), 0.02, 1)
look_away_s = lookaway * audio_dur
look_cam_s = audio_dur - look_away_s

yaw_std = clip(3.2 + 1.25 * vis_obs + 0.9 * motion + RNG.normal(0, .8, N), 0.3, 22)
pitch_std_h = clip(2.6 + 0.95 * vis_obs + 0.8 * motion + RNG.normal(0, .7, N), 0.2, 18)
roll_std_h = clip(1.9 + 0.62 * vis_obs + 0.6 * motion + RNG.normal(0, .5, N), 0.1, 14)
yaw = clip(RNG.normal(0, 1, N) * yaw_std + df.camera_angle_degrees.to_numpy() * 0.4, -45, 45)
pitch_h = clip(RNG.normal(0, 1, N) * pitch_std_h - 1.2 * clip(vis_obs, 0, None), -35, 35)
roll_h = clip(RNG.normal(0, 1, N) * roll_std_h, -25, 25)
head_moves = RNG.poisson(clip(1.1 + 0.70 * clip(vis_obs, -1.4, None) + 0.10 * audio_dur, 0.2, 35))
head_motion_score = clip((yaw_std + pitch_std_h + roll_std_h) / 3 / 8, 0.01, 1.5)

# expressions via softmax (guaranteed to sum to 1)
logits = np.column_stack([
    np.full(N, 2.30) - 0.30 * vis_obs,                 # neutral
    -0.25 - 0.22 * vis_obs + 0.30 * (cond == 0),       # happy
    -1.05 + 0.14 * vis_obs,                            # sad
    -1.55 + 0.16 * vis_obs,                            # angry
    -1.75 + 0.42 * vis_obs,                            # fear
    -1.35 + 0.36 * vis_obs,                            # surprise
    -2.05 + 0.10 * vis_obs,                            # disgust
]) + RNG.normal(0, .35, (N, 7))
ex = np.exp(logits - logits.max(1, keepdims=True))
ex = ex / ex.sum(1, keepdims=True)
EXPR = ["neutral", "happy", "sad", "angry", "fear", "surprise", "disgust"]
dominant_expr = np.array(EXPR)[ex.argmax(1)]
expr_entropy = -(ex * np.log(ex + 1e-9)).sum(1)

au_def = {"au01": 0.22, "au02": 0.20, "au04": 0.46, "au05": 0.30, "au06": -0.26,
          "au07": 0.38, "au09": 0.10, "au10": 0.12, "au12": -0.30, "au14": 0.34,
          "au15": 0.18, "au17": 0.24, "au20": 0.26, "au23": 0.20, "au25": 0.14,
          "au26": 0.16, "au45": 0.44}
AU = {f"{k}_intensity": clip(RNG.gamma(1.7, 0.42, N) + w * vis_obs, 0, 5).round(3)
      for k, w in au_def.items()}
au_activity = np.mean([v for v in AU.values()], axis=0)

mouth_ar = clip(0.30 + 0.055 * np.log1p(word_count) + RNG.normal(0, .04, N), 0.05, 0.85)
lip_move = clip(0.22 + 0.0042 * speak_rate + 0.02 * np.log1p(word_count) + RNG.normal(0, .05, N), 0.02, 1.4)
jaw_move = clip(lip_move * 0.78 + RNG.normal(0, .05, N), 0.01, 1.3)
mouth_freq = clip(speak_rate / 60 * 1.6 + RNG.normal(0, .25, N), 0.2, 8)

shoulder_angle = clip(RNG.normal(0, 2.4, N) + 0.35 * vis_obs, -14, 14)
body_motion = clip(0.16 + 0.10 * motion + 0.055 * clip(vis_obs, -1.2, None) + RNG.normal(0, .05, N), 0.01, 1.6)
posture_change = RNG.poisson(clip(0.5 + 0.42 * clip(vis_obs, -1.2, None), 0.05, 12))
lean_fwd = clip(0.32 + 0.05 * vis_obs + RNG.normal(0, .09, N), 0, 1)

expr_change = RNG.poisson(clip(0.7 + 0.5 * clip(vis_obs, -1.2, None), .05, 12))

# ──────────────────────────────────────────────────────────────────────────
# 8b. EYEBROW / HEAD-POSE / GAZE GEOMETRY  (baseline-relative, scale-free)
# ──────────────────────────────────────────────────────────────────────────
# Eyebrow raise is measured as the distance from brow centre to eye centre,
# divided by inter-ocular distance. Two reasons:
#   1. dividing by inter-ocular distance cancels camera distance, so leaning
#      toward the webcam does not register as an eyebrow raise;
#   2. it is measured inside the face coordinate system, so tilting the head
#      back does not register as an eyebrow raise either.
# The naive_* columns below deliberately skip step 2, to show what goes wrong.

# AU01 (inner brow raiser) and AU02 (outer brow raiser) ARE the brow raise in
# FACS terms, so the geometric measure is derived from them - the two must agree.
au01, au02 = AU["au01_intensity"], AU["au02_intensity"]
brow_drive = 0.5 * (au01 + au02)
brow_drive_rel = brow_drive - brow_drive.mean()

_bd = pv(brow_expressive_p) * 0.021 * brow_drive_rel + RNG.normal(0, 0.0035, N)
brow_l_delta = _bd + pv(brow_asym_p) / 2 + RNG.normal(0, 0.0018, N)
brow_r_delta = _bd - pv(brow_asym_p) / 2 + RNG.normal(0, 0.0018, N)

brow_l_base = clip(pv(base_brow_eye_p) + pv(brow_asym_p) / 2 + RNG.normal(0, .004, N), .15, .75)
brow_r_base = clip(pv(base_brow_eye_p) - pv(brow_asym_p) / 2 + RNG.normal(0, .004, N), .15, .75)
brow_l_cur = brow_l_base + brow_l_delta          # exact: current = baseline + delta
brow_r_cur = brow_r_base + brow_r_delta

brow_rise_t = clip(RNG.normal(0.30, 0.075, N), 0.08, 0.9)        # seconds to peak
brow_l_peak = brow_l_delta * clip(RNG.normal(2.15, 0.42, N), 1.05, 4.5)
brow_r_peak = brow_r_delta * clip(RNG.normal(2.15, 0.42, N), 1.05, 4.5)
brow_l_vel = brow_l_peak / brow_rise_t                            # units per second
brow_r_vel = brow_r_peak / brow_rise_t
brow_l_acc = brow_l_vel / (brow_rise_t / 2)
brow_r_acc = brow_r_vel / (brow_rise_t / 2)
brow_l_std = clip(0.36 * np.abs(brow_l_delta) + RNG.gamma(2, .0016, N), 1e-4, .09)
brow_r_std = clip(0.36 * np.abs(brow_r_delta) + RNG.gamma(2, .0016, N), 1e-4, .09)
brow_events = RNG.poisson(clip(0.45 + 1.3 * pv(brow_expressive_p) * clip(brow_drive_rel, 0, None), .02, 14))
brow_dur = np.where(brow_events > 0, clip(RNG.normal(430, 115, N), 90, 1400), 0.0)
brow_asym = np.abs(brow_l_delta - brow_r_delta)
brow_score = (np.abs(brow_l_delta) + np.abs(brow_r_delta)) / 2

# head pose: baseline window vs answer window. deltas are exact subtractions.
yaw_base = df.camera_angle_degrees.to_numpy() * 0.4 + RNG.normal(0, 1.15, N)
pitch_base = RNG.normal(0, 1.35, N)
roll_base = RNG.normal(0, 0.95, N)
yaw_d = yaw - yaw_base
pitch_d = pitch_h - pitch_base
roll_d = roll_h - roll_base
head_vel = (yaw_std + pitch_std_h + roll_std_h) * clip(RNG.normal(1.85, 0.32, N), 0.5, 4.5)

# THE CONFOUND, left in on purpose: measuring brow height in raw camera
# coordinates mixes in head pitch. Tilt the head back and the brows rise in the
# image without the person moving a muscle. Compare naive_* against the
# face-relative columns above - the naive version is a measurably worse feature.
naive_l = brow_l_delta + 0.0072 * pitch_d + RNG.normal(0, .0028, N)
naive_r = brow_r_delta + 0.0072 * pitch_d + RNG.normal(0, .0028, N)

# eye openness, baseline vs answer window
ear_l_base = clip(pv(base_ear_p) + RNG.normal(0, .0085, N), .13, .43)
ear_r_base = clip(pv(base_ear_p) + RNG.normal(0, .0085, N), .13, .43)
long_blinks = RNG.poisson(clip(0.22 + 0.16 * clip(vis_obs, 0, None), .01, 6))
eye_closure_ms = blink_count * mean_blink_dur + long_blinks * clip(RNG.normal(360, 85, N), 120, 900)

# gaze, baseline vs answer window
gx_base = pv(base_gaze_x_p) + RNG.normal(0, .028, N)
gy_base = pv(base_gaze_y_p) + RNG.normal(0, .026, N)
gx_d = gaze_x - gx_base
gy_d = gaze_y - gy_base
gaze_h_dev = np.abs(gx_d) * 22.5 + RNG.gamma(2, .35, N)
gaze_v_dev = np.abs(gy_d) * 18.0 + RNG.gamma(2, .30, N)
gaze_vel = gaze_shifts * clip(RNG.normal(9.5, 2.2, N), 2, 30) / clip(audio_dur, .3, None)

# whole-face motion aggregated over the answer window (per-frame landmark
# displacement, averaged across landmarks then across frames)
fm_mean = clip(0.58 * au_activity + 0.26 * body_motion + 0.16 * lip_move, 0.005, 6)
fm_std = clip(fm_mean * clip(RNG.normal(0.44, 0.09, N), .1, 1.2), 1e-3, 4)
fm_peak = fm_mean + 2.35 * fm_std
lm_vel_mean = fm_mean * clip(RNG.normal(0.056, 0.010, N), .01, .2)
lm_vel_max = lm_vel_mean * clip(RNG.normal(3.25, 0.62, N), 1.2, 8)
lm_acc_mean = lm_vel_mean * clip(RNG.normal(6.6, 1.25, N), 1.5, 16)
expr_stability = 1.0 / (1.0 + expr_change)


# ──────────────────────────────────────────────────────────────────────────
# 9. TEMPORAL WINDOWS + ENERGY/BLINK DELTAS
# ──────────────────────────────────────────────────────────────────────────
energy_pre = clip(rms_energy * clip(RNG.normal(0.30, .07, N), .05, .9), 1e-5, .6)
energy_during_q = clip(rms_energy * clip(RNG.normal(0.22, .06, N), .03, .8), 1e-5, .6)
reaction_time = resp_latency / 1000.0
peak_response_t = clip(reaction_time + speech_dur * clip(RNG.normal(0.45, .15, N), .05, .95), 0.1, 95)
recovery_time = clip(4.5 + 1.65 * phys_obs + RNG.normal(0, 1.2, N), 0.4, 22)


# ──────────────────────────────────────────────────────────────────────────
# 10. ASSEMBLE
# ──────────────────────────────────────────────────────────────────────────
out = pd.DataFrame()
out["participant_id"] = df.participant_id
out["session_id"] = df.session_id
out["trial_id"] = df.trial_id
out["trial_index"] = df.trial_index
out["question_id"] = df.question_id
out["question_text"] = [QMAP[q]["question_text"] for q in df.question_id]
out["question_type"] = qtype
out["question_category"] = qcat
out["question_difficulty"] = diff
out["expected_answer_type"] = [QMAP[q]["expected_answer_type"] for q in df.question_id]
out["session_date"] = df.session_date
out["question_start_timestamp"] = df.question_start_timestamp

# participant demographics
for c in ["age", "sex", "height_cm", "weight_kg", "bmi", "dominant_hand",
          "native_language", "education_level", "wears_glasses"]:
    out[c] = pv(participants[c].to_numpy())
out["age_group"] = pd.cut(out.age, [17, 20, 23, 26, 60], labels=["18-20", "21-23", "24-26", "27+"]).astype(str)

# ground truth
out["ground_truth_binary"] = cond.astype(int)
out["ground_truth_label"] = np.where(cond == 1, "deceptive", "truthful")
out["experiment_condition"] = np.where(cond == 1, "instructed_deception", "instructed_truth")
out["deception_instruction"] = np.where(cond == 1, "conceal", "disclose")
out["participant_answer"] = np.where(qtype == "yes_no",
                                     np.where(cond == 1, "No", RNG.choice(["Yes", "No"], N)),
                                     "[TRANSCRIPT_REDACTED]")
out["answer_length_words"] = word_count
out["answer_length_syllables"] = syllables
out["answer_duration_seconds"] = audio_dur.round(3)
out["experimenter_confidence"] = clip(RNG.normal(0.90, 0.07, N), 0.55, 1).round(3)

# ── physiological
out["baseline_heart_rate_bpm"] = pre_hr.round(1)
out["heart_rate_bpm"] = answer_hr.round(1)
out["heart_rate_change_from_baseline"] = (answer_hr - pre_hr).round(2)
out["heart_rate_percent_change_from_baseline"] = ((answer_hr - pre_hr) / pre_hr * 100).round(2)
out["mean_heart_rate_bpm"] = hr_mean.round(1)
out["min_heart_rate_bpm"] = hr_min.round(1)
out["max_heart_rate_bpm"] = hr_max.round(1)
out["heart_rate_std"] = hr_std.round(2)
out["heart_rate_range"] = (hr_max - hr_min).round(2)
out["heart_rate_recovery_rate"] = ((answer_hr - post_hr) / clip(recovery_time, .1, None)).round(3)
out["mean_rr_interval_ms"] = mean_rr.round(1)
out["std_rr_interval_ms"] = sdnn.round(2)
out["rmssd_ms"] = rmssd.round(2)
out["sdnn_ms"] = sdnn.round(2)
out["nn50_count"] = nn50
out["pnn50_percent"] = pnn50.round(2)
out["heart_rate_variability"] = rmssd.round(2)

out["baseline_spo2_percent"] = spo2_pre.round(2)
out["spo2_percent"] = spo2.round(2)
out["spo2_change_from_baseline"] = (spo2 - spo2_pre).round(3)
out["spo2_min"] = spo2_min.round(2)
out["spo2_max"] = spo2_max.round(2)
out["spo2_std"] = spo2_std.round(3)
out["spo2_range"] = (spo2_max - spo2_min).round(3)

out["baseline_perfusion_index"] = pv(base_pi_p).round(2)
out["perfusion_index"] = pi_trial.round(3)
out["perfusion_index_change_from_baseline"] = (pi_trial - pv(base_pi_p)).round(3)
out["pulse_amplitude"] = pulse_amp.round(4)
out["ppg_peak_count"] = ppg_peaks
out["ppg_signal_energy"] = (pulse_amp ** 2 * ppg_peaks).round(4)
out["ppg_snr_db"] = ppg_snr.round(2)
out["ppg_noise_level"] = (1 / clip(ppg_snr, .5, None)).round(4)
out["ppg_baseline_drift"] = clip(RNG.normal(0, .05, N) + 0.02 * motion, -.3, .4).round(4)
out["pulse_rise_time_ms"] = pulse_rise.round(1)
out["pulse_fall_time_ms"] = pulse_fall.round(1)
out["pulse_width_ms"] = pulse_width.round(1)
out["pulse_signal_quality"] = oxi_quality.round(3)
out["sensor_contact_quality"] = contact_quality.round(3)

# ── audio
out["audio_duration_seconds"] = audio_dur.round(3)
out["speech_duration_seconds"] = speech_dur.round(3)
out["silence_duration_seconds"] = silence_dur.round(3)
out["speech_to_silence_ratio"] = (speech_dur / clip(silence_dur, .01, None)).round(3)
out["speaking_rate_wpm"] = speak_rate.round(1)
out["articulation_rate_wpm"] = (word_count / clip(speech_dur, .05, None) * 60).round(1)
out["syllable_rate"] = (syllables / clip(speech_dur, .05, None)).round(3)
out["word_count"] = word_count
out["response_latency_ms"] = resp_latency.round(1)
out["time_to_first_word_ms"] = (resp_latency + clip(RNG.normal(45, 20, N), 0, None)).round(1)

out["pause_count"] = pause_count
out["short_pause_count"] = RNG.binomial(pause_count, 0.55)
out["long_pause_count"] = pause_count - out["short_pause_count"]
out["mean_pause_duration_ms"] = mean_pause.round(1)
out["max_pause_duration_ms"] = max_pause.round(1)
out["pause_duration_std"] = pause_std.round(1)
out["pause_ratio"] = (silence_dur / clip(audio_dur, .05, None)).round(4)

out["filler_word_count"] = filler_count
out["filler_word_rate"] = (filler_count / clip(word_count, 1, None)).round(4)
out["um_count"] = um_c
out["uh_count"] = uh_c
out["ah_count"] = ah_c
out["er_count"] = er_c
out["like_count"] = like_c
out["you_know_count"] = yk_c
out["other_filler_count"] = other_filler
out["mean_filler_duration_ms"] = mean_filler_dur.round(1)

out["stutter_detected"] = (stutter_events > 0).astype(int)
out["stutter_event_count"] = stutter_events
out["stutter_frequency"] = (stutter_events / clip(word_count, 1, None)).round(4)
out["word_repetition_count"] = word_rep
out["syllable_repetition_count"] = syl_rep
out["sound_repetition_count"] = snd_rep
out["repetition_count"] = repetition_count
out["prolongation_count"] = prolongation
out["block_count"] = block_count
out["self_correction_count"] = self_correction
out["false_start_count"] = false_start
out["hesitation_count"] = hesitation_count
out["hesitation_rate"] = (hesitation_count / clip(speech_dur, .05, None)).round(4)

out["mean_pitch_hz"] = mean_pitch.round(2)
out["min_pitch_hz"] = pitch_min.round(2)
out["max_pitch_hz"] = pitch_max.round(2)
out["pitch_std"] = pitch_std.round(2)
out["pitch_range_hz"] = (pitch_max - pitch_min).round(2)
out["jitter_percent"] = jitter.round(4)
out["shimmer_percent"] = shimmer.round(3)
out["hnr_db"] = hnr.round(2)
out["mean_rms_energy"] = rms_energy.round(5)
out["rms_energy_std"] = rms_std.round(5)
out["voice_intensity_db"] = intensity_db.round(2)
out["zero_crossing_rate"] = zcr.round(4)
out["spectral_centroid"] = spec_centroid.round(1)
out["spectral_bandwidth"] = spec_bandwidth.round(1)
out["spectral_rolloff"] = spec_rolloff.round(1)
out["spectral_flatness"] = spec_flatness.round(4)
for k, v in mfcc.items():
    out[k] = v

# ── vision
out["face_detected"] = 1
out["face_detection_confidence"] = face_conf.round(4)
out["face_area_pixels"] = face_area.round(0)
out["face_width_pixels"] = face_w.round(1)
out["face_height_pixels"] = face_h.round(1)
out["face_occlusion_ratio"] = occlusion.round(4)
out["landmark_detection_confidence"] = clip(face_conf - RNG.uniform(0, .04, N), .3, 1).round(4)

out["blink_count"] = blink_count
out["blink_rate_per_minute"] = blink_rate.round(2)
out["mean_blink_duration_ms"] = mean_blink_dur.round(1)
out["blink_duration_std"] = blink_dur_std.round(1)
out["eye_aspect_ratio_left"] = ear_l.round(4)
out["eye_aspect_ratio_right"] = ear_r.round(4)
out["mean_eye_aspect_ratio"] = ear_mean.round(4)
out["eye_openness_variance"] = clip(RNG.gamma(2, .0009, N) + .0004 * np.abs(vis_obs), 0, .02).round(5)

out["gaze_x"] = gaze_x.round(4)
out["gaze_y"] = gaze_y.round(4)
out["gaze_deviation_degrees"] = gaze_dev.round(3)
out["gaze_stability"] = gaze_stability.round(4)
out["gaze_shift_count"] = gaze_shifts
out["gaze_shift_frequency"] = (gaze_shifts / clip(audio_dur, .05, None)).round(4)
out["time_looking_at_camera_seconds"] = look_cam_s.round(3)
out["time_looking_away_seconds"] = look_away_s.round(3)
out["looking_away_ratio"] = lookaway.round(4)

out["head_yaw_degrees"] = yaw.round(2)
out["head_pitch_degrees"] = pitch_h.round(2)
out["head_roll_degrees"] = roll_h.round(2)
out["head_yaw_std"] = yaw_std.round(3)
out["head_pitch_std"] = pitch_std_h.round(3)
out["head_roll_std"] = roll_std_h.round(3)
out["head_movement_count"] = head_moves
out["head_motion_score"] = head_motion_score.round(4)

for j, e in enumerate(EXPR):
    out[f"{e}_expression_probability"] = ex[:, j].round(4)
out["dominant_expression"] = dominant_expr
out["expression_entropy"] = expr_entropy.round(4)
out["expression_change_count"] = expr_change
out["facial_expression_confidence"] = clip(ex.max(1) * .9 + .08, .2, 1).round(4)

for k, v in AU.items():
    out[k] = v
out["facial_action_unit_activity"] = au_activity.round(4)
out["facial_movement_score"] = clip(au_activity * .8 + body_motion * .2, 0, 5).round(4)

out["mouth_aspect_ratio"] = mouth_ar.round(4)
out["lip_movement_score"] = lip_move.round(4)
out["jaw_movement_score"] = jaw_move.round(4)
out["mouth_movement_frequency"] = mouth_freq.round(3)

out["shoulder_angle_degrees"] = shoulder_angle.round(2)
out["body_motion_score"] = body_motion.round(4)
out["posture_change_count"] = posture_change
out["lean_forward_ratio"] = lean_fwd.round(4)

# ── eyebrow geometry (face-relative, in inter-ocular units)
out["baseline_left_eyebrow_eye_distance"] = brow_l_base.round(5)
out["baseline_right_eyebrow_eye_distance"] = brow_r_base.round(5)
out["left_eyebrow_eye_distance"] = brow_l_cur.round(5)
out["right_eyebrow_eye_distance"] = brow_r_cur.round(5)
out["left_eyebrow_height_delta"] = brow_l_delta.round(5)
out["right_eyebrow_height_delta"] = brow_r_delta.round(5)
out["left_eyebrow_raise_ratio"] = (brow_l_cur / brow_l_base).round(5)
out["right_eyebrow_raise_ratio"] = (brow_r_cur / brow_r_base).round(5)
out["left_eyebrow_peak_raise"] = brow_l_peak.round(5)
out["right_eyebrow_peak_raise"] = brow_r_peak.round(5)
out["left_eyebrow_velocity"] = brow_l_vel.round(5)
out["right_eyebrow_velocity"] = brow_r_vel.round(5)
out["left_eyebrow_acceleration"] = brow_l_acc.round(4)
out["right_eyebrow_acceleration"] = brow_r_acc.round(4)
out["left_eyebrow_movement_std"] = brow_l_std.round(5)
out["right_eyebrow_movement_std"] = brow_r_std.round(5)
out["eyebrow_asymmetry"] = brow_asym.round(5)
out["eyebrow_raise_event_count"] = brow_events
out["eyebrow_raise_duration_ms"] = np.round(brow_dur, 1)
out["eyebrow_raise_rise_time_ms"] = (brow_rise_t * 1000).round(1)
out["eyebrow_movement_score"] = brow_score.round(5)
out["naive_left_eyebrow_delta_camera_frame"] = naive_l.round(5)
out["naive_right_eyebrow_delta_camera_frame"] = naive_r.round(5)

# ── head pose baselines and deltas
out["baseline_head_yaw"] = yaw_base.round(2)
out["baseline_head_pitch"] = pitch_base.round(2)
out["baseline_head_roll"] = roll_base.round(2)
out["head_yaw_delta"] = yaw_d.round(2)
out["head_pitch_delta"] = pitch_d.round(2)
out["head_roll_delta"] = roll_d.round(2)
out["head_movement_velocity_deg_s"] = head_vel.round(3)

# ── eye openness baselines and deltas
out["baseline_left_eye_openness"] = ear_l_base.round(4)
out["baseline_right_eye_openness"] = ear_r_base.round(4)
out["left_eye_openness"] = ear_l.round(4)
out["right_eye_openness"] = ear_r.round(4)
out["left_eye_openness_delta"] = (ear_l - ear_l_base).round(4)
out["right_eye_openness_delta"] = (ear_r - ear_r_base).round(4)
out["long_blink_count"] = long_blinks
out["eye_closure_duration_ms"] = eye_closure_ms.round(1)

# ── gaze baselines, deltas, velocity
out["baseline_gaze_x"] = gx_base.round(4)
out["baseline_gaze_y"] = gy_base.round(4)
out["gaze_x_delta"] = gx_d.round(4)
out["gaze_y_delta"] = gy_d.round(4)
out["gaze_horizontal_deviation"] = gaze_h_dev.round(3)
out["gaze_vertical_deviation"] = gaze_v_dev.round(3)
out["gaze_velocity_deg_s"] = gaze_vel.round(3)

# ── whole-face temporal motion
out["facial_motion_mean"] = fm_mean.round(4)
out["facial_motion_std"] = fm_std.round(4)
out["facial_motion_peak"] = fm_peak.round(4)
out["facial_landmark_velocity_mean"] = lm_vel_mean.round(5)
out["facial_landmark_velocity_max"] = lm_vel_max.round(5)
out["facial_landmark_acceleration_mean"] = lm_acc_mean.round(4)
out["expression_stability"] = expr_stability.round(4)

# ── temporal windows and deltas
out["pre_question_hr"] = pre_hr.round(1)
out["during_question_hr"] = during_q_hr.round(1)
out["post_answer_hr"] = post_hr.round(1)
out["hr_delta_pre_to_question"] = (during_q_hr - pre_hr).round(2)
out["hr_delta_question_to_answer"] = (answer_hr - during_q_hr).round(2)
out["hr_delta_answer_to_post"] = (post_hr - answer_hr).round(2)
out["pre_question_spo2"] = spo2_pre.round(2)
out["during_question_spo2"] = spo2_during.round(2)
out["spo2_delta_pre_to_question"] = (spo2_during - spo2_pre).round(3)
out["pre_question_voice_energy"] = energy_pre.round(5)
out["during_question_voice_energy"] = energy_during_q.round(5)
out["energy_delta_pre_to_answer"] = (rms_energy - energy_pre).round(5)
out["pre_question_blink_rate"] = blink_rate_pre.round(2)
out["post_answer_blink_rate"] = blink_rate_post.round(2)
out["blink_delta_pre_to_answer"] = (blink_rate - blink_rate_pre).round(2)
out["reaction_time_seconds"] = reaction_time.round(3)
out["peak_response_time_seconds"] = peak_response_t.round(3)
out["recovery_time_seconds"] = recovery_time.round(3)

# ── engineered composite scores (computed from the columns above, z-scored)
def zsc(a): return (a - np.nanmean(a)) / np.nanstd(a)
physio_score = zsc(0.55 * zsc(answer_hr - pre_hr) - 0.30 * zsc(rmssd) - 0.15 * zsc(pi_trial))
voice_score = zsc(0.40 * zsc(resp_latency) + 0.25 * zsc(pause_count) + 0.20 * zsc(jitter) - 0.15 * zsc(speak_rate))
hesit_score = zsc(0.5 * zsc(hesitation_count) + 0.5 * zsc(stutter_events))
facial_score = zsc(0.45 * zsc(blink_rate - blink_rate_pre) + 0.35 * zsc(gaze_dev) + 0.20 * zsc(au_activity))
out["physiological_change_score"] = physio_score.round(4)
out["voice_change_score"] = voice_score.round(4)
out["speech_hesitation_score"] = hesit_score.round(4)
out["facial_behavior_score"] = facial_score.round(4)
out["overall_behavioral_change_score"] = ((physio_score + voice_score + hesit_score + facial_score) / 4).round(4)

# ── quality
out["audio_signal_to_noise_ratio"] = snr_db.round(2)
out["audio_clipping_ratio"] = clipping_ratio.round(5)
out["audio_quality_score"] = audio_quality.round(4)
out["video_blur_score"] = blur.round(4)
out["video_brightness_score"] = brightness.round(4)
out["video_quality_score"] = video_quality.round(4)
out["oximeter_signal_quality"] = oxi_quality.round(4)
out["motion_artifact_score"] = motion.round(4)

# ── environment / session state
for c in ["room_temperature_celsius", "room_humidity_percent", "ambient_noise_db",
          "lighting_level_lux", "camera_distance_cm", "camera_angle_degrees",
          "microphone_distance_cm", "oximeter_finger", "background_type"]:
    out[c] = df[c].to_numpy()
for c in ["sleep_duration_hours", "caffeine_consumed", "caffeine_amount_mg",
          "exercise_before_test", "time_since_exercise_minutes",
          "time_since_last_meal_minutes", "resting_time_before_test_minutes"]:
    out[c] = pv(participants[c].to_numpy())

out["camera_fps"] = 30
out["camera_resolution"] = "1280x720"
out["microphone_type"] = "laptop_builtin"
out["oximeter_model"] = "MAX30102_ESP32C3"
out["data_source"] = "SIMULATED"
out["dataset_version"] = DATASET_VERSION
out["feature_extraction_version"] = FEATURE_VERSION


# ──────────────────────────────────────────────────────────────────────────
# 11. MISSING MODALITIES + QUALITY FLAGS  (realistic dropout)
# ──────────────────────────────────────────────────────────────────────────
AUDIO_COLS = [c for c in out.columns if c.startswith((
    "speech_", "speaking_", "articulation_", "syllable_", "pause_", "short_pause",
    "long_pause", "mean_pause", "max_pause", "filler_", "um_", "uh_", "ah_", "er_",
    "like_", "you_know", "other_filler", "stutter_", "word_repetition", "syllable_repetition",
    "sound_repetition", "repetition_count", "prolongation_", "block_", "self_correction",
    "false_start", "hesitation_", "mean_pitch", "min_pitch", "max_pitch", "pitch_",
    "jitter_", "shimmer_", "hnr_", "mean_rms", "rms_energy", "voice_intensity",
    "zero_crossing", "spectral_", "mfcc_", "response_latency", "time_to_first_word",
    "silence_duration", "audio_signal", "audio_clipping", "audio_quality"))]
VISION_COLS = [c for c in out.columns if c.startswith((
    "face_", "landmark_", "blink_", "eye_", "gaze_", "head_", "neutral_", "happy_",
    "sad_", "angry_", "fear_", "surprise_", "disgust_", "dominant_expression",
    "expression_", "facial_", "au0", "au1", "au2", "au4", "mouth_", "lip_", "jaw_",
    "shoulder_", "body_motion", "posture_", "lean_", "time_looking", "looking_away",
    "video_", "left_eyebrow", "right_eyebrow", "eyebrow_", "baseline_left_eyebrow",
    "baseline_right_eyebrow", "naive_", "baseline_head_", "left_eye_", "right_eye_",
    "baseline_left_eye", "baseline_right_eye", "long_blink", "eye_closure",
    "baseline_gaze", "gaze_"))]
PHYS_COLS = [c for c in out.columns if c.startswith((
    "baseline_heart", "heart_rate", "mean_heart", "min_heart", "max_heart",
    "mean_rr", "std_rr", "rmssd", "sdnn", "nn50", "pnn50", "baseline_spo2", "spo2_",
    "baseline_perfusion", "perfusion_", "pulse_", "ppg_", "pre_question_hr",
    "during_question_hr", "post_answer_hr", "hr_delta", "oximeter_signal",
    "sensor_contact"))]

drop = RNG.random(N)
miss_audio = drop < 0.020
miss_video = (drop >= 0.020) & (drop < 0.038)
miss_phys = (drop >= 0.038) & (drop < 0.052)

out["audio_available"] = (~miss_audio).astype(int)
out["video_available"] = (~miss_video).astype(int)
out["physiological_available"] = (~miss_phys).astype(int)
out["modality_count_available"] = out[["audio_available", "video_available", "physiological_available"]].sum(1)

out.loc[miss_audio, [c for c in AUDIO_COLS if out[c].dtype != object]] = np.nan
out.loc[miss_video, [c for c in VISION_COLS if out[c].dtype != object]] = np.nan
out.loc[miss_phys, [c for c in PHYS_COLS if out[c].dtype != object]] = np.nan
out.loc[miss_video, "face_detected"] = 0

out["overall_trial_quality"] = np.select(
    [ (out.audio_quality_score.fillna(0) < .30) | (out.video_quality_score.fillna(0) < .35) | (out.oximeter_signal_quality.fillna(0) < .25),
      (out.audio_quality_score.fillna(1) < .50) | (out.video_quality_score.fillna(1) < .55) | (out.oximeter_signal_quality.fillna(1) < .45) ],
    ["POOR", "WARNING"], default="GOOD")

num_cols = out.select_dtypes(include=[np.number]).columns
out["missing_feature_count"] = out[num_cols].isna().sum(1)
out["missing_data_percent"] = (out["missing_feature_count"] / len(num_cols) * 100).round(2)

_z = out[["heart_rate_change_from_baseline", "response_latency_ms", "blink_rate_per_minute"]].apply(
    lambda s: (s - s.mean()) / s.std())
out["outlier_flag"] = (_z.abs() > 3.5).any(axis=1).astype(int)
out["duplicate_record_flag"] = 0
out["annotation_status"] = "complete"
out["quality_control_status"] = np.where(out.overall_trial_quality == "POOR", "review_required", "passed")

out.to_csv("/sessions/clever-upbeat-hamilton/mnt/outputs/_stage1.csv", index=False)
participants.to_csv("/sessions/clever-upbeat-hamilton/mnt/outputs/_participants.csv", index=False)
QB.to_csv("/sessions/clever-upbeat-hamilton/mnt/outputs/_questions.csv", index=False)
print("stage1 rows:", len(out), "cols:", out.shape[1])
print("class balance:", out.ground_truth_binary.value_counts().to_dict())
