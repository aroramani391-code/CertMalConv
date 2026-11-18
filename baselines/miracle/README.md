# MIRACLE

**Reference.** I. Alam et al., DMKD 2025
**Upstream URL.** https://github.com/mirror-miracle/MIRACLE
**Status in this repository.** our re-implementation from the paper (I).
**Version.** v1.0
**Parameters.** 0.83 M (see Table XI).
**Preprocessing.** Image reshape
**Category.** image

## Hyperparameters used in the paper

Original paper; SGD, lr 5e-3

## Data splits

Uses the same splits, deduplication and calibration procedure as
CertMalConv — see `data/splits/standard/*.json` and
`configs/datasets/*.yaml`.  The calibration FPR is fixed at 0.1% to
match Table VII.

## How to run

```bash
python baselines/miracle/run.py \
    --dataset bodmas \
    --config baselines/miracle/config.yaml \
    --seed 42
```

Metrics are written to `results/baselines/miracle/summary.csv`.

## License

See the upstream repository.  Where redistribution is not permitted
this folder provides installation instructions only; no source is
copied.
