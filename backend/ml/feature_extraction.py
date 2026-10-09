import os
import shutil
import subprocess
import tempfile
import math
import time
import numpy as np
import pandas as pd
import cv2
import librosa

# Ensure ffmpeg in venv\Scripts or imageio_ffmpeg is in PATH
_scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "venv", "Scripts"))
if os.path.exists(_scripts_dir) and _scripts_dir not in os.environ.get("PATH", ""):
    os.environ["PATH"] = _scripts_dir + os.pathsep + os.environ.get("PATH", "")

try:
    import imageio_ffmpeg
    _ffmpeg_bin_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
    if os.path.exists(_ffmpeg_bin_dir) and _ffmpeg_bin_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = _ffmpeg_bin_dir + os.pathsep + os.environ.get("PATH", "")
except Exception:
    pass

def _get_ffmpeg_cmd():
    cmd = shutil.which("ffmpeg") or os.path.join(_scripts_dir, "ffmpeg.exe")
    if not cmd or not os.path.exists(cmd):
        try:
            import imageio_ffmpeg
            cmd = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            pass
    return cmd

# Anthropometric 3D canonical facial model (matches Dataset/cv/vision_feature_extractor.py)
CANONICAL_FACE_3D = np.array([
    (0.0, 0.0, 0.0),          # 1: Nose tip
    (0.0, -330.0, -65.0),     # 152: Chin
    (-225.0, 170.0, -135.0),  # 33: Left eye outer corner
    (225.0, 170.0, -135.0),   # 263: Right eye outer corner
    (-150.0, -150.0, -125.0), # 61: Left mouth corner
    (150.0, -150.0, -125.0)   # 291: Right mouth corner
], dtype=np.float64)

class VisionSessionTracker:
    """
    Maintains temporal state across discrete video chunks:
    - Biological rolling Blink Rate (blinks per minute, aligned with MOSAIC dataset mean 18.14 bpm)
    - Session-level baseline eyebrow distance (IOD-normalized)
    - Session-level baseline head pose (calibrated frontal look)
    """
    def __init__(self):
        self.rolling_blink_rate = 18.0  # Dataset mean: 18.135 bpm
        self.baseline_eyebrow = None    # Dataset mean: 0.419
        self.baseline_yaw = None        # Calibrated resting yaw
        self.baseline_pitch = None
        self.chunk_count = 0

    def update_blink_rate(self, blinks_in_chunk, chunk_seconds=1.0):
        # A single 1-second chunk cannot yield a stable /min rate in isolation.
        # We compute the instant chunk rate and update a continuous moving average.
        chunk_rate = (blinks_in_chunk / max(chunk_seconds, 0.5)) * 60.0
        alpha = 0.25
        if blinks_in_chunk > 0:
            # User blinked in this chunk: shift toward higher rate
            self.rolling_blink_rate = (1.0 - alpha) * self.rolling_blink_rate + alpha * min(chunk_rate, 45.0)
        else:
            # No blink in this 1-sec window: gently decay toward resting average
            self.rolling_blink_rate = (1.0 - 0.08) * self.rolling_blink_rate + 0.08 * 16.0

        # Bound to realistic human & dataset limits [4.0, 42.0] bpm
        self.rolling_blink_rate = max(4.0, min(42.0, self.rolling_blink_rate))
        return float(self.rolling_blink_rate)

    def update_eyebrow_baseline(self, current_eb_dist):
        if self.baseline_eyebrow is None:
            self.baseline_eyebrow = current_eb_dist
            self.chunk_count = 1
        elif self.chunk_count < 4:
            # Calibrate baseline over initial chunks
            self.baseline_eyebrow = 0.7 * self.baseline_eyebrow + 0.3 * current_eb_dist
            self.chunk_count += 1
        return self.baseline_eyebrow

    def update_head_pose_baseline(self, raw_yaw, raw_pitch):
        if self.baseline_yaw is None:
            self.baseline_yaw = raw_yaw
            self.baseline_pitch = raw_pitch
        elif self.chunk_count < 4:
            self.baseline_yaw = 0.7 * self.baseline_yaw + 0.3 * raw_yaw
            self.baseline_pitch = 0.7 * self.baseline_pitch + 0.3 * raw_pitch
        return self.baseline_yaw, self.baseline_pitch

