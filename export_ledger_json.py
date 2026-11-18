import sqlite3
import json
import os

DB_PATH = "castleberry_ledger.db"
OUTPUT_PATH = "castleberry_ledger_report.json"

def export_ledger():
    if not os.path.exists(DB_PATH):
        print(f"[-] Database {DB_PATH} not found in current directory.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Dynamically find all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"[*] Found tables: {tables}")
    
    export_data = {}
    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        rows = [dict(row) for row in cursor.fetchall()]
        export_data[table] = rows
        
    conn.close()
    
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2)
        
    print(f"[+] Successfully exported ledger records to {OUTPUT_PATH}")

if __name__ == "__main__":
    export_ledger()
