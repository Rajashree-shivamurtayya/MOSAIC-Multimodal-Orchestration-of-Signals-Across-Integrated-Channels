import sys
import os
import time
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from audio.audio_capture import AudioCapture
from audio.audio_inference import AudioInferencePipeline

def main():
    print("========================================")
    print("      MOSAIC AUDIO INFERENCE DEMO       ")
    print("========================================")
    
    pipeline = AudioInferencePipeline(sample_rate=16000)
    
    BASELINE_DUR = 5.0
    ANSWER_DUR = 15.0
    
    try:
        with AudioCapture(16000, 1) as cam:
            print("\nMicrophone: Connected")
            print("Listening for Baseline...")
            
            time.sleep(BASELINE_DUR)
            baseline_audio = cam.read_frames()
            print("Baseline captured.")
            
            print("Listening for Answer...")
            time.sleep(ANSWER_DUR)
            answer_audio = cam.read_frames()
            print("Answer captured.")
            
            print("Processing features...")
            result = pipeline.predict([baseline_audio], [answer_audio])
            
            print("\n========================================")
            print("             AUDIO ANALYSIS             ")
            print("========================================")
            print("Microphone: Connected")
            
            # The inference engine wraps result dict slightly differently from just returning raw schema
            # It returns {"classification": ..., "audio_probability": ...} but doesn't pass through all inputs
            # To get speech_duration we need it from extractor, or we just trust 'signal_quality'
            print(f"Speech: {'Detected' if result.get('signal_quality', '') != 'POOR' else 'Not Detected'}")
            print(f"Signal quality: {result.get('signal_quality', 'UNKNOWN')}")
            
            print(f"\nExperimental deceptive-class probability: {result.get('audio_probability', 0.5)*100:.1f}%")
            print("========================================")
            
    except RuntimeError as e:
        print(f"Audio Error: {e}")

if __name__ == "__main__":
    main()