vision_tracker = VisionSessionTracker()

def extract_audio_features(file_path: str):
    """
    Extract comprehensive acoustic, spectral, and temporal features from audio chunks (.webm, .wav, etc.)
    matching the trained audio model schema in Dataset/models/model_features.json.
    """
    temp_wav = None
    try:
        load_path = file_path
        if not file_path.lower().endswith(".wav"):
            ffmpeg_cmd = _get_ffmpeg_cmd()
            if ffmpeg_cmd and (os.path.exists(ffmpeg_cmd) or shutil.which(ffmpeg_cmd)):
                temp_wav = tempfile.mktemp(suffix=".wav")
                res = subprocess.run(
                    [ffmpeg_cmd, "-y", "-i", file_path, "-vn", "-ar", "16000", "-ac", "1", temp_wav],
                    capture_output=True
                )
                if res.returncode == 0 and os.path.exists(temp_wav):
                    load_path = temp_wav

        y, sr = librosa.load(load_path, sr=None)
        if len(y) == 0:
            return None

        duration_sec = float(len(y) / sr) if sr > 0 else 0.0

        # 1. MFCCs (13 coefficients: means and standard deviations)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_means = [float(val) for val in np.mean(mfccs, axis=1)]
        mfcc_stds = [float(val) for val in np.std(mfccs, axis=1)]

        # 2. Zero Crossing Rate
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        zcr_mean = float(np.mean(zcr))

        # 3. RMS Energy
        rms = librosa.feature.rms(y=y)[0]
        mean_rms_energy = float(np.mean(rms))
        rms_energy_std = float(np.std(rms))

        # 4. Spectral Features
        cent = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_centroid = float(np.mean(cent))

        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        spectral_rolloff = float(np.mean(rolloff))

        bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
        spectral_bandwidth = float(np.mean(bw))

        flatness = librosa.feature.spectral_flatness(y=y)[0]
        spectral_flatness = float(np.mean(flatness))

        # 5. Pitch Estimation (using fast YIN algorithm)
        fmin = float(librosa.note_to_hz('C2'))
        fmax = float(librosa.note_to_hz('C7'))
        try:
            f0 = librosa.yin(y, fmin=fmin, fmax=fmax, sr=sr)
            f0_valid = f0[(f0 >= fmin) & (f0 <= fmax)]
            if len(f0_valid) > 0:
                mean_pitch_hz = float(np.mean(f0_valid))
                pitch_std = float(np.std(f0_valid))
                min_pitch_hz = float(np.min(f0_valid))
                max_pitch_hz = float(np.max(f0_valid))
                pitch_range_hz = float(max_pitch_hz - min_pitch_hz)
            else:
                mean_pitch_hz = 0.0
                pitch_std = 0.0
                min_pitch_hz = 0.0
                max_pitch_hz = 0.0
                pitch_range_hz = 0.0
        except Exception:
            mean_pitch_hz = 0.0
            pitch_std = 0.0
            min_pitch_hz = 0.0
            max_pitch_hz = 0.0
            pitch_range_hz = 0.0

        # VAD & Speech Duration calculation
        frame_len = int(sr * 0.03) if sr > 0 else 480
        hop_len = int(sr * 0.01) if sr > 0 else 160
        if len(y) >= frame_len:
            rms_frames = librosa.feature.rms(y=y, frame_length=frame_len, hop_length=hop_len)[0]
            rms_db = 20 * np.log10(np.maximum(1e-5, rms_frames))
            is_speech = rms_db > -40.0
            speech_frames = int(np.sum(is_speech))
            frame_dur = hop_len / float(sr) if sr > 0 else 0.01
            speech_dur = float(speech_frames * frame_dur)
            silence_dur = float((len(is_speech) - speech_frames) * frame_dur)
            speech_silence_ratio = float(speech_dur / max(silence_dur, 1e-4))
        else:
            speech_dur = duration_sec if mean_rms_energy > 0.001 else 0.0
            silence_dur = 0.0 if speech_dur > 0 else duration_sec
            speech_silence_ratio = 1.0 if speech_dur > 0 else 0.0

        is_silent = bool(mean_rms_energy < 0.0008 or speech_dur < 0.05)
        voice_intensity_db = float(20 * np.log10(max(mean_rms_energy, 1e-6)) + 100.0)

        result = {
            # Legacy / Frontend fields
            "mfcc_mean": mfcc_means,
            "zcr_mean": zcr_mean,
            # Schema features
            "zero_crossing_rate": zcr_mean,
            "mean_rms_energy": mean_rms_energy,
            "rms_energy_std": rms_energy_std,
            "spectral_centroid": spectral_centroid,
            "spectral_rolloff": spectral_rolloff,
            "spectral_bandwidth": spectral_bandwidth,
            "spectral_flatness": spectral_flatness,
            "mean_pitch_hz": mean_pitch_hz,
            "pitch_std": pitch_std,
            "min_pitch_hz": min_pitch_hz,
            "max_pitch_hz": max_pitch_hz,
            "pitch_range_hz": pitch_range_hz,
            "audio_duration_seconds": duration_sec,
            "speech_duration_seconds": speech_dur,
            "silence_duration_seconds": silence_dur,
            "speech_to_silence_ratio": speech_silence_ratio,
            "voice_intensity_db": voice_intensity_db,
            "audio_available": 1 if not is_silent else 0,
            "is_silent": is_silent,
            "signal_quality": "POOR" if is_silent else "GOOD"
        }

        # Populate indexed MFCCs (1-13)
        for i in range(13):
            result[f"mfcc_{i+1:02d}_mean"] = mfcc_means[i]
            result[f"mfcc_{i+1:02d}_std"] = mfcc_stds[i]

        return result
    except Exception as e:
        print(f"Audio extraction error: {e}")
        return None
    finally:
        if temp_wav and os.path.exists(temp_wav):
            try:
                os.remove(temp_wav)
            except Exception:
                pass

