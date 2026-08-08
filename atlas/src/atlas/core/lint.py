"""The editorial linter: the standards, applied to one document at a time.

``atlas check`` asks whether the repository is in order. ``atlas lint`` asks
whether a *piece of writing* is. The rules here are the mechanical subset of the
standards — the ones a machine can judge without an opinion: a missing
declaration, a heading three levels deep, a sentence that has swallowed two
sentences, a term spelled a second way, a phrase we have already decided against.

What the linter deliberately does not do is score prose. Readability indices
measure syllables and pretend that is clarity. Every rule below points at
something a person can see and fix, and names the standard that asked for it.

Two severities, and the difference matters:

* **error** — a violation of a normative rule. It fails the run.
* **warn** — a judgement call worth a second look. It is reported and does not
  fail the run unless ``--strict`` is passed.
"""

from __future__ import annotations

import dataclasses
import pathlib
import re
import typing as t

from . import frontmatter
from .lexicon import Lexicon
from .manifest import Violation

__all__ = ["Finding", "LintResult", "RULES", "lint_document", "lint_path", "lint_paths", "Settings"]


@dataclasses.dataclass(frozen=True)
class Settings:
    """The few numbers the rules need, so house preferences are not hard-coded."""

    max_sentence_words: int = 34
    max_paragraph_sentences: int = 6
    max_heading_depth: int = 4
    required_fields: tuple[str, ...] = ("title", "kind", "owner", "status", "updated")

    @classmethod
    def from_manifest(cls, data: dict[str, t.Any] | None) -> Settings:
        section = (data or {}).get("lint") or {}
        if not isinstance(section, dict):
            return cls()
        required = section.get("required_fields")
        return cls(
            max_sentence_words=int(section.get("max_sentence_words", cls.max_sentence_words)),
            max_paragraph_sentences=int(
                section.get("max_paragraph_sentences", cls.max_paragraph_sentences)
            ),
            max_heading_depth=int(section.get("max_heading_depth", cls.max_heading_depth)),
            required_fields=tuple(required) if isinstance(required, list) else cls.required_fields,
        )


@dataclasses.dataclass(frozen=True)
class Finding:
    """One thing the linter noticed, at one place."""

    rule: str
    check: str
    message: str
    path: str
    line: int
    severity: str = "error"
    hint: str | None = None

    def as_dict(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)

    def as_violation(self) -> Violation:
        return Violation(
            rule=self.rule, message=self.message, path=self.path, line=self.line, hint=self.hint
        )

    def __str__(self) -> str:
        return f"{self.path}:{self.line} {self.severity}: {self.message} [{self.rule}]"


@dataclasses.dataclass
class LintResult:
    path: pathlib.Path
    findings: list[Finding]

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "warn"]

    @property
    def ok(self) -> bool:
        return not self.findings

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "path": str(self.path),
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "findings": [f.as_dict() for f in self.findings],
        }


# ---------------------------------------------------------------------------
# Text preparation
# ---------------------------------------------------------------------------

_FENCE = re.compile(r"^\s*(```|~~~)")
_INLINE_CODE = re.compile(r"`[^`]*`")
_LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
_HEADING = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<text>.*?)\s*#*\s*$")
_BOLD = re.compile(r"\*\*[^*]+\*\*")
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(\[])")
_ABBREVIATIONS = ("e.g.", "i.e.", "etc.", "vs.", "Dr.", "Mr.", "Ms.", "No.", "cf.")
_PROSE_SKIP = re.compile(r"^\s*(\||>|<|:?-{3,}\s*$)")
_URL = re.compile(r"<?https?://\S+|\]\([^)]*\)")


def _prose_lines(document: frontmatter.Document) -> list[tuple[int, str]]:
    """Body lines that are prose: no code blocks, no tables, no raw HTML.

    Returned as ``(editor_line_number, text)`` pairs so every finding can point
    at a line the writer can actually open.
    """
    out: list[tuple[int, str]] = []
    in_fence = False
    for index, raw in enumerate(document.lines):
        if _FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if _PROSE_SKIP.match(raw):
            continue
        out.append((document.line_number(index), raw))
    return out


def _strip_urls(text: str) -> str:
    """Remove link targets and bare URLs.

    A URL is not prose. Checking terminology inside one produces a violation for
    every `github.com` link, which teaches writers to switch the check off.
    """
    return _URL.sub(" ", text)


def _strip_markup(text: str) -> str:
    text = _INLINE_CODE.sub(" ", text)
    text = _LINK.sub(r"\1", text)
    return text.replace("**", "").replace("*", "").replace("_", "")


