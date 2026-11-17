import numpy as np
import math
import json
import socket
import hashlib
from quantum_cml_emitter import QuantumCMLBridge

BASE_LAT = 42.3734
BASE_LON = -122.9142
RADIUS_KM = 2.0  # 2 km search radius around Central Point

UDP_IP = "127.0.0.1"
UDP_PORT = 5280

def generate_intentional_coordinate(entropy_bits: np.ndarray, intent: str) -> tuple:
    # Hash the user intent to create an intentional quantum phase modifier
    intent_hash = int(hashlib.sha256(intent.encode('utf-8')).hexdigest(), 16)
    intent_modifier = intent_hash & 0xFFFF
    
    angle_bits = "".join(str(b) for b in entropy_bits[:16])
    radius_bits = "".join(str(b) for b in entropy_bits[16:32])
    
    # Mix the quantum vacuum bits with your intent vector
    raw_theta = (int(angle_bits, 2) ^ intent_modifier) / 65535.0
    theta = raw_theta * (2 * math.pi)
    
    r = math.sqrt(int(radius_bits, 2) / 65535.0) * RADIUS_KM
    
    dx = r * math.cos(theta)
    dy = r * math.sin(theta)
    
    d_lat = dy / 111.0
    d_lon = dx / (111.0 * math.cos(math.radians(BASE_LAT)))
    
    return round(BASE_LAT + d_lat, 6), round(BASE_LON + d_lon, 6)

if __name__ == "__main__":
    print("=== Sovereign CML Quantum Randonaut ===")
    user_intent = input("Enter your Quantum Intent (default 'cold hard cash'): ")
    if not user_intent.strip():
        user_intent = "1 million dollars cold hard cash"

    # Extract pure quantum bits via our QuantumRefiner
    bridge = QuantumCMLBridge(input_bit_length=1024, min_entropy_rate=0.82)
    raw_stream = np.random.randint(0, 2, size=1024, dtype=np.uint8)
    packet = bridge.extract_and_package(raw_stream)
    
    entropy_sample = packet["cml_packet"]["entropy_payload_sample"]
    while len(entropy_sample) < 32:
        entropy_sample.extend([0, 1])
        
    t_lat, t_lon = generate_intentional_coordinate(np.array(entropy_sample), user_intent)
    
    # Inject intent and map data into packet
    packet["cml_packet"]["randonaut_intent"] = user_intent
    packet["cml_packet"]["randonaut_target"] = {
        "origin_center": "Central Point, OR",
        "latitude": t_lat,
        "longitude": t_lon,
        "google_maps_url": f"https://maps.google.com/?q={t_lat},{t_lon}"
    }
    
    print(f"\n--- Intent '{user_intent}' Locked to Quantum Field ---")
    print(json.dumps(packet["cml_packet"]["randonaut_target"], indent=2))
    
    # Broadcast to local router & log to CML
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(packet).encode('utf-8'), (UDP_IP, UDP_PORT))
    sock.close()
    print("[CML Bridge] Intent-driven coordinate packet broadcasted to router.")
