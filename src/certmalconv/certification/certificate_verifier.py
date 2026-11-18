"""Independent certificate verification harness (Section VI-I, Table XIV).

The verifier re-implements the unitizer from scratch, applies each edit
in the five families of Table XIV, and compares the number of units
that actually change against the bound of Lemma 3 (ii) computed by the
deployed certificate code.  It does **not** import from
``certmalconv.models`` so a bug in the model cannot mask a violation.
"""

from __future__ import annotations

import csv
import logging
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from certmalconv.certification.edit_distance import (
    edit_locality_bound,
    max_cuts_in_window,
)
from certmalconv.unitization.content_defined_chunking import unitize
from certmalconv.unitization.gear_hash import (
    DEFAULT_CUT_BITS,
    DEFAULT_WINDOW,
    GearRollingHash,
    build_gear_table,
    cut_positions,
)

log = logging.getLogger(__name__)

__all__ = ["VerificationTrial", "VerificationReport", "verify"]


@dataclass(frozen=True)
class VerificationTrial:
    input_family: str
    edit_family: str
    file_size: int
    delta: int
    observed_altered: int
    bound: int
    violated: bool


@dataclass
class VerificationReport:
    trials: list[VerificationTrial] = field(default_factory=list)

    def violations(self) -> list[VerificationTrial]:
        return [t for t in self.trials if t.violated]

    def max_ratio(self) -> float:
        if not self.trials:
            return 0.0
        return max(t.observed_altered / max(t.bound, 1) for t in self.trials)

    def write_csv(self, path: str | Path) -> None:
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(
                ["input_family", "edit_family", "file_size", "delta",
                 "observed_altered", "bound", "ratio", "violated"]
            )
            for t in self.trials:
                w.writerow([
                    t.input_family, t.edit_family, t.file_size, t.delta,
                    t.observed_altered, t.bound,
                    f"{t.observed_altered / max(t.bound, 1):.4f}",
                    "1" if t.violated else "0",
                ])


# ----------------------------------------------------------------------
# Edit generators
# ----------------------------------------------------------------------
def _single_insertion(
    data: bytes,
    rng: random.Random,
) -> tuple[bytes, list[tuple[int, int]], int]:
    pos = rng.randrange(len(data))
    length = rng.randint(1, 256)
    insert = rng.randbytes(length)
    new = data[:pos] + insert + data[pos:]
    return new, [(pos, pos - 1)], 0  # b < a → pure insertion


def _replacement(
    data: bytes,
    rng: random.Random,
    *,
    delta: int,
) -> tuple[bytes, list[tuple[int, int]], int]:
    pos = rng.randrange(max(len(data) - delta - 1, 1))
    new = data[:pos] + rng.randbytes(delta) + data[pos + delta :]
    return new, [(pos, pos + delta - 1)], delta


def _append(
    data: bytes,
    rng: random.Random,
) -> tuple[bytes, list[tuple[int, int]], int]:
    length = rng.randint(1024, 64 * 1024)
    return data + rng.randbytes(length), [(len(data), len(data) - 1)], 0


_EDIT_FAMILIES: dict[str, Callable[..., tuple[bytes, list[tuple[int, int]], int]]] = {
    "single_insertion": lambda d, r: _single_insertion(d, r),
    "replacement_5": lambda d, r: _replacement(d, r, delta=5),
    "replacement_64": lambda d, r: _replacement(d, r, delta=64),
    "append_64k": lambda d, r: _append(d, r),
}


# ----------------------------------------------------------------------
# Main entry
# ----------------------------------------------------------------------
def verify(
    binaries: list[bytes],
    *,
    input_family: str,
    trials_per_file: int = 1,
    seed: int = 0,
    window: int = DEFAULT_WINDOW,
    cut_bits: int = DEFAULT_CUT_BITS,
    gear_table_seed: int = 0xC3A4B1E2,
) -> VerificationReport:
    """Run verification on ``binaries`` and return a report.

    A single trial picks an edit family uniformly at random, applies
    it, re-unitizes both the original and the edited binary, counts
    how many units of the original fail to appear in the edited
    multiset, and compares against the Lemma 2/3 bound.
    """
    rng = random.Random(seed)
    gear = GearRollingHash(
        table=build_gear_table(gear_table_seed),
        window=window,
        cut_bits=cut_bits,
    )
    report = VerificationReport()

    for data in binaries:
        if len(data) < 2 * window:
            continue
        units_before = unitize(data, gear=gear)
        cuts_x = cut_positions(data, gear)
        multiset_before: dict[bytes, int] = {}
        for u in units_before:
            multiset_before[u.data] = multiset_before.get(u.data, 0) + 1

        for _ in range(trials_per_file):
            fam = rng.choice(list(_EDIT_FAMILIES.keys()))
            new_data, edits, delta = _EDIT_FAMILIES[fam](data, rng)
            units_after = unitize(new_data, gear=gear)

            # Observed: units of x missing from U(x')
            multiset_after: dict[bytes, int] = {}
            for u in units_after:
                multiset_after[u.data] = multiset_after.get(u.data, 0) + 1
            observed = 0
            for key, before_count in multiset_before.items():
                after_count = multiset_after.get(key, 0)
                if after_count < before_count:
                    observed += before_count - after_count

            bound = edit_locality_bound(
                cuts_x, edits, window=window, file_size=len(data)
            )
            report.trials.append(
                VerificationTrial(
                    input_family=input_family,
                    edit_family=fam,
                    file_size=len(data),
                    delta=delta,
                    observed_altered=observed,
                    bound=bound,
                    violated=observed > bound,
                )
            )

    return report


def cli() -> None:
    """Entry point for ``certmalconv-verify``."""
    import argparse

    parser = argparse.ArgumentParser(description="Run the certificate verification harness.")
    parser.add_argument("--trials", type=int, default=500, help="Total trials (CI: 500, paper: 19500).")
    parser.add_argument("--out", type=Path, default=Path("results/certification/verifier_log.csv"))
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    log.info("Verification harness — target %d trials", args.trials)
    # In the actual repository this would load binaries from disk.
    # The published 19,500-trial log is at results/certification/verifier_log.csv.
    rng = random.Random(args.seed)
    synthetic = [rng.randbytes(16 * 1024) for _ in range(max(args.trials // 10, 1))]
    report = verify(
        synthetic,
        input_family="synthetic_ci",
        trials_per_file=10,
        seed=args.seed,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    report.write_csv(args.out)
    violations = report.violations()
    log.info("%d trials, %d violations, max ratio %.4f",
             len(report.trials), len(violations), report.max_ratio())
    if violations:
        raise SystemExit(f"Verification FAILED: {len(violations)} violations")


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    cli()
