---
id: library
order: 7
title: LIBRARY
tagline: "The shared-asset standard: prompts, icons, typefaces, and media as versioned, validated artifacts"
question: "Where do shared assets live, and on what terms?"
version: "1.0"
status: stable
rule_prefixes: [L-, L-A, L-I, L-T, L-M]
checklist_prefixes: []
companions: [project, presentation, admin]
---

# LIBRARY: Prompts, icons, typefaces, and media as versioned, validated artifacts

---

> An asset kept in someone's downloads folder is tribal memory with a filename.
> An asset in the library is a convention with a diff.
> This standard makes the reusable things: intent, marks, letterforms, media —
> first-class, reviewed, testable artifacts.

---

## 0. What This Is

The suite standardizes structure (WORKSPACE, PROJECT), classification
(MATRIX), quality (CHECKLIST), authority (ADMIN), and presentation
(PRESENTATION). What teams and agents still improvise daily is everything
*reusable*: the sentence that kicks off "cut the release", the icon that gets
redrawn slightly differently in each repository, the font file emailed around
with no license beside it, the screenshot nobody can find the source of.

Improvised reuse produces improvised results. Scope drifts per author,
constraints get forgotten, and the same thing exists in twenty near-identical
copies across a fleet with no way to tell which one is current.

LIBRARY defines the **shared-asset catalog**: things authored once, used many
times, stored in `library/`, indexed for machines, and governed exactly like the
rest of the standard: reviewed, versioned, and CI-checked.

### The four classes

| Class | Directory | Holds | Indexed by |
|---|---|---|---|
| **prompts** | `library/prompts/` | Reusable, tool-agnostic statements of intent | `library/prompts/index.yaml` |
| **icons** | `library/icons/` | Interface glyphs, one concept per file | `library/icons/index.yaml` |
| **typefaces** | `library/typefaces/` | Font files and the license that permits them | `library/typefaces/index.yaml` |
| **media** | `library/media/` | Diagrams, screenshots, recordings, and their sources | `library/media/index.yaml` |

A fifth class is not added by putting files in a new folder. It is added by
amending this section, which is the point: the closed set is what makes
`library/` navigable rather than a second downloads folder.

## 0.1 Rules for every class (normative)

These hold whatever the asset is. Class-specific rules follow in §1 and §7.

- **L-A1 One home.** An asset lives in exactly one place in `library/`. A copy
  elsewhere in the repository is a bug, not a convenience.
- **L-A2 Indexed.** Every class carries an `index.yaml` listing every asset
  with its id, path, and one-line description. An asset absent from the index
  does not exist; an index entry with no file is a broken build. CI checks both
  directions.
- **L-A3 Named for what it is.** `kebab-case`, describing the thing rather
  than its origin, its author, or its version. `arrow-right.svg`, never
  `Icon_final_v3 (2).svg`.
- **L-A4 Sourced.** Any asset that was derived from something else records
  what, in the index entry: the generator, the original, or the upstream project.
- **L-A5 Licensed.** Any asset the organization did not author records its
  license and its origin in the index entry. An unlicensed third-party asset is
  a legal defect, and it is treated as one.
- **L-A6 Reviewed like code.** Library changes go through pull request. There
  is no path by which an asset appears in the fleet without review.

## 1. The Prompt Contract (normative)

- **L-01 One objective per prompt.** Each file states a single clear
  operation with an unambiguous done-state. A prompt needing "and also" is
  two prompts.
- **L-02 Concise.** One to three sentences. The prompt carries *intent and
  constraints*; the standards it invokes carry the how. Long procedure
  belongs in `docs/guides/`, referenced, not inlined.
- **L-03 Implementation-agnostic.** Prompts name intents, standard
  concepts, and repo paths (`AGENTS.md`, `project.yaml`, checklist item IDs)
, never a specific assistant, IDE, or vendor feature. The same file must
  work pasted into any AI coding tool or handed to a human.
- **L-04 Safety is in the sentence.** Prompts for destructive or
  irreversible operations (deletion, deprecation, offboarding, releases)
  embed their guardrail: plan-before-act, confirmation gates, or explicit
  refusal conditions. A prompt that can be pasted carelessly must fail safe.
- **L-05 Complement, don't duplicate.** Prompts reference the standards
  (`spec/`, checklist IDs, gate names); they never restate their rules. When
  a spec changes, prompts that cite it are reviewed in the same change-set.

## 2. Files & Naming (normative)

