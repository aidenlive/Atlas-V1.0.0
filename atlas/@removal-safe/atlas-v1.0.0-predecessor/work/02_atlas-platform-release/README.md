# 02: Rebrand to Atlas and ship a first-class CLI

**Status:** done · **Owner:** `person:maintainer` · **Closed:** 2026-08-07
· **Depends on:** [`01`](../01_harden-repository-baseline/)

Workstream 01 made the repository agree with itself. This one makes it usable by
someone who has not read `scripts/`.

The suite was correct and close to unoperable: seven programs in `scripts/`, each
with its own invocation style, none importable, none individually testable, and
discoverable only by listing a directory. This workstream renames the suite to
**Atlas** and turns that drawer of scripts into a packaged library with a
first-class CLI on top.

The eight specifications are **unchanged**. Nothing in `spec/` moved, no rule was
added or renumbered, and every manifest already declaring `standard: project/1.0`
remains valid. The contract held; only the tooling changed.

## Sections

| | |
|---|---|
| [`01_plan/`](01_plan/) | The approach and its milestones |
| [`02_tasks/`](02_tasks/) | The canonical tracker |
| [`03_requirements/`](03_requirements/) | What had to be true to close |
| [`04_decisions/`](04_decisions/) | Decisions taken inside this workstream |
| [`05_research/`](05_research/) | The audit that set the scope |
| [`06_deliverables/`](06_deliverables/) | What shipped |
| [`07_validation/`](07_validation/) | Evidence against each criterion |
| [`08_agents/`](08_agents/) | Assignments, handoffs, logs |
| [`09_issues/`](09_issues/) | Issues, blockers, risks |
