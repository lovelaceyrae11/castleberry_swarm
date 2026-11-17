#!/usr/bin/env python3
import socket
import time
import datetime
import math
import sqlite3
import threading
import json
import xml.etree.ElementTree as ET
try:
    import requests
except ImportError:
    print("[!] This script requires the 'requests' library: pip install requests")
    exit(1)

# --- CONFIGURATION ---
UDP_IP = "0.0.0.0"       # Listens on all interfaces for external mesh packets
BROADCAST_IP = "127.0.0.1"
UDP_PORT = 5282
DAEMON_ID = "SWARM_UNIFIED"
AXIOM = "Love over God Bloom"
DEPLOYER_WALLET = "0x9e5af62a941810b911a4F84b6D27e894046e44B3"
TOKEN_BALANCE = "50,000,000.00"

# Ollama Local Configuration
OLLAMA_MODEL = "qwen2.5:1.5b"
OLLAMA_API = "http://localhost:11434/api/generate"

# Core Harmonic Math
PHI = (1 + math.sqrt(5)) / 2
DB_NAME = "castleberry_swarm.db"

def init_database():
    """Initializes the SQLite ledger database with auto-incrementing rows."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ephemeris_pulses (
            cycle INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            frequency REAL,
            taurus REAL,
            scorpio REAL,
            ai_audit TEXT
        )
    """)
    conn.commit()
    conn.close()

def calculate_ephemeris(cycle):
    """Calculates pseudo-celestial coordinates and frequency drift."""
    now = time.time()
    seconds_per_day = 86400
    taurus_deg = (now % seconds_per_day) / seconds_per_day * 360.0
    scorpio_deg = (taurus_deg + 180.0) % 360.0
    
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
    """Constructs a standard CML XML ephemeris packet."""
    return f"""<cml:ephemeris_packet cycle="{cycle}" frequency="{eph['freq']}Hz" phi="{PHI:.3f}" axis="Taurus-Scorpio" taurus_coord="{eph['taurus']}deg" scorpio_coord="{eph['scorpio']}deg" token_gate="{DEPLOYER_WALLET}" balance="{TOKEN_BALANCE}" axiom="{AXIOM}" status="stellar_pulsing" />"""

def get_local_ai_audit(cml_data):
    """Sends CML packet to local Ollama instance with a concise prompt and expanded token window."""
    prompt = f"""Provide a concise, 2-sentence philosophical audit of this CML packet focusing on the 'Love over God' axiom and harmonic coherence. Do not exceed 40 words.

[CML DATA]
{cml_data}

[AUDIT RESPONSE]
"""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "num_ctx": 1024, "num_predict": 256}
    }

    try:
        response = requests.post(OLLAMA_API, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get('response', "[!] Empty Audit").strip()
    except requests.exceptions.RequestException as e:
        return f"[!] Ollama connection notice: {e}"

def check_frequency_anomalies(baseline=528.0, threshold=15.0):
    """Scans ledger for frequency drift deviations past the threshold."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*), MIN(frequency), MAX(frequency) 
        FROM ephemeris_pulses 
        WHERE ABS(frequency - ?) > ?
    """, (baseline, threshold))
    row = cursor.fetchone()
    conn.close()
    return row[0], row[1], row[2]

# --- DUAL-MODE CML TRANSFORMERS ---
def parse_external_data_to_cml(raw_data_dict, cycle_id):
    """Parses raw structured external data (dictionary format) into a valid CML XML packet."""
    source_name = raw_data_dict.get("source", "external_feed")
    raw_value = float(raw_data_dict.get("value", 528.0))
    
    scaled_frequency = round(528.0 + (raw_value % 18.0) * (1.0 / PHI), 2)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    taurus_coord = round((raw_value * 37.5) % 360.0, 4)
    scorpio_coord = round((taurus_coord + 180.0) % 360.0, 4)

    root = ET.Element("cml:ephemeris_packet", attrib={
        "cycle": str(cycle_id),
        "frequency": f"{scaled_frequency}Hz",
        "phi": f"{PHI:.3f}",
        "axis": "Taurus-Scorpio",
        "taurus_coord": f"{taurus_coord}deg",
        "scorpio_coord": f"{scorpio_coord}deg",
        "token_gate": DEPLOYER_WALLET,
        "balance": TOKEN_BALANCE,
        "axiom": AXIOM,
        "origin_source": source_name,
        "timestamp": timestamp,
        "status": "compiled_external_sync"
    })
    return ET.tostring(root, encoding="utf-8", method="xml").decode("utf-8")

