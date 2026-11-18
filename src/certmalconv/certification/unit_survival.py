"""Unit survival verification (Lemma 1, operational check).

Given two unitizations ``U(x)`` and ``U(x')``, identify the units of
``x`` that survive into ``x'`` and assert their evidences match
bit-for-bit.  This is a runtime safety net in the verification harness
of Section VI-I.
"""

from __future__ import annotations

from typing import Sequence

from certmalconv.unitization.content_defined_chunking import Unit

__all__ = ["surviving_units", "assert_evidence_invariant"]


def surviving_units(
    u_x: Sequence[Unit],
    u_x_prime: Sequence[Unit],
) -> list[Unit]:
    """Multiset intersection of ``U(x) ∩ U(x')`` keyed by raw bytes."""
    counts: dict[bytes, int] = {}
    for u in u_x_prime:
        counts[u.data] = counts.get(u.data, 0) + 1
    survivors: list[Unit] = []
    for u in u_x:
        if counts.get(u.data, 0) > 0:
            survivors.append(u)
            counts[u.data] -= 1
    return survivors


def assert_evidence_invariant(
    survivors_before: dict[int, float],
    survivors_after: dict[int, float],
    *,
    atol: float = 0.0,
) -> None:
    """Assert bit-identical evidences across surviving units.

    Parameters
    ----------
    survivors_before, survivors_after
        Maps ``unit_index → evidence`` for the surviving units.
    atol
        Absolute tolerance — must be ``0.0`` for the formal invariant.
        A non-zero value is only meaningful when evidences are stored
        in reduced-precision format on disk.
    """
    missing = set(survivors_before) - set(survivors_after)
    if missing:
        raise AssertionError(f"Missing surviving units: {sorted(missing)[:10]} …")
    for idx, e_before in survivors_before.items():
        e_after = survivors_after[idx]
        if abs(e_before - e_after) > atol:
            raise AssertionError(
                f"Evidence changed for surviving unit {idx}: "
                f"{e_before} → {e_after} (Δ = {abs(e_before - e_after):.6e})"
            )
