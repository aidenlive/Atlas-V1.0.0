# Deliverables: 02 Rebrand to Atlas and ship a first-class CLI

| Deliverable | Location | Replaces |
|---|---|---|
| Installable package | [`src/atlas/`](../../../src/atlas/), [`pyproject.toml`](../../../pyproject.toml) | seven unimportable programs in `scripts/` |
| The `atlas` CLI | `src/atlas/cli/` | four invocation styles |
| Compliance registry | `src/atlas/core/compliance.py` | `check-compliance.sh` |
| Site generator, split by concern | `src/atlas/site/` | one 52 KB module |
| Generated CLI reference | [`docs/reference/cli.md`](../../../docs/reference/cli.md) | nothing — it did not exist |
| Install guide | [`docs/guides/install.md`](../../../docs/guides/install.md) | nothing |
| CLI design record | [`docs/architecture/cli-design.md`](../../../docs/architecture/cli-design.md) | nothing |
| ADR-0007, ADR-0008 | [`docs/decisions/`](../../../docs/decisions/) | — |
| Script wrappers | [`scripts/`](../../../scripts/) | the programs themselves |
| Atlas brand assets | [`assets/`](../../../assets/) | `machine-standard` wordmark and mark |

## Counted, not asserted

| Fact | Before | After |
|---|---|---|
| Tests | 98 | 202 |
| Compliance checks | 6 (untested) | 12 (fully tested) |
| Site pages | 144 | 177 |
| Highlighted languages | 4 | 11 |
| Executable files copied into `template/` | 1 | 0 |
| Commands to learn the tooling | list a directory | `atlas --help` |
