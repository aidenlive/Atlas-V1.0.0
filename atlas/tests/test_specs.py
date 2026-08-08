"""The standards are readable as data, and their rules are well formed."""

from __future__ import annotations

import pytest

from atlas.core import specs as specs_mod

EXPECTED = ["voice", "language", "structure", "content", "matrix", "checklist", "authority", "publication"]


def test_eight_standards_in_declared_order(repo):
    assert [spec.id for spec in specs_mod.load_specs(repo.spec_dir)] == EXPECTED


@pytest.mark.parametrize("field", specs_mod.REQUIRED_META)
def test_every_standard_declares_required_metadata(repo, field):
    for spec in specs_mod.load_specs(repo.spec_dir):
        assert spec.meta.get(field), f"{spec.id} is missing {field}"


def test_rules_are_gapless_and_prefixed(repo):
    for spec in specs_mod.load_specs(repo.spec_dir):
        numbers = [int(rule.id.split("-")[1]) for rule in spec.rules]
        assert numbers == list(range(1, len(numbers) + 1)), spec.id
        assert all(rule.id.startswith(spec.rule_prefix) for rule in spec.rules)


def test_rule_ids_are_unique_across_the_suite(repo):
    ids = [rule.id for rule in specs_mod.all_rules(repo.spec_dir)]
    assert len(ids) == len(set(ids))


def test_every_rule_has_a_title_and_a_requirement(repo):
    for rule in specs_mod.all_rules(repo.spec_dir):
        assert rule.title.strip()
        assert len(rule.text.split()) >= 5, rule.id


def test_companions_exist(repo):
    known = {spec.id for spec in specs_mod.load_specs(repo.spec_dir)}
    for spec in specs_mod.load_specs(repo.spec_dir):
        assert set(spec.companions) <= known, spec.id


def test_find_spec_is_forgiving(repo):
    assert specs_mod.find_spec(repo.spec_dir, "VOICE").id == "voice"
    assert specs_mod.find_spec(repo.spec_dir, "voice.md").id == "voice"
