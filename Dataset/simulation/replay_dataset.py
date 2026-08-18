import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from simulation.sensor_adapter import CSVSensorAdapter
from inference.predict import predict_trial

def main():
    adapter = CSVSensorAdapter()
    participant_id = adapter.df["participant_id"].iloc[0]
    trials = adapter.get_trials_for_participant(participant_id)
    
    for i, trial in enumerate(trials, start=1):
        res = predict_trial(trial)
        
        print("-" * 40)
        print(f"Participant: {participant_id}")
        print(f"Trial: {i}\n")
        
        print(f"Physiology probability: {res['physiology_probability']:.2f}")
        print(f"Audio probability:      {res['audio_probability']:.2f}")
        print(f"Vision probability:     {res['vision_probability']:.2f}")
        print(f"Fusion probability:     {res['fusion_probability']:.2f}\n")
        
        print("Experimental classification:")
        print(f"{res['classification']}\n")
        
        print("Signal quality:")
        print(f"{res['signal_quality']}\n")
        
        print("Modalities:")
        print(f"Physiology: {'AVAILABLE' if res['physiology_available'] else 'MISSING'}")
        print(f"Audio:      {'AVAILABLE' if res['audio_available'] else 'MISSING'}")
        print(f"Vision:     {'AVAILABLE' if res['vision_available'] else 'MISSING'}")
        
    print("-" * 40)

if __name__ == "__main__":
    main()
