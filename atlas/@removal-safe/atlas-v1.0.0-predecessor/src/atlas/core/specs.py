"""Reading the specification suite.

Every ``spec/*.md`` carries YAML front matter: id, order, title, tagline,
question, version, status, rule prefixes, companions. That front matter exists
so the suite is machine-discoverable without parsing prose, and this module is
the only place that parses it. ``atlas spec``, the site builder, and the
metadata tests all read through here, so a change to the front-matter contract
has exactly one place to land.
"""

from __future__ import annotations

import dataclasses
import pathlib
import re
import typing as t

import yaml

from ..errors import NotFoundError

__all__ = ["Spec", "FRONT_MATTER", "front_matter", "strip_front_matter", "load_specs", "find_spec"]

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
RULE_RE = re.compile(r"^\s*[-*|]?\s*\*{0,2}(?P<id>[A-Z]{1,4}-[A-Z]?\d{1,3})\*{0,2}[\s.:|]", re.M)


@dataclasses.dataclass(frozen=True)
class Spec:
    """One specification: its front matter, its body, and its path."""

    path: pathlib.Path
    meta: dict[str, t.Any]
    body: str

    @property
    def id(self) -> str:
        return str(self.meta.get("id", self.path.stem))

    @property
    def title(self) -> str:
        return str(self.meta.get("title", self.path.stem.upper()))

    @property
    def tagline(self) -> str:
        return str(self.meta.get("tagline", ""))

    @property
    def question(self) -> str:
        return str(self.meta.get("question", ""))

    @property
    def version(self) -> str:
        return str(self.meta.get("version", ""))

    @property
    def status(self) -> str:
        return str(self.meta.get("status", "draft"))

    @property
    def order(self) -> int:
        return int(self.meta.get("order", 99))

    @property
    def companions(self) -> list[str]:
        return list(self.meta.get("companions") or [])

    @property
    def prefixes(self) -> list[str]:
        """Every rule-identifier prefix this specification may issue."""
        return list(self.meta.get("rule_prefixes") or []) + list(
            self.meta.get("checklist_prefixes") or []
        )

    def rule_ids(self) -> list[str]:
        """Rule identifiers appearing in the body, in order of first mention.

        Deliberately a scan and not a parse: rules are stated in tables, in
        bold, and in prose, and the identifier is the stable part. Used by
        ``atlas spec rules`` and by the site's rule anchors.
        """
        seen: dict[str, None] = {}
        for match in RULE_RE.finditer(self.body):
            seen.setdefault(match.group("id"), None)
        if not self.prefixes:
            return list(seen)
        return [r for r in seen if any(r.startswith(p) for p in self.prefixes)]

    def summary(self) -> dict[str, t.Any]:
        return {
            "id": self.id,
            "title": self.title,
            "question": self.question,
            "tagline": self.tagline,
            "version": self.version,
            "status": self.status,
            "order": self.order,
            "companions": self.companions,
            "rule_prefixes": self.prefixes,
            "path": self.path.name,
        }


def front_matter(text: str) -> dict[str, t.Any]:
    """Parse leading YAML front matter, or return an empty mapping."""
    match = FRONT_MATTER.match(text)
    if not match:
        return {}
    parsed = yaml.safe_load(match.group(1))
    return parsed if isinstance(parsed, dict) else {}


def strip_front_matter(text: str) -> str:
    """Remove front matter. It is metadata about the document, not content."""
    return FRONT_MATTER.sub("", text, count=1)


def load_specs(spec_dir: pathlib.Path) -> list[Spec]:
    """Every specification, in declared reading order rather than alphabetical.

    Reading order is a property of the suite: WORKSPACE before PROJECT before
    MATRIX, and sorting by filename silently reorders it whenever a spec is
    renamed. The ``order`` key makes the sequence explicit and diffable.
    """
    if not spec_dir.is_dir():
        return []
    specs: list[Spec] = []
    for path in sorted(spec_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        specs.append(Spec(path, front_matter(text), strip_front_matter(text)))
    return sorted(specs, key=lambda s: (s.order, s.path.stem))


def find_spec(spec_dir: pathlib.Path, name: str) -> Spec:
    """Resolve a specification by id, filename stem, or title, case-insensitively.

    People reach for ``atlas spec show workstream``, ``… WORKSTREAM``, and
    ``… workstream.md`` interchangeably. All three resolve; failing on the
    grounds that the user chose the wrong one of three equivalent names is
    pedantry the tool can absorb.
    """
    wanted = name.lower().removesuffix(".md")
    specs = load_specs(spec_dir)
    for spec in specs:
        if wanted in {spec.id.lower(), spec.path.stem.lower(), spec.title.lower()}:
            return spec
    known = ", ".join(s.id for s in specs) or "none found"
    raise NotFoundError(
        f"no specification named {name!r}",
        hint=f"Known specifications: {known}",
    )
