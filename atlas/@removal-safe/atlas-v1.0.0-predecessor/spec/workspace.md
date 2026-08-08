---
id: workspace
order: 1
title: WORKSPACE
tagline: "An open standard for organizing digital work"
question: "Where does a file live?"
version: "1.0"
status: stable
rule_prefixes: []
checklist_prefixes: []
companions: [project]
---

# WORKSPACE: An open standard for organizing digital work

---

> A filesystem is not storage. It is the operating system of your attention.
> Organize it once, correctly, and never think about it again.

---

## 0. What This Is

WORKSPACE is a standard, not a suggestion. It defines a single, stable, machine-legible structure for all digital work: on a laptop, in cloud storage, on a NAS, inside an enterprise share, or under the hands of an AI agent. It is opinionated by design. Options are the enemy of habits, and habits are the only organizational system that survives contact with a Tuesday afternoon deadline.

This document answers *why* before *how*, because a rule you understand is a rule you keep. A rule you merely copied is a folder you will abandon by March.

---

## Part I: The Philosophy

### 1. Why Every Computer Eventually Becomes Disorganized

Disorganization is not a character flaw. It is the default outcome of three forces acting on every filesystem:

1. **Filing costs attention at the worst possible moment.** Files arrive while you are busy: mid-download, mid-meeting, mid-thought. Any system that demands a decision at arrival time will be bypassed under load, and the bypass location (Desktop, Downloads) becomes the real filing system.
2. **Categories decay faster than files.** You organize around today's mental model: this job, this project, this year's interests. The files outlive the model. Two years later, half your folders describe a life you no longer lead, and new files have nowhere honest to go.
3. **Entropy is asymmetric.** Making a mess takes zero seconds; cleaning one takes a weekend you will never schedule. Any structure that requires ongoing curation loses to any structure that doesn't.

The conclusion is inevitable: **a durable system must capture without deciding, categorize without predicting the future, and maintain itself without willpower.** Every rule in this standard exists to satisfy one of those three requirements.

### 2. Why Most Folder Hierarchies Fail

Folder trees fail for one root cause: **they encode categories instead of behavior.**

A category answers "what is this file *about*?": a question with many defensible answers. Is a mortgage PDF `finance`, `house`, `legal`, or `2024`? All four. So the file lands in one, you look in another, and trust in the hierarchy dies. Once you stop trusting the tree, you stop using it, and the collapse is total.

Behavior answers a different question: "what am I *doing* with this file?", and that question has exactly one answer at any moment. You are triaging it, working on it, referencing it, sharing it, or done with it. Five states. No ambiguity. This is why WORKSPACE's top level encodes **lifecycle, not topic**. Topics belong deeper in the tree, where the blast radius of a wrong guess is one subfolder, not your whole system.

Hierarchies also fail by being too deep (every level is a decision, and decisions are the tax that kills filing) and too clever (a structure only its author understands is a structure no colleague, spouse, or agent can use). The standard therefore caps depth and forbids cleverness.

### 3. Why Search Is Not a Substitute for Organization

"Just search for it" is the most seductive lie in personal computing. Search fails structurally, not incidentally:

- **Search requires remembering; structure requires only recognizing.** You cannot search for the contract whose filename you never knew, the photo with no text, or the spreadsheet you forgot exists. Browsing a stable tree surfaces what you didn't know to ask for.
- **Search returns instances; structure returns context.** Search finds *a* version of the proposal. The folder shows you all versions, the feedback beside them, and which one is final.
- **Search cannot express state.** No query distinguishes "the active draft" from "the abandoned one" unless *you* encoded that distinction somewhere, which is organization.
- **Search is a tool of last resort by definition.** Systems designed around the last resort have already failed.

Search is the smoke detector; organization is the building code. Keep both. Design for the second.

### 4. Why Temporary and Permanent Information Must Never Coexist

Mixing a scratch export with a signed contract in the same folder poisons both:

- The permanent file becomes **undeletable noise's hostage**: you can never bulk-clean the folder, because something in there matters.
- The temporary file gains **false permanence**: it gets backed up, synced, migrated, and searched for a decade because nothing marked it disposable.

