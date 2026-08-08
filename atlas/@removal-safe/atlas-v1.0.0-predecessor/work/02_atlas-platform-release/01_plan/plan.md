# Plan: 02 Rebrand to Atlas and ship a first-class CLI

## Problem

`v0.0.1` shipped a specification suite that passed its own checks and could not
be operated without reading its source. Three symptoms, one cause.

**The tooling was not a product.** Seven programs in `scripts/`: `validate.py`,
`work.py`, `check-compliance.sh`, `new-project.sh`, `sync-template.py`,
`build_assets.py`, `build_site.py`: each with its own argument style, output
format, and failure convention. There was no way to learn what the tooling could
do except to list a directory, and no way to learn what a script accepted except
to read it.

**Nothing could be imported.** `scripts/` is not a package. Tests either
re-implemented the logic they checked or shelled out and parsed stdout. The
compliance checks had no tests at all, because testing a bash script that `cd`s
to the root and exits non-zero costs more than the script.

**Reuse meant copying.** `template/` needed a working work system, so
`scripts/work.py` was copied into it, and the copy drifted, which is what
`sync-template.py` existed to police.

The name was a fourth problem of a different kind: `machine-standard` describes
a category, not a product, and nothing about it is memorable at a command prompt.

## Approach

Four passes, in order, each leaving the repository green.

1. **Extract.** Move the logic out of `scripts/` into `src/atlas/`, split into
   `core` (domain, no terminal), `site` (generation), and `cli` (parse, render,
   exit). PROJECT §9 already sanctions `src/`; it had simply never been used.
2. **Build the CLI.** One command, subcommand tree, grouped and exampled help,
   stable exit codes, `--json` everywhere. Generate the reference from the
   parser so it cannot drift.
3. **Rebuild the site.** Split the 52 KB generator by concern; add search, a
   theme control, breadcrumbs, pagination, a 404, and a sitemap.
4. **Rename.** Atlas throughout: manifest, forge metadata, schema `$id`s,
   banners, diagram, prose.

## Non-goals

- **No normative change.** Not one rule added, removed, or renumbered. A rebrand
  that quietly edits the contract is how adopters learn not to upgrade.
- **No renumbering of rule identifiers.** Carried over from 01 and still true:
  renumbering breaks every existing citation.
- **No new asset classes, no ninth standard.**

## Risks accepted

- **A packaging surface the repository did not have.** A release now means
  publishing to PyPI, not only tagging. Accepted: an uninstallable CLI is not a
  CLI. Mitigated by `scripts/atlas`, which runs everything from a bare checkout.
- **The template now depends on a published package.** A scaffolded repository
  needs network access to install it. Accepted: it replaces a *copy*, and a copy
  is a fork with a delay.
