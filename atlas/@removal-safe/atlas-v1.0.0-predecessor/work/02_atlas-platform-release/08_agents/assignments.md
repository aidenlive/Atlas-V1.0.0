# Agent assignments: 02 Rebrand to Atlas and ship a first-class CLI

| Agent | Role | Scope | Constraints |
|---|---|---|---|
| `agent:builder` | orchestrator | Package the tooling under `src/atlas/`, build the CLI, rebuild the site generator, and carry out the rename | May not alter normative text in `spec/`. May not renumber rule identifiers. Must leave `atlas check` green at each milestone. |

At most one orchestrator (W-15). Handoffs go in
[`handoffs/`](handoffs/); run logs in [`logs/`](logs/). A handoff that exists
only in a chat log did not happen (W-16).
