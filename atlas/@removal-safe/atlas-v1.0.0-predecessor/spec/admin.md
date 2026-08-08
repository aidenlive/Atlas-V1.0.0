---
id: admin
order: 5
title: ADMIN
tagline: "A universal administrative model for projects and organizations"
question: "Who may act, who answers, who pays?"
version: "1.0"
status: stable
rule_prefixes: [I-, R-]
checklist_prefixes: []
companions: [workspace, project, project-matrix, project-checklist]
---

# ADMIN: A universal administrative model for projects and organizations

---

> Structure without administration is a museum.
> Administration without structure is a bureaucracy.
> This document is the fourth wall of the standard: who may do what, who answers when, and how anyone (human, agent, or auditor) can verify both.

---

## 0. What This Is

WORKSPACE organizes files. PROJECT organizes repositories. The MATRIX classifies them; the CHECKLIST gates them. What remains is the layer every one of those depends on and none of them defines: **authority**. Who owns this? Who may change it? Who is accountable when it breaks, who pays for it, and how do we prove all of that to an auditor, or to an agent deciding whether it is allowed to act?

ADMIN defines that layer as a **platform-neutral model**: a small set of concepts (principals, roles, grants, teams, organizations), two manifests (`admin.yaml`, `org.yaml`), and a set of invariants that hold whether the underlying platform is GitHub, GitLab, a cloud IAM, a NAS, or a folder of documents. Platforms are *implementations* of this model; the model is the truth they are configured from.

The design bet is the same one the whole standard makes: **declared, versioned, machine-readable truth beats configured, scattered, click-created state.** Admin handled in web consoles is admin that cannot be reviewed, diffed, audited, or reasoned about by agents. Admin declared in files can be all four.

---

## Part I: The Philosophy

### 1. Why Administration Decays

Administrative state rots faster than code, through four mechanisms:

1. **Access accretes and never sheds.** People are granted access at the moment of need (loudly) and lose relevance silently. No event fires when someone stops needing access. Without scheduled review, every access list monotonically grows until it means nothing. *Consequence: reviews must be mandatory, calendared, and lapse-to-revoke: access that no one re-affirms expires on its own.*
2. **Authority hides in consoles.** Click-configured permissions live in a hundred admin panels with no history, no diff, no review. Nobody can answer "who can deploy prod?" without a scavenger hunt. *Consequence: authority must be declared in versioned files and pushed to platforms, never hand-set in them.*
3. **Ownership is claimed by teams and exercised by no one.** "The platform team owns it" satisfies the org chart while every actual duty (triage, review, renewal, incident response) goes unassigned. *Consequence: ownership must decompose into named duties with named holders (§7), and `unowned` must be visible, not hidden behind stale labels.*
4. **The exceptional becomes the permanent.** Break-glass access, temporary elevation, "just for this migration" grants: every emergency permission that lacks an expiry date is a standing permission with a misleading name. *Consequence: every grant carries a scope and every elevated grant carries an expiry: non-expiring elevation is a schema violation, not a choice.*

### 2. Why Agents Force the Issue

AI agents make implicit administration untenable, and explicit administration invaluable:

- **Agents are principals.** They hold credentials, open PRs, deploy services, and spend money. A model with no place for non-human principals will govern them by accident: usually with someone's personal token, which is the worst of all worlds (unauditable, over-scoped, tied to an employee's lifecycle).
- **Agents can read policy, but only if policy is data.** An agent cannot infer from tribal memory that prod deploys need two approvals. It can read `admin.yaml` and comply, or better, be *blocked* by CI that reads the same file. Declared policy is simultaneously agent documentation and agent enforcement.
- **Agents scale mistakes.** A human with excess permission makes occasional errors; an agent with excess permission makes them at machine speed. Least privilege stops being hygiene and becomes the load-bearing wall.

The now-familiar corollary: **an organization an agent can safely operate in (clear grants, clear limits, clear escalation) is exactly the organization a new employee can safely operate in.** Agent-governability is legibility, again.

