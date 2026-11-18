"""Shape and determinism tests for the byte-view encoder."""

from __future__ import annotations

import pytest

torch = pytest.importorskip("torch")

from certmalconv.models.byte_encoder import ByteEncoder, ByteEncoderConfig


def test_output_shape():
    enc = ByteEncoder(ByteEncoderConfig(out_dim=128)).eval()
    patch = torch.zeros((4, 1, 64, 64))
    out = enc(patch)
    assert out.shape == (4, 128)


def test_deterministic_forward():
    torch.manual_seed(0)
    enc = ByteEncoder(ByteEncoderConfig(out_dim=64)).eval()
    patch = torch.randn((2, 1, 64, 64))
    out1 = enc(patch)
    out2 = enc(patch)
    assert torch.allclose(out1, out2)
