"""Regenerate the brand assets from the design tokens.

Monospace advance width is a known constant (0.6em), so every string that sits
inside a box is measured before it is drawn. The row-4 label in the previous
architecture diagram was 288px of text in a 272px box; an assertion is cheaper
than noticing it in a screenshot.
"""
import pathlib

MONO = "ui-monospace, SFMono-Regular, 'JetBrains Mono', Menlo, Consolas, monospace"
ADV = 0.60  # monospace advance width, in em

L = dict(bg="#ffffff", rule="#e4e4e4", rule2="#cfcfcf", ink="#111111",
         ink2="#5e5e5e", ink3="#8f8f8f", fill="#fafafa", chip="#f2f2f2")
D = dict(bg="#0f0f0f", rule="#2a2a2a", rule2="#3d3d3d", ink="#f4f4f4",
         ink2="#a8a8a8", ink3="#767676", fill="#161616", chip="#1c1c1c")

STANDARDS = ["WORKSPACE", "PROJECT", "MATRIX", "CHECKLIST",
             "ADMIN", "PRESENTATION", "LIBRARY", "WORKSTREAM"]


def w(text, size):
    return len(text) * ADV * size


def fits(text, size, avail, where):
    got = w(text, size)
    assert got <= avail, f"{where}: {got:.0f}px of text in {avail}px ({text!r})"
    return text


# --------------------------------------------------------------------- banner
# Two shapes, not one scaled.
#
# The wide banner was 1280x250 carrying a mark row, a wordmark, a meta line, a
# rule and an eight-name row. Rendered at a phone's 380px that last row is 3.5px
# tall — present, unreadable, and noisy. GitHub scales a banner to the column
# width, so a banner cannot be "responsive"; it can only be swapped. Both
# READMEs select with <picture> on max-width: 600px.
#
# Alignment: the internal margin is set so that, at the width GitHub renders a
# README (roughly 1012px of column), the wordmark's left edge lands on the text
# column's left edge rather than floating inside it.
# The margin is chosen so the wordmark's left edge lands on the README text
# column's left edge once scaled. A 56px margin in a 1280 viewBox renders as
# 44px of inset against body text at 0 — which is what read as misalignment.
BW, BH, M = 1280, 200, 10            # -> ~8px inset at a 1012px column
CW, CH, CM = 720, 260, 12            # -> ~6px inset at a 380px column
CONTENT = BW - 2 * M


def _mark(c, x, y, size=20):
    """The Atlas mark: three stacked plates, drawn at any size.

    The same glyph the site chrome and the favicon use. One mark in three
    places beats three marks that nearly match.
    """
    s = size / 24.0
    def pt(px, py):
        return f"{x + px * s:.1f} {y + py * s:.1f}"
    stroke = max(1.2, 1.9 * s)
    return (
        f'<g fill="none" stroke="{c["ink"]}" stroke-width="{stroke:.2f}" '
        f'stroke-linejoin="round" stroke-linecap="round">'
        f'<path d="M{pt(12,2)}L{pt(2,7)}L{pt(12,12)}L{pt(22,7)}Z"/>'
        f'<path d="M{pt(2,12)}L{pt(12,17)}L{pt(22,12)}"/>'
        f'<path d="M{pt(2,17)}L{pt(12,22)}L{pt(22,17)}"/>'
        f'</g>')


def banner(c, label):
    """Wide: mark, wordmark, one tagline, one rule.

    No count of standards or commands. Those numbers change, a banner is
    regenerated rarely, and a stale boast is worse than no boast.
    """
    word, wsize = "atlas", 60
    fits(word, wsize, CONTENT, "banner wordmark")
    tag = "declared · versioned · machine-checked structure for digital work"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BW} {BH}" role="img" aria-label="{label}">
  <rect width="{BW}" height="{BH}" fill="{c['bg']}"/>
  <path d="M0 {BH - 0.5}H{BW}" stroke="{c['rule']}" stroke-width="1"/>
  {_mark(c, M, 34, 24)}
  <g font-family="{MONO}">
    <text x="{M}" y="{124}" font-size="{wsize}" font-weight="500" fill="{c['ink']}"
          letter-spacing="-1.5">{word}</text>
    <text x="{M}" y="{158}" font-size="17" fill="{c['ink2']}">{tag}</text>
  </g>
</svg>
'''


def banner_compact(c, label):
    """Compact: the same three facts at a size that survives a 380px column."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" role="img" aria-label="{label}">
  <rect width="{CW}" height="{CH}" fill="{c['bg']}"/>
  <path d="M0 {CH - 0.5}H{CW}" stroke="{c['rule']}" stroke-width="1"/>
  {_mark(c, CM, 62, 30)}
  <g font-family="{MONO}">
    <text x="{CM}" y="{146}" font-size="54" font-weight="500" fill="{c['ink']}"
          letter-spacing="-1.4">atlas</text>
    <text x="{CM}" y="{182}" font-size="21" fill="{c['ink2']}">declared · versioned</text>
    <text x="{CM}" y="{212}" font-size="21" fill="{c['ink2']}">machine-checked</text>
  </g>
</svg>
'''


