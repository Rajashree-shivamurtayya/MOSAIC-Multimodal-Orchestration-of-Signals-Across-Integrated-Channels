import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from inference.predict import predict_trial
from audio.audio_feature_extractor import AudioFeatureExtractor

class AudioInferencePipeline:
    def __init__(self, sample_rate=16000):
        self.extractor = AudioFeatureExtractor(sample_rate=sample_rate)
        
    def predict(self, baseline_audio, answer_audio):
        audio_features, quality = self.extractor.extract_trial_features(baseline_audio, answer_audio)
        
        trial_dict = {
            "physiological_available": 0,
            "video_available": 0,
            "overall_trial_quality": quality
        }
        trial_dict.update(audio_features)
        
        result = predict_trial(trial_dict)
        return result
