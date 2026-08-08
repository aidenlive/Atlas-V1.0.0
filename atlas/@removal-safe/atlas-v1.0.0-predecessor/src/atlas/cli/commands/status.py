"""``atlas status``: what this repository is, and where it stands."""

from __future__ import annotations

import typing as t

from ...core import prompts as prompts_mod
from ...core import specs as specs_mod
from ...core import workstream as ws
from ...core.manifest import load_manifest
from ...errors import ExitCode
from ...terminal import Style

if t.TYPE_CHECKING:  # pragma: no cover
    from .. import Context


def register(subparsers: t.Any, add_global_flags: t.Callable[..., None]) -> None:
    parser = subparsers.add_parser(
        "status",
        help="show what this project is and where it stands",
        description=(
            "One screen covering how this project is classified, who owns it, what work is "
            "live, and what is blocked. Every value is read from the declared manifest rather "
            "than guessed from the files, so this is what the repository says about itself. "
            "Where the claim and reality disagree, `atlas check` is what finds out."
        ),
    )
    add_global_flags(parser)
    parser.set_defaults(handler=run)


def run(ctx: Context) -> ExitCode:
    repo = ctx.repo
    console = ctx.console
    manifest = load_manifest(repo.manifest) if repo.manifest.exists() else None
    data = manifest.data if manifest else {}

    workstreams = ws.load_all(repo) if repo.has_workstreams() else []
    live = [w for w in workstreams if not w.archived]
    blocked = [w for w in live if w.status == "blocked"]
    specs = specs_mod.load_specs(repo.spec)

    prompt_count = 0
    if (repo.prompts / "index.yaml").exists():
        try:
            prompt_count = len(prompts_mod.load(repo).prompts)
        except Exception:  # noqa: BLE001 - status must not fail on a broken catalog
            prompt_count = 0

    payload = {
        "name": data.get("name", repo.root.name),
        "root": str(repo.root),
        "standard": data.get("standard"),
        "type": data.get("type"),
        "stage": data.get("stage"),
        "maturity": data.get("maturity"),
        "owner": data.get("owner"),
        "support": data.get("support"),
        "visibility": data.get("visibility"),
        "specs": len(specs),
        "prompts": prompt_count,
        "workstreams": {
            "live": len(live),
            "archived": len(workstreams) - len(live),
            "blocked": len(blocked),
            "tasks_done": sum(w.done for w in live),
            "tasks_total": sum(w.total for w in live),
        },
    }
    console.emit(payload)

    console.title(str(payload["name"]), str(repo.root))
    console.definitions(
        [
            ("standard", str(data.get("standard", "—"))),
            ("type", str(data.get("type", "—"))),
            ("stage", str(data.get("stage", "—"))),
            ("maturity", str(data.get("maturity", "—"))),
            ("owner", str(data.get("owner", "—"))),
            ("support", str(data.get("support", "—"))),
            ("visibility", str(data.get("visibility", "—"))),
        ]
    )

    console.write()
    console.rule("contents")
    console.definitions(
        [
            ("standards", str(len(specs)) if specs else "—"),
            ("prompts", str(prompt_count) if prompt_count else "—"),
            (
                "workstreams",
                f"{len(live)} live, {len(workstreams) - len(live)} archived"
                if workstreams
                else "—",
            ),
        ]
    )

    if live:
        console.write()
        console.rule("live work")
        order = {status: i for i, status in enumerate(ws.STATUS_ORDER)}
        console.table(
            ["#", "WORKSTREAM", "STATUS", "PROGRESS"],
            [
                (w.id, w.title, w.status, console.progress(w.done, w.total, width=12))
                for w in sorted(live, key=lambda w: (order.get(w.status, 99), w.id))
            ],
        )

    if blocked:
        console.write()
        console.status("warn", f"{len(blocked)} workstream(s) blocked",
                       ", ".join(w.id for w in blocked))

    console.write()
    console.detail("Run `atlas check` to verify compliance.")
    return ExitCode.OK
