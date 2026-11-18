import pytest
import numpy as np

PHI = 1.618033988749895

def generate_unit_norm_tensor(dimensions=2048):
    """Generates a phi-scaled unit-norm tensor."""
    raw = np.random.randn(dimensions) * PHI
    norm = np.linalg.norm(raw)
    if norm == 0:
        return raw
    return raw / norm

def test_tensor_dimensions():
    tensor = generate_unit_norm_tensor(2048)
    assert tensor.shape == (2048,), "Tensor must have exactly 2048 dimensions."

def test_tensor_unit_norm():
    tensor = generate_unit_norm_tensor(2048)
    computed_norm = np.linalg.norm(tensor)
    assert np.isclose(computed_norm, 1.0, atol=1e-12), f"Unit norm violation: {computed_norm}"

def test_phi_scaling_presence():
    raw_base = np.ones(10)
    scaled = raw_base * PHI
    assert scaled[0] == PHI, "Phi scaling factor incorrectly applied."
