---
id: project
order: 2
title: PROJECT
tagline: "An open standard for organizing software projects and repositories"
question: "What must be true inside a repository?"
version: "1.0"
status: stable
rule_prefixes: []
checklist_prefixes: []
companions: [workspace, project-matrix, project-checklist, admin, presentation, library]
---

# PROJECT: An open standard for organizing software projects and repositories

---

> A workspace organizes your *files*. A project organizes your *intent*.
> WORKSPACE tells you where a repository lives. PROJECT tells you what must be true inside it.

---

## 0. What This Is

PROJECT is the repository-level companion to WORKSPACE. Where WORKSPACE governs the filesystem *around* code (`~/code/work/`, `~/code/personal/`, …), PROJECT governs the universe *inside* a repository root: its structure, documents, lifecycle, conventions, and governance.

It is opinionated for the same reason WORKSPACE is: a repository is read a thousand times more often than it is designed, by humans who didn't design it and by agents who can't ask. Every convention below exists to make a repository **legible in sixty seconds, operable without a briefing, and maintainable for a decade.**

The standard is deliberately language-agnostic and tool-agnostic. It defines *invariants*, not stacks.

---

## Part I: The Philosophy

### 1. Why Repositories Rot

Repositories decay through the same three forces as filesystems, plus one of their own:

1. **Documentation drifts from code** because they change on different triggers. Code changes when behavior changes; docs change when someone feels guilty. Any standard that relies on discipline to keep them aligned will fail. The fix is structural: fewer documents, each with a single non-overlapping job, each living as close to what it describes as possible.
2. **Truth fragments.** Setup instructions live in the README, the wiki, a Notion page, a Slack pin, and three agents' config files, and disagree. Every additional copy of a fact is a future lie. The fix is a **single source of truth per fact**, with pointers everywhere else.
3. **The root becomes a landfill.** Config files, one-off scripts, screenshots, and abandoned experiments accumulate at the top level because the top level is where lazy filing lands. The fix is a small, *closed* set of permitted root entries: anything else is a violation a linter can catch.
4. **Endings are never declared.** Code is deprecated in conversation but never in the repo. Experiments end but their directories remain, indistinguishable from live code. A repository that cannot express "this is over" forces every reader to carbon-date every file. The fix is explicit lifecycle status: for the project and for its parts.

### 2. Why Agent-First Is Human-First

An AI agent is the harshest possible audit of your repository: it reads only what is written, follows only what is structured, and knows nothing that "everyone knows." A repository an agent can operate correctly (find the docs, build, test, respect constraints) is *by construction* one a new human contributor can operate too. Optimizing for agents isn't a new burden; it is finally taking legibility seriously, with a reader who can't compensate for your gaps.

The practical consequences:

- **Machine-checkable beats humanly-promised.** Conventions live in linters, manifests, and CI, not in tribal memory.
- **One canonical agent guide, many pointers.** Per-vendor config files (`CLAUDE.md`, `GEMINI.md`, `.cursorrules`, …) are compatibility stubs that redirect to one canonical `AGENTS.md`. Vendors multiply; truth must not.
- **Status is data.** "Is this maintained? What stage is it in? Who owns it?" are questions with machine-readable answers (see project-matrix.md), not archaeology.

### 3. Why Git Is the Archive: and In-Repo Graveyards Are Banned

The instinct to create `legacy/`, `old/`, `@removal-safe/`, or `deprecated/` folders comes from a real fear (losing history) aimed at the wrong tool. **Version control already is a perfect, immutable, first-class archive.** Every deleted file remains recoverable, blame-able, and searchable forever.

An in-repo graveyard, by contrast:

- **Poisons search and agents.** Every grep, every embedding, every "find the auth logic" now returns dead code beside live code, and nothing distinguishes them.
- **Rots silently.** Dead code doesn't compile, doesn't test, and doesn't update, but it still *looks* like code.
- **Repeals single-source-of-truth.** Two implementations of the same thing exist; one is a trap.

The standard therefore mandates: **delete dead code in a well-labeled commit; tag the commit if the removal is significant (`removed/feature-x`); record the removal in `CHANGELOG.md`.** History is preserved *better* than any folder could (with context, authorship, and a timestamp) and the working tree stays 100% alive. The only sanctioned "not yet dead" state is an explicit deprecation marker in code plus a dated entry in the changelog, with a removal deadline. (For material that must remain *visible* while superseded (old design docs, prior specs) see `docs/decisions/`: supersession is a decision, and decisions are recorded, not warehoused.)

