# RS-Del

**Reference.** Z. Huang et al., NeurIPS 2023
**Upstream URL.** https://github.com/dovermore/rs-del
**Status in this repository.** released implementation (R).
**Version.** v1.0
**Parameters.** 1.14 M (see Table XI).
**Preprocessing.** None
**Category.** cert

## Hyperparameters used in the paper

Deletion p = 0.95, 100 draws

## Data splits

Uses the same splits, deduplication and calibration procedure as
CertMalConv — see `data/splits/standard/*.json` and
`configs/datasets/*.yaml`.  The calibration FPR is fixed at 0.1% to
match Table VII.

## How to run

```bash
python baselines/rs_del/run.py \
    --dataset bodmas \
    --config baselines/rs_del/config.yaml \
    --seed 42
```

Metrics are written to `results/baselines/rs_del/summary.csv`.

## License

See the upstream repository.  Where redistribution is not permitted
this folder provides installation instructions only; no source is
copied.
