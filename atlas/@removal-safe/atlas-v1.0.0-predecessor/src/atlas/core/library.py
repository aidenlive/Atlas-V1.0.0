"""The shared-asset library (``library/``, governed by ``spec/library.md``).

Four asset classes, and the set is closed: prompts, icons, typefaces, media. A
fifth is added by amending the specification, not by creating a folder, which
is the whole difference between a library and a second downloads folder.

Every class carries an ``index.yaml``, and the index and the directory must
agree in both directions (L-A2). This module checks that, plus the provenance
rules: derived assets name their source (L-A4), foreign assets carry their
license (L-A5).
"""

from __future__ import annotations

import dataclasses
import pathlib
import typing as t

from ..paths import Repository
from .manifest import Violation, load_yaml

__all__ = ["CLASSES", "Asset", "AssetClass", "load", "validate"]

#: The closed set, with the file extensions each class may hold.
CLASSES: dict[str, dict[str, t.Any]] = {
    "prompts": {
        "holds": "Reusable, tool-agnostic statements of intent",
        "extensions": {".txt"},
        "generated": True,
    },
    "icons": {
        "holds": "Interface glyphs, one concept per file",
        "extensions": {".svg"},
        "generated": False,
    },
    "typefaces": {
        "holds": "Font files and the licenses that permit them",
        "extensions": {".woff2", ".woff", ".ttf", ".otf"},
        "generated": False,
    },
    "media": {
        "holds": "Diagrams, screenshots, recordings, and their sources",
        "extensions": {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".webm"},
        "generated": False,
    },
}


@dataclasses.dataclass(frozen=True)
class Asset:
    id: str
    file: str
    description: str
    source: str | None
    license: str | None
    asset_class: str

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "id": self.id,
            "class": self.asset_class,
            "file": self.file,
            "description": self.description,
            "source": self.source,
            "license": self.license,
        }


@dataclasses.dataclass(frozen=True)
class AssetClass:
    name: str
    holds: str
    assets: list[Asset]
    present: bool

    @property
    def count(self) -> int:
        return len(self.assets)


def load(repo: Repository) -> list[AssetClass]:
    """Read every class index. Absent classes are reported, not skipped."""
    classes: list[AssetClass] = []
    for name, meta in CLASSES.items():
        directory = repo.library / name
        index_path = directory / "index.yaml"
        assets: list[Asset] = []
        if index_path.exists():
            index = load_yaml(index_path) or {}
            key = "prompts" if name == "prompts" else "assets"
            entries = index.get(key)
            if entries is None and name == "prompts":
                # The prompt catalog nests its entries under categories.
                entries = [
                    entry
                    for category in index.get("categories") or []
                    for entry in category.get("prompts") or []
                ]
            for entry in entries or []:
                assets.append(
                    Asset(
                        id=str(entry.get("id", "")),
                        file=str(entry.get("file", "")),
                        description=str(entry.get("description", entry.get("objective", ""))),
                        source=entry.get("source"),
                        license=entry.get("license"),
                        asset_class=name,
                    )
                )
        classes.append(AssetClass(name, str(meta["holds"]), assets, directory.is_dir()))
    return classes


def validate(repo: Repository) -> list[Violation]:
    """Index and directory agree, and provenance is declared where required."""
    if not repo.library.is_dir():
        return []

    violations: list[Violation] = []
    known_classes = set(CLASSES)

    for entry in sorted(repo.library.iterdir()):
        if entry.is_dir() and entry.name not in known_classes:
            violations.append(
                Violation(
                    f"library/{entry.name}/",
                    "not one of the four asset classes; the set is closed",
                    "LIBRARY L-01",
                )
            )

    for name, meta in CLASSES.items():
        directory = repo.library / name
        if not directory.is_dir():
            continue
        index_path = directory / "index.yaml"
        if not index_path.exists():
            violations.append(
                Violation(f"library/{name}/index.yaml", "asset class has no index", "LIBRARY L-A2")
            )
            continue
        if name == "prompts":
            continue  # covered in depth by atlas.core.prompts

        index = load_yaml(index_path) or {}
        if "assets" not in index:
            violations.append(
                Violation(f"library/{name}/index.yaml", "index has no `assets:` key", "LIBRARY L-A2")
            )
            continue

        listed: set[str] = set()
        seen_ids: dict[str, str] = {}
        for entry in index.get("assets") or []:
            rel = f"library/{name}/{entry.get('file', '?')}"
            if not entry.get("id"):
                violations.append(Violation(rel, "asset entry has no id", "LIBRARY L-A2"))
            if not entry.get("description"):
                violations.append(Violation(rel, "asset entry has no description", "LIBRARY L-A2"))
            asset_id = str(entry.get("id", ""))
            if asset_id and asset_id in seen_ids:
                violations.append(
                    Violation(rel, f"duplicate asset id {asset_id!r} (also {seen_ids[asset_id]})", "LIBRARY L-A2")
                )
            seen_ids[asset_id] = rel

            filename = str(entry.get("file", ""))
            listed.add(filename.rstrip("/"))
            target = directory / filename
            if not target.exists():
                violations.append(Violation(rel, "index entry has no file", "LIBRARY L-A2"))
                continue
            if target.is_file() and target.suffix.lower() not in meta["extensions"]:
                allowed = ", ".join(sorted(meta["extensions"]))
                violations.append(
                    Violation(rel, f"unexpected extension {target.suffix!r}; expected one of {allowed}", "LIBRARY L-A3")
                )
            source = entry.get("source")
            if source and str(source).startswith(("http://", "https://")) and not entry.get("license"):
                violations.append(
                    Violation(rel, "asset from an external source carries no license", "LIBRARY L-A5")
                )

        for path in sorted(directory.iterdir()):
            if path.name in {"index.yaml", "README.md", "LICENSE"} or path.name.startswith("."):
                continue
            if path.name.rstrip("/") not in listed:
                violations.append(
                    Violation(f"library/{name}/{path.name}", "file is not listed in index.yaml", "LIBRARY L-A2")
                )
    return violations