Every file's disposability must be legible from its *location alone*. In WORKSPACE, anything in `00_inbox` is presumed disposable and drainable; anything in `05_archive` is presumed permanent and immutable. A human or a script can act on either with total confidence and zero inspection. That confidence is the entire point.

### 5. Why Active Work and Historical Records Are Fundamentally Different

Active work and finished records have opposite requirements on every axis:

| Axis | Active work | Historical record |
|---|---|---|
| Access | Constant, fast, local | Rare, tolerates latency |
| Mutation | Edited daily | Never modified again |
| Structure | Fluid, project-shaped | Frozen, time-shaped |
| Backup | Versioned, continuous | Write-once, verified |
| Mental role | "What am I doing?" | "What happened?" |

A single folder cannot serve opposite requirements. Systems that try (the eternal `Projects` folder holding 2017's work beside this week's) make active space cluttered and archives untrustworthy. WORKSPACE separates them absolutely: work lives in the numbered spaces; the moment it ends, it crosses into `05_archive` and never comes back. The archive is not where files go to die. It is where they go to become *facts*.

### 6. Why Archives Deserve First-Class Treatment

Most systems treat archiving as deletion's cowardly cousin: a `_old` folder, a `misc backup` drive. This is backwards. Your archive is the only part of your filesystem whose value *increases* with time. It is your tax defense, your legal record, your portfolio, your memory. It deserves the strongest guarantees in the system:

- **Organized by time, not topic**, because time is the one taxonomy that never needs refactoring. You will never rename 2019.
- **Immutable.** Files enter finished and are never edited. This makes verification (checksums), replication, and cold storage trivial.
- **Self-describing.** Each archived project carries its own context, because in ten years the folder is all that remains of the project's meaning.

### 7. Why Stability Beats Perfect Categorization

A merely *good* structure kept for twenty years is worth infinitely more than a *perfect* structure reorganized every eighteen months, because:

- **Muscle memory compounds.** Filing becomes reflex only when paths never move.
- **Every link, script, sync rule, and backup job is a bet on a path.** Reorganization defaults on all of them at once.
- **History becomes navigable.** When 2016 and 2026 share a shape, your past self's work is legible to your future self without translation.

This is why the standard's top level is deliberately small, deliberately generic, and deliberately boring. Boring is what survives.

### 8. Why Directory Structure Is Infrastructure

Roads, electrical grids, and HTTP share a property. They are dumb, stable substrates on which endless smart things are built. Your directory tree is the same class of object. When structure is predictable:

- **Backup policy becomes one line per space** ("version `02_work` continuously; cold-store `05_archive` yearly").
- **Sync policy becomes obvious** (personal cloud gets `01`, employer cloud gets `02`, nothing gets `00`).
- **Automation becomes trivial** (a cron job can drain the inbox because the inbox has an address).
- **AI agents become capable without configuration**, because the tree itself is the documentation.

When structure is ad hoc, every one of those requires bespoke rules that break silently. Infrastructure is the choice to pay the design cost once, up front, on behalf of every future decision.

---

## Part II: The Standard

### 9. Design Principles

1. **One home per file.** Every file has exactly one canonical location. Copies are caches; links are pointers; the home is truth. *Rationale: duplication is where version confusion, sync conflicts, and "which one is real?" are born.*
2. **Lifecycle over topic at the top.** The root encodes what you're *doing* with information, not what it's *about*. *Rationale: doing-state is unambiguous; aboutness is not (§2).*
3. **Capture is free; filing is scheduled.** Nothing may demand a filing decision at arrival time. Everything lands in the inbox; filing happens in batches. *Rationale: decisions under load get skipped (§1).*
4. **Shallow beats deep.** Three levels below the root is the working maximum. *Rationale: every level is a decision-tax at filing time and a guess-tax at retrieval time.*
5. **Time is the only safe global taxonomy.** When in doubt, organize by year. *Rationale: dates never get renamed, merged, or reconsidered.*
6. **Stability is a feature.** The top level may change once a decade, deliberately, with a migration. *Rationale: §7.*
7. **Machine-legible by default.** Names sort correctly in `ls`, survive every filesystem, and require no human to interpret. *Rationale: automation and AI compatibility are properties of names, not add-ons.*
8. **The structure is self-documenting.** A `README.md` sentinel at the root explains the system to any human or agent who lands there. *Rationale: a standard nobody can discover in place is folklore.*

