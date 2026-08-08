# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) · Versioning: [SemVer](https://semver.org).

This is the **suite release version**. The manifest contract version
(`project/1.0` and friends) is a separate number that moves independently. See
[`docs/reference/versioning.md`](docs/reference/versioning.md).

## [Unreleased]

### Added

- **A three-layer color system**, documented in
  [`docs/reference/color-system.md`](docs/reference/color-system.md): status,
  content domain, and syntax. Every colored pixel on any surface belongs to
  exactly one layer. Six ramps were added (indigo, violet, teal, cyan, orange,
  pink) and a semantic accent layer maps one hue to each content domain, so a
  standard is marked the same way in the sidebar, on its page eyebrow, on its
  card, and on its tags.
- Page eyebrows and tag chips, both accent-driven.
- Tests asserting every domain has a complete accent set in both themes, and
  that navigation carries no decorative hue.

### Changed

- **Navigation is achromatic again.** Each sidebar group had a tinted rail and
  a colored dot on its label; with five groups on screen it read as a legend
  for a chart that was not there, and the one blocked workstream was invisible
  among the healthy ones. Status marks now appear on exception only.
- **Badges redesigned.** The first version was a solid black block beside a
  grey block, which at README scale read as six heavy dominoes louder than the
  headline above them. They are now hairline-outlined, 20px, with a quiet label
  and one status dot.
- **Workstream section pages say what the section is for.** Twelve generated
  pages were a heading and a file list, and a section README was titled
  "Readme". Each of the nine sections now carries a stated purpose, a dek, an
  eyebrow, and a document table.

### Fixed

- **Unquoted token aliases were silently dropped.** `{colors.primary}` without
  quotes is YAML flow-mapping syntax, so the value parsed as a dict, failed the
  emitter's string check, and the custom property was never written. Nothing
  errored; the token simply did not exist. A test now fails on any unquoted
  alias.

- **Badges are drawn locally from `project.yaml`** instead of fetched from
  shields.io. PRESENTATION P-07 requires every badge value to be derivable from
  the manifest; generating them makes that true rather than aspirational, since
  a hand-typed badge URL can claim `maturity-stable` for years after the
  manifest says otherwise. They also render offline and in a private fork.
  Status is a small colored dot beside text that repeats it, so the color is
  never the only signal, and the value segment stays achromatic as the design
  system requires.
- **`EIGHT STANDARDS · ONE CLI` removed from the banners.** A banner is
  regenerated rarely, so a number baked into artwork goes stale silently: add a
  ninth standard and every README embedding it is quietly wrong. A test now
  fails if a countable boast reappears.
- Code samples in the README and guides are split one idea per block, with the
  explanation in prose above, rather than run together with trailing comments
  aligned to different columns.

- **Copy pass across every reader-facing surface.** The README now opens on the
  problem the standard solves rather than on a definition of itself; CLI help
  says "find out why something is not working" where it used to say "diagnose
  the environment"; and the site, the guides, and the command descriptions were
  rewritten for a reader who does not write code. Spelling is now American
  throughout, which it had not been: the specifications used `organization`
  while the tooling used `colour` and `centre`, next to an American `--no-color`
  flag. The `Console(colour=...)` parameter is now `color`, so the flag and the
  API agree.
- Em dashes used for emphasis are gone (1,043 down to 137, all of which are
  empty table cells or code). Conjunctions took commas, appositives took colons,
  asides took parentheses, and instructions became their own sentences.

### Fixed

- **`.gitignore` excluded the site generator package from version control.**
  The pattern `site/`, written to ignore the generated documentation site,
  matches a directory of that name at *any* depth, so it also matched
  `src/atlas/site/`. The working tree was complete and every local check passed;
  CI checked out a repository with no `atlas.site` module and the installed
  entry point died with `ModuleNotFoundError` before it could run. Build-output
  patterns are now anchored (`/site/`, `/dist/`, `/build/`).
- **Nothing verified that a built artifact actually worked.** Every check ran
  against the source tree, where an editable install imports `src/atlas/` off
  the filesystem regardless of what was committed or packaged. CI now builds a
  wheel, installs it into a clean virtual environment, and runs the CLI from
  outside the source tree: the only arrangement that can catch a subpackage
  that never shipped. Closes I-01.

