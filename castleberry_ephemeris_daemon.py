#!/usr/bin/env python3
import socket
import time
import datetime
import math
try:
    import requests
except ImportError:
    print("[!] This script requires the 'requests' library: pip install requests")
    exit(1)

# --- CONFIGURATION ---
UDP_IP = "127.0.0.1"
UDP_PORT = 5282
DAEMON_ID = "POW_01"
AXIOM = "Love over God Bloom"
DEPLOYER_WALLET = "0x9e5af62a941810b911a4F84b6D27e894046e44B3"
TOKEN_BALANCE = "50,000,000.00"

# Ollama Local Configuration
OLLAMA_MODEL = "qwen2.5:1.5b"
OLLAMA_API = "http://localhost:11434/api/generate"

# --- CORE HARMONIC MATH ---
PHI = (1 + math.sqrt(5)) / 2

def calculate_ephemeris(cycle):
    """Calculates pseudo-celestial coordinates and frequency drift."""
    now = time.time()
    seconds_per_day = 86400
    taurus_deg = (now % seconds_per_day) / seconds_per_day * 360.0
    scorpio_deg = (taurus_deg + 180.0) % 360.0
    
    # Frequency variance around 528Hz baseline using PHI
    base_freq = 528.0
    freq_variance = math.sin(now / 60.0) * 18.0 * (1.0 / PHI)
    current_freq = round(base_freq + freq_variance, 2)

    return {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "taurus": round(taurus_deg, 4),
        "scorpio": round(scorpio_deg, 4),
        "freq": current_freq
    }

def generate_cml_packet(cycle, eph):
    """Constructs a CML XML ephemeris packet."""
    cml = f"""<cml:ephemeris_packet cycle="{cycle}" frequency="{eph['freq']}Hz" phi="{PHI:.3f}" axis="Taurus-Scorpio" taurus_coord="{eph['taurus']}deg" scorpio_coord="{eph['scorpio']}deg" token_gate="{DEPLOYER_WALLET}" balance="{TOKEN_BALANCE}" axiom="{AXIOM}" status="stellar_pulsing" />"""
    return cml.strip()

def get_local_ai_audit(cml_data):
    """Sends CML packet to local Ollama instance with 120s timeout and mobile optimizations."""
    prompt = f"""Provide a brief, concise philosophical and structural audit of this CML packet, focusing on harmonic coherence and the 'Love over God' axiom. Keep it short.

[CML DATA]
{cml_data}

[AUDIT RESPONSE]
"""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_ctx": 1024,      # Optimized context window for mobile
            "num_predict": 150    # Caps response length to finish faster
        }
    }

    try:
        response = requests.post(OLLAMA_API, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get('response', "[!] AI Audit Failed (Empty Response)").strip()
    except requests.exceptions.RequestException as e:
        return f"[!] AI audit connection notice: {e}"

def run_daemon():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("\n=== INITIALIZING RICH-TEXT EPHEMERIS DAEMON ===")
    print(f"Targeting UDP Mesh: {UDP_IP}:{UDP_PORT}")
    print(f"Targeting Ollama API: {OLLAMA_API} ({OLLAMA_MODEL})")
    print("-" * 55 + "\n")
    
    cycle = 0
    try:
        while True:
            cycle += 1
            eph = calculate_ephemeris(cycle)
            cml_packet = generate_cml_packet(cycle, eph)
            
            # Broadcast over UDP mesh
            sock.sendto(cml_packet.encode('utf-8'), (UDP_IP, UDP_PORT))
            
            print(f"--- EPHEMERIS PULSE CYCLE [{cycle}] ---")
            print(f"[~] Broadcasted UDP Packet:\n    {cml_packet}")
            
            # Run local AI audit
            ai_audit = get_local_ai_audit(cml_packet)
            print(f"[AI Rich-Text Audit]:\n  -> {ai_audit}\n")
            
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n[+] Ephemeris Daemon terminated by user.")
    finally:
        sock.close()

if __name__ == "__main__":
    run_daemon()