### 10. Information Lifecycle

Every file moves through, at most, five stages. The directory it lives in *is* its stage: no metadata required.

```
CAPTURE ──▶ ACTIVE ──▶ REFERENCE ──▶ ARCHIVE ──▶ (DISPOSE)
 00_inbox    01–04       within        05_archive   trash
             spaces      spaces
```

- **Capture.** The file exists but has no decision attached. Lives in `00_inbox`. Maximum residence: days.
- **Active.** The file is part of ongoing work. Lives in `01_personal` … `04_shared`. Residence: the life of the task.
- **Reference.** The file is stable but consulted (templates, manuals, standing documents). Lives in `reference/` subfolders inside its space: reference is a *role within* a space, not a top-level dumping ground.
- **Archive.** The work is finished; the file is now a record. Lives in `05_archive/YYYY/`. Immutable. Residence: forever.
- **Dispose.** The file has no future value. Deleted, not archived. *Archiving garbage is the most common way archives lose trust.*

**The one transition rule:** files move *rightward only*. A resurrected old project is a *new* project in `03_projects` that may *copy from* the archive: the archived original never moves back. This single rule is what makes the archive immutable and therefore trustworthy.

### 11. Canonical Directory Hierarchy

```
~/                              (or the WORKSPACE root)
├── README.md                   ← sentinel: explains the structure in place
├── 00_inbox/                   ← capture. drained on a schedule, never stores.
│   ├── screenshots/
│   └── misc/
├── 01_personal/                ← private life. synced to personal cloud only.
│   ├── documents/              (identity, legal, insurance)
│   ├── finance/
│   ├── health/
│   ├── home/
│   ├── journal/
│   └── people/
├── 02_work/                    ← current employer. portable: leave job, archive folder.
│   ├── current/                (this week's live surface)
│   ├── projects/
│   ├── meetings/
│   ├── reviews/
│   └── reference/
├── 03_projects/                ← self-directed work with a definition of done.
│   ├── active/
│   ├── paused/
│   └── ideas/
├── 04_shared/                  ← jointly owned with specific people.
│   ├── household/
│   ├── family/
│   └── partner/
├── 05_archive/                 ← finished. immutable. organized by time.
│   ├── 2024/
│   ├── 2025/
│   └── 2026/
├── code/                       ← repositories (their own lifecycle: git)
│   ├── work/  personal/  playground/  forks/
├── notes/                      ← one flat notes vault (its own lifecycle: links)
├── assets/                     ← reusable raw material: fonts, icons, reference media
└── scripts/                    ← the automation that runs this workspace
```

**Rationale for each decision:**

- **Numeric prefixes (`00`–`05`)** force lifecycle order in every file browser on every OS, and give scripts stable, greppable anchors. The numbers *are* the standard's API.
- **`00_inbox` exists so nowhere else has to tolerate mess.** It is the only folder allowed to be chaotic, which is precisely what keeps the other five clean. Downloads and Desktop should redirect or drain into it.
- **`01_personal` vs `02_work` is a sync and trust boundary, not a topic boundary.** They separate because they belong to different clouds, different backup policies, and (on the day you change jobs) different fates. `02_work` is designed to be archived whole and recreated empty.
- **`03_projects` holds work with a definition of done.** `active/` is capped in practice by attention (if it exceeds ~5, something is lying about being active); `paused/` makes stalling honest instead of invisible; `ideas/` captures ambition without letting it impersonate commitment.
- **`04_shared` exists because shared ownership breaks single-owner rules** (naming discipline, drain schedules). Quarantining shared material protects the rest of the tree from other people's habits.
- **`05_archive/YYYY/`.** The year is the year the work *ended*. Within a year, folders keep the name they had in life, prefixed by their origin when useful (e.g. `2025/work_website-redesign/`).
- **`code/`, `notes/`, `assets/`, `scripts/` sit outside the numbered spaces** because each is governed by a stronger native lifecycle (git history, wiki links, reuse, execution) that the capture→archive pipeline would fight rather than help. The standard does not pretend one lifecycle fits artifacts that already have a better one.

