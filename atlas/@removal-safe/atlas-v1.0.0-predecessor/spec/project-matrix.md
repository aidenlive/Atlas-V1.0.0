---
id: project-matrix
order: 3
title: MATRIX
tagline: "The canonical taxonomy of software projects"
question: "What kind of project is it?"
version: "1.0"
status: stable
rule_prefixes: []
checklist_prefixes: []
companions: [project, project-checklist]
---

# MATRIX: The canonical taxonomy of software projects

---

> You cannot govern what you cannot classify.
> The Matrix gives every project a coordinate, and gives every tool, agent, and policy a handle to grab.

---

## 0. Purpose & Usage

The Matrix defines the controlled vocabulary used by `project.yaml` (project.md §11). Every project is classified along **eight independent dimensions**. Values are closed enumerations: tools validate against them, checklists key off them, and dashboards aggregate over them.

**Format convention:** every dimension below is presented twice: as human-readable prose/tables, and as a machine-digestible enum block. The enum blocks together constitute the schema; a project is Matrix-compliant when every dimension in its manifest uses a listed value.

```yaml
# The eight dimensions, as they appear in project.yaml
type:        # what it IS          (D1)
stage:       # where in its LIFE   (D2)
maturity:    # how TRUSTWORTHY     (D3)
packaging:   # how it SHIPS        (D4)
deployment:  # how it RUNS         (D5)
ownership:   # who ANSWERS for it  (D6)
visibility:  # who may SEE it      (D7)
support:     # what users may EXPECT (D8)
```

**Why independent dimensions instead of one grand hierarchy:** real projects refuse single-axis classification (a CLI can be experimental or critical, public or private, a binary or a container). Orthogonal dimensions mean every combination is expressible and no dimension's change forces reclassification of another: the same reason WORKSPACE separates lifecycle from topic.

---

## D1: Type: What It Is

Types are namespaced `family.kind`. The family determines which PROJECT-CHECKLIST profile applies; the kind refines scaffolding and defaults.

### `app.*`: Applications (software humans use directly)

| Type | Definition | Distinguishing test |
|---|---|---|
| `app.web` | Browser-delivered application | Users hold a URL |
| `app.mobile` | iOS/Android application | Users hold a store listing |
| `app.desktop` | Installed native/hybrid application | Users hold an installer |
| `app.tui` | Interactive terminal application | Users hold a session, not a command |

### `lib.*`: Libraries & Packages (software programs use directly)

| Type | Definition | Distinguishing test |
|---|---|---|
| `lib.package` | Published, importable code | Consumers hold a version constraint |
| `lib.framework` | Package that inverts control (it calls you) | Consumers write plugins/handlers |
| `lib.sdk` | Client library wrapping a specific service/API | Consumers hold API credentials |
| `lib.plugin` | Extension targeting a named host system | Useless without its host |

### `service.*`: Services (software that runs continuously and answers)

| Type | Definition | Distinguishing test |
|---|---|---|
| `service.api` | Network API (REST/GraphQL/gRPC) | Consumers hold an endpoint + contract |
| `service.worker` | Queue/event/schedule-driven processor | No inbound request surface |
| `service.gateway` | Routing/aggregation/edge layer | Its value is in what it fronts |
| `service.mcp` | Agent-facing tool server (MCP or similar) | Consumers are AI agents holding a tool list |

### `tool.*`: Tools (software run on demand, then exits)

| Type | Definition | Distinguishing test |
|---|---|---|
| `tool.cli` | Command-line tool | Users hold a command + flags |
| `tool.action` | CI/CD step or pipeline component | Runs only inside a pipeline |
| `tool.script` | Single-purpose automation, narrow audience | Would not survive a `--help` audit |

### `platform.*`: Foundations (software/config other projects stand on)

| Type | Definition | Distinguishing test |
|---|---|---|
| `platform.infra` | IaC: cloud, network, cluster definitions | `apply` changes the world |
| `platform.design` | Design system: tokens, components, patterns | Consumers are UIs |
| `platform.template` | Scaffold/starter/boilerplate | Its output is other projects |
| `platform.config` | Shared configuration (lint rules, policies, schemas) | Consumed by tools, not imported by code |

