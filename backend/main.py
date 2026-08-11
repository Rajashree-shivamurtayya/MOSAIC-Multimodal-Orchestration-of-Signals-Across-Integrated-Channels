from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MOSAIC Backend API",
    description="Multi-Model Orchestration of Signals Across Integrated Channels",
    version="1.0.0"
)

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the MOSAIC API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/trials")
def get_trials():
    # Mock data for frontend integration
    return [
        {"id": 1, "participant": "P001", "status": "completed", "prediction": "truthful", "confidence": 0.89},
        {"id": 2, "participant": "P002", "status": "processing", "prediction": None, "confidence": None}
    ]

@app.post("/api/predict")
def run_prediction(trial_id: int):
    # Mock ML prediction endpoint
    return {
        "trial_id": trial_id,
        "prediction": "deceptive",
        "confidence": 0.75,
        "modality_scores": {
            "audio": 0.8,
            "vision": 0.6,
            "physiological": 0.7
        }
    }