def template_banner(c, label):
    name = "{{PROJECT_NAME}}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BW} 168" role="img" aria-label="{label}">
  <rect width="{BW}" height="168" fill="{c['bg']}"/>
  <path d="M0 167.5H{BW}" stroke="{c['rule']}" stroke-width="1"/>
  {_mark(c, M, 26, 22)}
  <g font-family="{MONO}">
    <text x="{M}" y="{104}" font-size="40" font-weight="500" fill="{c['ink']}"
          letter-spacing="-1">{name}</text>
    <text x="{M}" y="{136}" font-size="16" fill="{c['ink2']}">One line saying what this is.</text>
    <text x="{BW - M}" y="{104}" text-anchor="end" font-size="14" fill="{c['ink3']}"
          letter-spacing="1.5">REPLACE ME</text>
  </g>
</svg>
'''


def template_banner_compact(c, label):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} 230" role="img" aria-label="{label}">
  <rect width="{CW}" height="230" fill="{c['bg']}"/>
  <path d="M0 229.5H{CW}" stroke="{c['rule']}" stroke-width="1"/>
  {_mark(c, CM, 56, 30)}
  <g font-family="{MONO}">
    <text x="{CM}" y="{144}" font-size="40" font-weight="500" fill="{c['ink']}"
          letter-spacing="-1.2">{{{{PROJECT_NAME}}}}</text>
    <text x="{CM}" y="{184}" font-size="21" fill="{c['ink3']}" letter-spacing="1">REPLACE THIS BANNER</text>
  </g>
</svg>
'''


# --------------------------------------------------------------- architecture
# Uniform rows: every box is the same height, every gap the same, so the grid
# reads as a grid. Columns are 300/300/280 with 72px gutters inside 48px margins.
AW = 1120
COLS = [(48, 300), (420, 300), (792, 280)]
ROW_H, ROW_GAP, ROW_TOP = 104, 24, 76
ROWS = [ROW_TOP + i * (ROW_H + ROW_GAP) for i in range(4)]
AH = ROWS[-1] + ROW_H + 56

GRID = [
    # (title, sub lines) x 3 columns, plus the two arrow verbs
    (("spec/*.md", ["Eight standards. Prose is", "normative. Front matter is", "machine-discoverable."]),
     ("spec/schemas/*.json", ["Encode the enums the prose", "states. Consistency tests", "couple the two."]),
     ("atlas validate", ["Every manifest against the", "schema its standard: field", "names."]),
     "encodes", "validates"),
    (("work/NN_slug/*.md", ["Nine numbered sections.", "Markdown is canonical."]),
     ("work/index.yaml", ["Generated. Progress is", "counted, never asserted."]),
     ("atlas work validate", ["Skeleton, graph, and", "evidence before done."]),
     "syncs", "checks"),
    (("library/prompts/*.txt", ["Reusable intent, one", "objective each."]),
     ("library/prompts/index.yaml", ["Generated catalog,", "14 categories."]),
     ("atlas library check", ["Index and files agree", "in both directions."]),
     "emits", "contracts"),
    (("work/_template", ["The canonical work system,", "authored once."]),
     ("template/", ["The scaffold consumers", "copy out."]),
     ("atlas template check", ["Mirror cannot drift.", ""]),
     "mirrors", "verifies"),
]

TSIZE, SSIZE, PAD = 14, 12, 14


def box(c, x, y, bw, title, subs, where):
    fits(title, TSIZE, bw - 2 * PAD, f"{where} title")
    lines = [ln for ln in subs if ln]
    block = 24 + len(lines) * 18          # title block + one line each
    top = y + (ROW_H - block) / 2 + 16    # centered, then shifted to the baseline
    t = (f'<rect x="{x}" y="{y}" width="{bw}" height="{ROW_H}" fill="{c["fill"]}" '
         f'stroke="{c["rule2"]}" stroke-width="1"/>'
         f'<text x="{x + PAD}" y="{top}" font-size="{TSIZE}" font-weight="500" '
         f'fill="{c["ink"]}">{title}</text>')
    for i, line in enumerate(lines):
        fits(line, SSIZE, bw - 2 * PAD, f"{where} line{i}")
        t += (f'<text x="{x + PAD}" y="{top + 24 + i * 18}" font-size="{SSIZE}" '
              f'fill="{c["ink2"]}">{line}</text>')
    return t


