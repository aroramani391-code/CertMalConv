#!/usr/bin/env python3
"""Run the evaluation experiment identified by --experiment."""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from pathlib import Path

log = logging.getLogger(__name__)

EXP_DIRS = {
    "detection":         "experiments/01_detection",
    "certification":     "experiments/02_certified_robustness",
    "attacks":           "experiments/03_adversarial_attacks",
    "family":            "experiments/04_family_classification",
    "efficiency":        "experiments/05_efficiency",
    "generalization":    "experiments/06_cross_platform_temporal",
    "ablation":          "experiments/07_ablation",
    "verification":      "experiments/08_certificate_verification",
    "statistics":        "experiments/10_statistical_analysis",
    "calibration":       "experiments/11_false_positive_calibration",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", required=True, choices=list(EXP_DIRS.keys()))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    exp_dir = Path(EXP_DIRS[args.experiment])
    run_script = exp_dir / "run.py"
    if not run_script.exists():
        log.error("Experiment script not found: %s", run_script)
        sys.exit(2)
    cmd = [sys.executable, str(run_script), "--seed", str(args.seed)]
    log.info("Dispatching: %s", " ".join(cmd))
    sys.exit(subprocess.call(cmd))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