### 4. Why the Root Is Sacred

The repository root is the repository's face and its API. It is the first (often only) screen a human sees and the first directory an agent lists. Every entry at the root therefore competes for the reader's next decision. A disciplined root answers, in one glance: *what is this, what state is it in, how do I run it, where is everything else.* The standard makes the root a **closed set**: a fixed list of documents and a fixed list of directories, everything else forbidden. Closed sets are what make sixty-second legibility (and mechanical validation) possible.

### 5. Why Structure Must Encode Lifecycle Here Too

WORKSPACE's core insight (organize by what you're *doing*, not what things are *about*) holds inside repositories. Source, tests, docs, tooling, and operations are not topics; they are **roles with different change cadences, different reviewers, and different failure modes**. The canonical layout (§9) separates by role so that a change's blast radius is visible from its path: a diff touching only `docs/` needs different review than one touching `src/`; CI can know that without reading a line.

---

## Part II: The Standard

### 6. Design Principles

1. **Single source of truth per fact.** Every fact (how to build, who owns this, what changed) lives in exactly one file; all other appearances are links. *Rationale: §1.2.*
2. **The root is a closed set.** Only sanctioned files and directories may appear at the top level. *Rationale: §4.*
3. **Lifecycle is explicit and machine-readable.** The project declares its stage, maturity, and ownership in a manifest, not in folklore. *Rationale: §1.4; taxonomy in project-matrix.md.*
4. **Git is the archive.** No graveyard directories. Deletion + changelog + tag is the archival ceremony. *Rationale: §3.*
5. **Docs live at the highest level that stays true.** Repo-wide truth in `docs/`; module truth beside the module; line truth in comments. *Rationale: proximity is the only force that keeps docs honest.*
6. **Agents read one file.** `AGENTS.md` is canonical; vendor files are two-line stubs pointing to it. *Rationale: §2.*
7. **Convention over configuration, configuration over documentation.** If a rule can be enforced by a formatter/linter/CI, it must be: prose is the fallback, not the mechanism.
8. **Boring is portable.** Standard names (`README.md`, `LICENSE`, `src/`, `tests/`) over clever ones, because every tool, forge, and model already understands boring.

### 7. The Project Lifecycle

Every project is in exactly one stage, declared in its manifest (§11) and badge-visible in its README:

```
IDEA ──▶ INCUBATING ──▶ ACTIVE ──▶ MAINTENANCE ──▶ DEPRECATED ──▶ ARCHIVED
```

| Stage | Meaning | Guarantees to users |
|---|---|---|
| `idea` | A README and intent; may not build | None |
| `incubating` | Builds; APIs unstable; seeking shape | None; expect breakage |
| `active` | Developed; releases; issues triaged | Semver honored; security fixes |
| `maintenance` | Feature-frozen; fixes only | Security + critical fixes |
| `deprecated` | Successor named; removal date set | Security fixes until date |
| `archived` | Read-only; repo archived on the forge | None; history preserved |

**Transition rules:** stages move rightward only (a revival is a *new* `active` declaration: an event worth a changelog entry, not a silent edit). Entering `deprecated` **requires** naming a successor (or explicitly "none") and a date. Entering `archived` requires archiving the repository on the forge, making the state mechanically true, not merely claimed. This mirrors WORKSPACE §10: rightward-only movement is what makes each stage's guarantees trustworthy.

### 8. Root Documents (the closed set, part 1)

Required in every repository past `idea` stage:

| File | Single job | Notes |
|---|---|---|
| `README.md` | Orient a stranger in 60 seconds | See required skeleton below |
| `LICENSE` | Legal terms | No license = not shippable (see PROJECT-CHECKLIST) |
| `CHANGELOG.md` | What changed, when, for whom | Keep-a-Changelog format; release notes derive from it |
| `AGENTS.md` | Everything an agent needs to operate | Canonical; §12 |
| `CONTRIBUTING.md` | How change happens here | Required once a second contributor is possible |
| `project.yaml` | Machine-readable classification & status | §11; the manifest |

Conditionally required:

