---
id: project-checklist
order: 4
title: CHECKLIST
tagline: "The minimum bar. Quality gates for every project, from first commit to production"
question: "Is it good enough?"
version: "1.0"
status: stable
rule_prefixes: []
checklist_prefixes: [AX-, BD-, CI-, CL-, DC-, GA-, GD-, GX-, HD-, ID-, OPS-, QG-, RL-, SEC-, ST-, TS-]
companions: [project, project-matrix]
---

# CHECKLIST: Quality gates for every project, from first commit to production

---

> A checklist is a promise made checkable.
> "Production-ready" is not a feeling; it is this document returning green.

---

## 0. How to Use This Document

- **Profiles, not one bar.** Requirements accumulate across four profiles keyed to Matrix maturity: **Baseline** (every repo), **Beta**, **Production** (`stable`), **Hardened**. A project claims a maturity level by passing that profile; PROJECT-MATRIX rule `stable-claims-are-checked` makes the claim CI-enforced.
- **Applicability is Matrix-driven.** Items tagged `[type]`, `[deploy]`, or `[vis]` apply only when the manifest matches: a library skips runbooks; a private script skips licensing ceremony. *Rationale: a checklist that demands irrelevant work gets ignored wholesale; conditional gates keep every item defensible.*
- **Machine-digestible.** Each item has a stable ID (`SEC-03`) so tooling can report per-item pass/fail and manifests can record waivers: `waivers: [{id: OPS-04, reason: "...", until: 2026-12-31, approver: team-lead}]`. Waivers expire; expired waivers are failures.
- ☐ items are checked by CI where mechanically possible; 🧭 items require human judgment and a reviewer's sign-off recorded in the PR.

---

## Profile 1: BASELINE (every repository, from `incubating` onward)

*The bar for existing at all. If this fails, the repo isn't a project yet; it's a directory.*

### Identity & Docs
- ☐ **ID-01** `README.md` present and follows the project.md §8 skeleton (name, one-liner, badges, what/why, quickstart, docs links, status)
- ☐ **ID-02** `project.yaml` present, schema-valid, all eight Matrix dimensions classified
- ☐ **ID-03** `LICENSE` present `[vis: public]`, or explicit `visibility: internal/private` in manifest (unlicensed public code is unusable code)
- ☐ **ID-04** `AGENTS.md` present with all seven sections (purpose, map, commands, conventions, constraints, definition of done, pointers)
- ☐ **ID-05** Vendor agent files (`CLAUDE.md`, `GEMINI.md`, …) are ≤3-line stubs pointing to `AGENTS.md`
- ☐ **ID-06** `CHANGELOG.md` present, Keep-a-Changelog format, `Unreleased` section exists
- 🧭 **ID-07** README quickstart is *actually true*: a stranger (or agent) on a clean machine reaches first success by copy-paste alone

### Structure & Hygiene
- ☐ **ST-01** Root is the project.md §9 closed set: no stray files, no graveyard directories (`legacy/`, `old/`, `@removal-safe/`…)
- ☐ **ST-02** `.gitignore` covers build output, dependency dirs, env files; no generated artifacts committed unmarked
- ☐ **ST-03** No secrets in history or tree (secret-scanning enabled; verified clean)
- ☐ **ST-04** All shipped code under a single source root (`src/` or ecosystem idiom); tests under `tests/` mirroring it
- ☐ **ST-05** Default branch protected `[ownership: team|community]`; force-push disabled

### Build & Run
- ☐ **BD-01** One-command build/install documented in `AGENTS.md` §3 and true
- ☐ **BD-02** Toolchain versions pinned (lockfile, `.tool-versions`, or container): "works on my machine" is a pinning failure
- ☐ **BD-03** Repo builds clean from fresh clone in CI

---

## Profile 2: BETA (claiming `maturity: beta`)

*The bar for asking strangers to try it.*

### Testing
- ☐ **TS-01** Automated test suite exists and runs in CI on every PR
- ☐ **TS-02** Tests cover the quickstart path and every documented public behavior (the docs are the test spec)
- ☐ **TS-03** Coverage measured and reported; ratchet configured (may not decrease): *a ratchet beats a threshold: thresholds invite gaming to a number; ratchets only demand non-regression*
- ☐ **TS-04** `examples/` runnable and executed in CI `[type: lib.*, tool.*, service.mcp]`

