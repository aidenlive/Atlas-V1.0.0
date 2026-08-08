"""A small, dependency-free syntax highlighter.

Deliberately a tokenizer and not a parser. The goal is that a reader can tell a
comment from a string from a flag at a glance, not that every language edge
case resolves correctly. Getting the common 95% right in 200 lines is a better
trade for a documentation site than a parser dependency and a build that breaks
when it releases.

Tokens become spans carrying semantic classes, colored from the syntax roles
the design tokens reserve. Every color is checked against the code surface in
both themes; nothing here invents a hue.

Ordering within a language matters: the first alternative to match at a
position wins, so comments and strings are always declared before the patterns
that would otherwise chew into them.
"""

from __future__ import annotations

import html
import re

__all__ = ["highlight", "LANGUAGES", "language_label"]

Rules = list[tuple[str, str]]

_BASE: dict[str, Rules] = {
    "bash": [
        ("c", r"#[^\n]*"),
        ("s", r"\"(?:\\.|[^\"\\])*\"|'[^']*'"),
        ("v", r"\$\{[^}]*\}|\$[A-Za-z_]\w*"),
        ("f", r"(?<=\s)--?[A-Za-z][\w-]*"),
        ("k", r"\b(?:if|then|else|elif|fi|for|in|do|done|while|case|esac|function|return|export|local|set|source|cd|exit)\b"),
        ("b", r"\b(?:atlas|python3?|pip3?|pytest|git|npm|npx|make|bash|sh|echo|less|cat|cp|mv|rm|mkdir|find|grep|curl|jq|sed|awk|open)\b"),
        ("n", r"\b\d+\b"),
    ],
    "yaml": [
        ("c", r"#[^\n]*"),
        ("s", r"\"(?:\\.|[^\"\\])*\"|'[^']*'"),
        ("a", r"^[ \t]*-?[ \t]*[A-Za-z_][\w.-]*(?=[ \t]*:)"),
        ("v", r"\{\{[^}]*\}\}"),
        ("n", r"(?<![\w.-])\d[\d._-]*(?![\w-])"),
        ("k", r"\b(?:true|false|null|yes|no|on|off)\b"),
    ],
    "json": [
        ("a", r"\"(?:\\.|[^\"\\])*\"(?=[ \t]*:)"),
        ("s", r"\"(?:\\.|[^\"\\])*\""),
        ("n", r"-?\b\d[\d.eE+-]*\b"),
        ("k", r"\b(?:true|false|null)\b"),
        ("p", r"[{}\[\],:]"),
    ],
    "python": [
        ("c", r"#[^\n]*"),
        ("s", r"(?:[rbf]{0,2})(?:\"\"\"(?:.|\n)*?\"\"\"|'''(?:.|\n)*?'''|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')"),
        ("d", r"@[\w.]+"),
        ("k", r"\b(?:def|class|return|import|from|as|if|elif|else|for|while|in|not|and|or|is|None|True|False|try|except|finally|raise|with|assert|yield|lambda|pass|continue|break|global|nonlocal|async|await|match|case)\b"),
        ("b", r"(?<=def )\w+|(?<=class )\w+"),
        ("n", r"\b\d[\d._]*\b"),
    ],
    "toml": [
        ("c", r"#[^\n]*"),
        ("t", r"^\s*\[{1,2}[^\]]+\]{1,2}"),
        ("s", r"\"(?:\\.|[^\"\\])*\"|'[^']*'"),
        ("a", r"^[ \t]*[A-Za-z_][\w.-]*(?=[ \t]*=)"),
        ("n", r"\b\d[\d._-]*\b"),
        ("k", r"\b(?:true|false)\b"),
    ],
    "javascript": [
        ("c", r"//[^\n]*|/\*(?:.|\n)*?\*/"),
        ("s", r"`(?:\\.|[^`\\])*`|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'"),
        ("k", r"\b(?:const|let|var|function|return|if|else|for|while|of|in|new|class|extends|import|export|from|default|async|await|try|catch|finally|throw|typeof|instanceof|null|undefined|true|false|this)\b"),
        ("b", r"(?<=function )\w+|(?<=class )\w+"),
        ("n", r"\b\d[\d._]*\b"),
    ],
    "html": [
        ("c", r"<!--(?:.|\n)*?-->"),
        ("t", r"</?[A-Za-z][\w-]*"),
        ("a", r"\b[A-Za-z-]+(?==)"),
        ("s", r"\"(?:\\.|[^\"\\])*\"|'[^']*'"),
        ("p", r"/?>"),
    ],
    "css": [
        ("c", r"/\*(?:.|\n)*?\*/"),
        ("v", r"--[\w-]+"),
        ("a", r"\b[a-z-]+(?=\s*:)"),
        ("s", r"\"(?:\\.|[^\"\\])*\"|'[^']*'"),
        ("n", r"\b\d[\d.]*(?:px|rem|em|%|vw|vh|ms|s|ch|dvh)?\b"),
        ("t", r"@[a-z-]+"),
    ],
    "markdown": [
        ("t", r"^#{1,6} [^\n]*"),
        ("s", r"`[^`\n]+`"),
        ("f", r"\[[^\]]*\]\([^)]*\)"),
        ("c", r"^>[^\n]*"),
        ("k", r"\*\*[^*\n]+\*\*"),
    ],
    "diff": [
        ("added", r"^\+[^\n]*"),
        ("removed", r"^-[^\n]*"),
        ("c", r"^@@[^\n]*"),
    ],
    "text": [],
}

#: Aliases. A fence tagged `sh`, `shell`, or `console` means the same thing to
#: a reader, and refusing to highlight one of them is a papercut with no upside.
ALIASES = {
    "sh": "bash", "shell": "bash", "console": "bash", "zsh": "bash", "shell-session": "bash",
    "yml": "yaml",
    "py": "python", "python3": "python",
    "js": "javascript", "mjs": "javascript", "jsx": "javascript",
    "ts": "javascript", "tsx": "javascript",
    "md": "markdown",
    "htm": "html", "xml": "html", "svg": "html",
    "jsonc": "json",
    "txt": "text", "plain": "text", "": "text",
}

LABELS = {
    "bash": "shell", "yaml": "YAML", "json": "JSON", "python": "Python",
    "toml": "TOML", "javascript": "JavaScript", "html": "HTML", "css": "CSS",
    "markdown": "Markdown", "diff": "diff", "text": "text",
}

LANGUAGES = tuple(sorted(_BASE))

_COMPILED = {
    name: re.compile("|".join(f"(?P<{cls}>{pat})" for cls, pat in rules), re.M)
    for name, rules in _BASE.items()
    if rules
}


def _canonical(lang: str) -> str:
    key = (lang or "").strip().lower()
    return ALIASES.get(key, key)


def language_label(lang: str) -> str:
    """A human label for a fence tag, for the code block's caption."""
    return LABELS.get(_canonical(lang), lang)


def highlight(code: str, lang: str) -> str:
    """Escape ``code``, wrapping recognized tokens in semantic spans.

    Unknown languages return escaped text rather than a guess. A wrong
    highlight is worse than none: it asserts structure that is not there.
    """
    pattern = _COMPILED.get(_canonical(lang))
    if not pattern:
        return html.escape(code)
    out: list[str] = []
    last = 0
    for match in pattern.finditer(code):
        out.append(html.escape(code[last:match.start()]))
        out.append(f'<span class="t-{match.lastgroup}">{html.escape(match.group())}</span>')
        last = match.end()
    out.append(html.escape(code[last:]))
    return "".join(out)
