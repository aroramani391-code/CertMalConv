"""Shape tests for the structure-view encoder (GIN over two modes)."""

from __future__ import annotations

import pytest

torch = pytest.importorskip("torch")
pyg = pytest.importorskip("torch_geometric")

from certmalconv.models.structure_encoder import StructureEncoder, StructureEncoderConfig


def test_output_shape_small_graph():
    enc = StructureEncoder(StructureEncoderConfig(attributes=11, out_dim=128)).eval()
    x = torch.randn(10, 11)
    edge_index = torch.tensor([[0, 1, 2, 3], [1, 2, 3, 4]], dtype=torch.long)
    batch = torch.zeros(10, dtype=torch.long)
    out = enc(x, edge_index, batch, x, edge_index, batch)
    assert out.shape == (1, 128)
