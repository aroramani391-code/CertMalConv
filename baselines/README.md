# Baselines

This folder holds the configuration, hyperparameters and runner for
every baseline compared against CertMalConv in the paper (Table IX,
Table XIX).

| Method | Code | Version | Par. (M) | Preprocessing |
|---|---|---|---:|---|
| [MalConv2](malconv2/) | R | v2.0 | 1.14 | None |
| [MIRACLE](miracle/) | I | v1.0 | 0.83 | Image reshape |
| [MalGraph](malgraph/) | R | v1.1 | 3.42 | Ghidra 11.0 |
| [Malformer](malformer/) | R | v1.0 | 12.74 | Radare2 5.8 |
| [DSMalConv](dsmalconv/) | R | v1.0 | 4.18 | Ghidra 11.0 |
| [DRSM](drsm/) | R | v1.0 | 1.14 | None |
| [DRS-Chunk (Gibert et al.)](drs_chunk/) | I | v1.0 | 1.14 | None |
| [RS-Del](rs_del/) | R | v1.0 | 1.14 | None |
| [AGNNCert](agnncert/) | R | v1.0 | 2.47 | Radare2 5.8 |
| [MMCert](mmcert/) | R | v1.0 | 4.32 | Radare2 5.8 |

- **R** = released implementation used as-is.
- **I** = our re-implementation from the paper.

All methods share the splits, deduplication, calibration procedure,
hardware and software of `configs/experiments/detection.yaml` and are
trained with the five canonical seeds (42, 123, 2024, 2025, 2026).

Respect third-party licenses: where redistribution is not permitted,
install from the upstream repository rather than copying source.
