"""Design tokens: loading, alias resolution, and CSS emission.

``assets/design/tokens.yaml`` is the source, not a copy. Every color, size,
and duration the generated site uses is emitted from it as a CSS custom
property, so re-theming is a token edit rather than a stylesheet hunt, and so
the site cannot quietly disagree with the design system it claims to follow.

Color is OKLCH throughout, per the organisation's color standard: perceptual
lightness means a ramp's steps are evenly spaced to the eye, and interpolation
between two tokens stays in gamut instead of detouring through grey.
"""

from __future__ import annotations

import pathlib
import re
import typing as t

import yaml

from ..errors import NotFoundError

__all__ = ["load", "resolve", "css_variables", "flatten"]

ALIAS = re.compile(r"\{([a-zA-Z]+)\.([a-zA-Z0-9-]+)\}")

#: Headline roles scale with the viewport; body and mono do not, because a
#: measure that holds at one width should hold at every width.
FLUID_CEILINGS = {"headline-display": 72, "headline-lg": 52, "headline-md": 36}


def load(path: pathlib.Path) -> dict[str, t.Any]:
    if not path.exists():
        raise NotFoundError(
            f"design tokens not found: {path}",
            hint="The site builder reads assets/design/tokens.yaml.",
        )
    parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        raise NotFoundError(f"{path}: tokens file must be a mapping")
    return parsed


def resolve(value: t.Any, tokens: dict[str, t.Any], depth: int = 0) -> t.Any:
    """Flatten ``{group.key}`` aliases, bounded against a cyclic reference."""
    if not isinstance(value, str) or depth > 6:
        return value

    def substitute(match: re.Match[str]) -> str:
        group, key = match.group(1), match.group(2)
        found = tokens.get(group, {})
        if isinstance(found, dict) and key in found:
            return str(found[key])
        return match.group(0)

    out = ALIAS.sub(substitute, value)
    return resolve(out, tokens, depth + 1) if out != value else out


def flatten(tokens: dict[str, t.Any], group: str) -> dict[str, str]:
    """A token group as resolved ``name -> value`` strings."""
    return {
        key: str(resolve(value, tokens))
        for key, value in (tokens.get(group) or {}).items()
        if isinstance(value, str)
    }


def _fluid(floor: str, ceiling: float) -> str:
    """Scale up from a stated floor, never below it.

    The floor is the size the role was designed at; a clamp whose lower bound
    is smaller than the design size means the type gets *worse* on the devices
    that need it most.
    """
    base = float(str(floor).rstrip("px"))
    return f"clamp({base}px, {base / 16:.4g}rem + {(ceiling - base) / 8.8:.4g}vw, {ceiling}px)"


def css_variables(tokens: dict[str, t.Any]) -> str:
    """Emit the token set as CSS custom properties for both themes.

    Three selectors, deliberately:

    * ``:root`` carries the light theme, so a stylesheet with no theme support
      still renders correctly;
    * ``@media (prefers-color-scheme: dark)`` honours the system setting for a
      reader who has never touched the site's own control;
    * ``[data-theme="dark"]`` / ``[data-theme="light"]`` let the explicit
      toggle override the system, in that order of specificity.
    """

    def emit(prefix: str, mapping: dict[str, t.Any], indent: str = "  ") -> str:
        return "\n".join(
            f"{indent}--{prefix}{key}: {resolve(value, tokens)};"
            for key, value in mapping.items()
            if isinstance(value, str)
        )

    typography: list[str] = []
    for role, spec in (tokens.get("typography") or {}).items():
        size = str(spec["fontSize"])
        if role in FLUID_CEILINGS:
            size = _fluid(size, FLUID_CEILINGS[role])
        typography += [
            f"  --font-{role}: {size};",
            f"  --lh-{role}: {spec['lineHeight']};",
            f"  --ls-{role}: {spec['letterSpacing']};",
            f"  --fw-{role}: {spec['fontWeight']};",
        ]

    structural = (
        [f"  --size-{k}: {v};" for k, v in (tokens.get("sizeClasses") or {}).items()]
        + [f"  --bp-{k}: {v};" for k, v in (tokens.get("breakpoints") or {}).items()]
        + [
            f"  --density: {(tokens.get('density') or {}).get('comfortable', 1)};",
            f"  --overscan: {(tokens.get('environment') or {}).get('overscan', 0)};",
        ]
    )

    light = "\n".join(
        part
        for part in (
            emit("", tokens.get("colors") or {}),
            emit("space-", tokens.get("spacing") or {}),
            emit("radius-", tokens.get("rounded") or {}),
            emit("elev-", tokens.get("elevation") or {}),
            emit("motion-", tokens.get("motion") or {}),
            "\n".join(typography),
            "\n".join(structural),
        )
        if part
    )

    dark_tokens = (tokens.get("themes") or {}).get("dark") or {}
    dark_colors = emit(
        "",
        {k: v for k, v in dark_tokens.items() if isinstance(v, str) and not k.startswith("elevation-")},
        indent="    ",
    )
    dark_elevation = "\n".join(
        f"    --elev-{k.removeprefix('elevation-')}: {v};"
        for k, v in dark_tokens.items()
        if isinstance(v, str) and k.startswith("elevation-")
    )
    dark_block = "\n".join(p for p in (dark_colors, dark_elevation) if p)

    # The same declarations are needed in two places; generating them once and
    # re-indenting keeps the two from diverging.
    dark_explicit = "\n".join("  " + line.strip() for line in dark_block.splitlines())
    light_explicit = "\n".join(
        "  " + line.strip()
        for line in "\n".join(
            p
            for p in (
                emit("", tokens.get("colors") or {}),
                emit("elev-", tokens.get("elevation") or {}),
            )
            if p
        ).splitlines()
    )

    return (
        "/* GENERATED from assets/design/tokens.yaml. Do not edit. */\n"
        f":root {{\n  color-scheme: light dark;\n{light}\n}}\n\n"
        f"@media (prefers-color-scheme: dark) {{\n  :root:not([data-theme]) {{\n{dark_block}\n  }}\n}}\n\n"
        f'[data-theme="dark"] {{\n  color-scheme: dark;\n{dark_explicit}\n}}\n\n'
        f'[data-theme="light"] {{\n  color-scheme: light;\n{light_explicit}\n}}\n'
    )
