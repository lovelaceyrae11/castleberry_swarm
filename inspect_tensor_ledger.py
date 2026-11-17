import sqlite3
import os

def query_tensor_history():
    ledger_path = "castleberry_ledger.db"
    if not os.path.exists(ledger_path):
        print(f">>> Error: Ledger '{ledger_path}' not found in current directory.")
        return

    print(f">>> Connecting to SQLite Ledger: {ledger_path}")
    conn = sqlite3.connect(ledger_path)
    cursor = conn.cursor()
    
    # Query all records from record_tensors ordered newest first
    try:
        cursor.execute("SELECT id, timestamp, dimensions, norm, status FROM record_tensors ORDER BY id DESC;")
        rows = cursor.fetchall()
        
        print("\n" + "=" * 85)
        print(f"{'ID':<4} | {'Timestamp':<26} | {'Dimensions':<10} | {'L2 Norm':<10} | {'Status'}")
        print("=" * 85)
        
        for row in rows:
            record_id, timestamp, dims, norm_val, status = row
            print(f"{record_id:<4} | {timestamp:<26} | {dims:<10} | {norm_val:<10.6f} | {status}")
            
        print("=" * 85)
        print(f">>> Total Recorded Tensor States: {len(rows)}")
        
    except Exception as e:
        print(f">>> Query Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    query_tensor_history()
