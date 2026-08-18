import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from inference.predict import predict_trial
from cv.vision_feature_extractor import VisionFeatureExtractor

class VisionInferencePipeline:
    def __init__(self, fps=30):
        self.extractor = VisionFeatureExtractor(fps=fps)
        
    def predict(self, baseline_frames, answer_frames, w, h):
        vision_features, quality = self.extractor.extract_trial_features(baseline_frames, answer_frames, w, h)
        
        trial_dict = {
            "physiological_available": 0,
            "audio_available": 0,
            "overall_trial_quality": quality
        }
        trial_dict.update(vision_features)
        
        result = predict_trial(trial_dict)
        return result
