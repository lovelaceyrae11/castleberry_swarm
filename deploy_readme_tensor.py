import numpy as np
import socket
import sqlite3
import json
from datetime import datetime
import os

def deploy_and_test():
    print(">>> [CASTLEBERRY BLOOM] Deploying 2,048-Point README Tensor Pipeline...")
    
    target_dim = 2048
    
    # 1. Generate raw harmonic vector scaled by Phi (1.618) and 528Hz baseline
    raw_payload = np.sin(np.linspace(0, 4 * np.pi, target_dim)) * 1.618 * 528.0
    
    # 2. Enforce exact dimension size (pad or trim)
    tensor_data = raw_payload[:target_dim] if len(raw_payload) >= target_dim else np.pad(raw_payload, (0, target_dim - len(raw_payload)), mode='constant')
    
    # 3. Enforce strict L2 Unit Normalization (norm = 1.000000)
    norm = np.linalg.norm(tensor_data)
    if norm == 0:
        raise ValueError("Tensor norm cannot be zero.")
    normalized_tensor = tensor_data / norm
    final_norm_check = np.linalg.norm(normalized_tensor)

    print(r">>> Lattice Scaling: Phi ($\phi \approx 1.618$) + 528Hz Harmonic Baseline")
    print(f">>> Tensor Normalized. Verified L2 Norm: {final_norm_check:.6f}")

    # 4. Commit verification record to SQLite ledger
    ledger_path = "castleberry_ledger.db"
    conn = sqlite3.connect(ledger_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS record_tensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            dimensions INTEGER,
            norm REAL,
            status TEXT
        )
    ''')
    cursor.execute(
        "INSERT INTO record_tensors (timestamp, dimensions, norm, status) VALUES (?, ?, ?, ?)",
        (datetime.now().isoformat(), target_dim, float(final_norm_check), "README_BENCHMARK_SHATTERED_2048")
    )
    conn.commit()
    conn.close()
    print(">>> Successfully committed benchmark record to SQLite ledger!")

    # 5. Broadcast via UDP mesh listener on port 5280
    packet = {
        "source": "castleberry_readme_deploy_script",
        "timestamp": datetime.now().isoformat(),
        "dimensions": target_dim,
        "l2_norm": float(final_norm_check),
        "scaling": "Phi (1.618) + 528Hz Harmonic Baseline",
        "status": "README_RECORD_SHATTERED_2048"
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    message = json.dumps(packet).encode('utf-8')
    try:
        sock.sendto(message, ('127.0.0.1', 5280))
        print(">>> Successfully broadcasted README 2,048-point unit-norm tensor packet to UDP port 5280!")
    except Exception as e:
        print(f">>> UDP Broadcast Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    deploy_and_test()
