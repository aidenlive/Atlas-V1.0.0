"""A focused Markdown renderer.

Not a general implementation, and deliberately so: it renders the Markdown this
repository actually writes: headings, tables, lists, fenced code, callouts,
quotes, rules, and raw HTML blocks, and nothing else. That keeps the site
build dependency-free, which matters because the site is rebuilt in CI on every
push and a documentation pipeline that breaks on an upstream release is a
documentation pipeline that stops running.

Where it goes beyond the minimum, it is to serve reading:

* headings emit stable slugs and a hover anchor, so any paragraph is linkable;
* tables recognize status words and progress bars and render them as
  components, so a dashboard reads as a dashboard rather than as a grid of
  words;
* wide children (tables, code) each own a scroll container, so the page itself
  never scrolls sideways;
* raw HTML blocks pass through untouched, which is what removed the previous
  build's un-escaping hack.
"""

from __future__ import annotations

import dataclasses
import html
import re
import typing as t

from .highlight import highlight

__all__ = ["Document", "Heading", "render", "slugify", "status_pill", "inline"]

STATUS_WORDS = frozenset(
    {
        "done", "active", "blocked", "planned", "review", "cancelled",
        "todo", "dropped", "pass", "fail", "open", "resolved", "mitigated",
        "stable", "beta", "draft", "superseded", "deprecated", "experimental",
    }
)

#: Status never rides on color alone: every pill carries a glyph and its word,
#: so the state survives a monochrome print and a color-blind reader.
STATUS_GLYPH = {
    "done": "\u2713", "pass": "\u2713", "resolved": "\u2713", "stable": "\u2713",
    "active": "\u25b6", "open": "\u25b6",
    "blocked": "\u2715", "fail": "\u2715",
    "review": "\u25cc", "beta": "\u25d0", "mitigated": "\u25d0",
    "planned": "\u25cb", "todo": "\u25cb", "draft": "\u25cb", "experimental": "\u25cb",
    "cancelled": "\u2014", "dropped": "\u2014", "superseded": "\u2014", "deprecated": "\u2014",
}

CALLOUT_RE = re.compile(r"\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*", re.I)
CALLOUT_TONE = {
    "note": "info", "tip": "success", "important": "neutral",
    "warning": "warning", "caution": "error",
}
CALLOUT_GLYPH = {
    "note": "i", "tip": "\u2713", "important": "\u25c6", "warning": "!", "caution": "\u2715",
}

PROGRESS_RE = re.compile(r"^`[\u2588\u00b7]+`\s*(\d+)/(\d+)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
LIST_RE = re.compile(r"^(?P<indent>\s*)(?P<marker>[-*+]|\d+[.)])\s+(?P<text>.*)$")
TASK_RE = re.compile(r"^\[(?P<mark>[ xX])\]\s+(?P<text>.*)$")
TABLE_SEP_RE = re.compile(r"^\s*\|[-: |]+\|\s*$")
RULE_RE = re.compile(r"^\s*(?:---+|\*\*\*+|___+)\s*$")
#: Rule identifiers, so a specification's rules are individually linkable.
RULE_ID_RE = re.compile(r"\b([A-Z]{1,4}-[A-Z]?\d{1,3})\b")
RAW_BLOCK_RE = re.compile(r"^\s*<(?P<tag>div|figure|section|table|details|aside|p|svg)\b", re.I)


@dataclasses.dataclass(frozen=True)
class Heading:
    level: int
    slug: str
    text: str


@dataclasses.dataclass(frozen=True)
class Document:
    html: str
    headings: list[Heading]
    #: Plain text, for the search index.
    text: str


def slugify(text: str) -> str:
    """A stable, readable anchor. Same input, same slug, across builds."""
    cleaned = re.sub(r"`|\*\*|\*|\[|\]|\(.*?\)", "", text)
    slug = re.sub(r"[^a-z0-9]+", "-", cleaned.lower()).strip("-")
    return slug or "section"


def link_href(href: str) -> str:
    """Rewrite a repository-relative link to its built location."""
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return html.escape(href, quote=True)
    anchor = ""
    if "#" in href:
        href, _, anchor = href.partition("#")
        anchor = f"#{anchor}"
    if not href:
        return html.escape(anchor, quote=True)
    if href.endswith(".txt"):
        href = href[:-4] + ".html"
    elif href.endswith("README.md"):
        href = href[:-9] + "index.html"
    elif href.endswith(".md"):
        href = href[:-3] + ".html"
    elif href.endswith("/"):
        href += "index.html"
    return html.escape(href + anchor, quote=True)


INLINE_PATTERNS: list[tuple[re.Pattern[str], t.Callable[[re.Match[str]], str]]] = [
    (re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)"),
     lambda m: f'<img src="{link_href(m.group(2))}" alt="{html.escape(m.group(1), quote=True)}" loading="lazy">'),
    (re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)"),
     lambda m: f'<a href="{link_href(m.group(2))}">{m.group(1)}</a>'),
    (re.compile(r"\*\*\*([^*]+)\*\*\*"), lambda m: f"<strong><em>{m.group(1)}</em></strong>"),
    (re.compile(r"\*\*([^*]+)\*\*"), lambda m: f"<strong>{m.group(1)}</strong>"),
    (re.compile(r"(?<![*\w])\*([^*\n]+)\*(?!\*)"), lambda m: f"<em>{m.group(1)}</em>"),
    (re.compile(r"~~([^~]+)~~"), lambda m: f"<del>{m.group(1)}</del>"),
]


