"""The static site generator.

Split by concern so each piece is testable on its own:

``markdown``   Markdown to HTML, headings, and plain text
``highlight``  dependency-free syntax highlighting
``theme``      the stylesheet, built entirely on design tokens
``layout``     the page shell and its client script
``search``     the client-side search index
``builder``    orchestration: what pages exist and what goes in them

The site is derived output. It is gitignored, rebuilt in CI, and never edited;
if it disagrees with the Markdown, the Markdown wins.
"""

from __future__ import annotations

from .builder import BuildResult, build

__all__ = ["build", "BuildResult"]
