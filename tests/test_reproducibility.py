"""Deterministic pipeline tests."""

from __future__ import annotations

import pytest

from certmalconv.training.seed import DEFAULT_SEEDS, set_global_seed


def test_seed_sets_python_rng():
    import random
    set_global_seed(42)
    a = random.random()
    set_global_seed(42)
    b = random.random()
    assert a == b


def test_seed_sets_numpy_rng():
    import numpy as np
    set_global_seed(7)
    a = np.random.rand(5)
    set_global_seed(7)
    b = np.random.rand(5)
    assert (a == b).all()


def test_five_canonical_seeds():
    assert DEFAULT_SEEDS == (42, 123, 2024, 2025, 2026)


@pytest.mark.slow
def test_unitize_is_deterministic_across_runs(small_binary, default_gear):
    from certmalconv.unitization.content_defined_chunking import unitize
    runs = [unitize(small_binary, gear=default_gear) for _ in range(5)]
    first = [u.data for u in runs[0]]
    for r in runs[1:]:
        assert [u.data for u in r] == first


@pytest.mark.slow
def test_disassembler_bitwise():
    """Linear-sweep decoding is deterministic — no seed dependency."""
    import random
    from certmalconv.preprocessing.disassembler import LinearSweepDecoder
    data = random.Random(0).randbytes(4096)
    dec = LinearSweepDecoder("x86_64")
    out1 = dec.decode(data)
    out2 = dec.decode(data)
    assert len(out1) == len(out2)
    for a, b in zip(out1, out2, strict=True):
        assert (a.mnemonic, a.op_str, a.size) == (b.mnemonic, b.op_str, b.size)