### 12. Naming Rules

Names are the layer of the standard that travels *inside* every email attachment and upload. Five rules:

1. **Dates lead, and dates are ISO.** `2026-08-03_invoice_acme.pdf`. ISO 8601 sorts chronologically as a side effect of sorting alphabetically: free ordering, forever, everywhere.
2. **lowercase_with_underscores** (or hyphens: pick one per workspace and never revisit). No spaces: spaces break shells, URLs, and scripts. No case-sensitivity landmines across filesystems.
3. **Pattern: `date_what_who-or-context_version`.** `2026-03-14_proposal_acme_v3.pdf`. Each segment answers the question a future searcher will actually ask.
4. **Versions are explicit and terminal.** `_v1`, `_v2`, `_final` is banned; `final_v2_REAL` is the punchline of a failed system. When a document is done, it stops versioning by *moving to the archive*.
5. **Names must survive amnesia.** The test: would the name make sense pasted alone into a chat message, stripped of its folder? `report.pdf` fails. `2026-06_q2-board-report_finmetrics.pdf` passes. Folders provide context at home; names provide context in transit.

**ASCII-safe characters only** (`a–z 0–9 _ - .`). *Rationale. This is the intersection of every filesystem, sync service, shell, and URL encoder you will ever meet.*

### 13. Metadata & Tags

The standard's position is deliberately austere: **structure and names are the primary metadata; everything else is enhancement.**

- **Location encodes lifecycle state.** (§10)
- **Filename encodes date, subject, context, version.** (§12)
- **A `README.md` (or `_about.md`) inside any non-obvious folder encodes intent.** What this project was, its status, key decisions. This is required for every folder entering the archive. *Rationale: plain-text sidecars survive every migration; extended attributes, Finder tags, and proprietary metadata do not. If it isn't in a file, it will be lost.*
- **Inline tags in notes** (`#invoice`, `#acme`) are permitted in `notes/` where full-text search is native.
- **What is forbidden:** encoding state in metadata that could be encoded in location. A "status: archived" tag on a file in `03_projects/active/` is a contradiction the filesystem cannot detect. Location is the single source of truth precisely so that no second source can disagree with it.

### 14. AI Compatibility

An AI agent dropped into a WORKSPACE-compliant root can reason about it with **zero configuration**, because the standard was designed as a prompt:

- **The tree is self-describing.** Numeric prefixes declare lifecycle order; the root `README.md` declares the rules. An agent's first action is defined: read `README.md`, then `ls`.
- **Safety boundaries are positional.** Agents may write freely in `00_inbox`, propose in `01–04`, and must treat `05_archive` as read-only. These permissions need no ACL system: they follow from the lifecycle semantics any model can infer.
- **Filing is a solvable task.** "Move each file in `00_inbox` to its home" is well-posed *only because* every file has exactly one home. Ambiguous structures make agents guess; this structure makes them right.
- **Plain-text sidecars are agent memory.** `_about.md` files give agents project context without vector databases or custom retrieval: the context lives next to the content, which is where retrieval-by-locality already looks.
- **Stable paths make agent actions durable.** An agent-written automation, link, or report keeps working next year for the same reason a human's muscle memory does (§7).

The design claim: **a workspace an agent can operate without configuration is the same workspace a new employee, a spouse, or your future self can operate without a briefing.** AI compatibility is not a feature bolted on; it is legibility, and legibility was the goal all along.

### 15. Automation Rules

Automation in WORKSPACE is not clever; it is *inevitable*, because every job reduces to "act on a known path on a schedule." The five canonical automations, all living in `scripts/`:

