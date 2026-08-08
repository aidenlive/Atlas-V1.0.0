# Adopting the standard in an existing repository

One bounded pass per repository. Total: an honest afternoon.

## 1. Manifest first (15 minutes)

Copy `template/project.yaml` and classify the project honestly along the eight
MATRIX dimensions ([`spec/project-matrix.md`](../../spec/project-matrix.md)). Classification forces the conversations: owner? stage?
successor?: that restructuring alone lets you avoid.

```bash
atlas validate project.yaml
```

## 2. Root cleanup (30 minutes)

Create the required root documents (stubs are fine to start). Move stray root
entries into their role directories. Delete dead files in one labeled commit
with a changelog entry: git is the archive, so no graveyard directories.

## 3. Consolidate truth (1–2 hours)

Find every fact stated in more than one place and give it a single home, with
links everywhere else. Write `AGENTS.md` with all seven sections, verifying
each command actually runs. Reduce vendor agent files to three-line stubs.

## 4. Present it (30 minutes)

Add the `metadata:` block to the manifest, a hero visual inheriting the fleet
banner geometry from `assets/`, and `.github/settings.yml` mirroring the
metadata. PRESENTATION items PR-01 through PR-04 are the bar.

## 5. Wire enforcement (1 hour)

Adapt `.github/workflows/ci.yml` and `atlas check` to the
project. Enable branch protection and `CODEOWNERS`.

---

Then claim a maturity level only when its PROJECT-CHECKLIST profile passes.
The claim *is* the checklist result, never a gap-fill-later promise.

Prompts for each of these steps live in
[`library/prompts/repository/`](../../library/prompts/repository/). If a term in this guide is
unfamiliar, [`docs/reference/glossary.md`](../reference/glossary.md) defines it.
