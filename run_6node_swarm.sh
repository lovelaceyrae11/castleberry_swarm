#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

echo "=== 1. Running 6-Node CML Pipeline & Ledger Log ==="
~/bloom_6node/run_all.sh

echo "=== 2. Running Swarm Bridge Unit Test ==="
cd ~/castleberry_swarm
python -m unittest test_load_bloom_6node.py -v

echo "=== 3. Firing Coherence-Gated UDP Broadcast (Port 5280) ==="
python ~/castleberry_swarm/emit_6node_udp.py

echo "=== 4. Checking OpenTimestamps Proof ==="
if command -v ots >/dev/null 2>&1 && [ -f ~/bloom_6node/bloom_6node_run.json.ots ]; then
  ots info ~/bloom_6node/bloom_6node_run.json.ots | head -n 10
fi
