"""Smoke tests for attack implementations."""

from __future__ import annotations

import pytest

from certmalconv.attacks.insertion_attack import InsertionConfig, insertion_attack
from certmalconv.attacks.phantomcall import PhantomCallConfig, phantomcall_attack
from certmalconv.attacks.tur import TURConfig, tur_attack


@pytest.mark.slow
def test_insertion_attack_runs():
    rng = __import__("random").Random(0)
    binary = (b"\x4D\x5A" + rng.randbytes(0x3E) + b"\x80" + b"\x00" * 3
              + b"PE\x00\x00" + rng.randbytes(1024))
    cfg = InsertionConfig(family="full_dos", payload_kib=1, iterations=3)
    out = insertion_attack(binary, cfg, score_fn=lambda b: len(b) / 1_000_000)
    assert len(out) >= len(binary)


def test_phantomcall_adds_bytes():
    rng = __import__("random").Random(1)
    binary = rng.randbytes(1024) + b"\xE8\x00\x00\x00\x00" + rng.randbytes(1024)
    out = phantomcall_attack(binary, PhantomCallConfig(injected_functions=1),
                             score_fn=lambda b: 0.5)
    assert len(out) >= len(binary)


def test_tur_respects_budget(monkeypatch):
    calls = []

    def fake_decide(b):
        calls.append(len(b))
        return {"verdict": 1 if len(calls) < 6 else 0,
                "score": 1.0 / max(len(calls), 1),
                "top_unit_index": 0}

    cfg = TURConfig(budget_units=4, restarts=1)
    _ = tur_attack(b"\x90" * 1024, cfg, fake_decide)
    # The greedy loop should not have exceeded the budget_units + initial call.
    assert len(calls) <= 4 * (len(cfg.rewrites) + 1) + 2
