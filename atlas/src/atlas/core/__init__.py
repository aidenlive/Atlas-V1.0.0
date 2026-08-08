"""The library half of Atlas.

Everything the CLI does lives here and can be imported with no terminal
involved, so the same code serves the command line, the test suite, CI, and
whatever you build on top.
"""

from __future__ import annotations

from . import (
    compliance,
    frontmatter,
    lexicon,
    lint,
    manifest,
    prompts,
    specs,
    template,
    workstream,
)

__all__ = [
    "compliance",
    "frontmatter",
    "lexicon",
    "lint",
    "manifest",
    "prompts",
    "specs",
    "template",
    "workstream",
]
