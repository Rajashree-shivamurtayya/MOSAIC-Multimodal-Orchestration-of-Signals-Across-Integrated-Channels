import serial
import json
import time
import random
import threading
import queue

class BaseSerialCapture:
    def __init__(self):
        self.q = queue.Queue()
        self.is_running = False
        self._thread = None
        
    def start(self):
        pass
        
    def stop(self):
        pass
        
    def read_packets(self):
        packets = []
        while not self.q.empty():
            packets.append(self.q.get())
        return packets

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


class RealSerialCapture(BaseSerialCapture):
    def __init__(self, port, baudrate=115200):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        
    def _read_loop(self):
        while self.is_running:
            if self.ser and self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line:
                        packet = json.loads(line)
                        self.q.put(packet)
                except Exception:
                    pass
            time.sleep(0.01)

    def start(self):
        if self.is_running: return
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        self.is_running = True
        self._thread = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self.is_running = False
        if self._thread:
            self._thread.join(timeout=1.0)
        if self.ser:
            self.ser.close()


class MockSerialCapture(BaseSerialCapture):
    def __init__(self, frequency=50):
        super().__init__()
        self.frequency = frequency # Packets per second
        
    def _mock_loop(self):
        print("[MOCK SERIAL] SIMULATION / REPLAY MODE STARTED")
        base_hr = 75.0
        base_spo2 = 98.0
        
        while self.is_running:
            packet = {
                "timestamp": int(time.time() * 1000),
                "hr": base_hr + random.uniform(-2, 2),
                "spo2": min(100.0, base_spo2 + random.uniform(-1, 1)),
                "ir": random.randint(50000, 60000),
                "red": random.randint(50000, 60000),
                "contact": True
            }
            self.q.put(packet)
            base_hr += random.uniform(-0.1, 0.1)
            time.sleep(1.0 / self.frequency)

    def start(self):
        if self.is_running: return
        self.is_running = True
        self._thread = threading.Thread(target=self._mock_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self.is_running = False
        if self._thread:
            self._thread.join(timeout=1.0)
        print("[MOCK SERIAL] SIMULATION / REPLAY MODE STOPPED")
