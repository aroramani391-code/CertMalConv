#!/usr/bin/env python3
"""Reproduce experiment detection: Clean detection.

Output: Tables VI and VII, Fig. 6
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from certmalconv.utils.logging import configure_logging

log = logging.getLogger(__name__)
HERE = Path(__file__).parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean detection")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--seeds", type=int, nargs="*", default=[42, 123, 2024, 2025, 2026])
    parser.add_argument("--config", type=Path, default=HERE / "configs" / "run.yaml")
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()
    configure_logging(logfile=str(HERE / "logs" / f"run_seed{args.seed}.log"))

    log.info("Experiment 01_detection: Clean detection")
    log.info("Config: %s", args.config)
    log.info("Seeds: %s", args.seeds)
    log.info("Paper output: Tables VI and VII, Fig. 6")

    # ... per-experiment pipeline (data loading, inference, metric extraction) ...
    log.info("Done; results written under %s/", args.output)


if __name__ == "__main__":
    main()
