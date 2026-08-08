"""Terminal rendering: color, symbols, tables, and the ``--json`` escape hatch.

Dependency-free by design. Atlas runs in CI containers, pre-commit hooks, and
agent sandboxes where installing a rendering library is friction and where the
output is as often piped as read. So:

* color is opt-out at three levels: ``--no-color``, ``NO_COLOR``, and "stdout
  is not a terminal", because a build log full of escape sequences is worse
  than no color at all;
* every glyph has an ASCII fallback, selected from the encoding the stream
  actually reports, so a Windows console or a ``LANG=C`` runner shows ``[x]``
  rather than a replacement character;
* status is never carried by color alone. Every state ships a glyph and a
  word, matching the same rule the design system applies to status pills. A
  color-blind reader and a monochrome log get identical information.
"""

from __future__ import annotations

import dataclasses
import json
import os
import shutil
import sys
import textwrap
import typing as t

__all__ = ["Console", "Style", "Status"]


class Style:
    """SGR sequences. Empty strings when color is disabled."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDER = "\033[4m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    GREY = "\033[90m"


@dataclasses.dataclass(frozen=True)
class Status:
    """A named outcome: glyph, ASCII fallback, color, and word."""

    key: str
    glyph: str
    ascii: str
    color: str

    @property
    def word(self) -> str:
        return self.key.upper()


STATUSES: dict[str, Status] = {
    "ok": Status("ok", "\u2713", "+", Style.GREEN),
    "fail": Status("fail", "\u2715", "x", Style.RED),
    "warn": Status("warn", "\u25b3", "!", Style.YELLOW),
    "info": Status("info", "\u2022", "-", Style.BLUE),
    "skip": Status("skip", "\u2014", "~", Style.GREY),
    "run": Status("run", "\u25b6", ">", Style.CYAN),
}


def _supports_color(stream: t.IO[str], explicit: bool | None) -> bool:
    if explicit is not None:
        return explicit
    if os.environ.get("NO_COLOR") is not None:
        return False
    if os.environ.get("FORCE_COLOR") not in (None, "", "0"):
        return True
    if os.environ.get("TERM") == "dumb":
        return False
    return bool(getattr(stream, "isatty", lambda: False)())


def _supports_unicode(stream: t.IO[str]) -> bool:
    encoding = (getattr(stream, "encoding", None) or "").lower()
    return "utf" in encoding


class Console:
    """Renders Atlas output to a stream.

    One instance is built per invocation and threaded through the commands, so
    that ``--quiet``, ``--json``, and color settings are decided once at the
    boundary instead of being re-derived by every command.
    """

    def __init__(
        self,
        stream: t.IO[str] | None = None,
        *,
        err: t.IO[str] | None = None,
        color: bool | None = None,
        quiet: bool = False,
        verbose: bool = False,
        json_mode: bool = False,
        width: int | None = None,
    ) -> None:
        self.stream = stream or sys.stdout
        self.err = err or sys.stderr
        self.color = _supports_color(self.stream, color)
        self.unicode = _supports_unicode(self.stream)
        self.quiet = quiet
        self.verbose = verbose
        self.json_mode = json_mode
        self._width = width

    # ------------------------------------------------------------- primitives
    @property
    def width(self) -> int:
        """Usable width, clamped so prose stays inside a readable measure."""
        if self._width:
            return self._width
        try:
            cols = shutil.get_terminal_size(fallback=(80, 24)).columns
        except OSError:  # pragma: no cover - exotic streams
            cols = 80
        return max(48, min(cols, 100))

    def paint(self, text: str, *styles: str) -> str:
        if not self.color or not styles:
            return text
        return "".join(styles) + text + Style.RESET

    def glyph(self, key: str) -> str:
        status = STATUSES[key]
        mark = status.glyph if self.unicode else status.ascii
        return self.paint(mark, status.color)

    # ----------------------------------------------------------------- output
    def write(self, text: str = "") -> None:
        """Write a line to stdout, unless suppressed by ``--quiet``/``--json``."""
        if self.quiet or self.json_mode:
            return
        print(text, file=self.stream)

    def detail(self, text: str) -> None:
        """Write only under ``--verbose``. Never load-bearing."""
        if self.verbose:
            self.write(self.paint(text, Style.GREY))

    def error(self, text: str) -> None:
        """Write to stderr. Survives ``--quiet``: silencing progress must not
        silence failures."""
        print(f"{self.glyph('fail')} {text}", file=self.err)

    def hint(self, text: str) -> None:
        if not self.quiet:
            print(self.paint(f"  hint: {text}", Style.GREY), file=self.err)

    # ------------------------------------------------------------ composition
    def title(self, text: str, subtitle: str = "") -> None:
        self.write()
        self.write(self.paint(text, Style.BOLD))
        if subtitle:
            self.write(self.paint(subtitle, Style.GREY))
        self.write()

    def status(self, key: str, message: str, detail: str = "") -> None:
        """One status line: glyph, message, optional dim trailing detail."""
        tail = f"  {self.paint(detail, Style.GREY)}" if detail else ""
        self.write(f"{self.glyph(key)} {message}{tail}")

    def bullet(self, text: str, indent: int = 2) -> None:
        pad = " " * indent
        wrapped = textwrap.fill(
            text,
            width=self.width,
            initial_indent=f"{pad}\u2022 " if self.unicode else f"{pad}- ",
            subsequent_indent=pad + "  ",
        )
        self.write(wrapped)

    def para(self, text: str, indent: int = 0) -> None:
        pad = " " * indent
        self.write(textwrap.fill(text, width=self.width,
                                 initial_indent=pad, subsequent_indent=pad))

    def rule(self, label: str = "") -> None:
        line = "\u2500" if self.unicode else "-"
        if label:
            head = f"{line * 2} {label} "
            self.write(self.paint(head + line * max(0, self.width - len(head)), Style.GREY))
        else:
            self.write(self.paint(line * self.width, Style.GREY))

    def table(
        self,
        headers: t.Sequence[str],
        rows: t.Sequence[t.Sequence[str]],
        *,
        align: t.Sequence[str] | None = None,
    ) -> None:
        """A plain column table.

        Column widths come from the content, then the widest *flexible* column
        is squeezed if the total exceeds the terminal: truncating the longest
        column beats wrapping every column, which destroys the alignment that
        made a table worth using.
        """
        if not rows:
            return
        cols = len(headers)
        align = list(align or ["l"] * cols)
        widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row[:cols]):
                widths[i] = max(widths[i], len(_plain(str(cell))))

        budget = self.width - (2 * (cols - 1))
        while sum(widths) > budget and max(widths) > 8:
            widths[widths.index(max(widths))] -= 1

        def fmt(cell: str, i: int) -> str:
            text = str(cell)
            visible = _plain(text)
            if len(visible) > widths[i]:
                text = visible[: max(1, widths[i] - 1)] + ("\u2026" if self.unicode else ".")
                visible = _plain(text)
            pad = " " * (widths[i] - len(visible))
            return pad + text if align[i] == "r" else text + pad

        self.write("  ".join(
            self.paint(fmt(h, i), Style.BOLD, Style.GREY) for i, h in enumerate(headers)))
        for row in rows:
            cells = list(row) + [""] * (cols - len(row))
            self.write("  ".join(fmt(c, i) for i, c in enumerate(cells[:cols])))

    def definitions(self, pairs: t.Sequence[tuple[str, str]], indent: int = 2) -> None:
        """Aligned ``key   value`` pairs: the shape of ``atlas status``."""
        if not pairs:
            return
        keyw = max(len(k) for k, _ in pairs)
        for key, value in pairs:
            self.write(f"{' ' * indent}{self.paint(key.ljust(keyw), Style.GREY)}  {value}")

    def progress(self, done: int, total: int, width: int = 16) -> str:
        """A text progress bar. Returned, not printed, so it can sit in a cell."""
        if not total:
            return self.paint("—" if self.unicode else "-", Style.GREY)
        filled = round(width * done / total)
        full, empty = ("\u2588", "\u00b7") if self.unicode else ("#", ".")
        bar = full * filled + empty * (width - filled)
        color = Style.GREEN if done >= total else Style.CYAN
        return f"{self.paint(bar, color)} {done}/{total}"

    # ------------------------------------------------------------------- json
    def emit(self, payload: t.Any) -> None:
        """Emit the machine-readable form. No-op unless ``--json`` is set.

        Commands call ``emit`` and the human renderers unconditionally; exactly
        one of them produces output. That keeps the two representations beside
        each other in the source, which is the only reliable way to stop the
        JSON drifting from what the terminal shows.
        """
        if self.json_mode:
            json.dump(payload, self.stream, indent=2, default=str, sort_keys=False)
            self.stream.write("\n")


def _plain(text: str) -> str:
    """Strip SGR sequences so widths are measured in visible characters."""
    out, i = [], 0
    while i < len(text):
        if text[i] == "\033":
            end = text.find("m", i)
            if end != -1:
                i = end + 1
                continue
        out.append(text[i])
        i += 1
    return "".join(out)
