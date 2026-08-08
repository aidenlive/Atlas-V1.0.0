"""The prose linter: each rule fires when it should, and stays quiet otherwise."""

from __future__ import annotations

import pathlib

import pytest

from atlas.core import frontmatter, lexicon as lexicon_mod, lint as lint_mod

CLEAN = """---
title: A clean document
kind: guide
owner: role:editorial-lead
status: draft
updated: 2026-08-08
---

# A clean document

This document is short, declares itself, and has one title.

## A section

It links to the [install guide](install.md) by name.
"""


@pytest.fixture(scope="module")
def lex(repo):
    return lexicon_mod.load_lexicon(repo.lexicon_path)


def check(text: str, lex, **kw) -> list[lint_mod.Finding]:
    document = frontmatter.parse(text, pathlib.Path("sample.md"))
    return lint_mod.lint_document(document, lex, **kw).findings


def rules_fired(findings) -> set[str]:
    return {finding.check for finding in findings}


def test_a_clean_document_is_clean(lex):
    assert check(CLEAN, lex) == []


def test_missing_front_matter(lex):
    findings = check("# Title\n\nBody.\n", lex)
    assert "declaration" in rules_fired(findings)


def test_missing_required_field(lex):
    text = CLEAN.replace("owner: role:editorial-lead\n", "")
    assert any("owner" in f.message for f in check(text, lex))


def test_second_h1(lex):
    assert "title" in rules_fired(check(CLEAN + "\n# Another title\n", lex))


def test_h1_inside_a_code_fence_is_not_a_title(lex):
    text = CLEAN + "\n```bash\n# a shell comment\necho hi\n```\n"
    assert "title" not in rules_fired(check(text, lex))


def test_heading_jump(lex):
    assert "headings" in rules_fired(check(CLEAN + "\n#### Too deep\n", lex))


def test_long_sentence_is_a_warning_not_an_error(lex):
    sentence = "word " * 50
    findings = check(CLEAN + f"\n{sentence.strip()}.\n", lex)
    sentence_findings = [f for f in findings if f.check == "sentence-length"]
    assert sentence_findings and all(f.severity == "warn" for f in sentence_findings)


def test_terminology_is_checked_against_the_lexicon(lex):
    findings = check(CLEAN + "\nWe host it on Github.\n", lex)
    assert "terminology" in rules_fired(findings)


def test_canonical_spelling_passes(lex):
    assert "terminology" not in rules_fired(check(CLEAN + "\nWe host it on GitHub.\n", lex))


def test_inline_code_is_exempt_from_terminology(lex):
    assert "terminology" not in rules_fired(check(CLEAN + "\nRun `atlas check` now.\n", lex))


def test_phrasing(lex):
    assert "phrasing" in rules_fired(check(CLEAN + "\nWe utilize it in order to win.\n", lex))


def test_empty_link_text(lex):
    findings = check(CLEAN + "\nRead more [here](install.md).\n", lex)
    assert "links" in rules_fired(findings)


def test_only_and_skip_select_rules(lex):
    text = "# No front matter\n\nWe utilize things.\n"
    assert rules_fired(check(text, lex, only=["declaration"])) == {"declaration"}
    assert "declaration" not in rules_fired(check(text, lex, skip=["declaration"]))


def test_unknown_rule_is_an_error(lex):
    from atlas.errors import NotFoundError

    with pytest.raises(NotFoundError):
        check(CLEAN, lex, only=["no-such-rule"])


def test_settings_come_from_the_manifest():
    settings = lint_mod.Settings.from_manifest({"lint": {"max_sentence_words": 12}})
    assert settings.max_sentence_words == 12
    assert settings.max_paragraph_sentences == lint_mod.Settings.max_paragraph_sentences


def test_findings_carry_editor_line_numbers(lex):
    findings = check(CLEAN + "\nWe utilize things.\n", lex, only=["phrasing"])
    assert findings and findings[0].line > 8


def test_the_same_word_is_reported_once(lex):
    """`avoid: [Github, GITHUB]` is one decision, so it is one finding."""
    findings = check(CLEAN + "\nWe use Github daily.\n", lex, only=["terminology"])
    assert len(findings) == 1
