#!/usr/bin/env python3
"""End-to-end reproduction driver — runs every experiment in sequence."""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from pathlib import Path

log = logging.getLogger(__name__)

STEPS = [
    ("Preprocess",         ["python", "scripts/preprocess_data.py", "--dataset", "all"]),
    ("Train (seed=42)",    ["python", "scripts/train_model.py", "--seed", "42"]),
    ("Train (seed=123)",   ["python", "scripts/train_model.py", "--seed", "123"]),
    ("Train (seed=2024)",  ["python", "scripts/train_model.py", "--seed", "2024"]),
    ("Train (seed=2025)",  ["python", "scripts/train_model.py", "--seed", "2025"]),
    ("Train (seed=2026)",  ["python", "scripts/train_model.py", "--seed", "2026"]),
    ("Detection",          ["python", "scripts/evaluate_model.py", "--experiment", "detection"]),
    ("Certification",      ["python", "scripts/evaluate_model.py", "--experiment", "certification"]),
    ("Attacks (FGSM)",     ["python", "scripts/run_attacks.py", "--config", "configs/attacks/fgsm.yaml"]),
    ("Attacks (SNIA)",     ["python", "scripts/run_attacks.py", "--config", "configs/attacks/snia.yaml"]),
    ("Attacks (insertion)",["python", "scripts/run_attacks.py", "--config", "configs/attacks/insertion.yaml"]),
    ("Attacks (rewriting)",["python", "scripts/run_attacks.py", "--config", "configs/attacks/rewriting.yaml"]),
    ("Attacks (TUR)",      ["python", "scripts/run_attacks.py", "--config", "configs/attacks/tur.yaml"]),
    ("Family",             ["python", "scripts/evaluate_model.py", "--experiment", "family"]),
    ("Efficiency",         ["python", "scripts/evaluate_model.py", "--experiment", "efficiency"]),
    ("Generalization",     ["python", "scripts/evaluate_model.py", "--experiment", "generalization"]),
    ("Ablation",           ["python", "scripts/evaluate_model.py", "--experiment", "ablation"]),
    ("Verification",       ["python", "scripts/verify_certificates.py"]),
    ("Statistics",         ["python", "scripts/evaluate_model.py", "--experiment", "statistics"]),
    ("Calibration",        ["python", "scripts/evaluate_model.py", "--experiment", "calibration"]),
    ("Tables",             ["python", "scripts/generate_tables.py", "--all"]),
    ("Figures",            ["python", "scripts/generate_figures.py", "--all"]),
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, nargs="*", default=[42, 123, 2024, 2025, 2026])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    _ = args.seeds

    for name, cmd in STEPS:
        log.info("=== %s ===", name)
        if args.dry_run:
            print(" ".join(cmd))
            continue
        rc = subprocess.call(cmd)
        if rc != 0:
            log.error("Step %s failed with rc=%d", name, rc)
            sys.exit(rc)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    main()
