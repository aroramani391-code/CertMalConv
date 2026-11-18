#!/usr/bin/env python3
"""Pull pre-trained checkpoints from Zenodo and verify their SHA-256."""

from __future__ import annotations

import argparse
import csv
import logging
from pathlib import Path
from urllib.request import urlopen

from certmalconv.utils.checkpoint import sha256_of_file

log = logging.getLogger(__name__)

ZENODO_BASE = "https://zenodo.org/records/14258123/files/"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, default=Path("checkpoints"))
    parser.add_argument("--manifest", type=Path,
                        default=Path("checkpoints/model_manifest.csv"))
    args = parser.parse_args()
    args.target.mkdir(parents=True, exist_ok=True)

    with open(args.manifest) as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        ckpt_name = f"{row['model_id']}.pt"
        dest = args.target / ckpt_name
        if dest.exists():
            got = sha256_of_file(dest)
            if got == row["sha256"]:
                log.info("Already present and verified: %s", ckpt_name)
                continue
            log.warning("Hash mismatch at %s; re-downloading", dest)
        log.info("Fetching %s", ckpt_name)
        try:
            with urlopen(ZENODO_BASE + ckpt_name) as src, open(dest, "wb") as out:
                while True:
                    chunk = src.read(1 << 20)
                    if not chunk:
                        break
                    out.write(chunk)
        except Exception as e:  # pragma: no cover
            log.error("Failed to fetch %s: %s", ckpt_name, e)
            continue
        got = sha256_of_file(dest)
        if got != row["sha256"]:
            log.error("Hash mismatch after download: %s", ckpt_name)
        else:
            log.info("Verified %s (SHA-256 OK)", ckpt_name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    main()
