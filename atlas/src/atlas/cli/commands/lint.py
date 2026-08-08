"""Edit one document against the standards.

``atlas check`` asks whether the repository is in order. ``atlas lint`` asks
whether a piece of writing is: what it declares, how it is shaped, which words
it uses. Errors fail the run; warnings are judgement calls and do not, unless
you pass ``--strict``.
"""

from __future__ import annotations

import argparse
import pathlib
import subprocess

from ...core import compliance, lexicon as lexicon_mod, lint as lint_mod
from ...core.manifest import load_yaml
from ...errors import ExitCode, UsageError
from ...paths import discover
from ...terminal import Console

SUMMARY = "check a document against the editorial standards"


def _plural(count: int, noun: str) -> str:
    """`1 file`, `2 files`. An editorial tool does not write "1 files"."""
    return f"{count} {noun}" if count == 1 else f"{count} {noun}s"


def configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("paths", nargs="*", metavar="PATH", help="files or directories to lint")
    parser.add_argument(
        "--only", metavar="RULE", action="append", help="run only this lint rule (repeatable)"
    )
    parser.add_argument("--skip", metavar="RULE", action="append", help="skip this lint rule (repeatable)")
    parser.add_argument("--changed", action="store_true", help="lint Markdown changed against the default branch")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--list", action="store_true", help="list the lint rules and exit")


def run(args: argparse.Namespace, console: Console) -> int:
    if args.list:
        return _list(console)

    repo = discover(args.directory)
    lex = lexicon_mod.load_lexicon(repo.lexicon_path)
    settings = lint_mod.Settings.from_manifest(load_yaml(repo.manifest_path))

    paths = _targets(args, repo)
    if not paths:
        raise UsageError(
            "nothing to lint",
            hint="pass a path, or use --changed inside a git repository",
        )

    results = lint_mod.lint_paths(paths, lex, settings, only=args.only, skip=args.skip)
    errors = sum(len(result.errors) for result in results)
    warnings = sum(len(result.warnings) for result in results)

    if console.json_mode:
        console.json(
            {
                "ok": errors == 0 and (warnings == 0 or not args.strict),
                "files": len(results),
                "errors": errors,
                "warnings": warnings,
                "results": [result.as_dict() for result in results if result.findings],
            }
        )
    else:
        console.title(f"atlas lint · {_plural(len(results), 'file')}")
        console.out()
        for result in results:
            if result.ok:
                console.step(f"ok  {repo.relative(result.path)}")
                continue
            console.state(
                "fail" if result.errors else "warn",
                repo.relative(result.path),
                f"{_plural(len(result.errors), 'error')}, "
                f"{_plural(len(result.warnings), 'warning')}",
            )
            for finding in result.findings:
                # The severity is on every line, not only in the header count.
                # Without it a reader cannot tell which three of fifteen
                # findings are the ones that fail the run.
                console.bullet(
                    f"{finding.line:>4}  {finding.severity:<5}  {finding.message}"
                    f"  [{finding.rule}]"
                )
                if finding.hint and console.verbose:
                    console.bullet(f"↳ {finding.hint}", indent=8)
        console.out()
        if errors or warnings:
            console.state(
                "fail" if errors else "warn",
                f"{_plural(errors, 'error')}, {_plural(warnings, 'warning')} "
                f"across {_plural(len(results), 'file')}",
            )
        else:
            console.state("ok", f"{_plural(len(results), 'file')} clean")

    if errors or (args.strict and warnings):
        return int(ExitCode.VIOLATIONS)
    return int(ExitCode.OK)


def _targets(args: argparse.Namespace, repo) -> list[pathlib.Path]:
    if args.changed:
        return _changed(repo.root)
    if not args.paths:
        return [
            path
            for directory in compliance.DECLARED_CONTENT_DIRS
            for path in repo.walk_markdown(directory)
        ]
    found: list[pathlib.Path] = []
    for raw in args.paths:
        path = pathlib.Path(raw)
        if path.is_dir():
            found.extend(sorted(path.rglob("*.md")))
        elif path.is_file():
            found.append(path)
        else:
            raise UsageError(f"no such file or directory: {raw}")
    return found


def _changed(root: pathlib.Path) -> list[pathlib.Path]:
    """Markdown this branch touched, according to git."""
    try:
        merge_base = subprocess.run(
            ["git", "merge-base", "HEAD", "origin/main"],
            cwd=root, capture_output=True, text=True, check=False,
        )
        base = merge_base.stdout.strip() or "HEAD~1"
        diff = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=d", base],
            cwd=root, capture_output=True, text=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise UsageError("could not ask git what changed", hint=str(exc)) from exc
    return [
        root / name
        for name in diff.stdout.split()
        if name.endswith(".md") and (root / name).is_file()
    ]


def _list(console: Console) -> int:
    if console.json_mode:
        console.json(
            [
                {"name": name, "summary": summary, "rule": rule}
                for name, (summary, rule, _fn) in lint_mod.RULES.items()
            ]
        )
        return int(ExitCode.OK)
    console.title(f"{len(lint_mod.RULES)} lint rules")
    console.out()
    for name, (summary, rule, _fn) in lint_mod.RULES.items():
        console.out(f"  {name:<20}{summary}")
        console.note(f"  {'':<20}{rule}")
    return int(ExitCode.OK)
