"""Shared fixtures.

Tests run against this repository itself. That is deliberate: the strongest
claim Atlas makes is that it passes the standard it defines, and the test suite
is where that claim is checked rather than asserted.
"""

from __future__ import annotations

import pathlib

import pytest

from atlas.paths import Repository

ROOT = pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def repo() -> Repository:
    return Repository(root=ROOT)


@pytest.fixture(scope="session")
def root() -> pathlib.Path:
    return ROOT
