"""The command tree.

Built on :mod:`argparse` deliberately. It is in the standard library, so
``pip install atlas-standard`` pulls no CLI framework, and the tool starts in
milliseconds inside a pre-commit hook.

Two things are worth knowing about the shape here:

* **The parser is the reference.** ``docs/reference/cli.md`` and the site's
  command reference are both rendered from this tree by :func:`render_reference`,
  so a flag cannot exist without being documented, and documentation cannot
  describe a flag that does not exist.
* **Help is grouped and exampled.** A flat alphabetical list of nineteen
  subcommands tells a newcomer nothing about where to start, so commands are
  grouped by what you are trying to do and every group carries a worked example.
"""

from __future__ import annotations

import argparse
import textwrap
import typing as t

from .. import DESCRIPTION, NAME, __version__
from .commands import (
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

__all__ = ["build_parser", "command_tree", "render_reference", "EPILOG"]

#: Command groups, in the order a newcomer meets them.
GROUPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Start", ("init", "status", "doctor")),
    ("Verify", ("check", "validate")),
    ("Work", ("work",)),
    ("Read", ("spec", "prompt", "library")),
    ("Publish", ("site", "template")),
    ("Shell", ("completion",)),
)

EPILOG = """\
examples:
  atlas check                               is this repository compliant?
  atlas check --only root-closed-set        work one check at a time
  atlas status                              what is this project, and who owns it
  atlas init payments-api ../payments-api   start a new compliant repository
  atlas work new migrate-fleet --owner person:you
  atlas work list --status blocked          what is stuck, and who owns it
  atlas spec show workstream --rules        the rules a standard defines
  atlas prompt search release               find a prompt for an assistant
  atlas site serve                          read the docs in a browser
  atlas check --json | jq '.checks[]'       output a script can read

Exit codes: 0 ok · 1 violations found · 2 bad usage · 3 not found
            4 not an Atlas repository
Docs: https://github.com/OWNER/atlas
"""


class AtlasHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Wider help, so option help does not wrap after three words."""

    def __init__(self, prog: str) -> None:
        super().__init__(prog, max_help_position=32, width=96)

    def _format_action_invocation(self, action: argparse.Action) -> str:
        # `-C DIR, --directory DIR` repeats the metavar; show it once.
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args = self._format_args(action, default)
        return f"{', '.join(action.option_strings)} {args}"


def _global_flags(parser: argparse.ArgumentParser) -> None:
    """Flags every command honours.

    Attached to each subparser as well as the root, so that both
    ``atlas --json check`` and ``atlas check --json`` work. People type them in
    either order, and being right about which one is "correct" is not worth a
    usage error.

    Every one uses ``default=SUPPRESS``. This matters: argparse applies a
    subparser's defaults *after* the parent has parsed, so an ordinary default
    on the subparser copy silently overwrites a value the parent already read —
    ``atlas -C /elsewhere check`` would quietly check the current directory
    instead. Suppressing means the attribute exists only when someone actually
    passed the flag, and :func:`resolve_globals` supplies the defaults once.
    """
    group = parser.add_argument_group("global options")
    group.add_argument(
        "-C", "--directory", metavar="DIR", default=argparse.SUPPRESS,
        help="operate on the repository at DIR instead of the current one",
    )
    group.add_argument("--json", action="store_true", dest="json_mode",
                       default=argparse.SUPPRESS,
                       help="emit machine-readable JSON instead of formatted output")
    group.add_argument("--no-color", action="store_true", default=argparse.SUPPRESS,
                       help="disable color and styling")
    group.add_argument("-q", "--quiet", action="store_true", default=argparse.SUPPRESS,
                       help="suppress progress output")
    group.add_argument("-v", "--verbose", action="store_true", default=argparse.SUPPRESS,
                       help="explain each step")


#: Global flag defaults, applied once after parsing. See :func:`_global_flags`.
GLOBAL_DEFAULTS = {
    "directory": None,
    "json_mode": False,
    "no_color": False,
    "quiet": False,
    "verbose": False,
}


def resolve_globals(args: argparse.Namespace) -> argparse.Namespace:
    """Fill in the global flags that were suppressed during parsing."""
    for name, default in GLOBAL_DEFAULTS.items():
        if not hasattr(args, name):
            setattr(args, name, default)
    return args


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="atlas",
        description=(
            f"{NAME} checks a repository against a written standard and tells you what is "
            "missing. Start with `atlas check`."
        ),
        epilog=EPILOG,
        formatter_class=AtlasHelpFormatter,
        add_help=True,
    )
    parser.add_argument(
        "--version", action="version", version=f"atlas {__version__}",
        help="print the version and exit",
    )
    _global_flags(parser)

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    for module in (
        init, status, doctor, check, validate, work, spec, prompt, library,
        site, template, completion,
    ):
        module.register(subparsers, _global_flags)  # type: ignore[attr-defined]
    return parser


# ------------------------------------------------------------------ reference

def _iter_subparsers(
    parser: argparse.ArgumentParser,
) -> t.Iterator[tuple[str, argparse.ArgumentParser]]:
    for action in parser._actions:  # noqa: SLF001 - argparse exposes no public API
        if isinstance(action, argparse._SubParsersAction):  # noqa: SLF001
            for name, sub in action.choices.items():
                yield name, sub


def command_tree() -> list[tuple[str, str, list[str]]]:
    """``(path, summary, flags)`` for every command, for docs and completion."""
    parser = build_parser()
    out: list[tuple[str, str, list[str]]] = []

    def walk(prefix: str, current: argparse.ArgumentParser) -> None:
        children = list(_iter_subparsers(current))
        for name, sub in children:
            path = f"{prefix}{name}".strip()
            flags = [
                option
                for action in sub._actions  # noqa: SLF001
                for option in action.option_strings
                if option.startswith("--") and option not in {"--help"}
            ]
            out.append((path, (sub.description or "").split("\n")[0].strip(), sorted(set(flags))))
            walk(f"{path} ", sub)

    walk("", parser)
    return out


def _format_arguments(parser: argparse.ArgumentParser) -> list[str]:
    lines: list[str] = []
    positionals = [
        a
        for a in parser._actions  # noqa: SLF001
        if not a.option_strings and not isinstance(a, argparse._SubParsersAction)  # noqa: SLF001
    ]
    if positionals:
        lines += ["| Argument | Required | Description |", "|---|---|---|"]
        for action in positionals:
            required = "no" if action.nargs in ("?", "*") else "yes"
            lines.append(
                f"| `{action.metavar or action.dest}` | {required} | {action.help or ''} |"
            )
        lines.append("")

    options = [
        a
        for a in parser._actions  # noqa: SLF001
        if a.option_strings and a.dest not in {"help", "directory", "json_mode", "quiet", "verbose"}
        and "--no-color" not in a.option_strings
    ]
    if options:
        lines += ["| Option | Default | Description |", "|---|---|---|"]
        for action in options:
            default = action.default
            shown = "—" if default in (None, False) else f"`{default}`"
            lines.append(
                f"| `{', '.join(action.option_strings)}` | {shown} | {action.help or ''} |"
            )
        lines.append("")
    return lines


def render_reference() -> str:
    """Render the full command reference as Markdown.

    Written to ``docs/reference/cli.md`` by ``atlas site build`` and checked in
    CI, so the committed reference is never out of date with the parser.
    """
    parser = build_parser()
    lines = [
        "# CLI reference",
        "",
        "<!-- GENERATED from the argument parser by `atlas site build --write-reference`.",
        "     Do not edit; change src/atlas/cli/ and regenerate. -->",
        "",
        f"Every command in `atlas` {__version__}. Generated from the parser itself, so it "
        "cannot drift from the tool.",
        "",
        "## Global options",
        "",
        "These are accepted by every command, before or after the subcommand.",
        "",
        "| Option | Description |",
        "|---|---|",
        "| `-C, --directory DIR` | Operate on the repository at `DIR` instead of the current one. |",
        "| `--json` | Emit machine-readable JSON instead of formatted output. |",
        "| `--no-color` | Disable color and styling. Also honoured: `NO_COLOR`. |",
        "| `-q, --quiet` | Suppress progress output. Errors still print to stderr. |",
        "| `-v, --verbose` | Explain each step. |",
        "| `--version` | Print the version and exit. |",
        "",
        "## Exit codes",
        "",
        "| Code | Meaning |",
        "|---|---|",
        "| `0` | Success. |",
        "| `1` | The command ran and found violations. |",
        "| `2` | The invocation was malformed. |",
        "| `3` | A named thing does not exist. |",
        "| `4` | Not run inside an Atlas repository. |",
        "| `70` | Internal error: always a bug in Atlas. |",
        "",
        "## Commands",
        "",
    ]

    def walk(prefix: str, current: argparse.ArgumentParser, depth: int) -> None:
        # `lines.extend`, not `lines +=`: augmented assignment inside a closure
        # rebinds the name locally and shadows the list being built.
        for name, sub in _iter_subparsers(current):
            path = f"{prefix}{name}".strip()
            heading = "#" * min(6, depth)
            lines.extend([f"{heading} `atlas {path}`", ""])
            description = textwrap.dedent(sub.description or "").strip()
            if description:
                lines.extend([description, ""])
            usage = " ".join(sub.format_usage().replace("usage: ", "").split())
            lines.extend(["```bash", usage, "```", ""])
            lines.extend(_format_arguments(sub))
            if sub.epilog:
                lines.extend(["```bash", textwrap.dedent(sub.epilog).strip(), "```", ""])
            walk(f"{path} ", sub, depth + 1)

    walk("", parser, 3)
    return "\n".join(lines).rstrip() + "\n"
