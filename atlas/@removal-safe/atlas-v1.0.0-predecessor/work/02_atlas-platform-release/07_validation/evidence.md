# Evidence: 02 Rebrand to Atlas and ship a first-class CLI

One row per criterion: how it was checked, by whom, when, and the result.
An unattributed checkmark is not evidence (W-08).

| Criterion | Check performed | By | Date | Result |
|---|---|---|---|---|
| C-01 | `atlas check` — 12 gates | agent:builder | 2026-08-07 | pass |
| C-02 | `python -m pytest tests/ -q` — 202 tests | agent:builder | 2026-08-07 | pass |
| C-03 | 9 commands parametrized through `json.loads` | agent:builder | 2026-08-07 | pass |
| C-04 | Asserted for OK, FAILURE, USAGE, NOT_FOUND, NO_REPOSITORY | agent:builder | 2026-08-07 | pass |
| C-05 | Rendered reference compared to the committed file | agent:builder | 2026-08-07 | pass |
| C-06 | Two runs compared for disk mtimes and report equality | agent:builder | 2026-08-07 | pass |
| C-07 | Build asserted for 404, sitemap, robots, search index, `.nojekyll` | agent:builder | 2026-08-07 | pass |
| C-08 | `grep -rn "machine-standard"` across the tree, excluding build output | agent:builder | 2026-08-07 | 5 matches, all historical: this record and the changelog entry naming the rename. 0 in shipped surfaces. |
| C-09 | `template/scripts/work.py` asserted absent | agent:builder | 2026-08-07 | pass |
| C-10 | Every resolved color token asserted to start `oklch(` | agent:builder | 2026-08-07 | pass |

## Defects found by these checks, and fixed

| Defect | Found by | Fix |
|---|---|---|
| `atlas -C <dir>` silently operated on the current directory instead. Argparse applies a subparser's defaults after the parent parses, so each subparser copy of a global flag overwrote the value already read. | C-04 | Every global flag parses with `SUPPRESS`; defaults applied once in `resolve_globals()` |
| The rewritten stylesheet dropped the `@container content` wide break-out, silently reverting structure to viewport-driven | C-07 (existing metadata test) | Rule restored with its rationale |
| `render_reference` rebound `lines` inside a closure via `+=`, shadowing the list being built | C-05 | `list.extend` |
| A quoted `{PROJECT_NAME}` in the install guide tripped the placeholder check | C-07 | Check ignores code elements and inspects prose only |
