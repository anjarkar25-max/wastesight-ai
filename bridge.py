"""
WasteSight AI Pro — Cloud-to-Serial IoT Hardware Bridge
Listens to real-time waste classification events from Streamlit Cloud via ntfy.sh
and actuates the physical Arduino Uno smart bin lid and indicator LEDs over USB Serial.
"""

import serial
import serial.tools.list_ports
import requests
import json
import time

BAUD = 9600
TOPIC_URL = "https://ntfy.sh/wastesight_uno_anjarkar/json"

def find_arduino():
    """Automatically scans USB ports to locate the connected Arduino Uno."""
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        desc = (p.description or "").lower()
        if any(k in desc for k in ["arduino", "ch340", "usb serial", "usb-serial"]):
            return p.device
    return ports[0].device if ports else None

def main():
    port = find_arduino()
    if not port:
        print("⚠️ No Arduino found on any USB port! Plug in your Arduino Uno and run 'python bridge.py' again.")
        return

    try:
        ser = serial.Serial(port, BAUD, timeout=1)
        time.sleep(2)  # Wait for Arduino bootloader reset
        print(f"✅ Connected to Arduino Uno on {port}!")
        print(f"📡 Listening for live WasteSight cloud scans on {TOPIC_URL}...")
        print("Press Ctrl + C to stop.\n")

        while True:
            try:
                with requests.get(TOPIC_URL, stream=True, timeout=90) as response:
                    for line in response.iter_lines():
                        if line:
                            data = json.loads(line.decode("utf-8"))
                            if data.get("event") == "message":
                                cmd = data.get("message", "").strip().upper()
                                if cmd in ["B", "G", "E", "R"]:
                                    ser.write(cmd.encode("utf-8"))
                                    print(f"⚡ Cloud Scan Received -> Sent '{cmd}' to Arduino Uno!")
            except requests.exceptions.RequestException:
                # Reconnect silently on normal stream timeout
                time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping hardware bridge...")
    except Exception as e:
        print(f"❌ Error connecting to {port}: {e}")
    finally:
        if "ser" in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    main()