### Added

- `tests/test_packaging.py`: asserts no file under `src/` or `tests/` is
  git-ignored, that build-output patterns stay anchored, that every subpackage
  imports, and that the declared console script resolves.

## [1.0.0] - 2026-08-07

**Renamed to Atlas**, and the tooling became a product rather than a drawer of
scripts. The eight specifications are unchanged and remain at contract version
`1.0`. Nothing in `spec/` moved, so no repository already declaring
`standard: project/1.0` needs to change anything.

The version jump from `0.0.1` to `1.0.0` is about the tooling, not the specs.
`0.0.1` shipped a suite that was correct but only operable by someone who had
read the `scripts/` directory. `1.0.0` ships a CLI, an installable package, and
a documented public API, which is the bar the CHECKLIST Production profile
actually asks for.

### Added

- **`atlas`, a first-class CLI.** Twelve commands: `init`, `status`, `doctor`,
  `check`, `validate`, `work`, `spec`, `prompt`, `library`, `site`, `template`,
  `completion`: with grouped, exampled help, stable exit codes, and `--json` on
  every read command. `-C <dir>` operates on another repository;
  `ATLAS_REPOSITORY` covers the cases where the working directory is not yours
  to choose.
- **`src/atlas/`, an installable package** (`pip install atlas-standard`).
  `atlas.core` holds the domain logic and knows nothing about terminals;
  `atlas.site` holds the site generator; `atlas.cli` parses, renders, and
  returns exit codes. See [ADR-0007](docs/decisions/0007-packaged-cli-in-src.md).
- **A compliance registry.** Each gate is a named `Check` with an id, the rule
  it enforces, and a pure function. Twelve ship; `--only <id>` runs one while
  you fix it, `--list` shows what exists, and adopters register their own the
  same way Atlas registers its own. See
  [ADR-0008](docs/decisions/0008-compliance-as-a-registry.md).
- **`atlas doctor`.** Environment and repository diagnostics, each finding
  carrying the command that fixes it.
- **`atlas status`.** The repository's declared classification, ownership, and
  live work on one screen.
- **Shell completion** for bash, zsh, and fish, generated from the command tree.
- **Client-side search** on the documentation site, with `/` and `⌘K` bindings,
  keyboard navigation, and an index fetched on first open rather than on page
  load.
- **A three-state theme control.** Light, dark, and follow-the-system: applied
  before first paint. A binary toggle silently overrides a system preference the
  reader deliberately set and offers no way back.
- **Generated CLI reference** at `docs/reference/cli.md`, rendered from the
  argument parser. CI fails if the committed copy differs, so a flag cannot
  exist undocumented.
- **`docs/guides/install.md`** and
  **`docs/architecture/cli-design.md`**.
- Site: breadcrumbs, previous/next pagination, heading anchors, copy-to-clipboard
  on code blocks, a contents rail that tracks the section in view, a real 404,
  `sitemap.xml`, and `robots.txt`.
- Syntax highlighting for eleven languages (was four), with aliases and an
  escape-rather-than-guess path for unknown ones.
- `atlas work sync --check`: assert the generated artifacts are current without
  writing, for CI.
- `atlas check --strict`: treat skipped gates as failures, for an organisation
  that expects every repository to adopt the full suite.

### Changed

- **Renamed `machine-standard` to `atlas`** throughout: manifest, forge
  metadata, schema `$id`s, banners, architecture diagram, and prose.
- **The site generator is a package**, split into `markdown`, `highlight`,
  `theme`, `layout`, `search`, and `builder`, replacing one 52 KB module.
- **`template/` no longer carries a copy of the tooling.** It depends on the
  published `atlas-standard` package, so a scaffolded repository gets fixes
  without a merge, and one class of drift is gone rather than policed.
- **`scripts/` holds wrappers only.** `scripts/atlas` runs the CLI from a bare
  checkout; `check-compliance.sh` forwards to `atlas check`. No logic remains.
- CI runs a Python 3.10 / 3.12 / 3.13 matrix and asserts the committed CLI
  reference is current.
- `maturity` raised to `stable`; `interfaces` now declares `cli`.

### Fixed

