# Malformer

**Reference.** S. Howard et al., arXiv:2608.19052, 2026
**Upstream URL.** https://github.com/sam-malformer/malformer
**Status in this repository.** released implementation (R).
**Version.** v1.0
**Parameters.** 12.74 M (see Table XI).
**Preprocessing.** Radare2 5.8
**Category.** multi

## Hyperparameters used in the paper

Transformer; AdamW, lr 5e-5

## Data splits

Uses the same splits, deduplication and calibration procedure as
CertMalConv — see `data/splits/standard/*.json` and
`configs/datasets/*.yaml`.  The calibration FPR is fixed at 0.1% to
match Table VII.

## How to run

```bash
python baselines/malformer/run.py \
    --dataset bodmas \
    --config baselines/malformer/config.yaml \
    --seed 42
```

Metrics are written to `results/baselines/malformer/summary.csv`.

## License

See the upstream repository.  Where redistribution is not permitted
this folder provides installation instructions only; no source is
copied.
