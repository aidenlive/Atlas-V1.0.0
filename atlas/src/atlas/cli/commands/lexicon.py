"""Ask the lexicon how we spell something, and why.

The lexicon is the one place that says what we call our things and which habits
of writing we have decided against. `atlas lint` reads the same file, so an
answer here is the answer the check will give.
"""

from __future__ import annotations

import argparse

from ...core import lexicon as lexicon_mod
from ...errors import ExitCode, UsageError
from ...paths import discover
from ...terminal import Console

SUMMARY = "look up a term or a phrasing decision"


def configure(parser: argparse.ArgumentParser) -> None:
    subparsers = parser.add_subparsers(dest="subcommand", metavar="<subcommand>")

    listing = subparsers.add_parser("list", help="list every term")
    listing.add_argument("--kind", help="only terms of this kind")

    find = subparsers.add_parser("find", help="look one up")
    find.add_argument("term", help="a word or part of one")

    subparsers.add_parser("phrases", help="list the phrases we replace")


def run(args: argparse.Namespace, console: Console) -> int:
    repo = discover(args.directory)
    lex = lexicon_mod.load_lexicon(repo.lexicon_path)
    subcommand = getattr(args, "subcommand", None) or "list"

    if subcommand == "list":
        terms = [t for t in lex.terms if not args.kind or t.kind == args.kind]
        return _terms(console, terms, f"{len(terms)} terms")
    if subcommand == "find":
        terms = lex.find(args.term)
        if not terms:
            if console.json_mode:
                console.json([])
            else:
                console.state("info", f"nothing in the lexicon matches {args.term!r}")
            return int(ExitCode.NOT_FOUND)
        return _terms(console, terms, f"{len(terms)} matches")
    if subcommand == "phrases":
        if console.json_mode:
            console.json([phrase.as_dict() for phrase in lex.phrases])
            return int(ExitCode.OK)
        console.title(f"{len(lex.phrases)} phrases")
        console.out()
        for phrase in lex.phrases:
            console.out(f"  {phrase.avoid:<28}→  {phrase.use}")
            if phrase.reason:
                console.note(f"  {'':<28}   {phrase.reason}")
        return int(ExitCode.OK)
    raise UsageError(f"unknown subcommand: {subcommand}")


def _terms(console: Console, terms, heading: str) -> int:
    if console.json_mode:
        console.json([term.as_dict() for term in terms])
        return int(ExitCode.OK)
    console.title(heading)
    console.out()
    for term in terms:
        console.out(f"  {term.use:<28}{term.kind}")
        if term.avoid:
            console.note(f"  {'':<28}not: {', '.join(term.avoid)}")
        if term.note:
            console.note(f"  {'':<28}{term.note}")
    return int(ExitCode.OK)
