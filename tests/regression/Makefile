# Regression safety-net targets. Determinism env vars are exported here, BEFORE the Python
# interpreter starts (setting them inside conftest.py is too late — numpy is already imported).
#
# Usage (from anywhere):
#   make -C tests/regression regression
#   make -C tests/regression regression-capture

REPO_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/../..)
PY        ?= $(REPO_ROOT)/articleenv/bin/python
DATA_DIR  ?= $(REPO_ROOT)/test_data/test_dataset
LIMIT     ?= 2

DETERMINISM_ENV := PYTHONHASHSEED=0 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1

.PHONY: regression regression-capture regression-dryrun

# Exact-tier regression run (CI gate). Requires pytest in the env (issue #5).
regression:
	cd $(REPO_ROOT) && $(DETERMINISM_ENV) $(PY) -m pytest \
		tests/regression -m "not distribution and not tolerance" -q

# Capture golden baselines into the committed baselines/ dir (review before committing).
regression-capture:
	cd $(REPO_ROOT) && $(DETERMINISM_ENV) $(PY) \
		tests/regression/capture_baselines.py --data-dir $(DATA_DIR) --limit $(LIMIT)

# Dry-run capture to a scratch dir (does not touch committed baselines).
regression-dryrun:
	cd $(REPO_ROOT) && $(DETERMINISM_ENV) $(PY) \
		tests/regression/capture_baselines.py \
		--data-dir $(DATA_DIR) --limit $(LIMIT) --out-dir /tmp/regr_dryrun
