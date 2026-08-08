"""The command tree.

Built on :mod:`argparse` deliberately. It is in the standard library, so
``pip install atlas-editorial`` pulls no CLI framework, and the tool starts in
milliseconds inside a pre-commit hook.

Two things are worth knowing about the shape here.

**The parser is the reference.** ``docs/reference/cli.md`` is rendered from this
tree by :func:`render_reference`, so a flag cannot exist without being
documented, and the documentation cannot describe a flag that does not exist.

**Help is grouped and exampled.** A flat alphabetical list of subcommands tells
a newcomer nothing about where to start, so commands are grouped by what you are
trying to do, and every group carries a worked example.
"""

from __future__ import annotations

import argparse
import typing as t

from .. import DESCRIPTION, NAME, STANDARD, __version__
from .commands import (
    check,
    completion,
    doctor,
    init,
    lexicon,
    lint,
    prompt,
    spec,
    status,
    validate,
    work,
)

__all__ = ["build_parser", "command_tree", "render_reference", "GROUPS", "EPILOG"]

#: Command groups, in the order a newcomer meets them.
GROUPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Start", ("init", "status", "doctor")),
    ("Verify", ("check", "lint", "validate")),
    ("Read", ("spec", "prompt", "lexicon")),
    ("Work", ("work",)),
    ("Shell", ("completion",)),
)

MODULES = {
    "init": init,
    "status": status,
    "doctor": doctor,
    "check": check,
    "lint": lint,
    "validate": validate,
    "spec": spec,
    "prompt": prompt,
    "lexicon": lexicon,
    "work": work,
    "completion": completion,
}

EPILOG = """\
examples:
  atlas check                              is this repository in order?
  atlas check --only content-declared      work one gate at a time
  atlas lint docs/guides/install.md        edit one document against the standards
  atlas lint --changed                     lint what this branch touched
  atlas status                             what is this, who owns it, where does it stand
  atlas spec show voice --rules            the rules a standard defines
  atlas lexicon find newsletter            how do we spell it, and why
  atlas prompt show write-guide            a written-once request to paste
  atlas work list --status blocked         what is stuck, and who owns it
  atlas check --json | jq '.checks[]'      output a script can read

exit codes: 0 ok · 1 violations found · 2 bad usage · 3 not found
            4 not an Atlas repository
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

    Attached to each subparser as well as the root, so both ``atlas --json
    check`` and ``atlas check --json`` work. People type them in either order,
    and being right about which one is "correct" is not worth a usage error.

    Every one uses ``default=SUPPRESS``. This matters: argparse applies a
    subparser's defaults *after* the parent has parsed, so an ordinary default on
    the subparser copy would silently overwrite a value the parent already read,
    and ``atlas -C /elsewhere check`` would quietly check the wrong directory.
    """
    group = parser.add_argument_group("global options")
    group.add_argument(
        "-C", "--directory", metavar="DIR", default=argparse.SUPPRESS,
        help="operate on the repository at DIR instead of the current one",
    )
    group.add_argument(
        "--json", action="store_true", dest="json_mode", default=argparse.SUPPRESS,
        help="emit machine-readable JSON instead of formatted output",
    )
    group.add_argument(
        "--no-color", action="store_true", default=argparse.SUPPRESS,
        help="disable color and styling",
    )
    group.add_argument(
        "-q", "--quiet", action="store_true", default=argparse.SUPPRESS,
        help="suppress progress output",
    )
    group.add_argument(
        "-v", "--verbose", action="store_true", default=argparse.SUPPRESS,
        help="explain each step",
    )


#: Applied once after parsing. See :func:`_global_flags`.
GLOBAL_DEFAULTS: dict[str, t.Any] = {
    "directory": None,
    "json_mode": False,
    "no_color": False,
    "quiet": False,
    "verbose": False,
}


def resolve_globals(namespace: argparse.Namespace) -> argparse.Namespace:
    for key, value in GLOBAL_DEFAULTS.items():
        if not hasattr(namespace, key):
            setattr(namespace, key, value)
    return namespace


