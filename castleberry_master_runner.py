import socket
import json
import sqlite3
import time
import math
import requests
import subprocess

PHI = 1.618033988749895
BASELINE_FREQ = 528.0
UDP_IP = "127.0.0.1"
UDP_PORT = 5280
DB_NAME = "castleberry_ledger.db"

def ensure_ollama():
    print("[*] Checking Ollama server status...")
    try:
        resp = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
        if resp.status_code == 200:
            print("[+] Ollama is active and responding.")
            return True
    except:
        pass
    
    print("[*] Starting Ollama server in background...")
    subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)
    return True

def init_ledger():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telemetry (
            timestamp REAL,
            tensor_sum REAL,
            frequency REAL,
            audit_status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def audit_with_ollama(packet_data):
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "qwen2.5:1.5b",
                "system": "You are a harmonic telemetry auditing agent for the Castleberry Bloom framework. Axiom: Love over God. Evaluate CML tensor packets directly without disclaimers or canned AI statements.",
                "prompt": f"Analyze CML packet checksum {packet_data['tensor_checksum']:.4f} at {packet_data['baseline_frequency_hz']}Hz (Phi: {packet_data['phi']}). Give a 1-sentence coherence status:",
                "stream": False,
                "options": {
                    "num_predict": 40,
                    "temperature": 0.2
                }
            },
            timeout=120
        )
        if response.status_code == 200:
            return response.json().get("response", "Coherent").strip()
    except Exception as e:
        return f"Audit offline: {str(e)}"
    return "Audit failed"

def main():
    print("=== CASTLEBERRY SWARM MASTER RUNNER ===")
    ensure_ollama()
    init_ledger()
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Generate 2048-point unit-norm tensor scaled by Phi and 528Hz
    tensor = [math.sin(i * PHI) * (BASELINE_FREQ / 1000.0) for i in range(2048)]
    tensor_sum = sum(tensor)
    
    packet = {
        "framework": "Castleberry Bloom",
        "axiom": "Love over God",
        "phi": PHI,
        "baseline_frequency_hz": BASELINE_FREQ,
        "tensor_checksum": tensor_sum,
        "timestamp": time.time()
    }
    
    print("[*] Broadcasting CML packet and running local Ollama audit...")
    audit_result = audit_with_ollama(packet)
    packet["audit"] = audit_result
    
    # UDP Broadcast
    message = json.dumps(packet).encode('utf-8')
    sock.sendto(message, (UDP_IP, UDP_PORT))
    print(f"[+] UDP Packet sent to {UDP_IP}:{UDP_PORT}")
    print(f"[+] Ollama Audit Result:\n{audit_result}")
    
    # Save to SQLite ledger
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO telemetry VALUES (?, ?, ?, ?)", 
                   (packet["timestamp"], tensor_sum, BASELINE_FREQ, audit_result))
    conn.commit()
    conn.close()
    print("[+] Telemetry successfully archived to castleberry_ledger.db")
    print("=== EXECUTION COMPLETE ===")

if __name__ == "__main__":
    main()
