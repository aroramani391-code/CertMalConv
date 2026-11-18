# Pre-trained checkpoints

This folder holds per-checkpoint metadata files (`<model_id>.json`)
and the authoritative manifest (`model_manifest.csv`). The actual
weights are **not** committed through Git — they live on Zenodo (DOI
`10.5281/zenodo.14258123`) and are fetched on demand by
`scripts/download_checkpoints.py`.

## Layout

```
checkpoints/
├── README.md
├── model_manifest.csv                   # authoritative list with SHA-256
├── certmalconv_bodmas_seed42.json       # per-checkpoint metadata
├── certmalconv_bodmas_seed123.json
├── …
```

## Manifest columns

| Field | Meaning |
|---|---|
| `model_id` | `certmalconv_<dataset>_seed<N>` |
| `dataset` | one of `bodmas`, `sorel20m`, `virusshare_pe64`, `virusshare_elf32`, `virusshare_elf64` |
| `platform` | PE-32, PE-64, ELF-32, ELF-64 |
| `seed` | one of 42, 123, 2024, 2025, 2026 |
| `epoch` | epoch of the selected checkpoint (chosen by validation `CDR` at `ρ_max`) |
| `sha256` | integrity hash of the `.pt` file on Zenodo |
| `config` | YAML path used at training time |
| `val_f1` | best validation F1 at the selected epoch |
| `val_cdr` | best validation certified detection rate at `ρ_max = 8` |

## Downloading

```bash
python scripts/download_checkpoints.py --target checkpoints/
```

The script fetches each `.pt` from Zenodo and verifies its SHA-256
against this manifest. Downloaded `.pt` files are ignored by Git.

## Reproducing from scratch

```bash
make train-all-seeds DATASET=bodmas
```

Each run writes its checkpoint to `logs/certmalconv_<dataset>_seed<N>/`
and registers the final SHA-256 next to the entry in
`model_manifest.csv`.
