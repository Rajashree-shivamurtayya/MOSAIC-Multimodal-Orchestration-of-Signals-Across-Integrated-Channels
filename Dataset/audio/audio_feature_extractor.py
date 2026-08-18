import numpy as np
import librosa
import os
import json

class AudioFeatureExtractor:
    def __init__(self, sample_rate=16000):
        self.sr = sample_rate
        self.frame_length_ms = 30
        self.hop_length_ms = 10
        self.frame_length = int(self.sr * self.frame_length_ms / 1000)
        self.hop_length = int(self.sr * self.hop_length_ms / 1000)

    def _vad(self, y, threshold=-40):
        if len(y) < self.frame_length:
            return np.array([])
        rms = librosa.feature.rms(y=y, frame_length=self.frame_length, hop_length=self.hop_length)[0]
        rms_db = 20 * np.log10(np.maximum(1e-5, rms))
        is_speech = rms_db > threshold
        return is_speech

    def _extract_vad_features(self, is_speech):
        if len(is_speech) == 0:
            return 0, 0, 0, 0, 0, 0, 0

        frame_dur = self.hop_length_ms / 1000.0
        
        speech_frames = np.sum(is_speech)
        speech_dur = speech_frames * frame_dur
        silence_dur = (len(is_speech) - speech_frames) * frame_dur
        
        first_speech = np.argmax(is_speech)
        if first_speech == 0 and not is_speech[0]:
            latency = len(is_speech) * frame_dur * 1000
        else:
            latency = first_speech * frame_dur * 1000

        changes = np.diff(is_speech.astype(int))
        starts = np.where(changes == 1)[0]
        ends = np.where(changes == -1)[0]
        
        pauses = []
        if len(ends) > 0 and len(starts) > 0:
            for e in ends:
                next_starts = starts[starts > e]
                if len(next_starts) > 0:
                    pauses.append((next_starts[0] - e) * frame_dur * 1000)
        
        pause_count = len(pauses)
        mean_pause = np.mean(pauses) if pause_count > 0 else 0
        max_pause = np.max(pauses) if pause_count > 0 else 0
        pause_ratio = (np.sum(pauses)/1000) / (speech_dur + silence_dur) if (speech_dur + silence_dur) > 0 else 0
        
        return latency, speech_dur, silence_dur, pause_count, mean_pause, max_pause, pause_ratio

    def _extract_acoustic_features(self, y):
        features = {}
        if len(y) == 0:
            return features
            
        f0, voiced_flag, _ = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr=self.sr)
        f0_valid = f0[voiced_flag]
        if len(f0_valid) > 0:
            features['mean_pitch_hz'] = np.mean(f0_valid)
            features['pitch_std'] = np.std(f0_valid)
            features['min_pitch_hz'] = np.min(f0_valid)
            features['max_pitch_hz'] = np.max(f0_valid)
            features['pitch_range_hz'] = np.max(f0_valid) - np.min(f0_valid)
        else:
            features['mean_pitch_hz'] = 0
            features['pitch_std'] = 0
            features['min_pitch_hz'] = 0
            features['max_pitch_hz'] = 0
            features['pitch_range_hz'] = 0

        rms = librosa.feature.rms(y=y)[0]
        features['mean_rms_energy'] = np.mean(rms)
        features['rms_energy_std'] = np.std(rms)
        
        cent = librosa.feature.spectral_centroid(y=y, sr=self.sr)[0]
        features['spectral_centroid'] = np.mean(cent)
        
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=self.sr)[0]
        features['spectral_rolloff'] = np.mean(rolloff)
        
        bw = librosa.feature.spectral_bandwidth(y=y, sr=self.sr)[0]
        features['spectral_bandwidth'] = np.mean(bw)
        
        flatness = librosa.feature.spectral_flatness(y=y)[0]
        features['spectral_flatness'] = np.mean(flatness)
        
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        features['zero_crossing_rate'] = np.mean(zcr)
        
        mfccs = librosa.feature.mfcc(y=y, sr=self.sr, n_mfcc=13)
        for i in range(13):
            features[f'mfcc_{i+1:02d}_mean'] = np.mean(mfccs[i])
            features[f'mfcc_{i+1:02d}_std'] = np.std(mfccs[i])
            
        return features

    def extract_trial_features(self, baseline_audio, answer_audio):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(base_dir, "models", "model_features.json")) as f:
            schema_keys = json.load(f)["audio_features"]

        features = {k: np.nan for k in schema_keys}
        
        if len(answer_audio) == 0:
            features["audio_available"] = 0
            return features, "POOR"
            
        features["audio_available"] = 1
        
        if isinstance(answer_audio, list):
            if len(answer_audio) > 0:
                y_ans = np.concatenate(answer_audio).flatten()
            else:
                y_ans = np.array([])
        else:
            y_ans = answer_audio.flatten()
            
        if len(y_ans) < self.frame_length:
            return features, "POOR"
            
        is_speech = self._vad(y_ans)
        latency, s_dur, sil_dur, p_cnt, p_mean, p_max, p_ratio = self._extract_vad_features(is_speech)
        
        features["response_latency_ms"] = latency
        features["speech_duration_seconds"] = s_dur
        features["silence_duration_seconds"] = sil_dur
        features["pause_count"] = p_cnt
        features["mean_pause_duration_ms"] = p_mean
        features["max_pause_duration_ms"] = p_max
        features["pause_ratio"] = p_ratio
        features["audio_duration_seconds"] = len(y_ans) / self.sr
        
        ac_feat = self._extract_acoustic_features(y_ans)
        for k, v in ac_feat.items():
            if k in features:
                features[k] = v
                
        if s_dur == 0:
            quality = "POOR"
        elif features.get("mean_rms_energy", 0) < 0.001:
            quality = "FAIR"
        else:
            quality = "GOOD"
            
        return features, quality
