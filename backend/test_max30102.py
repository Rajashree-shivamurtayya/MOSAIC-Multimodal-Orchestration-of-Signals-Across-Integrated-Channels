import os
import sys
import time
import csv
import re
import argparse
import serial
import serial.tools.list_ports

# ============================================================
# MOSAIC - MAX30102 Serial Data Collector
# Acquisition layer for ESP32-C3 via USB Serial COM3
# Saves raw physiological data to mosaic_ppg.csv
# ============================================================

DEFAULT_PORT = "COM3"
DEFAULT_BAUD = 115200
DEFAULT_OUTPUT_FILE = "mosaic_ppg.csv"
CSV_HEADER = ["timestamp_ms", "ir", "red", "temperature", "beat_status"]


def parse_args():
    parser = argparse.ArgumentParser(
        description="MOSAIC MAX30102 Real-Time PPG Acquisition"
    )
    parser.add_argument(
        "--port",
        type=str,
        default=DEFAULT_PORT,
        help=f"Serial port (default: {DEFAULT_PORT})"
    )
    parser.add_argument(
        "--baud",
        type=int,
        default=DEFAULT_BAUD,
        help=f"Baud rate (default: {DEFAULT_BAUD})"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output CSV file path (default: {DEFAULT_OUTPUT_FILE})"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--append",
        action="store_true",
        default=True,
        help="Append readings to existing CSV without overwriting (default: True)"
    )
    group.add_argument(
        "--new",
        action="store_true",
        help="Start a fresh CSV recording (overwrites existing file)"
    )
    return parser.parse_args()


def parse_serial_record(line: str):
    """
    Parses incoming serial record. Supports:
    1. Standard Arduino PBA format: PPG,timestamp_ms,ir,red,beatsPerMinute,beatAvg
    2. Formatted: Samples: <id> | IR=<ir> | RED=<red> | BPM=<bpm> | Status=<status>
    
    Returns:
        tuple (timestamp_ms, ir, red, bpm, beat_status) or None
    """
    line = line.strip()
    if not line:
        return None

    # Primary Format: PPG,timestamp_ms,IR,RED,beatsPerMinute,beatAvg
    if line.startswith("PPG,") or line.startswith("ppg,"):
        parts = line.split(",")
        if len(parts) >= 6:
            try:
                ts = int(parts[1].strip())
                ir = int(parts[2].strip())
                red = int(parts[3].strip())
                bpm = float(parts[4].strip())
                status = int(parts[5].strip())
                return ts, ir, red, bpm, status
            except (ValueError, IndexError):
                return None

    # Legacy text format fallback
    pattern = (
        r"Samples?:\s*(\d+)"
        r"\s*\|\s*IR=(\d+)"
        r"\s*\|\s*RED=(\d+)"
        r"\s*\|\s*(?:Temp|BPM)=([-+]?\d*\.?\d+)"
        r"\s*\|\s*(?:Status|Avg)=(\d+)"
    )
    match = re.search(pattern, line, re.IGNORECASE)
    if match:
        try:
            sample_idx = int(match.group(1))
            ts = int(time.time() * 1000)
            ir = int(match.group(2))
            red = int(match.group(3))
            bpm = float(match.group(4))
            status = int(match.group(5))
            return ts, ir, red, bpm, status
        except (ValueError, IndexError):
            return None

    return None


