---
id: workstream
order: 8
title: WORKSTREAM
tagline: "The work management standard: every initiative is a numbered, isolated, verifiable workstream"
question: "What work is happening, by whom, and is it done?"
version: "1.0"
status: stable
rule_prefixes: [W-, W-I]
checklist_prefixes: [WS-]
companions: [project, admin, library]
---

# WORKSTREAM: Every initiative is a numbered, isolated, verifiable workstream

---

> A plan in someone's head is a rumor. A plan in a chat thread is a rumor with
> a timestamp. A workstream is a plan with a number, an owner, a location, and
> a verification step, and that is the difference between work you can audit
> and work you can only remember.

---

## 0. What This Is

The suite governs files (WORKSPACE), repositories (PROJECT), classification
(MATRIX), quality (CHECKLIST), authority (ADMIN), presentation
(PRESENTATION), and requests (LIBRARY). What remained unstandardized is
the **work itself**: the initiatives that carry a repository from one state to
another, and the coordination between the humans and agents executing them.

WORKSTREAM defines `work/`: a single, indexed, human-readable home for every
initiative in a repository. It is deliberately *not* an issue tracker. Trackers
are excellent at tickets: small, fungible units with a state machine. They are
poor at initiatives: the multi-week efforts with a plan, a rationale, evidence,
several agents, and a handoff trail. Those belong in the repository, in
Markdown, versioned alongside the code they change, where a diff shows how the
thinking moved and where an agent can read the whole context without an API
token.

**The bet:** *the plan and the artifact should live in the same commit.*

## 1. Core Invariants

- **W-I1 One home per initiative.** Every initiative is exactly one
  workstream directory. Work that has no workstream is work no one can audit.
- **W-I2 Markdown is canonical.** Every fact a human must read is Markdown in
  `work/`. YAML manifests carry the machine view; the generated site carries
  the browsing view. Both are *derived*: if they disagree with the Markdown,
  they are wrong.
- **W-I3 Numbered and immutable.** A workstream's number is assigned once and
  never reused, never renumbered. Numbers are addresses, not rankings.
- **W-I4 Isolated.** A workstream owns its directory completely; nothing
  outside it is edited by reaching in, and no workstream writes into another.
  Cross-workstream relationships are *declared* (`depends_on`, `blocks`,
  `relates_to`), never implied by shared files.
- **W-I5 Verification is part of the work.** A workstream cannot reach
  `done` without evidence in `07_validation/`. "It works" is a claim; a
  recorded check is a fact.
- **W-I6 Every unit has one owner.** Workstreams, tasks, and agent
  assignments each name exactly one accountable principal (ADMIN
  identity syntax). Shared ownership is no ownership.

## 2. Directory Layout (normative)

```
work/
  README.md              generated dashboard: every workstream, status, owner
  index.yaml             generated machine index: the agent's entry point
  _template/             the canonical workstream skeleton, copied by tooling
  NN_slug/               one directory per workstream (see §3)
  archive/               completed and cancelled workstreams, moved intact
```

- **W-01 Root.** `work/` sits at the repository root, beside `docs/` and
  `src/`. It is the answer to "what is being done here?" as `docs/` is the
  answer to "how does this work?"
- **W-02 Naming.** `NN_slug`: zero-padded ordinal, underscore, then a
  lowercase-hyphenated verb-first slug: `01_setup-root-workspace`,
  `02_review-and-plan-migration`. The underscore separates the *address* from
  the *name*; the hyphens keep the name consistent with every other identifier
  in the suite.
- **W-03 Width grows, numbers don't shift.** Pad to two digits until 99, then
  three. Existing directories are never renumbered when the width grows —
  `99_x` and `100_y` coexist. Sorting is numeric, not lexical, and the tooling
  sorts on the parsed integer.
- **W-04 Archive, don't delete.** A finished workstream moves to
  `work/archive/` intact, keeping its number. This is not a graveyard
  (PROJECT §3): the directory is a completed record with a terminal status, not
  abandoned material kept "just in case."

## 3. Workstream Anatomy (normative)

