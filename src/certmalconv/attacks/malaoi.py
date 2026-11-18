"""MalAOI — active opcode insertion method with maliciousness preserving.

After Peng et al., Sci. Rep. 15:9174, 2025.  Inserts benign and jump
opcodes chosen by PPO.
"""

from __future__ import annotations

from dataclasses import dataclass, field

__all__ = ["MalAOIConfig", "malaoi_attack"]


@dataclass
class MalAOIConfig:
    policy: str = "ppo"
    opcode_pool: list[str] = field(default_factory=lambda: ["nop", "jmp", "pushpop", "test"])
    max_sites: int = 16
    max_opcodes_per_site: int = 4


def malaoi_attack(binary: bytes, config: MalAOIConfig, score_fn) -> bytes:
    """Return the perturbed binary after a PPO-driven opcode insertion."""
    from certmalconv.attacks._rl_search import ppo_insert
    return ppo_insert(
        binary,
        pool=config.opcode_pool,
        max_sites=config.max_sites,
        max_per_site=config.max_opcodes_per_site,
        score_fn=score_fn,
    )