### 3. Why Auditing Is a Design Input, Not an Afterthought

Every administrative question eventually becomes an audit question: *who had access, who approved, who changed it, when.* Systems that treat auditing as a report to assemble later discover that the evidence was never captured. The model therefore requires that **every administrative fact be attributable at the moment it is created**: grants are commits with authors, elevations are logged events with expiries, reviews are dated records with reviewers. Compliance then stops being a quarterly archaeology project and becomes a query over records that already exist. The archive philosophy of WORKSPACE §6 applies verbatim: administrative history is append-only, immutable, and organized by time.

### 4. Why Small Must Not Be Exempt

Most admin frameworks are enterprise cosplay: unusable below fifty people, so solo builders and small teams run on vibes until the day vibes fail (a departure, a dispute, an acquisition, a compromised token). This model scales *down* by design: a solo project's entire `admin.yaml` is five lines, and it still delivers the two things smallness actually needs: a named successor path (bus factor) and scoped agent credentials. The profiles in §13 make the floor proportionate; the *model* never changes shape, so growth is addition, not migration.

---

## Part II: The Model

### 5. Core Concepts

Five nouns, closed set. Everything administrative is expressible in them:

| Concept | Definition | Identified as |
|---|---|---|
| **Principal** | Any actor that can be granted authority: a human, an agent, or a service | `person:<handle>`, `agent:<name>`, `service:<name>` |
| **Role** | A named bundle of capabilities (§6) | `role:<name>` |
| **Grant** | Role × Principal × Scope × (Expiry) — the atomic unit of authority | entry in `admin.yaml` |
| **Team** | A named set of principals with shared grants and a declared charter | `team:<name>` |
| **Organization** | The root of trust: teams, policies, and defaults, declared in `org.yaml` | `org:<name>` |

**Invariants:**

- **I-1: All authority is grants.** No principal has capability except through a declared grant. Platform-side permissions not derivable from the manifests are *drift*, and drift is a CI-detectable defect (§11).
- **I-2: Agents are principals, never people.** An agent never operates on a human's credentials. Every agent has its own identity, its own scoped grants, and its own audit trail. *Rationale: §2: attribution, revocability, and lifecycle independence.*
- **I-3: Grants are scoped.** Every grant names its scope (org, team, project, or environment). Unscoped authority does not exist in the model.
- **I-4: Elevation expires.** Any grant above a scope's default role carries an expiry or a review date. `expires: never` is invalid for elevated roles.
- **I-5: Two-key rule for irreversible acts.** Ownership transfer, org-level policy change, production data deletion, visibility widening, and billing changes above threshold require two distinct human principals. *Rationale: the acts that cannot be rolled back are the acts one compromised account must not accomplish alone.*

### 6. Roles: The Capability Ladder

Roles are a fixed, ordered ladder. Platforms map their native roles onto it; policy is written against it. A closed set, because every custom role is a question auditors and agents can't answer from the standard alone.

| Role | Capabilities (cumulative) | Typical holder |
|---|---|---|
| `observer` | Read code, docs, issues, dashboards | Stakeholders, org members on internal repos |
| `contributor` | Open issues/PRs, comment, run CI | Anyone doing work; **the default working role** |
| `maintainer` | Merge, triage, release, edit docs/settings within the project | The people who answer for the code |
| `admin` | Grant/revoke up to `maintainer`, change project config, manage integrations | Team leads; **scoped to a project or team, never implicit org-wide** |
| `owner` | Transfer, archive, delete, change visibility; accountable for everything below | Exactly the `ownership` value from `project.yaml` |
| `steward` | Org-level: policy, billing, org membership, root credentials | 2–5 named humans per org, no more |

**Rules of the ladder:**

- **R-1:** Default role for any new principal is `contributor` at the narrowest useful scope. Broad-by-default is how §1.1 starts.
- **R-2:** `owner` in this document and `ownership` in `project.yaml` (MATRIX D6) are the same fact: the manifest points here; there is one source of truth for who answers.
- **R-3:** Agents may hold at most `maintainer`, and only with an expiry or review date; agents are never `owner` or `steward`. *Rationale: accountability is a human property. An agent can do the work of a maintainer; it cannot answer for an organization.*
- **R-4:** `steward` count is bounded (≥2 for bus factor, ≤5 for accountability). A twelve-steward org has no stewards.

