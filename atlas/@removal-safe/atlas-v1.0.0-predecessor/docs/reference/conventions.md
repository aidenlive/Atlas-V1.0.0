# Conventions

Every naming and structure rule in one place. If you are about to name a file,
a branch, a rule, or a directory, the answer is here.

These are conventions for *this repository and anything scaffolded from it*.
The normative rules they implement live in [`spec/`](../../spec/); where the two
could disagree, the specification wins and this page is the bug.

---

## The one rule underneath the rest

**Every fact has exactly one home.** Everywhere else it appears, it is a link or
a generated copy, never a second typed copy.

This is the whole reason for the conventions below. A repository does not decay
because someone writes something wrong; it decays because someone writes
something *right* in a second place, and then the first place changes.

When you find the same fact in two files, you have three options, in order of
preference:

1. **Delete one** and link to the other.
2. **Generate one** from the other, and add a check that fails when they drift
   (`atlas template check` is the worked example).
3. **Keep both and test that they agree.** Only when a reader genuinely needs
   the fact in both places without a click.

"Remember to update both" is not on the list.

---

## Naming

| Thing | Form | Example |
|---|---|---|
| Repository | lowercase, hyphenated, noun-first | `atlas` |
| Archive repository | as above, prefixed `@` | `@removal-safe` |
| Directory | lowercase, hyphenated | `docs/reference/` |
| Markdown file | `kebab-case.md` | `work-management.md` |
| Python module | `snake_case.py` | `build_assets.py`, `src/atlas/site/builder.py` |
| Shell script | `kebab-case.sh` | `check-compliance.sh` |
| Manifest | `<name>.yaml` at its home, `<slug>.<kind>.yaml` in `examples/` | `acme.org.yaml` |
| Architecture decision record | `NNNN-short-title.md` | `0002-sanctioned-root-extensions.md` |
| Workstream directory | `NN_slug` | `01_harden-repository-baseline` |
| Prompt | `request-<verb>-<object>.txt` | `request-cut-release.txt` |
| Branch | `type/short-description` | `docs/clarify-waivers` |
| Tag | `vX.Y.Z` | `v0.0.1` |

Two apparent inconsistencies are deliberate:

- **Python uses `snake_case`, shell uses `kebab-case`.** A Python file must be
  importable (`tests/test_workstreams.py` imports `work.py`) and `import
  build-site` is a syntax error. Shell scripts are never imported, so they
  follow the repository's general kebab-case rule.
- **Workstreams use `NN_slug`, not `NN-slug`.** The underscore separates the
  address from the name, so the number is visibly not part of the slug. Sorting
  is by number, and numbers are never reused (W-I3).

### The `@` prefix

A leading `@` marks a repository that is **not a live project**: an archive, a
graveyard, a holding pen. It sorts to the top of a directory listing and it
cannot be confused with a real project name, because the project name pattern
(`^[a-z0-9]+(-[a-z0-9]+)*$`) forbids it.

`@removal-safe` carries `name: removal-safe` in its manifest. The sigil belongs
to the directory, not to the project.

### Slugs never contain version numbers

`01_harden-repository-baseline`, not `01_baseline-v0-0-1`. Versions move;
addresses must not. If a slug names a version, the record becomes wrong the day
the next version ships.

---

## Directory roles

Every directory means the same thing here and in every repository scaffolded
from `template/`. This is what makes the fleet navigable: you already know where
things are before you open a repository you have never seen.

| Path | Holds | Changes |
|---|---|---|
| `spec/` (or `src/`) | The product | Deliberately, with a version |
| `tests/` | A mirror of the product's topology | With the product |
| `docs/architecture/` | How it is built, and why | On structural change |
| `docs/decisions/` | ADRs — append-only | On decisions |
| `docs/guides/` | Task-oriented how-tos | On workflow change |
| `docs/reference/` | Look-it-up surface docs | With the surface |
| `examples/` | Runnable samples, verified in CI | With the surface |
| `scripts/` | Development and maintenance automation | Freely |
| `assets/` | Brand, diagrams, the design system | Rarely |
| `work/` | Initiatives: plan, tasks, evidence | Continuously |
| `template/` | The scaffold consumers copy | Via `atlas template sync` |
| `library/` | Shared assets: prompts, icons, typefaces, media | By pull request; prompts are generated |

| `.github/` | CI and forge settings as code | On policy change |

**The root is a closed set.** Adding an entry to the repository root requires an
ADR. `atlas check` fails on anything unsanctioned. This is not
tidiness: the root is the first thing every reader and every agent sees, and it
is the only part of a repository that cannot be reorganized without breaking
links.

