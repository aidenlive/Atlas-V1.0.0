"""Check that a manifest is filled in correctly.

Where `check` runs every gate over a repository, `validate` answers one narrow
question about one file, which is what you want in a pre-commit hook or while
writing the file itself.
"""

from __future__ import annotations

import argparse
import pathlib

from ...core.manifest import KIND_SCHEMAS, detect_kind, validate_manifest
from ...errors import ExitCode, UsageError
from ...paths import discover
from ...terminal import Console

SUMMARY = "check that a manifest is filled in correctly"


def configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("paths", nargs="+", metavar="PATH", help="manifest files to validate")
    parser.add_argument(
        "--kind", choices=sorted(KIND_SCHEMAS), help="force a schema instead of inferring it"
    )


def run(args: argparse.Namespace, console: Console) -> int:
    repo = discover(args.directory)
    results = []
    for raw in args.paths:
        path = pathlib.Path(raw)
        if not path.is_file():
            raise UsageError(f"no such file: {raw}")
        kind = args.kind or detect_kind(path)
        violations = validate_manifest(path, repo.schema_dir, kind)
        results.append((path, kind, violations))

    total = sum(len(violations) for _, _, violations in results)

    if console.json_mode:
        console.json(
            {
                "ok": total == 0,
                "files": [
                    {
                        "path": str(path),
                        "kind": kind,
                        "violations": [v.as_dict() for v in violations],
                    }
                    for path, kind, violations in results
                ],
            }
        )
        return int(ExitCode.OK if total == 0 else ExitCode.VIOLATIONS)

    for path, kind, violations in results:
        console.state(
            "ok" if not violations else "fail", f"{path}", f"{kind} schema"
        )
        for violation in violations:
            console.bullet(violation.message)
    return int(ExitCode.OK if total == 0 else ExitCode.VIOLATIONS)