1. **`drain.sh`: inbox triage assist** (nightly). Sorts `00_inbox` contents by type into staging subfolders (`screenshots/`, `misc/`) and flags anything older than 7 days. It does not file (filing needs judgment) it *pressurizes*.
2. **`scaffold.sh`: structure creation** (once per machine/share). Creates the canonical tree idempotently. One script *is* the deployment story for laptops, NAS shares, and new hires.
3. **`archive.sh`: end-of-project ceremony.** Takes a folder, demands an `_about.md`, stamps checksums, and moves it to `05_archive/$YEAR/`. The ceremony is the feature: crossing into the archive should be a deliberate act, not a drag-and-drop.
4. **`audit.sh`: invariant checker** (weekly). Reports violations: files loitering in the inbox, spaces in filenames, writes detected inside the archive, projects in `active/` untouched for 60 days. *The standard is enforceable because it is checkable; it is checkable because every rule is positional or lexical.*
5. **`backup.sh`: policy per space** (continuous/nightly/yearly). Versioned sync for `01–04`, write-once replication with checksum verification for `05`, nothing for `00`. Three policies, six paths, done.

**The meta-rule:** any automation you write must key off the standard's paths and names (never off content inspection) so that it remains correct as content changes. Predictable structure is what lets dumb scripts be reliable, and reliable beats smart.

### 16. Synchronization Strategy

Sync disasters come from one cause: syncing a tree whose parts have different owners, sensitivities, and churn rates under a single policy. WORKSPACE's spaces *are* the sync units:

| Space | Policy | Rationale |
|---|---|---|
| `00_inbox` | **Local only.** Never synced. | Syncing chaos multiplies chaos across devices; the inbox drains before it would matter. |
| `01_personal` | Personal cloud, end-to-end where possible. | Your data, your account, your keys. |
| `02_work` | Employer's platform only. | Legal and contractual boundary; also makes offboarding a folder-archive, not a forensic audit. |
| `03_projects` | Personal cloud + versioning. | Your IP; churny; versions matter. |
| `04_shared` | The shared platform the *other people* actually use. | Shared space adopts the group's tool, or it isn't shared. |
| `05_archive` | Replicated (NAS + cold/cloud), **not live-synced.** | Immutable data needs replication and verification, not conflict resolution. Live sync on immutable data is pure risk. |
| `code/` | Git remotes. | Git *is* its sync; layering Dropbox on a repo is a known catastrophe. |

**Conflict doctrine:** because every file has one home and each home has one sync policy, a sync conflict is always a *bug report about a policy violation*, never a judgment call. Resolve the violation, not the file.

### 17. Archive Strategy

The archive is the system's crown jewel and gets its own contract:

- **Structure:** `05_archive/YYYY/origin_project-name/`. Year of completion, then the folder as it lived, plus its mandatory `_about.md`.
- **Immutability:** nothing in the archive is ever edited, renamed, or reorganized. Corrections are new files (`2026-01_correction_….md`) beside the originals. *Rationale: immutability is what makes checksums meaningful, replication safe, and the record trustworthy as evidence.*
- **Integrity:** `archive.sh` writes a `SHA256SUMS` manifest at deposit time; `audit.sh` re-verifies yearly. Silent corruption is the archive's only natural predator; checksums are the vaccine.
- **Media strategy:** primary copy on the NAS or main disk, second copy on a different medium or provider, refreshed when hardware is replaced (which happens naturally every 3–7 years: hardware churn *is* the media-migration schedule).
- **Formats:** prefer open, boring formats at archive time (PDF/A, plain text, CSV, standard image/video codecs). Export proprietary formats *at the archive ceremony*: the last moment the authoring app is guaranteed to exist.
- **Deletion discipline:** the archive is not a landfill. If it has no plausible future reader (legal, financial, sentimental, or professional) it is disposed, not deposited (§10). An archive you trust is small enough to have been curated.

### 18. Migration Guide

Migrating an existing mess is a bounded project, not a lifestyle. Four passes, in order:

