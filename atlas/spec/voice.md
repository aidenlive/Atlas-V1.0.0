---
id: voice
order: 1
title: "VOICE: how the company sounds"
tagline: "How the company sounds, in any channel, to any reader"
question: "How does the company sound?"
version: "1.0"
status: published
stability: stable
rule_prefix: "V-"
companions: [language, structure, matrix]
kind: standard
owner: role:editorial-lead
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, developers, leadership]
summary: "The one voice, the tones it takes, and the ten rules that make it recognisable."
---

# VOICE: how the company sounds

> Voice is what stays the same. Tone is what changes.
> A release note and a condolence email are the same company speaking, at
> different volumes, about different stakes.

## What this is

Every other standard in this suite is about the shape of writing. This one is
about its sound. Consistency of sound is what makes a set of documents feel like
one company rather than eleven people with keyboards. It is also why "make it
sound like us" is the least actionable note an editor can give.

The rules below are the actionable version.

## The voice

We sound like a **capable colleague explaining something they know well**. Not a
brand, not a spokesperson, not a manual.

Four properties define it, and each one has an opposite worth naming:

| We are | We are not | Because |
|---|---|---|
| Clear | Simplistic | The reader is capable; the subject may be hard. Simplify the sentence, not the idea. |
| Direct | Blunt | Say the thing. Saying it kindly costs nothing. |
| Concrete | Vague | A number, a name, or an example beats an adjective every time. |
| Human | Chummy | Written by a person, not performing friendliness. |

## Tone

Tone is voice adjusted for stakes and audience. It moves along one axis —
**how much room the reader needs** — and nothing else moves with it. Grammar,
terminology, and structure do not relax because a channel is casual.

| Situation | Tone | What changes |
|---|---|---|
| Reference and documentation | Neutral, instructive | Shorter sentences, more structure, no personality |
| Announcements and releases | Confident, plain | Lead with the change and who it affects |
| Marketing and the website | Warm, specific | More rhythm; claims still carry evidence |
| Incidents and outages | Calm, factual | What happened, what we are doing, when we will update |
| Apologies and bad news | Direct, unhedged | Say it in the first sentence; explain second |
| Internal and team writing | Relaxed, efficient | Shorthand allowed once it is in the lexicon |

> **Important**
> Tone never licenses vagueness. The calmest possible incident note still says
> exactly what broke.

## The rules

- **V-01 One voice.** Every document sounds like the same company. A reader who
  cannot tell which team wrote something is the goal, not a side effect.
- **V-02 Second person, active verbs.** Address the reader as *you* and name the
  actor. `You can revoke a key` and `The service revokes the key`, never
  `Keys may be revoked`. Passive voice is permitted only where the actor is
  genuinely unknown or irrelevant.
- **V-03 The shorter word.** Where two words mean the same thing, use the
  shorter one. `use`, not `utilise`; `to`, not `in order to`; `help`, not
  `facilitate`. The lexicon lists the ones we have already decided.
- **V-04 One sentence, one idea.** A sentence over 34 words is almost always two
  sentences wearing one coat. Split it.
- **V-05 Claims carry evidence.** No superlative without a number, a source, or
  a named example. `Fastest in the industry` is a claim; `2.1× faster than the
  previous release, measured on the same fleet` is a sentence.
- **V-06 Say the hard thing first.** Bad news, breaking changes, and limitations
  go in the first paragraph. Burying them does not soften them; it only moves
  the reader's anger to the moment they find out.
- **V-07 No hedging stack.** One qualifier is honest, three is evasion. Delete
  `we believe it may potentially`, and write what is true with the single
  qualifier the fact deserves.
- **V-08 No filler openers.** Cut `In today's fast-paced world`, `It is
  important to note that`, and every sentence whose removal changes nothing.
  Start at the first sentence that carries information.
- **V-09 Humour is allowed, jokes are not required.** Dry and specific is
  welcome; a joke that a reader in a hurry has to parse is a tax. Never make one
  in an apology, an incident note, or a security advisory.
- **V-10 Write for the reader who is not enjoying this.** Assume the reader is
  tired, interrupted, and reading on a phone, because often they are. Anything
  that survives that reader is good writing for everyone else.

## Before and after

> **Before**
> In order to facilitate a seamless onboarding experience, it is important to
> note that new users may be required to potentially verify their identity prior
> to accessing certain functionality within the platform.

> **After**
> New users verify their identity before they can invite teammates or move
> money. Everything else works immediately.

The rewrite is 22 words instead of 34, names the two things that are gated, and
answers the reader's actual question. Rules applied: V-03, V-04, V-07, V-08.

## Related

- [LANGUAGE](language.md) — the words, spellings, and mechanics
- [STRUCTURE](structure.md) — the shape a document takes
- [MATRIX](matrix.md) — which tone a kind of content takes
