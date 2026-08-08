# Rule identifiers

A rule you cannot cite is a rule you cannot waive, review, test, or argue with.
This page is the registry of every identifier namespace the suite uses.

## The pattern

Each specification owns up to two namespaces:

| Kind | Meaning | Example |
|---|---|---|
| **Rule prefix** | A normative statement. Something that must be true. | `P-02` — the README opens with a hero visual |
| **Checklist prefix** | A gate that checks one or more rules at a maturity level. | `PR-02` — Baseline: README opens with a hero visual with alt text |

The split exists because the two answer different questions. A rule says *what
is required*; a checklist item says *when you have to have it*. One rule can be
checked at several levels, and one checklist item can cover several rules.

## Registry

Declared in each specification's front matter as `rule_prefixes` and
`checklist_prefixes`, and asserted by `tests/test_spec_metadata.py`.

| Specification | Rules | Checklist | Notes |
|---|---|---|---|
| WORKSPACE | — | — | Unnumbered; cite by section (see below) |
| PROJECT | — | — | Unnumbered; cite by section |
| MATRIX | — | — | Unnumbered; the dimensions `D1`–`D8` serve as its addresses |
| CHECKLIST | — | `AX- BD- CI- CL- DC- GA- GD- GX- HD- ID- OPS- QG- RL- SEC- ST- TS-` | The whole document is checklist items, grouped by concern |
| ADMIN | `I-` invariants, `R-` roles | — | |
| PRESENTATION | `P-` | `PR-` | |
| LIBRARY | `L-` prompts · `L-A` all classes · `L-I` icons · `L-T` typefaces · `L-M` media | — | One namespace per asset class, so a rule names the class it governs |
| WORKSTREAM | `W-` rules, `W-I` invariants | `WS-` | |

## Known gaps

**Three specifications have no identifiers.** WORKSPACE, PROJECT, and MATRIX
state their rules in numbered prose sections, so the only way to cite one is
`PROJECT §9`. That is coarser than a rule id and it makes those rules harder to
waive or test.

They were left unnumbered in v0.0.1 on purpose. Assigning identifiers means
choosing where each rule begins and ends, which is a normative judgement about
documents that are currently essays: it needs review, not an audit pass. Tracked
as issue I-02 in [`work/01_harden-repository-baseline/`](../../work/01_harden-repository-baseline/09_issues/issues.md).

Until then: **cite unnumbered rules as `SPEC §N`**, using the standard's short
name and its section number, e.g. `WORKSPACE §11`, `PROJECT §15`.

## Workstream-local identifiers

Inside a workstream, four short namespaces are **local to that directory** and
carry no relationship to the specification namespaces above:

| Prefix | Meaning | Lives in |
|---|---|---|
| `T-` | Task | `02_tasks/tasks.md` |
| `R-` | Requirement | `03_requirements/requirements.md` |
| `C-` | Acceptance criterion | `07_validation/criteria.md` |
| `M-` | Milestone | `01_plan/milestones.md` |
| `I-` | Issue, blocker, or risk | `09_issues/issues.md` |

`R-` and `I-` collide by spelling with ADMIN's role and invariant
prefixes. The collision is tolerable because the scopes never meet: a
workstream's `I-01` is unambiguous inside `work/NN_slug/`, and a specification's
`I-1` is unambiguous in `spec/`. When citing across that boundary, qualify it:
`ADMIN I-1` or `work/01 I-01`.

## Adding a namespace

1. Choose a prefix not in the table above.
2. Declare it in the specification's front matter.
3. Add a row here.
4. `tests/test_spec_metadata.py` will fail until the registry and the front
   matter agree, which is the point.

Changing an existing prefix is a **breaking** change: it invalidates every
citation, waiver, and checklist cross-reference already written against it.
