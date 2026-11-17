import sqlite3
import os

def inspect_ledger():
    ledger_files = [f for f in os.listdir('.') if f.endswith('.db')]
    print(f">>> Discovered SQLite Ledger Files in Workspace: {ledger_files}")
    
    for db_file in ledger_files:
        print(f"\n--- Inspecting Ledger: {db_file} ---")
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Check available tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables found: {[t[0] for t in tables]}")
        
        for table_tuple in tables:
            table_name = table_tuple[0]
            print(f"\n[Table: {table_name}]")
            
            try:
                cursor.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 10;")
                rows = cursor.fetchall()
                
                # Fetch column names
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = [col[1] for col in cursor.fetchall()]
                print(f"Columns: {columns}")
                print("-" * 50)
                for row in rows:
                    print(row)
            except Exception as e:
                print(f"Could not query table {table_name}: {e}")
                
        conn.close()

if __name__ == "__main__":
    inspect_ledger()