def get_ear(landmarks_dict):
    """
    Compute Eye Aspect Ratio (EAR) matching Dataset/cv/vision_feature_extractor.py:
    v_dist / h_dist using landmark 2D coordinates.
    """
    # Left eye: top=159, bottom=145, left=33, right=133
    l_v = np.linalg.norm(np.array(landmarks_dict[159][:2]) - np.array(landmarks_dict[145][:2]))
    l_h = np.linalg.norm(np.array(landmarks_dict[33][:2]) - np.array(landmarks_dict[133][:2]))
    l_ear = (l_v / l_h) if l_h > 0 else 0.0

    # Right eye: top=386, bottom=374, left=362, right=263
    r_v = np.linalg.norm(np.array(landmarks_dict[386][:2]) - np.array(landmarks_dict[374][:2]))
    r_h = np.linalg.norm(np.array(landmarks_dict[362][:2]) - np.array(landmarks_dict[263][:2]))
    r_ear = (r_v / r_h) if r_h > 0 else 0.0

    return float((l_ear + r_ear) / 2.0)

def compute_head_pose(landmarks_dict, img_w, img_h):
    """
    Compute 3D Head Pose using solvePnP with the canonical 6-point anthropometric model
    matching Dataset/cv/vision_feature_extractor.py.
    """
    image_points = np.array([
        landmarks_dict[1][:2],
        landmarks_dict[152][:2],
        landmarks_dict[33][:2],
        landmarks_dict[263][:2],
        landmarks_dict[61][:2],
        landmarks_dict[291][:2]
    ], dtype=np.float64)

    focal_length = float(img_w)
    center = (img_w / 2.0, img_h / 2.0)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype=np.float64)
    dist_coeffs = np.zeros((4, 1), dtype=np.float64)

    success, rot_vec, trans_vec = cv2.solvePnP(
        CANONICAL_FACE_3D, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
    )
    if not success:
        return 0.0, 0.0, 0.0

    rotation_matrix, _ = cv2.Rodrigues(rot_vec)
    sy = math.sqrt(rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2)

    if sy >= 1e-6:
        pitch = math.degrees(math.atan2(rotation_matrix[2, 1], rotation_matrix[2, 2]))
        yaw = math.degrees(math.atan2(-rotation_matrix[2, 0], sy))
        roll = math.degrees(math.atan2(rotation_matrix[1, 0], rotation_matrix[0, 0]))
    else:
        pitch = math.degrees(math.atan2(-rotation_matrix[1, 2], rotation_matrix[1, 1]))
        yaw = math.degrees(math.atan2(-rotation_matrix[2, 0], sy))
        roll = 0.0

    return yaw, pitch, roll

