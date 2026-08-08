# Glossary

The terms this repository uses as though everyone already knows them. Written
for a reader who does not write code, because most of the people governed by a
standard are not the people who wrote its tooling.

---

**Agent.** An autonomous software system that acts on the repository, such as
an AI coding assistant. Agents are *principals*: they hold permissions, they are
named in records, and what they did is auditable. They are never treated as
people (ADMIN I-2).

**AGENTS.md.** The single file that tells an autonomous system how to operate
here: what this repository is, where things live, which commands to run, and
what it must not do. `CLAUDE.md` and `GEMINI.md` are three-line stubs pointing
at it, so there is one guide rather than one per vendor.

**ADR** (architecture decision record): a short, dated, numbered note recording
a decision, the options considered, and the consequences. ADRs are **append-only**:
once accepted, you never edit one. If the decision changes, you write a new ADR
that supersedes it, so the reasoning history survives. In
[`docs/decisions/`](../decisions/).

**Archived.** A project that is finished and frozen. Distinct from *deprecated*,
which is still running but on notice.

**Canonical.** The one authoritative copy. Everything else is derived from it.
"Markdown is canonical" means: if the website and the Markdown disagree, the
Markdown is right and the website is stale.

**Checklist item.** A row in [`spec/project-checklist.md`](../../spec/project-checklist.md)
that a project must pass to claim a maturity level. Identified by a prefix and a
number, such as `SEC-03`. See [`rule-ids.md`](rule-ids.md).

**Closed set.** A list that is complete, so anything not on it is a violation
rather than an unlisted extra. The repository root is a closed set.

**Compliance.** Passing the standard's own checks. `atlas check`
is the arm that enforces it locally and in CI.

**Design tokens.** Named values (colour, spacing, type, motion) that the
interface is built from, so a change is made once at the source rather than hunted
through a stylesheet. This repository uses Neue 1.0; see
[`assets/design/DESIGN.md`](../../assets/design/DESIGN.md).

**Deprecated.** Still working, but on a countdown. Declaring a project
deprecated requires naming a *successor* and a *sunset date*; the schema refuses
the manifest otherwise.

**Derived** / **generated**: produced by a script from something else. Never
edit a derived file; edit its source and re-run the script. The list of derived
files is in [`conventions.md`](conventions.md).

**Docked / overlay / sheet / drawer.** The four ways a region of the interface
can present itself as space runs out, in that order. A sidebar that is *docked*
on a wide screen becomes a *drawer* on a narrow one. The ladder only ever runs one
way: a region never becomes more prominent as space shrinks.

**Drift.** Two copies of the same fact that no longer agree. The characteristic
failure mode of documentation, and the thing most of this repository's tooling
exists to prevent.

**Region.** A named part of the interface: navigation, toolbar, content, panel,
inspector, banner, footer. A layout is this set with some of them turned off, not
a new design each time.

**Size class.** How much room a *region* has, in five steps (`compact`,
`medium`, `expanded`, `large`, `xlarge`). Deliberately distinct from a
*breakpoint*, which is how wide the *window* is. A pane responds to the room it
was given; a headline responds to the screen someone is holding.

**Fleet.** All the repositories an organization owns, taken together. The
standard's purpose is that any of them can be opened by anyone and understood
immediately, because they share a shape.

**Forge.** The hosting platform: GitHub, GitLab, Gitea. The word is
platform-neutral, so the standard does not have to be rewritten if you move.

**Forge metadata.** A repository's description, homepage, topics, and branch
protection. Declared in [`.github/settings.yml`](../../.github/settings.yml) and
applied from there, never configured by clicking, so it can be reviewed and
reverted like anything else.

**Grant.** Permission given to a principal, for a defined scope, usually with
an expiry. All authority in ADMIN is grants; nobody has permissions
merely by being who they are (I-1).

**Hero visual.** The image at the very top of a README, before any prose. It is
required (PRESENTATION P-02) because a repository's landing view is its user
interface, and it must carry alt text so it works for screen readers.

**Library.** The shared-asset catalog: things authored once and used many
times, in four classes (prompts, icons, typefaces, media). The class set is
closed: a fifth is added by amending the specification, not by making a folder.

**Manifest.** A small YAML file stating machine-checkable facts about something:
`project.yaml` for a repository, `workstream.yaml` for an initiative,
`admin.yaml` and `org.yaml` for authority. Manifests hold facts, never secrets.

**Maturity.** How much a project can be trusted: `experimental → alpha → beta →
stable → hardened`. A maturity claim is not an opinion. It is the result of the
matching checklist profile passing.

**Normative.** Text that defines what compliance means. Changing normative text
changes who is compliant, so it travels with a schema update, a version bump,
and a changelog entry. The opposite is *editorial*: typos, clarity, examples.

**Orchestrator.** The one agent responsible for a workstream as a whole. It may
assign scoped sub-agents. At most one per workstream (W-15).

**Principal.** Anyone or anything that can hold permissions: a person
(`person:jdoe`), a team (`team:payments`), or an agent (`agent:repo-bot`).

**Profile.** A named subset of a checklist: Baseline, Beta, Production,
Hardened. You claim a maturity level by passing its profile.

**Schema.** A machine-readable description of what a manifest may contain
(JSON Schema, in [`spec/schemas/`](../../spec/schemas/)). It encodes the same
rules the prose states, and tests compare the two so neither can drift alone.

**Scope.** The boundary of what an agent or grant may touch, written as paths
or task ids. An agent with no written scope has unbounded scope, which is why
vague scopes fail validation (W-14).

**Self-hosting.** The repository obeys the standard it publishes. A standards
repository that violates its own standard has already lost the argument
([ADR-0001](../decisions/0001-self-hosting.md)).

**Specification** (or *spec*, or *standard*): one of the eight normative
documents in [`spec/`](../../spec/). "The suite" means all eight together.

**Stage.** Where a project sits in its life: `idea → incubating → active →
maintenance → deprecated → archived`. Movement is rightward only.

**Successor.** The project that replaces a deprecated one. Required, so that
"this is going away" is always accompanied by "use this instead".

**Sunset date.** The date after which a deprecated project stops being
supported. Required alongside a successor.

**Template repository.** A repository the forge can copy to create new ones.
Here, [`template/`](../../template/) is the copyable scaffold, and its files are
mirrored from this repository's canonical sources.

**Waiver.** A recorded, time-limited exception to a checklist item. Waivers
expire, and **an expired waiver is a failure**, not a warning: otherwise a
waiver is just a permanent exemption with extra steps.

**Workstream.** One initiative, in one numbered directory, with a fixed
skeleton: plan, tasks, requirements, decisions, research, deliverables,
validation, agents, issues. It has a number, an owner, a location, and a
verification step, which is the difference between work you can audit and work
you can only remember.

**Workstream section.** One of the nine numbered directories inside a
workstream (`01_plan` through `09_issues`). Alongside them sit `README.md` and
`workstream.yaml`, which are not sections.
