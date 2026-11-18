"""Small PE helper functions used by PhantomCall."""

from __future__ import annotations

__all__ = ["find_call_sites", "add_dummy_function"]


def find_call_sites(binary: bytes) -> list[int]:
    """Return byte offsets of ``E8 ?? ?? ?? ??`` call instructions.

    This is a lightweight scanner; the full tool uses Capstone to avoid
    data-in-code false positives, but the fast path works well for the
    short-trampoline attacks of PhantomCall.
    """
    sites: list[int] = []
    for i in range(len(binary) - 5):
        if binary[i] == 0xE8:
            sites.append(i)
    return sites


def add_dummy_function(binary: bytes) -> bytes:
    """Append a short dummy function the detector can see as a new node."""
    stub = (
        b"\x55"                # push ebp
        b"\x89\xE5"            # mov ebp, esp
        + b"\x90" * 32         # nop padding
        + b"\x5D"              # pop ebp
        + b"\xC3"              # ret
    )
    return binary + stub
