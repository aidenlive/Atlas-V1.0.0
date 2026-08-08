"""The site generator: rendering, highlighting, theming, search, and the build.

The site is derived output, so these tests check the *derivation* — that the
Markdown this repository writes renders correctly, that nothing escapes as raw
HTML that should not, and that the build produces the files the deploy expects.
"""

from __future__ import annotations

import json
import pathlib

import pytest

import yaml

from atlas.core import tokens as tokens_mod
from atlas.paths import Repository
from atlas.site import build
from atlas.site.highlight import LANGUAGES, highlight, language_label
from atlas.site.markdown import render, slugify
from atlas.site.search import Index
from atlas.site.theme import STYLESHEET

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = Repository(ROOT)


# ------------------------------------------------------------------- markdown

def test_headings_get_stable_slugs_and_anchors():
    doc = render("## The two axes\n")
    assert 'id="the-two-axes"' in doc.html
    assert 'class="heading-anchor"' in doc.html
    assert doc.headings[0].slug == "the-two-axes"


def test_duplicate_headings_get_distinct_slugs():
    """Two identical headings must not both own the same anchor."""
    doc = render("## Notes\n\ntext\n\n## Notes\n")
    slugs = [h.slug for h in doc.headings]
    assert len(set(slugs)) == len(slugs)


def test_first_h1_is_not_rendered_twice():
    """The page shell draws the title; emitting it again showed it at two sizes."""
    doc = render("# Title\n\nBody.\n")
    assert "<h1" not in doc.html
    assert 'class="anchor-only"' in doc.html


def test_code_spans_are_not_reinterpreted():
    """A backticked `**literal**` must stay literal, not become bold."""
    doc = render("Use `**kwargs` carefully.\n")
    assert "<strong>" not in doc.html
    assert "**kwargs" in doc.html


def test_raw_html_blocks_pass_through_unescaped():
    """The previous build escaped these and un-escaped them again afterwards."""
    doc = render('<div class="cards"><a class="card">x</a></div>\n')
    assert '<div class="cards">' in doc.html
    assert "&lt;div" not in doc.html


def test_status_words_in_tables_become_pills_with_a_glyph():
    """Color is never the only channel: a pill carries its word and a glyph."""
    doc = render("| Status |\n|---|\n| blocked |\n")
    assert 'class="pill pill-blocked"' in doc.html
    assert 'class="pill-glyph"' in doc.html
    assert "blocked" in doc.html


def test_progress_cells_become_bars_with_an_accessible_label():
    doc = render("| Progress |\n|---|\n| `████··` 4/6 |\n")
    assert 'class="progress"' in doc.html
    assert 'aria-label="4 of 6 complete"' in doc.html


def test_tables_own_their_scroll_container():
    """No horizontal page scroll: every wide child scrolls itself."""
    doc = render("| A | B |\n|---|---|\n| 1 | 2 |\n")
    assert 'class="scroller"' in doc.html
    assert 'role="region"' in doc.html


def test_callouts_map_to_tones():
    doc = render("> [!WARNING]\n> Mind the gap.\n")
    assert "callout-warning" in doc.html
    assert "Mind the gap." in doc.html


def test_caution_callouts_are_announced():
    doc = render("> [!CAUTION]\n> This deletes things.\n")
    assert 'role="alert"' in doc.html


def test_nested_lists_nest():
    doc = render("- one\n  - inner\n- two\n")
    assert doc.html.count("<ul>") == 2


def test_task_lists_render_as_checkboxes():
    doc = render("- [x] done\n- [ ] pending\n")
    assert "is-checked" in doc.html
    assert "is-unchecked" in doc.html


def test_markdown_links_are_rewritten_to_built_paths():
    doc = render("See [the spec](workstream.md) and [the work](work/README.md).\n")
    assert 'href="workstream.html"' in doc.html
    assert 'href="work/index.html"' in doc.html


def test_external_links_are_left_alone():
    doc = render("[home](https://example.com/a?b=c)\n")
    assert 'href="https://example.com/a?b=c"' in doc.html


def test_rule_identifiers_become_anchors_when_requested():
    doc = render("The rule W-13 applies.\n", link_rules=True)
    assert 'id="rule-W-13"' in doc.html
    doc_plain = render("The rule W-13 applies.\n")
    assert "rule-W-13" not in doc_plain.html


