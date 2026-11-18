"""Tests for the top-k aggregator and certified radius (Eq. 8-9)."""

from __future__ import annotations

import numpy as np

from certmalconv.certification.certificate import (
    certified_radius,
    sorted_evidences,
    tail_sum,
    top_k_aggregate,
)


def test_sorted_evidences_descending():
    e = [0.2, 0.5, 0.1, 0.4]
    s = sorted_evidences(e)
    assert list(s) == [0.5, 0.4, 0.2, 0.1]


def test_top_k_padding_with_zero():
    assert top_k_aggregate([0.5, 0.1], k=4) == 0.5 + 0.1


def test_tail_sum_monotone_non_increasing():
    e = [0.9, 0.8, 0.5, 0.3, 0.2, 0.1]
    prev = float("inf")
    for rho in range(len(e)):
        t = tail_sum(e, k=3, rho=rho)
        assert t <= prev + 1e-12
        prev = t


def test_certified_radius_detected():
    # Evidences chosen so S_3 = 2.4, θ = 1.5
    e = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.1]
    out = certified_radius(e, k=3, theta=1.5)
    assert out.detected
    assert out.rho_star >= 0
    # Tail-sum at rho_star + 1 falls below theta
    assert tail_sum(e, k=3, rho=out.rho_star) >= 1.5
    assert tail_sum(e, k=3, rho=out.rho_star + 1) < 1.5


def test_certified_radius_not_detected():
    e = [0.1, 0.1, 0.1]
    out = certified_radius(e, k=3, theta=1.5)
    assert not out.detected
    assert out.rho_star == -1


def test_adding_units_cannot_lower_s_k():
    """Monotonicity of top-k under multiset insertion."""
    base = [0.9, 0.8, 0.5, 0.3]
    added = [0.9, 0.8, 0.5, 0.3, 0.0, 0.0, 0.0]
    assert top_k_aggregate(added, k=3) >= top_k_aggregate(base, k=3)


def test_certificate_output_shape():
    e = np.random.default_rng(0).uniform(0, 1, size=20).tolist()
    out = certified_radius(e, k=3, theta=0.5)
    assert out.tail_sums.ndim == 1
    assert out.tail_sums.size == len(e) - 3 + 1
