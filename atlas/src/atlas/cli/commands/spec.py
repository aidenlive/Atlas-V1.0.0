"""Read the standards, and cite their rules.

The standards are prose files, so they can be read in any editor. This command
exists for the two things an editor cannot do: list the suite as a table, and
pull every numbered rule out of a standard without anyone maintaining a second
copy of them.
"""

from __future__ import annotations

import argparse

from ...core import specs as specs_mod
from ...errors import ExitCode, UsageError
from ...paths import discover
from ...terminal import Console

SUMMARY = "read the standards and cite their rules"


def configure(parser: argparse.ArgumentParser) -> None:
    subparsers = parser.add_subparsers(dest="subcommand", metavar="<subcommand>")
    subparsers.add_parser("list", help="list the standards")

    show = subparsers.add_parser("show", help="show one standard")
    show.add_argument("name", help="standard id, e.g. voice")
    show.add_argument("--rules", action="store_true", help="list its rules instead of its prose")

    rules = subparsers.add_parser("rules", help="list every rule in the suite")
    rules.add_argument("--grep", metavar="WORD", help="only rules mentioning WORD")


def run(args: argparse.Namespace, console: Console) -> int:
    repo = discover(args.directory)
    subcommand = getattr(args, "subcommand", None) or "list"
    if subcommand == "list":
        return _list(console, repo)
    if subcommand == "show":
        return _show(args, console, repo)
    if subcommand == "rules":
        return _rules(args, console, repo)
    raise UsageError(f"unknown subcommand: {subcommand}")


def _list(console: Console, repo) -> int:
    specs = specs_mod.load_specs(repo.spec_dir)
    if console.json_mode:
        console.json([spec.as_dict() for spec in specs])
        return int(ExitCode.OK)
    if not specs:
        console.state("info", "this repository does not carry the standards")
        return int(ExitCode.OK)
    console.title(f"{len(specs)} standards")
    console.out()
    for spec in specs:
        console.out(f"  {spec.id:<14}{spec.question}")
        console.note(f"  {'':<14}{len(spec.rules)} rules · {spec.rule_prefix}nn · v{spec.meta.get('version')}")
    return int(ExitCode.OK)


def _show(args: argparse.Namespace, console: Console, repo) -> int:
    spec = specs_mod.find_spec(repo.spec_dir, args.name)
    if console.json_mode:
        console.json(spec.as_dict(with_rules=args.rules))
        return int(ExitCode.OK)
    if args.rules:
        console.title(f"{spec.title} · {len(spec.rules)} rules")
        console.out()
        for rule in spec.rules:
            console.out(f"  {rule.id}  {rule.title}")
            console.note(f"        {rule.text}")
        return int(ExitCode.OK)
    console.out(spec.body)
    return int(ExitCode.OK)


def _rules(args: argparse.Namespace, console: Console, repo) -> int:
    rules = specs_mod.all_rules(repo.spec_dir)
    if args.grep:
        needle = args.grep.lower()
        rules = [r for r in rules if needle in r.title.lower() or needle in r.text.lower()]
    if console.json_mode:
        console.json([rule.as_dict() for rule in rules])
        return int(ExitCode.OK)
    console.title(f"{len(rules)} rules")
    console.out()
    for rule in rules:
        console.out(f"  {rule.id:<8}{rule.title:<34}{rule.spec}")
    return int(ExitCode.OK)