def _grouped_help() -> str:
    lines = ["", "commands:"]
    for title, names in GROUPS:
        lines.append(f"  {title}")
        for name in names:
            lines.append(f"    {name:<12}{MODULES[name].SUMMARY}")
        lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=NAME,
        description=f"{DESCRIPTION}\nstandard: {STANDARD}\n{_grouped_help()}",
        epilog=EPILOG,
        formatter_class=AtlasHelpFormatter,
        add_help=True,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__} ({STANDARD})")
    _global_flags(parser)

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    for name, module in MODULES.items():
        subparser = subparsers.add_parser(
            name,
            help=module.SUMMARY,
            description=module.__doc__,
            formatter_class=AtlasHelpFormatter,
        )
        module.configure(subparser)
        _global_flags(subparser)
        # Nested subcommands (`atlas work list`, `atlas spec rules`) get them
        # too, or `atlas spec rules --json` would be a usage error while
        # `atlas --json spec rules` worked. Same flag, same command, either
        # position.
        for action in subparser._actions:  # noqa: SLF001
            if isinstance(action, argparse._SubParsersAction):  # noqa: SLF001
                for nested in action.choices.values():
                    _global_flags(nested)
        subparser.set_defaults(handler=module.run)
    return parser


def command_tree(parser: argparse.ArgumentParser | None = None) -> list[dict[str, t.Any]]:
    """The parser, as data: what the reference and the tests both read."""
    parser = parser or build_parser()
    tree: list[dict[str, t.Any]] = []
    for action in parser._actions:  # noqa: SLF001 - argparse exposes no public API
        if not isinstance(action, argparse._SubParsersAction):  # noqa: SLF001
            continue
        for name, subparser in action.choices.items():
            tree.append(
                {
                    "name": name,
                    "summary": MODULES[name].SUMMARY if name in MODULES else "",
                    "usage": subparser.format_usage().replace("usage: ", "").strip(),
                    "options": _options(subparser),
                    "subcommands": _subcommands(subparser),
                }
            )
    return tree


def _options(parser: argparse.ArgumentParser) -> list[dict[str, str]]:
    options: list[dict[str, str]] = []
    for action in parser._actions:  # noqa: SLF001
        if isinstance(action, argparse._SubParsersAction):  # noqa: SLF001
            continue
        if action.dest in {"help"} or action.dest in GLOBAL_DEFAULTS:
            continue
        flags = ", ".join(action.option_strings) or action.dest
        options.append({"flags": flags, "help": action.help or ""})
    return options


def _subcommands(parser: argparse.ArgumentParser) -> list[dict[str, t.Any]]:
    out: list[dict[str, t.Any]] = []
    for action in parser._actions:  # noqa: SLF001
        if not isinstance(action, argparse._SubParsersAction):  # noqa: SLF001
            continue
        for name, subparser in action.choices.items():
            out.append(
                {
                    "name": name,
                    "usage": subparser.format_usage().replace("usage: ", "").strip(),
                    "help": action._choices_actions and next(  # noqa: SLF001
                        (c.help or "" for c in action._choices_actions if c.dest == name), ""  # noqa: SLF001
                    ) or "",
                    "options": _options(subparser),
                }
            )
    return out


def render_reference() -> str:
    """Render ``docs/reference/cli.md`` from the parser itself."""
    import datetime as dt

    tree = {entry["name"]: entry for entry in command_tree()}
    lines = [
        "---",
        "title: CLI reference",
        "kind: reference",
        "owner: role:editorial-lead",
        "status: published",
        f"updated: {dt.date.today().isoformat()}",
        "generated_by: scripts/build_reference.py",
        "---",
        "",
        "<!-- Generated from the argument parser. Do not edit by hand. -->",
        "",
        "# CLI reference",
        "",
        f"`atlas` {__version__}, enforcing standard `{STANDARD}`.",
        "",
        "Every command accepts the global flags below, before or after the",
        "command name. Exit codes: `0` ok, `1` violations found, `2` bad usage,",
        "`3` not found, `4` not an Atlas repository.",
        "",
        "| Flag | Does |",
        "|---|---|",
        "| `-C, --directory DIR` | operate on the repository at DIR |",
        "| `--json` | emit machine-readable JSON |",
        "| `--no-color` | disable color and styling |",
        "| `-q, --quiet` | suppress progress output |",
        "| `-v, --verbose` | explain each step |",
        "",
    ]
    for title, names in GROUPS:
        lines += [f"## {title}", ""]
        for name in names:
            entry = tree[name]
            lines += [f"### `atlas {name}`", "", entry["summary"], "", "```text", entry["usage"], "```", ""]
            if entry["subcommands"]:
                lines += ["| Subcommand | Does |", "|---|---|"]
                for sub in entry["subcommands"]:
                    lines.append(f"| `{name} {sub['name']}` | {sub['help']} |")
                lines.append("")
            if entry["options"]:
                lines += ["| Option | Does |", "|---|---|"]
                for option in entry["options"]:
                    lines.append(f"| `{option['flags']}` | {option['help']} |")
                lines.append("")
    return "\n".join(lines).rstrip() + "\n"
