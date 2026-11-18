# Experiment 05_efficiency — Latency, throughput, memory

Paper output: **Table XI, Fig. 9**.

## Reproduce

```bash
python experiments/05_efficiency/run.py --seed 42
# or all five seeds
python experiments/05_efficiency/run.py --seeds 42 123 2024 2025 2026
```

Outputs are written to `results/efficiency/`.

## Inputs

- Config: `experiments/05_efficiency/configs/run.yaml`
- Checkpoints: `checkpoints/certmalconv_<dataset>_seed<N>.pt`
- Dataset splits: `data/splits/standard/*.json`

## Metrics computed

- `latency_vs_size`
- `early_exit_speedup`

## Logs

Each run appends to `experiments/05_efficiency/logs/run_seed<N>.log`.
