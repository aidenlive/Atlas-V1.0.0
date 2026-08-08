#!/usr/bin/env python3
"""Generate `docs/reference/cli.md` from the argument parser.

The parser is the reference. A flag cannot exist without being documented, and
the documentation cannot describe a flag the tool does not have.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from atlas.cli.app import render_reference  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> int:
    target = ROOT / "docs" / "reference" / "cli.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_reference(), encoding="utf-8")
    print(f"wrote {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