def _sentences(paragraph: str) -> list[str]:
    guarded = paragraph
    for abbreviation in _ABBREVIATIONS:
        guarded = guarded.replace(abbreviation, abbreviation.replace(".", "\u0000"))
    parts = [part.replace("\u0000", ".").strip() for part in _SENTENCE_END.split(guarded)]
    return [part for part in parts if part]


def _paragraphs(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Group prose lines into paragraphs, keeping the first line number."""
    paragraphs: list[tuple[int, str]] = []
    buffer: list[str] = []
    start = 0
    for number, text in lines:
        stripped = text.strip()
        if not stripped or _HEADING.match(text) or re.match(r"^\s*([-*+]|\d+\.)\s+", text):
            if buffer:
                paragraphs.append((start, " ".join(buffer)))
                buffer = []
            continue
        if not buffer:
            start = number
        buffer.append(stripped)
    if buffer:
        paragraphs.append((start, " ".join(buffer)))
    return paragraphs


def _word_boundary(needle: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![\w-]){re.escape(needle)}(?![\w-])", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------

RuleFn = t.Callable[[frontmatter.Document, Lexicon, Settings], list[Finding]]

RULES: dict[str, tuple[str, str, RuleFn]] = {}


def rule(check: str, summary: str, standard_rule: str) -> t.Callable[[RuleFn], RuleFn]:
    """Register one lint rule under a stable name.

    The name is what ``atlas lint --only`` takes, so it is part of the interface
    and does not change without a changelog entry.
    """

    def decorate(fn: RuleFn) -> RuleFn:
        RULES[check] = (summary, standard_rule, fn)
        return fn

    return decorate


@rule("declaration", "Every document declares its facts up front", "CONTENT C-01")
def _check_declaration(doc: frontmatter.Document, _lex: Lexicon, cfg: Settings) -> list[Finding]:
    if not doc.has_frontmatter:
        return [
            Finding(
                rule="CONTENT C-01",
                check="declaration",
                message="no front matter: the document declares nothing about itself",
                path=str(doc.path),
                line=1,
                hint="add a YAML block with " + ", ".join(cfg.required_fields),
            )
        ]
    missing = [field for field in cfg.required_fields if not doc.meta.get(field)]
    return [
        Finding(
            rule="CONTENT C-01",
            check="declaration",
            message=f"front matter is missing `{field}`",
            path=str(doc.path),
            line=1,
        )
        for field in missing
    ]


@rule("title", "One H1, and it matches the declared title", "STRUCTURE S-01")
def _check_title(doc: frontmatter.Document, _lex: Lexicon, _cfg: Settings) -> list[Finding]:
    # Fence-aware: `# comment` inside a shell block is a comment, not a title.
    headings: list[tuple[int, str]] = []
    in_fence = False
    for i, line in enumerate(doc.lines):
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence and line.startswith("# "):
            headings.append((doc.line_number(i), line[2:].strip()))
    if not headings:
        return [
            Finding(
                rule="STRUCTURE S-01",
                check="title",
                message="no H1: a reader cannot tell what this document is",
                path=str(doc.path),
                line=doc.body_offset,
            )
        ]
    findings = [
        Finding(
            rule="STRUCTURE S-01",
            check="title",
            message="second H1: a document has one title",
            path=str(doc.path),
            line=line,
        )
        for line, _ in headings[1:]
    ]
    declared = str(doc.meta.get("title", "")).strip()
    # A decision record numbers its H1 (`5. Archive the predecessor`) while its
    # declared title does not. That is the convention, not a mismatch.
    actual = re.sub(r"^\d+\.\s+", "", headings[0][1]).strip()
    if declared and declared.lower() != actual.lower():
        findings.append(
            Finding(
                rule="STRUCTURE S-01",
                check="title",
                message=f"H1 ({actual!r}) does not match the declared title ({declared!r})",
                path=str(doc.path),
                line=headings[0][0],
                severity="warn",
            )
        )
    return findings


@rule("headings", "Heading levels descend one at a time", "STRUCTURE S-02")
def _check_headings(doc: frontmatter.Document, _lex: Lexicon, cfg: Settings) -> list[Finding]:
    findings: list[Finding] = []
    previous = 0
    in_fence = False
    for index, raw in enumerate(doc.lines):
        if _FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = _HEADING.match(raw)
        if not match:
            continue
        level = len(match.group("hashes"))
        line = doc.line_number(index)
        if previous and level > previous + 1:
            findings.append(
                Finding(
                    rule="STRUCTURE S-02",
                    check="headings",
                    message=f"heading jumps from H{previous} to H{level}",
                    path=str(doc.path),
                    line=line,
                )
            )
        if level > cfg.max_heading_depth:
            findings.append(
                Finding(
                    rule="STRUCTURE S-02",
                    check="headings",
                    message=f"H{level} is deeper than the standard allows (H{cfg.max_heading_depth})",
                    path=str(doc.path),
                    line=line,
                    hint="deep nesting usually means the document should be split",
                )
            )
        previous = level
    return findings


@rule("heading-case", "Headings are sentence case", "LANGUAGE L-04")
def _check_heading_case(doc: frontmatter.Document, lex: Lexicon, _cfg: Settings) -> list[Finding]:
    canonical = {term.use.lower(): term.use for term in lex.terms}
    findings: list[Finding] = []
    in_fence = False
    for index, raw in enumerate(doc.lines):
        if _FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = _HEADING.match(raw)
        if not match:
            continue
        words = _strip_markup(match.group("text")).split()
        # A heading is Title Case when most of its non-leading words are
        # capitalised and are not names we have declared as capitalised.
        candidates = [w for w in words[1:] if w[:1].isalpha()]
        capitalised = [
            w
            for w in candidates
            if w[:1].isupper() and w.lower() not in canonical and not w.isupper()
        ]
        if len(candidates) >= 3 and len(capitalised) >= max(2, int(len(candidates) * 0.6)):
            findings.append(
                Finding(
                    rule="LANGUAGE L-04",
                    check="heading-case",
                    message="heading looks like Title Case; use sentence case",
                    path=str(doc.path),
                    line=doc.line_number(index),
                    severity="warn",
                )
            )
    return findings


@rule("sentence-length", "Sentences stay inside one breath", "VOICE V-04")
def _check_sentence_length(doc: frontmatter.Document, _lex: Lexicon, cfg: Settings) -> list[Finding]:
    findings: list[Finding] = []
    for line, paragraph in _paragraphs(_prose_lines(doc)):
        for sentence in _sentences(_strip_markup(paragraph)):
            count = len(sentence.split())
            if count > cfg.max_sentence_words:
                findings.append(
                    Finding(
                        rule="VOICE V-04",
                        check="sentence-length",
                        message=f"{count}-word sentence (limit {cfg.max_sentence_words})",
                        path=str(doc.path),
                        line=line,
                        severity="warn",
                        hint="usually two sentences wearing one coat",
                    )
                )
    return findings


@rule("paragraph-length", "Paragraphs stay scannable", "STRUCTURE S-03")
def _check_paragraph_length(doc: frontmatter.Document, _lex: Lexicon, cfg: Settings) -> list[Finding]:
    findings: list[Finding] = []
    for line, paragraph in _paragraphs(_prose_lines(doc)):
        count = len(_sentences(_strip_markup(paragraph)))
        if count > cfg.max_paragraph_sentences:
            findings.append(
                Finding(
                    rule="STRUCTURE S-03",
                    check="paragraph-length",
                    message=f"{count}-sentence paragraph (limit {cfg.max_paragraph_sentences})",
                    path=str(doc.path),
                    line=line,
                    severity="warn",
                    hint="split it, or turn the list hiding inside it into a list",
                )
            )
    return findings


@rule("terminology", "Our names have one spelling", "LANGUAGE L-01")
def _check_terminology(doc: frontmatter.Document, lex: Lexicon, _cfg: Settings) -> list[Finding]:
    findings: list[Finding] = []
    for line, raw in _prose_lines(doc):
        text = _strip_urls(_INLINE_CODE.sub(" ", raw))
        for term in lex.terms:
            for wrong in term.avoid:
                for match in _word_boundary(wrong).finditer(text):
                    if match.group(0) == term.use:
                        continue
                    findings.append(
                        Finding(
                            rule="LANGUAGE L-01",
                            check="terminology",
                            message=f"{match.group(0)!r} — the term is {term.use!r}",
                            path=str(doc.path),
                            line=line,
                            severity=term.severity,
                            hint=term.note or None,
                        )
                    )
    return findings


@rule("phrasing", "Say it the shorter way", "VOICE V-03")
def _check_phrasing(doc: frontmatter.Document, lex: Lexicon, _cfg: Settings) -> list[Finding]:
    findings: list[Finding] = []
    for line, raw in _prose_lines(doc):
        text = _strip_urls(_INLINE_CODE.sub(" ", raw))
        for phrase in lex.phrases:
            if _word_boundary(phrase.avoid).search(text):
                findings.append(
                    Finding(
                        rule="VOICE V-03",
                        check="phrasing",
                        message=f"{phrase.avoid!r} — write {phrase.use!r}",
                        path=str(doc.path),
                        line=line,
                        severity=phrase.severity,
                        hint=phrase.reason or None,
                    )
                )
    return findings


@rule("emphasis", "Bold is for the rare thing", "STRUCTURE S-06")
def _check_emphasis(doc: frontmatter.Document, _lex: Lexicon, _cfg: Settings) -> list[Finding]:
    findings: list[Finding] = []
    for line, paragraph in _paragraphs(_prose_lines(doc)):
        bolded = _BOLD.findall(paragraph)
        if len(bolded) > 3:
            findings.append(
                Finding(
                    rule="STRUCTURE S-06",
                    check="emphasis",
                    message=f"{len(bolded)} bold runs in one paragraph; emphasis stops meaning anything",
                    path=str(doc.path),
                    line=line,
                    severity="warn",
                )
            )
    return findings


@rule("links", "Link text says where it goes", "STRUCTURE S-07")
def _check_links(doc: frontmatter.Document, _lex: Lexicon, _cfg: Settings) -> list[Finding]:
    empty = {"here", "click here", "this", "this link", "read more", "more", "link"}
    findings: list[Finding] = []
    for line, raw in _prose_lines(doc):
        for match in _LINK.finditer(raw):
            text = match.group(1).strip().lower().rstrip(".")
            if text in empty:
                findings.append(
                    Finding(
                        rule="STRUCTURE S-07",
                        check="links",
                        message=f"link text {match.group(1)!r} describes nothing",
                        path=str(doc.path),
                        line=line,
                        hint="name the destination: the reader decides from the link text alone",
                    )
                )
    return findings


@rule("mechanics", "No stray characters", "LANGUAGE L-08")
def _check_mechanics(doc: frontmatter.Document, _lex: Lexicon, _cfg: Settings) -> list[Finding]:
    findings: list[Finding] = []
    for line, raw in _prose_lines(doc):
        if raw.rstrip() != raw and raw.strip():
            findings.append(
                Finding(
                    rule="LANGUAGE L-08",
                    check="mechanics",
                    message="trailing whitespace",
                    path=str(doc.path),
                    line=line,
                    severity="warn",
                )
            )
        if "\t" in raw:
            findings.append(
                Finding(
                    rule="LANGUAGE L-08",
                    check="mechanics",
                    message="hard tab: indent with spaces",
                    path=str(doc.path),
                    line=line,
                    severity="warn",
                )
            )
    return findings


# ---------------------------------------------------------------------------
# Running
# ---------------------------------------------------------------------------


def lint_document(
    document: frontmatter.Document,
    lexicon: Lexicon,
    settings: Settings | None = None,
    *,
    only: t.Sequence[str] | None = None,
    skip: t.Sequence[str] | None = None,
) -> LintResult:
    settings = settings or Settings()
    selected = list(only) if only else list(RULES)
    for name in selected:
        if name not in RULES:
            from ..errors import NotFoundError

            raise NotFoundError(
                f"no lint rule named {name!r}", hint=f"known rules: {', '.join(sorted(RULES))}"
            )
    findings: list[Finding] = []
    for name in selected:
        if skip and name in skip:
            continue
        _summary, _standard_rule, fn = RULES[name]
        findings.extend(fn(document, lexicon, settings))
    # Two spellings of the same name in one entry's `avoid` list would report
    # the same word twice. The writer has one thing to fix, so they see one
    # finding.
    seen: set[tuple[str, int, str]] = set()
    unique: list[Finding] = []
    for finding in findings:
        key = (finding.check, finding.line, finding.message)
        if key in seen:
            continue
        seen.add(key)
        unique.append(finding)
    unique.sort(key=lambda f: (f.line, f.check))
    return LintResult(path=document.path, findings=unique)


def lint_path(path: pathlib.Path, lexicon: Lexicon, settings: Settings | None = None, **kw) -> LintResult:
    return lint_document(frontmatter.read(path), lexicon, settings, **kw)


def lint_paths(
    paths: t.Iterable[pathlib.Path], lexicon: Lexicon, settings: Settings | None = None, **kw
) -> list[LintResult]:
    return [lint_path(path, lexicon, settings, **kw) for path in paths]
