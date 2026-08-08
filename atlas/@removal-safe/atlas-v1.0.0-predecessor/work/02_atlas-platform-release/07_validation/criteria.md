# Acceptance criteria: 02 Rebrand to Atlas and ship a first-class CLI

| ID | Criterion | How it is checked |
|---|---|---|
| C-01 | The repository passes its own standard | `atlas check` exits 0 |
| C-02 | The full test suite passes | `python -m pytest tests/ -q` |
| C-03 | Every read command emits valid JSON under `--json` | `tests/test_cli.py`, parametrized |
| C-04 | Exit codes match the documented contract | `tests/test_cli.py` |
| C-05 | The committed CLI reference matches the parser | `test_committed_cli_reference_is_current` |
| C-06 | Compliance gates are pure and deterministic | `tests/test_compliance.py` |
| C-07 | The site builds and emits its deploy contract | `tests/test_site.py` |
| C-08 | No `machine-standard` reference survives outside historical records | repository-wide grep; the changelog and this workstream necessarily name the old identifier |
| C-09 | The template ships no copy of the tooling | `tests/test_workstreams.py` |
| C-10 | Color tokens remain OKLCH-only | `test_colors_are_oklch` |