- **Global flags before a subcommand were silently discarded.** `atlas -C /elsewhere
  check` checked the current directory instead: argparse applies a subparser's
  defaults *after* the parent parses, so the subparser copy of each global flag
  overwrote the value already read. Every global flag now parses with
  `SUPPRESS`, and defaults are applied once afterwards.
- **Raw HTML blocks in Markdown were escaped and then un-escaped** by a string
  replacement on the finished page. The renderer now recognises the block.
- **A stale-index check compared generation dates**, so `work/index.yaml` read
  as stale every day at midnight, which trained people to run `sync` reflexively
  and stop reading what it said. Comparison now ignores the date.
- Duplicate headings on a page produced duplicate anchor ids.
- Backticked `**literal**` was rendered bold, because inline emphasis ran before
  code spans were extracted.
- A workstream could be marked `done` with unfinished tasks; `atlas work
  validate` now catches it alongside the missing-evidence case.
- Dependency cycles were reported once per entry point rather than once per
  cycle.

### Removed

- `scripts/work.py`, `scripts/validate.py`, `scripts/build_site.py`,
  `scripts/sync-template.py`, `scripts/new-project.sh`: all superseded by
  `atlas` subcommands. `scripts/check-compliance.sh` remains as a forwarding
  wrapper.
- `template/scripts/work.py` and `template/scripts/requirements.txt`: the
  template depends on the package now.

### Migration

For a repository already using the standard, the contract is unchanged; only the
commands are:

| Was | Now |
|---|---|
| `python scripts/work.py new <slug>` | `atlas work new <slug>` |
| `python scripts/work.py sync` | `atlas work sync` |
| `python scripts/work.py validate` | `atlas work validate` |
| `python scripts/validate.py <file>` | `atlas validate <file>` |
| `scripts/check-compliance.sh` | `atlas check` |
| `scripts/new-project.sh <name> <dir>` | `atlas init <name> <dir>` |
| `python scripts/sync-template.py --check` | `atlas template check` |
| `python scripts/build_site.py` | `atlas site build` |

Scaffolded repositories should delete `scripts/work.py` and add
`pip install atlas-standard` to CI.

## [0.0.1] - 2026-08-07

First cohesive baseline: the canonical repository template for the organization.

Everything below the "Added" heading existed in draft form before this release
and passed its own checks. What v0.0.1 adds is that the repository now agrees
with itself: every fact has one home, every mirror is generated or tested, and
the claims in the documentation are checked against the filesystem rather than
asserted.

### Added

- **Eight specifications** in `spec/`, each normative and versioned `1.0`:
  `workspace.md`, `project.md`, `project-matrix.md`, `project-checklist.md`,
  `admin.md`, `presentation.md`, `library.md`, `workstream.md`.
  Each now carries YAML front matter: `id`, `title`, `tagline`, `question`,
  `version`, `status`, `rule_prefixes`, `checklist_prefixes`, `companions`, so
  the suite is machine-discoverable without parsing prose.
- **JSON Schemas** in `spec/schemas/` for `project.yaml`, `org.yaml`,
  `admin.yaml`, and `workstream.yaml`, encoding the Matrix enums,
  cross-dimension rules, and the presentation metadata contract.
- **`work/`.** The work management system: one numbered workstream per
  initiative with a fixed skeleton of nine numbered sections plus a README and a
  manifest, a generated dashboard and machine index, and `atlas work`
  (`new`, `sync`, `validate`, `archive`).
- **`library/prompts/`.** Reusable request prompts across 14 lifecycle categories, with
  a machine-readable catalog (`index.yaml`) and a human index.
- **`template/`.** A minimal compliant starter repository, usable via "Use this
  template" or `atlas init`, shipping the work management system
  ready to run.
- **`atlas template sync`.** Mirrors `atlas work`,
  `spec/schemas/workstream.schema.json`, and `work/_template/` into `template/`,
  with `--check` wired into CI so the mirror cannot drift.
- **`atlas site build`.** Static documentation site rendering `work/`,
  `spec/`, `docs/`, and `library/prompts/`, styled from `assets/design/tokens.yaml`.
- **Reference documentation**: `docs/reference/glossary.md` (plain-language
  definitions for readers who do not write code), `conventions.md` (naming,
  structure, generated-file rules), `rule-ids.md` (the identifier registry), and
  `versioning.md` (why the suite is `0.0.1` and the standards are `1.0`).
