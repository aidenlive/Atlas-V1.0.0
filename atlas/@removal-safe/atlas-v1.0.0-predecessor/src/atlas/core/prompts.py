"""The prompt library (``library/prompts/``, governed by LIBRARY).

A prompt is one to three sentences, single-objective, tool-agnostic, and
safe-by-wording for anything destructive. The catalog in ``index.yaml`` is
machine-readable and must agree with the files on disk in *both* directions —
an entry with no file is a broken link, and a file with no entry is an asset
nobody can discover, which is the failure mode a library exists to prevent.
"""

from __future__ import annotations

import dataclasses
import pathlib
import typing as t

from ..errors import NotFoundError
from ..paths import Repository
from .manifest import Violation, load_yaml

__all__ = ["Prompt", "Category", "Catalog", "load", "validate", "search"]

#: A prompt that runs past this is doing more than one thing (L-04).
MAX_SENTENCES = 3
MAX_WORDS = 90


@dataclasses.dataclass(frozen=True)
class Prompt:
    id: str
    file: str
    objective: str
    category: str
    text: str

    @property
    def stem(self) -> str:
        return pathlib.Path(self.file).stem

    @property
    def words(self) -> int:
        return len(self.text.split())

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "id": self.id,
            "category": self.category,
            "file": self.file,
            "objective": self.objective,
            "words": self.words,
        }


@dataclasses.dataclass(frozen=True)
class Category:
    name: str
    description: str
    prompts: list[Prompt]


@dataclasses.dataclass(frozen=True)
class Catalog:
    categories: list[Category]

    @property
    def prompts(self) -> list[Prompt]:
        return [p for c in self.categories for p in c.prompts]

    def category(self, name: str) -> Category:
        for category in self.categories:
            if category.name == name.lower():
                return category
        known = ", ".join(c.name for c in self.categories)
        raise NotFoundError(f"no prompt category {name!r}", hint=f"Categories: {known}")

    def get(self, identifier: str) -> Prompt:
        """Resolve by id, filename stem, or ``category/id``."""
        wanted = identifier.strip().lower().removesuffix(".txt")
        if "/" in wanted:
            category, _, wanted = wanted.partition("/")
            pool = self.category(category).prompts
        else:
            pool = self.prompts
        for prompt in pool:
            if wanted in {prompt.id.lower(), prompt.stem.lower(), f"request-{prompt.id}".lower()}:
                return prompt
        raise NotFoundError(
            f"no prompt {identifier!r}",
            hint="List them with `atlas prompt list`, or search with `atlas prompt search <term>`.",
        )


def load(repo: Repository) -> Catalog:
    """Read the catalog and the prompt bodies it points at."""
    index_path = repo.prompts / "index.yaml"
    if not index_path.exists():
        raise NotFoundError(
            f"no prompt catalog at {repo.rel(index_path)}",
            hint="A repository adopting LIBRARY ships library/prompts/index.yaml.",
        )
    index = load_yaml(index_path) or {}
    categories: list[Category] = []
    for raw in index.get("categories") or []:
        name = str(raw.get("name", ""))
        prompts: list[Prompt] = []
        for entry in raw.get("prompts") or []:
            path = repo.prompts / entry["file"]
            prompts.append(
                Prompt(
                    id=str(entry.get("id", "")),
                    file=str(entry.get("file", "")),
                    objective=str(entry.get("objective", "")),
                    category=name,
                    text=path.read_text(encoding="utf-8").strip() if path.exists() else "",
                )
            )
        categories.append(Category(name, str(raw.get("description", "")), prompts))
    return Catalog(categories)


def search(catalog: Catalog, term: str) -> list[Prompt]:
    """Substring match across id, objective, category, and body."""
    needle = term.lower()
    return [
        prompt
        for prompt in catalog.prompts
        if needle in prompt.id.lower()
        or needle in prompt.objective.lower()
        or needle in prompt.category.lower()
        or needle in prompt.text.lower()
    ]


def validate(repo: Repository) -> list[Violation]:
    """Catalog and disk agree, and every prompt obeys the LIBRARY contract."""
    index_path = repo.prompts / "index.yaml"
    if not index_path.exists():
        return [Violation("library/prompts/index.yaml", "missing prompt catalog", "LIBRARY L-A2")]

    violations: list[Violation] = []
    catalog = load(repo)
    listed: set[str] = set()
    seen_ids: dict[str, str] = {}

    for category in catalog.categories:
        if not category.description:
            violations.append(
                Violation(f"library/prompts/{category.name}", "category has no description", "LIBRARY L-08")
            )
        for prompt in category.prompts:
            rel = f"library/prompts/{prompt.file}"
            listed.add(prompt.file)
            path = repo.prompts / prompt.file
            if not path.exists():
                violations.append(Violation(rel, "catalog entry has no file", "LIBRARY L-A2"))
                continue
            if not prompt.file.startswith(f"{category.name}/"):
                violations.append(
                    Violation(rel, f"file is not inside its category directory {category.name}/", "LIBRARY L-A3")
                )
            if not pathlib.Path(prompt.file).name.startswith("request-"):
                violations.append(Violation(rel, "prompt filename must begin with `request-`", "LIBRARY L-A3"))
            if prompt.id in seen_ids:
                violations.append(
                    Violation(rel, f"duplicate prompt id {prompt.id!r} (also {seen_ids[prompt.id]})", "LIBRARY L-A2")
                )
            seen_ids[prompt.id] = rel
            if not prompt.objective:
                violations.append(Violation(rel, "catalog entry has no objective", "LIBRARY L-08"))
            if not prompt.text:
                violations.append(Violation(rel, "prompt file is empty", "LIBRARY L-04"))
            elif prompt.words > MAX_WORDS:
                violations.append(
                    Violation(rel, f"{prompt.words} words; prompts stay under {MAX_WORDS}", "LIBRARY L-04")
                )
            sentences = [s for s in prompt.text.replace("\n", " ").split(". ") if s.strip()]
            if len(sentences) > MAX_SENTENCES:
                violations.append(
                    Violation(rel, f"{len(sentences)} sentences; at most {MAX_SENTENCES}", "LIBRARY L-04")
                )

    for path in sorted(repo.prompts.rglob("*.txt")):
        rel_file = path.relative_to(repo.prompts).as_posix()
        if rel_file not in listed:
            violations.append(
                Violation(f"library/prompts/{rel_file}", "file is not listed in index.yaml", "LIBRARY L-A2")
            )
    return violations
