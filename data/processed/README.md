# Processed data cache

This folder is populated by `scripts/preprocess_data.py`. The structure
is:

```
data/processed/
├── bodmas/
│   ├── PE-32.lmdb/            # tile byte patches
│   ├── PE-32.graph.lmdb/      # local ACFGs
│   ├── PE-32.unit_index.csv   # (sha256, unit_offset, unit_length)
│   └── PE-32.stats.json
├── sorel20m/
│   └── ...
└── ...
```

Contents are **not** versioned — see `.gitignore`. The caches exist
only on the training machine. If you want to share them, upload them
to Zenodo or an institutional object store and point
`configs/datasets/<name>.yaml:cache_path` at the download location.

## Cache format

- **LMDB `*.lmdb/`** — key: `sha256:unit_index`, value: raw tile
  bytes (`T = 4096` bytes).
- **LMDB `*.graph.lmdb/`** — key: `sha256:unit_index`, value:
  pickled `torch_geometric.data.Data` with the 11-dim node attributes
  of MAGIC/DSMalConv.
- **`unit_index.csv`** — one row per unit; carries the file offset and
  length so the certificate verifier can locate units in the original
  binary without re-parsing.
- **`stats.json`** — number of samples, total units, mean unit length,
  mean tiles per unit, Gear-table SHA-256.

## Rebuilding the cache

```bash
python scripts/preprocess_data.py --dataset bodmas
```

Expected time on the reference A100 host:

| Dataset | Preprocess time |
|---|---|
| BODMAS (G1) | 2 h 05 min |
| SOREL-20M (G2) | 55 min |
| VirusShare PE-64 (G3) | 22 min |
| VirusShare ELF-32 (G4) | 48 min |
| VirusShare ELF-64 (G5) | 10 min |
| **All five groups** | **4 h 20 min** |