### 7. Ownership: Decomposed Into Duties

"Owns" is a bundle, and unbundled it goes unexercised (§1.3). The model decomposes ownership into six named duties; each is held by a principal or team, defaulting to the owner but delegable explicitly:

```yaml
# admin.yaml: duties block
duties:
  triage:     team:payments        # issues answered per support policy
  review:     team:payments        # PRs reviewed; CODEOWNERS derives from this
  release:    person:jsmith        # releases cut per project.md §13
  security:   team:security        # vulns triaged, SEC-* checklist items owned
  oncall:     rotation:payments-oncall   # [deploy ≠ none] incidents answered
  renewal:    person:jsmith        # domains, certs, licenses, vendor contracts renewed
```

*Rationale: every production incident post-mortem that ends in "everyone thought someone else was watching it" is a duty that was bundled instead of named. The duties block is also what makes `support:` claims in the manifest checkable: CL-04 verifies a `triage` holder exists and acts.*

**Succession is mandatory:** every `owner` names a successor principal in `admin.yaml`. Untested succession is the administrative version of an untested backup restore (CHECKLIST OPS-07): departure of a single human must never orphan a project. MATRIX's `unowned` state exists to make failures of this rule visible, not survivable.

### 8. Teams & Organizations

**Teams** are the unit of granting (grant to teams, not individuals, wherever possible: individual grants are the long tail that reviews always miss). Every team declares, in `org.yaml`:

- a **charter** (one sentence: what this team answers for),
- a **lead** (a person, accountable for the team's grants and reviews),
- **membership** (principals, including agent members, explicitly),
- **default grants** (what joining this team confers).

**Organizations** are the root of trust. `org.yaml` declares:

```yaml
# org.yaml: the organization manifest (versioned, reviewed, applied)
standard: admin/1.0
org: acme
stewards: [person:ada, person:lin, person:sam]      # 2–5, humans only
teams:
  payments:
    charter: "Owns money movement services and their correctness."
    lead: person:jsmith
    members: [person:jsmith, person:kwu, agent:payments-ci]
    grants:
      - { role: maintainer, scope: "project:invoice-api" }
      - { role: contributor, scope: "org:acme" }
policies:
  default_role: contributor
  default_visibility: internal          # public is a declared event (MATRIX D7)
  review_cadence: quarterly             # access reviews, lapse-to-revoke
  elevation_ttl_max: P30D               # ISO-8601 duration; no eternal elevation
  two_key_acts: [transfer, delete-prod-data, org-policy, widen-visibility, billing-major]
  agent_policy:
    max_role: maintainer
    credential_ttl_max: P90D
    forbidden: [force-push, delete-repo, modify-org-policy, spend-above-limit]
billing:
  owner: person:ada
  cost_centers: { payments: team:payments, platform: team:infra }
compliance:
  frameworks: []                        # e.g. [soc2, gdpr]: activates §12 items
  evidence_dir: governance/evidence/
```

**Where these files live:** in a dedicated `org-admin` repository: itself a PROJECT-compliant repo (`type: platform.config`, `visibility: restricted`): with `admin.yaml` optionally per-project in each repo root for project-scoped grants and duties. Administration is thereby governed by the same standard it governs: changes are PRs, reviews are approvals, history is git, and the two-key rule is branch protection requiring two approvers. **The stack is self-hosting, and that is the proof it works.**

### 9. Administrative Surfaces

Every project and org exposes a fixed set of surfaces (the places where administration is *done*) so that no capability exists off-map:

| Surface | Governs | Truth source |
|---|---|---|
| **Access** | Who holds which role at which scope | `org.yaml` + `admin.yaml` |
| **Policy** | Rules of the road (defaults, TTLs, two-key list) | `org.yaml policies:` |
| **Registry** | What projects exist, their Matrix coordinates | Fleet of `project.yaml` |
| **Audit** | What happened, by whom, when | Append-only log store (§11) |
| **Billing** | Who pays, what it costs, per cost center | `org.yaml billing:` + provider exports |
| **Secrets** | Credentials, tokens, keys | Secret manager only — *referenced* by manifests, never contained |
| **Runtime** | Deploys, incidents, on-call | `ops/` per project.md + rotation tooling |

**Invariant I-6: manifests contain authority, never secrets.** `admin.yaml` says *who may* deploy; the secret manager holds *the key that* deploys. Confusing the two is how declared-admin repos become breach amplifiers.

### 10. Security Administration

- **Least privilege as schema:** the narrowest role and scope that accomplishes the duty, enforced by R-1 defaults and I-3 scoping.
- **Credential hygiene:** all long-lived human credentials require MFA; all agent/service credentials are scoped, rotated within `credential_ttl_max`, and bound to a single principal. Shared credentials are a violation with no waiver path: a shared credential is an audit trail with no author.
- **Break-glass:** a sealed, logged, two-key path to emergency `admin` with automatic expiry ≤ 24h and a mandatory post-use review. Emergencies are real; permanent emergency access is §1.4.
- **Offboarding is an event, not a cleanup:** departure of any principal (human resignation, agent decommission, vendor end) triggers revocation of all grants within one business day, transfer of held duties per succession, and rotation of any secret the principal could have held. *The duties block (§7) is what makes this checklist generatable per-person.*
- **Grant reviews:** every team lead re-affirms their team's grants each `review_cadence`; unaffirmed grants lapse to revoke. This single mechanism is the counterweight to §1.1, and it only works because lapse (not renewal) is the default.

### 11. Auditing & Drift

Two audit obligations, both mechanical:

1. **Event auditing.** Every administrative act (grant, revoke, elevation, break-glass, transfer, policy change) is recorded append-only with actor, act, scope, timestamp, and (for two-key acts) both approvers. Retention follows the archive strategy: immutable, replicated, organized by time (WORKSPACE §17). Because manifests are git-managed, *most of this log is the git history of the org-admin repo*: free, attributed, and immutable.
2. **Drift detection.** A scheduled reconciler compares declared state (manifests) against actual platform state (forge roles, cloud IAM, secret-manager ACLs) and files a violation for every difference in either direction: undeclared access (someone click-granted) or unapplied declaration (the manifest promised, the platform didn't deliver). Drift tolerated is I-1 repealed. This is `audit.sh` (WORKSPACE §15) and CI-02 (CHECKLIST) at the org tier: the standard's third enforcement arm.

### 12. Billing & Compliance

**Billing** follows the ownership graph: every project's cost rolls up through its owner's cost center (declared in `org.yaml`), making "what does team X cost?" a join between the registry and the provider export: a query, not a quarterly negotiation. Spend by agents is attributed to the agent principal and capped by `agent_policy` limits; an agent without a spend ceiling is an unbounded liability with an API key.

**Compliance** is framework-pluggable: declaring `frameworks: [soc2]` in `org.yaml` activates the corresponding evidence requirements, and the evidence *already exists* by construction: access reviews (§10), audit trails (§11), checklist results (PROJECT-CHECKLIST), classification records (`project.yaml`). The `evidence_dir` collects generated attestations per period, archived immutably. The design claim of §3, delivered: compliance is a *view over* the standard, not a parallel process beside it.

### 13. Conformance Profiles

The model scales down (§4) via three profiles, each a strict superset:

| Profile | For | Requires |
|---|---|---|
| **Solo** | One human, any number of agents | `admin.yaml` with: owner, successor, agent principals with scoped+expiring credentials. Five lines that survive a bus. |
| **Team** | 2–50 principals | + `org.yaml` with teams, duties blocks, quarterly reviews, offboarding procedure, break-glass |
| **Organization** | 50+ / regulated | + drift reconciler, cost centers, compliance frameworks, two-key enforcement in tooling, evidence generation |

A project's profile is declared in `admin.yaml` and validated like everything else: in CI, against schema, with waivers that expire.

### 14. Anti-patterns

- **Console-sourced truth.** Any permission that exists only in a web UI is invisible authority. Declare, then apply, never the reverse.
- **The personal-token agent.** An agent on a human's credentials inherits too much, attributes to the wrong actor, and dies with the employee. I-2 exists because this is the single most common real-world violation.
- **Role inflation.** Granting `admin` because `maintainer` was mildly inconvenient once. The ladder is a ratchet only if the ratchet holds.
- **The heroic owner.** One person holding all six duties with no successor is not ownership; it is a single point of failure wearing a title.
- **Review theater.** Quarterly reviews that rubber-stamp every grant. Lapse-to-revoke exists so that *inaction* cleans up; a review process where inaction preserves is upside-down.
- **Custom role sprawl.** Every bespoke role is a fact auditors and agents must learn separately. Six roles express everything; the seventh is the beginning of the end.
- **Secrets in manifests.** I-6. It has happened to everyone once; the standard's job is to make once the total.
- **Compliance as a parallel universe.** A separate compliance spreadsheet duplicating what manifests already declare is §1.2's truth-fragmentation at the org tier, and it will disagree with reality at audit time, which is the worst possible time.

### 15. Relationship to the Suite

| Question | Answered by |
|---|---|
| Where does a file live? | workspace.md |
| What must be true inside a repo? | project.md |
| What kind of project is it? | project-matrix.md |
| Is it good enough? | project-checklist.md |
| **Who may act, who answers, who pays, and how do we prove it?** | **admin.md** |

The seams are explicit: MATRIX D6 `ownership` resolves through §6–7; CHECKLIST items QG-03, CL-04, SEC-05, HD-02/07, and the deprecation/archive gates are *enforced* by grants and duties defined here; WORKSPACE's `04_shared` and archive immutability find their org-scale analogues in team scopes and append-only audit. Five documents, one system: **structure, content, classification, quality, authority.**

### 16. Future Extensions

- **Schema registry**: JSON Schemas for `org.yaml` / `admin.yaml`, shared with validators, reconcilers, and scaffolders.
- **Platform adapters.** Reference reconcilers mapping the role ladder onto GitHub/GitLab/cloud-IAM primitives.
- **Agent attestation.** Signed capability manifests per agent principal, closing the loop with project.md's `AGENTS.md` §5 constraints: what the repo forbids and what the org grants become one verified statement.
- **Delegation chains.** Bounded re-delegation (`admin` granting time-boxed `maintainer`) with full-chain audit.
- **Federated organizations.** Cross-org grants for partnerships and open-source, with each org's stewards as the trust anchors: the org-tier analogue of WORKSPACE's federated roots.

Extensions must preserve the invariants: all authority is grants; agents are principals; grants are scoped; elevation expires; two keys for the irreversible; manifests never hold secrets.

---

## Appendix A: The Standard on One Page

```
1. Five nouns: principal, role, grant, team, organization. Nothing else.
2. All authority is declared in org.yaml / admin.yaml: versioned, reviewed, applied.
3. Six roles, one ladder: observer → contributor → maintainer → admin → owner → steward.
4. Agents are principals: own identity, own credentials, ≤ maintainer, always expiring.
5. Ownership = six named duties + a named successor. Bundled ownership is no ownership.
6. Elevation expires. Reviews lapse-to-revoke. Break-glass logs and self-destructs.
7. Two humans for irreversible acts. Always.
8. Manifests hold authority; secret managers hold secrets. Never swap.
9. Audit = git history of the admin repo + append-only events + drift reconciliation.
10. Billing follows ownership; compliance is a view over records that already exist.
```

---

*ADMIN completes the standard: WORKSPACE for files, PROJECT for repositories, MATRIX for classification, CHECKLIST for quality, ADMIN for authority. Declare everything, review on a clock, let inaction revoke, and hand the auditors a query instead of a quarter.*