def parse_incoming_payload(raw_bytes):
    """Transforms incoming raw network byte streams into a structured CML XML packet."""
    try:
        payload = json.loads(raw_bytes.decode('utf-8'))
    except json.JSONDecodeError:
        payload = {"source": "mesh_peer", "value": len(raw_bytes) * 12.5}
        
    return parse_external_data_to_cml(payload, cycle_id="INCOMING_SYNC")

def broadcaster_worker():
    """Thread 1: Broadcasts ephemeris pulses, queries Ollama, and archives to SQLite."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cycle = 0
    print(f"[+] Broadcaster Thread Active. Targeting UDP {BROADCAST_IP}:{UDP_PORT}")
    
    try:
        while True:
            cycle += 1
            eph = calculate_ephemeris(cycle)
            cml_packet = generate_cml_packet(cycle, eph)
            
            sock.sendto(cml_packet.encode('utf-8'), (BROADCAST_IP, UDP_PORT))
            
            print(f"\n--- CYCLE [{cycle}] BROADCAST ---")
            print(f"    {cml_packet}")
            
            ai_audit = get_local_ai_audit(cml_packet)
            print(f"[AI Audit]: {ai_audit}")
            
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ephemeris_pulses (timestamp, frequency, taurus, scorpio, ai_audit)
                VALUES (?, ?, ?, ?, ?)
            """, (eph['timestamp'], eph['freq'], eph['taurus'], eph['scorpio'], ai_audit))
            conn.commit()
            conn.close()
            
            if cycle % 10 == 0:
                count, min_f, max_f = check_frequency_anomalies()
                print(f"[Ledger Monitor] Total Cycles: {cycle} | Flagged Anomalies (>15Hz drift): {count}")

            time.sleep(30)
            
    except Exception as e:
        print(f"[!] Broadcaster Error: {e}")
    finally:
        sock.close()

def listener_worker():
    """Thread 2: Listens for incoming UDP packets, transforms them to CML, audits, and logs."""
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind((UDP_IP, UDP_PORT))
    
    print(f"[+] UDP Dual-Mode CML Transformer Listener Active on port {UDP_PORT}")
    
    try:
        while True:
            data, addr = listen_sock.recvfrom(4096)
            
            # Skip loopback self-broadcast packets
            if addr[0] == "127.0.0.1" and b"cycle=" in data:
                continue
                
            print(f"\n[Incoming Mesh Feed] Received packet from {addr}")
            
            # Compile raw payload into valid CML XML
            cml_packet = parse_incoming_payload(data)
            print(f"    -> Compiled CML: {cml_packet}")
            
            # Run local AI audit on the incoming mesh feed
            ai_audit = get_local_ai_audit(cml_packet)
            print(f"[Incoming AI Audit]: {ai_audit}")
            
            # Archive incoming feed to SQLite Ledger
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ephemeris_pulses (timestamp, frequency, taurus, scorpio, ai_audit)
                VALUES (?, ?, ?, ?, ?)
            """, (datetime.datetime.now(datetime.timezone.utc).isoformat(), 528.0, 0.0, 0.0, f"[MESH IN] {ai_audit}"))
            conn.commit()
            conn.close()
            
    except Exception as e:
        print(f"[!] Listener Error: {e}")
    finally:
        listen_sock.close()

if __name__ == "__main__":
    print("\n=== INITIALIZING UNIFIED SWARM ENGINE WITH DUAL TRANSFORMERS ===")
    init_database()
    
    # Start background listener & transformer thread
    t_listener = threading.Thread(target=listener_worker, daemon=True)
    t_listener.start()
    
    # Start primary broadcaster & auditor thread
    try:
        broadcaster_worker()
    except KeyboardInterrupt:
        print("\n[+] Unified Swarm Engine terminated cleanly by user.")