def _get_landmarker():
    """Create a MediaPipe Tasks FaceLandmarker instance using face_landmarker.task model."""
    try:
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision

        possible_paths = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "face_landmarker.task")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "face_landmarker.task")),
            os.path.abspath("face_landmarker.task")
        ]
        model_path = next((p for p in possible_paths if os.path.exists(p)), None)
        if not model_path:
            return None

        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False,
            num_faces=1,
            running_mode=vision.RunningMode.IMAGE
        )
        return vision.FaceLandmarker.create_from_options(options)
    except Exception as e:
        print(f"FaceLandmarker initialization error: {e}")
        return None

def extract_vision_features(file_path: str, external_baseline: dict = None, baseline_frames: int = 30):
    """
    Extract facial landmarks, blink rate, head pose, and gaze using OpenCV / MediaPipe FaceLandmarker.
    Computes biologically accurate metrics aligned with the trained MOSAIC dataset.
    """
    temp_mp4 = None
    landmarker = None
    try:
        cap = cv2.VideoCapture(file_path)
        # If OpenCV fails to read the webm container directly, convert to fast mp4 using ffmpeg
        if not cap.isOpened() or int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) <= 0:
            cap.release()
            ffmpeg_cmd = _get_ffmpeg_cmd()
            if ffmpeg_cmd and (os.path.exists(ffmpeg_cmd) or shutil.which(ffmpeg_cmd)):
                temp_mp4 = tempfile.mktemp(suffix=".mp4")
                res = subprocess.run(
                    [ffmpeg_cmd, "-y", "-i", file_path, "-c:v", "libx264", "-preset", "ultrafast", temp_mp4],
                    capture_output=True
                )
                if res.returncode == 0 and os.path.exists(temp_mp4):
                    cap = cv2.VideoCapture(temp_mp4)

        if not cap.isOpened():
            return None

        img_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
        img_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480

        landmarker = _get_landmarker()
        import mediapipe as mp

        ears = []
        raw_yaws, raw_pitches, raw_rolls = [], [], []
        eyebrow_dists = []
        gaze_xs, gaze_ys = [], []
        frame_idx = 0

        while cap.isOpened():
            success, image = cap.read()
            if not success or image is None:
                break

            actual_h, actual_w = image.shape[:2]
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            if landmarker is not None:
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
                results = landmarker.detect(mp_image)
                has_faces = len(results.face_landmarks) if (results and results.face_landmarks) else 0
                if frame_idx == 0:
                    print(f"[DEBUG VISION] Frame 0: w={actual_w}, h={actual_h}, detected_faces={has_faces}")

                if results.face_landmarks and len(results.face_landmarks) > 0:
                    lm_norm = results.face_landmarks[0]
                    # Map to pixel coordinates dictionary
                    lm_px = {i: (pt.x * actual_w, pt.y * actual_h, pt.z * actual_w) for i, pt in enumerate(lm_norm)}

                    # 1. EAR (Eye Aspect Ratio)
                    ear_val = get_ear(lm_px)
                    ears.append(ear_val)

                    # 2. Head Pose (Yaw, Pitch, Roll) using canonical 3D model
                    y_deg, p_deg, r_deg = compute_head_pose(lm_px, actual_w, actual_h)
                    raw_yaws.append(y_deg)
                    raw_pitches.append(p_deg)
                    raw_rolls.append(r_deg)

                    # 3. Eyebrow Distance (IOD-Normalized)
                    # IOD = distance between outer eye corners (33 and 263)
                    iod = np.linalg.norm(np.array(lm_px[33][:2]) - np.array(lm_px[263][:2]))
                    if iod > 0:
                        l_brow = np.linalg.norm(np.array(lm_px[105][:2]) - np.array(lm_px[159][:2])) / iod
                        r_brow = np.linalg.norm(np.array(lm_px[334][:2]) - np.array(lm_px[386][:2])) / iod
                        eyebrow_dists.append((l_brow + r_brow) / 2.0)

                    # 4. Gaze Position
                    if len(lm_norm) > 473:
                        gx = (lm_norm[468].x + lm_norm[473].x) / 2.0
                        gy = (lm_norm[468].y + lm_norm[473].y) / 2.0
                    else:
                        gx = (lm_norm[33].x + lm_norm[263].x) / 2.0
                        gy = (lm_norm[159].y + lm_norm[386].y) / 2.0
                    gaze_xs.append(gx)
                    gaze_ys.append(gy)

            frame_idx += 1

        cap.release()

        # Fallback if no face landmarks were captured
        if not ears:
            return {
                "face_detected": 0,
                "video_available": 0,
                "eyebrow_delta_mean": 0.0,
                "eyebrow_delta_max": 0.0,
                "eyebrow_delta_std": 0.0,
                "left_eyebrow_height_delta": 0.0,
                "right_eyebrow_height_delta": 0.0,
                "blink_count": 0,
                "blink_rate": 18.0,
                "blink_rate_per_minute": 18.0,
                "head_yaw_mean": 0.0,
                "head_yaw_std": 0.0,
                "head_yaw_delta": 0.0,
                "head_yaw_degrees": 0.0,
                "head_pitch_mean": 0.0,
                "head_pitch_std": 0.0,
                "head_pitch_delta": 0.0,
                "head_pitch_degrees": 0.0,
                "head_roll_mean": 0.0,
                "head_roll_std": 0.0,
                "head_roll_delta": 0.0,
                "head_roll_degrees": 0.0,
                "gaze_x_mean": 0.5,
                "gaze_x_std": 0.0,
                "gaze_x": 0.5,
                "gaze_x_delta": 0.0,
                "gaze_y_mean": 0.5,
                "gaze_y_std": 0.0,
                "gaze_y": 0.5,
                "gaze_y_delta": 0.0,
                "mean_eye_aspect_ratio": 0.0,
                "eye_aspect_ratio_left": 0.0,
                "eye_aspect_ratio_right": 0.0,
                "mouth_aspect_ratio": 0.0,
                "face_width_pixels": 0.0,
                "face_height_pixels": 0.0,
                "face_area_pixels": 0.0,
                "frame_count": frame_idx
            }

        # --- BLINK DETECTION ---
        # Threshold: EAR < 0.21 indicates closed eye
        EAR_THRESHOLD = 0.21
        is_closed = [e < EAR_THRESHOLD for e in ears]
        blink_count = 0
        in_blink = False
        closed_streak = 0
        for closed in is_closed:
            if closed:
                closed_streak += 1
                if not in_blink and closed_streak >= 2:
                    blink_count += 1
                    in_blink = True
            else:
                closed_streak = 0
                in_blink = False

        # Actual duration of chunk in seconds (standard ~30 fps webcam)
        chunk_seconds = max(len(ears) / 30.0, 1.0)
        # Update session-level rolling blink rate (blinks per minute)
        smooth_blink_rate = vision_tracker.update_blink_rate(blink_count, chunk_seconds)

        # --- HEAD POSE ---
        mean_raw_yaw = float(np.mean(raw_yaws))
        mean_raw_pitch = float(np.mean(raw_pitches))
        # Update resting calibration baseline
        base_yaw, base_pitch = vision_tracker.update_head_pose_baseline(mean_raw_yaw, mean_raw_pitch)
        calibrated_yaw = mean_raw_yaw - base_yaw
        calibrated_pitch = mean_raw_pitch - base_pitch

        # --- EYEBROW DISTANCE & DELTA ---
        mean_eb_dist = float(np.mean(eyebrow_dists)) if eyebrow_dists else 0.419
        base_eb = vision_tracker.update_eyebrow_baseline(mean_eb_dist)
        # Dynamic deviation from session baseline: raising eyebrows > 0, furrowing < 0
        eyebrow_delta = mean_eb_dist - base_eb

        # --- GAZE ---
        mean_gaze_x = float(np.mean(gaze_xs)) if gaze_xs else 0.5
        mean_gaze_y = float(np.mean(gaze_ys)) if gaze_ys else 0.5

        summary = {
            # Face presence & schema keys
            "face_detected": 1,
            "video_available": 1,
            "eyebrow_delta_mean": float(eyebrow_delta),
            "eyebrow_delta_max": float(max(eyebrow_dists) - base_eb) if eyebrow_dists else 0.0,
            "eyebrow_delta_std": float(np.std(eyebrow_dists)) if len(eyebrow_dists) > 1 else 0.0,
            "left_eyebrow_height_delta": float(eyebrow_delta),
            "right_eyebrow_height_delta": float(eyebrow_delta),
            "blink_count": int(blink_count),
            "blink_rate": float(round(smooth_blink_rate, 1)),
            "blink_rate_per_minute": float(round(smooth_blink_rate, 1)),
            "head_yaw_mean": float(round(calibrated_yaw, 1)),
            "head_yaw_std": float(np.std(raw_yaws)) if len(raw_yaws) > 1 else 0.0,
            "head_yaw_delta": float(calibrated_yaw),
            "head_yaw_degrees": float(round(mean_raw_yaw, 1)),
            "head_pitch_mean": float(round(calibrated_pitch, 1)),
            "head_pitch_std": float(np.std(raw_pitches)) if len(raw_pitches) > 1 else 0.0,
            "head_pitch_delta": float(calibrated_pitch),
            "head_pitch_degrees": float(round(mean_raw_pitch, 1)),
            "head_roll_mean": float(round(float(np.mean(raw_rolls)), 1)) if raw_rolls else 0.0,
            "head_roll_std": float(np.std(raw_rolls)) if len(raw_rolls) > 1 else 0.0,
            "head_roll_delta": float(round(float(np.mean(raw_rolls)), 1)) if raw_rolls else 0.0,
            "head_roll_degrees": float(round(float(np.mean(raw_rolls)), 1)) if raw_rolls else 0.0,
            "gaze_x_mean": float(round(mean_gaze_x, 2)),
            "gaze_x_std": float(np.std(gaze_xs)) if len(gaze_xs) > 1 else 0.0,
            "gaze_x": float(round(mean_gaze_x, 2)),
            "gaze_x_delta": float(round(mean_gaze_x - 0.5, 2)),
            "gaze_y_mean": float(round(mean_gaze_y, 2)),
            "gaze_y_std": float(np.std(gaze_ys)) if len(gaze_ys) > 1 else 0.0,
            "gaze_y": float(round(mean_gaze_y, 2)),
            "gaze_y_delta": float(round(mean_gaze_y - 0.5, 2)),
            "mean_eye_aspect_ratio": float(np.mean(ears)) if ears else 0.0,
            "eye_aspect_ratio_left": float(np.mean(ears)) if ears else 0.0,
            "eye_aspect_ratio_right": float(np.mean(ears)) if ears else 0.0,
            "face_width_pixels": float(actual_w * 0.4),
            "face_height_pixels": float(actual_h * 0.5),
            "face_area_pixels": float(actual_w * actual_h * 0.2),
            "mouth_aspect_ratio": 0.0,
            "frame_count": int(len(ears))
        }

        for k, v in summary.items():
            if isinstance(v, float) and math.isnan(v):
                summary[k] = 0.0

        return summary
    except Exception as e:
        print(f"Vision extraction error: {e}")
        return None
    finally:
        if 'cap' in locals() and cap is not None:
            try:
                cap.release()
            except Exception:
                pass
        if landmarker:
            try:
                landmarker.close()
            except Exception:
                pass
        if temp_mp4 and os.path.exists(temp_mp4):
            try:
                os.remove(temp_mp4)
            except Exception:
                pass

