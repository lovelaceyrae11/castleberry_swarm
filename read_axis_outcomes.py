#!/usr/init/env python3
"""
Castleberry Bloom Swarm: Taurus-Scorpio Axis Outcome Reader
Description: Listens on UDP port 5281, parses incoming axis packets, 
             and displays phi-scaled harmonic metrics in real time.
"""

import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5281

def read_axis_telemetry():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    
    print(f"==================================================")
    print(f"  Taurus-Scorpio Axis Reader Active on Port {UDP_PORT}")
    print(f"  Listening for harmonic grounding telemetry...")
    print(f"==================================================\n")
    
    try:
        while True:
            data, addr = sock.recvfrom(65535)
            packet = json.loads(data.decode('utf-8'))
            
            # Filter specifically for axis packets
            if "axis_metrics" in packet:
                print(f"[{packet.get('timestamp', 'N/A')}] ✦ Subject: {packet.get('subject')}")
                print(f"Axiom: {packet.get('axiom')} | Active Node: {packet.get('active_node')}")
                print(f"  --- Harmonic Axis Metrics ---")
                
                for key, val in packet.get("axis_metrics", {}).items():
                    print(f"    • {key.replace('_', ' ').title()}: {val}")
                print(f"--------------------------------------------------\n")
                
    except KeyboardInterrupt:
        print("\n[!] Axis reader halted by operator.")
    finally:
        sock.close()

if __name__ == "__main__":
    read_axis_telemetry()
