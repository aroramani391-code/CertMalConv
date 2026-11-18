# Experiment 06_cross_platform_temporal — Cross-platform and temporal generalization

Paper output: **Table XII**.

## Reproduce

```bash
python experiments/06_cross_platform_temporal/run.py --seed 42
# or all five seeds
python experiments/06_cross_platform_temporal/run.py --seeds 42 123 2024 2025 2026
```

Outputs are written to `results/cross_platform_temporal/`.

## Inputs

- Config: `experiments/06_cross_platform_temporal/configs/run.yaml`
- Checkpoints: `checkpoints/certmalconv_<dataset>_seed<N>.pt`
- Dataset splits: `data/splits/standard/*.json`

## Metrics computed

- `held_out_f1`
- `monthly_f1`

## Logs

Each run appends to `experiments/06_cross_platform_temporal/logs/run_seed<N>.log`.
