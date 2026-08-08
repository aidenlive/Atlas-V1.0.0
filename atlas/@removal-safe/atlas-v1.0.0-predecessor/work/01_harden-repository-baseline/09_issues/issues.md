# Issues, blockers & risks: 01 Harden the repository into a canonical v0.0.1 baseline

A blocker with no owner is a wish. Risks are recorded before they fire, with
the mitigation that would make them survivable.

| ID | Type | Description | Owner | Severity | Status |
|---|---|---|---|---|---|
| I-01 | issue | `workspace.md` and `project.md` each open with eight or nine essay sections before reaching a single rule. The essay is good and load-bearing, but a reader looking up a rule must scroll past 40% of the document to find one. Splitting rationale from rules is a normative-adjacent restructure and needs its own reviewed workstream. | person:maintainer | medium | open |
| I-02 | issue | Rule identifiers use a consistent two-namespace pattern (`P-`/`PR-`, `W-`/`WS-`) that was never written down, and three specifications have no identifiers at all, so their rules cannot be cited or waived. v0.0.1 registers and tests the namespaces rather than renumbering, because renumbering breaks every existing citation. Assigning identifiers to the unnumbered rules is the follow-up. | person:maintainer | medium | open |
| I-03 | risk | Two example manifests carry dates that pass during 2026 (`solo.admin.yaml` grant expiry, `deprecated-tool.project.yaml` sunset). Neither is checked by `validate.py`, which only enforces waiver expiry, so they will quietly become misleading rather than failing. Mitigation: extend expiry checking to grants, or move both to relative dates. | person:maintainer | low | open |
| I-04 | risk | The suite release version (`0.0.1`) and the standard contract version (`project/1.0`) are different things that were previously displayed side by side without explanation. v0.0.1 documents the split in `docs/reference/versioning.md`; the risk is that a future release conflates them again. Mitigation: the versioning note is linked from `CONTRIBUTING.md`. | person:maintainer | low | open |
