"""Tests for the insertion bound (Lemma 2 append sentence)."""

from __future__ import annotations

from certmalconv.certification.edit_distance import edit_locality_bound
from certmalconv.certification.insertion_bound import bound_insertion


def test_append_bound_is_one():
    assert bound_insertion(1) == 1
    assert bound_insertion(5) == 1
    assert bound_insertion(0) == 0


def test_pure_append_through_edit_locality_bound():
    cuts = [10, 50, 100, 200, 400]
    file_size = 500
    # a pure append at file_size is still within window of only the last unit
    altered = edit_locality_bound(cuts, [(file_size, file_size - 1)],
                                  file_size=file_size)
    assert altered == 1


def test_mid_file_insertion_counts_one_unit_plus_zone_cuts():
    cuts = [100, 200, 300, 400]
    # pure insertion at position 250 with window=64 → zone is [250, 313]
    altered = edit_locality_bound(cuts, [(250, 249)], window=64, file_size=500)
    # zone contains no cut, so bound = 1
    assert altered == 1
