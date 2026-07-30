# Regression safety net (Stage 1 cleanup)

These tests prove that refactoring does **not** change experimental results. We capture short,
deterministically-seeded baseline runs as golden files (`baselines/*.json`) and compare future
runs against them. (Design rationale documented in `planning/REFACTOR_FINDINGS.md` on the
development branches; not included in this release snapshot.)

## Comparison tiers
| Tier | Optimisers | Comparison |
|---|---|---|
| exact | `random`, `greedy`, `linear` (`num_proc=1`), `rld2` (deterministic series) | equality |
| tolerance | stochastic RL | `np.allclose` (torch/SB3-version sensitive) |
| distribution | `grasp`, `ensemble` (GRASP reseeds from OS entropy) | aggregate stats only |

## Status (article-release-v1)
- `helpers.py`, `conftest.py`, `test_stage1_regression.py`, `capture_baselines.py` are in place.
- **Golden files ARE committed** (`baselines/stage1_{greedy,random,linear,grasp_det,rld2_det}.json`),
  captured in the canonical article environment — see `baselines/MANIFEST.json` for the exact
  package pins and determinism settings.
- **Input fixtures** (`inputs/stage1_states/state_0.pickle`, `state_10.pickle`) are committed
  (absolute path metadata stripped; data-preserving).
- `pytest` is required but not pinned in `article_requirements.txt` — `pip install pytest`.
- The `rld2` deterministic test additionally requires the gitignored trained model
  `superscript-abm/models/RLD2-v3.106-nonlinear_2` (not distributed with this repository).
  The `linear` test skips cleanly without PySCIPOpt/SCIP.
- Stage-2 / sensitivity / filter-sweep tests are not covered by this suite.

## How to capture baselines (after approval)
Run in the canonical env (articleenv) with determinism env vars exported **before** start:

```bash
make regression-capture        # writes baselines/stage1_*.json   (review, then commit)
# or a dry run to a scratch dir (does not touch committed baselines):
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  articleenv/bin/python tests/regression/capture_baselines.py \
  --data-dir test_data/test_dataset --limit 2 --out-dir /tmp/regr_dryrun
```

Also commit 2 small state pickles into `inputs/stage1_states/` so the tests are self-contained.

## Determinism caveats (from Agent 4 review)
- **`random['respect_constraints']` must be `False`** for seed-reproducibility of ABM-stepping runs
  (`example_run.py:24-27`). This matters for the Stage 2 / sensitivity baselines (which step the
  ABM); the Stage 1 exact-tier runs validated here solve fixed pickled states and are deterministic
  as-is. `example_run.py:141` has an existing model-variable equality assert to reuse.
- **Cross-platform bitwise parity is not guaranteed** (`static_testing.py:9`) — regenerate baselines
  per environment (articleenv / Py3.10) and record the env in `baselines/MANIFEST.json`.

## How to run
```bash
make regression                # exact tier only (CI gate)
```
The golden files record exact-tier results; a mismatch means the refactor changed a result.
Each golden is keyed by `state_file` (order-independent) and stores `workers` + numeric metrics
as plain JSON — deliberately NOT pickled `Solution`/`State` objects, so goldens survive the
class refactors we are guarding against.
