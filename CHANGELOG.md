# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Nothing yet.

## [0.3.2] — 2026-11-02

### Added
- `scripts/download_checkpoints.py` for pulling pre-trained weights from Zenodo.
- Family-aware split manifests in `data/splits/family_aware/`.
- Reproducibility checklist in `docs/reproducibility_checklist.md`.

### Changed
- Pinned `torch==2.3.1` and `torch-geometric==2.5.3` in `requirements.txt`
  to match the hardware reported in the paper.

### Fixed
- Off-by-one error in `certification/edit_distance.py` when the last unit
  has length exactly equal to the Gear window.

## [0.3.1] — 2026-09-14

### Added
- MOTIF and EMBER-2024 integrations for the leakage-control experiments
  of Section VI-K (Table XVI).
- Stratified bootstrap confidence intervals in
  `evaluation/statistical_tests.py` (Table XVII).

### Changed
- Energy threshold calibration now uses 95% TPR on the known-family
  validation subset, matching the paper.

## [0.3.0] — 2026-07-28

### Added
- Complete adaptive-attack suite (`attacks/tur.py`, `tur_opt.py`) with
  beam-search variant.
- Independent certificate-verification harness
  (`certification/certificate_verifier.py`) and reproducible 19,500-trial
  script (`experiments/08_certificate_verification/`).

### Changed
- Switched calibration from Gaussian tail to empirical quantiles
  (Proposition 2, union bound). Cuts calibration-FPR variance by ~40%.

## [0.2.1] — 2026-05-02

### Fixed
- Capstone decoding was reading past the tile boundary on 32-byte tail
  slices; introduced a bounded reader in `preprocessing/disassembler.py`.

## [0.2.0] — 2026-03-11

### Added
- Dual-mode (x86-32 and x86-64) linear-sweep decoder.
- ELF-32 and ELF-64 support via LIEF parser.
- Dataset manifests for G4 and G5.

## [0.1.0] — 2026-01-19

### Added
- Initial release accompanying the TDSC submission:
  content-defined unitization, dual-view encoder, monotone top-*k*
  certificate, global branch, open-set family head.
