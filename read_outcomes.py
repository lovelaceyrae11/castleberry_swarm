#!/usr/bin/env python3
"""
Castleberry Bloom Swarm: Live Outcome Reader
Description: Listens on UDP port 5280, parses CML JSON packets, 
             and prints formatted swarm outcomes in real time.
"""

import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5280

def read_telemetry():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    
    print(f"==================================================")
    print(f"  CML Swarm Outcome Reader Active on Port {UDP_PORT}")
    print(f"  Listening for incoming cosmic telemetry...")
    print(f"==================================================\n")
    
    try:
        while True:
            data, addr = sock.recvfrom(65535)
            packet = json.loads(data.decode('utf-8'))
            
            print(f"[{packet.get('timestamp', 'N/A')}] Received Packet from {addr[0]}:{addr[1]}")
            print(f"  Axiom: {packet.get('axiom')} | Base Resonance: {packet.get('base_resonance')}")
            print(f"  Subject: {packet.get('subject')}")
            print(f"  --- Active Swarm Nodes ---")
            
            for node_name, details in packet.get("swarm_nodes", {}).items():
                print(f"    • {node_name} [{details.get('layer')}] @ {details.get('frequency')}")
            print(f"--------------------------------------------------\n")
            
    except KeyboardInterrupt:
        print("\n[!] Reader halted by operator.")
    finally:
        sock.close()

if __name__ == "__main__":
    read_telemetry()
