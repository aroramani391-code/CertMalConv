# Datasets

CertMalConv uses the five dataset groups of DSMalConv. Live binaries
are **not** redistributed from this repository; this folder holds the
manifests, split files and preprocessing scripts needed to rebuild the
caches locally from a lawful copy of each dataset.

## Layout

```
data/
├── manifests/      # SHA-256 provenance per sample
├── splits/         # train/val/test and leakage-control partitions
└── processed/      # local LMDB caches (not versioned)
```

See [`../docs/dataset_documentation.md`](../docs/dataset_documentation.md)
for dataset sources, licensing and counts.

## How to obtain the datasets

| Dataset | Access |
|---|---|
| BODMAS | request form at <https://whyisyoung.github.io/BODMAS/> |
| SOREL-20M | `aws s3 sync s3://sorel-20m/09-DEC-2020/binaries/` |
| VirusShare | request form at <https://virusshare.com> |
| SymLM corpus | <https://github.com/OSUSecLab/SymLM> |
| EMBER-2024 | <https://github.com/elastic/ember> (Elastic v2.0) |
| MOTIF | <https://github.com/boozallen/MOTIF> (CC-BY-SA) |

Once a copy is in place, point the corresponding environment variable
at it (see [`../docs/reproduction_guide.md`](../docs/reproduction_guide.md))
and run:

```bash
python scripts/generate_manifests.py --dataset bodmas --verify-hashes
python scripts/preprocess_data.py --dataset bodmas
```

The second command writes to `data/processed/bodmas/` (not versioned;
see `.gitignore`).

## Verifying sample-level identity

`sample_hashes.csv` lists the SHA-256 of every sample that was used in
the published experiments. Before running the pipeline on your own copy
of a dataset, confirm the hash set matches:

```bash
python scripts/verify_sample_hashes.py --dataset bodmas \
    --root $BODMAS_ROOT
```

The script prints the number of missing hashes (should be 0) and the
number of extra samples not used in the paper.

## Responsible handling

Do **not** commit raw malware binaries, API keys, or any
dataset-provider credentials. The `.gitignore` already excludes
`data/raw/` and `data/processed/*.lmdb`.
