"""Edit-locality bound (Lemma 2) and edit-site radius (Corollary 1).

The companion computations in this module operate purely on cut
positions and never touch the model.  This makes them trivial to unit
test.
"""

from __future__ import annotations

from typing import Iterable

from certmalconv.unitization.gear_hash import (
    DEFAULT_WINDOW,
    max_cuts_in_window as _max_cuts_in_window,
)

__all__ = [
    "max_cuts_in_window",
    "edit_locality_bound",
    "edit_site_radius",
]


def max_cuts_in_window(cuts: Iterable[int], width: int) -> int:
    """Lemma 3 (ii).  Width is in positions (``δ + ω − 1``)."""
    return _max_cuts_in_window(list(cuts), width)


def edit_locality_bound(
    cuts: Iterable[int],
    edits: Iterable[tuple[int, int]],
    *,
    window: int = DEFAULT_WINDOW,
    file_size: int | None = None,
) -> int:
    """Lemma 2.  Maximum number of units of ``x`` that can be altered.

    Parameters
    ----------
    cuts
        Cut positions of the **original** file (in file order).
    edits
        Iterable of ``(a, b)`` pairs; edit ``i`` replaces
        ``x[a_i : b_i + 1]`` with arbitrary content (``b < a`` denotes a
        pure insertion at position ``a``).
    window
        Gear window ``ω`` (defaults to 64).
    file_size
        Optional length of ``x``.  When provided, an append after the
        last byte is counted as altering only the last unit.
    """
    cuts = sorted(cuts)
    bound = 0
    for a, b in edits:
        if file_size is not None and a >= file_size:
            # pure append
            bound += 1
            continue
        delta = max(b - a + 1, 0)
        width = delta + window - 1
        # zone is [a, b + ω − 1]; count cuts of x in that zone
        zone_lo, zone_hi = a, b + window - 1
        zone_cuts = sum(1 for c in cuts if zone_lo <= c <= zone_hi)
        bound += 1 + zone_cuts
    return bound


def edit_site_radius(
    cuts: Iterable[int],
    rho_star: int,
    *,
    delta: int,
    window: int = DEFAULT_WINDOW,
) -> int:
    """Eq. (10): ``s_δ*(x) = ⌊ ρ*(x) / (1 + c_ω^δ(x)) ⌋``.

    ``δ = 0`` corresponds to pure insertion.
    """
    if rho_star < 0:
        return 0
    c = max_cuts_in_window(cuts, delta + window - 1)
    return rho_star // (1 + c)