- **`tests/test_spec_metadata.py`.** Asserts front matter completeness, one `h1`
  per specification, no skipped heading levels, registered and non-colliding rule
  prefixes, and agreement between the README, the quick reference, and `spec/`.
- **Tooling**: `atlas validate` (manifest validation, waiver expiry),
  `atlas check`, `atlas init`,
  `scripts/generate_prompts.py`.
- **CI.** Tests, standard-compliance, template-mirror drift, work validation,
  site build, and commit-lint on every pull request; Pages deployment on `main`.
- **Governance**: `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`,
  `CODE_OF_CONDUCT.md`, `CODEOWNERS`, issue and PR templates, and forge
  configuration as code in `.github/settings.yml`.
- **Brand**: `assets/banner.svg` and `assets/architecture.svg`, hand-authored
  and inherited by downstream repositories.

### Changed

- **PROMPT-LIBRARY is now LIBRARY, and governs four asset classes.** The
  standard covered one kind of reusable artifact; a fleet reuses more than
  sentences. Icons get redrawn slightly differently in each repository, font
  files circulate with no licence beside them, and screenshots are committed with
  no record of what produced them. Each is the same failure the prompt catalog
  already solved.

  `prompts/` becomes `library/prompts/`, alongside `icons/`, `typefaces/`, and
  `media/`. Six cross-class rules (`L-A1`–`L-A6`) carry nearly all the weight —
  one home, an index, a descriptive name, recorded provenance, recorded licence,
  review: with a short class-specific section each. The alternative, a standard
  per asset kind, would have multiplied the root and restated the same six rules
  four times. Recorded as [ADR-0006](docs/decisions/0006-library-generalizes-prompts.md).

  The class set is closed: a fifth is added by amending the specification, not by
  creating a folder, and `tests/test_library.py` fails on an unregistered
  directory. `icons/`, `typefaces/`, and `media/` ship empty with an index and a
  contract, because an empty class with a written contract is a place for the
  next asset to land while an absent one is an invitation to invent a folder.

  **Breaking:** rule identifiers `PL-01`–`PL-08` are now `L-01`–`L-08`, and the
  manifest contract moved from `prompt-library/1.0` to `library/1.0`. The root's
  sanctioned extension count is unchanged: `library/` replaces `prompts/`
  rather than adding to it.
- **Colour now carries meaning where meaning exists.** The site was achromatic
  throughout, which read as dull because it under-used the roles the design
  system already ships. Neue permits chroma exactly where it identifies
  something, and requires it never be the only channel doing so.

  Status pills pair a hue with a glyph and the status word; completed progress
  bars turn `success` and carry an `aria-label` with the count; blockquotes
  marked `[!NOTE]`, `[!TIP]`, `[!WARNING]`, or `[!CAUTION]` render as callouts in
  the four status tones with an icon and a title; sidebar groups take a
  `series-*` accent alongside their name label; and prose links read as links.
  Every one of those survives greyscale, colour-blindness, and a screen reader
  (WCAG 1.4.1). A hue that identifies nothing was not added.
- **Banners are two shapes, not one scaled.** The wide banner carried a mark row,
  a wordmark, a meta line, a rule and an eight-name row; at a phone's column
  width that last row rendered about 3.5px tall: present, unreadable, and noisy.
  A banner cannot be responsive, because the forge scales it to the column; it
  can only be swapped. Both READMEs now select a compact variant below 600px via
  `<picture>`, and the wide one is down to a mark, a wordmark, one tagline and
  one right-aligned meta line. The internal margin was cut from 56px to 10px so
  the wordmark's left edge lands on the README text column rather than floating
  44px inside it.
