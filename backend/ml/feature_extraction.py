import numpy as np
import pandas as pd
import cv2
import mediapipe as mp
import librosa
import math

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_stylesdef extract_audio_features(file_path: str):
    """
    Extract MFCC, Pitch, and Pauses from Audio.
    """
    try:
        y, sr = librosa.load(file_path, sr=None)
        # Extract MFCCs
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfccs, axis=1)
        
        # Pitch extraction (simple mock using zero crossing rate as placeholder)
        zcr = librosa.feature.zero_crossing_rate(y)
        zcr_mean = np.mean(zcr)
        
        return {
            "mfcc_mean": mfcc_mean.tolist(),
            "zcr_mean": zcr_mean
        }
    except Exception as e:
        print(f"Audio extraction error: {e}")
        return None

def get_ear(landmarks, eye_indices):
    p1 = np.array([landmarks[eye_indices[0]].x, landmarks[eye_indices[0]].y])
    p2 = np.array([landmarks[eye_indices[1]].x, landmarks[eye_indices[1]].y])
    p3 = np.array([landmarks[eye_indices[2]].x, landmarks[eye_indices[2]].y])
    p4 = np.array([landmarks[eye_indices[3]].x, landmarks[eye_indices[3]].y])
    p5 = np.array([landmarks[eye_indices[4]].x, landmarks[eye_indices[4]].y])
    p6 = np.array([landmarks[eye_indices[5]].x, landmarks[eye_indices[5]].y])
    ear = (np.linalg.norm(p2 - p6) + np.linalg.norm(p3 - p5)) / (2.0 * np.linalg.norm(p1 - p4))
    return ear

def get_head_pose(landmarks, img_w, img_h):
    face_3d = []
    face_2d = []
    for idx in [1, 152, 33, 263, 61, 291]:
        lm = landmarks[idx]
        x, y = int(lm.x * img_w), int(lm.y * img_h)
        face_2d.append([x, y])
        face_3d.append([x, y, lm.z])
    face_2d = np.array(face_2d, dtype=np.float64)
    face_3d = np.array(face_3d, dtype=np.float64)
    focal_length = 1 * img_w
    cam_matrix = np.array([[focal_length, 0, img_h / 2], [0, focal_length, img_w / 2], [0, 0, 1]])
    dist_matrix = np.zeros((4, 1), dtype=np.float64)
    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
    rmat, _ = cv2.Rodrigues(rot_vec)
    angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
    return angles[1] * 360, angles[0] * 360, angles[2] * 360 # yaw, pitch, roll

def extract_vision_features(file_path: str, external_baseline: dict = None, baseline_frames: int = 30):
    """
    Extract facial landmarks, blink rate, and gaze using OpenCV / MediaPipe.
    """
    try:
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            return None
        img_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        img_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0: fps = 30

        left_eye_indices = [33, 160, 158, 133, 153, 144]
        right_eye_indices = [362, 385, 387, 263, 373, 380]
        left_eyebrow_idx, right_eyebrow_idx = 105, 334
        left_eye_center_idx, right_eye_center_idx = 159, 386

        features_list = []
        with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:
            frame_idx = 0
            while cap.isOpened():
                success, image = cap.read()
                if not success: break
                image.flags.writeable = False
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(image_rgb)

                if results.multi_face_landmarks:
                    landmarks = results.multi_face_landmarks[0].landmark
                    ear_avg = (get_ear(landmarks, left_eye_indices) + get_ear(landmarks, right_eye_indices)) / 2.0
                    yaw, pitch, roll = get_head_pose(landmarks, img_w, img_h)

                    left_eb = np.array([landmarks[left_eyebrow_idx].x, landmarks[left_eyebrow_idx].y])
                    left_eye = np.array([landmarks[left_eye_center_idx].x, landmarks[left_eye_center_idx].y])
                    left_eb_dist = np.linalg.norm(left_eb - left_eye)

                    right_eb = np.array([landmarks[right_eyebrow_idx].x, landmarks[right_eyebrow_idx].y])
                    right_eye = np.array([landmarks[right_eye_center_idx].x, landmarks[right_eye_center_idx].y])
                    right_eb_dist = np.linalg.norm(right_eb - right_eye)

                    gaze_x = (landmarks[468].x + landmarks[473].x) / 2.0
                    gaze_y = (landmarks[468].y + landmarks[473].y) / 2.0
                    
                    features_list.append({
                        'frame': frame_idx, 'ear': ear_avg, 'yaw': yaw, 'pitch': pitch, 'roll': roll,
                        'left_eb_dist': left_eb_dist, 'right_eb_dist': right_eb_dist,
                        'gaze_x': gaze_x, 'gaze_y': gaze_y
                    })
                frame_idx += 1
        cap.release()

        if not features_list: return None
        df_feat = pd.DataFrame(features_list)
        
        if external_baseline:
            baseline = pd.Series(external_baseline)
        else:
            baseline = df_feat.iloc[:baseline_frames].mean()
        
        left_eb_delta = df_feat['left_eb_dist'] - baseline['left_eb_dist']
        right_eb_delta = df_feat['right_eb_dist'] - baseline['right_eb_dist']
        
        blink_frames = df_feat['ear'] < 0.2
        blink_count = (blink_frames & ~blink_frames.shift(1).fillna(False)).sum()
        blink_rate = blink_count / (len(df_feat) / fps / 60.0) if len(df_feat) > 0 else 0

        summary = {
            "eyebrow_delta_mean": float(left_eb_delta.mean() + right_eb_delta.mean()) / 2.0,
            "eyebrow_delta_max": float(max(left_eb_delta.max(), right_eb_delta.max())),
            "eyebrow_delta_std": float((left_eb_delta.std() + right_eb_delta.std()) / 2.0),
            "blink_count": int(blink_count),
            "blink_rate": float(blink_rate),
            "head_yaw_mean": float(df_feat['yaw'].mean()),
            "head_yaw_std": float(df_feat['yaw'].std()),
            "head_yaw_delta": float((df_feat['yaw'] - baseline['yaw']).mean()),
            "head_pitch_mean": float(df_feat['pitch'].mean()),
            "head_pitch_std": float(df_feat['pitch'].std()),
            "head_pitch_delta": float((df_feat['pitch'] - baseline['pitch']).mean()),
            "gaze_x_mean": float(df_feat['gaze_x'].mean()),
            "gaze_x_std": float(df_feat['gaze_x'].std()),
            "gaze_y_mean": float(df_feat['gaze_y'].mean()),
            "gaze_y_std": float(df_feat['gaze_y'].std()),
            "frame_count": int(len(df_feat))
        }
        for k, v in summary.items():
            if np.isnan(v): summary[k] = 0.0
        return summary
    except Exception as e:
        print(f"Vision extraction error: {e}")
        return None

def extract_physiological_features(file_path: str):
    """
    Extract HRV, pulse rate from raw PPG CSV data.
    """
    try:
        df = pd.read_csv(file_path)
        # Example: assuming df has columns 'timestamp', 'ppg', 'hr', 'spo2'
        mean_hr = df['hr'].mean()
        mean_spo2 = df['spo2'].mean()
        
        return {
            "mean_hr": mean_hr,
            "mean_spo2": mean_spo2
        }
    except Exception as e:
        print(f"Physio extraction error: {e}")
        return None
