## What this changes

<!-- One sentence. If it changes a rule, name the rule. -->

## Kind of change

- [ ] Editorial — wording, examples, formatting, a prompt
- [ ] Standard — a rule added, changed, or removed
- [ ] Tooling — the CLI, a gate, or the linter

## Checks

- [ ] `atlas check` passes
- [ ] `atlas lint --changed --strict` passes, or each remaining warning is deliberate
- [ ] `python -m pytest tests/ -q` passes
- [ ] Generated files regenerated, if their sources changed

## If this changes a rule

- [ ] Prose in `spec/` updated
- [ ] Schema updated, if the rule is machine-checkable
- [ ] Standard version bumped in `project.yaml`
- [ ] `CHANGELOG.md` entry naming the rule and what to do about it
