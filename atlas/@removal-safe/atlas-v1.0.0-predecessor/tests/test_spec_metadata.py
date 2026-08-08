"""Specification metadata and information-architecture contract.

The v0.0.1 audit found four counts stated in prose that the filesystem
contradicted, and a rule-identifier convention that existed in practice but was
written down nowhere. Both are the same failure: a fact asserted by a human
where nothing compares it to reality. These tests are the comparison.
"""
import pathlib
import re

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPECS = sorted((ROOT / "spec").glob("*.md"))
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)

REQUIRED_FIELDS = {
    "id", "order", "title", "tagline", "question", "version", "status",
    "rule_prefixes", "checklist_prefixes", "companions",
}


def meta(p: pathlib.Path) -> dict:
    m = FRONT_MATTER.match(p.read_text())
    assert m, f"{p.name}: no YAML front matter"
    return yaml.safe_load(m.group(1))


def body(p: pathlib.Path) -> str:
    return FRONT_MATTER.sub("", p.read_text(), count=1)


ALL = {p: meta(p) for p in SPECS}


# --- front matter -----------------------------------------------------------

def test_every_spec_has_complete_front_matter():
    for p, m in ALL.items():
        assert REQUIRED_FIELDS <= set(m), f"{p.name}: missing {REQUIRED_FIELDS - set(m)}"


def test_front_matter_id_matches_filename():
    """The id is the address other documents cite; it cannot drift from the file."""
    for p, m in ALL.items():
        assert m["id"] == p.stem, f"{p.name}: id {m['id']!r}"


def test_order_is_a_complete_sequence():
    """Reading order is declared data, so the sidebar and the site agree."""
    orders = sorted(m["order"] for m in ALL.values())
    assert orders == list(range(1, len(ALL) + 1)), orders


def test_ids_and_titles_are_unique():
    assert len({m["id"] for m in ALL.values()}) == len(ALL)
    assert len({m["title"] for m in ALL.values()}) == len(ALL)


def test_companions_resolve_to_real_specs():
    ids = {m["id"] for m in ALL.values()}
    for p, m in ALL.items():
        for c in m["companions"]:
            assert c in ids, f"{p.name}: companion {c!r} is not a specification"
            assert c != m["id"], f"{p.name}: lists itself as a companion"


def test_status_and_version_are_declared_values():
    for p, m in ALL.items():
        assert m["status"] in {"draft", "stable", "superseded"}, p.name
        assert re.fullmatch(r"\d+\.\d+", str(m["version"])), p.name


# --- heading tree -----------------------------------------------------------

def test_exactly_one_h1_and_it_names_the_standard():
    for p, m in ALL.items():
        fence = False
        h1s = []
        for line in body(p).split("\n"):
            if line.lstrip().startswith("```"):
                fence = not fence
                continue
            if not fence and re.match(r"^# (?!#)", line):
                h1s.append(line)
        assert len(h1s) == 1, f"{p.name}: {len(h1s)} h1 headings, expected 1"
        assert h1s[0].startswith(f"# {m['title']}: "), f"{p.name}: {h1s[0]!r}"


def test_heading_levels_never_skip():
    """An h3 under an h1 is a hole in the outline; screen readers surface it."""
    for p in SPECS:
        fence, prev = False, 0
        for line in body(p).split("\n"):
            if line.lstrip().startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            m = re.match(r"^(#{1,6}) ", line)
            if not m:
                continue
            level = len(m.group(1))
            assert level <= prev + 1, f"{p.name}: h{prev} -> h{level} at {line!r}"
            prev = level


# --- rule identifier registry ----------------------------------------------

REGISTRY = (ROOT / "docs" / "reference" / "rule-ids.md").read_text()


def test_registry_exists_for_every_spec():
    for m in ALL.values():
        assert m["title"] in REGISTRY, f"{m['title']} is absent from rule-ids.md"