| File | When |
|---|---|
| `SECURITY.md` | Anything deployed or published |
| `CODE_OF_CONDUCT.md` | Public + community-accepting |
| `ROADMAP.md` | Only if maintained; a stale roadmap is worse than none — if you won't update it quarterly, put direction in the README's "Status" line instead |
| `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, … | One stub per agent tool actually used; each ≤ 3 lines, pointing to `AGENTS.md` |

**Explicitly rejected:** `INFO.md` and per-effort `XYZ-STATUS.md` files. Both duplicate truth that already has a home: the snapshot belongs in `README.md` + `project.yaml`; active-effort status belongs in the issue tracker, where it has an owner, a state machine, and notifications. Status files in the repo root are graveyards-in-waiting (§1.1): they rot the moment attention moves on, and a rotten status file is misinformation with authority.

**README required skeleton** (order fixed; sections may be short but not absent):

```
# Name: one-line value proposition
[badges: stage, CI, version, license]
Hero: screenshot / diagram / demo link   (for anything with a surface)
## What & Why        (3 sentences max)
## Quickstart        (copy-paste path to first success)
## Documentation     (links into docs/)
## Status            (stage, maturity, support policy: mirrors project.yaml)
## Contributing / License (links)
```

*Rationale: a fixed skeleton makes READMEs skimmable across an entire org, and lets tooling verify presence of each section.*

### 9. Canonical Directory Hierarchy (the closed set, part 2)

```
repo/
├── README.md  LICENSE  CHANGELOG.md  AGENTS.md  CONTRIBUTING.md  project.yaml
├── CLAUDE.md  GEMINI.md              ← stubs → AGENTS.md
├── src/            ← the product. all shipped code. one importable root.
├── tests/          ← all automated tests, mirroring src/ topology
├── docs/           ← prose truth (see below)
├── work/           ← initiatives as numbered workstreams (see workstream.md)
├── examples/       ← runnable, CI-verified usage samples
├── scripts/        ← dev & maintenance automation (not shipped)
├── ops/            ← deployment: Dockerfiles, IaC, manifests, pipelines-as-code
├── assets/         ← images, fonts, brand, fixtures too large/binary for src
├── library/prompts/        ← reusable request prompts (see library.md)
├── .github/        ← (or forge equivalent) CI workflows, templates, CODEOWNERS
└── [tool dotfiles] ← formatter/linter/build configs; dotfiles only
```

```
docs/
├── architecture/   ← system design; diagrams as code where possible
├── decisions/      ← ADRs: dated, numbered, immutable once accepted
├── guides/         ← task-oriented how-tos (install, deploy, migrate)
├── reference/      ← API/CLI/SDK reference (generated where possible)
└── assets/         ← images used by docs
```

**Rationale for the load-bearing choices:**

- **One `src/` root** (or the language's idiomatic equivalent: `lib/`, `app/`, a crate root): agents and humans alike get one answer to "where is the code?" Multi-package monorepos use `packages/<name>/`, where each package is itself PROJECT-shaped: the standard is fractal, like WORKSPACE §20's namespaced spaces.
- **`tests/` mirrors `src/`** so that the test for any file is at a *computable* path, which turns "is this covered?" into a script.
- **`docs/decisions/` (ADRs) is the repository's archive of thought.** Decisions are append-only and dated, like WORKSPACE's `05_archive`: you never edit an accepted ADR; you supersede it with a new one that links back. This is where "why is it like this?" goes to be answered forever, and where superseded designs remain visible without haunting the working tree (§3).
- **`ops/` separates run-the-thing from build-the-thing.** Deployment changes different from feature changes: different reviewers, different risk, different secrets exposure. Path-level separation makes that reviewable and CI-routable.
- **`examples/` is CI-verified** or it is deleted. An example that doesn't run is documentation that lies with confidence.
- **`work/` and `library/prompts/` are conditional roots.** They appear when the repository uses the companion standard that defines them (workstream.md, library.md) and are absent otherwise. Conditional does not mean optional in shape: where present, their internal structure is fully specified by that standard, not improvised per repository.
- **Anything not on this list is a root violation.** New needs go *inside* an existing role directory or trigger a deliberate standard revision, never an ad-hoc root entry.

### 10. Naming Rules

Inherit WORKSPACE §12, plus repository specifics:

1. **Repository names:** `lowercase-hyphenated`, noun-first, unprefixed by org name (the forge namespaces already). `invoice-api`, not `AcmeInvoiceAPI2`.
2. **Directories:** lowercase, plural for collections (`tests/`, `docs/`, `scripts/`), singular for roles (`src/`, `ops/`).
3. **Source files:** follow the language's idiom absolutely (`snake_case.py`, `kebab-case.ts` or camel per ecosystem, `PascalCase.cs`). *The standard defers to language idiom inside `src/` because fighting an ecosystem is a decade of paper cuts.*
4. **Docs:** `kebab-case.md`; ADRs as `NNNN-short-title.md` (`0007-switch-to-postgres.md`) so they sort by decision order.
5. **Branches:** `type/short-description` (`feat/webhook-retries`, `fix/tz-offset`). **Commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:` …). *Rationale: both are free machine-readable metadata: changelogs, semver bumps, and CI routing derive from them mechanically.*
6. **Versions:** SemVer for anything with consumers; CalVer permitted for continuously-deployed end-user apps. Tags are `vX.Y.Z`.

