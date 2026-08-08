"""One-off generator for the prompt library source files.

Kept in the repository so the library can be regenerated or reviewed as a set,
rather than assembled by hand one file at a time. The .txt files are the
original; `scripts/build_library.py` derives the index from them.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1] / "library" / "prompts"

PROMPTS: dict[str, dict[str, str]] = {
    "brief": {
        "write-brief": "Write an editorial brief for the piece described below. Cover what we are writing, who it is for, why now, the one thing the reader should take away, and the constraints. Keep each section to two sentences.",
        "sharpen-audience": "Name the single reader this piece is for, in one sentence, including what they already know and what they are trying to do. Then list the three assumptions the current draft makes that this reader would not share.",
        "find-the-question": "Read the material below and state the question the reader is actually asking, in their words rather than ours. Then say whether the piece answers it in the first screen, and where the answer currently appears.",
        "scope-the-piece": "Propose a scope for this piece: what it will cover, what it will deliberately leave to another document, and roughly how long it should be. Flag anything in the source material that is really a second document.",
    },
    "research": {
        "gather-sources": "List the sources this piece needs before it can make its claims, separating what we already have from what someone must go and find. For each, say which claim it supports.",
        "check-claims": "List every factual claim in the draft below, and for each one say whether it carries a number, a source, or a named example. Flag the claims that carry none.",
        "interview-questions": "Draft eight questions for a subject-matter expert that would give us what this piece is missing. Order them so the first three would still be worth asking if the conversation ended early.",
        "competitive-read": "Summarise how three comparable documents from other companies handle this subject, in one paragraph each. End with the single thing each does better than our draft.",
    },
    "drafting": {
        "draft-from-brief": "Write a first draft from the brief below, following the shape the declared kind requires. Lead with the answer, keep paragraphs under six sentences, and mark anything you had to guess with a TODO.",
        "write-first-screen": "Write the first screen for this document: a title, a one-sentence summary, and an opening paragraph of no more than three sentences that says what this is, who it is for, and what to do next.",
        "expand-outline": "Turn the outline below into prose, one section at a time, without adding sections. Keep the author's ordering and flag any section where the outline does not contain enough to write from.",
        "write-examples": "Write two concrete examples for the concept below: one showing the common case and one showing the edge case people actually hit. Use realistic names and numbers rather than foo and bar.",
    },
    "structure": {
        "restructure-document": "Propose a new structure for the document below, as a list of headings in order, with one line each saying what belongs there. Do not rewrite the prose; propose the shape and wait.",
        "list-or-table": "Read the document below and identify every place where prose is doing a list's or a table's job. For each, say which element it should be, and why that one.",
        "add-summary": "Write a summary of no more than three sentences for the document below, aimed at a reader who will not read the rest. State the conclusion, not the topic.",
        "split-document": "This document appears to serve two readers. Propose how to split it into two documents, naming each, saying who it is for, and listing which existing sections go where.",
    },
    "editing": {
        "tighten-prose": "Tighten the passage below without changing its meaning or removing a fact. Aim for a third fewer words, and show the result only.",
        "cut-hedging": "Find every hedge, qualifier, and filler opener in the passage below and rewrite each sentence to say what is true with the single qualifier the fact deserves. List what you removed.",
        "line-edit": "Line-edit the passage below for clarity and rhythm, keeping the author's voice and every technical detail intact. Return the edit, then a short list of the changes that were judgement calls rather than corrections.",
        "explain-the-edit": "For each change you would make to the passage below, give the sentence, the change, and the rule or reason behind it. Do not apply the changes yet.",
    },
    "voice": {
        "match-voice": "Rewrite the passage below so it sounds like a capable colleague explaining something they know well: clear, direct, concrete, and human. Keep every fact, and do not make it chattier than the subject deserves.",
        "adjust-tone": "Adjust the tone of the passage below for the situation named, moving only how much room the reader is given. Do not relax grammar, terminology, or structure.",
        "remove-marketing": "Strip the unsupported claims and superlatives from the passage below, replacing each with the specific thing that made someone want to make the claim. Where no specific thing exists, cut the sentence and say so.",
        "write-bad-news": "Write the opening two paragraphs of a message delivering the bad news below. Say the hard thing in the first sentence, then explain, and do not apologise more than once.",
    },
    "terminology": {
        "check-terms": "Check the document below against the lexicon and list every term used in a form the lexicon does not sanction, with the line and the canonical form. Do not change the file.",
        "propose-term": "Propose a lexicon entry for the concept below: the canonical form, the spellings to avoid, the kind, and one sentence of rationale. Note any existing entry it would conflict with.",
        "expand-acronyms": "List every acronym in the document below, with the line where it first appears and whether it is expanded there. Give the expansion you would use for the ones that are not.",
        "align-vocabulary": "Read the document below and find every concept that is given more than one name. For each, say which name to keep and where the others appear.",
    },
    "accessibility": {
        "write-alt-text": "Write alt text for each image in the document below, describing what the image tells the reader rather than what it depicts. Keep each under 125 characters.",
        "check-colour-dependence": "Find everywhere in the material below where meaning is carried by colour alone, and say what second signal to add in each case.",
        "plain-language-pass": "Rewrite the passage below for a reader who is tired, interrupted, and reading on a phone. Shorten sentences, cut jargon, and keep every fact.",
        "check-link-text": "List every link in the document below whose text would be meaningless read out of context, and give replacement text that names the destination.",
    },
    "localisation": {
        "prepare-for-translation": "Flag everything in the document below that will translate badly: idioms, culture-specific examples, puns, and units or dates in a local format. Suggest a neutral alternative for each.",
        "check-translation-drift": "Compare the translated document below against its source and list every place where a fact, a number, or an instruction differs. Report differences only; do not correct them yet.",
        "localise-examples": "Rewrite the examples in the document below for the market named, keeping the same teaching point. Change names, currencies, and formats, and nothing else.",
        "write-source-note": "Write the front matter note recording which document this translation came from and the version it was translated at, so later drift is visible.",
    },
    "review": {
        "review-against-checklist": "Review the document below against the Review profile and report each item as met or not met, with the evidence. Do not edit the document.",
        "second-reader": "Read the document below as its declared audience and list the three places you would stop, be confused, or leave. Quote the sentence in each case.",
        "challenge-the-argument": "State the strongest case against the argument in the document below, in three points. Then say which one the document must answer before it is published.",
        "summarise-review-comments": "Group the review comments below into decisions to make, edits to apply, and questions to ask the author. Keep each item to one line.",
    },
    "publication": {
        "write-metadata": "Write the title, one-sentence summary, and channel description for the document below, so all three say the same thing. Keep the title under 60 characters.",
        "prepare-announcement": "Draft an announcement of the change below: what changed, who is affected, what they must do, and by when. Four short paragraphs at most.",
        "adapt-for-channel": "Adapt the document below for the channel named, meeting that channel's requirements. Say which requirements forced a change, and what you cut.",
        "publication-checklist": "List what remains before this document can move to published: approvals, review date, supersession, discoverability, and metadata. Mark each done or outstanding.",
    },
    "maintenance": {
        "audit-freshness": "List the documents below whose review date has passed or is within a month, with their owner and kind. Order by how much a reader would be misled by the staleness.",
        "propose-retirement": "This document may no longer be true. Propose a plan for retiring or superseding it: what replaces it, what links must move, and what the changelog entry should say. Do not remove anything yet.",
        "find-duplication": "Find every fact stated in more than one of the documents below. For each, propose which document should own it and where the others should link instead.",
        "refresh-document": "Update the document below against the source of truth provided, changing only what is now wrong. List each change with the old and new value.",
    },
    "measurement": {
        "define-success": "Define what success looks like for the piece below, in measures we can actually collect. Name the measure, the current value if known, and the value that would mean it worked.",
        "read-feedback": "Group the reader feedback below into problems with the writing, problems with the product, and requests for something else. Rank each group by how many readers it affects.",
        "spot-content-gaps": "Given the questions readers keep asking below, list the documents that should exist and do not. For each, name the kind, the audience, and the one question it answers.",
        "report-editorial-health": "Write a short status report on the content set below: how much is fresh, how much is past review, how much has no owner. Lead with the number that should worry us most.",
    },
    "agents": {
        "brief-an-agent": "Write the instructions an AI assistant needs to draft the piece below: the standards it must follow, the terminology file to read, the shape to produce, and what it must not decide on its own.",
        "review-agent-output": "Review the drafted text below as an editor: check the claims against sources, check the terms against the lexicon, and list anything that reads as generated rather than written.",
        "constrain-an-agent": "Write the constraints for an agent working in this repository: what it may change, what it must propose before changing, and which files are generated and therefore off limits.",
        "write-handoff": "Write a handoff note for whoever picks this workstream up next: what is done, what is in flight, what is blocked and on whom, and where the drafts live. Ten lines at most.",
    },
}


def main() -> None:
    written = 0
    for stage, prompts in PROMPTS.items():
        directory = ROOT / stage
        directory.mkdir(parents=True, exist_ok=True)
        for slug, text in prompts.items():
            (directory / f"request-{slug}.txt").write_text(text.strip() + "\n", encoding="utf-8")
            written += 1
    print(f"wrote {written} prompts across {len(PROMPTS)} stages into {ROOT}")


if __name__ == "__main__":
    main()
