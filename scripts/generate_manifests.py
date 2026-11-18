#!/usr/bin/env python3
"""Build per-sample manifests (SHA-256 + split assignment) from a dataset root."""

from __future__ import annotations

import argparse
import csv
import logging
from pathlib import Path

from certmalconv.preprocessing.byte_extractor import sha256_of

log = logging.getLogger(__name__)


def walk_binaries(root: Path) -> list[Path]:
    exts = {".exe", ".dll", ".sys", ".bin", ".elf", ""}
    return [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in exts]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True,
                        choices=["bodmas", "sorel20m", "virusshare_pe64",
                                 "virusshare_elf32", "virusshare_elf64", "all"])
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=Path("data/manifests"))
    parser.add_argument("--verify-hashes", action="store_true")
    parser.add_argument("--all", action="store_true",
                        help="Shorthand for --dataset all")
    args = parser.parse_args()

    datasets = ["bodmas", "sorel20m", "virusshare_pe64",
                "virusshare_elf32", "virusshare_elf64"] \
        if (args.dataset == "all" or args.all) else [args.dataset]

    for ds in datasets:
        root = args.root or Path(f"/data/{ds}")
        if not root.exists():
            log.warning("Root %s does not exist — skipping", root)
            continue

        out_csv = args.out / f"{ds}_manifest_live.csv"
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        with open(out_csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["path", "sha256"])
            for b in walk_binaries(root):
                try:
                    h = sha256_of(b)
                    w.writerow([str(b.relative_to(root)), h])
                except OSError:
                    log.exception("Failed on %s", b)
        log.info("Wrote %s", out_csv)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    main()
