"""Manifests: the facts a repository states about itself.

Two files carry them. ``project.yaml`` says what this body of content is, what
stage it is in, and who owns it. ``authority.yaml`` says who may write, review,
and approve. Both are validated against JSON Schemas in ``spec/schemas/``, so a
typo is a failed check rather than a surprise six months later.
"""

from __future__ import annotations

import dataclasses
import json
import pathlib
import typing as t

import yaml

from ..errors import NotFoundError

__all__ = [
    "Violation",
    "Manifest",
    "load_yaml",
    "load_manifest",
    "load_schema",
    "validate_against_schema",
    "validate_manifest",
    "KIND_SCHEMAS",
]

#: manifest kind -> schema filename in spec/schemas/.
KIND_SCHEMAS: dict[str, str] = {
    "project": "project.schema.json",
    "authority": "authority.schema.json",
    "content": "content.schema.json",
    "workstream": "workstream.schema.json",
}


@dataclasses.dataclass(frozen=True)
class Violation:
    """One thing that is not true yet.

    A violation names the rule it breaks and, where it can, the file and line,
    so an editor, a CI annotation, and a person all read the same record.
    """

    rule: str
    message: str
    path: str | None = None
    line: int | None = None
    hint: str | None = None

    @property
    def location(self) -> str:
        if self.path and self.line:
            return f"{self.path}:{self.line}"
        return self.path or ""

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "rule": self.rule,
            "message": self.message,
            "path": self.path,
            "line": self.line,
            "hint": self.hint,
        }

    def __str__(self) -> str:
        where = f" ({self.location})" if self.location else ""
        return f"{self.rule}: {self.message}{where}"


@dataclasses.dataclass(frozen=True)
class Manifest:
    """A parsed manifest and where it came from."""

    kind: str
    path: pathlib.Path
    data: dict[str, t.Any]

    def get(self, key: str, default: t.Any = None) -> t.Any:
        return self.data.get(key, default)

    @property
    def name(self) -> str:
        return str(self.data.get("name", self.path.parent.name))


def _normalise(value: t.Any) -> t.Any:
    """Turn dates back into ISO strings.

    YAML parses an unquoted ``2026-08-08`` into a ``date`` object, which then
    fails a schema expecting a string. Writers should not have to quote a date
    to satisfy a parser, so the loader does it for them (LANGUAGE L-07).
    """
    import datetime

    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _normalise(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalise(item) for item in value]
    return value


def load_yaml(path: pathlib.Path) -> dict[str, t.Any]:
    """Parse a YAML document, raising a readable error instead of a traceback."""
    if not path.is_file():
        raise NotFoundError(f"{path} does not exist")
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:  # pragma: no cover - message shape varies
        raise NotFoundError(f"{path} is not valid YAML: {exc}") from exc
    if not isinstance(loaded, dict):
        raise NotFoundError(f"{path} must contain a mapping at the top level")
    return _normalise(loaded)


def load_manifest(path: pathlib.Path, kind: str = "project") -> Manifest:
    return Manifest(kind=kind, path=path, data=load_yaml(path))


def load_schema(schema_dir: pathlib.Path, kind: str) -> dict[str, t.Any]:
    filename = KIND_SCHEMAS.get(kind)
    if filename is None:
        raise NotFoundError(
            f"unknown manifest kind: {kind}",
            hint=f"known kinds: {', '.join(sorted(KIND_SCHEMAS))}",
        )
    path = schema_dir / filename
    if not path.is_file():
        raise NotFoundError(f"schema not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_against_schema(
    data: dict[str, t.Any], schema: dict[str, t.Any], *, source: str, rule: str
) -> list[Violation]:
    """Validate ``data``, returning violations rather than raising.

    Every error is reported, not just the first, because fixing a manifest one
    round-trip at a time is the slowest possible way to fix a manifest.
    """
    try:
        import jsonschema
    except ModuleNotFoundError:  # pragma: no cover - dependency is declared
        return [
            Violation(
                rule=rule,
                message="jsonschema is not installed, so this manifest could not be validated",
                path=source,
                hint="pip install atlas-editorial",
            )
        ]

    validator = jsonschema.Draft202012Validator(schema)
    violations: list[Violation] = []
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        where = ".".join(str(part) for part in error.path) or "(root)"
        violations.append(
            Violation(rule=rule, message=f"{where}: {error.message}", path=source)
        )
    return violations


def validate_manifest(
    path: pathlib.Path, schema_dir: pathlib.Path, kind: str = "project"
) -> list[Violation]:
    """Load and validate one manifest file."""
    rule = {"project": "CONTENT C-01", "authority": "AUTHORITY A-01"}.get(kind, "CONTENT C-01")
    data = load_yaml(path)
    schema = load_schema(schema_dir, kind)
    return validate_against_schema(data, schema, source=path.name, rule=rule)


def detect_kind(path: pathlib.Path) -> str:
    """Guess a manifest's kind from its filename.

    ``authority.yaml`` and ``payments.workstream.yaml`` are unambiguous; anything
    else is treated as a project manifest, which is the common case.
    """
    name = path.name
    for kind in KIND_SCHEMAS:
        if name == f"{kind}.yaml" or name.endswith(f".{kind}.yaml"):
            return kind
    return "project"