- **L-06 Location.** The library lives in `library/prompts/`, one directory per
  category, plus `library/prompts/index.yaml` (the machine-readable catalog) and
  `library/prompts/README.md` (the human index).
- **L-07 Naming.** Files are `request-<verb>-<object>.txt` in
  lowercase kebab-case: `request-initialize-project.txt`,
  `request-review-access.txt`. Plain `.txt` because prompts are paste
  payloads: no frontmatter, no markup, nothing a target tool could
  misinterpret. *(Note: the suite's naming rules: WORKSPACE §12, PROJECT
  §10: apply here as everywhere; TitleCase variants of the same names are
  non-compliant.)*
- **L-08 Index integrity.** Every prompt file appears in `index.yaml`
  with its category and one-line objective; every index entry resolves to a
  file. CI enforces both directions: an unindexed prompt is invisible, an
  indexed ghost is a lie.

## 3. Categories (the closed set)

Fourteen categories spanning the lifecycle; extension follows the Matrix
policy (new categories via a versioned revision, `x-` prefix for local ones):

`workspace · repository · architecture · documentation · github ·
administration · quality · security · releases · maintenance · design ·
agents · operations · workstreams`

## 4. Usage Model

- **Humans** copy a prompt into any assistant, optionally appending
  specifics ("…for the payments-api repo"). The prompt is the floor, not the
  ceiling.
- **Agents** may be pointed at `library/prompts/index.yaml` to discover sanctioned
  operations, and at a specific file as their task statement. `AGENTS.md`
  remains the canonical constraints document; prompts *invoke* it (see
  `agents/request-onboard-agent.txt`), never replace it.
- **Teams** treat prompt edits like spec edits: PR, review, changelog for
  behavior-relevant changes. A prompt that routinely needs local edits is a
  prompt with a defect: fix the library, not sixty pasted copies.

## 7. The Other Three Classes (normative)

### Icons

- **L-I1 One concept per file, drawn on a 24px grid** with a 1.5–1.75px stroke,
  round caps and joins, and no fill. An icon that only reads at one size has been
  drawn as a picture rather than as a glyph.
- **L-I2 `currentColor` only.** An icon carries no baked color, so it inherits
  from the surface that uses it and needs no dark-mode variant.
- **L-I3 No text inside an icon.** Text does not scale, does not translate, and
  is not accessible inside a glyph.
- **L-I4 The accessible name lives at the use site**, not in the file. The same
  glyph is "close" in one control and "dismiss" in another.

### Typefaces

- **L-T1 The license ships with the file.** A typeface directory contains the
  font files and the license that permits their use, in the same directory. No
  license, no typeface.
- **L-T2 Web formats are derived, not authored.** `woff2` is generated from the
  source by a script, and the script is in `scripts/`.
- **L-T3 Declare the fallback stack.** Every family records the stack that
  applies before it loads and if it never loads, because a missing font is a
  layout event, not a styling detail.

### Media

- **L-M1 The source travels with the output.** A diagram records what produced
  it: the generator script, the `.excalidraw`, the design file. A raster with no
  source is a dead end the next person cannot edit.
- **L-M2 Prefer generated over drawn.** If a script can emit it, a script
  should, and then it is drift-checked like everything else.
- **L-M3 Describe it in the index.** The index entry carries the description a
  reader would need; alt text at the use site is written for that context.

## 5. Checklist Additions

| ID | Profile | Item |
|---|---|---|
| ☐ PL-CI-01 | Beta | `library/prompts/index.yaml` and files are mutually complete (L-08), CI-checked |
| ☐ PL-CI-02 | Beta | Prompt files obey naming and length contracts (L-02, L-07) |
| 🧭 PL-CI-03 | Production | Destructive-operation prompts reviewed for fail-safe wording (L-04) |

## 6. Anti-patterns

- **The prompt novel.** A 400-word prompt restating the checklist. The
  standards are the how; the prompt is the ask.
- **Vendor lock-in wording.** "Use your Composer feature to…": dead the day
  the tool renames it. Name intents, not features.
- **The stale citation.** A prompt referencing a checklist ID or path that no
  longer exists. L-05 makes spec changes and prompt reviews one change-set.
- **Prompt forks.** Per-person variants of library prompts living in gists
  and notes apps: tribal memory reborn. Improve the shared file.
- **The unguarded footgun.** "Delete all deprecated repos" with no plan gate.
  If the worst careless paste is unrecoverable, L-04 was violated.

---

*LIBRARY completes the loop: the suite defines what good looks like,
and the library makes asking for it a one-paste, fleet-consistent act: for
every human and every agent, in every tool.*
