import os
import sys
import json
import sqlite3
import hashlib

HOME = os.path.expanduser("~")
MANIFEST_PATH = os.path.join(HOME, "snapshots", "hex_core_provenance_manifest.json")
SWARM_DB = os.path.join(HOME, "castleberry_swarm", "castleberry_ledger.db")
HEX_DIR = os.path.join(HOME, "lovelaceyrae11", "hex_core_project")

if HEX_DIR not in sys.path:
    sys.path.insert(0, HEX_DIR)

from provenance import get_provenance_anchor, PROVENANCE_DATA


def verify_system_ready(require_db: bool = True) -> dict:
    if not os.path.isfile(MANIFEST_PATH):
        raise RuntimeError(f"Missing provenance manifest: {MANIFEST_PATH}")

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    root = manifest["hex_core_root"]
    drifted = []
    for item in manifest["files"]:
        fpath = os.path.join(root, item["path"])
        if not os.path.isfile(fpath):
            drifted.append((item["path"], "MISSING"))
            continue
        h = hashlib.sha256()
        with open(fpath, "rb") as fp:
            for chunk in iter(lambda: fp.read(65536), b""):
                h.update(chunk)
        if h.hexdigest() != item["sha256"]:
            drifted.append((item["path"], "DRIFT"))

    if drifted:
        raise RuntimeError(f"Hex core drift detected: {drifted}")

    if require_db:
        conn = sqlite3.connect(SWARM_DB)
        conn.execute("SELECT 1 FROM concubine_swarm_dispatches LIMIT 1").fetchone()
        conn.close()

    return {
        "anchor": get_provenance_anchor(),
        "axiom": PROVENANCE_DATA["axiom"],
        "baseline_hz": PROVENANCE_DATA["baseline_frequency"],
        "tracked_files": len(manifest["files"]),
    }


if __name__ == "__main__":
    status = verify_system_ready(require_db=True)
    print("[SYSTEM READY]")
    print(f"  Axiom         : {status['axiom']} ({status['baseline_hz']} Hz)")
    print(f"  Provenance    : {status['anchor']}")
    print(f"  Tracked Files : {status['tracked_files']}/15 intact")
    print(f"  Ledger        : {SWARM_DB} (OK)")
