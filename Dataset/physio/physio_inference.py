import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from inference.predict import predict_trial
from physio.physio_feature_extractor import PhysioFeatureExtractor

class PhysioInferencePipeline:
    def __init__(self):
        self.extractor = PhysioFeatureExtractor()
        
    def predict(self, baseline_packets, answer_packets):
        physio_features, quality = self.extractor.extract_trial_features(baseline_packets, answer_packets)
        
        trial_dict = {
            "audio_available": 0,
            "video_available": 0,
            "overall_trial_quality": quality
        }
        trial_dict.update(physio_features)
        
        result = predict_trial(trial_dict)
        return result
