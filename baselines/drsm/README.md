# DRSM

**Reference.** S. Saha et al., ICLR 2024
**Upstream URL.** https://github.com/UMBC-DREAM-Lab/DRSM
**Status in this repository.** released implementation (R).
**Version.** v1.0
**Parameters.** 1.14 M (see Table XI).
**Preprocessing.** None
**Category.** cert

## Hyperparameters used in the paper

Window 256 B, 50% ablation

## Data splits

Uses the same splits, deduplication and calibration procedure as
CertMalConv — see `data/splits/standard/*.json` and
`configs/datasets/*.yaml`.  The calibration FPR is fixed at 0.1% to
match Table VII.

## How to run

```bash
python baselines/drsm/run.py \
    --dataset bodmas \
    --config baselines/drsm/config.yaml \
    --seed 42
```

Metrics are written to `results/baselines/drsm/summary.csv`.

## License

See the upstream repository.  Where redistribution is not permitted
this folder provides installation instructions only; no source is
copied.
