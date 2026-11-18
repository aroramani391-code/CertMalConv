# AGNNCert

**Reference.** J. Li, B. Wang, USENIX Sec. 2025
**Upstream URL.** https://github.com/YeChenAI/AGNNCert
**Status in this repository.** released implementation (R).
**Version.** v1.0
**Parameters.** 2.47 M (see Table XI).
**Preprocessing.** Radare2 5.8
**Category.** cert

## Hyperparameters used in the paper

Graph division k = 3

## Data splits

Uses the same splits, deduplication and calibration procedure as
CertMalConv — see `data/splits/standard/*.json` and
`configs/datasets/*.yaml`.  The calibration FPR is fixed at 0.1% to
match Table VII.

## How to run

```bash
python baselines/agnncert/run.py \
    --dataset bodmas \
    --config baselines/agnncert/config.yaml \
    --seed 42
```

Metrics are written to `results/baselines/agnncert/summary.csv`.

## License

See the upstream repository.  Where redistribution is not permitted
this folder provides installation instructions only; no source is
copied.
