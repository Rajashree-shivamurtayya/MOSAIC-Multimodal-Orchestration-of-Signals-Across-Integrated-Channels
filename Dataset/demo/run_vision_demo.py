import sys
import os
import cv2
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from cv.camera import Camera
from cv.face_landmarks import FaceLandmarkExtractor
from cv.vision_inference import VisionInferencePipeline

def main():
    print("Starting MOSAIC Vision Demo...")
    extractor = FaceLandmarkExtractor(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    pipeline = VisionInferencePipeline(fps=30)
    
    BASELINE_DURATION = 5.0
    ANSWER_DURATION = 15.0
    
    baseline_frames = []
    answer_frames = []
    
    state = "BASELINE"
    start_time = time.time()
    
    result = None
    
    # Do not crash if no webcam is present, but fail gracefully for demo purposes
    try:
        cam = Camera(0)
        cam.open()
    except RuntimeError:
        print("No webcam found. Skipping live demo.")
        return

    while True:
        ret, frame = cam.read_frame()
        if not ret:
            break
            
        h, w, _ = frame.shape
        landmarks = extractor.extract(frame)
        elapsed = time.time() - start_time
        
        if state == "BASELINE":
            baseline_frames.append(landmarks)
            if elapsed > BASELINE_DURATION:
                state = "ANSWER"
                start_time = time.time()
                elapsed = 0
        elif state == "ANSWER":
            answer_frames.append(landmarks)
            if elapsed > ANSWER_DURATION:
                state = "PROCESSING"
        
        cv2.putText(frame, f"State: {state}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        if state == "BASELINE":
            cv2.putText(frame, f"Time: {BASELINE_DURATION - elapsed:.1f}s", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif state == "ANSWER":
            cv2.putText(frame, f"Time: {ANSWER_DURATION - elapsed:.1f}s", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
        if state == "PROCESSING" and result is None:
            cv2.putText(frame, "Calculating features...", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
            cv2.imshow("MOSAIC Vision Demo", frame)
            cv2.waitKey(1)
            
            result = pipeline.predict(baseline_frames, answer_frames, w, h)
            state = "DONE"
            
        if state == "DONE":
            cv2.putText(frame, "INFERENCE COMPLETE", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, f"Vision Prob: {result['vision_probability']:.2f}", (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.putText(frame, f"Class: {result['classification']}", (30, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.putText(frame, f"Quality: {result['signal_quality']}", (30, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            
            cv2.putText(frame, "Press 'R' to restart, 'Q' to quit", (30, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        if landmarks is not None and state != "DONE":
            for pt in landmarks:
                cv2.circle(frame, (int(pt[0]), int(pt[1])), 1, (0, 255, 0), -1)

        cv2.imshow("MOSAIC Vision Demo", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r') and state == "DONE":
            baseline_frames = []
            answer_frames = []
            state = "BASELINE"
            start_time = time.time()
            result = None
            
    extractor.close()
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
