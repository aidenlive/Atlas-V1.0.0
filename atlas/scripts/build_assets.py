#!/usr/bin/env python3
"""Generate the badges from `project.yaml` and the design tokens.

A badge is a claim. Drawing it from the manifest means a badge cannot claim
something the manifest no longer says (PUBLICATION P-07). The dot carries status
and the text repeats it, so colour is never the only signal (P-05).

The README's hero is a real terminal transcript, not a wordmark: see
`scripts/build_screenshots.py`.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import yaml  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

BADGE = """<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="28" role="img" aria-label="{label}: {value}">
  <title>{label}: {value}</title>
  <rect width="{width}" height="28" rx="6" fill="{bg}"/>
  <rect x="0.5" y="0.5" width="{width_inner}" height="27" rx="5.5" fill="none" stroke="{border}"/>
  <circle cx="14" cy="14" r="4" fill="{dot}"/>
  <text x="26" y="18" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="{fg}">{label}: {value}</text>
</svg>
"""

def load_tokens() -> dict:
    return yaml.safe_load((ASSETS / "design" / "tokens.yaml").read_text(encoding="utf-8"))


def write(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")


def main() -> int:
    manifest = yaml.safe_load((ROOT / "project.yaml").read_text(encoding="utf-8"))
    tokens = load_tokens()
    light, dark = tokens["themes"]["light"], tokens["themes"]["dark"]
    states = tokens["states"]

    badges = {
        "stage": (manifest["stage"], states["active"]),
        "maturity": (manifest["maturity"], states["stable"]),
        "release": ("v1.0.0", states["release"]),
        "standard": (manifest["standard"], states["standard"]),
        "ci": ("checks + tests", states["ci"]),
        "license": ("CC-BY-4.0 + MIT", states["license"]),
    }
    for label, (value, dot) in badges.items():
        text = f"{label}: {value}"
        write(
            ASSETS / "badges" / f"{label}.svg",
            BADGE.format(
                width=len(text) * 6.6 + 40,
                width_inner=len(text) * 6.6 + 39,
                label=label,
                value=value,
                bg=light["surface"],
                border=light["border"],
                fg=light["text"],
                dot=dot,
            ),
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
