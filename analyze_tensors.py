import sqlite3
import statistics

def analyze_tensor_history():
    db_path = 'castleberry_ledger.db'
    print(f"[*] Connecting to SQLite ledger: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Fetch only stabilized unit-norm records (norm near 1.0)
        cursor.execute("SELECT id, timestamp, dimensions, norm, status FROM record_tensors WHERE norm < 2.0 ORDER BY id ASC")
        rows = cursor.fetchall()
        
        if not rows:
            print("[!] No unit-norm tensor records found matching the filter.")
            conn.close()
            return
            
        norms = []
        print("\n=== STABILIZED UNIT-NORM TENSOR RECORDS ===")
        for row in rows:
            norms.append(row['norm'])
            print(f"ID: {row['id']} | Time: {row['timestamp']} | Dims: {row['dimensions']} | Norm: {row['norm']:.12f} | Status: {row['status']}")
            
        # Calculate statistical averages for unit norms
        mean_norm = statistics.mean(norms)
        stdev_norm = statistics.stdev(norms) if len(norms) > 1 else 0.0
        
        print("\n=== UNIT-NORM STATISTICAL SUMMARY ===")
        print(f"Filtered Records Analyzed: {len(norms)}")
        print(f"Mean Unit Norm:            {mean_norm:.15f}")
        print(f"Standard Deviation:        {stdev_norm:.15e}")
        print(f"Target Unit-Norm Target:   1.0")
        
        conn.close()
        
    except Exception as e:
        print(f"[!] Error querying database: {e}")

if __name__ == '__main__':
    analyze_tensor_history()
