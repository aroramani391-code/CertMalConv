"""Feature-space FGSM on the byte patch (Section VI-C, Table IX).

The attacker perturbs pixels of the grayscale byte patch; the result
need not correspond to a valid file.
"""

from __future__ import annotations

import torch

__all__ = ["fgsm_attack"]


def fgsm_attack(
    patch: torch.Tensor,            # (B, 1, R, R) float in [0, 1]
    target: torch.Tensor,           # (B,) float, usually 0 to force benign
    model_logit_fn,                 # callable that returns scalar logit per sample
    *,
    epsilon: float = 0.01,
) -> torch.Tensor:
    """Single-step FGSM; returns the perturbed patch clipped to ``[0, 1]``."""
    patch = patch.clone().detach().requires_grad_(True)
    logit = model_logit_fn(patch)
    loss = torch.nn.functional.binary_cross_entropy_with_logits(logit, target)
    grad = torch.autograd.grad(loss, patch)[0]
    pert = patch - epsilon * grad.sign()
    return pert.clamp(0.0, 1.0).detach()