### 11. The Manifest: `project.yaml`

The manifest is the repository's classification record: one small, schema-validated YAML file that makes every PROJECT-MATRIX dimension (type, stage, maturity, ownership, visibility, deployment, support) machine-readable at a fixed path.

```yaml
# project.yaml: validated in CI against the PROJECT-MATRIX schema
standard: project/1.0
name: invoice-api
type: service.api            # PROJECT-MATRIX taxonomy
stage: active                # lifecycle (§7)
maturity: stable             # PROJECT-MATRIX maturity ladder
owner: team-payments         # a team or human, never "everyone"
visibility: internal         # public | internal | private
deployment: managed.k8s      # PROJECT-MATRIX deployment models
language: [python]
interfaces: [http-api, cli]
support: business-hours
successor: null              # required non-null when stage: deprecated
links:
  docs: ./docs/
  runbook: ./ops/runbook.md
  tracker: https://…
```

*Rationale: every question a platform team, dependency auditor, or fleet-managing agent asks across a hundred repos ("which services are deprecated? who owns this? what's public?") becomes a `yq` one-liner instead of a survey. The manifest is to a repo what numeric prefixes are to WORKSPACE: the API of the standard.* README badges and the Status section are *rendered from* the manifest, never hand-maintained: one truth, many views.

### 12. AGENTS.md: the Canonical Agent Guide

One file, at the root, containing everything an autonomous system needs:

```
# AGENTS.md required contents (fixed order)
1. Purpose: what this project is, in agent-usable terms
2. Map: annotated directory layout (what lives where, what's generated)
3. Commands: exact build / test / lint / run commands (copy-paste true)
4. Conventions: style, commit format, branch rules, review flow
5. Constraints: what agents must NOT do (files not to edit, generated
                    directories, secrets locations, protected branches,
                    destructive commands requiring human confirmation)
6. Definition of Done: what "complete" means here (tests pass, lint clean,
                    changelog entry, docs updated)
7. Pointers: links to docs/, ADRs, runbook
```

**Vendor stubs** (`CLAUDE.md`, `GEMINI.md`, `.cursorrules`, and whatever ships next quarter) contain exactly:

```md
# Claude
Read AGENTS.md. It is the canonical guide for all agents in this repository.
```

*Rationale: agent tooling is the fastest-churning layer in the stack. Stubs absorb the churn; the canonical file absorbs the truth. Configuration drift between agent files is the modern version of the wiki/README split (§1.2), and it is eliminated the same way: by demoting every copy but one to a pointer.*

### 13. Governance & Workflow

- **Every repo has an owner.** A named team or person in `project.yaml` and enforced via `CODEOWNERS`. "Everyone's" repositories are no one's, and unowned code is the enterprise version of the Desktop-as-workspace.
- **Change flows through review** for anything past `incubating`: branch → PR → CI green → review → squash/merge. Direct pushes to the default branch are disabled by branch protection: the rule is mechanical, not cultural (§6.7).
- **CI is the standard's enforcement arm.** Formatting, linting, tests, manifest validation, README skeleton check, root-closed-set check, and stub-integrity check all run on every PR. A convention that CI doesn't check is a suggestion; this document defines almost nothing that must remain a suggestion.
- **Releases are ceremonies, not accidents:** version bump + changelog finalize + tag + build from tag + publish, ideally as one scripted/automated pipeline triggered by the tag. The tag is the single source of truth for "what is released."
- **Deprecation is loud:** manifest updated, README bannered, changelog dated, successor named, consumers notified. Silent deprecation is the repository-level version of editing the archive.

### 14. Relationship to WORKSPACE