def test_plain_text_is_extracted_for_the_search_index():
    doc = render("# Title\n\nSome searchable prose.\n")
    assert "searchable prose" in doc.text
    assert "<p>" not in doc.text


@pytest.mark.parametrize("text,expected", [
    ("The Two Axes", "the-two-axes"),
    ("`code` heading", "code-heading"),
    ("!!!", "section"),
])
def test_slugify(text, expected):
    assert slugify(text) == expected


# ------------------------------------------------------------------ highlight

@pytest.mark.parametrize("lang", LANGUAGES)
def test_every_language_highlights_without_raising(lang):
    assert isinstance(highlight("x = 1 # comment\n", lang), str)


def test_unknown_languages_escape_rather_than_guess():
    """A wrong highlight asserts structure that is not there."""
    out = highlight("<script>alert(1)</script>", "brainfuck")
    assert "<span" not in out
    assert "&lt;script&gt;" in out


def test_highlighting_escapes_html():
    out = highlight('x = "<b>"', "python")
    assert "&lt;b&gt;" in out
    assert "<b>" not in out


def test_aliases_resolve():
    assert language_label("sh") == "shell"
    assert language_label("yml") == "YAML"
    assert highlight("# hi", "py") == highlight("# hi", "python")


def test_comments_and_strings_are_distinguished():
    out = highlight('# note\nx = "value"', "python")
    assert 't-c"' in out and 't-s"' in out


# --------------------------------------------------------------------- theme

def test_stylesheet_uses_tokens_not_literal_colors():
    """Re-theming must be a token edit, not a stylesheet hunt."""
    import re

    literals = re.findall(r"#[0-9a-fA-F]{6}\b", STYLESHEET)
    # The only permitted literals are the print-stylesheet fallbacks, where
    # custom properties are unreliable across print engines.
    assert set(literals) <= {"#ffffff", "#fff", "#000", "#555"}, literals


def test_css_variables_emit_both_themes_and_an_explicit_override():
    css = tokens_mod.css_variables(tokens_mod.load(REPO.tokens))
    assert ":root {" in css
    assert "prefers-color-scheme: dark" in css
    assert '[data-theme="dark"]' in css
    assert '[data-theme="light"]' in css


def test_token_aliases_are_resolved():
    css = tokens_mod.css_variables(tokens_mod.load(REPO.tokens))
    assert "{colors." not in css, "an unresolved alias reached the stylesheet"


def test_no_token_alias_is_an_unquoted_yaml_mapping():
    """`{colors.primary}` unquoted is YAML flow-mapping syntax, not a string.

    An unquoted alias parses as `{'colors.primary': None}`, silently fails the
    `isinstance(value, str)` check in the CSS emitter, and the custom property
    is never written. Nothing errors; the token simply does not exist, and
    every rule referencing it falls back. Quote aliases.
    """
    raw = yaml.safe_load(REPO.tokens.read_text(encoding="utf-8"))
    groups = {"colors": raw.get("colors", {}), "dark": (raw.get("themes") or {}).get("dark", {})}
    for group, mapping in groups.items():
        unquoted = [k for k, v in mapping.items() if isinstance(v, dict)]
        assert not unquoted, f"{group}: unquoted alias tokens are dropped: {unquoted}"


def test_colors_are_oklch():
    """The organisation's color standard is OKLCH-only."""
    tokens = tokens_mod.load(REPO.tokens)
    for name, value in tokens["colors"].items():
        resolved = str(tokens_mod.resolve(value, tokens))
        assert resolved.startswith(("oklch(", "transparent", "currentColor")), (name, resolved)


# -------------------------------------------------------------------- search

def test_search_index_serialises_compactly():
    index = Index()
    index.add("a.html", "Title", crumb="Docs", headings=["One"], body="Body text")
    payload = json.loads(index.to_json())
    assert payload[0]["u"] == "a.html"
    assert payload[0]["t"] == "Title"
    assert " " not in index.to_json()[:12]  # no pretty-printing


def test_search_bodies_are_truncated_on_a_word_boundary():
    index = Index()
    index.add("a.html", "T", body="word " * 1000)
    body = json.loads(index.to_json())[0]["b"]
    assert len(body) < 1500
    assert body.endswith("\u2026")


# --------------------------------------------------------------------- build

@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("site")
    return build(REPO, out), out


def test_build_produces_pages(built):
    result, _ = built
    assert result.pages > 100
    assert result.warnings == []


