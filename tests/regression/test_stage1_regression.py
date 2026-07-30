"""Stage 1 (single-algorithm) regression tests.

Exact tier: deterministic optimisers must reproduce the captured golden exactly. Tests skip
(not fail) when the golden has not been captured yet, so the suite is green before baselines
are committed (baseline capture is gated on author approval — see README.md).
"""
from pathlib import Path

import pytest

from helpers import assert_exact, load_golden, to_comparable  # noqa: E402  (path set in conftest)

# Deterministic, no-trained-model-needed optimisers (exact tier). `linear` is included but
# requires SCIP (pyscipopt) and num_proc=1; it skips cleanly if SCIP is unavailable.
EXACT_ALGOS = ["greedy", "random", "linear"]

REGRESSION_SEED = 0


def _run(algo, stage1_input_dir, repo_root):
    import run_stage_1_single_algorithm as rs1

    overrides = {
        "OPTIMISER_TYPE": algo,
        "RUNNER_TYPE": "series",
        "FILTER_SIZE": 100,      # -> FILTER_TYPES=[] (no ml_filter / trained model needed)
        "OBJECTIVE": "nonlinear",
    }
    return rs1.run_stage1(
        overrides,
        config_path=repo_root / "scripts" / "stage_1_config.yaml",
        data_dir=stage1_input_dir,
        random_seed=REGRESSION_SEED,
        make_results_dir=False,
        write_results=False,
        use_wandb=False,
    )


@pytest.mark.parametrize("algo", EXACT_ALGOS)
def test_stage1_exact(algo, stage1_input_dir, repo_root):
    golden = load_golden(f"stage1_{algo}")
    if golden is None:
        pytest.skip(f"baseline stage1_{algo}.json not captured yet (run capture_baselines.py, commit with approval)")
    if algo == "linear":
        pytest.importorskip("pyscipopt", reason="SCIP not installed")
    actual = to_comparable(_run(algo, stage1_input_dir, repo_root))
    assert_exact(actual, golden)


def test_stage1_determinism_self_consistent(stage1_input_dir, repo_root):
    """Sanity check independent of any golden: greedy must reproduce within a session."""
    a = to_comparable(_run("greedy", stage1_input_dir, repo_root))
    b = to_comparable(_run("greedy", stage1_input_dir, repo_root))
    assert_exact(a, b)
    for sf, rec in a.items():
        assert 0.0 <= rec["probability"] <= 1.0
        assert len(rec["workers"]) > 0


# --- Deterministic tier: stochastic solvers made reproducible via opt-in seeding. ---
# GRASP uses optimisers.grasp.random_seed (bitwise deterministic, incl. num_proc>1); rld2 is the
# deterministic RL config (deterministic=True, num_repeats=1). Both use deterministic_config.yaml.
# The stochastic-RL/ensemble determinism is tracked as a follow-up (see issue for RLD1 nesting).
DETERMINISTIC_ALGOS = ["grasp", "rld2"]


def _run_det(algo, stage1_input_dir, repo_root):
    import run_stage_1_single_algorithm as rs1

    overrides = {"OPTIMISER_TYPE": algo, "OBJECTIVE": "nonlinear"}
    if algo != "rld2":  # rld2 maps to its own RL runner/config inside run_stage1
        overrides.update({"RUNNER_TYPE": "series", "FILTER_SIZE": 100})
    return rs1.run_stage1(
        overrides,
        config_path=repo_root / "tests" / "regression" / "inputs" / "deterministic_config.yaml",
        data_dir=stage1_input_dir,
        random_seed=REGRESSION_SEED,
        make_results_dir=False,
        write_results=False,
        use_wandb=False,
    )


@pytest.mark.deterministic
@pytest.mark.parametrize("algo", DETERMINISTIC_ALGOS)
def test_stage1_deterministic(algo, stage1_input_dir, repo_root):
    golden = load_golden(f"stage1_{algo}_det")
    if golden is None:
        pytest.skip(f"baseline stage1_{algo}_det.json not captured yet")
    actual = to_comparable(_run_det(algo, stage1_input_dir, repo_root))
    assert_exact(actual, golden)
