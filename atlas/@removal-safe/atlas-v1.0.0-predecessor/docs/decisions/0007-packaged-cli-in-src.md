# 7. The tooling is a package in `src/`, with a first-class CLI

Date: 2026-08-07

## Status

Accepted. Extends [ADR-0002](0002-sanctioned-root-extensions.md).

## Context

Through v0.0.1 the tooling was seven programs in `scripts/`: `validate.py`,
`work.py`, `check-compliance.sh`, `new-project.sh`, `sync-template.py`,
`build_assets.py`, `build_site.py`. Each had its own invocation style, its own
output conventions, and its own idea of how to report a failure.

Three specific problems followed from that shape.

**Nothing could import it.** `scripts/` is dev automation, not a package. Tests
either re-implemented the logic they were checking or shelled out and parsed
stdout. The compliance checks in `check-compliance.sh` had no tests at all,
because testing a bash script that `cd`s to the repository root and exits
non-zero is more work than the check itself.

**Reuse meant copying.** `template/` needed a working work system, and the only
way to give it one was to copy `scripts/work.py` in. That copy drifted: the
template's version gained a schema-path resolver the canonical one never
received, which is what prompted `sync-template.py`, a script whose entire job
was policing a copy that should not have existed.

**Discovery was directory listing.** There was no way to find out what the
tooling could do except to read `scripts/`, and no way to find out what a script
accepted except to read its source.

PROJECT §9 already sanctions `src/` as "the product; all shipped code; one
importable root". The tooling had simply never been treated as shipped code.

## Decision

The tooling moves to `src/atlas/`, a packaged, installable Python library with a
CLI entry point.

- `atlas.core` holds domain logic: manifests, specs, workstreams, library,
  template mirroring, tokens, compliance. It has no knowledge of terminals,
  argument parsing, or exit codes.
- `atlas.site` holds the static site generator, split by concern.
- `atlas.cli` holds the argparse command tree. Each command parses, calls one
  core function, renders, and returns an exit code.
- `pyproject.toml` at the root declares the package and the `atlas` console
  script.

`scripts/` survives as thin wrappers so a bare checkout still works with no
install, and so the paths CI has always used keep working. They contain no
logic.

`template/` no longer carries a copy of the tooling. It depends on the published
`atlas-standard` package, so a scaffolded repository gets fixes without a merge.

### Root closed set

Two root entries are added to the sanctioned set: `src/` (already named by
PROJECT §9, previously unused here) and `pyproject.toml`.

`pyproject.toml` is not a dotfile, so PROJECT §9's "tool dotfiles" clause does
not cover it. It is admitted deliberately rather than by stretching that clause:
it is the Python ecosystem's single declaration point for build backend,
dependencies, entry points, and tool configuration, and the alternative is four
or five dotfiles carrying the same information. One named file is the better
trade, and naming it here is cheaper than pretending it is something it is not.

## Consequences

**Good.** The logic is importable and directly unit-testable: the compliance
engine went from zero tests to full coverage because testing it is now a
function call. Adopters can register their own gates in Python. The template
carries no copy of anything executable, so one class of drift is gone rather
than policed. Discovery is `atlas --help`. The CLI reference is generated from
the parser, so it cannot drift either.

**Costs.** The repository now has a build system and a packaging story it did
not have, which is a real maintenance surface: a release means publishing to
PyPI, not only tagging. Contributors need `pip install -e .` to get the entry
point, though `scripts/atlas` covers anyone who cannot or would rather not.

**Rejected: keeping the scripts and adding a dispatcher.** A single `atlas.sh`
forwarding to seven scripts would have given discovery without the packaging
work. It fixes the smallest of the three problems and neither of the others: the
logic stays unimportable and the template still needs its copy.

**Rejected: publishing the specs and the tooling as separate packages.** Cleaner
in principle, and wrong in practice at this size: the tooling's whole purpose is
enforcing these specifications, and two release cadences for one contract is a
version-skew problem invented for no benefit.
