"""The lexicon loads, and it does not contradict itself."""

from __future__ import annotations

from atlas.core import compliance, lexicon as lexicon_mod


def test_lexicon_loads(repo):
    lex = lexicon_mod.load_lexicon(repo.lexicon_path)
    assert lex.terms and lex.phrases


def test_every_phrase_has_a_replacement(repo):
    lex = lexicon_mod.load_lexicon(repo.lexicon_path)
    assert all(phrase.use for phrase in lex.phrases)


def test_severities_are_known(repo):
    lex = lexicon_mod.load_lexicon(repo.lexicon_path)
    for entry in (*lex.terms, *lex.phrases):
        assert entry.severity in lexicon_mod.SEVERITIES


def test_no_term_forbids_its_own_canonical_form(repo):
    lex = lexicon_mod.load_lexicon(repo.lexicon_path)
    for term in lex.terms:
        assert term.use not in term.avoid


def test_find_is_case_insensitive(repo):
    lex = lexicon_mod.load_lexicon(repo.lexicon_path)
    assert lex.find("GITHUB")


def test_a_missing_lexicon_is_not_an_error(tmp_path):
    lex = lexicon_mod.load_lexicon(tmp_path / "nope.yaml")
    assert lex.terms == () and lex.phrases == ()


def test_the_gate_agrees(repo):
    assert compliance.run(repo, only=["lexicon-consistent"]).ok