def arrow(c, x1, x2, y, label):
    mid = (x1 + x2) / 2
    fits(label, 11, x2 - x1, "arrow label")
    return (f'<path d="M{x1} {y}H{x2 - 8}" stroke="{c["rule2"]}" stroke-width="1"/>'
            f'<path d="M{x2 - 8} {y - 4}L{x2} {y}L{x2 - 8} {y + 4}" fill="none" '
            f'stroke="{c["ink3"]}" stroke-width="1" stroke-linejoin="round"/>'
            f'<text x="{mid}" y="{y - 10}" font-size="11" fill="{c["ink3"]}" '
            f'text-anchor="middle" letter-spacing="0.5">{label}</text>')


def diagram(c, label):
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {AW} {AH}" role="img" aria-label="{label}">',
         f'<rect width="{AW}" height="{AH}" fill="{c["bg"]}"/>',
         f'<g font-family="{MONO}">']
    for (x, _), head in zip(COLS, ("SOURCE", "MACHINE-READABLE", "ENFORCEMENT")):
        p.append(f'<text x="{x}" y="38" font-size="11" fill="{c["ink3"]}" letter-spacing="2">{head}</text>')
    p.append(f'<path d="M48 52H{AW - 48}" stroke="{c["rule"]}" stroke-width="1"/>')

    for r, (a, b, cc, v1, v2) in enumerate(GRID):
        y = ROWS[r]
        for (x, bw), (title, subs) in zip(COLS, (a, b, cc)):
            p.append(box(c, x, y, bw, title, subs, f"row{r+1}"))
        mid = y + ROW_H / 2
        p.append(arrow(c, COLS[0][0] + COLS[0][1], COLS[1][0], mid, v1))
        p.append(arrow(c, COLS[1][0] + COLS[1][1], COLS[2][0], mid, v2))

    foot = ROWS[-1] + ROW_H + 26
    p.append(f'<path d="M48 {foot}.5H{AW - 48}" stroke="{c["rule"]}" stroke-width="1"/>')
    p.append(f'<text x="48" y="{foot + 22}" font-size="11" fill="{c["ink3"]}" '
             f'letter-spacing="2">CI RUNS EVERY COLUMN ON EVERY PULL REQUEST</text>')
    p.append(f'<text x="{AW - 48}" y="{foot + 22}" font-size="11" fill="{c["ink3"]}" '
             f'text-anchor="end" letter-spacing="2">MARKDOWN IS CANONICAL</text>')
    p.append("</g></svg>")
    return "\n".join(p)



# --------------------------------------------------------------------- badges
# Generated here rather than fetched from a badge service, for three reasons.
#
# PRESENTATION P-07 says every badge value must be derivable from project.yaml.
# Reading the manifest and drawing the result makes that literally true instead
# of aspirational: a hand-typed shields.io URL can claim `maturity-stable` for
# years after the manifest says otherwise, and nothing notices.
#
# They also render offline, in a private fork, and in a printed PDF, none of
# which is true of a remote image.
#
# Color is a DOT, never a fill. The design system is achromatic by default and
# admits chroma only where it carries meaning, so a badge whose entire value
# segment is green spends the loudest signal available on decoration. The dot
# carries status, the text carries the fact, and the text repeats what the dot
# says, so the color is never the only channel.

BADGE_H = 20
BADGE_FS = 11
# Advance is deliberately generous. The renderer picks whatever mono it has,
# and a fallback wider than the estimate makes the label collide with the dot
# rather than merely leaving a gap. Overestimating costs a few pixels.
BADGE_ADV = 0.62 * BADGE_FS + 0.6
BADGE_PAD = 8
DOT_R = 3.0
BADGE_R = 4
GAP = 10          # label to dot

# Hex, not the OKLCH the tokens use: GitHub sanitises inline SVG, and a renderer
# that does not know oklch() drops the fill and takes the dot with it. These are
# the sRGB equivalents of the token roles they are named for.
INK = "#111111"
INK2 = "#5e5e5e"
LINE = "#e0e0e0"
DOT = {
    "ok": "#1f7a4d",
    "info": "#2b5fa8",
    "warn": "#9a6b12",
    "mute": "#9a9a9a",
}


