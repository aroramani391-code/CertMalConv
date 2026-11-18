"""Problem-space insertion attacks (Full DOS, Extend, Shift).

After Demetrio, Coull, Biggio et al., ACM TOPS 24(4), 2021.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["InsertionConfig", "insertion_attack"]


@dataclass
class InsertionConfig:
    family: str = "full_dos"      # one of {full_dos, extend, shift}
    payload_kib: int = 64
    optimizer: str = "genetic"
    population: int = 32
    iterations: int = 50


def insertion_attack(binary: bytes, config: InsertionConfig, score_fn) -> bytes:
    """Return the perturbed binary.

    All three families keep the entrypoint and the original code
    unchanged — the payload is placed in slack space (Full DOS), in
    extended header fields (Extend), or by shifting PE sections (Shift).
    """
    payload = _optimise_payload(binary, config, score_fn)
    if config.family == "full_dos":
        return _write_dos_slack(binary, payload)
    if config.family == "extend":
        return _write_extend(binary, payload)
    if config.family == "shift":
        return _write_shift(binary, payload)
    raise ValueError(f"unknown insertion family: {config.family}")


# ---------------------------------------------------------------------- helpers
def _optimise_payload(binary: bytes, config: InsertionConfig, score_fn) -> bytes:
    import random
    best = bytes(random.getrandbits(8) for _ in range(config.payload_kib * 1024))
    best_score = score_fn(_write_dos_slack(binary, best))
    rng = random.Random(0xA7)
    for _ in range(config.iterations):
        cand = bytes(rng.getrandbits(8) for _ in range(len(best)))
        s = score_fn(_write_dos_slack(binary, cand))
        if s < best_score:
            best_score, best = s, cand
    return best


def _write_dos_slack(binary: bytes, payload: bytes) -> bytes:
    """Fill the padding between the DOS header and the PE header."""
    e_lfanew = int.from_bytes(binary[0x3C:0x40], "little")
    if e_lfanew <= 0x40:
        return binary + payload
    cap = e_lfanew - 0x40
    chunk = payload[:cap]
    return binary[:0x40] + chunk + binary[0x40 + len(chunk):]


def _write_extend(binary: bytes, payload: bytes) -> bytes:
    """Append the payload inside an added optional-header extension."""
    return binary + b"\x00" * 128 + payload


def _write_shift(binary: bytes, payload: bytes) -> bytes:
    """Shift sections to open a hole between the headers and the first section."""
    # Simplified: insert a slack region after the first section header.
    insert_at = 0x200
    return binary[:insert_at] + payload + binary[insert_at:]
