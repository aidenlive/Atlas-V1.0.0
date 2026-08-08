"""Terminal output: color when it helps, plain text when it would not.

Three rules hold everywhere in the CLI.

* **Color is never the only signal.** Every styled state is also a word, so the
  output survives a pipe, a log file, and color blindness.
* **Color is off unless a person is watching.** Not a TTY, ``NO_COLOR`` set, or
  ``--no-color`` passed means plain text.
* **Machine output is separate.** ``--json`` prints data on stdout and nothing
  else, so ``atlas check --json | jq`` needs no filtering.
"""

from __future__ import annotations

import dataclasses
import json
import os
import sys
import typing as t

__all__ = ["Console", "Style"]


class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"


#: state -> (marker, color). The marker carries the meaning on its own.
_STATES: dict[str, tuple[str, str]] = {
    "ok": ("ok  ", Style.GREEN),
    "fail": ("FAIL", Style.RED),
    "warn": ("warn", Style.YELLOW),
    "skip": ("skip", Style.DIM),
    "info": ("··  ", Style.CYAN),
}


@dataclasses.dataclass
class Console:
    """Everything the CLI prints goes through one object."""

    color: bool = True
    json_mode: bool = False
    quiet: bool = False
    verbose: bool = False
    stream: t.TextIO = dataclasses.field(default_factory=lambda: sys.stdout)

    def __post_init__(self) -> None:
        if os.environ.get("NO_COLOR") is not None or not self.stream.isatty():
            self.color = False

    # -- primitives ------------------------------------------------------
    def paint(self, text: str, *codes: str) -> str:
        if not self.color or not codes:
            return text
        return f"{''.join(codes)}{text}{Style.RESET}"

    def out(self, text: str = "") -> None:
        if self.json_mode:
            return
        print(text, file=self.stream)

    def err(self, text: str) -> None:
        print(text, file=sys.stderr)

    # -- shapes ----------------------------------------------------------
    def title(self, text: str) -> None:
        self.out(self.paint(text, Style.BOLD))

    def rule(self, text: str = "") -> None:
        self.out(self.paint(text or "─" * 60, Style.DIM))

    def state(self, state: str, text: str, detail: str = "") -> None:
        marker, color = _STATES.get(state, _STATES["info"])
        line = f"{self.paint(marker, color)}  {text}"
        if detail:
            line += f"  {self.paint(detail, Style.DIM)}"
        self.out(line)

    def bullet(self, text: str, indent: int = 6) -> None:
        self.out(" " * indent + f"- {text}")

    def field(self, label: str, value: str, width: int = 14) -> None:
        self.out(f"{self.paint(label.ljust(width), Style.DIM)}{value}")

    def note(self, text: str) -> None:
        if not self.quiet:
            self.out(self.paint(text, Style.DIM))

    def step(self, text: str) -> None:
        if self.verbose and not self.quiet:
            self.out(self.paint(f"··  {text}", Style.CYAN))

    def json(self, payload: t.Any) -> None:
        print(json.dumps(payload, indent=2, sort_keys=False), file=self.stream)

    def failure(self, message: str, hint: str | None = None) -> None:
        self.err(self.paint(f"error: {message}", Style.RED))
        if hint:
            self.err(self.paint(f"hint:  {hint}", Style.DIM))
