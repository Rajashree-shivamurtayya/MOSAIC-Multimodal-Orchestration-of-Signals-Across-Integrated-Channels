import sounddevice as sd
import numpy as np
import threading
import queue

class AudioCapture:
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.q = queue.Queue()
        self.stream = None
        self.is_recording = False
        
    def _audio_callback(self, indata, frames, time, status):
        if status:
            pass # Could log buffer underflow/overflow
        self.q.put(indata.copy())

    def start(self):
        if self.is_recording:
            return
            
        try:
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=self._audio_callback
            )
            self.stream.start()
            self.is_recording = True
        except Exception as e:
            raise RuntimeError(f"Failed to start audio stream: {e}")

    def read_frames(self):
        frames = []
        while not self.q.empty():
            frames.append(self.q.get())
        if frames:
            return np.concatenate(frames, axis=0)
        return np.array([])

    def stop(self):
        if self.is_recording and self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
            self.is_recording = False
            
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
