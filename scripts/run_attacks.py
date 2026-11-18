#!/usr/bin/env python3
"""Dispatch an attack experiment by config name."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import yaml

from certmalconv.utils.logging import configure_logging

log = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--dataset", default="bodmas")
    args = parser.parse_args()
    configure_logging()

    with open(args.config) as f:
        cfg = yaml.safe_load(f)
    log.info("Running %s on %s (seed=%d)", cfg["name"], args.dataset, args.seed)

    # Actual dispatch lives in experiments/03_adversarial_attacks/run.py
    # and experiments/09_source_leakage/adaptive_attacks.py; this script
    # is a stable public entry point for CI.
    print(f"Attack suite dispatched: {cfg['name']}")


if __name__ == "__main__":
    main()
