# Changelog

Notable changes to Atlas. Dates are ISO; newest first.

Two version numbers move here and they are not the same number: the **release
version** of the tooling (`1.0.0`) and the **standard version** every repository
declares (`editorial/1.0`). See [docs/reference/versioning.md](docs/reference/versioning.md).

## [1.0.0] - 2026-08-08

First release of Atlas as a company-wide editorial system. Rebuilt from first
principles; the predecessor repository is archived under `@removal-safe/` and
superseded in full (see [ADR-0005](docs/decisions/0005-archive-then-rebuild.md)).

### Added

- **The standard `editorial/1.0`**: eight standards — VOICE, LANGUAGE,
  STRUCTURE, CONTENT, MATRIX, CHECKLIST, AUTHORITY, PUBLICATION — defining 69
  numbered rules, each carrying a permanent identifier.
- **Four JSON Schemas** for the project manifest, the authority manifest,
  document front matter, and workstream manifests.
- **`atlas`**, a command-line tool with eleven commands, grouped help, `--json`
  on every command, and exit codes that distinguish violations from misuse.
- **Fourteen compliance gates** in a registry, selectable one at a time with
  `atlas check --only`.
- **A prose linter** with eleven rules, run over a file, a directory, or what a
  branch changed. Errors fail a run; warnings are judgement calls a writer may
  keep.
- **A lexicon** at `library/lexicon/terms.yaml`, read directly by the linter, so
  house terminology is data rather than advice.
- **A prompt library** of 56 written-once requests across 14 stages of a piece
  of writing.
- **A work system**: numbered workstreams with five fixed sections, a dashboard
  and index generated from the task tables.
- **A starter template** that passes every gate on its first run, verified by
  scaffolding it during the check rather than by inspection.
- **Documentation**: five guides, six references, two architecture explainers,
  and seven decision records.
- **93 tests**, including a self-hosting suite asserting that this repository
  passes the standard it defines, and a check that the starter template passes
  on its first run from a clean install.

### Changed

- The README leads with a terminal transcript of `atlas lint` finding real
  violations, instead of a wordmark and a tagline. The transcripts are recorded
  by running the commands (`scripts/build_screenshots.py`), so a screenshot
  cannot show a result the tool does not produce.
- `atlas lint` prints each finding's severity on its own line, so a reader can
  see which findings fail the run without counting against the header.
- Counts in CLI output are pluralised. An editorial tool does not print
  "1 files".

- The suite now governs **writing**, where the predecessor governed **repository
  structure**. The architecture, the manifest model, and the CLI philosophy are
  carried over; none of the files are.
- `admin.yaml` becomes `authority.yaml`, and roles hold authority rather than
  people.
- Workstreams drop from nine sections to five, matching the editorial life cycle
  rather than a software one.

### Removed

- The decorative banner. It repeated the repository name and the tagline
  directly above the same name and tagline, and told a first-time reader
  nothing.
- The documentation site generator. It was a second rendering pipeline to
  maintain, and it is not what makes writing better.
- The icon, typeface, and media registries. Only the assets that carry editorial
  meaning remain: the lexicon, the prompts, and the content templates.

### Deprecated

- `@removal-safe/` is exempt from every check and **will be deleted no later
  than 2027-02-08**, once the predecessor is published to its own repository
  with its history intact.
