# Phase 11: Laptop Camera & Microphone Integration Report

## Objective
Integrate the laptop's built-in camera and microphone into the MOSAIC Next.js dashboard using the browser's `navigator.mediaDevices.getUserMedia()` API, and connect them to the existing Phase 7 and Phase 8 Python feature extraction pipelines.

## Architecture
1. **Frontend Integration**:
   - The `SystemContext` was extended to manage live media streams (`isCameraActive`, `isMicActive`) alongside the existing pipeline states.
   - We utilized the HTML5 `<video>` element to render the live Camera feed directly in the browser when active.
   - Simulation mode acts as a strict guardrail: when activated, live sensors are immediately stopped and replaced with UI placeholders to ensure live data is not accidentally mixed with dataset simulations.
   - The React UI periodically captures 3-second chunks of active media via `MediaRecorder` and uploads them to the backend for processing.

2. **Backend API Expansion**:
   - `main.py` was extended with two new endpoints: `POST /api/extract/vision` and `POST /api/extract/audio`.
   - These endpoints utilize FastAPI's `UploadFile` to stream incoming video/audio blobs into temporary files (`tempfile.mkstemp`).
   - The temporary files are passed directly to the existing Python extraction logic (`extract_vision_features` and `extract_audio_features`), fulfilling the requirement to reuse the Phase 7/7.2 extractors.

3. **Inference Safety**:
   - The Late Fusion output is explicitly labeled as "PENDING" when real hardware is active, with a warning that multimodal inference is awaiting Physiological Sensor Integration (Phase 12).
   - We do *not* fabricate values to force the ML model to predict.
   - We explicitly state the classification is experimental and not a lie detector.

## Files Changed
- `backend/main.py`: Added extraction API endpoints and `python-multipart` / `aiofiles` dependencies.
- `frontend/src/context/SystemContext.tsx`: Added state and async handlers for `startCamera` and `startMicrophone`.
- `frontend/src/app/live/page.tsx`: Rewrote the Live Monitoring page to include live `<video>` streams, feature extraction polling, and "Pending Hardware" UI states for inference.

## Limitations & Next Steps
- **Latency**: Because we are polling 3-second chunks of `.webm` data and running them through Python MediaPipe on the backend, there is an inherent ~3 second delay in metric updates (Gaze, Blinks, ZCR). 
- **Physiology**: The system is actively waiting for Phase 12 to integrate the MAX30102 via the ESP32-C3 for physiological inputs before running the final Late Fusion model.

## Commands to Run

**1. Start the Backend:**
To serve the feature extraction APIs, ensure your backend is running:
```bash
cd d:\MOSAIC\backend
venv\Scripts\activate
pip install -r requirements.txt # Ensure python-multipart and aiofiles are installed
uvicorn main:app --reload --port 8000
```

**2. Start the Frontend:**
```bash
cd d:\MOSAIC\frontend
npm run dev
```
