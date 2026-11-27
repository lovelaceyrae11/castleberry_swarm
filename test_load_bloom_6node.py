import unittest
from load_bloom_6node import load_6node_spec, latest_6node_run


class TestSwarmBloomBridge(unittest.TestCase):
    def test_spec_and_ledger_bridge(self):
        spec = load_6node_spec()
        self.assertEqual(len(spec["nodes"]), 6)
        self.assertEqual(spec["nodes"][-1]["key"], "mycelium")

        latest = latest_6node_run()
        self.assertIsNotNone(latest)
        self.assertEqual(latest["node_count"], 6)
        self.assertEqual(latest["checkpoints"], 12)
        self.assertAlmostEqual(latest["mean_coherence"], 0.645, places=3)


if __name__ == "__main__":
    unittest.main()
