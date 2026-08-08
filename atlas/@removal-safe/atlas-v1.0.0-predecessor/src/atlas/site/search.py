"""Search index construction.

A static site cannot query a server, so the index ships with it. The design
constraint is size. It is downloaded in full on first search, so every field is
one character long and the body text is truncated to the first stretch that
usefully distinguishes one page from another.

Field names: ``u`` url, ``t`` title, ``c`` crumb, ``h`` headings, ``b`` body —
are terse because they repeat once per page, and a two-character saving per
field across several hundred entries is the difference between an index that
feels instant and one that does not.
"""

from __future__ import annotations

import dataclasses
import json
import re
import typing as t

__all__ = ["Entry", "Index", "build"]

#: Body text kept per page. Enough for a meaningful snippet and for matching
#: terms that appear well into a document, without shipping the whole corpus.
BODY_LIMIT = 1400

WHITESPACE = re.compile(r"\s+")


@dataclasses.dataclass
class Entry:
    url: str
    title: str
    crumb: str
    headings: list[str] = dataclasses.field(default_factory=list)
    body: str = ""

    def as_dict(self) -> dict[str, str]:
        return {
            "u": self.url,
            "t": self.title,
            "c": self.crumb,
            "h": " ".join(self.headings),
            "b": self.body,
        }


class Index:
    """Accumulates entries during the build, then serializes once."""

    def __init__(self) -> None:
        self._entries: list[Entry] = []

    def add(
        self,
        url: str,
        title: str,
        *,
        crumb: str = "",
        headings: t.Sequence[str] = (),
        body: str = "",
    ) -> None:
        self._entries.append(
            Entry(
                url=url,
                title=title,
                crumb=crumb,
                headings=[h for h in headings if h],
                body=_clean(body),
            )
        )

    def __len__(self) -> int:
        return len(self._entries)

    @property
    def entries(self) -> list[Entry]:
        return list(self._entries)

    def to_json(self) -> str:
        """Serialise compactly. Whitespace in an index is bytes with no reader."""
        return json.dumps(
            [entry.as_dict() for entry in self._entries],
            separators=(",", ":"),
            ensure_ascii=False,
        )


def _clean(text: str) -> str:
    collapsed = WHITESPACE.sub(" ", text).strip()
    if len(collapsed) <= BODY_LIMIT:
        return collapsed
    # Cut on a word boundary; a snippet that begins mid-word looks like a bug.
    cut = collapsed[:BODY_LIMIT]
    space = cut.rfind(" ")
    return (cut[:space] if space > BODY_LIMIT * 0.8 else cut).rstrip() + "\u2026"


def build(entries: t.Iterable[Entry]) -> str:
    index = Index()
    index._entries = list(entries)  # noqa: SLF001 - same module
    return index.to_json()