1. **Scaffold (30 minutes).** Run `scaffold.sh`. The new structure exists *beside* the old mess. Nothing is at risk yet.
2. **Declare bankruptcy on history (1 hour).** Move the entire old structure (Desktop residue, `Documents (old)`, `backup_final/`) into `05_archive/YYYY/pre-workspace/`, untouched. *Do not sort it.* Sorting a decade of history is the trap that kills every migration; the archive's job is to hold it findable-by-search and out of the way. Sort individual items later, on demand, when you actually need one.
3. **Rehome the living (2–4 hours).** Only files touched in the last ~90 days deserve hand-filing into `01–04`. This is a small set (typically a few hundred files) and it is the *entire* active surface of your digital life.
4. **Wire the plumbing (1 hour).** Point browser downloads at `00_inbox`. Set sync clients per §16. Install `drain.sh` and `audit.sh` on schedules.

Total: one honest afternoon. The asymmetry is the point: the standard is cheap to adopt *because* it refuses to demand retroactive perfection. Enterprises follow the same passes per team share, with `04_shared` semantics applied to the whole root.

### 19. Anti-patterns

Each of these is banned because it destroys a specific guarantee:

- **The Desktop-as-workspace.** A capture zone with no drain. It is `00_inbox` without the standard's one redeeming rule. Empty it into the inbox; keep it empty.
- **`misc/`, `stuff/`, `to_sort/` inside active spaces.** These are inboxes hiding where the drain schedule can't see them. There is exactly one inbox.
- **Topic folders at the root** (`Photos of house`, `Taxes`, `Ideas`). They compete with lifecycle for the top level and reintroduce the many-answers problem of §2. Topics live *inside* spaces.
- **Deep nesting** (`clients/acme/2026/q1/proposals/drafts/old/`). Six decisions to file, six guesses to retrieve. Flatten; let names carry the detail.
- **`final_v2_REALFINAL.docx`.** Version chaos is lifecycle failure wearing a filename. Done means archived (§12.4).
- **Editing archived files.** One edit and the archive is no longer a record; it's just another folder you have to doubt.
- **Duplicate homes** ("it's in Dropbox *and* on the NAS *and* in the project folder"). Copies for backup are fine: invisible, mechanical, policy-driven. Copies as *organization* mean no file has a home, which repeals principle #1.
- **The Grand Reorganization.** The urge to redesign the tree is a signal to file your inbox, not to move your foundations. Structure changes are versioned events with migration notes, at most once a decade.
- **Metadata as a second source of truth** (§13). If a tag can contradict a location, one of them is lying and you can't tell which.

### 20. Future Extensions

The standard is complete for v1 but designed with extension seams:

- **`workspace.yaml`.** An optional machine-readable manifest at the root declaring space paths, sync policies, and retention rules, so tooling and agents can consume policy without parsing prose. The prose `README.md` remains authoritative for humans.
- **Namespaced spaces for organizations**: `02_work/` generalizes to per-team roots that each carry the full six-space lifecycle, giving enterprises fractal consistency: every level of the org looks like every other.
- **Agent capability contracts.** A standard `AGENTS.md` sidecar declaring what autonomous systems may do per space, extending §14's positional permissions into auditable policy.
- **Retention schedules.** Per-year archive metadata (`retain-until:`) enabling lawful, automatic disposal in regulated environments.
- **Federation.** Conventions for linking multiple WORKSPACE roots (personal + employer + household NAS) so that "one home per file" holds *across* roots, not just within one.

Extensions must preserve the invariants: one home per file, rightward-only lifecycle, positional truth, stable roots. Anything that preserves those is WORKSPACE; anything that doesn't is a different system wearing its folders.

---

## Appendix A: The Standard on One Page

```
1. Everything arrives in 00_inbox. Nothing lives there.
2. Six spaces: inbox → personal → work → projects → shared → archive.
3. Files move rightward only. The archive is immutable.
4. One home per file. Location is the source of truth.
5. Names: YYYY-MM-DD_what_context_version, lowercase, ASCII, no spaces.
6. Done means archived, under the year it ended, with an _about.md.
7. Sync policy follows the space, never the file.
8. Scripts key off paths, never contents.
9. The root README explains everything. Agents read it first.
10. The tree changes once a decade, on purpose, or not at all.
```

---

*WORKSPACE is released as an open standard. Implement it, extend it, script against it, and then stop thinking about your filesystem forever. That was the deal.*
