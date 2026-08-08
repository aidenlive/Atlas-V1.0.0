"""Shared test fixtures.

``src/`` is put on the path here as well as in pyproject so the suite runs the
same way under a bare ``pytest tests/`` as it does under the configured
invocation. A test suite that only passes one way is a test suite people stop
running.
"""

from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@pytest.fixture(scope="session")
def repo_root() -> pathlib.Path:
    return ROOT


@pytest.fixture(scope="session")
def repository():
    from atlas.paths import Repository

    return Repository(ROOT)
