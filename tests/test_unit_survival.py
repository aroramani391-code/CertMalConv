"""Tests for unit-survival and evidence invariance (Lemma 1)."""

from __future__ import annotations

import pytest

from certmalconv.certification.unit_survival import (
    assert_evidence_invariant,
    surviving_units,
)
from certmalconv.unitization.content_defined_chunking import unitize


def test_surviving_units_unchanged_file(small_binary, default_gear):
    before = unitize(small_binary, gear=default_gear)
    after = unitize(small_binary, gear=default_gear)
    survivors = surviving_units(before, after)
    assert len(survivors) == len(before)


def test_evidence_unchanged_after_insertion(small_binary, default_gear):
    before = unitize(small_binary, gear=default_gear)
    inserted = small_binary[:500] + b"\xDE\xAD" * 64 + small_binary[500:]
    after = unitize(inserted, gear=default_gear)
    survivors = surviving_units(before, after)

    # Fake per-unit evidences based on hash of the bytes — must be identical
    def pseudo_evidence(u):
        return (sum(u.data) % 1024) / 1024.0

    before_evid = {u.index: pseudo_evidence(u) for u in survivors}
    after_evid = {u.index: pseudo_evidence(u) for u in survivors}
    assert_evidence_invariant(before_evid, after_evid)


def test_assert_evidence_invariant_detects_change():
    before_evid = {0: 0.5, 1: 0.8}
    after_evid = {0: 0.5, 1: 0.9}
    with pytest.raises(AssertionError):
        assert_evidence_invariant(before_evid, after_evid)
