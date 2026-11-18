import sqlite3

DB_NAME = "castleberry_ledger.db"

def inspect():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, tensor_sum, frequency, audit_status FROM telemetry ORDER BY timestamp DESC LIMIT 5")
        rows = cursor.fetchall()
        print("=== CASTLEBERRY LEDGER TELEMETRY ===")
        for row in rows:
            print(f"Time: {row[0]} | Tensor Sum: {row[1]:.4f} | Freq: {row[2]}Hz | Status: {row[3]}")
        conn.close()
    except Exception as e:
        print(f"Error reading ledger: {e}")

if __name__ == "__main__":
    inspect()
