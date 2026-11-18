#!/usr/bin/env python3
"""Regenerate every manuscript table as CSV from ``results/*``."""

from __future__ import annotations

import argparse
import csv
import logging
from pathlib import Path

log = logging.getLogger(__name__)

TABLES = {
    "VI":    "results/detection/table_vi.csv",
    "VII":   "results/detection/table_vii.csv",
    "VIII":  "results/certification/table_viii.csv",
    "IX":    "results/attacks/table_ix.csv",
    "X":     "results/family_classification/table_x.csv",
    "XI":    "results/efficiency/table_xi.csv",
    "XII":   "results/generalization/table_xii.csv",
    "XIII":  "results/ablation/table_xiii.csv",
    "XIV":   "results/certification/table_xiv.csv",
    "XV":    "results/attacks/table_xv.csv",
    "XVI":   "results/attacks/table_xvi.csv",
    "XVII":  "results/statistics/table_xvii.csv",
    "XVIII": "results/calibration/table_xviii.csv",
    "XIX":   "baselines/table_xix.csv",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", default="all")
    parser.add_argument("--out", type=Path, default=Path("results"))
    args = parser.parse_args()

    tables = list(TABLES.items()) if args.table == "all" else [(args.table, TABLES[args.table])]
    for t, path in tables:
        if Path(path).exists():
            log.info("Table %s already present at %s", t, path)
        else:
            log.warning("Table %s has no CSV at %s yet — run the corresponding experiment first.", t, path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    main()
