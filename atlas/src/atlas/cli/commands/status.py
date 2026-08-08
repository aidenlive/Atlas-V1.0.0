"""What is this repository, who owns it, and where does it stand?

One screen, read from the manifests and the generated indexes rather than from
memory. If a fact appears here, some file said it.
"""

from __future__ import annotations

import argparse

from ...core import compliance, prompts as prompts_mod, specs as specs_mod
from ...core import workstream as workstream_mod
from ...core.manifest import load_yaml
from ...errors import ExitCode
from ...paths import discover
from ...terminal import Console

SUMMARY = "show what this project is and where it stands"


def configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--check", action="store_true", help="also run the compliance gates")


def run(args: argparse.Namespace, console: Console) -> int:
    repo = discover(args.directory)
    manifest = load_yaml(repo.manifest_path)
    workstreams = workstream_mod.load_workstreams(repo.work_dir)
    tasks_done = sum(ws.done for ws in workstreams)
    tasks_total = sum(ws.total for ws in workstreams)

    payload = {
        "name": manifest.get("name"),
        "standard": manifest.get("standard"),
        "kind": manifest.get("kind"),
        "stage": manifest.get("stage"),
        "maturity": manifest.get("maturity"),
        "owner": manifest.get("owner"),
        "audiences": manifest.get("audiences", []),
        "root": str(repo.root),
        "standards": len(specs_mod.load_specs(repo.spec_dir)),
        "rules": len(specs_mod.all_rules(repo.spec_dir)),
        "prompts": len(prompts_mod.load_prompts(repo.prompts_dir)),
        "workstreams": len(workstreams),
        "tasks": {"done": tasks_done, "total": tasks_total},
    }

    exit_code = ExitCode.OK
    if args.check:
        report = compliance.run(repo)
        payload["check"] = report.as_dict()["summary"]
        if not report.ok:
            exit_code = ExitCode.VIOLATIONS

    if console.json_mode:
        console.json(payload)
        return int(exit_code)

    console.title(f"{payload['name']}  ·  {payload['stage']} / {payload['maturity']}")
    console.out()
    console.field("standard", str(payload["standard"]))
    console.field("kind", str(payload["kind"]))
    console.field("owner", str(payload["owner"]))
    console.field("audiences", ", ".join(payload["audiences"]) or "—")
    console.field("root", str(repo.root))
    console.out()
    console.field("standards", f"{payload['standards']} ({payload['rules']} rules)")
    console.field("prompts", str(payload["prompts"]))
    console.field(
        "work", f"{len(workstreams)} workstreams, {tasks_done}/{tasks_total} tasks done"
    )
    if workstreams:
        console.out()
        for ws in workstreams:
            console.out(f"  {ws.number}  {ws.title:<38}{ws.status:<10}{ws.done}/{ws.total}")
    if args.check:
        summary = payload["check"]
        console.out()
        console.state(
            "ok" if exit_code == ExitCode.OK else "fail",
            f"{summary['passed']} gates passed, {summary['failed']} failed",
            f"{summary['violations']} violations",
        )
    return int(exit_code)
