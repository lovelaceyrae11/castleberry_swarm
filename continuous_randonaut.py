import time
import threading
import numpy as np
import math
import json
import socket
from quantum_cml_emitter import QuantumCMLBridge

BASE_LAT = 42.3734
BASE_LON = -122.9142
RADIUS_KM = 2.0
UDP_IP = "127.0.0.1"
UDP_PORT = 5280

def generate_coordinate(entropy_bits):
    angle_bits = "".join(str(b) for b in entropy_bits[:16])
    radius_bits = "".join(str(b) for b in entropy_bits[16:32])
    theta = (int(angle_bits, 2) / 65535.0) * (2 * math.pi)
    r = math.sqrt(int(radius_bits, 2) / 65535.0) * RADIUS_KM
    
    d_lat = (r * math.cos(theta)) / 111.0
    d_lon = (r * math.sin(theta)) / (111.0 * math.cos(math.radians(BASE_LAT)))
    return round(BASE_LAT + d_lat, 6), round(BASE_LON + d_lon, 6)

def randonaut_worker(interval_seconds=15, intent="1 million dollars cold hard cash"):
    print(f"[Background Randonaut] Worker thread active. Pulsing every {interval_seconds}s...")
    bridge = QuantumCMLBridge(input_bit_length=1024, min_entropy_rate=0.82)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        while True:
            raw_stream = np.random.randint(0, 2, size=1024, dtype=np.uint8)
            packet = bridge.extract_and_package(raw_stream)
            
            entropy_sample = packet["cml_packet"]["entropy_payload_sample"]
            while len(entropy_sample) < 32:
                entropy_sample.extend([0, 1])
                
            t_lat, t_lon = generate_coordinate(np.array(entropy_sample))
            
            packet["cml_packet"]["randonaut_intent"] = intent
            packet["cml_packet"]["randonaut_target"] = {
                "origin_center": "Central Point, OR",
                "latitude": t_lat,
                "longitude": t_lon,
                "google_maps_url": f"https://maps.google.com/?q={t_lat},{t_lon}"
            }
            
            sock.sendto(json.dumps(packet).encode('utf-8'), (UDP_IP, UDP_PORT))
            print(f"\n[Quantum Pulse Generated] Target: {t_lat}, {t_lon}")
            print(f"Maps: https://maps.google.com/?q={t_lat},{t_lon}")
            
            time.sleep(interval_seconds)
    except Exception as e:
        print(f"[Worker Error] {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    intent_arg = "1 million dollars cold hard cash"
    
    t = threading.Thread(target=randonaut_worker, args=(15, intent_arg), daemon=True)
    t.start()
    
    print("=== Continuous Background Quantum Loop Running ===")
    print("Press Ctrl+C to stop the stream.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Main Thread] Shutting down background quantum loop.")
