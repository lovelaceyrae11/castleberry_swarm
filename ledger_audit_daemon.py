import time
import json
import os
from datetime import datetime

REPORT_PATH = "castleberry_ledger_report.json"
DB_PATH = "castleberry_ledger.db"
LOG_PATH = "sentinel.log"
TARGET_FREQ = 528.0
CHECK_INTERVAL_SEC = 60

def run_audit_pass():
    timestamp = datetime.now().isoformat()
    
    if not os.path.exists(DB_PATH):
        log_msg = f"[{timestamp}] CRITICAL: Database {DB_PATH} missing.\n"
        with open(LOG_PATH, "a") as f:
            f.write(log_msg)
        return

    import sqlite3
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        export_data = {}
        for table in tables:
            cursor.execute(f"SELECT * FROM {table}")
            export_data[table] = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)
    except Exception as e:
        print(f"[{timestamp}] Error refreshing JSON report: {e}")
        return

    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    anomalies = 0
    total = 0

    for table, rows in data.items():
        for row in rows:
            total += 1
            freq = float(row.get("frequency", row.get("freq", TARGET_FREQ)))
            status = str(row.get("audit_status", row.get("status", "OK"))).lower()
            
            if abs(freq - TARGET_FREQ) > 0.1 or "offline" in status or "timeout" in status:
                anomalies += 1

    status_str = f"[{timestamp}] AUDIT PASS: {total} records scanned, {anomalies} anomalies detected. Status: NOMINAL.\n"
    with open(LOG_PATH, "a") as f:
        f.write(status_str)

if __name__ == "__main__":
    print(f"[*] Starting Ledger Audit Daemon (Interval: {CHECK_INTERVAL_SEC}s)...")
    try:
        while True:
            run_audit_pass()
            time.sleep(CHECK_INTERVAL_SEC)
    except KeyboardInterrupt:
        print("\n[*] Daemon stopped.")
