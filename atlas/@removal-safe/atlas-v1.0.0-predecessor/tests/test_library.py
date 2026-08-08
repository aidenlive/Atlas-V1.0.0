"""LIBRARY conformance: every asset indexed, every index entry backed by a file.

L-A2 says an asset absent from its index does not exist, and an index entry with
no file is a broken build. Both directions are checked here, for every class, so
the claim is enforced rather than asserted.
"""
import pathlib

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / "library"
CLASSES = ["prompts", "icons", "typefaces", "media"]
# prompts carries a generated, category-shaped index; the other three are flat.
FLAT = ["icons", "typefaces", "media"]


def test_the_class_set_is_closed():
    """A fifth class is added by amending the spec, not by creating a folder."""
    found = sorted(d.name for d in LIB.iterdir() if d.is_dir())
    assert found == sorted(CLASSES), f"unregistered library class: {set(found) ^ set(CLASSES)}"


@pytest.mark.parametrize("cls", CLASSES)
def test_every_class_has_an_index_and_a_readme(cls):
    assert (LIB / cls / "index.yaml").exists(), f"{cls} has no index (L-A2)"
    assert (LIB / cls / "README.md").exists(), f"{cls} has no README"


@pytest.mark.parametrize("cls", FLAT)
def test_index_entries_resolve_to_files(cls):
    index = yaml.safe_load((LIB / cls / "index.yaml").read_text()) or {}
    for entry in index.get("assets") or []:
        assert (LIB / cls / entry["file"]).exists(), \
            f"{cls}/index.yaml lists {entry['file']!r}, which does not exist"


@pytest.mark.parametrize("cls", FLAT)
def test_every_file_is_indexed(cls):
    index = yaml.safe_load((LIB / cls / "index.yaml").read_text()) or {}
    listed = {e["file"].rstrip("/") for e in (index.get("assets") or [])}
    on_disk = {p.name for p in (LIB / cls).iterdir()
               if p.name not in {"index.yaml", "README.md"}}
    assert on_disk <= listed, f"{cls}: unindexed assets {sorted(on_disk - listed)} (L-A2)"


@pytest.mark.parametrize("cls", FLAT)
def test_entries_carry_provenance_and_licence(cls):
    """L-A4 and L-A5: derived says from what, foreign says under what license."""
    index = yaml.safe_load((LIB / cls / "index.yaml").read_text()) or {}
    for entry in index.get("assets") or []:
        for field in ("id", "description", "source", "license"):
            assert field in entry, f"{cls}/{entry.get('id', '?')} missing {field!r}"


@pytest.mark.parametrize("cls", FLAT)
def test_asset_ids_are_kebab_case(cls):
    import re
    index = yaml.safe_load((LIB / cls / "index.yaml").read_text()) or {}
    for entry in index.get("assets") or []:
        assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", entry["id"]), \
            f"{cls}: {entry['id']!r} is not kebab-case (L-A3)"


def test_typeface_families_ship_their_licence():
    """L-T1: no license, no typeface."""
    index = yaml.safe_load((LIB / "typefaces" / "index.yaml").read_text()) or {}
    for entry in index.get("assets") or []:
        assert entry.get("license"), f"typeface {entry['id']} declares no license"
        assert entry.get("fallback"), f"typeface {entry['id']} declares no fallback stack (L-T3)"