def inline(text: str) -> str:
    """Render inline markup.

    Code spans are extracted first and reinserted last, so that a backticked
    ``**literal**`` stays literal: the ordering bug that makes naive renderers
    bold half of a code sample.
    """
    spans: list[str] = []

    def stash(match: re.Match[str]) -> str:
        spans.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"\x00{len(spans) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text, quote=False)
    for pattern, replacement in INLINE_PATTERNS:
        text = pattern.sub(replacement, text)
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], text)


def status_pill(status: str) -> str:
    glyph = STATUS_GLYPH.get(status, "\u25cb")
    return (
        f'<span class="pill pill-{status}">'
        f'<span class="pill-glyph" aria-hidden="true">{glyph}</span>{status}</span>'
    )


def _cell(text: str) -> str:
    plain = text.strip().lower()
    if plain in STATUS_WORDS:
        return f"<td>{status_pill(plain)}</td>"
    match = PROGRESS_RE.match(text.strip())
    if match:
        done, total = int(match.group(1)), int(match.group(2))
        percent = 100 * done // max(1, total)
        state = "is-complete" if total and done >= total else "is-partial"
        return (
            '<td><div class="progress">'
            f'<div class="progress-track {state}" role="img" aria-label="{done} of {total} complete">'
            f'<span style="width:{percent}%"></span></div>'
            f'<span class="progress-count">{done}/{total}</span></div></td>'
        )
    return f"<td>{inline(text)}</td>"


