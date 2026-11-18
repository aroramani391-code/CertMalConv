"""Tests for the Gear rolling hash (Eq. 1)."""

from __future__ import annotations

import pytest

from certmalconv.unitization.gear_hash import (
    GearRollingHash,
    build_gear_table,
    cut_positions,
    max_cuts_in_window,
)


def test_table_is_strictly_positive():
    table = build_gear_table(seed=0)
    assert (table > 0).all()


def test_constant_run_does_not_cut(default_gear):
    """A run of zero bytes must not trigger a cut on every byte."""
    data = b"\x00" * 1024
    cuts = cut_positions(data, default_gear)
    # only the forced terminal cut at n-1
    assert cuts == [len(data) - 1]


def test_cut_rate_matches_target(default_gear):
    """With ℓ=11, expect ~1 cut per 2048 bytes on average."""
    import random
    data = random.Random(0).randbytes(200 * 1024)
    cuts = cut_positions(data, default_gear)
    rate = len(cuts) / len(data)
    assert 1 / 4096 < rate < 1 / 1024


def test_determinism(default_gear):
    import random
    data = random.Random(0xABC).randbytes(32 * 1024)
    c1 = cut_positions(data, default_gear)
    c2 = cut_positions(data, default_gear)
    assert c1 == c2


def test_max_cuts_in_window():
    cuts = [100, 150, 200, 500, 1024]
    assert max_cuts_in_window(cuts, 100) == 2
    assert max_cuts_in_window(cuts, 50) == 1
    assert max_cuts_in_window(cuts, 1024) == 4
    assert max_cuts_in_window([], 100) == 0


def test_window_must_pass(default_gear):
    assert not default_gear.is_cut(0, 0)
    assert not default_gear.is_cut(0, default_gear.window - 1)


@pytest.mark.parametrize("cut_bits", [9, 10, 11, 12, 13])
def test_cut_rate_scales_with_bits(cut_bits):
    import random
    gear = GearRollingHash(table=build_gear_table(0), cut_bits=cut_bits)
    data = random.Random(1).randbytes(128 * 1024)
    cuts = cut_positions(data, gear)
    expected = len(data) / (2 ** cut_bits)
    # tolerate 2× deviation from the expected count
    assert 0.5 * expected < len(cuts) < 2 * expected
