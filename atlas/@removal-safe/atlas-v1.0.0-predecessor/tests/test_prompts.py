"""LIBRARY contract tests (L-02, L-07, L-08)."""
import pathlib
import re

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "library" / "prompts"
INDEX = yaml.safe_load((P / "index.yaml").read_text())

CATEGORIES = {
    "workspace", "repository", "architecture", "documentation", "github",
    "administration", "quality", "security", "releases", "maintenance",
    "design", "agents", "operations", "workstreams",
}


def _files_on_disk():
    return {str(f.relative_to(P)) for f in P.glob("*/request-*.txt")}


def _files_in_index():
    return {p["file"] for c in INDEX["categories"] for p in c["prompts"]}


def test_categories_are_the_closed_set():
    assert {c["name"] for c in INDEX["categories"]} == CATEGORIES
    on_disk = {d.name for d in P.iterdir() if d.is_dir()}
    assert on_disk == CATEGORIES


def test_index_and_files_mutually_complete():
    """L-08: an unindexed prompt is invisible; an indexed ghost is a lie."""
    assert _files_on_disk() == _files_in_index()


def test_naming_convention():
    """L-07: request-<verb>-<object>.txt, lowercase kebab-case."""
    pat = re.compile(r"^request-[a-z0-9]+(-[a-z0-9]+)+\.txt$")
    for f in P.glob("*/*.txt"):
        assert pat.match(f.name), f"non-compliant prompt name: {f}"


def test_prompt_length_and_shape():
    """L-02: 1-3 sentences, concise; non-empty; ends with a period."""
    for f in P.glob("*/request-*.txt"):
        text = f.read_text().strip()
        assert text, f"empty prompt: {f}"
        assert len(text) <= 600, f"prompt exceeds concision budget: {f} ({len(text)} chars)"
        assert text.endswith("."), f"prompt must end with a period: {f}"
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text.replace("\n", " "))
        assert 1 <= len(sentences) <= 3, f"{f}: {len(sentences)} sentences (L-02 allows 1-3)"


def test_tool_agnostic():
    """L-03: no vendor tool names inside prompt bodies."""
    banned = re.compile(r"\b(cursor|copilot|codex|gemini|claude code|chatgpt|windsurf)\b", re.I)
    for f in P.glob("*/request-*.txt"):
        assert not banned.search(f.read_text()), f"vendor reference in {f}"


def test_index_objectives_are_short():
    for c in INDEX["categories"]:
        for p in c["prompts"]:
            assert len(p["objective"]) <= 120, f"objective too long: {p['id']}"
