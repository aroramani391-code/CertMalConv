"""Shared pytest fixtures and command-line flags."""

from __future__ import annotations

import pytest


def pytest_addoption(parser):
    parser.addoption("--run-slow", action="store_true", default=False,
                     help="Run tests marked @pytest.mark.slow")
    parser.addoption("--run-full", action="store_true", default=False,
                     help="Run full-scale tests (hours of wall time)")


def pytest_collection_modifyitems(config, items):
    skip_slow = pytest.mark.skip(reason="slow test; pass --run-slow")
    skip_full = pytest.mark.skip(reason="full-scale test; pass --run-full")
    for item in items:
        if "slow" in item.keywords and not config.getoption("--run-slow"):
            item.add_marker(skip_slow)
        if "full" in item.keywords and not config.getoption("--run-full"):
            item.add_marker(skip_full)


@pytest.fixture
def small_binary() -> bytes:
    """A deterministic 16 KiB test binary."""
    import random
    r = random.Random(0xC0FFEE)
    return r.randbytes(16 * 1024)


@pytest.fixture
def default_gear():
    from certmalconv.unitization.gear_hash import GearRollingHash, build_gear_table
    return GearRollingHash(table=build_gear_table(0xC3A4B1E2))