### `content.*`: Knowledge artifacts in repo form

| Type | Definition | Distinguishing test |
|---|---|---|
| `content.docs` | Documentation site/corpus as its own project | The prose is the product |
| `content.spec` | Standard, protocol, or schema definition | Implementations cite it |
| `content.data` | Versioned dataset | Consumers hold a download, not an import |
| `content.research` | Experiments, notebooks, papers | Findings are the product; code is evidence |

```yaml
# D1 enum
type:
  app:      [web, mobile, desktop, tui]
  lib:      [package, framework, sdk, plugin]
  service:  [api, worker, gateway, mcp]
  tool:     [cli, action, script]
  platform: [infra, design, template, config]
  content:  [docs, spec, data, research]
# Hybrids declare a primary type plus optional `interfaces: [http-api, cli, sdk, ui, mcp]`
#   classify by center of gravity, enumerate surfaces separately.
```

*Rationale for the family split: families differ in who the consumer is (humans / code / networks / operators / other projects / readers), and consumer identity (not tech stack) is what changes the obligations in PROJECT-CHECKLIST.*

---

## D2: Stage: Where It Is in Life

Defined normatively in project.md §7; the Matrix records the enum and transition matrix.

```yaml
# D2 enum + legal transitions (rightward only)
stage: [idea, incubating, active, maintenance, deprecated, archived]
transitions:
  idea:        [incubating, archived]
  incubating:  [active, archived]
  active:      [maintenance, deprecated]
  maintenance: [active, deprecated]        # re-activation is a declared event
  deprecated:  [archived]
  archived:    []                          # terminal; revival = new project
constraints:
  deprecated: { requires: [successor, sunset_date] }
  archived:   { requires: [forge_archived: true] }
```

---

## D3: Maturity: How Trustworthy It Is

Stage says *where in its life* a project is; maturity says *how much you may lean on it*. They are independent: a young project can be solid; an old one can be fragile.

| Level | Name | Meaning | Objective bar (validated via PROJECT-CHECKLIST) |
|---|---|---|---|
| 0 | `experimental` | May not work; may vanish | Builds |
| 1 | `alpha` | Works for its author | Builds + smoke tests + README quickstart true |
| 2 | `beta` | Works for early adopters; API settling | Test suite + CI + versioned releases |
| 3 | `stable` | Works as documented; breaking changes are semver events | Checklist "Production" profile passes |
| 4 | `hardened` | Trusted for critical paths | Stable + security review + SLOs + on-call/runbook |

```yaml
# D3 enum
maturity: [experimental, alpha, beta, stable, hardened]
# Invariant: maturity may move in either direction, but a downgrade is a
# CHANGELOG event and a README banner: silent downgrades are banned.
```

*Rationale: separating maturity from stage kills the two classic lies: "1.0 therefore reliable" and "0.x therefore excused."*

---

## D4: Packaging: How It Ships

| Value | Artifact | Typical types |
|---|---|---|
| `registry` | Package on npm/PyPI/crates/Maven… | `lib.*` |
| `container` | OCI image | `service.*`, `app.web` |
| `binary` | Compiled executable per platform | `tool.cli`, `app.desktop` |
| `installer` | Store package / signed installer | `app.mobile`, `app.desktop` |
| `bundle` | Static assets (site, docs build) | `app.web`, `content.docs` |
| `source` | Consumed as source (templates, IaC, config) | `platform.*`, `content.*` |
| `none` | Not distributed | `idea` stage, internal scripts |

```yaml
# D4 enum
packaging: [registry, container, binary, installer, bundle, source, none]  # list; multi allowed
```

---

## D5: Deployment: How It Runs

| Value | Meaning | Operational implication |
|---|---|---|
| `none` | Nothing runs (libraries, content, templates) | No runtime obligations |
| `client` | Runs on the user's device | Update channel + crash reporting matter |
| `serverless` | Functions/edge; provider-managed runtime | Cold starts, provider limits |
| `managed.paas` | Platform-managed app hosting | Config via platform |
| `managed.k8s` | Org-run orchestration | Manifests in `ops/`, runbook required |
| `selfhosted` | Users deploy it themselves | Install docs are a product surface |
| `embedded` | Runs inside a host product/device | Host's lifecycle dominates |