def test_build_emits_the_deploy_contract(built):
    """Files the deploy and the crawlers depend on."""
    _, out = built
    for name in ("index.html", "404.html", "sitemap.xml", "robots.txt",
                 "search-index.json", ".nojekyll", "assets/site.css"):
        assert (out / name).exists(), f"missing {name}"


def test_every_standard_and_document_has_a_page(built):
    _, out = built
    from atlas.core import specs as specs_mod

    for spec in specs_mod.load_specs(REPO.spec):
        assert (out / "spec" / f"{spec.path.stem}.html").exists()
    assert (out / "cli" / "reference.html").exists()
    assert (out / "docs" / "index.html").exists()


def test_search_index_covers_the_pages(built):
    result, out = built
    payload = json.loads((out / "search-index.json").read_text(encoding="utf-8"))
    assert len(payload) == result.indexed
    urls = {entry["u"] for entry in payload}
    assert "spec/workstream.html" in urls


def test_pages_declare_a_language_and_a_description(built):
    _, out = built
    html = (out / "index.html").read_text(encoding="utf-8")
    assert '<html lang="en"' in html
    assert '<meta name="description"' in html


def test_pages_carry_a_skip_link_and_a_main_landmark(built):
    _, out = built
    html = (out / "spec" / "project.html").read_text(encoding="utf-8")
    assert 'class="skip-link"' in html
    assert '<main class="content" id="content">' in html


def test_theme_is_applied_before_first_paint(built):
    """Reading the stored theme after paint flashes the wrong theme every time."""
    _, out = built
    html = (out / "index.html").read_text(encoding="utf-8")
    head = html[: html.index("</head>")]
    assert "atlas-theme" in head


def test_no_unresolved_template_placeholders_in_output(built):
    """A scaffold placeholder must never reach a rendered page.

    Quoted placeholders inside code are legitimate — the install guide explains
    what `{{PROJECT_NAME}}` is — so the check ignores code elements and looks
    only at prose, which is where an unsubstituted token would actually be a bug.
    """
    import re

    code = re.compile(r"<code>.*?</code>|<pre.*?</pre>", re.S)
    for page in out_pages(built):
        prose = code.sub("", page.read_text(encoding="utf-8"))
        assert "{{" not in prose, f"{page.name} has an unsubstituted placeholder"


def test_page_heads_are_fully_populated(built):
    """A `None` in the head means a metadata field was rendered before it was set."""
    for page in out_pages(built):
        head = page.read_text(encoding="utf-8").split("<body")[0]
        assert ">None<" not in head and 'content="None"' not in head, page.name


def out_pages(built):
    _, out = built
    return sorted(out.rglob("*.html"))


# ---------------------------------------------------------- content accents

def test_every_content_domain_has_a_complete_accent_set():
    """A domain with a partial accent set falls back mid-component.

    `--accent` without `--accent-soft` gives a tag saturated text on an
    untinted ground, which looks like a rendering bug rather than a decision.
    """
    from atlas.site.builder import DOMAINS

    tokens = tokens_mod.load(REPO.tokens)
    colors = tokens["colors"]
    for _, domain in DOMAINS:
        for suffix in ("", "-soft", "-line"):
            key = f"accent-{domain}{suffix}"
            assert key in colors, f"missing token {key}"


def test_accents_are_defined_for_both_themes():
    """A light-only accent becomes an unreadable chip on a dark page."""
    tokens = tokens_mod.load(REPO.tokens)
    dark = (tokens.get("themes") or {}).get("dark", {})
    from atlas.site.builder import DOMAINS

    for _, domain in DOMAINS:
        assert f"accent-{domain}" in dark, f"{domain} has no dark-theme accent"


def test_navigation_carries_no_decorative_hue():
    """Structure stays achromatic; hue belongs where it carries information.

    An earlier sidebar tinted each group's rail and dotted every label. With
    five groups on screen it read as a legend for a chart that was not there.
    """
    assert "series-" not in STYLESHEET, "a data-series color is styling navigation"
    assert "nth-of-type" not in STYLESHEET, "navigation is assigning hue by position"


def test_status_marks_appear_on_exception_only(built):
    """A dot beside every item buries the one that needs attention."""
    _, out = built
    html = (out / "spec" / "project.html").read_text(encoding="utf-8")
    sidebar = html[html.index('<aside class="sidebar"'):html.index("</aside>")]
    for healthy in ("is-done", "is-active", "is-planned"):
        assert healthy not in sidebar, f"navigation marks the healthy state {healthy}"
