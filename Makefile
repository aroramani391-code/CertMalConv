.PHONY: help install test lint format preprocess train evaluate verify-certificates attack figures reproduce-all clean

PYTHON   ?= python
SEEDS    ?= 42 123 2024 2025 2026
SEED     ?= 42
DATASET  ?= bodmas
EXP_DIR  ?= experiments

help:  ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-24s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Create the conda env and install the package in editable mode
	conda env create -f environment.yml
	conda run -n certmalconv pip install -e ".[dev]"

test:  ## Run the fast test suite
	$(PYTHON) -m pytest tests/ -q

test-full:  ## Run the full test suite including certificate verification
	$(PYTHON) -m pytest tests/ -q --run-full

lint:  ## Lint with ruff and mypy
	ruff check src/ tests/
	mypy src/certmalconv

format:  ## Auto-format with ruff and black
	ruff check --fix src/ tests/
	black src/ tests/

preprocess:  ## Unitize every sample and cache tile embeddings
	$(PYTHON) scripts/preprocess_data.py \
		--config configs/datasets/$(DATASET).yaml

train:  ## Train a single-seed CertMalConv model
	$(PYTHON) scripts/train_model.py \
		--config configs/training/training_config.yaml \
		--seed $(SEED)

train-all-seeds:  ## Train with all five seeds
	for s in $(SEEDS); do \
		$(PYTHON) scripts/train_model.py --seed $$s ; \
	done

evaluate:  ## Evaluate detection (Tables VI and VII)
	$(PYTHON) scripts/evaluate_model.py --experiment detection

verify-certificates:  ## Run the 19,500-trial verification harness (Table XIV)
	$(PYTHON) scripts/verify_certificates.py

attack:  ## Run the full attack suite (Tables IX and XV)
	$(PYTHON) scripts/run_attacks.py --config configs/attacks/tur.yaml
	$(PYTHON) scripts/run_attacks.py --config configs/attacks/tur_opt.yaml

figures:  ## Regenerate all manuscript figures
	$(PYTHON) scripts/generate_figures.py --all

tables:  ## Regenerate all manuscript tables as CSV
	$(PYTHON) scripts/generate_tables.py --all

reproduce-all:  ## Full end-to-end reproduction (≈ 56 h on one A100)
	$(PYTHON) scripts/run_all_experiments.py --seeds $(SEEDS)
	$(PYTHON) scripts/generate_tables.py --all
	$(PYTHON) scripts/generate_figures.py --all

clean:  ## Remove caches and build artefacts (leaves checkpoints alone)
	rm -rf build/ dist/ *.egg-info .pytest_cache .ruff_cache .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
