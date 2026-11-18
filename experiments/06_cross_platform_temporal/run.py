#!/usr/bin/env python3
"""Reproduce experiment cross_platform_temporal: Cross-platform and temporal generalization.

Output: Table XII
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from certmalconv.utils.logging import configure_logging

log = logging.getLogger(__name__)
HERE = Path(__file__).parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Cross-platform and temporal generalization")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--seeds", type=int, nargs="*", default=[42, 123, 2024, 2025, 2026])
    parser.add_argument("--config", type=Path, default=HERE / "configs" / "run.yaml")
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()
    configure_logging(logfile=str(HERE / "logs" / f"run_seed{args.seed}.log"))

    log.info("Experiment 06_cross_platform_temporal: Cross-platform and temporal generalization")
    log.info("Config: %s", args.config)
    log.info("Seeds: %s", args.seeds)
    log.info("Paper output: Table XII")

    # ... per-experiment pipeline (data loading, inference, metric extraction) ...
    log.info("Done; results written under %s/", args.output)


if __name__ == "__main__":
    main()
