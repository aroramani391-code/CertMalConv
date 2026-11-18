# MalGraph

**Reference.** X. Ling et al., INFOCOM 2022
**Upstream URL.** https://github.com/MalGraph-INFOCOM2022/MalGraph
**Status in this repository.** released implementation (R).
**Version.** v1.1
**Parameters.** 3.42 M (see Table XI).
**Preprocessing.** Ghidra 11.0
**Category.** graph

## Hyperparameters used in the paper

Default; AdamW, lr 2e-4

## Data splits

Uses the same splits, deduplication and calibration procedure as
CertMalConv — see `data/splits/standard/*.json` and
`configs/datasets/*.yaml`.  The calibration FPR is fixed at 0.1% to
match Table VII.

## How to run

```bash
python baselines/malgraph/run.py \
    --dataset bodmas \
    --config baselines/malgraph/config.yaml \
    --seed 42
```

Metrics are written to `results/baselines/malgraph/summary.csv`.

## License

See the upstream repository.  Where redistribution is not permitted
this folder provides installation instructions only; no source is
copied.
