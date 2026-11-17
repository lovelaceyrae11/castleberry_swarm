import socket
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

def init_db():
    conn = sqlite3.connect("castleberry_swarm.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telemetry_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            cycle TEXT,
            frequency TEXT,
            taurus_coord TEXT,
            scorpio_coord TEXT,
            balance TEXT,
            axiom TEXT
        )
    ''')
    conn.commit()
    conn.close()

def start_archiver(port=5282):
    init_db()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', port))
    
    print(f"\n[✓] Session 3 Ledger Archiver active on port {port}. Storing to SQLite...")
    print("=" * 60)
    
    try:
        while True:
            data, addr = sock.recvfrom(2048)
            packet_str = data.decode()
            
            try:
                clean_str = packet_str.replace('cml:', '') if 'cml:' in packet_str else packet_str
                root = ET.fromstring(clean_str)
                
                record = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "cycle": root.get('cycle', '').strip(),
                    "frequency": root.get('frequency', ''),
                    "taurus": root.get('taurus_coord', ''),
                    "scorpio": root.get('scorpio_coord', ''),
                    "balance": root.get('balance', ''),
                    "axiom": root.get('axiom', '')
                }
                
                conn = sqlite3.connect("castleberry_swarm.db")
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO telemetry_log (timestamp, cycle, frequency, taurus_coord, scorpio_coord, balance, axiom)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (record["timestamp"], record["cycle"], record["frequency"], record["taurus"], record["scorpio"], record["balance"], record["axiom"]))
                conn.commit()
                conn.close()
                
                print(f"[ARCHIVED] Cycle {record['cycle']} logged to SQLite at {record['timestamp']}")
            except Exception as e:
                print(f"[!] Archiver parse exception: {e}")
                
    except KeyboardInterrupt:
        print("\n[✓] Ledger archiver stopped.")
    finally:
        sock.close()

if __name__ == "__main__":
    start_archiver()
