# Dataset Documentation

CertMalConv uses the five dataset groups of DSMalConv so that results
are directly comparable. This document records the source of every
split, the preprocessing steps, and the legal conditions under which
samples may be obtained.

## Dataset groups

| Group | Platform | Malware source | Benign source | After dedup (M / B) |
|---|---|---|---|---|
| G1 | PE-32 | BODMAS [26] | Windows installations, public repos | 19,842 / 22,415 |
| G2 | PE-32 | SOREL-20M [24] | Windows installations, public repos | 7,513 / 9,647 |
| G3 | PE-64 | VirusShare [30] | Windows installations, public repos | 3,872 / 4,881 |
| G4 | ELF-32 | VirusShare [30] | SymLM [31] corpus | 7,618 / 10,712 |
| G5 | ELF-64 | VirusShare [30] | SymLM [31] corpus | 1,154 / 1,168 |
| Total | | | | 39,999 / 48,823 |

## Split protocol

The standard split is **70 / 15 / 15** stratified by label. 5% of the
training benign files are held out as `D_cal` for threshold
calibration. Deduplication is in two stages: SHA-256 (removes exact
copies) and unit-multiset identity (removes files that differ only in
appended padding).

Three further splits support RQ4 and RQ6:

- **Temporal** (TESSERACT protocol): BODMAS malware ordered by
  first-seen month; training August 2019 – January 2020, validation
  February 2020, test March – September 2020. Benign files are split
  at random (no timestamps).
- **Platform**: train on three of PE-32, PE-64, ELF-32, ELF-64; test
  on the fourth.
- **Family**: BODMAS families with ≥ 20 training samples are *known*;
  all others are *unknown*.

Section VI-K adds leakage-control splits (Table XVI):

- Near-duplicate filter (TLSH ≤ 30, Jaccard ≥ 0.90).
- Family-aware (AVClass2 [58] whole-family assignment).
- Malware source held out (BODMAS, SOREL-20M, VirusShare).
- Benign source held out.
- Toolchain-artefact normalization.
- Common collection (MOTIF [59]).

## Obtaining the data

| Dataset | License | Access |
|---|---|---|
| BODMAS | Academic | <https://whyisyoung.github.io/BODMAS/> (request form) |
| SOREL-20M | Apache 2.0 | <https://github.com/sophos/SOREL-20M> |
| VirusShare | Restricted academic | <https://virusshare.com> (request form) |
| SymLM corpus | MIT | <https://github.com/OSUSecLab/SymLM> |
| EMBER-2024 | Elastic v2.0 | <https://github.com/elastic/ember> |
| MOTIF | CC-BY-SA | <https://github.com/boozallen/MOTIF> |

Live malware binaries are **not** redistributed from this repository.
Every evaluation sample is identified by SHA-256 in
`data/manifests/sample_hashes.csv` so a reviewer who holds a copy of
the raw dataset can verify sample-level identity before preprocessing.

## Manifests shipped with this repository

- `data/manifests/dataset_manifest.csv` — one row per retained sample
  (SHA-256, platform, label, family, source, collection month, split).
- `data/manifests/sample_hashes.csv` — SHA-256 only, for quick dedup
  verification without the full manifest.
- `data/manifests/train_manifest.csv`,
  `validation_manifest.csv`,
  `test_manifest.csv` — standard split assignments.
- `data/splits/temporal/*.json` — month-by-month lists for the
  temporal evaluation.
- `data/splits/family_aware/*.json` — AVClass2 family partition into
  train/test.
- `data/splits/source_held_out/*.json` — three held-out malware-source
  variants and the held-out benign-source variant.
- `data/splits/near_duplicate_filtered/*.json` — surviving test set
  after TLSH and Jaccard filtering.

## Preprocessing

`scripts/preprocess_data.py` applies, in order:

1. `pefile` / `pyelftools` sanity-parse (rejects malformed headers).
2. SHA-256 + unit-multiset dedup against training set.
3. Gear unitization (`ω = 64`, `ℓ = 11`, random `Γ` seeded by sample).
4. Per-tile linear sweep (x86-32 and x86-64) + local ACFG extraction.
5. Tile-level byte-image reshape (`64 × 64`).
6. Cache to an LMDB keyed by `(sha256, tile_index)`.

Preprocessing time: ~0.42 s/file median, 2.1 s/file 95th percentile.

## Responsible handling

- Malware samples live only on air-gapped infrastructure.
- Preprocessed caches contain byte patches and ACFG attributes, never
  executable code.
- Adversarial samples generated for Section VI-C are stored
  encrypted-at-rest and are not uploaded to any scanning service.
- All processing complies with the licenses listed above and with the
  responsible-use policies of the originating datasets.
