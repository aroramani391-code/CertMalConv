# DSMalConv

**Reference.** Z. Li et al., IEEE TDSC 2026
**Upstream URL.** https://github.com/dsmalconv/dsmalconv
**Status in this repository.** released implementation (R).
**Version.** v1.0
**Parameters.** 4.18 M (see Table XI).
**Preprocessing.** Ghidra 11.0
**Category.** multi

## Hyperparameters used in the paper

Default DS weights, warm-up 3

## Data splits

Uses the same splits, deduplication and calibration procedure as
CertMalConv — see `data/splits/standard/*.json` and
`configs/datasets/*.yaml`.  The calibration FPR is fixed at 0.1% to
match Table VII.

## How to run

```bash
python baselines/dsmalconv/run.py \
    --dataset bodmas \
    --config baselines/dsmalconv/config.yaml \
    --seed 42
```

Metrics are written to `results/baselines/dsmalconv/summary.csv`.

## License

See the upstream repository.  Where redistribution is not permitted
this folder provides installation instructions only; no source is
copied.
