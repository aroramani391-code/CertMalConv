"""Shared RL / black-box search helpers for the attack modules."""

from __future__ import annotations

from typing import Callable

__all__ = ["black_box_rewrite", "ppo_insert"]


def black_box_rewrite(
    binary: bytes,
    *,
    operations: list[str],
    max_sites: int,
    max_bytes_per_site: int,
    max_queries: int,
    score_fn: Callable[[bytes], float],
) -> bytes:
    """Black-box greedy search as in MalGuise [5]."""
    current = binary
    best_score = score_fn(current)
    queries = 0
    for _ in range(max_sites):
        improved = False
        for _ in range(len(operations)):
            if queries >= max_queries:
                break
            cand = _apply_random_op(current, operations, max_bytes_per_site)
            s = score_fn(cand)
            queries += 1
            if s < best_score:
                best_score, current, improved = s, cand, True
        if not improved:
            break
    return current


def ppo_insert(
    binary: bytes,
    *,
    pool: list[str],
    max_sites: int,
    max_per_site: int,
    score_fn: Callable[[bytes], float],
) -> bytes:
    """Placeholder PPO policy that walks opcode-insertion actions."""
    current = binary
    best_score = score_fn(current)
    for _ in range(max_sites):
        for _ in range(max_per_site):
            cand = current + _opcode_bytes(pool[0])
            s = score_fn(cand)
            if s < best_score:
                best_score, current = s, cand
    return current


# ---------------------------------------------------------------- helpers
def _apply_random_op(binary: bytes, ops: list[str], budget: int) -> bytes:
    import random
    op = random.choice(ops)
    payload = random.randbytes(budget)
    if op == "redivide_call":
        return binary + b"\xE8" + payload
    if op == "replace_call":
        return binary[:-budget] + payload
    if op == "add_chain":
        return binary + payload
    return binary


def _opcode_bytes(name: str) -> bytes:
    return {
        "nop": b"\x90",
        "jmp": b"\xEB\x00",
        "pushpop": b"\x50\x58",
        "test": b"\x85\xC0",
    }.get(name, b"\x90")
