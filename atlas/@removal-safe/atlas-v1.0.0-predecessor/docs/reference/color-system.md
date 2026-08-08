# The color system

Atlas is achromatic by default. Neutrals carry structure, and hue appears only
where it carries information a reader would otherwise have to work out. That is
a constraint from the design system rather than a stylistic preference: in a
monochrome interface, a single colored element is unmissable, and an interface
that colors everything has spent that signal before the reader needs it.

There are three layers, and every colored pixel on any Atlas surface belongs to
exactly one of them.

## 1. Status

Something is healthy, needs attention, or has failed. Four roles, fixed by the
organization's color standard, identical in every product.

| Role | Ramp | Means |
|---|---|---|
| `success` | green 500 | Settled and verified |
| `info` | blue 500 | In motion, nothing wrong |
| `warning` | amber 500 | Needs a decision |
| `error` | red 500 | Failed or blocked |

Status color is never the only channel. A pill carries a glyph and the status
word; a badge carries a dot and the value; the CLI prints a glyph, a word, and
color only when the stream is a terminal. Remove the hue and every status is
still readable, which is what makes the system work in a build log, in
greyscale, and for a colorblind reader.

## 2. Content domains

The site has five kinds of content, and each gets one accent used identically
everywhere it appears.

| Domain | Accent | Appears on |
|---|---|---|
| Standards | indigo | Page eyebrow, card edge, tags |
| Work | blue | Page eyebrow, card edge, tags |
| Documentation | teal | Page eyebrow, tags |
| Library | amber | Page eyebrow, tags |
| CLI | violet | Page eyebrow, tags |

A page sets `data-domain` once on its shell; `--accent`, `--accent-soft`, and
`--accent-line` resolve from there, and every component below reads those three
rather than naming a hue. Adding a domain is two token lines and one selector.

The accent marks a 2px rule, a glyph, or text on a softly tinted chip. It never
fills a card, tints a surface, or colors a navigation rail. Eight standards
rendered as eight tinted cards read as eight warnings; the same eight with a
2px edge read as a set.

**Navigation is exempt.** An earlier sidebar gave each group a tinted rail and a
colored dot. With five groups on screen it read as a legend for a chart that was
not there, and the one blocked workstream was invisible among the healthy ones.
Navigation now uses weight and position, which is what it was using to
communicate all along, and a status mark appears only on exception.

## 3. Syntax

Code is the one place where many hues appear at once, because each one is
carrying a real distinction: comment, string, keyword, number, function,
attribute, tag. These live in the `code-*` tokens, are checked to at least
4.5:1 against the code surface in both themes, and are used nowhere else. A
keyword purple must not appear on a tag, or the reader learns that purple means
two things.

## Applying it

Components read semantic tokens and never a ramp. The ramps exist so the
semantic layer has a principled source and so re-theming is a ramp swap rather
than a hunt through a stylesheet.

```css
/* Yes */
color: var(--accent);
background: var(--accent-soft);

/* No: components never name a palette step */
color: var(--indigo-600);
```

Both themes declare the same token names and differ only in values, so a theme
switch changes no component. `tests/test_site.py` asserts that every domain has
a complete accent set in both themes, because a domain with `--accent` but no
`--accent-soft` renders saturated text on an untinted ground and looks like a
bug rather than a decision.

## Where the values live

[`assets/design/tokens.yaml`](../../assets/design/tokens.yaml) is the source.
Every color is OKLCH, so a ramp's steps are evenly spaced to the eye and
interpolation between two of them stays in gamut instead of detouring through
grey. The site stylesheet is generated from that file and contains no literal
colors, which a test enforces.

Badges are the one exception, and deliberately: they are drawn as standalone
SVGs in `assets/badges/` using sRGB hex, because GitHub sanitizes inline SVG and
a renderer that does not understand `oklch()` drops the fill and takes the
status dot with it.