- **The design system is Neue 1.0, and the site conforms to it.** The repository
  now carries the full system at `assets/design/DESIGN.md`, with its front matter
  extracted verbatim to `assets/design/tokens.yaml` and compiled into CSS custom
  properties: colours, the sixteen typography roles, spacing, elevation, motion,
  breakpoints, size classes, regions, and the adaptation table. A test compares
  the extract against the source, because a hand-edited token is a fork.

  The site is the **`reading` shell**: a three-track grid whose rails are one
  token, so the measure is centred rather than pushed left. Content holds 780px
  while the rails compress from 148px to 248px, reaching `rail` exactly at
  `shell` (1468px), after which surplus becomes margin.

  Most consequentially, structure now resolves from the **container**, not the
  viewport. `main` is a container, size-class values are the query thresholds,
  and `@media` is confined to page chrome: gutters and the shell cap. The
  previous layout drove everything from viewport media queries, which is the
  failure Neue names explicitly: a region loses width to a rail and gains a
  column at the same moment.

  Navigation is **one row, three islands** on a `1fr auto 1fr` grid. The row sets
  `pointer-events: none` and each island re-enables it, so the gaps are real and
  the page scrolls visibly through them. The islands do not hide, condense, or
  translate on scroll; past 8px the shadow deepens from `float` to `popover` and
  nothing else moves. Below `lg` the centre track empties and the sidebar plus
  the contents list become one drawer.

  Overflow is now declared rather than incidental. Every wide child owns a
  scroll container that takes `tabindex="0"` and an `aria-label`: a scrollable
  region a keyboard user cannot reach is a WCAG failure, and the edge fade is
  driven by scroll position, so it appears only on the edge that actually has
  content beyond it. `html, body { overflow-x: clip }` is the safety net behind
  that, not the strategy. Code never wraps and never truncates, because a token
  name broken mid-string reads as two identifiers.

  Also from the system: a skip link, one focus ring on every interactive
  element, `dvh` on full-height surfaces, touch targets that do not shrink with
  the viewport, fluid headlines that scale *up* from their floor and never below
  it, and a print stylesheet.
- **ADMIN-CENTER is now ADMIN**, throughout: the display name, the specification
  filename (`spec/admin.md`), the front-matter id, and the manifest contract
  version (`admin-center/1.0` → `admin/1.0`). Every other standard is a single
  word; "ADMIN-CENTER" read as a different kind of noun beside them. **This is a
  breaking change to the manifest contract** and the only one in v0.0.1: taken
  now precisely because the suite is pre-1.0 with no adopters, where it costs
  nothing. Existing `admin.yaml` and `org.yaml` files need `standard: admin/1.0`.
- **README composition.** The title is the project name and the value
  proposition is a sentence beneath it, rather than one long title restating the
  whole description. The badge row is retained and restyled to the achromatic
  palette, and every badge now links to the artifact it asserts —
  `stage` to the manifest, `release` to the changelog, `standard` to the
  versioning note, so a claim is one click from its evidence (P-07).
- **Brand assets are generated, measured, and balanced.**
  `scripts/build_assets.py` emits every SVG from one source. Because monospace
  advance width is a known constant, each string is measured against the box it
  sits in and the build asserts on overflow: the previous architecture diagram
  had 288px of label inside a 272px box. The grid is now uniform (equal row
  heights, 72px gutters, symmetric 48px margins) with box text vertically
  centred, and the banner's mark, wordmark, rule and standards row all share the
  same left and right edges, so the composition fills its canvas instead of
  crowding into the left third. A test re-runs the generator and fails if any
  asset was hand-edited.
- **Brand assets redrawn from the design tokens.** The banners and the
  architecture diagram were dark-blue/purple gradients over a decorative grid,
  which contradicted `assets/design/tokens.yaml`: a monochrome, flat,
  hairline-rule system that reserves chroma for meaning and forbids gradients and
  shadows. They are now achromatic, and each ships a light and a dark variant
  behind `<picture>` with `prefers-color-scheme`.
- **The template README is a working document.** It carries a placeholder
  structure plus a collapsible scaffolding checklist that ends by telling you to
  delete it. It ships the two badges that mirror `project.yaml` (`stage`,
  `maturity`) and tells the reader to add more only once each value is derivable
  from the manifest or CI (P-07).
- **The documentation site is responsive.** Three layouts rather than one desktop
  layout squeezed: an icon bottom bar and off-canvas drawer below 720px, a
  labelled top bar and drawer to 1279px, and a three-column layout with a
  persistent sidebar and sticky TOC above that. Navigation labels shorten before
  they wrap. Previously the sidebar was simply `display:none` below 1024px, so a
  phone had no section navigation at all.
