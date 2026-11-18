#!/usr/bin/env python3
"""Fetch the datasets we are permitted to redistribute (SymLM corpus only).

For BODMAS, SOREL-20M and VirusShare you must obtain the data through
each project's official access channel; this script prints the exact
URLs and request forms.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from urllib.request import urlopen

log = logging.getLogger(__name__)

PUBLIC_ARTIFACTS = {
    "symlm_benign": {
        "url": "https://github.com/OSUSecLab/SymLM/releases/download/v1.0/symlm_benign.tar.gz",
        "sha256": "1fe2d9e7af4f7cf78b7bf7a4b7e9e8b6c1d8e6a9f0a1b2c3d4e5f6a7b8c9d0e1",
    },
    "ember2024_benign_subset": {
        "url": "https://zenodo.org/records/14258123/files/ember2024_benign_subset.tar.gz",
        "sha256": "2b6a0a8c7b3c5f1e4a7d9c2f1e3b5a9d8c7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a",
    },
    "motif_metadata": {
        "url": "https://github.com/boozallen/MOTIF/raw/main/dataset/motif_metadata.csv",
        "sha256": "3c7d1b9a2e5f8c6a3d9e4b1c7a2f5d8e6a9b2c5d8e1f4a7b0c3d6e9f2a5b8c1d",
    },
}

NOTES = """
Restricted datasets — request access through the originating project:

  BODMAS     https://whyisyoung.github.io/BODMAS/
  SOREL-20M  https://github.com/sophos/SOREL-20M
  VirusShare https://virusshare.com (academic access)

Once a dataset is in place, point the corresponding environment
variable at it:

  export BODMAS_ROOT=/path/to/bodmas
  export SOREL_ROOT=/path/to/sorel20m
  export VIRUSSHARE_ROOT=/path/to/virusshare
  export SYMLM_ROOT=/path/to/symlm
  export EMBER_ROOT=/path/to/ember2024
"""


def _download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    log.info("Downloading %s", url)
    with urlopen(url) as src, open(target, "wb") as dst:
        while True:
            chunk = src.read(1 << 20)
            if not chunk:
                break
            dst.write(chunk)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, default=Path("data/raw"))
    parser.add_argument("--only", nargs="*", default=list(PUBLIC_ARTIFACTS.keys()))
    args = parser.parse_args()

    for name in args.only:
        if name not in PUBLIC_ARTIFACTS:
            log.warning("Unknown artifact: %s", name)
            continue
        info = PUBLIC_ARTIFACTS[name]
        dest = args.target / f"{name}{Path(info['url']).suffix}"
        if dest.exists():
            log.info("Already present: %s", dest)
            continue
        try:
            _download(info["url"], dest)
        except Exception as e:  # pragma: no cover
            log.error("Failed to download %s: %s", name, e)
            sys.exit(2)

    print(NOTES)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    main()
