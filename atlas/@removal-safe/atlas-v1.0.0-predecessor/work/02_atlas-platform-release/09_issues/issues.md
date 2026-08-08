# Issues, blockers & risks: 02 Rebrand to Atlas and ship a first-class CLI

Status values: `open · mitigated · resolved`

| ID | Kind | Description | Owner | Severity | Status |
|---|---|---|---|---|---|
| I-01 | risk | Publishing to PyPI is now part of releasing, and nothing in CI verified the package installs from a built artifact. **This risk materialised before the first release**: `.gitignore` excluded `src/atlas/site/` and no check could see it, because every check ran against the source tree. CI now builds a wheel, installs it into a clean virtual environment, and runs the CLI from outside the source tree. | person:maintainer | medium | resolved |
| I-02 | risk | The template depends on a published package, so scaffolding needs network access. Offline scaffolding regressed relative to the copied script. Accepted deliberately — a copy is a fork with a delay — but it is a real trade, not a free win. | person:maintainer | low | mitigated |
| I-03 | issue | Compliance gates run in registration order, which is implicit. Making it explicit needs a priority field that nothing yet requires; noted so the next person does not read the ordering as meaningful. | person:maintainer | low | open |
| I-04 | issue | Gates are registered by decorator, so a third party must edit the repository to add one. Entry-point discovery is the right answer eventually and premature now (ADR-0008). | person:maintainer | low | open |
| I-05 | risk | The syntax highlighter is a tokenizer, not a parser, so it will mis-highlight edge cases. Deliberate: a parser dependency can break the docs build. Unknown languages escape rather than guess, which bounds the damage. | person:maintainer | low | mitigated |

## I-01, in detail

Worth writing down, because the failure was invisible from every angle the
project was looking from.

`.gitignore` carried `site/` to exclude the generated documentation site. Git
patterns without a leading slash match at any depth, so the same line excluded
`src/atlas/site/`: the site generator package. Nothing on the author's machine
could detect this: the files were on disk, imports resolved, 202 tests passed,
`atlas check` was green, and the delivered archive contained every file because
`zip` does not consult `.gitignore`.

The first symptom was `ModuleNotFoundError: No module named 'atlas.site'` from
an installed console script in CI, thrown at import time before any command ran.

Two things were wrong, and only fixing both helps:

1. **The pattern.** Anchored to `/site/`. A test now asserts that no source file
   is git-ignored, and a second asserts that build-output patterns stay
   anchored, so the fix survives the next person who adds `dist/`.
2. **The blind spot.** An editable install imports `src/` off the filesystem, so
   *no* test running in the source tree could have caught this, however many
   there were. The check that catches it has to install a built artifact into a
   clean environment and run it from somewhere else. That job now exists.

The generalisable lesson: a test suite that only ever runs against the working
tree cannot verify what ships. Packaging needs a check that leaves the tree.
