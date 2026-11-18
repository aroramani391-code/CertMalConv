# Experiment 04_family_classification — Family classification and open-set rejection

Paper output: **Table X**.

## Reproduce

```bash
python experiments/04_family_classification/run.py --seed 42
# or all five seeds
python experiments/04_family_classification/run.py --seeds 42 123 2024 2025 2026
```

Outputs are written to `results/family_classification/`.

## Inputs

- Config: `experiments/04_family_classification/configs/run.yaml`
- Checkpoints: `checkpoints/certmalconv_<dataset>_seed<N>.pt`
- Dataset splits: `data/splits/standard/*.json`

## Metrics computed

- `family_metrics`
- `unknown_auroc`

## Logs

Each run appends to `experiments/04_family_classification/logs/run_seed<N>.log`.
