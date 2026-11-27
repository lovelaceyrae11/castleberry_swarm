import json
import sqlite3
from pathlib import Path
import xml.etree.ElementTree as ET


def load_6node_spec(cml_path=None):
    path = Path(cml_path) if cml_path else (Path.home() / "bloom_6node" / "bloom_6node_matrix.cml")
    root = ET.parse(path).getroot()
    nodes = [
        {
            "id": int(el.attrib.get("id", "0")),
            "key": el.attrib.get("key", ""),
            "name": el.attrib.get("name", ""),
            "role": el.attrib.get("role", ""),
        }
        for el in root.findall("./nodes/node")
    ]
    return {"schema": root.attrib.get("schema", ""), "nodes": nodes}


def latest_6node_run(db_path=None):
    path = Path(db_path) if db_path else (Path.home() / "castleberry_swarm" / "castleberry_ledger.db")
    if not path.exists():
        return None
    conn = sqlite3.connect(path)
    try:
        row = conn.execute(
            """
            SELECT id, timestamp_utc, node_count, checkpoints, mean_coherence, coherence_series_json
            FROM bloom_6node_runs
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()
    finally:
        conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "timestamp_utc": row[1],
        "node_count": row[2],
        "checkpoints": row[3],
        "mean_coherence": row[4],
        "coherence_series": json.loads(row[5]),
    }


if __name__ == "__main__":
    spec = load_6node_spec()
    latest = latest_6node_run()
    print("Nodes:", [n["key"] for n in spec["nodes"]])
    print("Latest run:", latest["id"] if latest else None, latest["mean_coherence"] if latest else None)
