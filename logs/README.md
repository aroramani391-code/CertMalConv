# Training and evaluation logs

Per-run text logs from the published experiments live here.  File name
convention:

```
logs/<experiment-id>_<dataset>_seed<N>.log
```

Each line follows the pattern

```
YYYY-MM-DD HH:MM:SS LEVEL    certmalconv.<module> | message
```

so `grep`-friendly queries work out of the box:

```bash
grep "val_cdr" logs/certmalconv_bodmas_seed42.log | tail
grep "Calibrated" logs/*.log
grep "Early stopping" logs/*.log | wc -l
```

## Training runs shipped with the release

| Dataset | Seeds |
|---|---|
| bodmas | 42, 123, 2024, 2025, 2026 |
| sorel20m | 42, 123, 2024, 2025, 2026 |
| virusshare_pe64 | 42, 123, 2024, 2025, 2026 |
| virusshare_elf32 | 42, 123, 2024, 2025, 2026 |
| virusshare_elf64 | 42, 123, 2024, 2025, 2026 |

Twenty-five training runs in total, matching the entries in
`checkpoints/model_manifest.csv`.

## TensorBoard event files

Not committed to the repository (see `.gitignore`).  They are
regenerated locally by `make train` and uploaded to Zenodo alongside
the checkpoint.
