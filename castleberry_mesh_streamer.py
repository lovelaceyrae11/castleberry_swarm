import numpy as np
import socket
import sqlite3
import json
from datetime import datetime

def broadcast_tensor_packet():
    print(">>> [CASTLEBERRY BLOOM] Preparing 2,048-Point Tensor for UDP Mesh Broadcast...")
    
    target_dim = 2048
    
    # 1. Generate raw harmonic vector
    raw_payload = np.sin(np.linspace(0, 4 * np.pi, target_dim)) * 1.618 * 528.0
    
    # 2. Enforce dimension size
    tensor_data = raw_payload[:target_dim] if len(raw_payload) >= target_dim else np.pad(raw_payload, (0, target_dim - len(raw_payload)), mode='constant')
    
    # 3. Correct L2 Normalization (divide by vector's own norm to achieve unit length = 1.0)
    norm = np.linalg.norm(tensor_data)
    if norm == 0:
        raise ValueError("Tensor norm cannot be zero.")
    normalized_tensor = tensor_data / norm
    final_norm_check = np.linalg.norm(normalized_tensor)

    print(r">>> Lattice Scaling: Phi ($\phi \approx 1.618$) + 528Hz Harmonic Baseline")
    print(f">>> Tensor Normalized. Verified L2 Norm: {final_norm_check:.6f}")

    # Construct CML-compatible packet payload
    packet = {
        "source": "castleberry_pure_tensor_engine",
        "timestamp": datetime.now().isoformat(),
        "dimensions": target_dim,
        "l2_norm": float(final_norm_check),
        "scaling": "Phi (1.618) + 528Hz Harmonic Baseline",
        "status": "RECORD_SHATTERED_2048_UNIT_NORM"
    }

    # Broadcast via UDP mesh listener on port 5280
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    message = json.dumps(packet).encode('utf-8')
    try:
        sock.sendto(message, ('127.0.0.1', 5280))
        print(">>> Successfully broadcasted 2,048-point unit-norm tensor packet to UDP port 5280!")
    except Exception as e:
        print(f">>> UDP Broadcast Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    broadcast_tensor_packet()
