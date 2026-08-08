"""Manifest loading and schema validation.

A manifest is any YAML file carrying a ``standard:`` field. Which schema
applies is decided from the manifest's own *content*, never from its filename,
so a manifest is equally valid at ``examples/acme.org.yaml`` and at
``org.yaml``. Dispatching on filenames is what made the first version of this
code crash on the example it shipped with.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import functools
import json
import pathlib
import typing as t

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from ..errors import NotFoundError, UsageError

__all__ = [
    "Manifest",
    "Violation",
    "load_yaml",
    "normalize",
    "schema_for",
    "validate_file",
    "validate_manifest",
    "check_waivers",
]


@dataclasses.dataclass(frozen=True)
class Violation:
    """One failed assertion, addressable enough to fix without a search.

    ``rule`` carries the identifier from the specification where one exists
    (``P-02``, ``W-13``); ``docs/reference/rule-ids.md`` explains the format.
    """

    path: str
    message: str
    rule: str | None = None
    pointer: str | None = None

    def render(self) -> str:
        where = f"{self.path}"
        if self.pointer:
            where += f":{self.pointer}"
        rule = f" ({self.rule})" if self.rule else ""
        return f"{where}: {self.message}{rule}"

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "path": self.path,
            "pointer": self.pointer,
            "message": self.message,
            "rule": self.rule,
        }


@dataclasses.dataclass(frozen=True)
class Manifest:
    """A parsed manifest and where it came from."""

    path: pathlib.Path
    data: dict[str, t.Any]

    @property
    def standard(self) -> str | None:
        return self.data.get("standard")

    @property
    def name(self) -> str:
        return self.data.get("name") or self.path.stem

    def get(self, key: str, default: t.Any = None) -> t.Any:
        return self.data.get(key, default)


def normalize(obj: t.Any) -> t.Any:
    """Recursively convert YAML date objects to ISO strings.

    PyYAML parses a bare ``2026-01-31`` into ``datetime.date``; JSON Schema's
    ``format: date`` expects a string. Normalising on load means every consumer
    downstream sees one type.
    """
    if isinstance(obj, dt.datetime):
        return obj.isoformat()
    if isinstance(obj, dt.date):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: normalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize(v) for v in obj]
    return obj


def load_yaml(path: pathlib.Path) -> t.Any:
    """Read and parse a YAML file, with errors that name the file."""
    if not path.exists():
        raise NotFoundError(f"no such file: {path}")
    try:
        return normalize(yaml.safe_load(path.read_text(encoding="utf-8")))
    except yaml.YAMLError as exc:  # pragma: no cover - message shape varies
        raise UsageError(f"{path}: not valid YAML: {exc}") from exc


def load_manifest(path: pathlib.Path) -> Manifest:
    data = load_yaml(path)
    if not isinstance(data, dict):
        raise UsageError(f"{path}: manifest must be a mapping, got {type(data).__name__}")
    return Manifest(path, data)


def schema_for(manifest: Manifest, schemas: pathlib.Path) -> pathlib.Path:
    """Resolve the schema a manifest declares itself against.

    ADMIN ships two shapes under one ``standard:`` value. They are told apart
    by the keys they declare: an organisation manifest names an ``org:``, a
    solo manifest names a ``profile:``, because there is no other honest
    signal, and the filename is not a signal at all.
    """
    standard = manifest.standard
    if standard == "project/1.0":
        return schemas / "project.schema.json"
    if standard == "workstream/1.0":
        return schemas / "workstream.schema.json"
    if standard == "admin/1.0":
        if "org" in manifest.data or "teams" in manifest.data:
            return schemas / "org.schema.json"
        if "profile" in manifest.data or "owner" in manifest.data:
            return schemas / "admin.schema.json"
        raise UsageError(
            f"{manifest.path}: admin manifest declares neither an organisation "
            f"(`org:`/`teams:`) nor a solo profile (`profile:`/`owner:`)",
            hint="Add `org:` for an organisation manifest, or `profile:` for a solo one.",
        )
    raise UsageError(
        f"{manifest.path}: unknown or missing `standard:` field: {standard!r}",
        hint="Declare one of: project/1.0, workstream/1.0, admin/1.0.",
    )


@functools.lru_cache(maxsize=16)
def _validator(schema_path: pathlib.Path) -> Draft202012Validator:
    if not schema_path.exists():
        raise NotFoundError(f"schema not found: {schema_path}")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return Draft202012Validator(schema, format_checker=FormatChecker())


def check_waivers(data: dict[str, t.Any], today: dt.date | None = None) -> list[str]:
    """Return messages for waivers that have lapsed.

    CHECKLIST is explicit that an expired waiver is a failure, not a warning: a
    waiver is a dated promise to come back, and a promise with no enforcement
    is just a comment.
    """
    today = today or dt.date.today()
    messages: list[str] = []
    for waiver in data.get("waivers") or []:
        if not isinstance(waiver, dict):
            messages.append(f"waiver {waiver!r}: not a mapping")
            continue
        raw = waiver.get("until")
        try:
            until = dt.date.fromisoformat(str(raw))
        except (TypeError, ValueError):
            messages.append(f"waiver {waiver.get('id')}: invalid `until` date {raw!r}")
            continue
        if until < today:
            messages.append(
                f"waiver {waiver.get('id')}: expired {until.isoformat()} "
                f"(expired waivers are failures)"
            )
    return messages


def validate_manifest(
    manifest: Manifest,
    schemas: pathlib.Path,
    *,
    today: dt.date | None = None,
) -> list[Violation]:
    """Validate a parsed manifest, returning violations in document order."""
    schema_path = schema_for(manifest, schemas)
    validator = _validator(schema_path)
    rel = manifest.path.name
    violations = [
        Violation(
            path=rel,
            pointer="/".join(str(p) for p in error.path) or None,
            message=error.message,
        )
        for error in sorted(validator.iter_errors(manifest.data), key=lambda e: list(e.path))
    ]
    violations += [
        Violation(path=rel, message=message, rule="CHECKLIST")
        for message in check_waivers(manifest.data, today)
    ]
    return violations


def validate_file(
    path: pathlib.Path,
    schemas: pathlib.Path,
    *,
    today: dt.date | None = None,
) -> list[Violation]:
    """Load and validate one manifest file."""
    return validate_manifest(load_manifest(path), schemas, today=today)
