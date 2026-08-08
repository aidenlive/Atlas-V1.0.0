"""Error taxonomy and exit codes.

Exit codes are part of the CLI's contract: scripts and CI branch on them, so
they are enumerated here rather than scattered as integer literals. The split
between ``FAILURE`` (the thing you asked about is not true) and ``USAGE`` /
``INTERNAL`` (the tool could not answer) matters: a CI job that treats "the
repository is non-compliant" the same as "you typed the flag wrong" reports a
red build for the wrong reason.
"""

from __future__ import annotations

import enum

__all__ = ["ExitCode", "AtlasError", "UsageError", "NotFoundError", "CheckFailed"]


class ExitCode(enum.IntEnum):
    """Process exit codes. Stable across releases; additions only."""

    OK = 0
    #: A check ran to completion and found violations.
    FAILURE = 1
    #: The command line itself was wrong: bad flag, missing argument.
    USAGE = 2
    #: A required file, workstream, prompt, or specification does not exist.
    NOT_FOUND = 3
    #: The command was not run inside an Atlas repository.
    NO_REPOSITORY = 4
    #: An unexpected exception escaped. Always a bug in Atlas.
    INTERNAL = 70


class AtlasError(Exception):
    """Base class for every error Atlas raises deliberately.

    Carries its own exit code and an optional ``hint``: the next thing the
    reader should try. A bare error message tells someone they are stuck; a
    hint tells them how to stop being stuck, which is most of what separates a
    tool people tolerate from one they reach for.
    """

    exit_code: ExitCode = ExitCode.FAILURE

    def __init__(self, message: str, *, hint: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint


class UsageError(AtlasError):
    """The invocation was malformed."""

    exit_code = ExitCode.USAGE


class NotFoundError(AtlasError):
    """A named thing does not exist."""

    exit_code = ExitCode.NOT_FOUND


class CheckFailed(AtlasError):
    """A validation or compliance gate found violations.

    ``violations`` is retained so ``--json`` can emit the full list rather than
    a rendered summary.
    """

    exit_code = ExitCode.FAILURE

    def __init__(
        self,
        message: str,
        violations: list[str] | None = None,
        *,
        hint: str | None = None,
    ) -> None:
        super().__init__(message, hint=hint)
        self.violations = violations or []
