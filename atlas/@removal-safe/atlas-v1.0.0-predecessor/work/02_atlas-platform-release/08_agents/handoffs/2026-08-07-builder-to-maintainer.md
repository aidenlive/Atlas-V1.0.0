# Handoff: agent:builder → person:maintainer

Date: 2026-08-07 · Workstream: 02 · Status at handoff: done

## What was done

The tooling moved from `scripts/` to `src/atlas/` as an installable package, a
twelve-command CLI was built on top of it, the site generator was split by
concern and given search, and the suite was renamed to Atlas. All nine tasks are
closed with evidence in [`07_validation/evidence.md`](../../07_validation/evidence.md).

The eight specifications were not touched. No rule was added, removed, or
renumbered.

## State at handoff

- `atlas check`: 12 gates, 0 failures
- `python -m pytest tests/ -q`: 202 passed
- `atlas site build --write-reference`: 177 pages, leaves the tree clean

## What is NOT done, and needs a human

1. **`OWNER` is still a placeholder** in `project.yaml`, `.github/settings.yml`,
   `CHANGELOG.md`, and `.github/CODEOWNERS`. Replace it before publishing.
2. **The PyPI name `atlas-standard` is unclaimed.** Nothing verifies it is
   available. Check before tagging `v1.0.0`.
3. **No release has been cut.** `pyproject.toml` says `1.0.0` and the changelog
   has the entry, but there is no tag and no published artifact. See I-01: CI
   does not yet prove the built wheel installs.
4. **`maturity: stable` is a claim I raised.** It is defensible: the Production
   profile passes, but a maturity claim should be reviewed by the accountable
   owner, not asserted by the agent that did the work. Confirm or lower it.

## Judgement calls worth reviewing

- **The prompt generator stayed a script.** It generates one repository's
  content; making it a CLI command would put it in every adopter's tool. If you
  disagree, it is a small move.
- **The template now depends on a published package** rather than carrying a
  copy. This trades offline scaffolding for the removal of a whole drift class
  (I-02). It is the decision I would most expect you to want to revisit.
- **Skipped compliance gates report as "skip", not "pass".** A repository that
  adopts nothing therefore passes trivially. `--strict` exists for organisations
  that consider that unacceptable; the default is permissive.
