"""The prompt library: shape, index, and lookup."""

from __future__ import annotations

import yaml

from atlas.core import prompts as prompts_mod


def test_every_prompt_asks_for_one_thing(repo):
    for prompt in prompts_mod.load_prompts(repo.prompts_dir):
        assert prompt.sentences <= prompts_mod.MAX_SENTENCES, prompt.slug
        assert "\n\n" not in prompt.text, prompt.slug


def test_prompts_cover_the_life_cycle(repo):
    stages = prompts_mod.stages(repo.prompts_dir)
    assert len(stages) >= 12
    assert {"brief", "drafting", "editing", "review", "publication"} <= set(stages)


def test_index_matches_the_files(repo):
    generated = prompts_mod.build_index(repo.prompts_dir)
    on_disk = yaml.safe_load((repo.prompts_dir / "index.yaml").read_text(encoding="utf-8"))
    assert generated["count"] == on_disk["count"]
    assert [s["name"] for s in generated["stages"]] == [s["name"] for s in on_disk["stages"]]


def test_find_prompt_accepts_several_forms(repo):
    assert prompts_mod.find_prompt(repo.prompts_dir, "write-brief").slug == "write-brief"
    assert prompts_mod.find_prompt(repo.prompts_dir, "request-write-brief.txt").slug == "write-brief"


def test_search(repo):
    assert prompts_mod.search_prompts(repo.prompts_dir, "lexicon")
    assert prompts_mod.search_prompts(repo.prompts_dir, "", stage="review")