### CI/CD
- ☐ **CI-01** CI on every PR: build + tests + linter + formatter check
- ☐ **CI-02** Standard-compliance job: manifest schema, root closed-set, README skeleton, stub integrity (the project.md enforcement arm)
- ☐ **CI-03** CI is green on the default branch *now* (a red main is an outage of trust)
- ☐ **CI-04** Conventional Commits enforced (commit-lint): changelog and semver derive from them

### Releases & Versioning
- ☐ **RL-01** Versioned releases exist; tags `vX.Y.Z`; SemVer (or declared CalVer) honored
- ☐ **RL-02** Release process is scripted or documented step-by-step in `CONTRIBUTING.md`
- ☐ **RL-03** `CHANGELOG.md` updated per release; release notes derive from it
- ☐ **RL-04** Artifacts built from tags in CI, not from laptops `[packaging: ≠ none]`

### Documentation
- ☐ **DC-01** `docs/` structured per project.md §9 (architecture / decisions / guides / reference, as applicable)
- ☐ **DC-02** At least one ADR exists in `docs/decisions/` (the practice must be alive, not aspirational)
- ☐ **DC-03** Public API/CLI/config surface documented `[type: lib.*, tool.cli, service.api]`: generated from source where possible
- 🧭 **DC-04** A newcomer can answer "what is this, how do I use it, how do I change it" from the repo alone: no tribal supplements

---

## Profile 3: PRODUCTION (claiming `maturity: stable`)

*The bar for other people depending on you.*

### Security
- ☐ **SEC-01** Dependency vulnerability scanning in CI; no known-critical vulns unwaivered
- ☐ **SEC-02** Automated dependency update flow (bot PRs) enabled and not rotting (open update PRs < 30 days old)
- ☐ **SEC-03** `SECURITY.md` with disclosure channel `[vis: public]`
- ☐ **SEC-04** Static analysis / SAST appropriate to the stack in CI
- ☐ **SEC-05** Least-privilege CI: scoped tokens, no long-lived credentials in workflows; provenance/signing for artifacts `[packaging: registry|container|binary]`
- 🧭 **SEC-06** Threat model sketch exists in `docs/architecture/` `[type: service.*, app.*]`: one page: assets, trust boundaries, top abuse cases

### Quality Gates
- ☐ **QG-01** Linter + formatter enforced (not advisory): style debate ended by tooling
- ☐ **QG-02** Type checking enforced where the ecosystem supports it
- ☐ **QG-03** Review required for every change; `CODEOWNERS` routes it; no self-merge `[ownership: team|community]`
- ☐ **QG-04** Breaking changes gated: semver-major + migration notes in changelog + deprecation window for prior API `[type: lib.*, service.api]`

### Operations `[deploy: ≠ none]`
- ☐ **OPS-01** Deployment fully described as code in `ops/`; no console-click deployments
- ☐ **OPS-02** Rollback procedure exists and has been exercised at least once
- ☐ **OPS-03** Health/readiness endpoints or liveness signals `[type: service.*]`
- ☐ **OPS-04** Logs structured; metrics on the golden signals; alerts wired to owners `[deploy: managed.*|serverless]`
- ☐ **OPS-05** `ops/runbook.md` exists: start, stop, deploy, roll back, common failures, escalation
- ☐ **OPS-06** Config via environment/secret manager; zero secrets in repo; sample env documented
- ☐ **OPS-07** Data: backup + restore documented and restore *tested* `[stateful services]`: an untested restore is a rumor

