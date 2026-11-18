"""Monotone top-*k* aggregation and deterministic certified radius.

Implements Eq. (8)–(9) and Proposition 1 of the paper.  All functions
return plain Python / NumPy objects to make the certificate logic easy
to audit independently of PyTorch.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

__all__ = [
    "sorted_evidences",
    "top_k_aggregate",
    "tail_sum",
    "certified_radius",
    "CertificateOutput",
]


@dataclass(frozen=True)
class CertificateOutput:
    """Bundle returned by :func:`certified_radius`."""

    s_k: float                # Σ of the k largest evidences
    rho_star: int             # certified unit radius; -1 if file not flagged
    detected: bool            # ŷ_cert(x)
    tail_sums: np.ndarray     # T_rho for ρ = 0, …, |U(x)| − k


# ----------------------------------------------------------------------
# Internals
# ----------------------------------------------------------------------
def sorted_evidences(evidences: Sequence[float]) -> np.ndarray:
    """Return evidences sorted in **descending** order."""
    arr = np.asarray(evidences, dtype=np.float64)
    if arr.size == 0:
        return arr
    return np.sort(arr)[::-1]


def top_k_aggregate(evidences: Sequence[float], k: int) -> float:
    """Eq. (8): ``S_k(x) = Σ_{j=1..k} e_(j)``.

    If the file contains fewer than *k* units, the missing evidences
    count as zero (Section III-D).
    """
    e = sorted_evidences(evidences)
    if e.size == 0:
        return 0.0
    return float(e[:k].sum())


def tail_sum(evidences: Sequence[float], k: int, rho: int) -> float:
    """Eq. (9): ``T_ρ(x) = Σ_{j=ρ+1..ρ+k} e_(j)``.

    Values beyond the end of the sorted list are treated as zero.
    """
    e = sorted_evidences(evidences)
    if e.size == 0:
        return 0.0
    padded = np.concatenate([e, np.zeros(k, dtype=e.dtype)])
    return float(padded[rho : rho + k].sum())


def certified_radius(
    evidences: Sequence[float],
    *,
    k: int,
    theta: float,
) -> CertificateOutput:
    """Proposition 1: largest ρ such that ``T_ρ(x) ≥ θ``.

    Returns the full :class:`CertificateOutput`.  When the file is not
    flagged (``S_k < θ``), ``rho_star`` is set to ``-1`` by convention.
    """
    e = sorted_evidences(evidences)
    m = e.size
    s_k = float(e[:k].sum()) if m else 0.0
    detected = s_k >= theta

    # T_ρ for every ρ up to m - k (beyond that the top-k window has no
    # new elements to drop).
    max_rho = max(m - k, 0)
    tails = np.zeros(max_rho + 1, dtype=np.float64)
    for rho in range(max_rho + 1):
        tails[rho] = e[rho : rho + k].sum()

    if not detected:
        return CertificateOutput(s_k=s_k, rho_star=-1, detected=False, tail_sums=tails)

    # Largest ρ for which T_ρ ≥ θ.  T_ρ is non-increasing in ρ.
    valid = np.where(tails >= theta)[0]
    rho_star = int(valid.max()) if valid.size else 0
    return CertificateOutput(
        s_k=s_k,
        rho_star=rho_star,
        detected=True,
        tail_sums=tails,
    )
