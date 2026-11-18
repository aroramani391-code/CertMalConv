#!/usr/bin/env python3
"""Thin wrapper around the full 19,500-trial verification harness."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from certmalconv.certification.certificate_verifier import cli as verifier_cli

log = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=19500,
                        help="Total trials (CI: 500, paper: 19500).")
    parser.add_argument("--out", type=Path,
                        default=Path("results/certification/verifier_log.csv"))
    parser.add_argument("--seed", type=int, default=0)
    args, _ = parser.parse_known_args()
    import sys
    sys.argv = ["verify_certificates",
                "--trials", str(args.trials),
                "--out", str(args.out),
                "--seed", str(args.seed)]
    verifier_cli()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    main()