| WORKSPACE concept | PROJECT equivalent |
|---|---|
| `00_inbox` (capture, drained) | Issues/branches (triaged, merged or closed) |
| Active spaces `01–04` | `stage: incubating/active/maintenance` |
| `05_archive` (immutable, by time) | Git history + tags + ADRs + forge-archived repos |
| `README.md` sentinel | `README.md` + `AGENTS.md` + `project.yaml` |
| One home per file | One source of truth per fact |
| Rightward-only lifecycle | Rightward-only stages (§7) |
| `audit.sh` invariant checks | CI standard-compliance checks |

Repositories live under WORKSPACE's `code/` tree and are opaque to it: WORKSPACE governs *between* repos, PROJECT governs *within* them, and the seam between the two standards is the repository root.

### 15. Anti-patterns

- **Graveyard directories** (`legacy/`, `old/`, `@removal-safe/`, `deprecated/`). Git is the archive; the working tree is for the living (§3).
- **Status files as documents** (`INFO.md`, `XYZ-STATUS.md`, `TODO.md` at root). Status is tracker data or manifest data; documents rot.
- **Root sprawl.** Every unsanctioned root entry is a small repeal of §4; twenty of them are a landfill.
- **The wiki fork.** Prose truth split between repo and wiki always diverges. Docs live in the repo (`docs/`), versioned with the code they describe.
- **Duplicate agent configs with real content.** Two agent files with instructions is one agent file too many; drift is guaranteed.
- **The eternal `incubating`.** Projects that ship to users while claiming instability are extracting active-stage trust while dodging active-stage guarantees. Stage claims are promises; CI can't check honesty, but reviewers must.
- **Generated files committed as source** (build output, lockfile-derived docs) without marking. Agents and humans will edit them; mark generated paths in `AGENTS.md` §5 and gitignore or CI-verify them.
- **The Grand Restructure.** Same as WORKSPACE §19: layout changes are versioned standard events with migration notes, not weekend moods. Stability of paths is what CI, docs links, and muscle memory are built on.

### 16. Adoption & Migration

Bounded, like WORKSPACE §18: one pass per repo:

1. **Manifest first (15 min).** Write `project.yaml` honestly. Classification forces the conversations (owner? stage? successor?) that restructuring alone avoids.
2. **Root cleanup (30 min).** Create missing required docs (stubs are fine); move root strays into role directories; delete dead files in one labeled commit (`chore: remove dead code. See CHANGELOG`).
3. **Consolidate truth (1–2 h).** Fold duplicate docs into single sources + pointers; write `AGENTS.md`; reduce vendor agent files to stubs.
4. **Wire enforcement (1 h).** Add CI checks for the closed set, manifest schema, formatting, and tests; enable branch protection and `CODEOWNERS`.

History is preserved by *default* (it's git); `git mv` where practical for rename tracking. Fleet migration is this loop plus a dashboard built on `project.yaml`, which is the moment the manifest starts paying for the whole standard.

### 17. Future Extensions

- **Hosted schema registry.** The JSON Schemas in `spec/schemas/` published at stable versioned URLs so third-party validators resolve them by `$id`.
- **Fleet dashboards.** Org-wide views over manifests: stages, owners, deprecations, support gaps.
- **Language-specific scaffolds.** Per-ecosystem variants of `template/`, each still PROJECT-shaped.
- **Compliance levels**: Bronze/Silver/Gold conformance tiers (defined by which PROJECT-CHECKLIST sections pass) for gradual enterprise adoption.
- **Agent capability contracts.** Extending `AGENTS.md` §5 constraints into signed, machine-enforced policy.

Invariants that every extension must preserve: single source of truth per fact, closed root, rightward-only lifecycle, git-as-archive, one canonical agent guide.

---

## Appendix A: The Standard on One Page

```
1. The root is a closed set: six required docs, a fixed directory list, nothing else.
2. Every fact has one home; everything else links to it.
3. project.yaml declares type, stage, maturity, owner, visibility: machine-readable.
4. Stages move rightward: idea → incubating → active → maintenance → deprecated → archived.
5. Git is the archive. No graveyard folders. Delete + changelog + tag.
6. AGENTS.md is canonical; CLAUDE.md / GEMINI.md are 3-line pointers.
7. docs/ holds prose truth; decisions/ is append-only ADRs; examples run in CI.
8. Conventional commits, semver tags, protected default branch.
9. Every rule that can be CI-checked is CI-checked.
10. Layout changes are standard revisions with migrations: rare and deliberate.
```

---

*PROJECT is released as an open standard alongside workspace.md, project-matrix.md, and project-checklist.md. Adopt the manifest, close the root, and let the machines hold the line.*
