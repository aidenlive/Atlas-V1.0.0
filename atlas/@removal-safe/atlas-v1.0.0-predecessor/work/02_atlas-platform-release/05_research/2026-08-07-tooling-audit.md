# Tooling audit: what the v0.0.1 scripts actually did

Date: 2026-08-07 · Author: agent:builder

Taken before any code moved, to set the scope honestly rather than by
impression.

## The seven programs

| Script | Lines | Invocation | Importable | Tested |
|---|---|---|---|---|
| `build_site.py` | ~1090 | `python scripts/build_site.py` | no | no |
| `generate_prompts.py` | ~560 | `python scripts/generate_prompts.py` | no | output only |
| `work.py` | ~380 | `python scripts/work.py <cmd>` | no | output only |
| `build_assets.py` | ~230 | `python scripts/build_assets.py` | no | output only |
| `check-compliance.sh` | ~90 | `scripts/check-compliance.sh` | no | **no** |
| `sync-template.py` | ~90 | `python scripts/sync-template.py` | no | via CI only |
| `new-project.sh` | ~20 | `scripts/new-project.sh <n> <d>` | no | no |

Four invocation styles across seven programs. Three different ways to report a
failure: `VIOLATION:` on stderr, `FAIL <path>` on stdout, and a bare non-zero
exit.

## What the audit changed about the plan

**`check-compliance.sh` was the priority, not `build_site.py`.** The site
generator was the largest file and the obvious target. But it was *working*, and
its output was checked by the metadata tests. The compliance script was 90 lines
enforcing the repository's central promise with **zero** tests, printing prose
nothing could parse. Extracting it first is what made ADR-0008 a registry rather
than a straight port.

**`sync-template.py` is a symptom.** Its entire job was policing a copy of
`work.py` that should not have existed. Once the template depends on the
published package, the copy is gone and the script's remaining job shrinks to
two mirrored data files: small enough to be a subcommand, not a program.

**The prompt generator stays a script.** It is dev automation that emits
`library/prompts/`, run rarely and by a maintainer. Making it a CLI command
would put a generator for one repository's content into every adopter's tool.
It stays in `scripts/`, which is exactly what PROJECT §9 says `scripts/` is for.

## Counts recorded, so later prose can be checked against them

| Fact | v0.0.1 |
|---|---|
| Specifications | 8 |
| Prompts / categories | 78 / 14 |
| Tests | 98 |
| Compliance checks | 6 (untested) |
| Site pages | 144 |
| Files duplicated into `template/` | 18 |
