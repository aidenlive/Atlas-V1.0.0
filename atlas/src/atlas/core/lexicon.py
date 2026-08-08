"""The lexicon: one place that says how we spell and what we call things.

Two lists, doing two different jobs.

**Terms** are the words that name our things — products, roles, systems. Each
has one canonical form and a list of forms that are the same word spelled some
other way. Disagreement here is the cheapest kind of inconsistency to remove and
the most visible when it remains.

**Phrases** are habits of writing we have decided against, each paired with what
to write instead. A phrase entry without a replacement is a complaint; with one,
it is an edit.

The lexicon is data, not prose, because ``atlas lint`` reads it. Adding a term
to the house style is a one-line change to one file, and every check picks it up.
"""

from __future__ import annotations

import dataclasses
import pathlib
import typing as t

from .manifest import load_yaml

__all__ = ["Term", "Phrase", "Lexicon", "load_lexicon"]

SEVERITIES = ("error", "warn")


@dataclasses.dataclass(frozen=True)
class Term:
    """A name with one canonical spelling."""

    id: str
    use: str
    avoid: tuple[str, ...] = ()
    kind: str = "term"
    note: str = ""
    severity: str = "error"

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "id": self.id,
            "use": self.use,
            "avoid": list(self.avoid),
            "kind": self.kind,
            "note": self.note,
            "severity": self.severity,
        }


@dataclasses.dataclass(frozen=True)
class Phrase:
    """A habit of writing, and what to write instead."""

    avoid: str
    use: str
    reason: str = ""
    severity: str = "warn"

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "avoid": self.avoid,
            "use": self.use,
            "reason": self.reason,
            "severity": self.severity,
        }


@dataclasses.dataclass(frozen=True)
class Lexicon:
    path: pathlib.Path
    version: str
    terms: tuple[Term, ...]
    phrases: tuple[Phrase, ...]

    def find(self, needle: str) -> list[Term]:
        wanted = needle.strip().lower()
        return [
            term
            for term in self.terms
            if wanted in term.id.lower()
            or wanted in term.use.lower()
            or any(wanted in alt.lower() for alt in term.avoid)
        ]

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "version": self.version,
            "terms": [term.as_dict() for term in self.terms],
            "phrases": [phrase.as_dict() for phrase in self.phrases],
        }


def _as_tuple(value: t.Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, list):
        return tuple(str(item) for item in value)
    return ()


def load_lexicon(path: pathlib.Path) -> Lexicon:
    """Load the lexicon, or return an empty one if the repository has none.

    An empty lexicon is a legitimate state: a repository that has not yet
    written its house terms should still be able to run every other check.
    """
    if not path.is_file():
        return Lexicon(path=path, version="0", terms=(), phrases=())

    data = load_yaml(path)
    terms = tuple(
        Term(
            id=str(entry.get("id") or entry.get("use", "")).strip(),
            use=str(entry.get("use", "")).strip(),
            avoid=_as_tuple(entry.get("avoid")),
            kind=str(entry.get("kind", "term")),
            note=str(entry.get("note", "")),
            severity=str(entry.get("severity", "error")),
        )
        for entry in data.get("terms", []) or []
        if isinstance(entry, dict) and entry.get("use")
    )
    phrases = tuple(
        Phrase(
            avoid=str(entry.get("avoid", "")).strip(),
            use=str(entry.get("use", "")).strip(),
            reason=str(entry.get("reason", "")),
            severity=str(entry.get("severity", "warn")),
        )
        for entry in data.get("phrases", []) or []
        if isinstance(entry, dict) and entry.get("avoid")
    )
    return Lexicon(
        path=path,
        version=str(data.get("version", "0")),
        terms=terms,
        phrases=phrases,
    )
