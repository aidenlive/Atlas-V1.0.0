"""Atlas: the company editorial system.

Atlas states, in eight short standards, what must be true of a piece of
company writing — how it sounds, which words it uses, how it is shaped, what it
must declare, what its kind requires, when it is ready, who may approve it, and
where it goes. The :mod:`atlas` package checks a repository of content against
those standards.

The package is a library first. Everything the CLI does can be imported from
:mod:`atlas.core` with no terminal involved, so one body of code serves the
command line, the test suite, CI, and whatever you build on top.
"""

from __future__ import annotations

#: Distribution version. Moves on every release of the tooling.
__version__ = "1.0.0"

#: The contract version of the standard the tooling enforces. Moves only when
#: the standard's requirements change. See docs/reference/versioning.md.
STANDARD = "editorial/1.0"

NAME = "atlas"

DESCRIPTION = "Declared, versioned, machine-checked standards for company writing"

__all__ = ["__version__", "STANDARD", "NAME", "DESCRIPTION"]
