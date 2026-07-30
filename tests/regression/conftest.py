"""Pytest configuration for the regression safety-net suite.

Determinism note: for exact-tier comparisons the run must be reproducible. Seeds are passed
explicitly via run_stage1(random_seed=...). Thread/hash determinism (PYTHONHASHSEED=0,
OMP/MKL/OPENBLAS_NUM_THREADS=1) must be exported BEFORE the interpreter starts — see the
`regression` target in the Makefile. This conftest only *checks* and warns, it cannot fix it
after numpy is imported.
"""
import os
import sys
import warnings
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"
REGRESSION_DIR = Path(__file__).resolve().parent


def pytest_configure(config):
    # Make the experiment runner scripts and the regression helpers importable.
    for p in (str(REGRESSION_DIR), str(SCRIPTS_DIR)):
        if p not in sys.path:
            sys.path.insert(0, p)
    if os.environ.get("PYTHONHASHSEED") != "0":
        warnings.warn(
            "PYTHONHASHSEED != 0; exact-tier comparisons may be unstable. "
            "Run via `make regression` (sets PYTHONHASHSEED=0 and single-threaded BLAS)."
        )


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def stage1_input_dir() -> Path:
    """Directory of 2 tiny state pickles used for stage-1 regression runs.

    Not committed yet (input fixtures are added under author approval — see README). If the
    directory is absent the dependent tests skip rather than fail.
    """
    d = Path(__file__).parent / "inputs" / "stage1_states"
    if not (d.exists() and any(d.glob("*.pickle"))):
        pytest.skip(f"stage-1 input fixtures not present at {d} (see regression/README.md)")
    return d
