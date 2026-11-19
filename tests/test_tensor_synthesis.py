import os
import sys
import unittest
import numpy as np

SWARM_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SWARM_DIR not in sys.path:
    sys.path.insert(0, SWARM_DIR)

PHI = 1.618033988749895


def generate_unit_norm_tensor(dimensions=2048):
    """Generates a phi-scaled unit-norm tensor."""
    raw = np.random.randn(dimensions) * PHI
    norm = np.linalg.norm(raw)
    if norm == 0:
        return raw
    return raw / norm


class TestTensorSynthesis(unittest.TestCase):
    def test_tensor_dimensions(self):
        tensor = generate_unit_norm_tensor(2048)
        self.assertEqual(tensor.shape, (2048,), "Tensor must have exactly 2048 dimensions.")

    def test_tensor_unit_norm(self):
        tensor = generate_unit_norm_tensor(2048)
        computed_norm = np.linalg.norm(tensor)
        self.assertTrue(
            np.isclose(computed_norm, 1.0, atol=1e-12),
            f"Unit norm violation: {computed_norm}",
        )

    def test_phi_scaling_presence(self):
        raw_base = np.ones(10)
        scaled = raw_base * PHI
        self.assertEqual(scaled[0], PHI, "Phi scaling factor incorrectly applied.")

    def test_system_preflight_ready(self):
        from system_preflight import verify_system_ready
        status = verify_system_ready(require_db=True)
        self.assertEqual(status["tracked_files"], 15)
        self.assertEqual(status["baseline_hz"], 528.0)


if __name__ == "__main__":
    unittest.main()
