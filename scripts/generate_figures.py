#!/usr/bin/env python3
"""Regenerate every manuscript figure from the CSVs in ``results/``.

Each figure has its own helper under ``experiments/*/plot_*.py``; this
script is a thin dispatcher.
"""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from pathlib import Path

log = logging.getLogger(__name__)

FIGURE_SCRIPTS = {
    5:  "scripts/draw_attack_suite.py",
    6:  "experiments/01_detection/plot_roc.py",
    7:  "experiments/02_certified_robustness/plot_cdr.py",
    8:  "experiments/03_adversarial_attacks/plot_asr.py",
    9:  "experiments/05_efficiency/plot_latency.py",
    10: "experiments/07_ablation/plot_heatmap.py",
    11: "experiments/07_ablation/plot_evidence.py",
    12: "experiments/08_certificate_verification/plot_verify.py",
    13: "experiments/09_source_leakage/plot_adaptive.py",
    14: "experiments/11_false_positive_calibration/plot_drift.py",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--figure", type=int, default=None, help="Figure number; omit with --all")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if args.all:
        figs = sorted(FIGURE_SCRIPTS.keys())
    elif args.figure is not None:
        figs = [args.figure]
    else:
        parser.error("Pass --figure N or --all")

    for n in figs:
        script = FIGURE_SCRIPTS.get(n)
        if script is None:
            log.warning("No regeneration script for Fig. %d", n)
            continue
        path = Path(script)
        if not path.exists():
            log.warning("Missing script for Fig. %d: %s", n, path)
            continue
        log.info("Regenerating Fig. %d via %s", n, script)
        subprocess.call([sys.executable, str(path)])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    main()
