# Experiment 03_adversarial_attacks — Attack success rates

Paper output: **Table IX, Fig. 8**.

## Reproduce

```bash
python experiments/03_adversarial_attacks/run.py --seed 42
# or all five seeds
python experiments/03_adversarial_attacks/run.py --seeds 42 123 2024 2025 2026
```

Outputs are written to `results/adversarial_attacks/`.

## Inputs

- Config: `experiments/03_adversarial_attacks/configs/run.yaml`
- Checkpoints: `checkpoints/certmalconv_<dataset>_seed<N>.pt`
- Dataset splits: `data/splits/standard/*.json`

## Metrics computed

- `asr_vs_budget`
- `per_attack_breakdown`

## Logs

Each run appends to `experiments/03_adversarial_attacks/logs/run_seed<N>.log`.
