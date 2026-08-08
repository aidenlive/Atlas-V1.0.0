# Running the work management system

Every initiative in this repository lives in [`work/`](../../work/) as a
numbered workstream. This guide is the operating manual;
[`spec/workstream.md`](../../spec/workstream.md) is the rule set.

## Daily loop

```bash
atlas work new <slug> --owner person:you --title "..."
```

Then edit the Markdown: the plan, the tasks, the decisions, the evidence. When
the task table changes, regenerate what is derived from it and check the result:

```bash
atlas work sync
atlas work validate
```

`sync` and `validate` are cheap and idempotent. Run them before every commit
that touches `work/`; CI runs both.

## Opening a workstream well

The scaffold is free; the thinking is not. Before writing tasks:

1. **Objective.** The outcome, written for a reader arriving in six months.
2. **Scope, both halves.** The out-of-scope list is the one that keeps the
   workstream finishable.
3. **Acceptance criteria** in `07_validation/criteria.md`, written *before* the
   work. Criteria written afterward describe what happened, not what was
   required.

Only then decompose into tasks. A workstream whose criteria are "the tasks are
done" has no criteria.

## Tasks

`02_tasks/tasks.md` is the canonical tracker; the dashboard counts its rows.
Keep the table shape: `T-NN` ids, one owner per non-`todo` task, evidence on
every `done`. Progress in the manifest is overwritten by `sync`: editing it
by hand is a lie with a schema behind it.

Tickets stay in the issue tracker and are linked. Do not mirror them here.

## Orchestrating agents

The coordination layer is `08_agents/`:

- **`assignments.md`.** One orchestrator, sub-agents with scope as concrete
  paths or task IDs, a definition of done each, and an expiry. If you cannot
  write the scope concretely, the task is not ready to delegate.
- **`handoffs/`.** One dated file per transfer: what was done, what remains,
  where the artifacts are, known risks, next action. This is what lets a fresh
  agent resume without re-deriving context.
- **`logs/`.** Append-only evidence of what ran and what failed.

Authority comes from `admin.yaml`, never from an assignment. An assignment
narrows scope; it cannot grant permission the principal does not hold.

A useful pattern from workstream 04: **the agent that did the work should not
be the agent that verifies it.** Give the auditor read-only scope and let it
write only inside its own workstream.

## Closing

A workstream reaches `done` when every criterion in `07_validation/criteria.md`
has a row in `evidence.md` naming the check, the checker, the date, and the
result. Then:

```bash
atlas work archive <id>    # refuses unless status is done/cancelled
```

The directory moves to `work/archive/` intact, keeping its number. Numbers are
addresses. Nothing is renumbered, and every prior reference still resolves.

## Scaling past a hundred

Nothing here needs a database. Numeric addressing (`42/T-07`) gives every task
a speakable global reference; the dashboard partitions by status; `archive/`
keeps terminal work out of the active view; and `depends_on` / `blocks` make
the dependency graph queryable and cycle-checked. Both indexes are generated,
so neither rots.

## Reference

| Path | Contents |
|---|---|
| `work/README.md` | generated dashboard — humans start here |
| `work/index.yaml` | generated machine index — agents start here |
| `work/_template/` | the skeleton `work.py new` copies |
| `work/NN_slug/` | one initiative, nine numbered sections |
| `work/archive/` | completed and cancelled workstreams |

Prompts for each operation live in [`library/prompts/workstreams/`](../../library/prompts/workstreams/).
