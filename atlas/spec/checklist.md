---
id: checklist
order: 6
title: "CHECKLIST: is it ready?"
tagline: "Three profiles that decide whether a piece of writing is ready"
question: "Is it ready to publish?"
version: "1.0"
status: published
stability: stable
rule_prefix: "Q-"
companions: [content, matrix, authority, publication]
kind: standard
owner: role:editorial-lead
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, leadership]
summary: "Draft, Review, and Published profiles, each a short list of things that are either true or not."
---

# CHECKLIST: is it ready?

> Two people can argue about whether a draft is good.
> Nobody argues about whether it has an owner.

## What this is

CHECKLIST turns "is this ready?" into a list of statements that are either true
or false. It is the standard that ends the review meeting.

Three profiles, each a superset of the one before. A document claims a profile;
`atlas check` and `atlas lint` verify the mechanical half; a reviewer verifies
the rest.

## Draft

Enough to share with a colleague. Nothing here requires polish.

- [ ] Front matter present, with `title`, `kind`, `owner`, `status: draft`, `updated`
- [ ] The kind is right, and the shape follows MATRIX for that kind
- [ ] Audience declared
- [ ] One H1, headings descend one at a time
- [ ] The first screen says what this is and who it is for
- [ ] `atlas lint` reports no errors

## Review

Ready for someone else's name on it.

Everything in Draft, plus:

- [ ] Every claim carries a number, a source, or a named example (V-05)
- [ ] Every relative link resolves
- [ ] Terminology matches the lexicon; no unexplained acronyms (L-01, L-09)
- [ ] Structure varies enough to scan (S-10)
- [ ] Examples are real and have been run, not invented
- [ ] Prerequisites and limitations are stated, not implied
- [ ] Reviewers named in front matter, and each has actually read it
- [ ] `atlas lint --strict` reports no warnings, or each remaining warning is a
      deliberate choice someone can defend

## Published

Relied on by people who will not check it against anything else.

Everything in Review, plus:

- [ ] An approver named in `authority.yaml` has signed off (AUTHORITY A-03)
- [ ] `review_by` set from the cadence for this kind (M-05)
- [ ] The document it replaces is marked `superseded`, with `supersedes` filled in
- [ ] Discoverable: linked from the index a reader actually starts at (P-04)
- [ ] Metadata correct: description, title, and summary say the same thing (P-01)
- [ ] Accessible: alt text on every image, no meaning carried by colour alone
- [ ] `atlas check` passes on the repository

## The rules

- **Q-01 Profile is claimed, not assumed.** A document's `status` is its claimed
  profile. Claiming `published` while failing Published is a violation, not an
  oversight.
- **Q-02 Profiles nest.** Review contains Draft; Published contains Review.
  There is no route to `published` that skips a profile.
- **Q-03 The mechanical half is automated.** Anything a check can decide is
  decided by a check, so reviewers spend their attention on judgement rather
  than on missing front matter.
- **Q-04 A reviewer who has not read it has not reviewed it.** Naming someone in
  `reviewers` asserts that they read the document. Nothing else counts.
- **Q-05 Failing is normal.** A failed gate is information, not an accusation.
  The list exists so the fix is obvious, not so anyone is judged by it.
- **Q-06 Exceptions are recorded, not negotiated.** Publishing something that
  does not pass requires a dated note in the workstream saying what failed, who
  accepted the risk, and when it will be fixed.

## Related

- [CONTENT](content.md) — the facts a document declares
- [AUTHORITY](authority.md) — who may approve
- [PUBLICATION](publication.md) — what happens after sign-off