```yaml
# D5 enum
deployment: [none, client, serverless, managed.paas, managed.k8s, selfhosted, embedded]
```

*Rationale: deployment model (not type) determines the operational half of PROJECT-CHECKLIST (runbooks, observability, rollback). A `service.api` that is `selfhosted` owes documentation where a `managed.k8s` one owes SLOs.*

---

## D6: Ownership: Who Answers for It

| Value | Meaning | Rule |
|---|---|---|
| `team:<name>` | A named team owns it | Default for org work |
| `person:<handle>` | A named individual owns it | Personal & small projects |
| `community` | Governed maintainer group (public OSS) | Requires GOVERNANCE.md |
| `unowned` | **A defect, not a category.** | Legal only during `deprecated`→`archived` transition, max 90 days |

```yaml
# D6 enum
ownership: { pattern: "team:*|person:*|community|unowned" }
```

*Rationale: making `unowned` representable-but-illegal lets dashboards surface the fleet's real orphans instead of letting them hide behind a stale team name.*

---

## D7: Visibility: Who May See It

| Value | Meaning |
|---|---|
| `public` | World-readable; license and conduct obligations apply |
| `internal` | Org-readable |
| `restricted` | Named-principals only (compliance, secrets-adjacent, embargoed) |
| `private` | Owner only (personal work) |

```yaml
# D7 enum
visibility: [public, internal, restricted, private]
# Invariant: visibility may widen only via a declared release event (it is a
# one-way door in the other direction: narrowing after exposure is mitigation, not undo).
```

---

## D8: Support: What Users May Expect

| Value | Meaning |
|---|---|
| `none` | As-is; issues may never be read |
| `best-effort` | Issues read; no timing promises |
| `business-hours` | Triage within N business days; security fixes prioritized |
| `sla` | Contractual response/uptime targets; on-call exists |

```yaml
# D8 enum
support: [none, best-effort, business-hours, sla]
# Invariant: support ≥ business-hours requires maturity ≥ stable and stage ∈ {active, maintenance}.
```

---

## Cross-Dimension Rules (the Matrix's grammar)

Classifications are constrained, not free-form: these rules are CI-validatable from the manifest alone:

```yaml
rules:
  - id: deprecated-needs-successor
    when: { stage: deprecated }
    require: [successor, sunset_date]
  - id: shipped-needs-license
    when: { visibility: public, packaging: "!none" }
    require: [license]
  - id: running-needs-runbook
    when: { deployment: [managed.paas, managed.k8s, serverless] }
    require: [links.runbook]
  - id: sla-needs-hardening
    when: { support: sla }
    require: { maturity: hardened, ownership: "!unowned" }
  - id: stable-claims-are-checked
    when: { maturity: [stable, hardened] }
    require: [checklist.production: pass]
  - id: archived-is-terminal
    when: { stage: archived }
    forbid: [releases, deployments]
```

---

## Worked Examples

```yaml
# A public Python package
type: lib.package        stage: active       maturity: stable
packaging: [registry]    deployment: none    ownership: person:jdoe
visibility: public       support: best-effort

# An internal payments API
type: service.api        stage: active       maturity: hardened
packaging: [container]   deployment: managed.k8s   ownership: team-payments
visibility: internal     support: sla

# A weekend experiment
type: content.research   stage: incubating   maturity: experimental
packaging: [none]        deployment: none    ownership: person:jdoe
visibility: private      support: none

# The design system
type: platform.design    stage: active       maturity: beta
packaging: [registry, bundle]  deployment: none  ownership: team-design
visibility: internal     support: business-hours
```

---

## Extension Policy

New enum values enter the Matrix only via a versioned revision of this document (the Matrix is itself a `content.spec` project and obeys project.md). Local extensions use an `x-` prefix (`type: x-firmware.rtos`) so validators can distinguish "not yet standard" from "typo": the same seam HTTP headers and vendor CSS properties use, because it works.

---

*The Matrix is the shared coordinate system beneath project.md's structure and project-checklist.md's gates. Classify honestly; everything downstream depends on it.*
