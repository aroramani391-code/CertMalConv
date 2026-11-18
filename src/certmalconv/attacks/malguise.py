"""MalGuise — call-based redividing attack (Ling et al., USENIX Sec. 2024)."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["MalGuiseConfig", "malguise_attack"]


@dataclass
class MalGuiseConfig:
    max_sites: int = 8
    max_bytes_per_site: int = 5
    search: str = "black_box_rl"
    max_queries: int = 500


def malguise_attack(binary: bytes, config: MalGuiseConfig, score_fn) -> bytes:
    """Return the perturbed binary after a MalGuise black-box search.

    The implementation here is the public wrapper; the full RL loop
    lives under ``experiments/03_adversarial_attacks/`` to keep the
    core library import-light.
    """
    from certmalconv.attacks._rl_search import black_box_rewrite
    return black_box_rewrite(
        binary,
        operations=["redivide_call", "replace_call", "add_chain"],
        max_sites=config.max_sites,
        max_bytes_per_site=config.max_bytes_per_site,
        max_queries=config.max_queries,
        score_fn=score_fn,
    )
