"""The standards, read as data.

Each standard in ``spec/`` opens with a block of machine-readable metadata: its
id, order, title, the question it answers, its version, status, rule prefix, and
companions. A tool can therefore discover what the suite covers without reading
a word of the prose, and the CLI can list every rule a standard defines without
anyone maintaining a second list of them.

Rules are written in one shape and one shape only::

    - **V-03 Plain words.** Prefer the shorter word where it means the same.

Anything matching that shape *is* a rule. There is no separate registry to keep
in step, which is the point: the prose and the rule index cannot disagree.
"""

from __future__ import annotations

import dataclasses
import pathlib
import re
import typing as t

from ..errors import NotFoundError
from . import frontmatter

__all__ = ["Rule", "Spec", "load_spec", "load_specs", "find_spec", "all_rules", "RULE_PATTERN"]

#: `- **V-03 Plain words.** …` — id, then a short title, then the requirement.
RULE_PATTERN = re.compile(r"^\s*[-*]\s+\*\*(?P<id>[A-Z]{1,4}-\d{2})\s+(?P<title>[^*]+?)\*\*\s*(?P<text>.*)$")

#: Metadata every standard must declare. Enforced by `atlas check`.
REQUIRED_META = ("id", "order", "title", "question", "version", "status", "rule_prefix")


@dataclasses.dataclass(frozen=True)
class Rule:
    """One numbered requirement."""

    id: str
    title: str
    text: str
    spec: str
    line: int

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "spec": self.spec,
            "line": self.line,
        }


@dataclasses.dataclass(frozen=True)
class Spec:
    """One standard: its declared metadata, its prose, and its rules."""

    id: str
    path: pathlib.Path
    meta: dict[str, t.Any]
    body: str
    rules: tuple[Rule, ...]

    @property
    def title(self) -> str:
        return str(self.meta.get("title", self.id.upper()))

    @property
    def question(self) -> str:
        return str(self.meta.get("question", ""))

    @property
    def order(self) -> int:
        try:
            return int(self.meta.get("order", 99))
        except (TypeError, ValueError):
            return 99

    @property
    def rule_prefix(self) -> str:
        return str(self.meta.get("rule_prefix", ""))

    @property
    def companions(self) -> list[str]:
        value = self.meta.get("companions") or []
        return [str(item) for item in value] if isinstance(value, list) else []

    def as_dict(self, *, with_rules: bool = False) -> dict[str, t.Any]:
        payload = {
            "id": self.id,
            "title": self.title,
            "question": self.question,
            "version": self.meta.get("version"),
            "status": self.meta.get("status"),
            "rule_prefix": self.rule_prefix,
            "companions": self.companions,
            "path": self.path.name,
            "rule_count": len(self.rules),
        }
        if with_rules:
            payload["rules"] = [rule.as_dict() for rule in self.rules]
        return payload


def _extract_rules(document: frontmatter.Document, spec_id: str) -> tuple[Rule, ...]:
    """Find every rule, including the part written on continuation lines.

    A rule is usually two or three lines of wrapped text. Reading only the first
    line would truncate the requirement, so the parser keeps consuming indented
    continuation lines until the next bullet or a blank line.
    """
    lines = document.lines
    rules: list[Rule] = []
    for index, line in enumerate(lines):
        match = RULE_PATTERN.match(line)
        if not match:
            continue
        text = [match.group("text").strip()]
        for continuation in lines[index + 1 :]:
            if not continuation.strip() or RULE_PATTERN.match(continuation):
                break
            if not continuation.startswith((" ", "\t")):
                break
            text.append(continuation.strip())
        rules.append(
            Rule(
                id=match.group("id"),
                title=match.group("title").strip().rstrip("."),
                text=" ".join(part for part in text if part),
                spec=spec_id,
                line=document.line_number(index),
            )
        )
    return tuple(rules)


def load_spec(path: pathlib.Path) -> Spec:
    document = frontmatter.read(path)
    spec_id = str(document.meta.get("id") or path.stem)
    return Spec(
        id=spec_id,
        path=path,
        meta=document.meta,
        body=document.body,
        rules=_extract_rules(document, spec_id),
    )


def load_specs(spec_dir: pathlib.Path) -> list[Spec]:
    """Every standard in ``spec_dir``, in declared order."""
    if not spec_dir.is_dir():
        return []
    specs = [load_spec(path) for path in sorted(spec_dir.glob("*.md")) if path.name != "README.md"]
    return sorted(specs, key=lambda spec: (spec.order, spec.id))


def find_spec(spec_dir: pathlib.Path, name: str) -> Spec:
    """Look a standard up by id, filename, or title, case-insensitively."""
    wanted = name.strip().lower().removesuffix(".md")
    for spec in load_specs(spec_dir):
        if wanted in {spec.id.lower(), spec.path.stem.lower(), spec.title.lower()}:
            return spec
    known = ", ".join(spec.id for spec in load_specs(spec_dir)) or "none"
    raise NotFoundError(f"no standard named {name!r}", hint=f"known standards: {known}")


def all_rules(spec_dir: pathlib.Path) -> list[Rule]:
    return [rule for spec in load_specs(spec_dir) for rule in spec.rules]
