"""Capture stage-1 golden baselines from short, deterministic runs.

Run this DELIBERATELY (and review the output) before committing golden files — capturing and
committing baselines is gated on author approval. It must run in the canonical environment
(articleenv) with determinism env vars set:

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \\
        articleenv/bin/python superscript-abm/tests/regression/capture_baselines.py \\
        --data-dir test_data/test_dataset --limit 2 --out-dir <dir>

Use --out-dir to write goldens somewhere other than the committed baselines/ dir for a dry run.
Only the deterministic (exact-tier) algorithms are captured here.
"""
import argparse
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).parent))

from helpers import BASELINE_DIR, aggregate_stats, save_golden, to_comparable  # noqa: E402

EXACT_ALGOS = ["greedy", "random", "linear"]
SEED = 0


def _stage_input(data_dir: Path, limit: int) -> Path:
    """Copy the first `limit` state pickles into a temp dir (sorted for stability)."""
    states = sorted(data_dir.glob("*.pickle"))[:limit]
    if not states:
        raise SystemExit(f"no state pickles found in {data_dir}")
    tmp = Path(tempfile.mkdtemp(prefix="regr_states_"))
    for s in states:
        (tmp / s.name).write_bytes(s.read_bytes())
    return tmp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, default=REPO_ROOT / "test_data" / "test_dataset")
    ap.add_argument("--limit", type=int, default=2)
    ap.add_argument("--out-dir", type=Path, default=BASELINE_DIR)
    ap.add_argument("--algos", nargs="*", default=EXACT_ALGOS)
    ap.add_argument("--config", type=Path, default=REPO_ROOT / "scripts" / "stage_1_config.yaml",
                    help="ABM/optimiser config (use the deterministic config for grasp/rld2)")
    ap.add_argument("--suffix", default="", help="golden filename suffix, e.g. _det")
    args = ap.parse_args()

    import run_stage_1_single_algorithm as rs1

    in_dir = _stage_input(args.data_dir, args.limit)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    for algo in args.algos:
        if algo == "linear":
            try:
                import pyscipopt  # noqa: F401
            except Exception as e:
                print(f"[skip] linear: SCIP unavailable ({e})")
                continue
        overrides = {"OPTIMISER_TYPE": algo, "OBJECTIVE": "nonlinear"}
        # rld2 uses the parallel/deterministic RL mapping in run_stage1; greedy/random/linear/grasp are series.
        if algo != "rld2":
            overrides.update({"RUNNER_TYPE": "series", "FILTER_SIZE": 100})
        results = rs1.run_stage1(
            overrides,
            config_path=args.config,
            data_dir=in_dir,
            random_seed=SEED,
            make_results_dir=False,
            write_results=False,
            use_wandb=False,
        )
        comparable = to_comparable(results)
        # write to out_dir (may be the committed baselines/ dir, or a dry-run scratch dir)
        import json
        out = args.out_dir / f"stage1_{algo}{args.suffix}.json"
        with open(out, "w") as f:
            json.dump(comparable, f, indent=2, sort_keys=True)
        print(f"[ok] {algo}: wrote {out}  ({aggregate_stats(results)})")


if __name__ == "__main__":
    main()
