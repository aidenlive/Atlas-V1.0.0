"""Atlas: declared, versioned, machine-checked structure for digital work.

This package is the product's tooling surface. Everything a human or an agent
can do to an Atlas repository is reachable through :mod:`atlas.cli`, and every
command in that CLI is a thin shell around a function in :mod:`atlas.core` or
:mod:`atlas.site`. That split is deliberate: the library is importable and unit
testable without a terminal, and the CLI owns argument parsing, exit codes, and
rendering. Nothing else.

Two version numbers live here and they move independently:

``__version__``
    The release version of this repository and its tooling.
``STANDARD_VERSION``
    The contract version of the specification suite. A repository declaring
    ``standard: project/1.0`` is promising to satisfy *that* contract, not to
    run any particular Atlas release.

See ``docs/reference/versioning.md`` for why they are separate.
"""

from __future__ import annotations

__all__ = [
    "__version__",
    "STANDARD_VERSION",
    "NAME",
    "TAGLINE",
    "DESCRIPTION",
    "HOMEPAGE",
    "STANDARDS",
]

__version__ = "1.0.0"

#: The specification-suite contract version. Not the release version.
STANDARD_VERSION = "project/1.0"

NAME = "Atlas"
TAGLINE = "Structure a machine can check and a human can read"
DESCRIPTION = (
    "Declared, versioned, machine-checked structure for files, repositories, "
    "quality, authority, and intent"
)
HOMEPAGE = "https://github.com/OWNER/atlas"

#: The eight standards, in reading order. The canonical source is the YAML
#: front matter in ``spec/*.md``; this tuple exists so that code with no
#: repository in hand (``atlas --help``, packaging metadata) can still name
#: them. :func:`atlas.core.specs.load_specs` is authoritative when a repository
#: is available, and ``tests/test_cli.py`` asserts the two agree.
STANDARDS = (
    "workspace",
    "project",
    "project-matrix",
    "project-checklist",
    "admin",
    "presentation",
    "library",
    "workstream",
)
