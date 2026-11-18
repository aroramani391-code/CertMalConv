# MMCert

**Reference.** Y. Wang et al., CVPR 2024
**Upstream URL.** https://github.com/yangbaixiong/MMCert
**Status in this repository.** released implementation (R).
**Version.** v1.0
**Parameters.** 4.32 M (see Table XI).
**Preprocessing.** Radare2 5.8
**Category.** cert

## Hyperparameters used in the paper

Sub-sampling N = 200

## Data splits

Uses the same splits, deduplication and calibration procedure as
CertMalConv — see `data/splits/standard/*.json` and
`configs/datasets/*.yaml`.  The calibration FPR is fixed at 0.1% to
match Table VII.

## How to run

```bash
python baselines/mmcert/run.py \
    --dataset bodmas \
    --config baselines/mmcert/config.yaml \
    --seed 42
```

Metrics are written to `results/baselines/mmcert/summary.csv`.

## License

See the upstream repository.  Where redistribution is not permitted
this folder provides installation instructions only; no source is
copied.
