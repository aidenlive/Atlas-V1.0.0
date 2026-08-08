# 0005: Work lives in the repository, not only in the tracker

Date: 2026-08-07 · Status: Accepted

## Context
Issue trackers handle tickets well: small, fungible units with a state machine,
notifications, and an owner. They handle *initiatives* poorly: the multi-week
efforts that carry a plan, a rationale, accumulated evidence, several agents,
and a handoff trail. That material ends up scattered across tickets, documents,
and chat threads, none of which is versioned with the code it changed. Agents
suffer worst: reconstructing context costs them an API token and a guess.

## Decision
Every initiative is a workstream directory under `work/`, with a fixed
nine-section skeleton and a schema-valid manifest (`spec/workstream.md`).
Markdown is canonical; the dashboard (`work/README.md`), the machine index
(`work/index.yaml`), and the static site are all generated. Tickets stay in the
tracker and are linked: `work/` tracks the initiative, not its tickets.

## Consequences
The plan and the artifact land in the same commit, so a diff shows how the
thinking moved. Agents get one entry point (`index.yaml`) and one place to
write handoffs and evidence. The cost is a discipline: workstreams that are not
maintained become stale claims, which is why status, progress, and evidence are
all validated rather than trusted: `work.py validate` runs in CI, and a `done`
without evidence fails the build.
