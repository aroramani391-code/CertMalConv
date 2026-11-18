"""PhantomCall — function-call graph perturbation.

After Akil, Li, Karim, Iyengar, Kundu, Bertino, arXiv:2609.00705, 2026.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["PhantomCallConfig", "phantomcall_attack"]


@dataclass
class PhantomCallConfig:
    injected_functions: int = 1
    trampoline_bytes: int = 5


def phantomcall_attack(binary: bytes, config: PhantomCallConfig, score_fn) -> bytes:
    """Insert a trampoline at a single call site and an injected function elsewhere.

    The resulting edit is exactly the two-site case covered by
    Corollary 1 at ``s = 2``.
    """
    from certmalconv.attacks._pe_tools import find_call_sites, add_dummy_function
    call_sites = find_call_sites(binary)
    if not call_sites:
        return binary
    # Rewrite one call to go through a trampoline
    site = call_sites[0]
    trampoline = b"\xE8" + b"\x00" * (config.trampoline_bytes - 1)
    patched = binary[:site] + trampoline + binary[site + config.trampoline_bytes:]
    # Append the dummy function
    for _ in range(config.injected_functions):
        patched = add_dummy_function(patched)
    return patched
