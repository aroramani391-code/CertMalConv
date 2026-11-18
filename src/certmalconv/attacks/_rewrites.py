"""Semantics-preserving rewrites applied by TUR and MalGuise."""

from __future__ import annotations

__all__ = ["apply_rewrite"]


def apply_rewrite(binary: bytes, unit_index: int, rewrite: str) -> bytes:
    """Return a new binary with the given rewrite applied to ``unit_index``.

    This is an interface stub — the actual byte-level rewrites live in
    ``experiments/03_adversarial_attacks/`` and are driven by Capstone
    + a small PE/ELF patcher.  The unit test suite monkey-patches this
    function to return pre-computed variants.
    """
    if rewrite == "instruction_substitution":
        return binary + b"\x90"               # nop sled; placeholder
    if rewrite == "register_reassignment":
        return binary + b"\x87\xC0"           # xchg eax, eax; placeholder
    if rewrite == "block_reorder":
        return binary + b"\xEB\x00"           # jmp +0; placeholder
    raise ValueError(f"unknown rewrite: {rewrite}")
