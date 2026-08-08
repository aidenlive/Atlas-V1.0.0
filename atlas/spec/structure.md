---
id: structure
order: 3
title: "STRUCTURE: the shape of a document"
tagline: "The shape of a document, and the visual vocabulary that carries it"
question: "How is a piece of writing shaped?"
version: "1.0"
status: published
stability: stable
rule_prefix: "S-"
companions: [voice, language, matrix, checklist]
kind: standard
owner: role:editorial-lead
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, developers, customers]
summary: "Lead with the answer, vary the shape, and let a reader understand a document before reading it."
---

# STRUCTURE: the shape of a document

> A reader decides whether to read your document by scanning it.
> Structure is that decision's user interface.

## What this is

STRUCTURE governs composition: what comes first, how sections nest, and which
visual element carries which kind of information. It applies to every document
we publish, in Markdown or anywhere else.

The test the whole standard serves: **a reader should be able to scan a document
and understand its shape before reading a word of it in detail.**

## Composition

Every substantial document follows the same order, because it is the order a
reader's questions arrive in:

1. **Context** — what this is, and who it is for.
2. **Key takeaway** — the answer, before the reasoning.
3. **Supporting detail** — the reasoning, in descending order of importance.
4. **Examples or visual explanation** — the thing made concrete.
5. **Next steps or references** — where to go now.

An FAQ, a runbook, and a launch announcement are all this order in different
clothes.

## Visual vocabulary

Use a rich but intentional mix. Each element has a job, and using it for another
job costs the reader time:

| Element | Job |
|---|---|
| Headings | Create a hierarchy a reader can navigate by scanning |
| Short paragraphs | Carry argument and explanation |
| Bulleted lists | Hold items with no inherent order |
| Numbered lists | Hold steps, in order, that must be followed |
| Tables | Compare attributes, options, states, or specifications |
| Blockquotes | Set apart context that would interrupt the narrative |
| Callouts | Flag a note, a warning, a tip, or a decision |
| Code blocks | Show exact input and output, with a language label |
| Inline code | Name commands, paths, keys, and identifiers |
| Checklists | Track actionable work |
| Diagrams | Show relationships and flows that prose describes badly |
| Summaries | Give the reader who stops after 30 seconds the answer |

## Callouts

Four kinds, and nothing else. More kinds means the reader learns none of them.

> **Note**
> Additional context or clarification.

> **Important**
> Information that materially changes interpretation or execution.

> **Warning**
> A real risk, limitation, or way this fails.

> **Tip**
> A shortcut, recommendation, or better default.

## The rules

- **S-01 One title.** Every document has exactly one H1, and it says what the
  document is. The declared `title` in front matter matches it.
- **S-02 Headings descend one at a time.** No jumping from H2 to H4, and nothing
  deeper than H4. If you need H5, the document is two documents.
- **S-03 Paragraphs stay scannable.** Six sentences is the ceiling. Longer than
  that usually means a list is hiding inside a paragraph.
- **S-04 Lead with the answer.** The first screen states what this is and what
  the reader should do. Background comes after, not before.
- **S-05 Structure earns its place.** Use a table when attributes are compared,
  a numbered list when order matters, a callout when something must not be
  missed. Formatting with no informational job is noise.
- **S-06 Emphasis stays rare.** More than three bold runs in a paragraph and
  bold stops meaning anything. Bold marks the sentence a skimmer must not miss.
- **S-07 Link text names its destination.** Write `see the install guide`
  around the link, never `click here`. Every relative link resolves to
  something that exists.
- **S-08 One fact, one home.** State a fact in one place and link to it from
  everywhere else. Every duplicate is a future contradiction.
- **S-09 Progressive disclosure.** Common cases first, edge cases after, full
  reference last or elsewhere. A document that front-loads exceptions teaches
  nobody the normal path.
- **S-10 Enough variation to scan.** A substantial document that is an
  uninterrupted wall of paragraphs fails this standard even when every sentence
  in it is good.

## What to avoid

- Long uninterrupted paragraphs
- Nesting past two levels
- The same information repeated in three formats
- Decorative formatting with no informational value
- Walls of links with no annotation
- Headings that exist to break up text rather than to name a section

## Related

- [VOICE](voice.md) — how the company sounds
- [MATRIX](matrix.md) — what a kind of content requires
- [CHECKLIST](checklist.md) — whether it is ready to publish
