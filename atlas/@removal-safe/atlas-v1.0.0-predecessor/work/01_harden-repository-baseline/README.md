# 01: Harden the repository into a canonical v0.0.1 baseline

| | |
|---|---|
| **Status** | `done` |
| **Owner** | `person:maintainer` |
| **Opened** | 2026-08-07 |
| **Manifest** | [`workstream.yaml`](workstream.yaml) |
| **Dashboard** | [`../README.md`](../README.md) |

## Objective

Turn a working but accreted draft into the repository every other repository in
the organization will be copied from. The draft passed its own tests, so the
problem was never correctness. It was that the same fact lived in several
places at once, several of those copies disagreed, and nothing failed when they
did. This workstream gives every fact one home, makes the copies generated
rather than typed, and writes down the conventions that were previously only
inferable by reading everything.

## Scope

**In scope**

- Repository architecture, folder structure, and naming conventions
- Consolidating duplicated sources of truth and correcting factual drift
- Documentation and information architecture, including a route in for readers
  who are not engineers
- Configuration, developer experience, and the enforcement chain
- Relocating stale, duplicate, and experimental material to `@removal-safe`

**Out of scope**

- Rewriting the normative bodies of the eight specifications. Two of them mix a
  long philosophical essay with the rules it motivates, which is a real
  information-architecture problem, but restructuring 50 KB of normative prose
  is a reviewed change, not an audit side effect. Recorded as
  [`09_issues/issues.md`](09_issues/issues.md) I-01.
- Renumbering rule identifiers. See I-02.
- Anything requiring credentials, a live forge, or a deployed site.

## Definition of done

This workstream is `done` when every acceptance criterion in
[`07_validation/criteria.md`](07_validation/criteria.md) has recorded evidence.

## Sections

| | Contents |
|---|---|
| [`01_plan/`](01_plan/) | Approach and milestones |
| [`02_tasks/`](02_tasks/) | The task tracker — canonical progress |
| [`03_requirements/`](03_requirements/) | What must be true, and the sources |
| [`04_decisions/`](04_decisions/) | Decisions scoped to this workstream |
| [`05_research/`](05_research/) | Notes, spikes, findings |
| [`06_deliverables/`](06_deliverables/) | The artifacts produced |
| [`07_validation/`](07_validation/) | Acceptance criteria and evidence |
| [`08_agents/`](08_agents/) | Assignments, handoffs, logs |
| [`09_issues/`](09_issues/) | Open issues, blockers, risks |
