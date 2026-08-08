"""Domain logic: manifests, specifications, workstreams, library, compliance.

Nothing in this package knows about terminals, argument parsing, or exit codes.
Functions return data or raise :class:`atlas.errors.AtlasError`; rendering and
process control belong to :mod:`atlas.cli`. That boundary is what lets the same
code back the CLI, the test suite, and anything an adopter builds on top.
"""

from __future__ import annotations

from . import compliance, library, manifest, prompts, specs, template, tokens, workstream

__all__ = [
    "compliance",
    "library",
    "manifest",
    "prompts",
    "specs",
    "template",
    "tokens",
    "workstream",
]
