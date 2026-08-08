# Quick reference

The whole suite on one page. Every claim here is checked against the repository
by `tests/test_spec_metadata.py`, so it cannot quietly rot.

## The suite in one line each

| Question | Standard | Spec |
|---|---|---|
| Where does a file live? | WORKSPACE | [`spec/workspace.md`](../../spec/workspace.md) |
| What must be true inside a repository? | PROJECT | [`spec/project.md`](../../spec/project.md) |
| What kind of project is it? | MATRIX | [`spec/project-matrix.md`](../../spec/project-matrix.md) |
| Is it good enough? | CHECKLIST | [`spec/project-checklist.md`](../../spec/project-checklist.md) |
| Who may act, who answers, who pays? | ADMIN | [`spec/admin.md`](../../spec/admin.md) |
| How does it show itself? | PRESENTATION | [`spec/presentation.md`](../../spec/presentation.md) |
| Where do shared assets live, and on what terms? | LIBRARY | [`spec/library.md`](../../spec/library.md) |
| What work is happening, by whom, and is it done? | WORKSTREAM | [`spec/workstream.md`](../../spec/workstream.md) |

## The eight dimensions (MATRIX)

`type · stage · maturity · packaging · deployment · ownership · visibility · support`

## Maturity ↔ checklist profile

| Claim | Must pass |
|---|---|
| `experimental` | builds |
| `alpha` | + smoke tests, true quickstart |
| `beta` | Baseline + Beta profile |
| `stable` | + Production profile |
| `hardened` | + Hardened profile |

A maturity claim is the checklist result, never a promise to fill gaps later.

## Lifecycle

`idea → incubating → active → maintenance → deprecated → archived`: rightward
only. Deprecation requires a successor and a sunset date; archival must be
mechanically true on the forge.

## Role ladder (ADMIN)

`observer → contributor → maintainer → admin → owner → steward`

Agents hold at most `maintainer`, always with an expiry.

## The root closed set

Files: `README.md LICENSE CHANGELOG.md AGENTS.md CONTRIBUTING.md project.yaml
CLAUDE.md GEMINI.md SECURITY.md CODE_OF_CONDUCT.md .gitignore`

Directories: `spec/` (or `src/`) `docs/ examples/ tests/ scripts/ assets/
.github/`: plus, in this repository only and by [ADR-0002](../decisions/0002-sanctioned-root-extensions.md),
`template/ library/prompts/ work/`.

Anything else at the root is a violation. Build output is not structure and is
skipped because git ignores it.

## Workstream anatomy

`work/NN_slug/` · nine numbered sections · `01_plan 02_tasks 03_requirements
04_decisions 05_research 06_deliverables 07_validation 08_agents 09_issues` ·
plus `README.md` and `workstream.yaml`, which are not sections.

Status: `planned → active → (blocked ↔ active) → review → done`, or `cancelled`.

Progress is counted from the task table, never asserted. `done` requires
evidence for every acceptance criterion.

## Library

Four classes, a closed set: `prompts/` `icons/` `typefaces/` `media/`. Every
asset has one home (L-A1), an index entry (L-A2), a name describing the thing
(L-A3), recorded provenance (L-A4) and license (L-A5), and arrives by pull
request (L-A6).

## Prompt anatomy

14 categories · `request-<verb>-<object>.txt` · one to three sentences ·
single-objective · tool-agnostic · plan-before-act wording for anything
destructive. Generated from `scripts/generate_prompts.py`; never hand-edited.

## Citing a rule

`PRESENTATION P-02`, `WORKSTREAM W-15`, `CHECKLIST SEC-03`. Specifications
without rule identifiers are cited by section: `PROJECT §9`. Full registry in
[`rule-ids.md`](rule-ids.md).

## Two version numbers

`v0.0.1` is this repository's release. `project/1.0` is the manifest contract.
They move independently. See [`versioning.md`](versioning.md).

## Commands

```bash
pip install atlas-standard            # the CLI
pip install -e ".[dev]"               # working on Atlas itself

atlas check                           # this repository obeys its own standard
atlas status                          # what it is, and where it stands
atlas doctor                          # environment + repository diagnostics
atlas validate <manifest>             # one manifest against its schema
atlas init <name> <dest>              # scaffold a compliant repository
atlas work new|list|show|sync|validate|archive
atlas spec list|show|rules            # read the standards, cite their rules
atlas prompt list|show|search         # the reusable request library
atlas library list|check              # shared assets
atlas template check|sync             # refresh or verify template/
atlas site build|serve|clean          # the documentation site
atlas completion bash|zsh|fish        # shell completion

python -m pytest tests/ -q            # the full suite
python scripts/generate_prompts.py    # regenerate library/prompts/
python scripts/build_assets.py        # regenerate the brand SVGs
scripts/atlas <command>               # any of the above, with no install
```

Every command takes `--json`, `-C <dir>`, `--quiet`, and `--no-color`.
Exit codes: `0` ok · `1` violations · `2` usage · `3` not found · `4` not a
repository. Full detail: [`cli.md`](cli.md).
