import json
import sqlite3
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from load_bloom_6node import latest_6node_run

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "concubine:latest"


def audit_latest_run(timeout: int = 300) -> str:
    latest = latest_6node_run()
    if not latest:
        raise RuntimeError("No 6-node run found in castleberry_ledger.db")

    prompt = (
        f"Audit this 6-node run in 2 short sentences. "
        f"RunID={latest['id']}, MeanCoherence={latest['mean_coherence']}, Gate=0.600, "
        f"Series={latest['coherence_series']}. "
        f"Confirm if it clears the gate and note any drift."
    )

    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": 512,
            "num_predict": 80,
            "num_thread": 2,
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            summary = body.get("response", "").strip()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"Ollama audit skipped ({exc})")
        return ""

    db_path = Path.home() / "castleberry_swarm" / "castleberry_ledger.db"
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bloom_6node_audits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                timestamp_utc TEXT NOT NULL,
                model TEXT NOT NULL,
                audit_text TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            INSERT INTO bloom_6node_audits (run_id, timestamp_utc, model, audit_text)
            VALUES (?, ?, ?, ?)
            """,
            (
                latest["id"],
                datetime.now(timezone.utc).isoformat(),
                MODEL,
                summary,
            ),
        )
        conn.commit()
    finally:
        conn.close()

    print(f"Ollama Audit ({MODEL}) [RunID={latest['id']}]:\n{summary}")
    return summary


if __name__ == "__main__":
    audit_latest_run()
