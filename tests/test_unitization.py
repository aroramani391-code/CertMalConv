"""Tests for content-defined unitization (Eq. 2)."""

from __future__ import annotations

import random

from certmalconv.unitization.content_defined_chunking import iter_units, multiset, unitize


def test_unitize_covers_full_file(small_binary, default_gear):
    units = unitize(small_binary, gear=default_gear)
    total = sum(len(u) for u in units)
    assert total == len(small_binary)


def test_unit_offsets_are_consecutive(small_binary, default_gear):
    units = unitize(small_binary, gear=default_gear)
    prev_end = 0
    for u in units:
        assert u.offset == prev_end
        prev_end = u.end
    assert prev_end == len(small_binary)


def test_insertion_only_disturbs_local_units(small_binary, default_gear):
    units_before = unitize(small_binary, gear=default_gear)
    multiset_before = multiset(units_before)

    pos = len(small_binary) // 2
    data_after = small_binary[:pos] + b"\xDE\xAD\xBE\xEF" + small_binary[pos:]
    units_after = unitize(data_after, gear=default_gear)
    multiset_after = multiset(units_after)

    # No unit far from the edit should disappear
    removed = {
        k: multiset_before[k] - multiset_after.get(k, 0)
        for k in multiset_before
        if multiset_before[k] - multiset_after.get(k, 0) > 0
    }
    # Removed units must all touch the edit zone; sum of removals is bounded.
    assert sum(removed.values()) <= 3


def test_iter_units_matches_unitize(small_binary, default_gear):
    seq = list(iter_units(small_binary, default_gear))
    bulk = unitize(small_binary, gear=default_gear)
    assert len(seq) == len(bulk)
    for s, b in zip(seq, bulk, strict=True):
        assert s.index == b.index
        assert s.offset == b.offset
        assert s.data == b.data
