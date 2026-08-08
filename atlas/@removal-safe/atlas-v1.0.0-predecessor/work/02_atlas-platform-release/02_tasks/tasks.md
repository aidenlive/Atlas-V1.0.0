# Tasks: 02 Rebrand to Atlas and ship a first-class CLI

Canonical tracker. `atlas work sync` counts these rows into the dashboard,
so the table shape matters: `T-NN` ids, one owner per non-todo task, evidence
on every `done` (W-12, W-13).

Status values: `todo · active · blocked · done · dropped`

| ID | Task | Owner | Status | Evidence |
|---|---|---|---|---|
| T-01 | Audit the v0.0.1 tooling surface and record what each script does | agent:builder | done | [`05_research/2026-08-07-tooling-audit.md`](../05_research/2026-08-07-tooling-audit.md) |
| T-02 | Extract domain logic into `src/atlas/core/` with no terminal dependency | agent:builder | done | `src/atlas/core/`, ADR-0007 |
| T-03 | Replace the shell compliance script with a gate registry | agent:builder | done | ADR-0008, `tests/test_compliance.py` |
| T-04 | Build the `atlas` CLI: twelve commands, grouped help, stable exit codes | agent:builder | done | `src/atlas/cli/`, `tests/test_cli.py` |
| T-05 | Generate the CLI reference from the parser and prove it current in CI | agent:builder | done | `docs/reference/cli.md`, `test_committed_cli_reference_is_current` |
| T-06 | Split the site generator by concern; add search, theme, 404, sitemap | agent:builder | done | `src/atlas/site/`, `tests/test_site.py` |
| T-07 | Package as `atlas-standard`; reduce `scripts/` to wrappers | agent:builder | done | `pyproject.toml`, `scripts/README.md` |
| T-08 | Cut the template over to the published package, dropping its copy | agent:builder | done | `test_template_no_longer_ships_a_copy_of_the_tooling` |
| T-09 | Rename to Atlas across manifest, metadata, schemas, assets, and prose | agent:builder | done | `atlas check`, regenerated `assets/*.svg` |
