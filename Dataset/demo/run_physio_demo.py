import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from physio.serial_capture import MockSerialCapture
from physio.physio_inference import PhysioInferencePipeline

def main():
    print("========================================")
    print("     MOSAIC PHYSIOLOGY INFERENCE DEMO   ")
    print("========================================")
    print("NOTE: HARDWARE NOT CONNECTED.")
    print("USING SIMULATION / REPLAY MODE ONLY.")
    print("========================================")
    
    pipeline = PhysioInferencePipeline()
    
    BASELINE_DUR = 5.0
    ANSWER_DUR = 15.0
    
    try:
        with MockSerialCapture(frequency=50) as sensor:
            print("\nSensor: MOCK (Connected)")
            print("Reading Baseline (simulating 5s)...")
            time.sleep(BASELINE_DUR)
            baseline_packets = sensor.read_packets()
            print(f"Baseline packets collected: {len(baseline_packets)}")
            
            print("Reading Answer (simulating 15s)...")
            time.sleep(ANSWER_DUR)
            answer_packets = sensor.read_packets()
            print(f"Answer packets collected: {len(answer_packets)}")
            
            print("Processing features...")
            result = pipeline.predict(baseline_packets, answer_packets)
            
            print("\n========================================")
            print("          PHYSIOLOGICAL ANALYSIS        ")
            print("========================================")
            print("Mode: SIMULATION / REPLAY")
            print(f"Signal quality: {result.get('signal_quality', 'UNKNOWN')}")
            
            print(f"\nExperimental deceptive-class probability: {result.get('physiology_probability', 0.5)*100:.1f}%")
            print("========================================")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
