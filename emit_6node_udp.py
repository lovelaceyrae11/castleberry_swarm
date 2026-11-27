import json
import socket
from load_bloom_6node import load_6node_spec, latest_6node_run


def emit_if_coherent(host: str = "127.0.0.1", port: int = 5280, min_coherence: float = 0.600) -> dict:
    spec = load_6node_spec()
    latest = latest_6node_run()
    if not latest:
        raise RuntimeError("No 6-node run found in castleberry_ledger.db")

    status = "BROADCAST" if latest["mean_coherence"] >= min_coherence else "HOLD_NOVELTY"
    packet = {
        "system": "castleberry_bloom_6node",
        "status": status,
        "run_id": latest["id"],
        "mean_coherence": latest["mean_coherence"],
        "nodes": [n["key"] for n in spec["nodes"]],
        "latest_checkpoint": latest["coherence_series"][-1],
    }

    if status == "BROADCAST":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(json.dumps(packet).encode("utf-8"), (host, port))
        finally:
            sock.close()

    return packet


if __name__ == "__main__":
    result = emit_if_coherent()
    print(f"Gate={result['status']} | RunID={result['run_id']} | MeanCoherence={result['mean_coherence']:.3f} | Port=5280")