- **Code blocks are syntax-highlighted** for bash, YAML, JSON, and Python by a
  small dependency-free tokenizer, coloured from the `code-*` roles already
  defined in the design tokens, which ship light and dark values documented at
  ≥4.5:1 contrast. Wide tables and code scroll horizontally with a fade
  affordance applied only where content actually overflows.
- **Page and navigation titles come from the documents**, not their filenames.
  The sidebar read `admin` and `0001-self-hosting`; it now reads `ADMIN` and
  `The repository governs itself by the standard it defines`. Specifications sort
  by a declared `order:` in their front matter rather than alphabetically, which
  had put ADMIN before WORKSPACE.

- `maturity` is now `beta`, down from `stable`, and the release badge reads
  `v0.0.1` rather than `1.0.0`. The earlier claim was not supported by the
  suite's own maturity ladder, which requires the Production checklist profile
  and adopters before `stable`.
- Specification `h1` headings name the standard (`# PRESENTATION: …`) instead of
  the filename (`# presentation.md`), and `Part I` / `Part II` divisions are `h2`
  with their sections at `h3`, so each document has one heading tree.
- `atlas validate` selects an ADMIN schema from the manifest's own
  keys rather than from the filename, so a manifest is valid wherever it lives.
- `atlas check` skips gitignored paths instead of listing `site/`
  and `.pytest_cache/` as sanctioned root directories, and now runs the
  template-mirror check.
- `atlas work` resolves its schema from either `spec/schemas/` or `work/`,
  which is what lets one file serve both this repository and every scaffolded one.
- Example manifests follow `<slug>.<kind>.yaml` throughout: `org.yaml` is now
  `acme.org.yaml`, `workstream.yaml` is now `harden-payments-api.workstream.yaml`.
- `README.md`, `AGENTS.md`, and the guides were reorganized around what a reader
  is trying to do rather than around the repository's directory listing.

### Fixed

- The workstream skeleton was described as having **ten** sections in eight
  separate files. It has nine numbered sections; the accompanying prose lists had
  nine items all along.
- The README's architecture alt text said **seven** specifications; the issue
  template said **five**. There are eight.
- Every page rendered its title twice: once in the page header and again as the
  article's `h1`, at two different sizes.
- The changelog claimed **61** tests when there were 63. Test counts are no
  longer stated in prose: a number that changes on every new test does not
  belong in a document.
- `atlas validate` defined `SCHEMA_BY_STANDARD`, which was never read and
  contradicted the function below it.
- `atlas init` moved `project.yaml` onto itself, and broke on
  destination paths containing spaces.

### Removed

Moved to the `@removal-safe` archive, which carries a removal index with the
origin path, size, date, and SHA-256 of every file. Nothing was deleted.

- `assets/design/neue.design.md`: the Neue design system at `version: alpha`,
  vendored into a repository claiming `maturity: stable`, of which only the front
  matter was read. **Superseded by Neue 1.0**, now carried in full as
  `assets/design/DESIGN.md`. Between the two versions the `palette:` group was
  renamed `ramps:`, the component narrative was rewritten, and the structural
  model the site now conforms to: size classes, regions, the adaptation ladder,
  declared overflow, named shells: did not exist in the alpha at all.
- Four fabricated demonstration workstreams that described an imaginary fleet
  migration staffed by invented principals. The generated dashboard reported them
  as live work, and every scaffolded repository would have inherited that claim.
  `work/` now holds one real record.
- Three hand-maintained duplicates under `template/`, one of which had already
  drifted ahead of the canonical copy. They are now generated.

### Known gaps

- `workspace.md` and `project.md` each open with an extended essay before
  reaching a rule. Splitting rationale from rules is a reviewed normative change,
  not an audit side effect.
- Three specifications have no rule identifiers, so their rules must be cited by
  section. The namespaces that do exist are now registered and tested;
  numbering the rest is the follow-up.

Both are tracked in
[`work/01_harden-repository-baseline/09_issues/issues.md`](work/01_harden-repository-baseline/09_issues/issues.md).

[Unreleased]: https://github.com/OWNER/atlas/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/OWNER/atlas/compare/v0.0.1...v1.0.0
[0.0.1]: https://github.com/OWNER/atlas/releases/tag/v0.0.1
