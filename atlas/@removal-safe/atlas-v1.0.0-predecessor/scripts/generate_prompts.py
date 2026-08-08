#!/usr/bin/env python3
"""One-shot generator for the prompt library. Run from repo root."""
import pathlib, textwrap, yaml

ROOT = pathlib.Path(".").resolve()
P = ROOT / "library" / "prompts"

LIB = {
"workspace": {
  "_desc": "Operating the WORKSPACE standard: capture, filing, archiving, integrity.",
  "audit-workspace": "Audit this workspace against spec/workspace.md: report files loitering in the inbox, naming violations, writes inside the archive, duplicate homes, and projects in active/ untouched for 60+ days. Output a prioritized violation list; fix nothing without confirmation.",
  "scaffold-workspace": "Create the canonical WORKSPACE tree (00_inbox through 05_archive plus code/, notes/, assets/, scripts/) idempotently at the given root, with the sentinel README explaining the system in place. Touch nothing that already exists.",
  "drain-inbox": "Triage everything in 00_inbox: propose one canonical home per file using the naming pattern date_what_context_version, flag items older than 7 days, and list anything with no plausible future value for disposal. Move files only after I approve the plan.",
  "archive-project-folder": "Run the archive ceremony for the named project folder: verify or draft its _about.md, normalize names to the standard, write a SHA256SUMS manifest, and move it to 05_archive/<year-ended>/. Refuse to proceed without the _about.md.",
  "plan-workspace-migration": "Plan a migration of my current file mess into WORKSPACE using the four bounded passes (scaffold, declare bankruptcy on history, rehome the last ~90 days, wire the plumbing). Output the plan with time estimates before touching anything.",
  "verify-archive-integrity": "Re-verify every SHA256SUMS manifest in 05_archive/ and report checksum mismatches, unmanifested folders, and any file modified after deposit. The archive is immutable; treat every finding as an incident, not a cleanup task.",
},
"repository": {
  "_desc": "Bringing a repository to PROJECT.md compliance: root, manifest, truth consolidation.",
  "initialize-project": "Initialize this repository to atlas compliance: the required root documents, a schema-valid project.yaml classified along all eight Matrix dimensions, the canonical directory layout, and vendor agent stubs pointing to AGENTS.md. Finish by running the compliance checker and fixing every violation.",
  "classify-project": "Classify this project honestly along the eight Matrix dimensions in spec/project-matrix.md and write or correct project.yaml, validating it against spec/schemas/project.schema.json. Where a classification is arguable, state the alternatives and why you chose.",
  "adopt-standard": "Run the four-pass adoption from docs/guides/adoption.md on this existing repository: manifest first, root cleanup, truth consolidation, then CI enforcement. Work one pass at a time and show me the diff before each commit.",
  "write-agents-guide": "Write or update AGENTS.md with all seven required sections (purpose, map, commands, conventions, constraints, definition of done, pointers), verifying every command is copy-paste true by running it. Reduce any vendor agent files to three-line stubs.",
  "consolidate-truth": "Find every fact stated in more than one place in this repository (setup steps, ownership, versions, conventions), pick the single correct home for each per PROJECT.md, and replace all other copies with links. List each consolidation as fact → home → former locations.",
  "close-root": "Enforce the closed root set: move every unsanctioned root entry into its role directory, delete dead files in one labeled commit with a changelog entry, and update the compliance checker's allow-list only via an ADR if something genuinely new must stay.",
},
"architecture": {
  "_desc": "Designing, recording, and reviewing system structure.",
  "document-architecture": "Write docs/architecture/ for this system: the parts, their relations, the trust boundaries, and the load-bearing design decisions with rationale. Prefer diagrams-as-code; link every decision to its ADR or create the missing one.",
  "record-decision": "Record the decision we just made as the next numbered ADR in docs/decisions/ (context, decision, consequences), immutable once accepted. If it supersedes an earlier ADR, link both directions; never edit the old one.",
  "draw-system-diagram": "Produce an architecture diagram of this repository or system as a hand-editable SVG or Mermaid file under docs/architecture/ or assets/, with meaningful alt text and the fleet's visual style. Show parts and data flow, not implementation trivia.",
  "review-architecture": "Review the current architecture against its documentation: find drift between docs and code, single points of failure, and boundaries that exist in prose but not in the module graph. Report findings with severity; propose the smallest correcting changes.",
  "threat-model": "Write the one-page threat model sketch required by checklist item SEC-06: assets, trust boundaries, and top abuse cases for this system, stored in docs/architecture/. Keep it honest and short enough that it will actually be maintained.",
},
"documentation": {
  "_desc": "Keeping prose truthful, single-sourced, and structured per docs/ conventions.",
  "audit-documentation": "Audit all documentation for drift: run every documented command, follow the quickstart on a clean state, and check each claim against the code. Report lies with their locations; fix only what I approve.",
  "write-readme": "Write or rebuild README.md to the PRESENTATION composition: hero visual, title matching metadata.description, badge row derived from project.yaml, then What & Why, Quickstart, Documentation, Status, and Contributing/License. The quickstart must be copy-paste true.",
  "update-changelog": "Update CHANGELOG.md from the commits since the last release, in Keep-a-Changelog format under Unreleased, written for consumers rather than committers. Flag anything that looks like an undeclared breaking change.",
  "write-guide": "Write a task-oriented guide in docs/guides/ for the named workflow: prerequisites, exact steps, verification, and failure modes. Test every step before writing it down.",
  "generate-reference": "Generate or refresh docs/reference/ for this project's public surface (API, CLI, or config) from the source of truth, and wire the generation into CI so the reference cannot drift from the code.",
},
"github": {
  "_desc": "Forge configuration as declared, reviewable state.",
  "configure-forge-metadata": "Set this repository's forge metadata from project.yaml's metadata block — description, homepage, and topics per PRESENTATION P-01..P-05 — by updating .github/settings.yml, never by hand-editing the forge. Verify manifest and settings agree.",
  "setup-branch-protection": "Declare branch protection for the default branch in settings-as-code: required reviews, required status checks matching the CI job names, no force pushes, and squash-only merges. Explain any rule you relax and why.",
  "setup-ci": "Create or repair the CI workflow so every PR runs build, tests, lint, the standard-compliance job, and commit-lint, with the checks required by branch protection. CI must be green on the default branch before you finish.",
  "triage-issues": "Triage the open issues per the declared support policy: label, deduplicate, close what is stale or out of scope with a reason, and surface anything that is actually a security report or an undeclared breaking change.",
  "sync-settings": "Detect drift between .github/settings.yml, project.yaml metadata, and the live forge configuration, and produce the change set that reconciles them with the manifests as the source of truth. Never resolve drift by editing the manifest to match the console.",
},
"administration": {
  "_desc": "Authority, duties, access, and succession per ADMIN.",
  "declare-ownership": "Write or correct the ownership facts for this project: owner in project.yaml, the duties block and successor in admin.yaml, and CODEOWNERS derived from the review duty. Flag any duty that currently has no real holder as unowned rather than papering over it.",
  "assign-duties": "Decompose this project's ownership into the six named duties (triage, review, release, security, oncall, renewal) with a named holder each, and record them in admin.yaml. Report any duty the current team cannot actually staff.",
  "review-access": "Run an access review against org.yaml and admin.yaml: list every grant, its scope, its last affirmation, and whether the holder still needs it. Apply lapse-to-revoke — anything unaffirmed is proposed for revocation, not renewal.",
  "offboard-principal": "Execute offboarding for the named principal: enumerate their grants for revocation, transfer their duties per the succession declarations, and list every secret they could have held for rotation. Produce the checklist first; act only on approval.",
  "provision-agent": "Provision the named AI agent as a first-class principal: its own identity, scoped grants no higher than maintainer, an expiry or review date, and an entry in the relevant manifests. Never configure it to run on a human's credentials.",
  "plan-succession": "Verify every owner in this org or repository names a live successor, and draft the succession update for any that do not. Treat a departed or unreachable successor as no successor.",
},
"quality": {
  "_desc": "Gates, maturity claims, tests, and waivers per PROJECT-CHECKLIST.",
  "run-quality-gates": "Evaluate this repository against the checklist profile for its claimed maturity, item by item, honoring applicability tags from its manifest. Output per-item pass, fail, or waived status with evidence, and flag any claim the results do not support.",
  "raise-maturity": "Plan the promotion of this project to the next maturity level: list every checklist item newly required, its current status, and the work to close each gap. The claim changes only when the profile passes.",
  "add-tests": "Add automated tests covering the quickstart path and every documented public behavior — the docs are the test spec. Mirror src/ topology under tests/ and wire the suite into CI.",
  "fix-coverage-ratchet": "Configure coverage measurement with a ratchet (coverage may not decrease) rather than a fixed threshold, and make CI fail on regression. Report the current baseline and the least-covered public surfaces.",
  "review-waivers": "List every waiver in the fleet's manifests with its reason, approver, and expiry; flag expired ones as failures and any waiver renewed more than twice as a decision to change the item or the claim. Propose the resolution for each.",
},
"security": {
  "_desc": "Scanning, credentials, disclosure, and response.",
  "security-audit": "Audit this repository against the SEC checklist items: secret scanning, dependency vulnerabilities, SAST, least-privilege CI, and the presence of a real disclosure channel. Report findings by severity with the smallest fix for each.",
  "scan-dependencies": "Run dependency vulnerability and license scanning, waiver-check any known-critical findings, and verify the automated update flow is alive (no bot PRs older than 30 days). Summarize what ships in the artifact versus what is dev-only.",
  "rotate-credentials": "Enumerate every credential this project or principal touches, verify each is scoped, single-owner, and within its TTL, and produce a rotation plan for anything long-lived or shared. A shared credential is a violation with no waiver path.",
  "write-security-policy": "Write SECURITY.md with a private disclosure channel, scope of what counts as a vulnerability here, and an acknowledgement target consistent with the declared support level. No security theater — promise only what the duty holder can honor.",
  "respond-to-vulnerability": "Handle the reported vulnerability end to end: assess severity and affected versions, prepare the fix and advisory, coordinate the release per the disclosure policy, and record the timeline for the postmortem.",
},
"releases": {
  "_desc": "Versioning ceremonies: tag is truth.",
  "prepare-release": "Prepare the next release: derive the version bump from Conventional Commits since the last tag, finalize the changelog section, and verify the release checklist (tests green, docs current, migration notes for anything breaking). Stop before tagging and show me the summary.",
  "cut-release": "Execute the release ceremony: version bump, changelog finalize, annotated tag vX.Y.Z, artifacts built from the tag in CI, and publication. The tag is the single source of truth for what is released; nothing ships from a laptop.",
  "write-release-notes": "Write release notes for the new version derived from CHANGELOG.md, ordered by consumer impact: breaking changes with migration steps first, then features, then fixes. Link the full changelog; invent nothing not in it.",
  "verify-release": "Verify the just-published release as a consumer would: install or pull the artifact from the registry, run the quickstart against it, and confirm version metadata, provenance, and changelog agree. Report any mismatch as a release defect.",
  "plan-breaking-change": "Plan the proposed breaking change per gate QG-04: semver-major impact, migration notes, a deprecation window for the prior surface, and consumer notification through their actual channels. Output the plan and timeline before any code changes.",
},
"maintenance": {
  "_desc": "Fleet health and honest lifecycle transitions.",
  "audit-fleet-health": "Survey every project.yaml in the fleet and report: stage and maturity distribution, unowned or successor-less projects, expired waivers, stale support claims, and repos whose CI is red. Output a ranked list of the ten most urgent interventions.",
  "deprecate-project": "Execute the deprecation gate for this project: set successor and sunset_date in the manifest, banner the README, date the changelog entry, notify consumers via their real channels, and publish the migration guide. Silent deprecation is not an option.",
  "archive-repository": "Execute the archival gate: confirm the sunset date passed, tag the final release, mark registry packages deprecated with a pointer, decommission running deployments, and archive the repository on the forge so the state is mechanically true.",
  "revive-project": "Revive the named maintenance-mode or archived work as an explicit event: for archived code, a new project that copies from history rather than reanimating the old repo; either way, a changelog entry, refreshed manifest, and re-run quality gates before any new release.",
  "remove-dead-code": "Find code that is unreachable, unimported, or feature-flagged off permanently, and delete it in one well-labeled commit with a changelog entry and, for significant removals, a removed/ tag. Git is the archive; create no graveyard directories.",
  "renew-assets": "Inventory every expiring asset this project depends on — domains, certificates, licenses, vendor contracts, tokens — with expiry dates and the renewal duty holder, and flag anything expiring within 90 days or held by no one.",
},
"design": {
  "_desc": "Visual identity and README composition per PRESENTATION.",
  "apply-brand": "Apply the fleet visual identity to this repository: inherit the banner geometry and palette from the standards repo's assets/, adapt the wordmark, and verify the hero renders correctly with meaningful alt text. Do not invent a new brand per P-11.",
  "create-banner": "Create a hero banner for this project as a hand-authored SVG in assets/ following the fleet geometry: dark substrate, accent gradient, wordmark, one-line value proposition. It must degrade gracefully to its alt text.",
  "compose-readme-visuals": "Rework the README's first screen to the P-06 composition: hero visual, title, derived badge row, What & Why, and Quickstart within one default viewport. Move everything else below the fold.",
  "audit-presentation": "Audit this repository against PRESENTATION items PR-01..PR-06: metadata block validity, hero visual with alt text, settings-as-code without drift, derivable badges, first-screen comprehension, and the architecture diagram. Report pass or fail with the fix for each.",
},
"agents": {
  "_desc": "Operating AI agents as governed principals.",
  "onboard-agent": "Onboard yourself to this repository by reading AGENTS.md end to end, confirming each command in its Commands section runs, and restating the constraints and definition of done in your own words before taking any action.",
  "define-agent-constraints": "Write or tighten the Constraints section of AGENTS.md: files never to edit, generated paths, protected branches, secret locations, and destructive commands requiring human confirmation. Every constraint must be specific enough for an agent to obey mechanically.",
  "verify-agent-compliance": "Review the recent agent-authored changes in this repository against AGENTS.md and admin.yaml: constraint violations, edits to generated or frozen paths, actions above the agent's granted role, and commits missing the required conventions. Report violations with evidence.",
  "delegate-task": "Turn the following goal into a well-posed agent task: the objective, the definition of done from AGENTS.md, the relevant constraints, and the verification the agent must run before claiming completion. Ambiguity in the task is a defect in the delegation.",
  "review-agent-output": "Review this agent-produced change as a maintainer would: correctness against the task, compliance with conventions and constraints, test and changelog presence, and any scope the agent silently added or dropped. Approve, request changes, or reject with reasons.",
},
"workstreams": {
  "_desc": "Running the work management system: workstreams, tasks, agents, verification.",
  "open-workstream": "Open a new workstream for the named initiative: scaffold it with the standard skeleton, write the objective, explicit in-and-out scope, and acceptance criteria before any task exists. Criteria written after the work are recollection, not criteria.",
  "plan-workstream": "Draft this workstream's plan and milestones: the phased approach, why it beats the alternatives considered, and the assumptions that are actually unverified facts. Turn each phase into tasks with owners in the task table.",
  "update-workstream-status": "Reconcile this workstream with reality: update task statuses and evidence links, regenerate the index and dashboard, and correct the manifest status if the current one is a stale claim. Never hand-edit generated indexes.",
  "assign-agents": "Write the agent assignments for this workstream: one orchestrator, sub-agents with scope as concrete paths or task IDs, a definition of done each, and an expiry. Report any assignment you cannot scope concretely rather than writing a vague one.",
  "write-handoff": "Write the handoff for the work just completed: what was done, what remains, where the artifacts are, known risks, and the single next action for the receiver. Save it as a dated file in the workstream's handoffs directory.",
  "verify-workstream": "Verify this workstream against its own acceptance criteria: check each one, record how it was checked, by whom, and the result. Report criteria you cannot verify as failures rather than assuming success.",
  "close-workstream": "Close this workstream: confirm every acceptance criterion has recorded evidence, set the terminal status and close date, regenerate the index, and archive the directory intact. Refuse to close it if any criterion lacks evidence.",
  "triage-blockers": "Review every open issue, blocker, and risk across the live workstreams, and report those with no owner, no mitigation, or no movement since they were raised. An unowned blocker is a wish; name who must act on each.",
  "report-work-status": "Produce a status report across all live workstreams: progress against targets, blocked work with its blocker, agent assignments in flight, and the workstreams whose status claims look stale. Lead with what needs a decision.",
},
"operations": {
  "_desc": "Running services: runbooks, observability, failure practice.",
  "write-runbook": "Write ops/runbook.md for this service: start, stop, deploy, roll back, the common failure modes with their remedies, and the escalation path with real duty holders. Every procedure must be executable as written.",
  "setup-observability": "Wire structured logging, golden-signal metrics, and alerts routed to the owning duty holders for this deployment, as code under ops/. An alert with no owner is noise; a metric no alert reads is decoration.",
  "exercise-rollback": "Exercise the rollback procedure for this service in a safe environment, record the actual time and steps taken, and update the runbook where reality diverged from the document. An unexercised rollback is a rumor.",
  "test-restore": "Perform a full backup restore test for this stateful service: restore to an isolated environment, verify data integrity and application function, record duration against the declared RPO/RTO, and file the evidence. An untested restore is a rumor.",
  "handle-incident": "Coordinate the active incident per the runbook: assess impact, engage the on-call duty holder, execute mitigation, and keep an append-only timeline of actions and decisions for the postmortem. Mitigate first; root-cause later.",
  "write-postmortem": "Write the blameless postmortem for the named incident: timeline, impact, contributing causes, what worked, and specific actioned follow-ups with owners and dates. Publish it per HD-08; a postmortem without actioned learnings is theater.",
},
}

index = {"standard": "library/1.0", "categories": []}
for cat, items in LIB.items():
    desc = items.pop("_desc")
    d = P / cat
    d.mkdir(parents=True, exist_ok=True)
    entries = []
    for pid, text in items.items():
        fname = f"request-{pid}.txt"
        (d / fname).write_text(textwrap.fill(text, width=80) + "\n")
        entries.append({"id": pid, "file": f"{cat}/{fname}",
                        "objective": (text.split(":")[0].split(".")[0].strip())[:110]})
    index["categories"].append({"name": cat, "description": desc, "prompts": entries})

(P / "index.yaml").write_text(
    "# library/prompts/index.yaml — machine-readable catalog; tests keep it in sync with files\n"
    + yaml.safe_dump(index, sort_keys=False, width=100)
)
total = sum(len(c["prompts"]) for c in index["categories"])
print(f"generated {total} prompts across {len(index['categories'])} categories")
