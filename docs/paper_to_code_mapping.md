# Paper-to-Code Mapping

This document is the authoritative pointer from every table and figure
in the paper to the exact script, configuration, and output CSV that
produces it.

## Tables

| Paper | Topic | Config | Script | Output |
|---|---|---|---|---|
| V | Model hyper-parameters | `configs/model/certmalconv.yaml` | — | — |
| VI | Clean detection | `configs/experiments/detection.yaml` | `experiments/01_detection/run.py` | `results/detection/table_vi.csv` |
| VII | AUC and TPR at fixed FPR | `configs/experiments/detection.yaml` | `experiments/01_detection/run.py` | `results/detection/table_vii.csv` |
| VIII | Certified detection vs edit sites | `configs/experiments/certification.yaml` | `experiments/02_certified_robustness/run.py` | `results/certification/table_viii.csv` |
| IX | Attack success rates | `configs/experiments/attack_suite.yaml` | `experiments/03_adversarial_attacks/run.py` | `results/attacks/table_ix.csv` |
| X | Family classification | `configs/experiments/family_classification.yaml` | `experiments/04_family_classification/run.py` | `results/family_classification/table_x.csv` |
| XI | Efficiency | `configs/experiments/efficiency.yaml` | `experiments/05_efficiency/run.py` | `results/efficiency/table_xi.csv` |
| XII | Cross-platform and temporal | `configs/experiments/generalization.yaml` | `experiments/06_cross_platform_temporal/run.py` | `results/generalization/table_xii.csv` |
| XIII | Ablation on PE-32 | `configs/experiments/ablation.yaml` | `experiments/07_ablation/run.py` | `results/ablation/table_xiii.csv` |
| XIV | Certificate verification | `configs/experiments/verification.yaml` | `experiments/08_certificate_verification/run.py` | `results/certification/table_xiv.csv` |
| XV | Adaptive attacks by property | `configs/experiments/adaptive_attacks.yaml` | `experiments/09_source_leakage/adaptive_attacks.py` | `results/attacks/table_xv.csv` |
| XVI | Leakage controls | `configs/experiments/leakage_controls.yaml` | `experiments/09_source_leakage/run.py` | `results/attacks/table_xvi.csv` |
| XVII | Statistical comparison | `configs/experiments/statistics.yaml` | `experiments/10_statistical_analysis/run.py` | `results/statistics/table_xvii.csv` |
| XVIII | Calibration and drift | `configs/experiments/calibration.yaml` | `experiments/11_false_positive_calibration/run.py` | `results/calibration/table_xviii.csv` |
| XIX | Baseline sources and configs | `baselines/*/README.md` | `scripts/generate_baseline_table.py` | `baselines/table_xix.csv` |

## Figures

| Paper | Topic | Script | Output |
|---|---|---|---|
| Fig. 1 | Per-view vs problem-space edit | hand-drawn in Illustrator, SVG in `figures/fig01/` | `figures/fig01/fig01.pdf` |
| Fig. 2 | CertMalConv overview | hand-drawn SVG | `figures/fig02/fig02.pdf` |
| Fig. 3 | Locality of content-defined units | hand-drawn SVG | `figures/fig03/fig03.pdf` |
| Fig. 4 | Certified inference and training | hand-drawn SVG | `figures/fig04/fig04.pdf` |
| Fig. 5 | Attack suite | `scripts/draw_attack_suite.py` | `figures/fig05_attack_suite/fig05.pdf` |
| Fig. 6 | ROC curves (SOREL-20M) | `experiments/01_detection/plot_roc.py` | `figures/fig06_roc/fig06.pdf` |
| Fig. 7 | CDR vs unit radius | `experiments/02_certified_robustness/plot_cdr.py` | `figures/fig07_certified_robustness/fig07.pdf` |
| Fig. 8 | ASR vs attack budget | `experiments/03_adversarial_attacks/plot_asr.py` | `figures/fig08_attack_success/fig08.pdf` |
| Fig. 9 | Latency vs file size | `experiments/05_efficiency/plot_latency.py` | `figures/fig09_latency/fig09.pdf` |
| Fig. 10 | Ablation and sensitivity | `experiments/07_ablation/plot_heatmap.py` | `figures/fig10_ablation/fig10.pdf` |
| Fig. 11 | Evidence localization | `experiments/07_ablation/plot_evidence.py` | `figures/fig11_evidence_localization/fig11.pdf` |
| Fig. 12 | Certificate verification scatter | `experiments/08_certificate_verification/plot_verify.py` | `figures/fig12_certificate_verification/fig12.pdf` |
| Fig. 13 | Adaptive-attack ASR by branch | `experiments/09_source_leakage/plot_adaptive.py` | `figures/fig13_adaptive_attacks/fig13.pdf` |
| Fig. 14 | Monthly FPR / TPR drift | `experiments/11_false_positive_calibration/plot_drift.py` | `figures/fig14_temporal_drift/fig14.pdf` |

## Mathematical statements

| Paper | File | Function |
|---|---|---|
| Lemma 1 (Unit isolation) | `src/certmalconv/models/certmalconv.py` | `forward_units` |
| Lemma 2 (Edit locality) | `src/certmalconv/certification/edit_distance.py` | `edit_locality_bound` |
| Lemma 3 (Cut-density bound) | `src/certmalconv/certification/edit_distance.py` | `max_cuts_in_window` |
| Proposition 1 (Certified detection) | `src/certmalconv/certification/certificate.py` | `certified_radius` |
| Corollary 1 (Edit-site certificate) | `src/certmalconv/certification/edit_distance.py` | `edit_site_radius` |
| Remark 1 (Tightness) | `src/certmalconv/attacks/tur.py` | `TopUnitRewrite` |
| Proposition 2 (OR gate) | `src/certmalconv/models/certmalconv.py`, `training/calibration.py` | `decide`, `calibrate_quantile` |

## Equations

| Paper | File | Line |
|---|---|---|
| Eq. (1)–(2) Gear hash | `unitization/gear_hash.py` | 42–87 |
| Eq. (3) Byte view | `models/byte_encoder.py` | 31–74 |
| Eq. (4) GIN update | `models/gin.py` | 28–65 |
| Eq. (5) Structure embedding | `models/structure_encoder.py` | 88–112 |
| Eq. (6) Gated fusion | `models/fusion.py` | 24–48 |
| Eq. (7) Unit evidence | `models/fusion.py` | 56–70 |
| Eq. (8) Top-k decision | `certification/certificate.py` | 65–92 |
| Eq. (9) Tail sum and radius | `certification/certificate.py` | 98–135 |
| Eq. (10) Edit-site radius | `certification/edit_distance.py` | 71–104 |
| Eq. (11) Gated-attention global | `models/global_branch.py` | 36–82 |
| Eq. (12) OR gate | `models/certmalconv.py` | 141 |
| Eq. (13)–(14) Family head | `models/family_head.py` | 25–89 |
| Eq. (15) Certificate loss | `training/losses.py` | 32–71 |
| Eq. (16) Global + family loss | `training/losses.py` | 74–122 |
| Eq. (17) Total objective | `training/losses.py` | 125–140 |
| Eq. (18) Radius schedule | `training/train.py` | 118–132 |
| Eq. (19) Threshold calibration | `training/calibration.py` | 44–98 |
| Eq. (20) Balanced accuracy | `evaluation/detection_metrics.py` | 46–58 |
| Eq. (21) ASR | `evaluation/robustness_metrics.py` | 24–40 |
| Eq. (22) AUT | `evaluation/generalization.py` | 31–54 |
