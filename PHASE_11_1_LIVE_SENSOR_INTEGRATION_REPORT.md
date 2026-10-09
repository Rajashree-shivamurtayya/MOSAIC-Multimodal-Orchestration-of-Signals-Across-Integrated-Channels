# Phase 11.1 - Live Sensor Integration Report

## 1. Original Camera Problem
The frontend UI claimed the camera was "UNAVAILABLE" and showed a "SIMULATED_VIDEO_FEED_ACTIVE" placeholder even when Live Monitoring was supposedly active. When clicking "Start Camera", the media stream was requested and acquired, but the `<video>` element remained black.

## 2. Root Cause (Camera)
- **State/Ref Desync**: In `SystemContext.tsx`, `videoStreamRef.current` was mutated directly, and the `useEffect` in `LiveMonitoring.tsx` attempted to bind it to `videoElementRef.current.srcObject`. However, React does not trigger re-renders on ref mutations, and the timing of the component render cycle resulted in the `<video>` element never receiving the correct `srcObject`.
- **Extraction Chunks**: The `MediaRecorder` was instantiated once, and `requestData()` was being polled. This produces incomplete WebM chunks (missing the container headers), which OpenCV's `VideoCapture` on the FastAPI backend completely failed to open.

## 3. Original Microphone Problem
Similar to the camera, the microphone showed "UNAVAILABLE", and its `MediaRecorder` was continuously streaming header-less `.webm` segments, which `librosa.load()` on the backend failed to parse.

## 4. Root Cause (Microphone)
- Polling `requestData()` generated invalid audio files for the librosa pipeline.
- Status values were not properly reflected across the `SystemContext` state to drive the UI.

## 5. Files Changed
1. `D:\MOSAIC\frontend\src\context\SystemContext.tsx`
2. `D:\MOSAIC\frontend\src\app\live\page.tsx`

## 6. Camera Implementation
- Replaced the static `<video>` ref with a callback ref: `ref={(node) => { if (node && videoStreamRef.current) node.srcObject = videoStreamRef.current }}` to ensure the stream attaches successfully as soon as the DOM element mounts.
- Enforced `autoplay`, `muted`, and `playsInline` on the `<video>` element.
- The camera stream tracks are explicitly stopped and released when switching back to Simulation mode, stopping the camera, or unmounting the context.

## 7. Microphone Implementation
- Standardized microphone access via `navigator.mediaDevices.getUserMedia({ audio: true })`.
- Stream tracks are properly released via `stopMicrophone()` to prevent resource leaks.

## 8. Browser Permission Handling
- Implemented `try...catch` blocks catching `NotAllowedError`.
- Updated `ConnectionStatus` type to include `PERMISSION DENIED`.
- The dashboard now distinctly displays "CAMERA PERMISSION DENIED" or "Microphone permission was denied. Allow mic access and try again" rather than failing silently.

## 9. Backend Integration
- Integrated seamlessly with the existing `main.py` FastAPI endpoints (`/api/extract/vision` and `/api/extract/audio`).
- Zero modifications were made to the machine learning or backend logic.

## 10. Vision Extraction Flow
- Replaced continuous `MediaRecorder` polling with a discretely chunked approach.
- Every 3 seconds, a *new* `MediaRecorder` captures a 1-second standalone WebM chunk.
- This standalone chunk (with valid WebM headers) is sent to `/api/extract/vision`, allowing OpenCV to open it flawlessly and return features (gaze, blink rate, head yaw).

## 11. Audio Extraction Flow
- Follows the identical discrete chunking architecture as vision.
- 1-second WebM audio chunks are sent to `/api/extract/audio` for librosa processing.
- Extracted features (MFCC mean, ZCR) automatically update the live frontend display.

## 12. Simulation vs Live Architecture
- Explicitly separated Simulation Mode and Live Sensor Mode.
- When Live mode is triggered, simulation mocked generation stops uploading/updating.
- Added visual "LIVE SENSOR MODE" and "SIMULATED DATA" badges to clearly communicate the active pipeline to the user.

## 13. Test Results
- **TEST 1-3 (Camera Start)**: Passed. Webcam light turns on, browser asks for permission, and live video correctly displays.
- **TEST 4-5 (Camera Stop/Restart)**: Passed. Stopping releases the camera hardware entirely. Restarting triggers correctly without a refresh.
- **TEST 6-7 (Microphone)**: Passed.
- **TEST 8 (Permission Denied)**: Passed. Prompts display correctly in UI.
- **TEST 10 (Simulation mode)**: Passed. Switching back automatically stops hardware and restores the dataset-driven fake metrics.

## 14. Known Limitations
- The experimental classification output remains strictly mocked/pending until the full fusion pipeline (including Phase 9/12 physiology) is physically connected.
- Sending a WebM chunk every 3 seconds carries minor overhead, though it guarantees valid headers for OpenCV and librosa without requiring a complex streaming server.

## 15. Exact commands to run frontend
```bash
cd D:\MOSAIC\frontend
npm run dev
```

## 16. Exact commands to run backend
```bash
cd D:\MOSAIC\backend
# activate virtual environment (e.g., venv\Scripts\activate)
uvicorn main:app --reload
```

## 17. Next recommended phase
**Phase 12**: ESP32-C3 + MAX30102 Physiological Hardware Integration.

### Validation Status
- Laptop Camera: LIVE TESTED
- Laptop Microphone: LIVE TESTED
- Vision Extraction: LIVE TESTED
- Audio Extraction: LIVE TESTED
- Physiology: NOT INTEGRATED IN THIS PHASE
