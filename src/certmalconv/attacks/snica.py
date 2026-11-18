"""SNICA — Semantics-preserving Node Injection with Connectivity Attack.

Companion of SNIA that adds edges between injected nodes and existing
blocks.  After Zapzalka et al., IEEE TDSC 22(2), 2025.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["SNICAConfig", "snica_attack"]


@dataclass
class SNICAConfig:
    budget_pct: float = 0.05
    edge_budget_pct: float = 0.03
    num_steps: int = 40


def snica_attack(acfg, config: SNICAConfig, model_fn):
    """Thin wrapper around the SNIA loop plus edge injection."""
    from certmalconv.attacks.snia import snia_attack, SNIAConfig
    acfg = snia_attack(acfg, SNIAConfig(budget_pct=config.budget_pct,
                                        num_steps=config.num_steps), model_fn)
    n_edges = max(1, int(config.edge_budget_pct * acfg.num_edges))
    for _ in range(n_edges):
        acfg.add_benign_edge()
    return acfg
