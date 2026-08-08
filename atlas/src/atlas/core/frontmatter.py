"""Front matter: the manifest a single document carries.

Every piece of published content declares its own facts — what it is, who owns
it, who reviewed it, when it was last checked — in a YAML block at the top of
the file. Keeping those facts in the document rather than in a tracking
spreadsheet is the whole bet: a fact stored beside the thing it describes gets
updated in the same edit.
"""

from __future__ import annotations

import dataclasses
import pathlib
import typing as t

import yaml

__all__ = ["Document", "parse", "read"]

_FENCE = "---"


@dataclasses.dataclass
class Document:
    """A Markdown file split into its declared facts and its prose."""

    path: pathlib.Path
    meta: dict[str, t.Any]
    body: str
    #: 1-based line number where the body starts, so lint messages point at the
    #: line a person sees in their editor rather than an offset into a slice.
    body_offset: int = 1
    has_frontmatter: bool = False

    @property
    def title(self) -> str:
        declared = self.meta.get("title")
        if isinstance(declared, str) and declared.strip():
            return declared.strip()
        for line in self.body.splitlines():
            if line.startswith("# "):
                return line[2:].strip()
        return self.path.stem

    @property
    def lines(self) -> list[str]:
        return self.body.splitlines()

    def line_number(self, index: int) -> int:
        """Editor line number for zero-based index ``index`` into the body."""
        return self.body_offset + index


def parse(text: str, path: pathlib.Path | None = None) -> Document:
    """Split ``text`` into front matter and body.

    A file without front matter is not an error here — it is a fact the caller
    may want to report, so it is recorded rather than raised.
    """
    path = path or pathlib.Path("<string>")
    lines = text.splitlines()
    if not lines or lines[0].strip() != _FENCE:
        return Document(path=path, meta={}, body=text, body_offset=1, has_frontmatter=False)

    for index in range(1, len(lines)):
        if lines[index].strip() == _FENCE:
            raw = "\n".join(lines[1:index])
            try:
                meta = yaml.safe_load(raw) or {}
            except yaml.YAMLError:
                meta = {}
            if not isinstance(meta, dict):
                meta = {}
            from .manifest import _normalise

            meta = _normalise(meta)
            body = "\n".join(lines[index + 1 :])
            return Document(
                path=path,
                meta=meta,
                body=body.lstrip("\n"),
                body_offset=index + 2 + (len(body) - len(body.lstrip("\n"))),
                has_frontmatter=True,
            )

    # An opening fence with no closing fence: treat the whole file as body and
    # let the caller report the missing block.
    return Document(path=path, meta={}, body=text, body_offset=1, has_frontmatter=False)


def read(path: pathlib.Path) -> Document:
    return parse(path.read_text(encoding="utf-8"), path)
