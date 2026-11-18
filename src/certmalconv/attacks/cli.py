"""CLI entry point for the attack suite."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

log = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser("certmalconv-attack")
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--dataset", default="bodmas")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("results/attacks"))
    args = parser.parse_args()

    if not args.config.exists():
        log.error("Attack config not found: %s", args.config)
        sys.exit(2)

    log.info("Running %s against %s (seed=%d)", args.config.name, args.dataset, args.seed)
    print(f"Attack dispatch: config={args.config}, dataset={args.dataset}, seed={args.seed}")
    print(f"Outputs will be written to {args.output}/")


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.INFO)
    main()
