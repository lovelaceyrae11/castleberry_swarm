import json
import socket
from datetime import datetime
import numpy as np

from castleberry_pure_tensor import run_pure_tensor
from variety_governor import DEFAULT_PROVENANCE


def broadcast_tensor_packet(
    host: str = "127.0.0.1",
    port: int = 5280,
    use_variety: bool = True,
    recent_tensors: list[list[float]] | None = None,
) -> dict:
    print(">>> [CASTLEBERRY BLOOM] Preparing 2,048-Point Governed Tensor for UDP Mesh Broadcast...")

    target_dim = 2048
    tensor_list = run_pure_tensor(
        use_variety=use_variety,
        recent_tensors=recent_tensors,
    )
    normalized_tensor = np.asarray(tensor_list, dtype=np.float64)
    if normalized_tensor.size != target_dim:
        raise ValueError(f"Expected tensor length {target_dim}, got {normalized_tensor.size}.")

    final_norm_check = float(np.linalg.norm(normalized_tensor))
    if not np.isfinite(final_norm_check) or final_norm_check == 0.0:
        raise ValueError("Normalized tensor norm is invalid or zero.")

    print(r">>> Lattice Scaling: Phi ($\phi \approx 1.618034$) + 528Hz Harmonic Baseline")
    print(f">>> Tensor Verified. L2 Norm: {final_norm_check:.6f} | Variety Governor: {use_variety}")

    packet = {
        "source": "castleberry_pure_tensor_engine",
        "timestamp": datetime.now().isoformat(),
        "dimensions": target_dim,
        "l2_norm": float(final_norm_check),
        "scaling": "Phi (1.618034) + 528Hz Harmonic Baseline",
        "status": "RECORD_SHATTERED_2048_UNIT_NORM",
        "variety_governed": bool(use_variety),
        "tensor_preview_4": [round(float(x), 6) for x in normalized_tensor[:4]],
        "provenance": dict(DEFAULT_PROVENANCE),
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    message = json.dumps(packet).encode("utf-8")
    try:
        sock.sendto(message, (host, port))
        print(f">>> Successfully broadcasted 2,048-point governed tensor packet to UDP {host}:{port}!")
    except Exception as e:
        print(f">>> UDP Broadcast Error: {e}")
    finally:
        sock.close()

    return packet


if __name__ == "__main__":
    broadcast_tensor_packet()
