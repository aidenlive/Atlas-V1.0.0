---
id: presentation
order: 6
title: PRESENTATION
tagline: "The repository presentation standard: metadata, README composition, and visual identity"
question: "How does it show itself?"
version: "1.0"
status: stable
rule_prefixes: [P-]
checklist_prefixes: [PR-]
companions: [project, project-matrix, project-checklist, library]
---

# PRESENTATION: Metadata, README composition, and visual identity

---

> A repository's landing view is its user interface.
> Structure makes a repo operable; presentation makes it *adoptable*.
> Both are engineering, and both are checkable.

---

## 0. What This Is

PROJECT defines what must be true *inside* a repository. PRESENTATION defines
what must be true about how the repository *shows itself*: on the forge
listing, in the README's first screen, and in the consistency of names and
visuals across a fleet. It exists because discovery and trust are decided in
the first ten seconds of contact, long before anyone reads `docs/`.

The same design bet as the rest of the suite: **declared beats configured.**
Forge metadata typed into a settings page is unreviewable state; forge
metadata declared in the manifest and applied by tooling is a diff.

## 1. Forge Metadata (normative)

Every repository past `idea` stage declares, in `project.yaml` under
`metadata:`, the fields its forge listing renders:

```yaml
metadata:
  description: "One sentence, ≤ 160 chars, value-first, no trailing period"
  website: https://example.dev          # or the docs path as placeholder
  topics: [kebab-case, three-to-ten, of-them]
```

**Rules:**

- **P-01 Description.** Required. ≤ 160 characters (forge truncation
  boundary), states *value*, not implementation ("Validates fleet manifests
  in CI", not "A Python repo with some scripts"). It must be the same
  sentence as the README's title line: one truth, two views.
- **P-02 Hero visual.** The README opens with a visual before any prose. Where
  the forge supports it, ship a light and a dark variant behind `<picture>` with
  `prefers-color-scheme`; a single dark-only banner is unreadable for half the
  audience. The `<img>` inside `<picture>` is the fallback and still carries the
  alt text. The visual is one of:
  a banner, screenshot, architecture diagram, or demo GIF, stored under
  `assets/` (or `docs/assets/` for docs-only visuals). SVG preferred:
  versionable, diffable, dark/light-safe, no binary churn. Every image
  carries meaningful alt text: the hero must degrade to words.
- **P-03 Topics.** 3–10, kebab-case. First topic is the Matrix family
  (`app`, `lib`, `service`, `tool`, `platform`, `content`); the rest are
  ecosystem and domain terms a searcher would actually type.
- **P-04 Website.** Required for `visibility: public`; a placeholder
  pointing at `docs/` or the repo itself is acceptable and honest. Broken
  links are not.
- **P-05 Settings as code.** Forge metadata is applied *from* the manifest
  (e.g. a `settings.yml` consumed by an app/action, or a sync script), never
  hand-typed. Drift between manifest and forge is a defect, same as
  ADMIN drift.

## 2. README Composition (normative)

The PROJECT §8 skeleton is extended with a fixed *visual order*. Top to
bottom, first screen:

```
1. Hero visual        (P-02: banner / screenshot / diagram, with alt text)
2. # Name: one-line value proposition   (identical to metadata.description)
3. Badge row          (stage, maturity, CI, version, license: rendered from
                       project.yaml, never hand-drifted)
4. ## What & Why      (≤ 3 sentences)
5. ## Quickstart      (copy-paste true)
… then Documentation / Status / Contributing per PROJECT §8.
```

- **P-06 One screen to comprehension.** Items 1–5 fit in the first viewport
  of a default forge render. Everything below the fold is elaboration.
- **P-07 Badges are views, not facts.** Every badge value must be derivable
  from `project.yaml` or CI; a badge that can disagree with the manifest is a
  second source of truth and therefore banned.
- **P-08 Architecture is drawn.** Any repo with more than one moving part
  includes a diagram (in `docs/architecture/` or the README) showing the
  parts and their relations. Diagrams-as-code (SVG, Mermaid) preferred so
  diffs review like prose.

## 3. Fleet Consistency (normative)

- **P-09 One shape everywhere.** Every repository, regardless of type,
  presents the same skeleton: same root set, same README order, same
  `docs/` substructure, same badge row. A reader who has seen one repo has
  seen the navigation of all of them. Type-specific content varies;
  *composition* does not.
- **P-10 Names align across layers.** Repo name (lowercase-hyphenated),
  manifest `name:`, README `#` title, and package/artifact name agree
  (modulo registry-imposed prefixes). Renames are release events with
  redirects, changelog entries, and forge redirects verified.
- **P-11 Visual identity is inherited.** Fleet-level brand assets (palette,
  banner geometry, badge style) live once: in a `platform.design` or the
  standards repo, and downstream repos consume, not fork, them. A fleet
  with fifty hand-made banners has no brand; it has fifty.

## 4. Checklist Additions

These items extend PROJECT-CHECKLIST and are claimed with the profiles shown:

| ID | Profile | Item |
|---|---|---|
| ☐ PR-01 | Baseline | `metadata:` block present and schema-valid (P-01, P-03, P-04) |
| ☐ PR-02 | Baseline | README opens with a hero visual with alt text (P-02) |
| ☐ PR-03 | Beta | Forge metadata applied from the manifest; no drift (P-05) |
| ☐ PR-04 | Beta | Badge row present; values derivable from manifest/CI (P-07) |
| 🧭 PR-05 | Production | First README screen passes P-06 on a default render, reviewer-attested |
| ☐ PR-06 | Production | Architecture diagram exists for multi-part repos (P-08) |

## 5. Anti-patterns

- **The blank storefront.** No description, no topics, default social image —
  a repo invisible to the search that would have found it.
- **The wall of text.** A README whose first screen is prose. Readers triage
  visually; the hero and badge row are the triage interface.
- **Screenshot rot.** A hero image of a UI three versions old is misinformation
  with authority: regenerate at release, or use diagrams that CI can rebuild.
- **Badge cosplay.** Static badges hand-set to green. If it isn't derived,
  it's decoration pretending to be evidence.
- **Fifty brands.** Per-repo visual improvisation. Inherit the fleet identity
  (P-11); spend creativity on the product, not the banner.

---

*PRESENTATION completes the reader-facing half of the suite: PROJECT makes a
repository operable, PRESENTATION makes it legible at first contact, and both
are enforced the same way, by schema and CI, not by taste.*
