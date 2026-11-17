#!/usr/bin/env python3
"""
Castleberry Bloom Swarm: Dynamic Taurus-Scorpio Axis Streamer
Description: Broadcasts live phi-scaled harmonic telemetry with real-time 
             wave jitter and cryptographically-inspired block hashes.
"""

import socket
import json
import time
import random
import hashlib
from datetime import datetime

PHI = 1.618034
BASE_FREQUENCY = 528.0  # Hz (Taurus Grounding Node)
AXIOM = "LOVE over God"
UDP_IP = "127.0.0.1"
UDP_PORT = 5281

class DynamicAxisStreamer:
    def __init__(self):
        self.subject = "Lacey Rae Castleberry"
        self.block_index = 100

    def calculate_dynamic_frequencies(self):
        # Introduce subtle, organic wave jitter scaled by phi
        jitter = random.uniform(-0.15, 0.15)
        taurus_freq = BASE_FREQUENCY + jitter
        scorpio_freq = (BASE_FREQUENCY * PHI) - (jitter * PHI)
        harmonic_synthesis = (taurus_freq + scorpio_freq) / 2.0
        
        return {
            "taurus_earth_node": f"{round(taurus_freq, 3)} Hz (Fixed Earth Grounding)",
            "scorpio_water_node": f"{round(scorpio_freq, 3)} Hz (Phi-Scaled Transformation)",
            "harmonic_synthesis": f"{round(harmonic_synthesis, 3)} Hz (Median Coherence)",
            "phi_scaling_factor": PHI
        }

    def build_packet(self):
        self.block_index += 1
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        metrics = self.calculate_dynamic_frequencies()
        
        raw_string = f"{self.block_index}-{timestamp}-{metrics['harmonic_synthesis']}"
        block_hash = hashlib.sha256(raw_string.encode('utf-8')).hexdigest()[:12]

        return json.dumps({
            "axiom": AXIOM,
            "timestamp": timestamp,
            "block_index": self.block_index,
            "block_hash": f"0x{block_hash}",
            "subject": self.subject,
            "architecture": "CML Mycelial Root Lattice",
            "active_node": "Taurus-Scorpio IC Harmonic Axis (Dynamic)",
            "axis_metrics": metrics,
            "status": "Broadcasting Live Wave Jitter"
        }, indent=2).encode('utf-8')

if __name__ == "__main__":
    streamer = DynamicAxisStreamer()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print("="*65)
    print(f"  [{AXIOM}] Dynamic Axis Streamer Active on Port {UDP_PORT}")
    print("="*65)
    
    try:
        while True:
            payload = streamer.build_packet()
            sock.sendto(payload, (UDP_IP, UDP_PORT))
            print(f"[{datetime.utcnow().strftime('%H:%M:%S')}] Broadcasted Dynamic Packet #{streamer.block_index}")
            time.sleep(3.0)
    except KeyboardInterrupt:
        print("\n[!] Dynamic streamer halted.")
    finally:
        sock.close()