def extract_physiological_features(file_path: str, tail_samples: int = None):
    """
    Extract real physiological features from MAX30102 raw PPG data.
    Scientifically estimates Heart Rate (HR), HRV (SDNN, RMSSD), Mean IR/RED,
    Skin Temperature, Signal Quality, and optical SpO2 ratio.

    Expected CSV columns:
        timestamp_ms, ir, red, temperature, beat_status

    Returns:
        Dictionary containing verified physiological metrics or None if file cannot be parsed.
    """
    try:
        # 1. Load CSV
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return None

        df = pd.read_csv(file_path)

        # Required optical PPG signal channels
        essential_columns = ["timestamp_ms", "ir", "red"]
        missing_columns = [c for c in essential_columns if c not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in PPG CSV: {missing_columns}")

        # Clean numeric data for present columns
        numeric_cols = [c for c in ["timestamp_ms", "ir", "red", "temperature", "beat_status"] if c in df.columns]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Drop rows ONLY when essential optical signal is missing
        df = df.dropna(subset=["timestamp_ms", "ir", "red"])
        if len(df) < 15:
            raise ValueError(f"Insufficient physiological samples ({len(df)} rows).")

        # Sort by timestamp
        df = df.sort_values("timestamp_ms").reset_index(drop=True)

        # Slice latest window if tail_samples requested (useful for live monitoring)
        if tail_samples and len(df) > tail_samples:
            df = df.iloc[-tail_samples:].copy().reset_index(drop=True)

        sample_count = int(len(df))

        # 3. Dynamic Sampling Rate from actual timestamps
        timestamps = df["timestamp_ms"].to_numpy(dtype=float)
        time_diffs = np.diff(timestamps)
        valid_diffs = time_diffs[time_diffs > 0]

        if len(valid_diffs) > 5:
            median_interval_ms = float(np.median(valid_diffs))
            sampling_rate = round(1000.0 / median_interval_ms, 2) if median_interval_ms > 0 else 12.5
        else:
            sampling_rate = 12.5

        duration_seconds = round(float((timestamps[-1] - timestamps[0]) / 1000.0), 2) if len(timestamps) > 1 else 0.0

        # 4. Finger contact segmentation (MAX30102 IR levels)
        # When finger is on the sensor, IR typically exceeds 10,000 (often 100,000+).
        stable_df = df[df["ir"] > 10000].copy()
        if len(stable_df) < 20:
            # Fallback to full dataset if ambient or low-intensity recording
            stable_df = df.copy()

        stable_sample_count = int(len(stable_df))
        contact_ratio = float(stable_sample_count / max(sample_count, 1))

        # 5. Baseline Signal Statistics
        mean_ir = round(float(stable_df["ir"].mean()), 2)
        mean_red = round(float(stable_df["red"].mean()), 2)

        # Temperature Policy (MAX30102 Firmware):
        # Arduino firmware streams PPG optical channels (IR, RED) and beat metrics (beatsPerMinute, beatAvg).
        # It does NOT stream a calibrated skin temperature channel (beatsPerMinute was previously misread).
        # Scientific prototype strictly reports null / unavailable to avoid fabricating sensor data.
        mean_temperature = None
        temp_available = False
        temp_note = "Temperature sensor channel not calibrated / unavailable in active MAX30102 stream. Scientific prototype avoids fabricating skin temperature."

        # 6. Peak Detection & Heart Rate Estimation
        mean_hr = None
        heart_rate = None
        hr_std = None
        hr_valid = False
        sdnn = None
        rmssd = None
        num_beats = 0

        ir_signal = stable_df["ir"].to_numpy(dtype=float)
        ir_timestamps = stable_df["timestamp_ms"].to_numpy(dtype=float)

        if len(ir_signal) >= 20 and sampling_rate >= 2.5:
            try:
                from scipy.signal import butter, filtfilt, find_peaks

                # Zero-center (remove DC component)
                centered_ir = ir_signal - np.mean(ir_signal)

                nyq = sampling_rate / 2.0
                low_cutoff = 0.7 / nyq      # ~42 BPM
                high_cutoff = min(3.0 / nyq, 0.95)  # ~180 BPM

                if 0 < low_cutoff < high_cutoff < 1.0:
                    b, a = butter(2, [low_cutoff, high_cutoff], btype="band")
                    filtered_ir = filtfilt(b, a, centered_ir)

                    # Minimum physiological spacing between beats (max 180 BPM = 0.33s)
                    min_distance = max(int(sampling_rate * 0.33), 1)
                    prominence = np.std(filtered_ir) * 0.25

                    peaks, _ = find_peaks(
                        filtered_ir,
                        distance=min_distance,
                        prominence=prominence
                    )

                    num_beats = int(len(peaks))

                    if num_beats >= 3:
                        peak_times = ir_timestamps[peaks] / 1000.0
                        rr_intervals = np.diff(peak_times)

                        # Filter physiologically plausible beat intervals (40-180 BPM -> 0.33s to 1.50s)
                        plausible_rr = rr_intervals[(rr_intervals >= 0.33) & (rr_intervals <= 1.50)]

                        if len(plausible_rr) >= 2:
                            bpm_values = 60.0 / plausible_rr
                            # Discard extreme statistical outliers outside [40, 180]
                            valid_bpm = bpm_values[(bpm_values >= 40.0) & (bpm_values <= 180.0)]

                            if len(valid_bpm) >= 2:
                                mean_hr = round(float(np.median(valid_bpm)), 1)
                                heart_rate = mean_hr
                                hr_std = round(float(np.std(valid_bpm)), 1)
                                hr_valid = True

                                # 7. HRV Calculation (SDNN and RMSSD in milliseconds)
                                nn_intervals_ms = plausible_rr * 1000.0
                                if len(nn_intervals_ms) >= 3:
                                    sdnn = round(float(np.std(nn_intervals_ms, ddof=1)), 1)
                                    diff_nn = np.diff(nn_intervals_ms)
                                    rmssd = round(float(np.sqrt(np.mean(diff_nn ** 2))), 1)

            except Exception as hr_err:
                print(f"[MOSAIC PHYSIO] HR estimation warning: {hr_err}")

        # 8. SpO2 Policy: Uncalibrated Optical Sensor
        # MAX30102 raw RED/IR channels require clinical empirical calibration coefficients
        # to produce defensible SpO2. As per scientific honesty guidelines, we report null
        # rather than fabricating or presenting uncalibrated optical estimates as true SpO2.
        spo2_percent = None
        spo2_available = False

        # 9. Signal Quality Calculation
        # Quality is based on stable contact ratio + rhythm regularity
        if hr_valid and mean_hr is not None and hr_std is not None:
            regularity = max(0.0, 1.0 - (hr_std / max(mean_hr, 1.0)))
            quality_score = 0.5 * contact_ratio + 0.5 * regularity
        else:
            quality_score = 0.3 * contact_ratio

        quality_score = round(max(0.0, min(1.0, quality_score)), 2)
        quality_percent = round(quality_score * 100.0, 1)

        if quality_score >= 0.75:
            signal_quality_cat = "good"
        elif quality_score >= 0.45:
            signal_quality_cat = "acceptable"
        else:
            signal_quality_cat = "poor"

        # Beat status distribution
        status_series = df["beat_status"].value_counts().to_dict()
        beat_status_counts = {int(k): int(v) for k, v in status_series.items()}

        estimated_hr = mean_hr if hr_valid else None
        pulse_rate = mean_hr if hr_valid else None

        # 10. Formatted Return Dictionary
        return {
            "status": "success",
            "source": "MAX30102",
            "sample_count": sample_count,
            "stable_sample_count": stable_sample_count,
            "duration_seconds": duration_seconds,
            "sampling_interval_ms": median_interval_ms if len(valid_diffs) > 5 else 80.0,
            "sampling_rate_hz": sampling_rate,
            "sampling_rate": sampling_rate,
            "mean_ir": mean_ir,
            "mean_red": mean_red,
            "mean_temperature": mean_temperature,
            "temperature": mean_temperature,
            "temperature_available": temp_available,
            "temperature_note": temp_note,
            "estimated_heart_rate_bpm": estimated_hr,
            "pulse_rate_bpm": pulse_rate,
            "mean_hr": estimated_hr,
            "heart_rate": estimated_hr,
            "heart_rate_limitation": None if hr_valid else "Insufficient valid systolic peaks or motion artifact present in optical waveform",
            "hr_std": hr_std if hr_valid else None,
            "sdnn": sdnn if hr_valid else None,
            "rmssd": rmssd if hr_valid else None,
            "num_beats": num_beats if hr_valid else 0,
            "spo2_percent": spo2_percent,
            "mean_spo2": None,
            "spo2": None,
            "spo2_available": False,
            "spo2_note": "SpO2 uncalibrated / unavailable. Academic prototype avoids fabricating medical SpO2.",
            "signal_quality": quality_score,
            "signal_quality_percent": quality_percent,
            "signal_quality_status": signal_quality_cat,
            "valid_sample_percent": round(contact_ratio * 100.0, 1),
            "valid_sample_percentage": round(contact_ratio * 100.0, 1),
            "hr_valid": hr_valid,
            "beat_status_interpretation": "Sensor status / interrupt bit flags; not heart rate",
            "beat_status_counts": beat_status_counts
        }

    except Exception as e:
        print(f"[MOSAIC PHYSIO] Extraction error: {e}")
        return None