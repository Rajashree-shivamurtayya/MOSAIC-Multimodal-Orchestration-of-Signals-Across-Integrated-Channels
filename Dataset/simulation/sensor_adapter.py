import pandas as pd
import os

class CSVSensorAdapter:
    def __init__(self, csv_path: str = "processed/mosaic_clean.csv"):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        full_path = os.path.join(base_dir, csv_path)
        self.df = pd.read_csv(full_path)
        
    def get_trials_for_participant(self, participant_id: str):
        """Yields one trial at a time for the given participant."""
        participant_data = self.df[self.df["participant_id"] == participant_id]
        if participant_data.empty:
            raise ValueError(f"Participant {participant_id} not found.")
            
        for _, row in participant_data.iterrows():
            yield row.to_dict()