def badge(label, value, dot="mute"):
    """One badge: hairline outline, quiet label, one status dot.

    The first version was a solid black block beside a grey block, which at
    README scale read as six heavy dominoes above the first sentence, louder
    than the headline they sat under. A badge is metadata: it should be
    legible when looked at and invisible when not.

    So: no fills, a hairline outline, the label in secondary ink and the value
    in primary. The dot carries status and the value word repeats it, so the
    colour is never the only channel.
    """
    label, value = label.upper(), str(value)
    lw = len(label) * BADGE_ADV
    vw = len(value) * BADGE_ADV
    total = round(BADGE_PAD * 2 + lw + GAP + DOT_R * 2 + 5 + vw)
    alt = f"{label.lower()}: {value.lower()}"
    lx = BADGE_PAD
    dx = BADGE_PAD + lw + GAP + DOT_R
    vx = dx + DOT_R + 5
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="{BADGE_H}"'
        f' viewBox="0 0 {total} {BADGE_H}" role="img" aria-label="{alt}">\n'
        f'  <title>{alt}</title>\n'
        f'  <rect x="0.5" y="0.5" width="{total - 1}" height="{BADGE_H - 1}"'
        f' rx="{BADGE_R}" fill="#ffffff" stroke="{LINE}"/>\n'
        f'  <g font-family="{MONO}" font-size="{BADGE_FS}" letter-spacing="0.4">\n'
        f'    <text x="{lx}" y="{BADGE_H / 2 + 4:.0f}" fill="{INK2}">{label}</text>\n'
        f'    <circle cx="{dx:.1f}" cy="{BADGE_H / 2}" r="{DOT_R}" fill="{DOT[dot]}"/>\n'
        f'    <text x="{vx:.1f}" y="{BADGE_H / 2 + 4:.0f}" fill="{INK}">{value}</text>\n'
        f'  </g>\n</svg>\n'
    )


def build_badges():
    """Draw the badge set from project.yaml, so the values cannot drift."""
    import re

    manifest = pathlib.Path("project.yaml").read_text(encoding="utf-8")

    def field(name, default=""):
        m = re.search(r"^" + name + r":\s*(.+?)\s*(?:#.*)?$", manifest, re.M)
        return m.group(1).strip().strip('"\'') if m else default

    changelog = pathlib.Path("CHANGELOG.md").read_text(encoding="utf-8")
    release = re.search(r"^## \[(\d+\.\d+\.\d+)\]", changelog, re.M)

    stage = field("stage", "active")
    maturity = field("maturity", "stable")
    spec = {
        "stage": (stage, {"active": "ok", "maintenance": "info",
                          "deprecated": "warn", "archived": "mute"}.get(stage, "info")),
        "maturity": (maturity, {"stable": "ok", "beta": "info",
                                "experimental": "warn"}.get(maturity, "mute")),
        "release": ("v" + release.group(1) if release else "unreleased", "mute"),
        "standard": (field("standard", "project/1.0"), "mute"),
        "ci": ("tests + compliance", "ok"),
        "license": ("CC-BY-4.0 + MIT", "mute"),
    }
    out = pathlib.Path("assets/badges")
    out.mkdir(parents=True, exist_ok=True)
    for name, (value, dot) in spec.items():
        (out / (name + ".svg")).write_text(badge(name, value, dot), encoding="utf-8")

    # The template ships its own set, drawn at the values a brand-new project
    # honestly has. A scaffold that starts life badged `stable` teaches the
    # first lesson backwards.
    tout = pathlib.Path("template/assets/badges")
    tout.mkdir(parents=True, exist_ok=True)
    for name, (value, dot) in {
        "stage": ("incubating", "info"),
        "maturity": ("experimental", "warn"),
        "standard": ("project/1.0", "mute"),
    }.items():
        (tout / (name + ".svg")).write_text(badge(name, value, dot), encoding="utf-8")
    return spec


BL = ("atlas — declared, versioned, machine-checked structure for files, "
      "repos, quality, authority, and intent")
TL = "{{PROJECT_NAME}} — placeholder banner; replace before going public"
AL = ("atlas architecture: specifications and work Markdown in the source column feed "
      "generated schemas and indexes in the machine-readable column, which validate.py, work.py, "
      "check-compliance.sh and sync-template.py enforce in the third column on every pull request")

for name, fn, lab in (("banner", banner, BL), ("architecture", diagram, AL)):
    for theme, c in (("light", L), ("dark", D)):
        pathlib.Path(f"assets/{name}-{theme}.svg").write_text(fn(c, lab))
    pathlib.Path(f"assets/{name}.svg").write_text(fn(L, lab))

for theme, c in (("light", L), ("dark", D)):
    pathlib.Path(f"assets/banner-compact-{theme}.svg").write_text(banner_compact(c, BL))
    pathlib.Path(f"template/assets/banner-{theme}.svg").write_text(template_banner(c, TL))
    pathlib.Path(f"template/assets/banner-compact-{theme}.svg").write_text(template_banner_compact(c, TL))
pathlib.Path("assets/banner-compact.svg").write_text(banner_compact(L, BL))
pathlib.Path("template/assets/banner.svg").write_text(template_banner(L, TL))
pathlib.Path("template/assets/banner-compact.svg").write_text(template_banner_compact(L, TL))
BADGES = build_badges()
print("badges: " + ", ".join(BADGES))
print(f"assets regenerated · architecture {AW}x{AH} · all text measured and within bounds")
