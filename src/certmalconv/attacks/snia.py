"""SNIA — Semantics-preserving Node Injection Attack on ACFG classifiers.

After Zapzalka, Salem and Mohaisen (IEEE TDSC 22(2), 2025).
"""

from __future__ import annotations

from dataclasses import dataclass

import torch

__all__ = ["SNIAConfig", "snia_attack"]


@dataclass
class SNIAConfig:
    budget_pct: float = 0.05        # injected nodes as fraction of |V|
    num_steps: int = 40
    lr: float = 0.01


def snia_attack(acfg, config: SNIAConfig, model_fn):
    """Inject functionality-preserving nodes into the ACFG.

    This public shim exists to keep the API surface stable; the actual
    loop lives in ``_snia_inner`` and is invoked from
    ``experiments/03_adversarial_attacks/run.py``.
    """
    # Compute number of nodes to inject
    n_nodes = max(1, int(config.budget_pct * acfg.num_nodes))
    # Insert dummy nodes that chain back to a reachable block (semantics-preserving)
    injected = [acfg.add_dummy_node() for _ in range(n_nodes)]
    opt = torch.optim.Adam([n.features for n in injected], lr=config.lr)
    for _ in range(config.num_steps):
        opt.zero_grad()
        score = model_fn(acfg)
        loss = score  # we want score to drop, so minimise it
        loss.backward()
        opt.step()
    return acfg
