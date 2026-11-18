"""Tests for gated fusion and unit evidence (Eq. 6-7)."""

from __future__ import annotations

import pytest

torch = pytest.importorskip("torch")

from certmalconv.models.fusion import GatedFusion, GatedFusionConfig, UnitEvidenceHead


def test_fusion_shape():
    fuse = GatedFusion(GatedFusionConfig(dim=128)).eval()
    a = torch.randn(4, 128)
    b = torch.randn(4, 128)
    assert fuse(a, b).shape == (4, 128)


def test_gate_bounds():
    """Gate output must stay in [0, 1]."""
    fuse = GatedFusion(GatedFusionConfig(dim=32)).eval()
    a = torch.randn(1, 32)
    b = torch.randn(1, 32)
    z = fuse(a, b)
    # Since γ ∈ (0, 1), fused output must lie between min and max of a, b per dim
    lo = torch.min(a, b)
    hi = torch.max(a, b)
    assert ((z >= lo - 1e-5) & (z <= hi + 1e-5)).all()


def test_unit_evidence_in_range():
    head = UnitEvidenceHead(dim=64).eval()
    tile_emb = torch.randn(3, 5, 64)   # 3 units, 5 tiles each
    z_u, e_u = head(tile_emb)
    assert z_u.shape == (3, 64)
    assert e_u.shape == (3,)
    assert ((e_u >= 0) & (e_u <= 1)).all()
