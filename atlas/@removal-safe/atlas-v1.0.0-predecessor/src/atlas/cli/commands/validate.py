"""``atlas validate``: schema-validate manifests."""

from __future__ import annotations

import argparse
import pathlib
import typing as t

from ...core.manifest import validate_file
from ...errors import ExitCode
from ...terminal import Style

if t.TYPE_CHECKING:  # pragma: no cover
    from .. import Context


def register(subparsers: t.Any, add_global_flags: t.Callable[..., None]) -> None:
    parser = subparsers.add_parser(
        "validate",
        help="check that a manifest is filled in correctly",
        description=(
            "Validate one or more manifests. The schema is chosen from the manifest's own "
            "`standard:` field and content, never from its filename, so a manifest is equally "
            "valid at examples/acme.org.yaml and at org.yaml. Expired waivers are failures."
        ),
        epilog=(
            "atlas validate project.yaml\n"
            "atlas validate examples/*.yaml\n"
            "atlas validate --all"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("files", nargs="*", metavar="FILE", help="manifests to validate")
    parser.add_argument(
        "--all", action="store_true", dest="validate_all",
        help="validate project.yaml plus every manifest in examples/",
    )
    add_global_flags(parser)
    parser.set_defaults(handler=run)


def run(ctx: Context) -> ExitCode:
    console = ctx.console
    targets = [pathlib.Path(f) for f in ctx.args.files]

    if ctx.args.validate_all or not targets:
        repo = ctx.repo
        targets = [repo.manifest] if repo.manifest.exists() else []
        if repo.examples.is_dir():
            targets += sorted(repo.examples.glob("*.yaml"))
        if not targets:
            console.status("skip", "no manifests found")
            return ExitCode.OK

    results = []
    failed = 0
    for path in targets:
        violations = validate_file(path, ctx.repo.schemas)
        results.append(
            {"path": str(path), "ok": not violations,
             "violations": [v.as_dict() for v in violations]}
        )
        if violations:
            failed += 1
            console.status("fail", str(path))
            for violation in violations:
                console.write(f"    {console.paint(violation.render(), Style.RED)}")
        else:
            console.status("ok", str(path))

    console.emit({"ok": failed == 0, "checked": len(targets), "results": results})
    console.write()
    if failed:
        console.status("fail", f"{failed} of {len(targets)} manifest(s) invalid")
        return ExitCode.FAILURE
    console.status("ok", f"{len(targets)} manifest(s) valid")
    return ExitCode.OK
