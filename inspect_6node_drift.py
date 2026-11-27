import statistics
from load_bloom_6node import latest_6node_run

GATE = 0.600
MAX_SPREAD = 0.300


def main():
    latest = latest_6node_run()
    if not latest:
        raise RuntimeError("No 6-node run found in castleberry_ledger.db")

    series = latest["coherence_series"]
    k_vals = [8 * (i + 1) for i in range(len(series))]
    min_c = min(series)
    max_c = max(series)
    spread = round(max_c - min_c, 3)
    stdev = round(statistics.pstdev(series), 3)
    dips = [(k, c) for k, c in zip(k_vals, series) if c < GATE]

    # Compare first half vs second half to separate downward drift from oscillation
    half = len(series) // 2
    first_half_mean = round(statistics.mean(series[:half]), 3)
    second_half_mean = round(statistics.mean(series[half:]), 3)
    drift_delta = round(second_half_mean - first_half_mean, 3)

    print(f"RunID={latest['id']} | Mean={latest['mean_coherence']:.3f} | Min={min_c:.3f} | Max={max_c:.3f}")
    print(f"Spread={spread:.3f} (limit {MAX_SPREAD:.3f}) | StdDev={stdev:.3f}")
    print(f"First-half mean={first_half_mean:.3f} | Second-half mean={second_half_mean:.3f} | Drift={drift_delta:+.3f}")
    print(f"Checkpoints below {GATE:.3f} ({len(dips)}/{len(series)}): {dips}")

    if spread > MAX_SPREAD or drift_delta < -0.05:
        print("STATUS: WARNING - High variance or downward drift detected.")
    else:
        print("STATUS: STABLE - Within spread and drift limits.")


if __name__ == "__main__":
    main()
