# Reproduction Guide

This guide walks through the steps needed to independently reproduce
every table and figure of the paper from a clean checkout. Each step
lists its inputs, its outputs, and an expected wall-clock time on the
reference hardware (one NVIDIA A100-SXM4 40 GB).

## 0. Prerequisites

- An NVIDIA GPU with CUDA ≥ 12.1 and ≥ 16 GB of memory.
- 500 GB of free disk (preprocessed caches dominate).
- Access to the original datasets (see
  [`dataset_documentation.md`](dataset_documentation.md)).

## 1. Install (≈ 10 min)

```bash
git clone https://github.com/certmalconv/certmalconv.git
cd certmalconv
conda env create -f environment.yml
conda activate certmalconv
pip install -e ".[dev]"
pytest tests/ -q      # fast tests; must all pass
```

## 2. Download pre-trained checkpoints (≈ 25 min at 100 Mbit/s)

If you only want to reproduce evaluation tables and figures, skip
retraining:

```bash
python scripts/download_checkpoints.py --target checkpoints/
```

Hashes are verified against `checkpoints/model_manifest.csv`.

## 3. Prepare the data (≈ 4 h 20 min)

Point to the directory holding your copy of each dataset:

```bash
export BODMAS_ROOT=/data/bodmas
export SOREL_ROOT=/data/sorel20m
export VIRUSSHARE_ROOT=/data/virusshare
export SYMLM_ROOT=/data/symlm
export EMBER_ROOT=/data/ember2024

python scripts/generate_manifests.py --all
python scripts/preprocess_data.py --dataset all
```

Outputs:

- `data/manifests/*.csv` — provenance tables
- `data/processed/<dataset>/<platform>.lmdb` — per-unit byte patches,
  tile embeddings and local ACFGs.

## 4. Train (≈ 46 h for all 5 seeds × 5 groups)

```bash
make train-all-seeds DATASET=bodmas
make train-all-seeds DATASET=sorel20m
make train-all-seeds DATASET=virusshare_pe64
make train-all-seeds DATASET=virusshare_elf32
make train-all-seeds DATASET=virusshare_elf64
```

Alternatively, skip this step and reuse the downloaded checkpoints.

## 5. Detection, certification, attribution (≈ 1 h 40 min)

```bash
python scripts/evaluate_model.py --experiment detection          # Tables VI, VII
python scripts/evaluate_model.py --experiment certification      # Table VIII, Fig. 7
python scripts/evaluate_model.py --experiment family             # Table X
python scripts/evaluate_model.py --experiment efficiency         # Table XI, Fig. 9
python scripts/evaluate_model.py --experiment generalization     # Table XII
python scripts/evaluate_model.py --experiment ablation           # Table XIII, Fig. 10
```

Each run writes raw per-seed CSVs under `results/<experiment>/raw_*`
and an aggregate `summary.csv`.

## 6. Independent certificate verification (≈ 3 h)

```bash
python scripts/verify_certificates.py --trials 19500
```

Writes `results/certification/verifier_log.csv` with one row per
trial (input type, edit family, bound, observed, ratio, violated).

**Expected: 19,500 trials, 0 violations.** A single violation would
be a bug in either the implementation or the proof and must be
investigated before publication.

## 7. Attack suite (≈ 7 h 15 min)

```bash
python scripts/run_attacks.py --config configs/attacks/fgsm.yaml
python scripts/run_attacks.py --config configs/attacks/snia.yaml
python scripts/run_attacks.py --config configs/attacks/snica.yaml
python scripts/run_attacks.py --config configs/attacks/insertion.yaml
python scripts/run_attacks.py --config configs/attacks/rewriting.yaml
python scripts/run_attacks.py --config configs/attacks/tur.yaml
python scripts/run_attacks.py --config configs/attacks/tur_opt.yaml
```

Functionality is verified in-sandbox; only functionality-preserving
samples count as successes.

## 8. Statistical analysis (≈ 20 min)

```bash
python scripts/run_statistics.py     # Table XVII
```

## 9. Calibration and drift (≈ 45 min)

```bash
python scripts/run_calibration.py    # Table XVIII, Fig. 14
```

## 10. Regenerate tables and figures (≈ 5 min)

```bash
make tables        # writes results/<experiment>/table_*.tex
make figures       # writes figures/fig*/*.pdf
```

Every PDF in `figures/` is produced from CSV inputs in `results/`.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `torch_geometric` import error | CUDA mismatch | reinstall from the PyG wheel matching CUDA 12.1 |
| `capstone` crashes on an ELF sample | corrupt binary | sanity-parse logs in `logs/preprocess_*.log` |
| F1 differs > 0.3 points from paper | different split | confirm `data/splits/standard/*.json` matches the shipped hashes |
| CDR = 0 for all files | threshold mis-calibrated | re-run `scripts/calibrate_thresholds.py` |
| GPU OOM | batch size too large | override `batch_size: 8` in `configs/training/training_config.yaml` |

## Reproducibility status

Status of each result when this guide was last published is in
[`reproducibility_checklist.md`](reproducibility_checklist.md).
