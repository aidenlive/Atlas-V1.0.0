"""Command handlers.

One module per top-level command. Each exposes ``register(subparsers, flags)``
and one or more handlers taking a :class:`atlas.cli.Context` and returning an
:class:`atlas.errors.ExitCode`. Handlers render; they do not compute: the
logic lives in :mod:`atlas.core` so it can be tested without a terminal.
"""

from __future__ import annotations

from . import (
    check,
    completion,
    doctor,
    init,
    library,
    prompt,
    site,
    spec,
    status,
    template,
    validate,
    work,
)

__all__ = [
    "check",
    "completion",
    "doctor",
    "init",
    "library",
    "prompt",
    "site",
    "spec",
    "status",
    "template",
    "validate",
    "work",
]
