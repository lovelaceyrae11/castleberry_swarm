#!/usr/bin/env python3
"""
Castleberry Bloom Swarm: Full-Payload Outcome Reader (Channel 5281)
"""

import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5281

def read_telemetry():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    
    print(f"==================================================")
    print(f"  CML Full-Payload Reader Active on Port {UDP_PORT}")
    print(f"  Waiting for deep cosmic packet payload...")
    print(f"==================================================\n")
    
    try:
        while True:
            data, addr = sock.recvfrom(65535)
            packet = json.loads(data.decode('utf-8'))
            
            print(f"[{packet.get('timestamp', 'N/A')}] ✦ Subject: {packet.get('subject')}")
            print(f"Axiom: {packet.get('axiom')} | Base Resonance: {packet.get('base_resonance')}\n")
            
            for node_name, details in packet.get("swarm_nodes", {}).items():
                print(f"🔹 [{node_name}]")
                print(f"   Layer: {details.get('layer')} (@ {details.get('frequency')})")
                
                # Unpack the deep data payload dictionary
                data_dict = details.get('data', {})
                for k, v in data_dict.items():
                    print(f"     • {k.replace('_', ' ').title()}: {v}")
                print()
            print("="*65 + "\n")
            
    except KeyboardInterrupt:
        print("\n[!] Reader halted.")
    finally:
        sock.close()

if __name__ == "__main__":
    read_telemetry()
