"""Tests for the local-rewrite bound (Corollary 1)."""

from __future__ import annotations

from certmalconv.certification.edit_distance import edit_site_radius


def test_edit_site_radius_positive():
    # ρ* = 6, no cuts in window → one edit site alters 1 unit
    cuts = []
    s = edit_site_radius(cuts, rho_star=6, delta=5, window=64)
    assert s == 6


def test_edit_site_radius_zero_when_not_detected():
    assert edit_site_radius([0, 100, 200], rho_star=-1, delta=5) == 0


def test_edit_site_radius_shrinks_with_dense_cuts():
    # Many cuts inside δ+ω-1 = 68 positions
    cuts = list(range(0, 1000, 10))  # every 10 bytes
    s = edit_site_radius(cuts, rho_star=6, delta=5, window=64)
    assert 0 <= s < 6   # dense cuts should reduce the radius

    # With no cuts the full radius survives
    s_clean = edit_site_radius([], rho_star=6, delta=5, window=64)
    assert s_clean == 6


def test_delta_zero_is_pure_insertion():
    cuts = [100, 500, 900]
    s = edit_site_radius(cuts, rho_star=4, delta=0)
    # δ=0: window = 63, which might contain 0 or 1 cut depending on placement
    assert s in (2, 4)