class _Renderer:
    def __init__(self, source: str, *, link_rules: bool = False) -> None:
        self.lines = source.replace("\r\n", "\n").split("\n")
        self.i = 0
        self.out: list[str] = []
        self.headings: list[Heading] = []
        self.text: list[str] = []
        self.link_rules = link_rules
        self.seen_slugs: dict[str, int] = {}
        self.first_h1_consumed = False

    # -- helpers ----------------------------------------------------------
    @property
    def line(self) -> str:
        return self.lines[self.i]

    def done(self) -> bool:
        return self.i >= len(self.lines)

    def unique_slug(self, base: str) -> str:
        count = self.seen_slugs.get(base, 0)
        self.seen_slugs[base] = count + 1
        return base if count == 0 else f"{base}-{count}"

    def annotate_rules(self, rendered: str) -> str:
        """Wrap rule identifiers so each is individually linkable."""
        if not self.link_rules:
            return rendered
        return RULE_ID_RE.sub(
            lambda m: f'<a class="rule-ref" id="rule-{m.group(1)}" href="#rule-{m.group(1)}">{m.group(1)}</a>',
            rendered,
        )

    # -- block parsers ----------------------------------------------------
    def code_fence(self) -> bool:
        if not self.line.startswith("```"):
            return False
        info = self.line[3:].strip()
        lang = info.split()[0] if info else ""
        body: list[str] = []
        self.i += 1
        while not self.done() and not self.lines[self.i].startswith("```"):
            body.append(self.lines[self.i])
            self.i += 1
        self.i += 1
        raw = "\n".join(body)
        label = html.escape(lang, quote=True) if lang else ""
        attr = f' data-lang="{label}"' if label else ""
        header = (
            f'<figcaption class="code-lang">{label}</figcaption>' if label else ""
        )
        self.out.append(
            f'<figure class="codeblock"{attr}>{header}'
            f'<button class="code-copy" type="button" data-copy aria-label="Copy code">Copy</button>'
            f'<pre class="code scroller" tabindex="0" role="region" '
            f'aria-label="{label or "Code"} sample, scrollable">'
            f"<code>{highlight(raw, lang)}</code></pre>"
            f"</figure>"
        )
        self.text.append(raw)
        return True

    def heading(self) -> bool:
        match = HEADING_RE.match(self.line)
        if not match:
            return False
        level, text = len(match.group(1)), match.group(2).strip()
        slug = self.unique_slug(slugify(text))
        plain = re.sub(r"[`*\[\]]|\(.*?\)", "", text).strip()
        self.headings.append(Heading(level, slug, plain))
        self.text.append(plain)
        self.i += 1
        if level == 1 and not self.first_h1_consumed:
            # The page shell renders the document title; emitting it again here
            # showed every title twice at two different sizes. Keep the anchor.
            self.first_h1_consumed = True
            self.out.append(f'<span id="{slug}" class="anchor-only"></span>')
            return True
        anchor = (
            f'<a class="heading-anchor" href="#{slug}" aria-label="Link to this section">#</a>'
        )
        self.out.append(f'<h{level} id="{slug}">{inline(text)}{anchor}</h{level}>')
        return True

    def table(self) -> bool:
        if not self.line.strip().startswith("|"):
            return False
        if self.i + 1 >= len(self.lines) or not TABLE_SEP_RE.match(self.lines[self.i + 1]):
            return False
        header = [c.strip() for c in self.line.strip().strip("|").split("|")]
        self.i += 2
        rows: list[list[str]] = []
        while not self.done() and self.line.strip().startswith("|"):
            rows.append([c.strip() for c in self.line.strip().strip("|").split("|")])
            self.i += 1
        thead = "".join(f"<th scope=\"col\">{inline(c)}</th>" for c in header)
        tbody = "".join("<tr>" + "".join(_cell(c) for c in row) + "</tr>" for row in rows)
        self.text += header + [c for row in rows for c in row]
        self.out.append(
            '<div class="table-wrap">'
            '<div class="scroller" tabindex="0" role="region" aria-label="Table, scrollable">'
            f"<table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table>"
            "</div></div>"
        )
        return True

    def list_block(self) -> bool:
        match = LIST_RE.match(self.line)
        if not match:
            return False
        items = self._collect_list(len(match.group("indent")))
        self.out.append(self._render_list(items))
        return True

    def _collect_list(self, base_indent: int) -> list[dict[str, t.Any]]:
        items: list[dict[str, t.Any]] = []
        while not self.done():
            match = LIST_RE.match(self.line)
            if match and len(match.group("indent")) >= base_indent:
                indent = len(match.group("indent"))
                if indent > base_indent and items:
                    items[-1]["children"] = self._collect_list(indent)
                    continue
                ordered = bool(re.match(r"\d", match.group("marker")))
                items.append(
                    {"text": match.group("text"), "ordered": ordered, "children": []}
                )
                self.i += 1
                continue
            # A continuation line: indented, non-blank, not a new marker.
            if items and self.line.strip() and self.line.startswith(" " * (base_indent + 2)):
                items[-1]["text"] += " " + self.line.strip()
                self.i += 1
                continue
            break
        return items

    def _render_list(self, items: list[dict[str, t.Any]]) -> str:
        if not items:
            return ""
        ordered = items[0]["ordered"]
        tag = "ol" if ordered else "ul"
        parts: list[str] = []
        checklist = False
        for item in items:
            body = item["text"]
            task = TASK_RE.match(body)
            if task:
                checklist = True
                checked = task.group("mark").lower() == "x"
                mark = "\u2713" if checked else "\u00a0"
                state = "is-checked" if checked else "is-unchecked"
                rendered = (
                    f'<span class="task-box {state}" aria-hidden="true">{mark}</span>'
                    f'<span class="task-text">{inline(task.group("text"))}</span>'
                )
                self.text.append(task.group("text"))
            else:
                rendered = self.annotate_rules(inline(body))
                self.text.append(body)
            nested = self._render_list(item["children"]) if item["children"] else ""
            parts.append(f"<li>{rendered}{nested}</li>")
        css = ' class="checklist"' if checklist else ""
        return f"<{tag}{css}>" + "".join(parts) + f"</{tag}>"

    def quote(self) -> bool:
        if not self.line.startswith(">"):
            return False
        body: list[str] = []
        while not self.done() and self.line.startswith(">"):
            body.append(self.line.lstrip("> ").rstrip())
            self.i += 1
        joined = " ".join(part for part in body if part)
        self.text.append(joined)
        match = CALLOUT_RE.match(joined)
        if match:
            tone = match.group(1).lower()
            rest = joined[match.end():].strip()
            role = ' role="alert"' if tone == "caution" else ""
            self.out.append(
                f'<div class="callout callout-{CALLOUT_TONE[tone]}"{role}>'
                f'<span class="callout-icon" aria-hidden="true">{CALLOUT_GLYPH[tone]}</span>'
                f'<div class="callout-body"><p class="callout-title">{tone.capitalize()}</p>'
                f"<p>{inline(rest)}</p></div></div>"
            )
        else:
            self.out.append(f"<blockquote>{inline(joined)}</blockquote>")
        return True

    def raw_html(self) -> bool:
        """Pass an HTML block through untouched.

        The previous build escaped these and then un-escaped them again with a
        string replace on the finished page. Recognising the block here is both
        correct and considerably less alarming.
        """
        if not RAW_BLOCK_RE.match(self.line):
            return False
        block: list[str] = []
        while not self.done() and self.line.strip():
            block.append(self.line)
            self.i += 1
        self.out.append("\n".join(block))
        return True

    def horizontal_rule(self) -> bool:
        if not RULE_RE.match(self.line):
            return False
        self.out.append("<hr>")
        self.i += 1
        return True

    def paragraph(self) -> bool:
        if not self.line.strip():
            self.i += 1
            return True
        parts = [self.line.strip()]
        self.i += 1
        while (
            not self.done()
            and self.line.strip()
            and not re.match(r"^\s*(#|\||>|```|[-*+]\s|\d+[.)]\s|---+$|<)", self.line)
        ):
            parts.append(self.line.strip())
            self.i += 1
        joined = " ".join(parts)
        self.text.append(joined)
        self.out.append(f"<p>{self.annotate_rules(inline(joined))}</p>")
        return True

    def run(self) -> Document:
        parsers = (
            self.code_fence,
            self.heading,
            self.table,
            self.raw_html,
            self.list_block,
            self.quote,
            self.horizontal_rule,
            self.paragraph,
        )
        while not self.done():
            if re.match(r"^\s*<!--", self.line):
                while not self.done() and "-->" not in self.line:
                    self.i += 1
                self.i += 1
                continue
            for parser in parsers:
                if parser():
                    break
            else:  # pragma: no cover - paragraph() always consumes
                self.i += 1
        return Document(
            html="\n".join(part for part in self.out if part),
            headings=self.headings,
            text=" ".join(self.text),
        )


def render(source: str, *, link_rules: bool = False) -> Document:
    """Render Markdown to HTML, headings, and plain text."""
    return _Renderer(source, link_rules=link_rules).run()
