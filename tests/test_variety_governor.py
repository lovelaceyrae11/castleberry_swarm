import math
import sqlite3
import tempfile
import unittest
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from variety_governor import (
    BASE_HZ,
    PHI,
    GovernorConfig,
    apply_variety_projection,
    kuramoto_offset_step,
    l2_norm,
    record_variety_event,
    tune_criticality,
)


class TestVarietyGovernor(unittest.TestCase):
    def test_unit_norm_and_novelty_projection(self):
        dim = 2048
        cfg = GovernorConfig(novelty_ceiling=0.85)
        base = [math.sin(2.0 * math.pi * (BASE_HZ * PHI) * (i / dim)) for i in range(dim)]

        vec1, nov1, adj1 = apply_variety_projection(base, [], cfg, step_idx=1)
        self.assertEqual(len(vec1), dim)
        self.assertAlmostEqual(l2_norm(vec1), 1.0, places=5)
        self.assertFalse(adj1)
        self.assertAlmostEqual(nov1, 1.0, places=5)

        # Near-identical vector should trigger projection and stay unit-norm
        vec2, nov2, adj2 = apply_variety_projection(base, [vec1], cfg, step_idx=2)
        self.assertEqual(len(vec2), dim)
        self.assertAlmostEqual(l2_norm(vec2), 1.0, places=5)
        self.assertTrue(adj2)
        self.assertGreater(nov2, 0.1)

    def test_kuramoto_offset_and_criticality_tuning(self):
        theta0 = 0.2
        neighbors = [(1.1, 0.8, math.pi / 6.0)]
        theta1 = kuramoto_offset_step(theta0, omega_i=0.25, neighbors=neighbors, k_gain=0.35)
        self.assertNotAlmostEqual(theta0, theta1, places=5)
        self.assertGreaterEqual(theta1, 0.0)
        self.assertLess(theta1, 2.0 * math.pi)

        # Low novelty should increase temp and lower K toward more exploration
        k_low, temp_low = tune_criticality(0.10, current_k=0.40, current_temp=0.70, guardrail_trips=0)
        self.assertLess(k_low, 0.40)
        self.assertGreater(temp_low, 0.70)

        # Guardrail trip should raise K and lower temp toward stability
        k_trip, temp_trip = tune_criticality(0.50, current_k=0.40, current_temp=0.70, guardrail_trips=1)
        self.assertGreater(k_trip, 0.40)
        self.assertLess(temp_trip, 0.70)

    def test_sqlite_variety_log_persistence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_file = str(Path(tmpdir) / "test_ledger.db")
            record_variety_event(
                db_path=db_file,
                node_id="test_node",
                novelty_score=0.42,
                was_adjusted=True,
                k_gain=0.35,
                ollama_temp=0.70,
                phase_rad=0.15,
                meta={"suite": "unittest"},
            )

            conn = sqlite3.connect(db_file)
            try:
                rows = conn.execute(
                    "SELECT node_id, novelty_score, was_adjusted FROM variety_log"
                ).fetchall()
            finally:
                conn.close()

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0][0], "test_node")
            self.assertAlmostEqual(rows[0][1], 0.42, places=5)
            self.assertEqual(rows[0][2], 1)


if __name__ == "__main__":
    unittest.main()