### Compliance & Legal
- ☐ **CL-01** Dependency licenses audited; no incompatible licenses in the shipped artifact `[packaging: ≠ none]`
- ☐ **CL-02** `CODE_OF_CONDUCT.md` present `[vis: public, ownership: community]`
- ☐ **CL-03** Data handling documented if user data touched (what's collected, where it lives, retention) `[type: app.*, service.*]`
- ☐ **CL-04** Support policy declared in manifest matches reality (issue triage actually happens at the declared cadence)

### Accessibility & UX `[type: app.*]`
- ☐ **AX-01** Automated a11y checks in CI for UI surfaces
- 🧭 **AX-02** Keyboard-only and screen-reader pass on primary flows
- ☐ **AX-03** Error states and empty states designed, not defaulted

---

## Profile 4: HARDENED (claiming `maturity: hardened`)

*The bar for critical paths: money, auth, safety, reputation.*

- ☐ **HD-01** SLOs defined and measured; error budget policy written `[type: service.*]`
- ☐ **HD-02** On-call rotation exists with escalation policy; `support: sla` honored in tooling
- ☐ **HD-03** Load/performance tests with recorded baselines; regressions gate release
- ☐ **HD-04** Chaos/failure-mode testing for stated availability claims `[deploy: managed.*]`
- ☐ **HD-05** Independent security review or pentest within the last 12 months; findings tracked to closure
- ☐ **HD-06** Disaster recovery: RTO/RPO declared, DR exercised on a schedule
- ☐ **HD-07** Multi-maintainer bus factor ≥ 2 with review coverage across the whole surface
- 🧭 **HD-08** Post-incident review practice exists with published learnings (blameless, actioned)

---

## Lifecycle Gate Checklists

*Beyond maturity profiles, three transitions get their own ceremony:*

### Gate: `incubating → active`
- ☐ **GA-01** Baseline profile passes
- ☐ **GA-02** First tagged release exists
- ☐ **GA-03** Owner confirmed in manifest and `CODEOWNERS`
- 🧭 **GA-04** Definition of done (AGENTS.md §6) reflects how the team actually works

### Gate: `active/maintenance → deprecated`
- ☐ **GD-01** `successor` and `sunset_date` set in manifest (Matrix rule)
- ☐ **GD-02** README bannered; changelog entry dated
- ☐ **GD-03** Consumers notified via their actual channels (release notes, registry deprecation flag, internal announce)
- ☐ **GD-04** Migration guide to successor published `[if successor ≠ none]`

### Gate: `deprecated → archived`
- ☐ **GX-01** Sunset date reached; final release tagged
- ☐ **GX-02** Repository archived on the forge (read-only, mechanically true)
- ☐ **GX-03** Registry packages marked deprecated with pointer `[packaging: registry]`
- ☐ **GX-04** Running deployments decommissioned; DNS/endpoints retired `[deploy: ≠ none]`

---

## Machine-Digestible Summary

```yaml
# checklist.yaml: profiles as data; CI consumes this
standard: project-checklist/1.0
profiles:
  baseline:   { requires: [], items: [ID-01..ID-07, ST-01..ST-05, BD-01..BD-03] }
  beta:       { requires: [baseline], items: [TS-01..TS-04, CI-01..CI-04, RL-01..RL-04, DC-01..DC-04] }
  production: { requires: [beta], items: [SEC-01..SEC-06, QG-01..QG-04, OPS-01..OPS-07, CL-01..CL-04, AX-01..AX-03] }
  hardened:   { requires: [production], items: [HD-01..HD-08] }
gates:
  to-active:     [GA-01..GA-04]
  to-deprecated: [GD-01..GD-04]
  to-archived:   [GX-01..GX-04]
conditions:     # item applicability keys off project.yaml
  syntax: "[dimension: value|pattern]"
waivers:
  fields: [id, reason, until, approver]
  expiry: hard-fail
```

---

## Anti-patterns of Checklist Use

- **Checkbox theater.** Passing SEC-01 with a scanner nobody reads, or DC-04 with docs nobody tested. The 🧭 items exist precisely because some quality is unfakeable by machine: a reviewer's name goes next to them.
- **The permanent waiver.** Waivers expire by design; renewing one thrice is a decision to change the item or the claim, not to renew again.
- **Retroactive maturity.** Claiming `stable` first and gap-filling later inverts the promise. The claim *is* the checklist result.
- **One bar for everything.** Forcing HD-items on a weekend experiment teaches people the checklist is noise. Profiles and applicability tags are the standard's respect for proportionality: honor them.

---

*Together: project.md says what a repository is, project-matrix.md says what kind it is, and this document says when it is good. Green means done. Nothing else does.*
