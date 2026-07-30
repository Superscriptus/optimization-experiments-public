<!-- SUPERSCRIPT BRANDING -->
<!-- Badges + logo in the style of Superscriptus/SuperScript (othneildrew Best-README-Template). -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![AGPL-3.0 License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/Superscriptus/SuperScript">
    <img src="documentation/images/logo.svg" alt="SuperScript logo" width="390" height="80">
  </a>

  <h3 align="center">Team-allocation optimisation experiments</h3>

  <p align="center">
    Top-level codebase for the SuperScript article: experiment drivers, configuration, results, analysis, and the golden regression suite.
  </p>
</p>

---

# OptimizationExperiments

Experiments comparing **team-allocation optimisation methods** for
**SuperScript**, an agent-based model (ABM) of team formation in
project-based organisations. This repository is the top-level codebase for
the accompanying article: it contains the experiment drivers, experiment
configuration, results, analysis, and the golden regression suite used to
verify that the article results reproduce.

The optimisers compared are: Random, Greedy, GRASP, MILP (the "linear"
optimiser, solved with SCIP), hierarchical reinforcement learning
(RLD2 team selection over an RLD1 hard-skill allocator), and an Ensemble of
methods. Each is run over datasets of pickled ABM states (100-worker
organisations) and scored by the resulting project-success probability.

## Repository architecture (submodules)

This repository nests three submodules — clone **recursively**:

```
OptimizationExperiments          (this repo: experiments, config, results, regression goldens)
└── superscript-abm              (the SuperScript ABM + all team-allocation optimisers)
    ├── gym-superscript          (Gymnasium RL environments wrapping the ABM: RLD1/RLD2 families)
    └── rl-baselines3-zoo        (fork of the SB3 training zoo used to train the RL policies)
```

- [superscript-abm](https://github.com/Superscriptus/superscript-abm-public) —
  the ABM (Mesa-based) and the optimiser implementations
  (`superscript_abm/optimisation_decoupled.py`); optimiser hyperparameters
  live in `superscript_abm/config.yaml` (overridden per-experiment by
  `scripts/stage_1_config.yaml` here). Also ships the trained RLD2 policies
  (`superscript-abm/models/`, via **Git LFS** — see Install).
- [gym-superscript](https://github.com/Superscriptus/gym-superscript-public) —
  the custom Gymnasium environments used to train and run the RL policies;
  ships the trained RLD1 (lower-level) agents.
- [rl-baselines3-zoo](https://github.com/Superscriptus/rl-baselines3-zoo) —
  fork of [DLR-RM/rl-baselines3-zoo](https://github.com/DLR-RM/rl-baselines3-zoo)
  with the tuned PPO hyperparameters for the SuperScript envs and the
  project's training/evaluation workflow.

## Repository layout

- `scripts/` — experiment drivers and configuration:
  - `run_stage_1_single_algorithm.py` — solves every state in a dataset with
    one algorithm (the main article experiment); importable as
    `run_stage1()` and used by the regression suite.
  - `run_stage_2_single_algorithm.py` — stage-2 (dynamic/ABM-stepping) runs.
  - `run_sensitivity_single_algorithm.py`, `filter_sweep_single_state.py`,
    `filter_sweep_multi_state.py` — sensitivity and workforce-filter sweeps.
  - `create_test_data.py` — generates datasets of ABM states by repeated
    simulation.
  - `stage_1_config.yaml`, `stage_2_config.yaml`, `scenario_*_abm_config.yaml`
    — experiment configuration (ABM + optimiser settings).
- `stage_1_results/` — committed stage-1 result pickles.
- `analysis/` — analysis notebooks producing the aggregate results/plots.
- `tests/regression/` — golden regression suite (see "Verifying
  reproduction" below).
- `article_requirements.txt` — **pinned package set of the environment in
  which the article results were produced and verified** (see Install).
- `requirements.txt` — an older (Python 3.7-era) freeze kept for reference;
  do not use for reproduction.

**Datasets.** The article datasets `test_data/dataset_1`
(D<sub>test</sub>, 100 states) and `test_data/validation_dataset_1`
(D<sub>val</sub>) are **not committed** to this repository. Equivalent
committed data: `superscript-abm/test_data/` (test_dataset +
validation_dataset state pickles) and the regression-suite input states in
`tests/regression/inputs/stage1_states/`.

## Install

Requires **Python 3.10** (the article environment was Python 3.10.13) and
**[Git LFS](https://git-lfs.com)** — the trained RL policies (under
`superscript-abm/models/`) are stored via Git Large File Storage.

**Install Git LFS *before* cloning.** If you clone without it, the model
files come down as small text pointer files instead of the actual weights,
and the RL/Ensemble optimisers will fail to load:

```bash
# Debian/Ubuntu (see https://git-lfs.com for macOS/Windows/other)
sudo apt-get install git-lfs
git lfs install            # one-time, sets up the LFS filters for your user
```

Then clone recursively (fetches the submodules and, with Git LFS installed,
the trained models):

```bash
git clone --recursive https://github.com/Superscriptus/optimization-experiments-public.git
cd optimization-experiments-public
# Already cloned before installing Git LFS? Fetch the models now:
#   git -C superscript-abm lfs pull
python3.10 -m venv articleenv
source articleenv/bin/activate
python -m pip install --upgrade pip wheel
pip install -r article_requirements.txt
pip install torch==1.13.1     # not in article_requirements.txt; see torch note
pip install -e superscript-abm/rl-baselines3-zoo
pip install -e superscript-abm/gym-superscript
pip install -e superscript-abm
pip install pytest            # for the regression suite (not in article_requirements.txt)
```

Key pins in `article_requirements.txt` (recorded in
`tests/regression/baselines/MANIFEST.json`): numpy 1.26.4, scipy 1.13.0,
pandas 2.2.2, scikit-learn 1.4.1.post1, Mesa 0.9.0, gymnasium 0.29.1,
stable-baselines3 2.3.2, PySCIPOpt 5.1.1.

**PySCIPOpt / SCIP note (needed for the MILP "linear" optimiser).**
Installing `pyscipopt` on Linux historically required building
[SCIP](https://www.scipopt.org/) manually and setting `SCIPOPTDIR`
(see the [SCIP install guide](https://github.com/scipopt/scip/blob/master/INSTALL.md)).
Recent PySCIPOpt releases (>= 4.3, including the pinned 5.1.1) publish
binary wheels that bundle SCIP, so `pip install pyscipopt==5.1.1` normally
works out of the box on x86-64 Linux/macOS/Windows; fall back to the manual
SCIP + `SCIPOPTDIR` route only if no wheel matches your platform. Without
SCIP the `linear` regression test skips cleanly; everything else still runs.

**Torch note.** The article environment used `torch 1.13.1+cu116` (CUDA).
The RL policies run inference only in these experiments, so a CPU
torch 1.13.1 build is expected to suffice, but the goldens were recorded
against the CUDA build — for strict environment parity use `+cu116`.

**Trained RL models.** The lower-level RLD1 agents are committed inside
gym-superscript. The top-level RLD2 PPO models
(`superscript-abm/models/RLD2*`) are **shipped via Git LFS** (install Git
LFS before cloning — see Install); they are required for the RL and Ensemble
experiments and for the `rld2` deterministic regression golden. See
`superscript-abm/README.md` for the list of shipped models.

## Running the experiments

The stage-1 experiment (solve every state in a dataset with one algorithm)
is driven by `run_stage1()`; the experiment is selected via a globals dict
(`OPTIMISER_TYPE`: `greedy` / `random` / `grasp` / `linear` /
`rld2` / `rld2_100_10` / `ensemble` / ..., `OBJECTIVE`: `linear` /
`nonlinear`, `FILTER_SIZE`, `RUNNER_TYPE`). Because the full article
datasets are not committed (see "Datasets" above), point `data_dir` at a
committed dataset, e.g.:

```python
import sys; sys.path.insert(0, 'scripts')
from pathlib import Path
from run_stage_1_single_algorithm import run_stage1

results = run_stage1(
    {'OPTIMISER_TYPE': 'greedy', 'FILTER_SIZE': 100,
     'RUNNER_TYPE': 'series', 'OBJECTIVE': 'nonlinear'},
    data_dir=Path('superscript-abm/test_data/test_dataset'),
)
```

Running the script bare (`python scripts/run_stage_1_single_algorithm.py`)
uses its `DEFAULT_GLOBALS` and expects a dataset at
`test_data/test_dataset`.

Optimiser hyperparameters come from `scripts/stage_1_config.yaml`
(GRASP, MILP time limits/coefficients, RL repeat counts, filters, etc.).

## Verifying reproduction (canonical path)

The canonical check that your environment reproduces the article
computations is the **stage-1 golden regression suite**: it re-runs the real
optimisers on committed input states and compares against committed golden
JSON results (`tests/regression/baselines/`), byte-for-byte for the
deterministic tiers.

```bash
make -C tests/regression regression       # exact tier: greedy, random, linear (MILP)
# deterministic tier (adds seeded GRASP + deterministic RL; RL uses the
# LFS-shipped trained model models/RLD2-v3.106-nonlinear_2 in superscript-abm):
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  articleenv/bin/python -m pytest tests/regression -m "not distribution" -q
```

Notes:

- The Makefile assumes the venv is at `./articleenv` (override with
  `make PY=/path/to/python ...`).
- The determinism environment variables must be set **before** Python
  starts (the Makefile does this for you).
- Golden equality is environment-sensitive: use the pins above
  (`tests/regression/baselines/MANIFEST.json` records the exact
  environment; cross-platform bitwise parity is not guaranteed).
- The `linear` test skips if PySCIPOpt/SCIP is unavailable; the `rld2`
  deterministic test requires the LFS-shipped trained model (above).

A separate observation-encoding golden for the gym environments
(`tests/data/golden_obs_unmodified.pickle` + capture script) exists on the
development branches of gym-superscript and verifies the RL observation
encodings; it is not part of this snapshot.

## License and copyright

Copyright (C) 2025 Michael Christen <michael.christen@mobi.ch>

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version. See [LICENSE](LICENSE) for the full text.

The `rl-baselines3-zoo` submodule is a fork of MIT-licensed upstream code;
it retains the upstream MIT license for upstream code, with fork
modifications under AGPL-3.0 (see its README and LICENSE files).


<!-- MARKDOWN LINKS & IMAGES (SuperScript branding; reference-style) -->
[contributors-shield]: https://img.shields.io/github/contributors/Superscriptus/optimization-experiments-public.svg?style=for-the-badge
[contributors-url]: https://github.com/Superscriptus/optimization-experiments-public/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Superscriptus/optimization-experiments-public.svg?style=for-the-badge
[forks-url]: https://github.com/Superscriptus/optimization-experiments-public/network/members
[stars-shield]: https://img.shields.io/github/stars/Superscriptus/optimization-experiments-public.svg?style=for-the-badge
[stars-url]: https://github.com/Superscriptus/optimization-experiments-public/stargazers
[issues-shield]: https://img.shields.io/github/issues/Superscriptus/optimization-experiments-public.svg?style=for-the-badge
[issues-url]: https://github.com/Superscriptus/optimization-experiments-public/issues
[license-shield]: https://img.shields.io/badge/License-AGPL--3.0-blue.svg?style=for-the-badge
[license-url]: LICENSE
