"""Helpers for the Stage 1 regression-test safety net.

The goal of these tests is to prove that refactoring does NOT change experimental
results. We capture short, deterministically-seeded baseline runs as golden files and
compare future runs against them.

Comparison is three-tier (see REFACTOR_FINDINGS.md / Agent 6 design):
  - exact       : random, greedy, linear (num_proc=1), rld2 (deterministic series)
  - tolerance   : stochastic RL (torch/SB3-version sensitive)  -> assert_close
  - distribution: grasp, ensemble (GRASP reseeds from OS entropy) -> aggregate stats only

Golden files are stored as plain numeric structures (NOT pickled Solution/State objects),
so they survive the class refactors we are guarding against.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

# Numeric keys worth pinning from a stage-1 results dict. `runtime`/`timeout` are volatile
# (wall-clock / machine-dependent) and excluded from comparison.
NUMERIC_KEYS = [
    "probability",
    "team_size",
    "probability_ovr",
    "probability_skill_balance",
    "probability_creativity_match",
    "probability_individual_chemistry",
    "probability_team_chemistry",
    "probability_risk",
    "ovr",
    "skill_balance",
    "creativity_match",
    "creativity_level",
    "risk",
    "individual_chemistry",
    "team_chemistry",
]

BASELINE_DIR = Path(__file__).parent / "baselines"


def to_comparable(results: dict) -> dict:
    """Reduce a stage-1 results dict to a stable, order-independent, JSON-able structure.

    Keyed by state_file so comparison does not depend on glob/filesystem ordering. `workers`
    (a numpy array of selected indices) is stored as a sorted plain list. Volatile fields
    (runtime, timeout) are dropped.
    """
    states = list(results["state_file"])
    out = {}
    for i, sf in enumerate(states):
        rec = {"workers": sorted(int(w) for w in results["workers"][i])}
        for k in NUMERIC_KEYS:
            if k in results and len(results[k]) > i:
                v = results[k][i]
                # Some metrics can legitimately be None for a given solution; preserve as-is
                # (JSON null) rather than crashing — a None vs number change is a real change.
                rec[k] = float(v) if v is not None else None
        out[sf] = rec
    return out


def save_golden(name: str, comparable: dict) -> Path:
    BASELINE_DIR.mkdir(parents=True, exist_ok=True)
    path = BASELINE_DIR / f"{name}.json"
    with open(path, "w") as f:
        json.dump(comparable, f, indent=2, sort_keys=True)
    return path


def load_golden(name: str) -> dict | None:
    path = BASELINE_DIR / f"{name}.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def assert_exact(actual: dict, golden: dict):
    """Exact equality, per state and per key. For deterministic-tier algorithms."""
    assert set(actual) == set(golden), (
        f"state set differs: only-in-actual={set(actual) - set(golden)}, "
        f"only-in-golden={set(golden) - set(actual)}"
    )
    for sf, grec in golden.items():
        arec = actual[sf]
        assert arec["workers"] == grec["workers"], f"{sf}: team differs {arec['workers']} != {grec['workers']}"
        for k, gv in grec.items():
            if k == "workers":
                continue
            assert arec[k] == gv, f"{sf}.{k}: {arec[k]} != {gv}"


def assert_close(actual: dict, golden: dict, rtol: float = 1e-5, atol: float = 1e-8):
    """Tolerance comparison for numeric fields. For version-sensitive (RL) results.

    Teams (worker selections) are still compared exactly — a different team is a real change,
    not a floating-point artefact.
    """
    assert set(actual) == set(golden), "state set differs"
    for sf, grec in golden.items():
        arec = actual[sf]
        assert arec["workers"] == grec["workers"], f"{sf}: team differs"
        for k, gv in grec.items():
            if k == "workers":
                continue
            if gv is None or arec[k] is None:
                assert arec[k] == gv, f"{sf}.{k}: {arec[k]} != {gv} (None mismatch)"
            else:
                np.testing.assert_allclose(arec[k], gv, rtol=rtol, atol=atol, err_msg=f"{sf}.{k}")


def aggregate_stats(results: dict, key: str = "probability") -> dict:
    """Distribution-tier summary for non-reproducible methods (grasp, ensemble)."""
    raw = list(results[key])
    vals = np.asarray([v for v in raw if v is not None], dtype=float)
    n_none = sum(1 for v in raw if v is None)
    if vals.size == 0:
        return {"n": len(raw), "n_none": n_none, "mean": None}
    return {
        "n": len(raw),
        "n_none": n_none,
        "mean": float(vals.mean()),
        "median": float(np.median(vals)),
        "min": float(vals.min()),
        "max": float(vals.max()),
        "std": float(vals.std()),
    }
