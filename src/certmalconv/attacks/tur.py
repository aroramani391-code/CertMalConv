"""Top-Unit Rewriting (TUR): the adaptive white-box attack on CertMalConv.

Each step takes the unit with the largest evidence, applies the
semantics-preserving rewrite that lowers its evidence most, and inserts
benign-looking units to lower the global score, until the file is
classified as benign or a budget of ``ρ_max`` rewritten units is spent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

__all__ = ["TURConfig", "TopUnitRewrite", "tur_attack", "tur_opt_attack"]


@dataclass
class TURConfig:
    budget_units: int = 8
    restarts: int = 1
    search: str = "greedy"             # "greedy" or "beam"
    beam_width: int = 1
    iterations: int = 40
    rewrites: list[str] = field(default_factory=lambda: [
        "instruction_substitution",
        "register_reassignment",
        "block_reorder",
    ])
    insert_benign_units: bool = True
    target: str = "full"               # one of {full, certified_path, global_branch, family}


class TopUnitRewrite:
    """Thin wrapper around the search loop so tests can stub it."""

    def __init__(self, config: TURConfig) -> None:
        self.config = config

    def __call__(
        self,
        binary: bytes,
        decide_fn: Callable[[bytes], dict],
    ) -> bytes:
        search = _beam_search if self.config.search == "beam" else _greedy_search
        best = binary
        best_score = decide_fn(binary)["score"]
        for _ in range(self.config.restarts):
            cand = search(binary, self.config, decide_fn)
            s = decide_fn(cand)["score"]
            if s < best_score:
                best_score, best = s, cand
        return best


def tur_attack(binary: bytes, config: TURConfig, decide_fn) -> bytes:
    return TopUnitRewrite(config)(binary, decide_fn)


def tur_opt_attack(binary: bytes, config: TURConfig, decide_fn) -> bytes:
    cfg = TURConfig(**{**config.__dict__, "search": "beam"})
    return TopUnitRewrite(cfg)(binary, decide_fn)


# ----------------------------------------------------------------- search
def _greedy_search(binary: bytes, config: TURConfig, decide_fn) -> bytes:
    from certmalconv.attacks._rewrites import apply_rewrite
    current = binary
    for _ in range(config.budget_units):
        decision = decide_fn(current)
        if decision["verdict"] == 0:
            return current
        top_unit = decision["top_unit_index"]
        best = current
        best_score = decision["score"]
        for rw in config.rewrites:
            cand = apply_rewrite(current, top_unit, rw)
            s = decide_fn(cand)["score"]
            if s < best_score:
                best_score, best = s, cand
        current = best
        if config.insert_benign_units:
            current = _append_benign_unit(current)
    return current


def _beam_search(binary: bytes, config: TURConfig, decide_fn) -> bytes:
    from certmalconv.attacks._rewrites import apply_rewrite
    beam = [(binary, decide_fn(binary)["score"])]
    for _ in range(config.iterations):
        next_beam: list[tuple[bytes, float]] = []
        for cand, _ in beam:
            decision = decide_fn(cand)
            if decision["verdict"] == 0:
                return cand
            top_unit = decision["top_unit_index"]
            for rw in config.rewrites:
                new = apply_rewrite(cand, top_unit, rw)
                next_beam.append((new, decide_fn(new)["score"]))
        beam = sorted(next_beam, key=lambda x: x[1])[: config.beam_width]
    return beam[0][0] if beam else binary


def _append_benign_unit(binary: bytes) -> bytes:
    """Append a short benign-looking unit (zero-padded instructions)."""
    return binary + b"\x90" * 64 + b"\xC3"
