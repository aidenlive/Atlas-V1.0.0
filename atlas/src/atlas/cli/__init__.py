"""Entry point: parse, dispatch, translate errors into exit codes.

One function owns the exit code. Commands return one; they never call
``sys.exit``, so the same functions can be called from a test without the test
having to survive a raised ``SystemExit``.
"""

from __future__ import annotations

import sys
import typing as t

from ..errors import AtlasError, ExitCode
from ..terminal import Console
from .app import build_parser, resolve_globals

__all__ = ["main", "run_argv"]


def run_argv(argv: t.Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = resolve_globals(parser.parse_args(list(argv) if argv is not None else None))

    if not getattr(args, "command", None):
        parser.print_help()
        return int(ExitCode.OK)

    console = Console(
        color=not args.no_color,
        json_mode=args.json_mode,
        quiet=args.quiet,
        verbose=args.verbose,
    )

    try:
        return int(args.handler(args, console))
    except AtlasError as error:
        if args.json_mode:
            console.json({"ok": False, "error": error.message, "hint": error.hint})
        else:
            console.failure(error.message, error.hint)
        return int(error.exit_code)
    except BrokenPipeError:
        # `atlas prompt list | head` closes the pipe early. That is the shell
        # working as intended, not an error, so exit quietly rather than
        # printing a traceback over the output the reader wanted.
        _silence_broken_pipe()
        return int(ExitCode.OK)
    except KeyboardInterrupt:  # pragma: no cover - interactive only
        console.err("interrupted")
        return int(ExitCode.USAGE)


def _silence_broken_pipe() -> None:
    """Point stdout at nothing, so interpreter shutdown does not flush into a
    closed pipe and print a second traceback."""
    import os

    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())


def main(argv: t.Sequence[str] | None = None) -> t.NoReturn:
    sys.exit(run_argv(argv))
