"""Specialised insertion bound (pure append; Lemma 2 last sentence).

Appending content after the last byte of ``x`` leaves every cut of the
original intact and therefore alters at most one unit (the last one).
The certificate therefore covers inserted content of **any** size.
"""

from __future__ import annotations

__all__ = ["bound_insertion"]


def bound_insertion(num_appends: int = 1) -> int:
    """Return the number of altered units for ``num_appends`` appends.

    Each append after the last byte alters at most the single last
    unit of ``x``.  Successive appends may extend the last unit further
    but never alter earlier units.
    """
    if num_appends < 0:
        raise ValueError("num_appends must be non-negative")
    return 1 if num_appends > 0 else 0
