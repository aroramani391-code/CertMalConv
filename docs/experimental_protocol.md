# Experimental Protocol

## Hardware

| Component | Value |
|---|---|
| GPU | NVIDIA A100-SXM4 40 GB |
| CUDA | 12.1 (driver 535.86) |
| CPU | Intel Xeon, 12 vCPUs @ 2.20 GHz |
| RAM | 83.5 GB |
| OS | Ubuntu 22.04 LTS |
| Disk | 2 TB NVMe for preprocessed caches |

## Software (pinned)

| Package | Version |
|---|---|
| Python | 3.11.6 |
| PyTorch | 2.3.1 (+cu121) |
| PyTorch Geometric | 2.5.3 |
| Capstone | 5.0.1 |
| LIEF | 0.14.1 |
| NumPy | 1.26.4 |
| scikit-learn | 1.5.0 |

The pinned set is in `environment.yml` and `requirements.txt`. Docker
image: `certmalconv:0.3.2`.

## Seeds

Every experiment is repeated with five seeds: **42, 123, 2024, 2025,
2026**. The same seed assignment is used for the paired statistical
tests of Table XVII.

## Training schedule

| Setting | Value |
|---|---|
| Optimizer | AdamW |
| Learning rate | 1e-4 |
| Weight decay | 5e-4 |
| Batch size | 16 files |
| Epochs | 60, early stopping patience 10 |
| Warm-up (ρ ramp start) | 5 epochs |
| Ramp length | 25 epochs |
| ρ_max | 8 |
| k | 3 |
| θ_0 | 1.5 (= k / 2) |
| m (margin) | 0.1 |
| r (random units per file in mining) | 8 |
| λ_1 (global branch weight) | 0.5 |
| λ_2 (family head weight) | 0.3 |
| γ_f (focal) | 2 |
| α_1 = α_2 | 0.05 % |

Checkpoints are saved every epoch; the one with the highest validation
`CDR` at `ρ_max` is kept.

## Evaluation protocol

For every (model, split, seed) triple we report:

- **Detection**: ACC, precision, recall, F1, balanced accuracy at 1%
  and 0.1% FPR, AUC.
- **Certification**: `CDR(ρ)` for `ρ ∈ {0, …, 15}`, median
  `s_δ*(x)` at `δ = 5` B.
- **Attacks**: ASR per attack from Table IX, and per-branch ASR in
  Table XV.
- **Family**: closed-set accuracy, macro-F1, unknown-family AUROC,
  known-family TPR at the energy threshold.
- **Efficiency**: preprocessing time, GPU and CPU inference time,
  peak memory, parameter count.

All five-seed raw results are kept in `results/*/raw_*.csv` so means,
standard deviations and bootstrap confidence intervals can be
recomputed independently of our aggregation code.

## Statistical tests (Section VI-L)

- Paired t-test over five seeds (4 df).
- McNemar on per-file test predictions per seed.
- Stratified bootstrap over the test set (10,000 resamples) for F1.
- Family-wise correction: Holm–Bonferroni over six comparisons.

## Logging

- **TensorBoard**: per-epoch scalars under `logs/<run>/events.out.*`.
- **Weights & Biases** (optional): run id and git SHA recorded in
  `results/<experiment>/wandb_run_ids.csv`.
- **Training JSON logs**: `logs/train_<dataset>_seed<N>.log` (one line
  per epoch with F1, CDR, θ, θ_g).

## Reproduction entry points

| Goal | Command |
|---|---|
| Single-seed training | `make train SEED=42 DATASET=bodmas` |
| All five seeds | `make train-all-seeds DATASET=bodmas` |
| Detection tables | `make evaluate` |
| Verification harness | `make verify-certificates` |
| Full attack suite | `make attack` |
| Figures | `make figures` |
| Full repro | `make reproduce-all` |

Expected wall clock on one A100:

| Stage | Time |
|---|---|
| Preprocess (all 5 groups) | 4 h 20 min |
| Train (1 seed, 1 group) | 3 h 10 min |
| Train (5 seeds × 5 groups) | 46 h |
| Evaluate + certify | 1 h 40 min |
| Attack suite | 7 h 15 min |
| **Total `make reproduce-all`** | **~ 56 h** |
