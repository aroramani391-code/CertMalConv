# CertMalConv Architecture

This document describes the full data-flow of CertMalConv from an input
executable to a verdict, a certified radius, and a family label. It is the
authoritative source for how the modules in `src/certmalconv/` fit together;
every step maps to a numbered equation from Section III of the paper.

## 1. End-to-end pipeline

```
  binary x  (n bytes)
       │
       ▼                                          Section III-B, Eq. (1)–(2)
  Content-defined unitization
    - Gear rolling hash (ω = 64 B)
    - cut bits ℓ = 11 (mean unit 2 KiB)
    - no min/max size, constant-run guard
       │
       ▼  u1, u2, …, um   (variable-length byte units)
  Per-unit tiling
    - T = 4096 B → 64 × 64 grayscale patch
    - alignment to the first byte of u
       │
       ▼
  Dual-view unit encoder                           Section III-C, Eq. (3)–(7)
    - Byte view:  CNN f_C (3 blocks, GAP, d=128)   Eq. (3)
    - Structure:  two linear-sweep decoders (x86-32, x86-64)
                  + GIN (L = 4, 32→64→128)         Eq. (4)–(5)
    - Fusion:     element-wise gate                Eq. (6)
    - Evidence:   max over tiles, linear head      Eq. (7)
       │                        │
       ▼                        ▼
  Top-k aggregator     Global branch                Section III-D, III-E
    - S_k(x) = Σ e_(j)     - gated attention       Eq. (8), (11)
    - threshold θ          - threshold θ_g
       │                        │
       ▼                        ▼
  Certified verdict     Uncertified verdict         Eq. (9), (12)
    - ρ*(x) from tail sums
    - s*(x) from edit sites
       │                        │
       └────────── OR ──────────┘
                   │
                   ▼
  Family head on top-k unit embeddings              Section III-F, Eq. (13)–(14)
    - softmax over C known families
    - energy threshold η for unknown rejection
                   │
                   ▼
          y, ρ*, s*, c
```

## 2. Module map

| Pipeline stage | Source file | Class/function |
|---|---|---|
| Unitization | `src/certmalconv/unitization/gear_hash.py` | `GearRollingHash`, `cut_positions` |
| Unit assembly | `src/certmalconv/unitization/content_defined_chunking.py` | `unitize` |
| Linear-sweep | `src/certmalconv/preprocessing/disassembler.py` | `LinearSweepDecoder` |
| Local ACFG | `src/certmalconv/preprocessing/cfg_extractor.py` | `extract_local_acfg` |
| Byte-view CNN | `src/certmalconv/models/byte_encoder.py` | `ByteEncoder` |
| Structure GIN | `src/certmalconv/models/structure_encoder.py` | `StructureEncoder` |
| Gated fusion | `src/certmalconv/models/fusion.py` | `GatedFusion` |
| Top-k aggregator | `src/certmalconv/certification/certificate.py` | `top_k_aggregate` |
| Certified radius | `src/certmalconv/certification/certificate.py` | `certified_radius` |
| Edit-site bound | `src/certmalconv/certification/edit_distance.py` | `edit_site_radius` |
| Insertion bound | `src/certmalconv/certification/insertion_bound.py` | `bound_insertion` |
| Rewrite bound | `src/certmalconv/certification/rewrite_bound.py` | `bound_rewrite` |
| Unit survival check | `src/certmalconv/certification/unit_survival.py` | `surviving_units` |
| Global branch | `src/certmalconv/models/global_branch.py` | `GlobalBranch` |
| Family head | `src/certmalconv/models/family_head.py` | `FamilyHead` |

## 3. Invariants maintained across modules

1. **Unit isolation (Lemma 1).** No tensor computed from `u_i` ever reads a
   file offset, a header byte, or the bytes of `u_{i±1}`.
2. **Monotonicity of top-k (Section III-D).** Adding evidences to the
   multiset can only raise the top-k sum; the certificate code relies on
   this at line `certification/certificate.py:98`.
3. **Decoder determinism.** `LinearSweepDecoder` is pure — no random
   initialization, no cache state. The verification harness
   `tests/test_reproducibility.py::test_disassembler_bitwise` enforces
   this by decoding the same tile under five seeds and comparing basic
   blocks.
4. **Evidence invariance.** Where a unit survives an edit, its evidence
   after the edit is bit-identical. `tests/test_unit_survival.py`
   enforces this across the full test split.

## 4. Operational configuration

The operational configuration reported in the paper (Table V) is:

```
ω               = 64 B     # Gear window
ℓ               = 11        # mean unit 2 KiB
T               = 4096 B    # 64 × 64 byte patch
k               = 3         # top-k aggregation
ρ_max           = 8         # training radius target
θ_0             = k / 2     # training threshold anchor
m               = 0.1       # training margin
α_1 = α_2       = 0.05 %    # per-branch FPR budget (Eq. 19)
d               = 128       # fusion dimension
L               = 4         # GIN layers
seeds           = 42, 123, 2024, 2025, 2026
```

These values live in `configs/model/certmalconv.yaml` and are loaded by
Hydra at every entry point. Do not hard-code them elsewhere.
