---
title: Naming and placement conventions
kind: reference
owner: role:standards-maintainer
status: published
updated: 2026-08-08
review_by: 2026-11-08
audience: [internal, developers]
summary: "Where anything goes, and what to call it, decided once so nobody decides again."
---

# Naming and placement conventions

## Files and directories

| Thing | Convention | Example |
|---|---|---|
| Content and docs | `lower-case-with-hyphens.md` | `two-factor-setup.md` |
| Root documents | `SCREAMING_CASE.md` | `README.md`, `SECURITY.md` |
| Manifests | `lower.yaml` at the root | `project.yaml` |
| Schemas | `<kind>.schema.json` | `content.schema.json` |
| Standards | `<id>.md`, matching the declared `id` | `spec/voice.md` |
| Prompts | `request-<verb>-<object>.txt` | `request-write-brief.txt` |
| Workstreams | `NN_slug/` | `work/02_roll-out-to-teams/` |
| Decisions | `NNNN-short-title.md` | `docs/decisions/0005-archive-then-rebuild.md` |

## Where things live

| If it is… | It goes in |
|---|---|
| A rule the company must follow | `spec/` |
| An explanation of how to do something | `docs/guides/` |
| A list, table, or lookup | `docs/reference/` |
| A record of a decision and why | `docs/decisions/` |
| Reusable text, terms, or prompts | `library/` |
| Published writing in a content repository | `content/` |
| Work in progress | `work/NN_slug/` |
| A worked, validated sample manifest | `examples/` |

## Identifiers

| Kind | Shape | Example |
|---|---|---|
| Principal | `person:`, `role:`, `team:`, or `agent:` plus a slug | `role:editorial-lead` |
| Rule | Standard prefix, two digits | `S-07` |
| Workstream | Two digits, underscore, slug | `01_rebuild-editorial-system` |
| Task | `T` plus a number, unique in its table | `T4` |

## Dates

ISO dates (`2026-08-08`) in front matter, manifests, and tables. Long dates
(`8 August 2026`) in a sentence. Never a numeric format that means two different
days on two continents.

## Sanctioned root entries

The root is a closed set (CONTENT C-02). Files: `README.md`, `CHANGELOG.md`,
`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `LICENSE`, `AGENTS.md`,
vendor agent stubs, `project.yaml`, `authority.yaml`, `pyproject.toml`, and
dotfiles. Directories: `spec/`, `docs/`, `library/`, `content/`, `work/`,
`src/`, `tests/`, `scripts/`, `template/`, `examples/`, `assets/`, `.github/`.