def test_declared_prefixes_are_registered():
    """A prefix a spec declares must appear in the registry table."""
    for p, m in ALL.items():
        for prefix in list(m["rule_prefixes"]) + list(m["checklist_prefixes"]):
            assert f"`{prefix}" in REGISTRY or f" {prefix}" in REGISTRY, \
                f"{p.name}: prefix {prefix!r} not registered in rule-ids.md"


def test_rule_prefixes_do_not_collide_across_specs():
    """Two specs owning the same prefix makes every citation ambiguous."""
    seen: dict[str, str] = {}
    for p, m in ALL.items():
        for prefix in list(m["rule_prefixes"]) + list(m["checklist_prefixes"]):
            assert prefix not in seen, \
                f"{prefix!r} claimed by both {seen.get(prefix)} and {p.name}"
            seen[prefix] = p.name


def test_used_prefixes_are_declared():
    """A spec must not use an identifier namespace it has not declared."""
    known = {"D"}  # MATRIX dimensions D1..D8 are addresses, not rules
    for p, m in ALL.items():
        declared = {x.rstrip("-") for x in
                    list(m["rule_prefixes"]) + list(m["checklist_prefixes"])} | known
        used = {x.rstrip("-") for x in
                re.findall(r"\*\*([A-Z]{1,4}(?:-[A-Z])?)-\d{1,2}[.:) ]", body(p))}
        undeclared = used - declared
        assert not undeclared, f"{p.name}: uses undeclared prefixes {sorted(undeclared)}"


# --- the deliberate mirrors -------------------------------------------------

def test_readme_and_quick_reference_list_every_spec():
    """The suite table is mirrored on purpose (P-06); mirrors get tested."""
    readme = (ROOT / "README.md").read_text()
    quickref = (ROOT / "docs" / "reference" / "quick-reference.md").read_text()
    for p, m in ALL.items():
        assert f"spec/{p.name}" in readme, f"{p.name} missing from README"
        assert f"spec/{p.name}" in quickref, f"{p.name} missing from quick-reference"
        assert m["question"] in readme, f"{p.name}: question drifted in README"
        assert m["question"] in quickref, f"{p.name}: question drifted in quick-reference"


def test_no_document_claims_a_wrong_section_count():
    """The 'ten-section skeleton' error appeared in eight files at once."""
    sections = sorted(d.name for d in (ROOT / "work" / "_template").iterdir() if d.is_dir())
    assert len(sections) == 9, sections
    for p in list((ROOT / "docs").rglob("*.md")) + [
        ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "CHANGELOG.md",
        ROOT / "work" / "_template" / "README.md",
    ]:
        text = p.read_text().lower()
        assert "ten-section" not in text and "ten fixed section" not in text \
            and "ten sections" not in text, f"{p}: stale section count"


# --- links ------------------------------------------------------------------

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
LINK_EXEMPT = {ROOT / "spec" / "workstream.md"}  # contains an illustrative table row


def test_relative_links_resolve():
    """A dead link is a documentation defect that no reader reports."""
    broken = []
    for md in ROOT.rglob("*.md"):
        if md.parts[len(ROOT.parts)] in {"site", ".git"} or md in LINK_EXEMPT:
            continue
        for href in LINK.findall(md.read_text()):
            if href.startswith(("http://", "https://", "#", "mailto:")):
                continue
            if not (md.parent / href.split("#")[0]).resolve().exists():
                broken.append(f"{md.relative_to(ROOT)} -> {href}")
    assert not broken, "broken relative links:\n  " + "\n  ".join(sorted(set(broken)))


# --- brand assets -----------------------------------------------------------

ASSET_SETS = [
    (ROOT / "assets", ["banner", "architecture"]),
    (ROOT / "template" / "assets", ["banner"]),
]


def test_every_asset_ships_light_dark_and_default():
    """P-02: a dark-only hero is unreadable for half the audience."""
    for d, names in ASSET_SETS:
        for n in names:
            for suffix in ("-light", "-dark", ""):
                assert (d / f"{n}{suffix}.svg").exists(), f"{d.name}/{n}{suffix}.svg"