def main():
    args = parse_args()
    port = args.port
    baud = args.baud
    output_path = os.path.abspath(args.output)
    append_mode = not args.new

    print("=" * 60)
    print("MOSAIC MAX30102 PPG DATA COLLECTOR")
    print("Multimodal Orchestration of Signals Across Integrated Channels")
    print("=" * 60)
    print(f"Serial Port : {port}")
    print(f"Baud Rate   : {baud}")
    print(f"Output File : {output_path}")
    print(f"Write Mode  : {'APPEND' if append_mode else 'NEW (Fresh Recording)'}")
    print()

    # 1. Connect to serial port with auto-detection fallback
    available_ports = [p.device for p in serial.tools.list_ports.comports()]
    if port not in available_ports and available_ports:
        print(f"[PORT NOTICE] Requested {port} not found. Available: {available_ports}")
        port = available_ports[0]
        print(f"[PORT NOTICE] Auto-selected {port}")

    print(f"Opening {port}...")
    ser = None
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baud,
            timeout=1.0
        )
    except serial.SerialException as e:
        print(f"\nERROR: Could not open {port}.")
        print(f"Details: {e}")
        print("\nTroubleshooting Steps:")
        print(f"1. Verify that the ESP32-C3 is firmly plugged into USB.")
        print(f"2. Ensure the Arduino Serial Monitor or any other terminal is CLOSED.")
        print(f"3. Ensure no other Python script is accessing {port}.")
        print(f"4. Available serial ports on this system: {available_ports}")
        sys.exit(1)

    # Allow ESP32 time to reboot and stabilize after DTR/RTS trigger
    print("Connected to ESP32-C3.")
    print("Waiting 2 seconds for sensor stabilization...")
    time.sleep(2)
    ser.reset_input_buffer()

    print(f"Writing physiological data to {os.path.basename(output_path)}")
    print("Press Ctrl+C to stop recording.\n")

    # 2. Setup CSV
    file_exists = os.path.exists(output_path)
    file_mode = "a" if append_mode else "w"
    needs_header = True

    if append_mode and file_exists and os.path.getsize(output_path) > 0:
        # Check if header already exists
        with open(output_path, "r", encoding="utf-8", errors="ignore") as f:
            first_line = f.readline()
            if "timestamp_ms" in first_line:
                needs_header = False

    csv_file = open(output_path, mode=file_mode, newline="", encoding="utf-8")
    writer = csv.writer(csv_file)

    if needs_header:
        writer.writerow(CSV_HEADER)
        csv_file.flush()

    # 3. Acquisition loop
    sample_count = 0
    start_time = time.time()
    last_flush_time = time.time()

    try:
        while True:
            try:
                raw_bytes = ser.readline()
            except (serial.SerialException, OSError) as read_err:
                print(f"\n[WARNING] Serial read error: {read_err}")
                print("Attempting to reconnect in 2 seconds...")
                time.sleep(2)
                try:
                    ser.close()
                    ser = serial.Serial(port=port, baudrate=baud, timeout=1.0)
                    ser.reset_input_buffer()
                    print("Reconnected to serial port.")
                    continue
                except Exception:
                    print("Reconnection failed. Halting acquisition.")
                    break

            if not raw_bytes:
                continue

            line = raw_bytes.decode("utf-8", errors="ignore").strip()
            if not line:
                continue

            record = parse_serial_record(line)
            if record is None:
                # Discard non-PPG debug lines silently
                continue

            ts_ms, ir_val, red_val, bpm_val, status_val = record

            # Append valid sensor row (column 4 stores bpm value from Arduino PBA)
            writer.writerow([ts_ms, ir_val, red_val, f"{bpm_val:.2f}", status_val])
            sample_count += 1

            # Regularly flush buffer to avoid loss on sudden termination
            now = time.time()
            if now - last_flush_time >= 0.5:
                csv_file.flush()
                last_flush_time = now

            # Live readable status
            print(
                f"Samples: {sample_count:5d} | "
                f"IR={ir_val:7d} | "
                f"RED={red_val:6d} | "
                f"BPM={bpm_val:5.1f} | "
                f"Avg={status_val:2d}",
                flush=True
            )

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        if ser and ser.is_open:
            try:
                ser.close()
            except Exception:
                pass
        if csv_file and not csv_file.closed:
            try:
                csv_file.flush()
                csv_file.close()
            except Exception:
                pass

        duration = time.time() - start_time
        print("=" * 60)
        print("DATA COLLECTION SUMMARY")
        print("=" * 60)
        print(f"Samples saved : {sample_count}")
        print(f"Elapsed time  : {duration:.2f} s")
        if duration > 0 and sample_count > 0:
            print(f"Sampling rate : {sample_count / duration:.2f} Hz")
        print(f"Output CSV    : {output_path}")
        print(f"{port} closed.")
        print("=" * 60)


if __name__ == "__main__":
    main()