from typing import TypedDict

VALID_QUALITIES = {"GOOD", "FAIR", "POOR", "WARNING"}

class InferenceResult(TypedDict):
    physiology_probability: float
    audio_probability: float
    vision_probability: float
    fusion_probability: float
    classification: str
    physiology_available: bool
    audio_available: bool
    vision_available: bool
    signal_quality: str
    model_version: str
