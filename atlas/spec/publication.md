---
id: publication
order: 8
title: "PUBLICATION: how it shows itself"
tagline: "How content shows itself, where it goes, and what happens after"
question: "How does it show itself, and where does it go?"
version: "1.0"
status: published
stability: stable
rule_prefix: "P-"
companions: [content, matrix, checklist, language]
kind: standard
owner: role:editorial-lead
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, customers, press]
summary: "Titles, summaries, channels, accessibility, and the retirement of content that is no longer true."
---

# PUBLICATION: how it shows itself

> Most readers meet a document as a title in a list.
> That title is the document, as far as the decision to read it is concerned.

## What this is

PUBLICATION governs the last mile: the metadata a reader sees before the
content, the channel it goes to, the accessibility it owes every reader, and
what happens when it stops being true.

The design bet is the same as everywhere else in the suite: **declared beats
configured.** A description typed into a publishing tool is unreviewable state.
A description in front matter is a diff.

## The first screen

Three fields carry almost all of the decision to read:

| Field | Job | Limit |
|---|---|---|
| `title` | Names the thing, in the reader's words | 60 characters |
| `summary` | One sentence: what this is and who it is for | 200 characters |
| Opening paragraph | The answer, before the reasoning | 3 sentences |

They must agree with each other. A title promising a tutorial over a reference
is a broken promise the reader pays for.

## Channels

A document declares where it goes, and each channel has requirements it does not
get to skip:

| Channel | Additionally requires |
|---|---|
| `docs-site` | Navigation entry, working relative links, code samples that run |
| `handbook` | Owner role, review date, internal-only check |
| `website` | Approved claims, alt text, meta description |
| `blog` | Named author, date, no unapproved forward-looking statements |
| `email` | Subject under 60 characters, one call to action, plain-text fallback |
| `in-product` | Sentence case, no jargon, tested at 320 pixels wide |
| `social` | Standalone meaning without the link, no unexplained acronyms |
| `print` | No live links as the only route to a fact |

## The rules

- **P-01 One sentence, three places.** The `title` and `summary` in front
  matter, the H1, and the description on the channel say the same thing. One
  truth, several views.
- **P-02 Titles describe, not tease.** A reader scanning a list of titles can
  tell which one answers their question. Curiosity gaps are for advertising.
- **P-03 Every document declares its channel.** Content with no declared
  destination is a draft, whatever its status field says.
- **P-04 Published means discoverable.** Publishing includes linking the
  document from the index a reader actually starts at. A document nobody can
  reach was not published; it was uploaded.
- **P-05 Accessibility is not a phase.** Alt text on every image that carries
  meaning, no meaning carried by colour alone, headings used for structure
  rather than for size, and link text that works when read out of context.
- **P-06 Translated content declares its source.** A localised document names the
  document it was translated from and the version it was translated at, so drift
  is visible rather than discovered.
- **P-07 Generated views cannot outrun their source.** Any published artefact
  assembled by a tool — an index, a badge, a reference page — is generated from
  the file that makes its claim true, and regenerated in the same change.
- **P-08 Retirement is an act, not a lapse.** Content that stops being true is
  marked `superseded` or `retired`, removed from navigation, and pointed at its
  replacement. Silence is the worst possible redirect.

## Retirement

Every published document eventually stops being true. Three ways to end one,
and one of them is not allowed:

| Ending | When | What happens |
|---|---|---|
| Superseded | A newer document does the same job | New one names the old in `supersedes`; old one keeps a link forward |
| Retired | The thing it describes is gone | Status set, removed from navigation, one line in the changelog |
| Abandoned | — | **Not permitted.** Content left published and untrue is worse than no content |

## Related

- [CONTENT](content.md) — declaration and lifecycle
- [CHECKLIST](checklist.md) — the Published profile
- [LANGUAGE](language.md) — titles, capitalisation, and dates
