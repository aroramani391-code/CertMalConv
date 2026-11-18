# Experiment 01_detection — Clean detection

Paper output: **Tables VI and VII, Fig. 6**.

## Reproduce

```bash
python experiments/01_detection/run.py --seed 42
# or all five seeds
python experiments/01_detection/run.py --seeds 42 123 2024 2025 2026
```

Outputs are written to `results/detection/`.

## Inputs

- Config: `experiments/01_detection/configs/run.yaml`
- Checkpoints: `checkpoints/certmalconv_<dataset>_seed<N>.pt`
- Dataset splits: `data/splits/standard/*.json`

## Metrics computed

- `detection_metrics`
- `roc_curves`

## Logs

Each run appends to `experiments/01_detection/logs/run_seed<N>.log`.