Build output is not structure. `site/` is generated, gitignored, and skipped by
the closed-set check because git ignores it.

---

## Generated files

Some files in this repository are written by scripts. Editing them is always a
mistake: your change is correct until the next `sync`, and then it is gone.

| File | Generated by | Edit instead |
|---|---|---|
| `work/README.md` | `atlas work sync` | The workstream Markdown |
| `work/index.yaml` | `atlas work sync` | The workstream Markdown |
| `library/prompts/**` | `scripts/generate_prompts.py` | The generator |
| `library/prompts/index.yaml` | `scripts/generate_prompts.py` | The generator |
| `library/prompts/README.md` | `scripts/generate_prompts.py` | The generator |
| `template/atlas work` | `atlas template sync` | `atlas work` |
| `template/work/_template/**` | `atlas template sync` | `work/_template/` |
| `template/work/workstream.schema.json` | `atlas template sync` | `spec/schemas/workstream.schema.json` |
| `site/**` | `atlas site build` | The Markdown it renders |
| `assets/*.svg`, `template/assets/*.svg` | `scripts/build_assets.py` | The generator |
| `assets/design/tokens.yaml` | extracted from `assets/design/DESIGN.md` | The design system's front matter |

Every one of these is drift-checked in CI. If you edit a generated file, the
build goes red, which is the system working.

---

## Colour

The palette is achromatic by default. Chroma appears only where it **carries
meaning** (status, syntax, data series) and it is never the only channel
carrying it. Every status use pairs the hue with a glyph and a word, so the
meaning survives greyscale, colour-blindness, and a screen reader (WCAG 1.4.1).

| Use | Role | Second channel |
|---|---|---|
| Workstream and spec status | `success` `info` `warning` `error` | Glyph + the status word |
| Callouts | the four `*-surface` tones plus a neutral aside | Icon + title |
| Completed progress | `success` | The `n/m` count, and an `aria-label` |
| Syntax | the `code-*` roles | The code itself |
| Sidebar section accents | `series-1`–`series-4` | The group's name label |

Adding a colour that identifies nothing is the thing this table exists to
prevent. If a hue would be the only way to tell two things apart, it is the
wrong tool.

## Design

The site and the brand assets are built from **Neue 1.0**, carried in full at
[`assets/design/DESIGN.md`](../../assets/design/DESIGN.md). Its front matter is
extracted verbatim to `tokens.yaml`, which `atlas site build` compiles into
CSS custom properties. Editing `tokens.yaml` by hand forks the design system; a
test compares the two.

Two of its rules shape every layout decision here:

- **The two axes.** Structure: how many panes, where navigation lives, whether
  a region is docked or a drawer: resolves from the *container* it was given,
  using the `sizeClasses` thresholds and `@container`. Only page-level chrome —
  gutters, the shell cap: resolves from the *viewport* with `@media`. Using one
  for the other's job is the bug the two differently-named scales exist to make
  visible in review.
- **Horizontal scrolling is a component, not an accident.** There is no
  horizontal page scroll; every wide child owns a `.scroller` that takes
  `tabindex="0"` and an `aria-label`, and shows an edge affordance on whichever
  edge actually has content beyond it.

## Writing

- **Markdown is canonical.** Anything rendered (the site, a PDF, a wiki) is
  derived and may be stale.
- **One `h1` per document**, and it names the document, not the filename.
- **Specifications carry YAML front matter.** See
  [`rule-ids.md`](rule-ids.md) for the fields.
- **Do not put counts in prose** unless something checks them. "78 prompts" is
  fine because `tests/test_prompts.py` counts them. "61 tests" is not, because
  nothing did, and it was wrong.
- **Link, do not restate.** If you find yourself explaining something a
  specification already says, link to it and cite the rule id.
- Line length is not enforced; wrapping around 80 columns keeps diffs readable.

---

## Commits and changes

Commits follow [Conventional Commits](https://www.conventionalcommits.org):

```
feat | fix | docs | chore | spec | test | ci | refactor
```

`spec:` is local to this repository and marks a **normative** change: one that
alters what compliance means. Those travel as one change-set: the specification
prose, the matching JSON Schema, the version header in the front matter, and a
`CHANGELOG.md` entry. CI enforces the schema half.

Everything else is editorial and merges freely once CI is green.

See [`CONTRIBUTING.md`](../../CONTRIBUTING.md) for the full workflow, and
[`versioning.md`](versioning.md) for what bumps what.
