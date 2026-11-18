# Reproducibility Checklist

Status of each result as of release **0.3.2** (2026-11-02). "Independently
regenerated" means the full pipeline was re-run from preprocessed caches
on a fresh A100 and matched the reported mean within one standard
deviation over five seeds.

| Paper item | Status | Notes |
|---|---|---|
| Table V (configuration) | ✅ complete | All values live in YAML, no hard-coded defaults |
| Table VI (clean detection) | ✅ independently regenerated | 5 seeds × 5 groups; mean within 0.07 F1 |
| Table VII (AUC and low-FPR) | ✅ independently regenerated | Low-FPR values require ≥ 3 seeds for stable CI |
| Table VIII (certified detection) | ✅ independently regenerated | CDR curves match to 0.3 points at every ρ |
| Table IX (attack success rates) | ⚠️ partially regenerated | Problem-space attacks require sandbox; `tests/` runs them on 1,000 samples |
| Table X (family classification) | ✅ independently regenerated | Energy threshold recalibrated per seed |
| Table XI (efficiency) | ✅ independently regenerated | Reported on the same A100; rerun on other hardware will differ |
| Table XII (generalization) | ✅ independently regenerated | AUT and cross-platform both within 0.4 F1 |
| Table XIII (ablation) | ✅ independently regenerated | All nine variants trained with the same seeds |
| Table XIV (certificate verification) | ✅ independently regenerated | 19,500 trials, 0 violations, log in `results/certification/verifier_log.csv` |
| Table XV (adaptive attacks) | ⚠️ partially regenerated | TUR-Opt beam-8 takes 4.5 h; CI runs beam-2 only |
| Table XVI (leakage controls) | ✅ independently regenerated | MOTIF experiment requires MOTIF access |
| Table XVII (statistical tests) | ✅ independently regenerated | Bootstrap CI reproducible with `--bootstrap-seed 0` |
| Table XVIII (calibration) | ✅ independently regenerated | EMBER-2024 requires license agreement |
| Table XIX (baseline configs) | ✅ complete | Every baseline has a README under `baselines/` |
| Fig. 5 (attack suite diagram) | ✅ complete | Static SVG, no data dependency |
| Fig. 6 (ROC) | ✅ independently regenerated | Script: `experiments/01_detection/plot_roc.py` |
| Fig. 7 (CDR curves) | ✅ independently regenerated | Script: `experiments/02_certified_robustness/plot_cdr.py` |
| Fig. 8 (ASR vs budget) | ⚠️ partially regenerated | Insertion and TUR panels only in CI |
| Fig. 9 (latency) | ✅ independently regenerated | Script: `experiments/05_efficiency/plot_latency.py` |
| Fig. 10 (ablation heatmap) | ✅ independently regenerated | Script: `experiments/07_ablation/plot_heatmap.py` |
| Fig. 11 (evidence localization) | ✅ independently regenerated | Case-study sample SHA-256 in fig script |
| Fig. 12 (verification scatter) | ✅ independently regenerated | Source: `results/certification/verifier_log.csv` |
| Fig. 13 (adaptive-attack ASR) | ⚠️ partially regenerated | TUR-Opt beam-8 required for full curve |
| Fig. 14 (temporal drift) | ✅ independently regenerated | Script: `experiments/11_false_positive_calibration/plot_drift.py` |

## Tests included in continuous integration

- Unit tests over Gear hash, unitization, encoder shapes, certificate
  arithmetic, insertion and rewrite bounds.
- Reproducibility test: deterministic unitization and bit-identical
  evidence on unaffected units.
- Short verification harness: 500 trials across all five input
  families (zero violations) — runs in CI.
- Lint (`ruff`) and types (`mypy`).

## Tests run only on demand

- Full 19,500-trial verification harness (~ 3 h; run before every
  release with `pytest --run-full`).
- TUR-Opt beam-8 adaptive attack (~ 4.5 h).
- Problem-space attack functionality checks in a live sandbox.

## Known reviewer frictions

1. **Restricted datasets.** BODMAS, SOREL-20M, VirusShare and MOTIF
   each require an access request. Our manifests include SHA-256
   hashes so a reviewer with access can verify they hold the same
   samples before training.
2. **Hardware-dependent timings.** Table XI assumes the A100 above.
   Relative speedups (5.32× end-to-end) are stable across hardware
   with similar memory bandwidth; absolute numbers will differ.
3. **Sandbox dependencies.** Table IX and Table XV require Cuckoo
   2.0.7 and an Ubuntu 22.04 guest image. Without them, the attack
   pipeline runs but cannot filter non-functional adversarial
   samples; ASR becomes an upper bound rather than a measurement.
