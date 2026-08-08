"""The CLI entry point.

This module owns three things and nothing else: parsing arguments, building the
:class:`~atlas.terminal.Console`, and translating outcomes into exit codes.
Every command handler receives a fully-formed context and returns an
:class:`~atlas.errors.ExitCode`, so no command calls ``sys.exit`` or prints a
traceback of its own.
"""

from __future__ import annotations

import dataclasses
import sys
import typing as t

from ..errors import AtlasError, ExitCode
from ..paths import Repository, find_repository
from ..terminal import Console

__all__ = ["main", "Context"]


@dataclasses.dataclass
class Context:
    """What every command handler is given."""

    args: t.Any
    console: Console

    @property
    def repo(self) -> Repository:
        """The enclosing repository, resolved lazily.

        Lazily, because ``atlas --help``, ``atlas init``, and
        ``atlas completion`` are useful outside a repository and should not
        fail just because the working directory is not one.
        """
        if getattr(self, "_repo", None) is None:
            self._repo = find_repository(getattr(self.args, "directory", None))
        return self._repo


def main(argv: t.Sequence[str] | None = None) -> int:
    from .app import build_parser, resolve_globals

    parser = build_parser()
    args = resolve_globals(parser.parse_args(list(argv) if argv is not None else None))

    if not getattr(args, "command", None):
        parser.print_help()
        return int(ExitCode.OK)

    console = Console(
        color=False if args.no_color else None,
        quiet=args.quiet,
        verbose=args.verbose,
        json_mode=args.json_mode,
    )
    context = Context(args=args, console=console)

    try:
        return int(args.handler(context))
    except AtlasError as error:
        if console.json_mode:
            console.json_mode = False  # errors are not part of the data contract
            import json

            json.dump(
                {"ok": False, "error": error.message, "hint": error.hint},
                sys.stderr,
                indent=2,
            )
            sys.stderr.write("\n")
        else:
            console.error(error.message)
            if error.hint:
                console.hint(error.hint)
        return int(error.exit_code)
    except KeyboardInterrupt:  # pragma: no cover - interactive only
        console.error("interrupted")
        return 130
    except BrokenPipeError:  # pragma: no cover - `atlas ... | head`
        return int(ExitCode.OK)
    except Exception as error:  # noqa: BLE001 - the last line of defence
        console.error(f"internal error: {type(error).__name__}: {error}")
        console.hint("This is a bug in Atlas. Re-run with --verbose and please report it.")
        if args.verbose:
            raise
        return int(ExitCode.INTERNAL)
