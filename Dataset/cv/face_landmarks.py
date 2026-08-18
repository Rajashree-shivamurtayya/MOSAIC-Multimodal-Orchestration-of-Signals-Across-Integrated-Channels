import cv2
import mediapipe as mp
import numpy as np

class FaceLandmarkExtractor:
    def __init__(self, static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=static_image_mode,
            max_num_faces=max_num_faces,
            refine_landmarks=True, # Iris landmarks
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def extract(self, bgr_frame):
        rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            return None
            
        landmarks_normalized = results.multi_face_landmarks[0].landmark
        
        h, w, _ = bgr_frame.shape
        landmarks_px = []
        for lm in landmarks_normalized:
            landmarks_px.append((lm.x * w, lm.y * h, lm.z * w))
            
        return np.array(landmarks_px)

    def close(self):
        self.face_mesh.close()
