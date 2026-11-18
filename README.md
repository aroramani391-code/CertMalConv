# CertMalConv

> Efficient and Certifiably Robust Deep Learning for Multi-modal Malware
> Detection and Classification

[![Tests](https://github.com/certmalconv/certmalconv/actions/workflows/tests.yml/badge.svg)](https://github.com/certmalconv/certmalconv/actions/workflows/tests.yml)
[![Reproducibility](https://github.com/certmalconv/certmalconv/actions/workflows/reproducibility.yml/badge.svg)](https://github.com/certmalconv/certmalconv/actions/workflows/reproducibility.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![PyTorch 2.3](https://img.shields.io/badge/PyTorch-2.3-ee4c2c.svg)](https://pytorch.org/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14258123.svg)](https://doi.org/10.5281/zenodo.14258123)

This repository contains the reference implementation, trained-model
checkpoints, verification harness and experimental scripts for CertMalConv, a
multi-modal malware detector whose malicious verdicts carry a deterministic
certificate against coupled byte-level and control-flow-graph edits.

## Research contributions

1. **Coupled perturbation model.** A unit edit distance over
   content-defined units turns a problem-space edit into a single quantity
   that bounds the change seen by every view the detector reads.
2. **Content-defined unitization.** A Gear rolling hash cuts a binary into
   variable-length units whose boundaries move with the content, so an edit
   disturbs only the units around it.
3. **Dual-view unit encoder.** Each unit is scored from its own bytes by a
   light CNN over a grayscale patch and a GIN over a local attributed
   control-flow graph (ACFG) recovered by per-tile linear sweep.
4. **Deterministic certificate.** Monotone top-*k* evidence aggregation
   turns the three properties above into a per-file certificate
   $\rho^\star(x)$ that survives unbounded insertion and up to
   $\rho^\star(x)$ altered units, computed in $O(m \log m)$ time.
5. **Open-set family attribution.** A family head reads the top-*k* unit
   embeddings and rejects unseen families with an energy threshold.

## System architecture

```
                   binary
                     │
                     ▼
     ┌─────────────────────────────────┐
     │   Content-defined unitization   │   Gear hash, ω = 64 B, ℓ = 11
     └─────────────────────────────────┘
                     │  u1, u2, ..., um
                     ▼
     ┌─────────────────────────────────┐
     │   Dual-view unit encoder        │   CNN (byte) + GIN (ACFG)
     │                                 │   gated fusion → unit evidence
     └─────────────────────────────────┘
          │                      │
          ▼                      ▼
 ┌────────────────────┐   ┌───────────────────┐
 │  Top-k aggregator  │   │  Global branch    │
 │  (certified path)  │   │  (recall)         │
 └────────────────────┘   └───────────────────┘
          │                      │
          └──────── OR ──────────┘
                   │
                   ▼
            verdict + certificate radius + family
```

## Headline results

| Metric | CertMalConv | DSMalConv [1] |
|---|---:|---:|
| F1 on BODMAS | **99.46%** | 99.70% |
| F1 on SOREL-20M | **99.16%** | 99.46% |
| F1 on VirusShare-ELF | **97.82%** | 98.06% |
| Certified detection at 2 edit sites | **86.74%** | n/a |
| Family macro-F1 (BODMAS) | **83.52%** | 81.37% |
| Unknown-family AUROC | **83.46%** | 78.63% |
| End-to-end GPU latency (early exit) | **0.458 s** | 2.558 s |

See Section VI of the paper and `results/` in this repository for the
complete tables.

## Technical stack

| Component | Version |
|---|---|
| Python | 3.11.6 |
| PyTorch | 2.3.1 |
| PyTorch Geometric | 2.5.3 |
| Capstone | 5.0.1 |
| NumPy | 1.26.4 |
| Pandas | 2.2.2 |
| scikit-learn | 1.5.0 |
| LIEF | 0.14.1 |
| matplotlib | 3.9.0 |
| CUDA | 12.1 |

## Hardware requirements

The reported experiments were run on:

- **GPU:** NVIDIA A100-SXM4 40 GB (CUDA 12.1, driver 535.86)
- **CPU:** Intel Xeon, 12 vCPUs, 2.20 GHz
- **RAM:** 83.5 GB
- **OS:** Ubuntu 22.04 LTS

A single A100 is sufficient to train every configuration reported in the
paper. The light CNN and GIN fit in under 2 GB of GPU memory per sample
batch.

## Installation

```bash
# 1. Clone
git clone https://github.com/certmalconv/certmalconv.git
cd certmalconv

# 2. Create environment (conda preferred for CUDA matching)
conda env create -f environment.yml
conda activate certmalconv

# 3. Install the package in editable mode
pip install -e .

# 4. Verify installation (runs the lightweight test suite; ~30 s)
pytest tests/ -q
```

A Dockerfile is provided for a fully pinned CUDA 12.1 environment:

```bash
docker build -t certmalconv:0.3.2 .
docker run --gpus all -it certmalconv:0.3.2 bash
```

## Dataset preparation

The datasets are **not** redistributed from this repository. See
[`data/README.md`](data/README.md) for lawful access instructions. The
manifests (SHA-256 hashes, split assignments, AVClass2 family labels)
are in `data/manifests/`, so a reviewer who obtains a dataset can
verify sample-level identity with:

```bash
python scripts/generate_manifests.py \
    --dataset bodmas \
    --root  /path/to/BODMAS \
    --verify-hashes
```

## Reproduction, in one command

```bash
make reproduce-all          # ≈ 56 h on one A100
```

For incremental reproduction:

```bash
make preprocess             # unitize every sample, cache tile embeddings
make train SEED=42          # a single-seed run
make evaluate               # Table VI, VII, X results
make verify-certificates    # Table XIV, 19,500 trials
make attack                 # Table IX and Table XV
make figures                # Fig. 6–14 PDFs
```

## Mapping manuscript results to scripts

| Paper location | Script | Output |
|---|---|---|
| Table V | `configs/model/certmalconv.yaml` | Configuration |
| Tables VI, VII, Fig. 6 | `experiments/01_detection/run.py` | `results/detection/` |
| Table VIII, Fig. 7 | `experiments/02_certified_robustness/run.py` | `results/certification/` |
| Table IX, Fig. 8 | `experiments/03_adversarial_attacks/run.py` | `results/attacks/` |
| Table X | `experiments/04_family_classification/run.py` | `results/family_classification/` |
| Table XI, Fig. 9 | `experiments/05_efficiency/run.py` | `results/efficiency/` |
| Table XII | `experiments/06_cross_platform_temporal/run.py` | `results/generalization/` |
| Table XIII, Fig. 10 | `experiments/07_ablation/run.py` | `results/ablation/` |
| Table XIV, Fig. 12 | `experiments/08_certificate_verification/run.py` | `results/certification/verify_*.csv` |
| Tables XV, XVI, Fig. 13 | `experiments/09_source_leakage/run.py` | `results/attacks/adaptive_*.csv` |
| Table XVII | `experiments/10_statistical_analysis/run.py` | `results/statistics/` |
| Table XVIII, Fig. 14 | `experiments/11_false_positive_calibration/run.py` | `results/calibration/` |
| Table XIX | `baselines/README.md` | Baseline configurations |

See [`docs/paper_to_code_mapping.md`](docs/paper_to_code_mapping.md) for
the full table.

## Pre-trained models

Checkpoints for all five seeds and all five dataset groups are hosted on
Zenodo:
<https://doi.org/10.5281/zenodo.14258123>. `scripts/download_checkpoints.py`
fetches them and verifies their SHA-256 hashes against
[`checkpoints/model_manifest.csv`](checkpoints/model_manifest.csv).

```bash
python scripts/download_checkpoints.py --target checkpoints/
```

## Citation

If you use this code or its results, please cite:

```bibtex
@article{certmalconv2026,
  title   = {Efficient and Certifiably Robust Deep Learning for Multi-modal
             Malware Detection and Classification},
  author  = {First A. Author and Second B. Author and Third C. Author},
  journal = {IEEE Transactions on Dependable and Secure Computing},
  year    = {2026},
  doi     = {10.1109/TDSC.2026.XXXXXXX}
}
```

A machine-readable record is in [`CITATION.cff`](CITATION.cff).

## License

Source code is released under the MIT License (see [`LICENSE`](LICENSE)).
The datasets remain under their respective original licenses (BODMAS,
SOREL-20M, VirusShare, SymLM). Do not redistribute any live binaries.

## Responsible disclosure

CertMalConv is a defensive research artifact. The adversarial samples
generated by `src/certmalconv/attacks/` are attacks against the models
shipped in this repository and against the re-implemented baselines.

