import numpy as np
import math
import cv2
import json
import os

LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145
LEFT_EYE_LEFT = 33
LEFT_EYE_RIGHT = 133
RIGHT_EYE_TOP = 386
RIGHT_EYE_BOTTOM = 374
RIGHT_EYE_LEFT = 362
RIGHT_EYE_RIGHT = 263
LEFT_BROW = 105
RIGHT_BROW = 334

class VisionFeatureExtractor:
    def __init__(self, fps=30):
        self.fps = fps

    def compute_ear(self, landmarks, top, bottom, left, right):
        # Strict 2D Euclidean distance to match standard webcam logic
        v_dist = np.linalg.norm(landmarks[top][:2] - landmarks[bottom][:2])
        h_dist = np.linalg.norm(landmarks[left][:2] - landmarks[right][:2])
        return v_dist / h_dist if h_dist > 0 else 0

    def compute_eyebrow_distance(self, landmarks, brow, eye_top, eye_left, eye_right):
        # Strict 2D Euclidean distance
        brow_dist = np.linalg.norm(landmarks[brow][:2] - landmarks[eye_top][:2])
        iod = np.linalg.norm(landmarks[LEFT_EYE_LEFT][:2] - landmarks[RIGHT_EYE_RIGHT][:2])
        return brow_dist / iod if iod > 0 else 0
        
    def compute_mar(self, landmarks):
        # Mouth aspect ratio
        v_dist = np.linalg.norm(landmarks[13][:2] - landmarks[14][:2])
        h_dist = np.linalg.norm(landmarks[78][:2] - landmarks[308][:2])
        return v_dist / h_dist if h_dist > 0 else 0

    def compute_face_metrics(self, landmarks):
        xs = [pt[0] for pt in landmarks]
        ys = [pt[1] for pt in landmarks]
        w = max(xs) - min(xs)
        h = max(ys) - min(ys)
        return w * h, w, h

    def compute_head_pose(self, landmarks, w, h):
        NOSE_TIP = 1
        CHIN = 152
        LEFT_EYE = 33
        RIGHT_EYE = 263
        LEFT_MOUTH = 61
        RIGHT_MOUTH = 291

        image_points = np.array([
            landmarks[NOSE_TIP][:2],
            landmarks[CHIN][:2],
            landmarks[LEFT_EYE][:2],
            landmarks[RIGHT_EYE][:2],
            landmarks[LEFT_MOUTH][:2],
            landmarks[RIGHT_MOUTH][:2]
        ], dtype="double")

        model_points = np.array([
            (0.0, 0.0, 0.0),
            (0.0, -330.0, -65.0),
            (-225.0, 170.0, -135.0),
            (225.0, 170.0, -135.0),
            (-150.0, -150.0, -125.0),
            (150.0, -150.0, -125.0)
        ])

        focal_length = w
        center = (w/2, h/2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype="double"
        )

        dist_coeffs = np.zeros((4,1))
        success, rotation_vector, translation_vector = cv2.solvePnP(
            model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
        )

        if not success:
            return 0, 0, 0

        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
        sy = math.sqrt(rotation_matrix[0,0] * rotation_matrix[0,0] +  rotation_matrix[1,0] * rotation_matrix[1,0])
        singular = sy < 1e-6

        if not singular:
            x = math.atan2(rotation_matrix[2,1] , rotation_matrix[2,2])
            y = math.atan2(-rotation_matrix[2,0], sy)
            z = math.atan2(rotation_matrix[1,0], rotation_matrix[0,0])
        else:
            x = math.atan2(-rotation_matrix[1,2], rotation_matrix[1,1])
            y = math.atan2(-rotation_matrix[2,0], sy)
            z = 0

        pitch = math.degrees(x)
        yaw = math.degrees(y)
        roll = math.degrees(z)

        return yaw, pitch, roll

    def extract_trial_features(self, baseline_frames, answer_frames, w=640, h=480):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(base_dir, "models", "model_features.json")) as f:
            schema_keys = json.load(f)["vision_features"]

        features = {k: np.nan for k in schema_keys}
        
        valid_baseline = [f for f in baseline_frames if f is not None]
        valid_answer = [f for f in answer_frames if f is not None]
        
        total_frames = len(baseline_frames) + len(answer_frames)
        valid_total = len(valid_baseline) + len(valid_answer)
        
        if valid_total == 0:
            features["video_available"] = 0
            return features, "POOR"
            
        features["video_available"] = 1
        
        b_left_brow, b_right_brow, b_left_ear, b_right_ear = [], [], [], []
        b_yaw, b_pitch, b_roll = [], [], []
        b_gaze_x, b_gaze_y = [], []
        
        # 468 landmarks natively + 10 iris landmarks (468-477) if refine_landmarks=True
        # iris centers: 468 (left eye), 473 (right eye)
        
        for lm in valid_baseline:
            b_left_brow.append(self.compute_eyebrow_distance(lm, LEFT_BROW, LEFT_EYE_TOP, LEFT_EYE_LEFT, LEFT_EYE_RIGHT))
            b_right_brow.append(self.compute_eyebrow_distance(lm, RIGHT_BROW, RIGHT_EYE_TOP, RIGHT_EYE_LEFT, RIGHT_EYE_RIGHT))
            b_left_ear.append(self.compute_ear(lm, LEFT_EYE_TOP, LEFT_EYE_BOTTOM, LEFT_EYE_LEFT, LEFT_EYE_RIGHT))
            b_right_ear.append(self.compute_ear(lm, RIGHT_EYE_TOP, RIGHT_EYE_BOTTOM, RIGHT_EYE_LEFT, RIGHT_EYE_RIGHT))
            y, p, r = self.compute_head_pose(lm, w, h)
            b_yaw.append(y); b_pitch.append(p); b_roll.append(r)
            if len(lm) > 473:
                b_gaze_x.append((lm[468][0] + lm[473][0]) / 2)
                b_gaze_y.append((lm[468][1] + lm[473][1]) / 2)
            else:
                b_gaze_x.append((lm[LEFT_EYE_LEFT][0] + lm[RIGHT_EYE_RIGHT][0]) / 2)
                b_gaze_y.append((lm[LEFT_EYE_TOP][1] + lm[RIGHT_EYE_TOP][1]) / 2)
            
        base_l_brow = np.mean(b_left_brow) if b_left_brow else 0
        base_r_brow = np.mean(b_right_brow) if b_right_brow else 0
        base_l_ear = np.mean(b_left_ear) if b_left_ear else 0
        base_r_ear = np.mean(b_right_ear) if b_right_ear else 0
        base_y = np.mean(b_yaw) if b_yaw else 0
        base_p = np.mean(b_pitch) if b_pitch else 0
        base_r = np.mean(b_roll) if b_roll else 0
        base_gaze_x = np.mean(b_gaze_x) if b_gaze_x else 0
        base_gaze_y = np.mean(b_gaze_y) if b_gaze_y else 0
        
        features["baseline_left_eyebrow_eye_distance"] = base_l_brow
        features["baseline_right_eyebrow_eye_distance"] = base_r_brow
        features["baseline_left_eye_openness"] = base_l_ear
        features["baseline_right_eye_openness"] = base_r_ear
        features["baseline_head_yaw"] = base_y
        features["baseline_head_pitch"] = base_p
        features["baseline_head_roll"] = base_r
        features["baseline_gaze_x"] = base_gaze_x
        features["baseline_gaze_y"] = base_gaze_y
        
        if len(valid_answer) == 0:
            return features, "POOR"
            
        a_left_brow, a_right_brow, a_left_ear, a_right_ear, a_mar = [], [], [], [], []
        a_yaw, a_pitch, a_roll = [], [], []
        a_areas, a_widths, a_heights = [], [], []
        a_gaze_x, a_gaze_y = [], []
        
        for lm in valid_answer:
            a_left_brow.append(self.compute_eyebrow_distance(lm, LEFT_BROW, LEFT_EYE_TOP, LEFT_EYE_LEFT, LEFT_EYE_RIGHT))
            a_right_brow.append(self.compute_eyebrow_distance(lm, RIGHT_BROW, RIGHT_EYE_TOP, RIGHT_EYE_LEFT, RIGHT_EYE_RIGHT))
            a_left_ear.append(self.compute_ear(lm, LEFT_EYE_TOP, LEFT_EYE_BOTTOM, LEFT_EYE_LEFT, LEFT_EYE_RIGHT))
            a_right_ear.append(self.compute_ear(lm, RIGHT_EYE_TOP, RIGHT_EYE_BOTTOM, RIGHT_EYE_LEFT, RIGHT_EYE_RIGHT))
            a_mar.append(self.compute_mar(lm))
            y, p, r = self.compute_head_pose(lm, w, h)
            a_yaw.append(y); a_pitch.append(p); a_roll.append(r)
            area, fw, fh = self.compute_face_metrics(lm)
            a_areas.append(area); a_widths.append(fw); a_heights.append(fh)
            
            if len(lm) > 473:
                a_gaze_x.append((lm[468][0] + lm[473][0]) / 2)
                a_gaze_y.append((lm[468][1] + lm[473][1]) / 2)
            else:
                a_gaze_x.append((lm[LEFT_EYE_LEFT][0] + lm[RIGHT_EYE_RIGHT][0]) / 2)
                a_gaze_y.append((lm[LEFT_EYE_TOP][1] + lm[RIGHT_EYE_TOP][1]) / 2)
            
        # Eyebrows
        mean_l_brow = np.mean(a_left_brow)
        mean_r_brow = np.mean(a_right_brow)
        features["left_eyebrow_eye_distance"] = mean_l_brow
        features["right_eyebrow_eye_distance"] = mean_r_brow
        features["left_eyebrow_height_delta"] = mean_l_brow - base_l_brow
        features["right_eyebrow_height_delta"] = mean_r_brow - base_r_brow
        features["left_eyebrow_movement_std"] = np.std(a_left_brow)
        features["right_eyebrow_movement_std"] = np.std(a_right_brow)
        features["left_eyebrow_peak_raise"] = np.max(a_left_brow) - base_l_brow
        features["right_eyebrow_peak_raise"] = np.max(a_right_brow) - base_r_brow
        features["left_eyebrow_raise_ratio"] = mean_l_brow / base_l_brow if base_l_brow > 0 else 1.0
        features["right_eyebrow_raise_ratio"] = mean_r_brow / base_r_brow if base_r_brow > 0 else 1.0
        
        # Eyebrow Velocity
        l_brow_vel = np.diff(a_left_brow) * self.fps
        r_brow_vel = np.diff(a_right_brow) * self.fps
        features["left_eyebrow_velocity"] = np.mean(np.abs(l_brow_vel)) if len(l_brow_vel) > 0 else 0
        features["right_eyebrow_velocity"] = np.mean(np.abs(r_brow_vel)) if len(r_brow_vel) > 0 else 0
        
        # Eyes
        mean_l_ear = np.mean(a_left_ear)
        mean_r_ear = np.mean(a_right_ear)
        features["eye_aspect_ratio_left"] = mean_l_ear
        features["eye_aspect_ratio_right"] = mean_r_ear
        features["mean_eye_aspect_ratio"] = (mean_l_ear + mean_r_ear) / 2
        features["left_eye_openness"] = mean_l_ear
        features["right_eye_openness"] = mean_r_ear
        features["left_eye_openness_delta"] = mean_l_ear - base_l_ear
        features["right_eye_openness_delta"] = mean_r_ear - base_r_ear
        
        # Blink and Eye Closure Duration
        EAR_THRESH = 0.2
        is_closed = [ear < EAR_THRESH for ear in a_left_ear]
        blink_count = 0
        closure_frames = 0
        in_blink = False
        for c in is_closed:
            if c:
                closure_frames += 1
                if not in_blink:
                    blink_count += 1
                    in_blink = True
            else:
                in_blink = False
                
        features["blink_count"] = blink_count
        features["eye_closure_duration_ms"] = (closure_frames / self.fps) * 1000
        
        # Head Pose
        features["head_yaw_degrees"] = np.mean(a_yaw)
        features["head_pitch_degrees"] = np.mean(a_pitch)
        features["head_roll_degrees"] = np.mean(a_roll)
        features["head_yaw_delta"] = np.mean(a_yaw) - base_y
        features["head_pitch_delta"] = np.mean(a_pitch) - base_p
        features["head_roll_delta"] = np.mean(a_roll) - base_r
        features["head_yaw_std"] = np.std(a_yaw)
        features["head_pitch_std"] = np.std(a_pitch)
        features["head_roll_std"] = np.std(a_roll)
        
        camera_look_frames = sum(1 for y, p in zip(a_yaw, a_pitch) if abs(y) < 15 and abs(p) < 15)
        features["time_looking_at_camera_seconds"] = camera_look_frames / self.fps
        features["time_looking_away_seconds"] = (len(a_yaw) - camera_look_frames) / self.fps
        
        # Gaze
        g_x_delta = np.mean(a_gaze_x) - base_gaze_x
        g_y_delta = np.mean(a_gaze_y) - base_gaze_y
        features["gaze_x"] = np.mean(a_gaze_x)
        features["gaze_y"] = np.mean(a_gaze_y)
        features["gaze_x_delta"] = g_x_delta
        features["gaze_y_delta"] = g_y_delta
        
        gaze_vel = np.diff(a_gaze_x) * self.fps
        gaze_shifts = sum(1 for v in gaze_vel if abs(v) > 5) # Heuristic
        features["gaze_shift_count"] = gaze_shifts
        features["gaze_shift_frequency"] = gaze_shifts / (len(a_gaze_x) / self.fps) if len(a_gaze_x) > 0 else 0
        
        # Face Metrics
        features["face_area_pixels"] = np.mean(a_areas)
        features["face_width_pixels"] = np.mean(a_widths)
        features["face_height_pixels"] = np.mean(a_heights)
        
        # Mouth
        mar_vel = np.diff(a_mar) * self.fps
        mouth_moves = sum(1 for v in mar_vel if abs(v) > 0.1)
        features["mouth_movement_frequency"] = mouth_moves / (len(a_mar) / self.fps) if len(a_mar) > 0 else 0
        features["mouth_aspect_ratio"] = np.mean(a_mar)
        
        # Facial Motion
        motion = []
        for i in range(1, len(valid_answer)):
            diff = np.linalg.norm(valid_answer[i] - valid_answer[i-1], axis=1).mean()
            motion.append(diff)
            
        features["facial_motion_mean"] = np.mean(motion) if motion else 0
        features["facial_motion_peak"] = np.max(motion) if motion else 0
        features["facial_motion_std"] = np.std(motion) if motion else 0
        features["facial_landmark_velocity_mean"] = np.mean(motion) * self.fps if motion else 0
        features["facial_landmark_velocity_max"] = np.max(motion) * self.fps if motion else 0
        
        features["face_detected"] = 1
        
        valid_ratio = valid_total / total_frames if total_frames > 0 else 0
        
        if valid_ratio > 0.8:
            quality = "GOOD"
        elif valid_ratio > 0.4:
            quality = "FAIR"
        else:
            quality = "POOR"
            
        return features, quality