def test_assets_are_reproducible_from_the_generator():
    """Hand-editing a generated SVG is how the boxes stopped fitting the text."""
    import subprocess
    import sys
    before = {p: p.read_bytes() for d, ns in ASSET_SETS for n in ns
              for p in d.glob(f"{n}*.svg")}
    r = subprocess.run([sys.executable, "scripts/build_assets.py"],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    drifted = [str(p.relative_to(ROOT)) for p, b in before.items()
               if p.read_bytes() != b]
    assert not drifted, f"hand-edited assets: {drifted}"


# --- design system conformance ----------------------------------------------

DESIGN = ROOT / "assets" / "design" / "DESIGN.md"
TOKENS = ROOT / "assets" / "design" / "tokens.yaml"


def _design_front_matter() -> dict:
    lines = DESIGN.read_text().split("\n")
    end = next(i for i, l in enumerate(lines[1:], 1) if l.strip() == "---")
    return yaml.safe_load("\n".join(lines[1:end]))


def test_tokens_are_the_design_systems_front_matter():
    """tokens.yaml is an extract, not a fork. A hand-edited token is a fork."""
    design = _design_front_matter()
    tokens = yaml.safe_load(TOKENS.read_text())
    assert tokens == design, "tokens.yaml has drifted from DESIGN.md front matter"
    assert str(tokens["version"]) == "1.0", tokens["version"]
    assert tokens["name"] == "Neue"


def test_structural_groups_are_present():
    """The groups the site's layout is built on must exist to be built on."""
    t = yaml.safe_load(TOKENS.read_text())
    for group in ("ramps", "colors", "typography", "spacing", "rounded", "elevation",
                  "motion", "breakpoints", "sizeClasses", "grid", "regions",
                  "adaptation", "overflow", "shells", "themes"):
        assert group in t, f"missing token group: {group}"
    assert "palette" not in t, "`palette` is the alpha name; 1.0 uses `ramps`"


def test_adaptation_ladder_only_runs_one_way():
    """Neue: a region does not become more prominent as space shrinks."""
    t = yaml.safe_load(TOKENS.read_text())
    ladder = ["docked", "inline", "overlay", "sheet", "hidden"]
    classes = list(t["sizeClasses"])          # compact -> xlarge, narrow to wide
    for region, by_class in t["adaptation"].items():
        seen = [ladder.index(by_class[c]) for c in classes if c in by_class]
        assert seen == sorted(seen, reverse=True), \
            f"{region}: adaptation becomes more prominent as space shrinks: {by_class}"


def test_every_region_declares_an_overflow_answer():
    """Declare an answer for every region, including ones you think never overflow."""
    t = yaml.safe_load(TOKENS.read_text())
    answers = {"scroll", "collapse", "wrap", "paginate", "clip"}
    for region in t["regions"]:
        assert region in t["overflow"], f"{region} has no declared overflow answer"
        assert t["overflow"][region] in answers, t["overflow"][region]


def test_site_shell_uses_container_queries_for_structure():
    """The two axes: containers govern structure, viewport governs page chrome."""
    src = (ROOT / "src" / "atlas" / "site" / "theme.py").read_text()
    flat = src.replace(" ", "")
    assert "container:content/inline-size" in flat, "content region is not a container"
    assert "@container content" in src, "no container query drives structure"
    assert "overflow-x:clip" in flat, "missing the no-horizontal-page-scroll net"


def test_size_class_values_are_used_as_thresholds_not_fresh_numbers():
    """A region and the shell around it must agree on what `expanded` means."""
    t = yaml.safe_load(TOKENS.read_text())
    src = (ROOT / "src" / "atlas" / "site" / "theme.py").read_text()
    import re as _re
    used = {int(m) for m in _re.findall(r"@container content \(min-width: ?(\d+)px\)", src)}
    known = {int(str(v).rstrip("px")) for v in t["sizeClasses"].values()}
    assert used <= known, f"container queries use unknown thresholds: {used - known}"
