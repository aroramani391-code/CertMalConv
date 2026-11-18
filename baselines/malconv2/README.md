# MalConv2

**Reference.** E. Raff et al., AAAI 2021
**Upstream URL.** https://github.com/NeuromorphicComputationResearchProgram/MalConv2
**Status in this repository.** released implementation (R).
**Version.** v2.0
**Parameters.** 1.14 M (see Table XI).
**Preprocessing.** None
**Category.** byte

## Hyperparameters used in the paper

Default; AdamW, lr 1e-4, batch 16

## Data splits

Uses the same splits, deduplication and calibration procedure as
CertMalConv — see `data/splits/standard/*.json` and
`configs/datasets/*.yaml`.  The calibration FPR is fixed at 0.1% to
match Table VII.

## How to run

```bash
python baselines/malconv2/run.py \
    --dataset bodmas \
    --config baselines/malconv2/config.yaml \
    --seed 42
```

Metrics are written to `results/baselines/malconv2/summary.csv`.

## License

See the upstream repository.  Where redistribution is not permitted
this folder provides installation instructions only; no source is
copied.