Every workstream contains exactly this skeleton. Numbered sections give humans
and agents a stable reading order and make "where does this go?" answerable
without judgment.

```
NN_slug/
  README.md              charter + live status; the workstream's front page
  workstream.yaml        machine manifest (§4)
  01_plan/               plan.md, milestones.md: the approach and its dates
  02_tasks/              tasks.md (canonical) + tasks.yaml (derived): the tracker
  03_requirements/       requirements.md, references.md: what must be true, and sources
  04_decisions/          NNNN-title.md: ADRs scoped to this workstream
  05_research/           notes, spikes, findings; dated, append-only in spirit
  06_deliverables/       the artifacts this workstream exists to produce
  07_validation/         acceptance criteria + recorded evidence of each check
  08_agents/             assignments.md, handoffs/, logs/: the coordination layer
  09_issues/             open issues, blockers, and risks with owners
```

- **W-05 Complete skeleton.** All ten entries exist from creation. An empty
  section carries a one-line placeholder stating it is intentionally empty. A
  missing directory is indistinguishable from forgotten work; an empty one is
  a declaration.
- **W-06 Deliverables versus outputs.** `06_deliverables/` holds finished
  artifacts (or pointers to where they landed in the repository).
  `08_agents/logs/` holds raw agent transcripts and intermediate output. Never
  the reverse: a deliverables directory full of transcripts is unusable to a
  reviewer.
- **W-07 Decisions are local, then promoted.** Decisions affecting only the
  workstream live in its `04_decisions/`. A decision that outlives the
  workstream is promoted to `docs/decisions/` with a link back to its origin.
- **W-08 Evidence, not assertion.** Each acceptance criterion in
  `07_validation/` records how it was checked, by whom, when, and the result.
  Command output, a review sign-off, or a link to a CI run all qualify; an
  unattributed checkmark does not.

## 4. Metadata (normative)

`workstream.yaml` is the machine view, validated against
`spec/schemas/workstream.schema.json`:

```yaml
standard: workstream/1.0
id: "01"
slug: setup-root-workspace
title: Set up the root workspace
status: active            # planned | active | blocked | review | done | cancelled
owner: person:jdoe        # exactly one accountable principal
opened: 2026-08-07
target: 2026-08-21        # optional
closed: null
progress: { tasks_total: 12, tasks_done: 5 }
depends_on: []            # workstream ids
blocks: []
relates_to: []
agents:
  - { id: agent:planner,  role: orchestrator, scope: "whole workstream" }
  - { id: agent:migrator, role: sub-agent,    scope: "03_requirements, 06_deliverables" }
tags: [migration, tooling]
```

- **W-09 Status is a closed enum** with rightward-biased movement:
  `planned → active → (blocked ↔ active) → review → done`, with `cancelled`
  reachable from any non-terminal state. `done` requires validation evidence
  (W-I5) and `closed` set.
- **W-10 Progress is counted, not felt.** `progress` is derived from
  `02_tasks/tasks.md` by tooling. Hand-edited progress is a lie with a
  schema.
- **W-11 The index is generated.** `work/index.yaml` and `work/README.md` are
  emitted from the workstream manifests. Editing them by hand is the
  three-views-of-one-fact failure the suite exists to prevent.

## 5. Tasks (normative)

`02_tasks/tasks.md` is a table, because a table is readable by a human at a
glance, diffable in review, and parseable by tooling without a database:

```markdown
| ID | Task | Owner | Status | Evidence |
|---|---|---|---|---|
| T-01 | Draft the migration plan | person:jdoe | done | [plan](../01_plan/plan.md) |
| T-02 | Classify all repositories | agent:migrator | active | — |
```

- **W-12 Stable task IDs.** `T-NN`, unique within the workstream, never
  reused. Cross-workstream references are `NN/T-MM`.
- **W-13 Task status enum:** `todo · active · blocked · done · dropped`.
  Every non-`todo` task names an owner; every `done` task names evidence.

## 6. Agent Coordination (normative)

