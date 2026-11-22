"""
Variety Governor for Castleberry Bloom (~/castleberry_swarm)
Preserves emergent variety during tensor synthesis, phase coupling, and generation
while maintaining unit-norm stability and SQLite ledger traceability.
"""

from __future__ import annotations

import json
import math
import sqlite3
import time
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
BASE_HZ: float = 528.0


@dataclass
class GovernorConfig:
    novelty_ceiling: float = 0.85       # Max allowed cosine similarity to recent vectors
    orthogonal_alpha: float = 0.65      # Projection strength away from over-used directions
    jitter_scale: float = 0.015         # Small deterministic harmonic perturbation when saturated
    base_k: float = 0.35                # Baseline Kuramoto coupling gain
    min_k: float = 0.12                 # Lower K -> more exploratory phase spread
    max_k: float = 0.85                 # Upper K -> stronger coherence lock
    base_temp: float = 0.70             # Baseline Ollama temperature
    min_temp: float = 0.25              # Lower temp -> tighter/safer generation
    max_temp: float = 1.05              # Upper temp -> higher diversity/exploration
    target_novelty: float = 0.45        # Target (1 - max_recent_similarity) around criticality
    window_size: int = 24               # Recent vectors compared for novelty


def l2_norm(vec: Sequence[float]) -> float:
    return math.sqrt(sum(x * x for x in vec))


def normalize_unit(vec: Sequence[float], fallback_seed: int = 1) -> List[float]:
    n = l2_norm(vec)
    if n > 1e-12:
        return [x / n for x in vec]
    # Deterministic fallback unit vector if norm collapses
    dim = max(1, len(vec))
    out = [
        math.sin((i + 1) * PHI * fallback_seed) / math.sqrt(dim)
        for i in range(dim)
    ]
    fn = l2_norm(out)
    return [x / fn for x in out] if fn > 1e-12 else out


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    na = l2_norm(a)
    nb = l2_norm(b)
    if na <= 1e-12 or nb <= 1e-12:
        return 0.0
    return dot(a, b) / (na * nb)


def apply_variety_projection(
    candidate: Sequence[float],
    recent_vectors: Sequence[Sequence[float]],
    config: GovernorConfig | None = None,
    step_idx: int = 1,
) -> Tuple[List[float], float, bool]:
    """
    Projects out dominant overlap if candidate is too similar to recent unit-norm vectors,
    adds subtle harmonic residual when needed, and returns:
      (unit_norm_vector, novelty_score, was_adjusted)
    where novelty_score = 1.0 - max_similarity in [0.0, 2.0] (higher = more novel).
    """
    cfg = config or GovernorConfig()
    vec = normalize_unit(candidate, fallback_seed=step_idx)

    if not recent_vectors:
        return vec, 1.0, False

    sims = [cosine_similarity(vec, rv) for rv in recent_vectors[-cfg.window_size :]]
    max_sim = max(sims) if sims else 0.0
    novelty = max(0.0, 1.0 - max_sim)
    adjusted = False

    if max_sim > cfg.novelty_ceiling:
        adjusted = True
        working = list(vec)
        for rv in recent_vectors[-cfg.window_size :]:
            s = dot(working, rv)
            if s > 0.25:
                proj_coeff = cfg.orthogonal_alpha * s
                working = [w - proj_coeff * r for w, r in zip(working, rv)]

        # Subtle deterministic phase-seeded perturbation to break symmetry cleanly
        for i in range(len(working)):
            phase_nudge = math.sin((i + 1) * (step_idx + 1) * (PHI / BASE_HZ) * 100.0)
            working[i] += cfg.jitter_scale * phase_nudge

        vec = normalize_unit(working, fallback_seed=step_idx + 7)
        new_sims = [cosine_similarity(vec, rv) for rv in recent_vectors[-cfg.window_size :]]
        novelty = max(0.0, 1.0 - (max(new_sims) if new_sims else 0.0))

    return vec, novelty, adjusted


def kuramoto_offset_step(
    theta_i: float,
    omega_i: float,
    neighbors: Iterable[Tuple[float, float, float]],
    k_gain: float,
    dt: float = 0.05,
) -> float:
    """
    Advances oscillator phase theta_i with target phase offsets:
      neighbors: iterable of (theta_j, weight_ij, target_delta_phi_ij)
      d(theta_i)/dt = omega_i + (K / N) * sum(w_ij * sin(theta_j - theta_i - delta_phi_ij))
    Non-zero delta_phi_ij preserves structured polyrhythmic variety.
    """
    nbrs = list(neighbors)
    if not nbrs:
        return (theta_i + omega_i * dt) % (2.0 * math.pi)

    coupling_sum = 0.0
    for theta_j, w_ij, delta_phi in nbrs:
        coupling_sum += w_ij * math.sin((theta_j - theta_i) - delta_phi)

    d_theta = omega_i + (k_gain / len(nbrs)) * coupling_sum
    return (theta_i + d_theta * dt) % (2.0 * math.pi)


def tune_criticality(
    novelty_score: float,
    current_k: float,
    current_temp: float,
    guardrail_trips: int = 0,
    config: GovernorConfig | None = None,
) -> Tuple[float, float]:
    """
    Balances emergent variety vs. coherence/guardrail stability around criticality.
    - If guardrails trip or novelty is too high (chaotic drift): raise K, lower temp.
    - If novelty is too low (mode collapse / lock-in): lower K, raise temp.
    """
    cfg = config or GovernorConfig()
    k = current_k
    temp = current_temp

    if guardrail_trips > 0 or novelty_score > (cfg.target_novelty + 0.30):
        k = min(cfg.max_k, k + 0.06)
        temp = max(cfg.min_temp, temp - 0.05)
    elif novelty_score < (cfg.target_novelty - 0.15):
        k = max(cfg.min_k, k - 0.05)
        temp = min(cfg.max_temp, temp + 0.05)
    else:
        # Gentle relaxation toward baseline
        k = k + 0.15 * (cfg.base_k - k)
        temp = temp + 0.15 * (cfg.base_temp - temp)

    return round(k, 4), round(temp, 4)


def ensure_variety_table(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS variety_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts REAL NOT NULL,
                node_id TEXT NOT NULL,
                novelty_score REAL NOT NULL,
                was_adjusted INTEGER NOT NULL,
                k_gain REAL NOT NULL,
                ollama_temp REAL NOT NULL,
                phase_rad REAL NOT NULL,
                meta_json TEXT
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def record_variety_event(
    db_path: str,
    node_id: str,
    novelty_score: float,
    was_adjusted: bool,
    k_gain: float,
    ollama_temp: float,
    phase_rad: float,
    meta: dict | None = None,
) -> None:
    ensure_variety_table(db_path)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO variety_log (
                ts, node_id, novelty_score, was_adjusted, k_gain, ollama_temp, phase_rad, meta_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                time.time(),
                node_id,
                float(novelty_score),
                1 if was_adjusted else 0,
                float(k_gain),
                float(ollama_temp),
                float(phase_rad),
                json.dumps(meta or {}),
            ),
        )
        conn.commit()
    finally:
        conn.close()
