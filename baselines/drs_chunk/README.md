# DRS-Chunk (Gibert et al.)

**Reference.** D. Gibert et al., arXiv:2405.00392, 2024
**Upstream URL.** https://github.com/danielgibert/drs-chunk
**Status in this repository.** our re-implementation from the paper (I).
**Version.** v1.0
**Parameters.** 1.14 M (see Table XI).
**Preprocessing.** None
**Category.** cert

## Hyperparameters used in the paper

Chunk 256 B, votes = 15

## Data splits

Uses the same splits, deduplication and calibration procedure as
CertMalConv — see `data/splits/standard/*.json` and
`configs/datasets/*.yaml`.  The calibration FPR is fixed at 0.1% to
match Table VII.

## How to run

```bash
python baselines/drs_chunk/run.py \
    --dataset bodmas \
    --config baselines/drs_chunk/config.yaml \
    --seed 42
```

Metrics are written to `results/baselines/drs_chunk/summary.csv`.

## License

See the upstream repository.  Where redistribution is not permitted
this folder provides installation instructions only; no source is
copied.
