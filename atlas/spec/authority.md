---
id: authority
order: 7
title: "AUTHORITY: who may act"
tagline: "Who writes, who reviews, who approves, and who answers for it later"
question: "Who may write, review, approve, and retire content?"
version: "1.0"
status: published
stability: stable
rule_prefix: "A-"
companions: [content, checklist, matrix]
kind: standard
owner: role:editorial-lead
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, leadership]
summary: "Roles, approvals, and the workstream shape that makes editorial work visible and countable."
---

# AUTHORITY: who may act

> Ownership that lives in someone's head leaves when they do.
> Ownership that lives in a file survives the handover.

## What this is

AUTHORITY declares who may do what to content: draft it, edit it, review it,
approve it, publish it, retire it, and change the standard itself. It also
defines the shape editorial work takes while it is in progress.

Everything here is declared in [`authority.yaml`](../authority.yaml) and checked,
because the moment authority is informal, the answer to "who signed off on this?"
becomes a search through chat history.

## Roles

Roles, not people, hold authority. People hold roles. When someone leaves, one
line changes:

```yaml
principals:
  - id: person:dana
    name: Dana Okafor
    kind: person
roles:
  - name: editorial-lead
    held_by: [person:dana]
    may: [draft, edit, review, approve, publish, retire, change-standard]
```

| Verb | Means |
|---|---|
| `draft` | Create new content in `draft` |
| `edit` | Change content owned by someone else |
| `review` | Read a document and record that it meets its profile |
| `approve` | Accept the content for publication |
| `publish` | Move it to its channel |
| `retire` | Take it out of the reader's path |
| `change-standard` | Alter a rule in `spec/` |

## Workstreams

Work in progress lives in `work/`, one numbered folder per initiative, with the
same five sections in the same order, every time:

| Section | Holds |
|---|---|
| `01_brief` | What we are writing, for whom, and why |
| `02_tasks` | The task table — the only place status is recorded |
| `03_drafts` | Drafts in progress, or pointers to where they live |
| `04_review` | Reviewers, comments, and sign-off |
| `05_publication` | Where it went, when, and what happens to it next |

A fixed shape means a person joining on Tuesday and an agent picking the work up
on Wednesday both find the brief in `01_brief/` without asking anyone.

## The rules

- **A-01 Authority is declared.** Every repository carries an `authority.yaml`
  naming principals, roles, and what each role may do.
- **A-02 Every named holder exists.** A role held by an undeclared principal,
  or an owner who is not a principal, is a violation. Names that resolve to
  nobody are the mechanism by which ownership disappears.
- **A-03 Publication requires an approver.** Nothing reaches `published` without
  sign-off from a role holding `approve` for that kind of content.
- **A-04 The author is never the sole approver.** One other pair of eyes, always.
  The rule holds for the editorial lead's own writing.
- **A-05 Standards changes travel as one change-set.** A change to a rule in
  `spec/` moves with its schema change, its version bump, and its changelog
  entry, so the contract and its enforcement never disagree.
- **A-06 Every workstream declares itself.** A `workstream.yaml` naming the id,
  title, status, owner, kind, audience, and open date.
- **A-07 Every workstream has the same five sections.** No workstream invents
  its own layout, however small it is.
- **A-08 Status lives in the task table.** Tasks are `todo`, `doing`, `blocked`,
  or `done`, recorded in one table and nowhere else.
- **A-09 Generated views stay current.** The dashboard and the index are
  regenerated from the task tables by `atlas work sync`. Progress is counted,
  never claimed: a workstream cannot report itself further along than its own
  tasks say it is.
- **A-10 Agents act under a principal.** An AI agent doing editorial work is
  declared as a principal, is assigned tasks like anyone else, and cannot hold
  `approve`. Machines draft and check; people accept the risk.

## Handover

When an owner changes, three things change in the same pull request. The
`owner` field in the affected front matter, the holder in `authority.yaml`, and
a dated line in the workstream saying what was handed over and what was left
undone. Anything less is not a handover; it is an absence.

## Related

- [CONTENT](content.md) — the facts a document declares
- [CHECKLIST](checklist.md) — what approval is asserting
- [MATRIX](matrix.md) — which kinds need which approvals
