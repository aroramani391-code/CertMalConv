# Experiment 02_certified_robustness — Certified robustness vs edit sites

Paper output: **Table VIII, Fig. 7**.

## Reproduce

```bash
python experiments/02_certified_robustness/run.py --seed 42
# or all five seeds
python experiments/02_certified_robustness/run.py --seeds 42 123 2024 2025 2026
```

Outputs are written to `results/certified_robustness/`.

## Inputs

- Config: `experiments/02_certified_robustness/configs/run.yaml`
- Checkpoints: `checkpoints/certmalconv_<dataset>_seed<N>.pt`
- Dataset splits: `data/splits/standard/*.json`

## Metrics computed

- `cdr_curves`
- `edit_site_radius`

## Logs

Each run appends to `experiments/02_certified_robustness/logs/run_seed<N>.log`.
