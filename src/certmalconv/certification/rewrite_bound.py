"""Local-rewrite bound (Corollary 1)."""

from __future__ import annotations

from typing import Iterable

from certmalconv.certification.edit_distance import edit_site_radius
from certmalconv.unitization.gear_hash import DEFAULT_WINDOW

__all__ = ["bound_rewrite"]


def bound_rewrite(
    cuts: Iterable[int],
    rho_star: int,
    *,
    delta: int,
    window: int = DEFAULT_WINDOW,
) -> int:
    """Return the number of ``δ``-byte rewrites the verdict withstands.

    Thin wrapper around :func:`edit_distance.edit_site_radius` for
    discoverability.
    """
    return edit_site_radius(cuts, rho_star, delta=delta, window=window)