This is what makes `work/` a working substrate rather than a folder of plans: an
orchestrating agent uses it to delegate to specialists and to prove what happened.

- **W-14 Assignments are explicit.** `08_agents/assignments.md` states, per
  agent: identity, role (`orchestrator` or `sub-agent`), scope as concrete
  paths or task IDs, and its definition of done. An agent with no written scope
  has unbounded scope, which is a defect.
- **W-15 One orchestrator.** A workstream has at most one agent in the
  `orchestrator` role. Sub-agents receive scope from it and report back; they
  do not delegate onward without an assignment entry.
- **W-16 Handoffs are artifacts.** Every transfer of work: agent to agent,
  agent to human: writes
  `08_agents/handoffs/YYYY-MM-DD-from-to-topic.md` containing: what was done,
  what remains, where the artifacts are, known risks, and the next action. A
  handoff that exists only in a chat log did not happen.
- **W-17 Logs are append-only and dated.**
  `08_agents/logs/YYYY-MM-DD-<agent>.md`. Logs are evidence, not narrative:
  what ran, what changed, what failed.
- **W-18 Agent authority is inherited, not invented.** An agent's grants come
  from ADMIN (`admin.yaml`); an assignment narrows scope and never
  widens permission. Agents hold at most `maintainer`, always with an expiry.

## 7. The Generated Site

- **W-19 Derived, never authored.** `atlas site build` renders `work/`
  and `docs/` into a static site. The site is build output: gitignored, rebuilt
  in CI, and never edited. If the site says something the Markdown does not, the
  site is stale.
- **W-20 Style is inherited.** The site consumes the fleet design tokens in
  `assets/design/` (PRESENTATION P-11), so browsing work looks like every other
  surface the organization ships.

## 8. Scaling

Hundreds of concurrent workstreams stay navigable through four mechanisms,
none of which require a database:

1. **Numeric addressing.** `42/T-07` is a globally unique, speakable reference.
2. **Status partitioning.** The dashboard groups by status; `archive/` removes
   terminal work from the active view without losing it.
3. **Declared graphs.** `depends_on` / `blocks` / `relates_to` make the
   dependency structure queryable and renderable, replacing tribal knowledge of
   "who's waiting on whom."
4. **Generated indexes.** Humans read the dashboard; agents read `index.yaml`.
   Neither is maintained by hand, so neither rots.

## 9. Checklist Additions

| ID | Profile | Item |
|---|---|---|
| ☐ WS-01 | Baseline | `work/` exists with a generated `README.md` and `index.yaml` |
| ☐ WS-02 | Baseline | Every workstream has a schema-valid `workstream.yaml` and the complete §3 skeleton |
| ☐ WS-03 | Beta | Index and dashboard regenerate cleanly in CI; no hand-edited drift |
| ☐ WS-04 | Beta | Every `active` workstream has a named owner and at least one task with an owner |
| 🧭 WS-05 | Production | Every `done` workstream carries validation evidence for each acceptance criterion |
| ☐ WS-06 | Production | Declared dependencies resolve to existing workstreams; no cycles |

## 10. Anti-patterns

- **The ghost workstream.** A directory created, never updated, status stuck at
  `active` for months. Status is a claim; stale claims are misinformation.
  Close it or work it.
- **The tracker mirror.** Copying every issue into `02_tasks/`. Workstreams
  track the *initiative's* tasks; tickets stay in the tracker and are linked.
- **Hand-edited indexes.** Editing `work/README.md` because regeneration felt
  slow. The moment the dashboard and the manifests disagree, both become
  unusable.
- **The unbounded agent.** An assignment reading "help with the migration."
  Scope is paths and task IDs, or it is nothing.
- **Renumbering.** Resequencing directories so they "look tidy" invalidates
  every reference, link, and log entry that ever cited them. Numbers are
  addresses (W-I3).
- **Deliverables as transcript dump.** See W-06; a reviewer must find the
  artifact, not excavate it.

---

*WORKSTREAM closes the loop between the standards and the work: PROJECT says
what a repository must be, and `work/` records: auditably, for humans and
agents alike: how it got that way.*
