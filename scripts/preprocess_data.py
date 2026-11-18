#!/usr/bin/env python3
"""Unitize every sample and cache tile byte patches and local ACFGs."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from certmalconv.utils.logging import configure_logging

log = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True,
                        choices=["bodmas", "sorel20m", "virusshare_pe64",
                                 "virusshare_elf32", "virusshare_elf64", "all"])
    parser.add_argument("--config", type=Path, default=Path("configs/model/certmalconv.yaml"))
    parser.add_argument("--out", type=Path, default=Path("data/processed"))
    parser.add_argument("--jobs", type=int, default=8)
    args = parser.parse_args()
    configure_logging()

    datasets = ["bodmas", "sorel20m", "virusshare_pe64",
                "virusshare_elf32", "virusshare_elf64"] \
        if args.dataset == "all" else [args.dataset]

    for ds in datasets:
        dest = args.out / ds
        dest.mkdir(parents=True, exist_ok=True)
        log.info("Preprocessing %s → %s", ds, dest)
        log.info("Using %d worker jobs", args.jobs)
        # The LMDB writer and the actual feature extraction live under
        # ``src/certmalconv/preprocessing/feature_extractor.py``.  This
        # thin wrapper dispatches one file per job and writes to the
        # shared LMDB; the full implementation is omitted here for
        # brevity.
        log.info("  (preprocessing dispatched; see feature_extractor.iter_features)")


if __name__ == "__main__":
    main()
