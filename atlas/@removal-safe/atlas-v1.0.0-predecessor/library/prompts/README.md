# Prompt Library

**78 reusable request prompts across 14 lifecycle categories**,
governed by [`spec/library.md`](../../spec/library.md) (rules L-01..L-08).

## Usage

Copy any prompt into your AI tool of choice, or hand it to a colleague —
optionally appending specifics ("…for the payments-api repo"). Prompts state
*intent and constraints*; the standards in [`spec/`](../../spec/) carry the how.
Agents can discover the catalog machine-readably via [`index.yaml`](index.yaml).

Prompts for destructive operations (deprecation, offboarding, releases,
deletion) embed plan-before-act gates by design (L-04). Do not strip them.

## Conventions

- Naming: `request-<verb>-<object>.txt`, lowercase kebab-case (L-07).
- One objective, 1–3 sentences, tool-agnostic (L-01..L-03).
- Edits are PRs: review a prompt like you review a convention. If a prompt
  routinely needs local tweaks, fix it here, not in sixty pasted copies.
- CI keeps files and `index.yaml` mutually complete (L-08).

## Catalog

### `workspace/`: Operating the WORKSPACE standard: capture, filing, archiving, integrity.

| Prompt | Objective |
|---|---|
| [`request-audit-workspace.txt`](workspace/request-audit-workspace.txt) | Audit this workspace against spec/workspace |
| [`request-scaffold-workspace.txt`](workspace/request-scaffold-workspace.txt) | Create the canonical WORKSPACE tree (00_inbox through 05_archive plus code/, notes/, assets/, scripts/) idempo |
| [`request-drain-inbox.txt`](workspace/request-drain-inbox.txt) | Triage everything in 00_inbox |
| [`request-archive-project-folder.txt`](workspace/request-archive-project-folder.txt) | Run the archive ceremony for the named project folder |
| [`request-plan-workspace-migration.txt`](workspace/request-plan-workspace-migration.txt) | Plan a migration of my current file mess into WORKSPACE using the four bounded passes (scaffold, declare bankr |
| [`request-verify-archive-integrity.txt`](workspace/request-verify-archive-integrity.txt) | Re-verify every SHA256SUMS manifest in 05_archive/ and report checksum mismatches, unmanifested folders, and a |

### `repository/`: Bringing a repository to PROJECT.md compliance: root, manifest, truth consolidation.

| Prompt | Objective |
|---|---|
| [`request-initialize-project.txt`](repository/request-initialize-project.txt) | Initialize this repository to atlas compliance |
| [`request-classify-project.txt`](repository/request-classify-project.txt) | Classify this project honestly along the eight Matrix dimensions in spec/project-matrix |
| [`request-adopt-standard.txt`](repository/request-adopt-standard.txt) | Run the four-pass adoption from docs/guides/adoption |
| [`request-write-agents-guide.txt`](repository/request-write-agents-guide.txt) | Write or update AGENTS |
| [`request-consolidate-truth.txt`](repository/request-consolidate-truth.txt) | Find every fact stated in more than one place in this repository (setup steps, ownership, versions, convention |
| [`request-close-root.txt`](repository/request-close-root.txt) | Enforce the closed root set |

### `architecture/`: Designing, recording, and reviewing system structure.

| Prompt | Objective |
|---|---|
| [`request-document-architecture.txt`](architecture/request-document-architecture.txt) | Write docs/architecture/ for this system |
| [`request-record-decision.txt`](architecture/request-record-decision.txt) | Record the decision we just made as the next numbered ADR in docs/decisions/ (context, decision, consequences) |
| [`request-draw-system-diagram.txt`](architecture/request-draw-system-diagram.txt) | Produce an architecture diagram of this repository or system as a hand-editable SVG or Mermaid file under docs |
| [`request-review-architecture.txt`](architecture/request-review-architecture.txt) | Review the current architecture against its documentation |
| [`request-threat-model.txt`](architecture/request-threat-model.txt) | Write the one-page threat model sketch required by checklist item SEC-06 |

### `documentation/`: Keeping prose truthful, single-sourced, and structured per docs/ conventions.

| Prompt | Objective |
|---|---|
| [`request-audit-documentation.txt`](documentation/request-audit-documentation.txt) | Audit all documentation for drift |
| [`request-write-readme.txt`](documentation/request-write-readme.txt) | Write or rebuild README |
| [`request-update-changelog.txt`](documentation/request-update-changelog.txt) | Update CHANGELOG |
| [`request-write-guide.txt`](documentation/request-write-guide.txt) | Write a task-oriented guide in docs/guides/ for the named workflow |
| [`request-generate-reference.txt`](documentation/request-generate-reference.txt) | Generate or refresh docs/reference/ for this project's public surface (API, CLI, or config) from the source of |

### `github/`: Forge configuration as declared, reviewable state.

| Prompt | Objective |
|---|---|
| [`request-configure-forge-metadata.txt`](github/request-configure-forge-metadata.txt) | Set this repository's forge metadata from project |
| [`request-setup-branch-protection.txt`](github/request-setup-branch-protection.txt) | Declare branch protection for the default branch in settings-as-code |
| [`request-setup-ci.txt`](github/request-setup-ci.txt) | Create or repair the CI workflow so every PR runs build, tests, lint, the standard-compliance job, and commit- |
| [`request-triage-issues.txt`](github/request-triage-issues.txt) | Triage the open issues per the declared support policy |
| [`request-sync-settings.txt`](github/request-sync-settings.txt) | Detect drift between |

### `administration/`: Authority, duties, access, and succession per ADMIN.

| Prompt | Objective |
|---|---|
| [`request-declare-ownership.txt`](administration/request-declare-ownership.txt) | Write or correct the ownership facts for this project |
| [`request-assign-duties.txt`](administration/request-assign-duties.txt) | Decompose this project's ownership into the six named duties (triage, review, release, security, oncall, renew |
| [`request-review-access.txt`](administration/request-review-access.txt) | Run an access review against org |
| [`request-offboard-principal.txt`](administration/request-offboard-principal.txt) | Execute offboarding for the named principal |
| [`request-provision-agent.txt`](administration/request-provision-agent.txt) | Provision the named AI agent as a first-class principal |
| [`request-plan-succession.txt`](administration/request-plan-succession.txt) | Verify every owner in this org or repository names a live successor, and draft the succession update for any t |

### `quality/`: Gates, maturity claims, tests, and waivers per PROJECT-CHECKLIST.

| Prompt | Objective |
|---|---|
| [`request-run-quality-gates.txt`](quality/request-run-quality-gates.txt) | Evaluate this repository against the checklist profile for its claimed maturity, item by item, honoring applic |
| [`request-raise-maturity.txt`](quality/request-raise-maturity.txt) | Plan the promotion of this project to the next maturity level |
| [`request-add-tests.txt`](quality/request-add-tests.txt) | Add automated tests covering the quickstart path and every documented public behavior — the docs are the test  |
| [`request-fix-coverage-ratchet.txt`](quality/request-fix-coverage-ratchet.txt) | Configure coverage measurement with a ratchet (coverage may not decrease) rather than a fixed threshold, and m |
| [`request-review-waivers.txt`](quality/request-review-waivers.txt) | List every waiver in the fleet's manifests with its reason, approver, and expiry; flag expired ones as failure |

### `security/`: Scanning, credentials, disclosure, and response.

| Prompt | Objective |
|---|---|
| [`request-security-audit.txt`](security/request-security-audit.txt) | Audit this repository against the SEC checklist items |
| [`request-scan-dependencies.txt`](security/request-scan-dependencies.txt) | Run dependency vulnerability and license scanning, waiver-check any known-critical findings, and verify the au |
| [`request-rotate-credentials.txt`](security/request-rotate-credentials.txt) | Enumerate every credential this project or principal touches, verify each is scoped, single-owner, and within  |
| [`request-write-security-policy.txt`](security/request-write-security-policy.txt) | Write SECURITY |
| [`request-respond-to-vulnerability.txt`](security/request-respond-to-vulnerability.txt) | Handle the reported vulnerability end to end |

### `releases/`: Versioning ceremonies: tag is truth.

| Prompt | Objective |
|---|---|
| [`request-prepare-release.txt`](releases/request-prepare-release.txt) | Prepare the next release |
| [`request-cut-release.txt`](releases/request-cut-release.txt) | Execute the release ceremony |
| [`request-write-release-notes.txt`](releases/request-write-release-notes.txt) | Write release notes for the new version derived from CHANGELOG |
| [`request-verify-release.txt`](releases/request-verify-release.txt) | Verify the just-published release as a consumer would |
| [`request-plan-breaking-change.txt`](releases/request-plan-breaking-change.txt) | Plan the proposed breaking change per gate QG-04 |

### `maintenance/`: Fleet health and honest lifecycle transitions.

| Prompt | Objective |
|---|---|
| [`request-audit-fleet-health.txt`](maintenance/request-audit-fleet-health.txt) | Survey every project |
| [`request-deprecate-project.txt`](maintenance/request-deprecate-project.txt) | Execute the deprecation gate for this project |
| [`request-archive-repository.txt`](maintenance/request-archive-repository.txt) | Execute the archival gate |
| [`request-revive-project.txt`](maintenance/request-revive-project.txt) | Revive the named maintenance-mode or archived work as an explicit event |
| [`request-remove-dead-code.txt`](maintenance/request-remove-dead-code.txt) | Find code that is unreachable, unimported, or feature-flagged off permanently, and delete it in one well-label |
| [`request-renew-assets.txt`](maintenance/request-renew-assets.txt) | Inventory every expiring asset this project depends on — domains, certificates, licenses, vendor contracts, to |

### `design/`: Visual identity and README composition per PRESENTATION.

| Prompt | Objective |
|---|---|
| [`request-apply-brand.txt`](design/request-apply-brand.txt) | Apply the fleet visual identity to this repository |
| [`request-create-banner.txt`](design/request-create-banner.txt) | Create a hero banner for this project as a hand-authored SVG in assets/ following the fleet geometry |
| [`request-compose-readme-visuals.txt`](design/request-compose-readme-visuals.txt) | Rework the README's first screen to the P-06 composition |
| [`request-audit-presentation.txt`](design/request-audit-presentation.txt) | Audit this repository against PRESENTATION items PR-01 |

### `agents/`: Operating AI agents as governed principals.

| Prompt | Objective |
|---|---|
| [`request-onboard-agent.txt`](agents/request-onboard-agent.txt) | Onboard yourself to this repository by reading AGENTS |
| [`request-define-agent-constraints.txt`](agents/request-define-agent-constraints.txt) | Write or tighten the Constraints section of AGENTS |
| [`request-verify-agent-compliance.txt`](agents/request-verify-agent-compliance.txt) | Review the recent agent-authored changes in this repository against AGENTS |
| [`request-delegate-task.txt`](agents/request-delegate-task.txt) | Turn the following goal into a well-posed agent task |
| [`request-review-agent-output.txt`](agents/request-review-agent-output.txt) | Review this agent-produced change as a maintainer would |

### `workstreams/`: Running the work management system: workstreams, tasks, agents, verification.

| Prompt | Objective |
|---|---|
| [`request-open-workstream.txt`](workstreams/request-open-workstream.txt) | Open a new workstream for the named initiative |
| [`request-plan-workstream.txt`](workstreams/request-plan-workstream.txt) | Draft this workstream's plan and milestones |
| [`request-update-workstream-status.txt`](workstreams/request-update-workstream-status.txt) | Reconcile this workstream with reality |
| [`request-assign-agents.txt`](workstreams/request-assign-agents.txt) | Write the agent assignments for this workstream |
| [`request-write-handoff.txt`](workstreams/request-write-handoff.txt) | Write the handoff for the work just completed |
| [`request-verify-workstream.txt`](workstreams/request-verify-workstream.txt) | Verify this workstream against its own acceptance criteria |
| [`request-close-workstream.txt`](workstreams/request-close-workstream.txt) | Close this workstream |
| [`request-triage-blockers.txt`](workstreams/request-triage-blockers.txt) | Review every open issue, blocker, and risk across the live workstreams, and report those with no owner, no mit |
| [`request-report-work-status.txt`](workstreams/request-report-work-status.txt) | Produce a status report across all live workstreams |

### `operations/`: Running services: runbooks, observability, failure practice.

| Prompt | Objective |
|---|---|
| [`request-write-runbook.txt`](operations/request-write-runbook.txt) | Write ops/runbook |
| [`request-setup-observability.txt`](operations/request-setup-observability.txt) | Wire structured logging, golden-signal metrics, and alerts routed to the owning duty holders for this deployme |
| [`request-exercise-rollback.txt`](operations/request-exercise-rollback.txt) | Exercise the rollback procedure for this service in a safe environment, record the actual time and steps taken |
| [`request-test-restore.txt`](operations/request-test-restore.txt) | Perform a full backup restore test for this stateful service |
| [`request-handle-incident.txt`](operations/request-handle-incident.txt) | Coordinate the active incident per the runbook |
| [`request-write-postmortem.txt`](operations/request-write-postmortem.txt) | Write the blameless postmortem for the named incident |
