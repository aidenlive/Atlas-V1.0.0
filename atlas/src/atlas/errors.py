"""Errors and exit codes.

Exit codes are part of the interface. A script that runs ``atlas check`` needs
to tell "this content has violations" from "you typed the flag wrong", and both
from "this is not an Atlas repository". Prose on stderr cannot carry that
distinction; a number can.
"""

from __future__ import annotations

import enum

__all__ = ["ExitCode", "AtlasError", "UsageError", "NotFoundError", "NotARepositoryError"]


class ExitCode(enum.IntEnum):
    """Every code the CLI can return."""

    OK = 0
    #: The command ran and found violations.
    VIOLATIONS = 1
    #: The command was invoked incorrectly.
    USAGE = 2
    #: A named thing (spec, prompt, term, workstream) does not exist.
    NOT_FOUND = 3
    #: The working directory is not an Atlas repository.
    NOT_A_REPOSITORY = 4


class AtlasError(Exception):
    """Base class for errors the CLI reports rather than tracebacks."""

    exit_code: ExitCode = ExitCode.USAGE

    def __init__(self, message: str, *, hint: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        #: One line telling the reader what to do next. Optional, but an error
        #: that says only what went wrong makes the reader guess the remedy.
        self.hint = hint


class UsageError(AtlasError):
    exit_code = ExitCode.USAGE


class NotFoundError(AtlasError):
    exit_code = ExitCode.NOT_FOUND


class NotARepositoryError(AtlasError):
    exit_code = ExitCode.NOT_A_REPOSITORY
